import datetime
import io
from decimal import Decimal

import xlsxwriter
from django.http import HttpResponse
from django.shortcuts import render

from administracion_contabilidad.models import Impucompras, Movims
from consultas_administrativas.forms import ReporteMovimientosComprasForm
from consultas_administrativas.models import VReporteSubdiarioCompras


def subdiario_compras(request):
    if request.method == 'POST':
        form = ReporteMovimientosComprasForm(request.POST)
        if form.is_valid():
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            moneda = form.cleaned_data['moneda']
            todas_monedas = form.cleaned_data['todas_monedas']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            socio_comercial = form.cleaned_data['socio_comercial_i']
            movimiento = form.cleaned_data['movimiento']
            estado = form.cleaned_data['estado']

            filtros = {
                'fecha__range': (fecha_desde, fecha_hasta)
            }

            if not todas_monedas and moneda:
                filtros['moneda'] = moneda.nombre

            if socio_comercial:
                filtros['nro_proveedor'] = socio_comercial

            if movimiento and movimiento != 'todos':
                filtros['tipo'] = movimiento

            queryset = VReporteSubdiarioCompras.objects.filter(**filtros)
            pagos_factura = {}
            for q in queryset:
                impucompras = Impucompras.objects.filter(autofac=q.autogen_factura).only('autogen', 'monto')

                if impucompras.exists():
                    lista_pagos = []
                    for i in impucompras:
                        movim = Movims.objects.filter(mautogen=i.autogen).only('mfechamov', 'mcambio',
                                                                               'mparidad').first()

                        pago = {
                            'autogen': i.autogen,
                            'monto': i.monto,
                            'fecha': movim.mfechamov if movim else None,
                            'cambio': movim.mcambio if movim else None,
                            'paridad': movim.mparidad if movim else None,
                        }
                        lista_pagos.append(pago)

                    pagos_factura[q.autogen_factura] = lista_pagos

            for q in queryset:
                pagos = pagos_factura.get(q.autogen_factura, [])

                if pagos:
                    # Obtener el último cobro por fecha
                    ultimo_pago = max(pagos, key=lambda c: c['fecha'])

                    # Sumar montos
                    suma_pagos = sum(c['monto'] for c in pagos)

                    # Determinar estado de cancelación
                    if suma_pagos == q.total:
                        q.cancelada = "SI"
                    elif suma_pagos > 0:
                        q.cancelada = "PARCIAL"

                    # Asignar datos del último cobro
                    if ultimo_pago:
                        q.pago = ultimo_pago['fecha']
                        q.tipo_cambio_pago = ultimo_pago['cambio']
                    else:
                        q.pago = None
                        q.tipo_cambio_pago = None

                else:
                    q.cancelada = "NO"
                    q.pago = None
                    q.tipo_cambio_pago = None

            datos = []
            for q in queryset:
                datos.append((
                    q.fecha, q.tipo, str(q.serie or '')+str(q.prefijo or '') +str(q.numero or ''),
                    q.nro_proveedor, q.proveedor, q.detalle, q.exento, q.gravado,
                    q.total, q.arbitraje, q.paridad, q.cancelada,
                    q.posicion, q.cuenta,q.vencimiento, q.pago, q.tipo_cambio_pago,
                    q.moneda, q.rut,
                ))

            return generar_excel_subdiario_compras(datos, fecha_desde, fecha_hasta, consolidar_dolares)

    else:
        form = ReporteMovimientosComprasForm(initial={'estado': 'todo'})

    return render(request, 'compras_ca/subdiario_compras.html', {'form': form})

def generar_excel_subdiario_compras(datos, fecha_desde, fecha_hasta, consolidar_dolares):
    try:
        nombre_archivo = f'Subdiario_Compras_{fecha_desde}_al_{fecha_hasta}.xlsx'
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Subdiario_compras")

        title = f"Compras entre el {fecha_desde} y el {fecha_hasta}"
        worksheet.merge_range('A1:AD1', title, workbook.add_format({'bold': True, 'align': 'left'}))

        encabezados = [
            'Fecha', 'Tipo', 'Nro', 'Proveedor', 'Nombre', 'Detalle', 'Exento', 'Gravado', 'Total',
            'T. Cambio', 'Paridad','Cancelada','Posición','Cuenta','Vencimiento','Pago','Tca. Pago',
            'Moneda', 'RUT'
        ]

        worksheet.set_column(0, 0, 8)  # Fecha
        worksheet.set_column(26, 27, 10)  # Pago, Tca. Pago
        worksheet.set_column(22, 23, 10)  # ETD, ETA

        header_format = workbook.add_format({'bold': True, 'bg_color': '#d9d9d9', 'border': 1})
        normal_format = workbook.add_format({'border': 1})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        datos_convertidos = []

        for fila in datos:
            fila = list(fila)

            if consolidar_dolares:
                try:
                    if fila[11] == 'DOLARES USA':
                        moneda_origen = 2
                    else:
                        moneda_origen = 1

                    moneda_destino = 2
                    arbitraje = Decimal(fila[9] or 1)
                    paridad = Decimal(fila[10] or 1)

                    for idx in [6, 7, 8]:  # exento, gravado, total
                        monto = Decimal(fila[idx] or 0)
                        fila[idx] = convertir_monto(monto, moneda_origen, moneda_destino, arbitraje, paridad)
                except Exception as e:
                    print(f"Error al convertir moneda: {e}")

            datos_convertidos.append(fila)

        for col_num, header in enumerate(encabezados):
            worksheet.write(1, col_num, header, header_format)

        columnas_fecha = [0, 22, 23, 25, 26]

        row_num = 2
        for fila in datos_convertidos:
            for col_num, valor in enumerate(fila):
                if col_num in columnas_fecha and isinstance(valor, (datetime.date, datetime.datetime)):
                    worksheet.write(row_num, col_num, valor, date_format)
                else:
                    worksheet.write(row_num, col_num, valor, normal_format)
            row_num += 1

        workbook.close()
        output.seek(0)

        return HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
        )
    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel de compras: {e}")

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