from decimal import Decimal
import io

import xlsxwriter
from django.http import HttpResponse
from django.shortcuts import render

from administracion_contabilidad.models import Movims, Asientos
from consultas_administrativas.forms import ReporteCobranzasForm, ReportePagosForm
from mantenimientos.models import Clientes


def reporte_pagos(request):
    if request.method == 'POST':
        form = ReportePagosForm(request.POST)
        if form.is_valid():
            fecha_hasta = form.cleaned_data['fecha_hasta']
            fecha_desde = form.cleaned_data['fecha_desde']
            moneda = form.cleaned_data['moneda']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            consolidar_moneda_nac = form.cleaned_data['consolidar_moneda_nac']
            ver_detalle = form.cleaned_data['ver_detalle']
            ver_anuladas = form.cleaned_data['ver_anuladas']

            cobranzas = Movims.objects.filter(
                mtipo=45,
                mmoneda=moneda.codigo,
                mfechamov__range=(fecha_desde, fecha_hasta)
            ).only(
                'mboleta', 'mfechamov', 'mcliente', 'mnombre',
                'mtotal', 'mcambio','mparidad', 'mmoneda', 'mautogen',
                'mdetalle', 'mactivo'
            )

            codigos_clientes = cobranzas.values_list('mcliente', flat=True).distinct()
            autogenerados = cobranzas.values_list('mautogen', flat=True).distinct()

            clientes = Clientes.objects.filter(codigo__in=codigos_clientes).only('codigo', 'empresa', 'ruc')
            asientos = Asientos.objects.filter(
                autogenerado__in=autogenerados,
                fecha__range=(fecha_desde, fecha_hasta)
            ).only('autogenerado', 'cuenta', 'modo', 'banco', 'imputacion')

            # Transformar en diccionarios
            clientes_dict = {c.codigo: c for c in clientes}
            asientos_dict = {}
            for a in asientos:
                asientos_dict.setdefault(a.autogenerado, []).append(a)

            return generar_excel_pagos(
                cobranzas,
                clientes_dict,
                asientos_dict,
                fecha_desde,
                fecha_hasta,
                consolidar_dolares,
                consolidar_moneda_nac,
                moneda,
                ver_detalle,
                ver_anuladas
            )
    else:
        form = ReportePagosForm()

    return render(request, 'compras_ca/reporte_pagos.html', {'form': form})

def generar_excel_pagos(pagos, clientes_dict, asientos_dict, fecha_desde, fecha_hasta,
                             consolidar_dolares, consolidar_moneda_nac, moneda,
                             ver_detalle, ver_anuladas):
    try:
        if consolidar_dolares:
            nombre_moneda = "CONSOLIDADO USD"
            moneda_destino = 2
        elif consolidar_moneda_nac:
            nombre_moneda = "CONSOLIDADO MONEDA NACIONAL"
            moneda_destino = 1
        else:
            nombre_moneda = moneda.nombre.upper() if moneda else "TODAS LAS MONEDAS"
            moneda_destino = None

        nombre_archivo = f"Reporte_Pagos_{fecha_desde}_al_{fecha_hasta}.xlsx"
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Pagos")

        # Formatos
        header_format = workbook.add_format({'bold': True, 'bg_color': '#d9d9d9', 'border': 1, 'align': 'center'})
        text_format = workbook.add_format({'border': 1})
        money_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        small_text = workbook.add_format({'font_size': 9, 'italic': True, 'border': 1})

        # Título
        titulo = f'Pagos entre el {fecha_desde.strftime("%d/%m/%Y")} y el {fecha_hasta.strftime("%d/%m/%Y")} en {nombre_moneda}'
        worksheet.merge_range('A1:I1', titulo)

        # Encabezados
        headers = ['Fecha', 'Documento', 'Cliente', 'Nombre']
        if ver_detalle:
            headers.append('Detalle')
        headers += ['Moneda original', 'Monto', 'Cuenta', 'Destino']

        worksheet.write_row(1, 0, headers, header_format)
        row = 2
        for cob in pagos:
            if not ver_anuladas and cob.mactivo == 'N':
                continue  # omitir anuladas si no se pidió verlas

            cliente = clientes_dict.get(cob.mcliente)
            asiento_principal = next(
                (a for a in asientos_dict.get(cob.mautogen, []) if getattr(a, 'imputacion', None) == 1), None)

            cuenta = asiento_principal.cuenta if asiento_principal else ''
            destino = asiento_principal.banco if asiento_principal else ''

            # Monto con conversión si es necesario
            monto = Decimal(cob.mtotal or 0)
            moneda_origen = cob.mmoneda
            arbitraje = getattr(cob, 'mcambio', Decimal('1.0'))
            paridad = getattr(cob, 'mparidad', Decimal('1.0'))

            if moneda_destino and moneda_origen != moneda_destino:
                monto = convertir_monto(monto, moneda_origen, moneda_destino, arbitraje, paridad)

            # Armar fila principal
            data = [
                cob.mfechamov.strftime("%d/%m/%Y"),
                cob.mboleta,
                cob.mcliente,
                cliente.empresa if cliente else '',
            ]
            if ver_detalle:
                data.append(cob.mdetalle or '')
            data += [
                moneda.nombre.upper(),
                float(monto),
                cuenta,
                destino
            ]

            worksheet.write_row(row, 0, data, text_format)
            row += 1

            # Filas extra de detalle si se pidió ver (imputación == 2)
            if ver_detalle:
                detalle_format = workbook.add_format({'bg_color': '#f4cccc', 'font_size': 9, 'border': 1})
                for asiento in asientos_dict.get(cob.mautogen, []):
                    if getattr(asiento, 'imputacion', None) == 2:
                        detalle_labels = ['Modo', 'Cuenta', 'Monto', 'Fecha']
                        detalle_valores = [
                            asiento.modo or '',
                            asiento.cuenta or '',
                            float(asiento.monto or 0),
                            asiento.fecha.strftime('%d/%m/%Y') if asiento.fecha else ''
                        ]

                        for col, (label, valor) in enumerate(zip(detalle_labels, detalle_valores)):
                            contenido = f"{label}: {valor}"
                            worksheet.write(row, col, contenido, detalle_format)

                        row += 1

        # Ajustar ancho de columnas
        worksheet.set_column('A:A', 12)  # Fecha
        worksheet.set_column('B:B', 15)  # Documento
        worksheet.set_column('C:C', 10)  # Cliente
        worksheet.set_column('D:D', 35)  # Nombre

        col_offset = 1 if ver_detalle else 0
        worksheet.set_column(f'{chr(69 + col_offset)}:{chr(69 + col_offset)}', 14)  # Moneda original
        worksheet.set_column(f'{chr(70 + col_offset)}:{chr(70 + col_offset)}', 14)  # Monto
        worksheet.set_column(f'{chr(71 + col_offset)}:{chr(71 + col_offset)}', 12)  # Cuenta
        worksheet.set_column(f'{chr(72 + col_offset)}:{chr(72 + col_offset)}', 20)  # Destino

        workbook.close()
        output.seek(0)

        return HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
        )

    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel de cobranzas: {e}")


def convertir_monto(monto, origen, destino, arbitraje, paridad):
    """
    Convierte un monto desde 'origen' a 'destino' utilizando arbitraje y paridad.
    origen y destino son enteros representando códigos de moneda:
    1 = moneda nacional, 2 = dólar, otros = otras monedas (ej: euro)
    """

    try:
        if origen == destino or monto == 0:
            return round(monto, 2)

        if destino == 1:  # convertir a moneda nacional
            if origen == 2 and arbitraje:
                return round(monto * arbitraje, 2)
            elif origen not in [1, 2] and arbitraje and paridad:
                dolares = monto / paridad
                return round(dolares * arbitraje, 2)

        elif destino == 2:  # convertir a dólares
            if origen == 1 and arbitraje:
                return round(monto / arbitraje, 2)
            elif origen not in [1, 2] and paridad:
                return round(monto / paridad, 2)

        else:  # convertir a otra moneda
            if origen == 1 and arbitraje and paridad:
                dolares = monto / arbitraje
                return round(dolares * paridad, 2)
            elif origen == 2 and paridad:
                return round(monto * paridad, 2)
            elif origen == destino:
                return round(monto, 2)

        # Si no se puede convertir, devolver sin modificar
        return round(monto, 2)
    except Exception as e:
        return str(e)