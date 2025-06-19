from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
import io

import xlsxwriter
from django.db.models import OuterRef, Sum, Subquery, ExpressionWrapper, F, DecimalField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render

from administracion_contabilidad.models import Movims, Asientos, Impuvtas, Boleta
from consultas_administrativas.forms import ReporteCobranzasForm, AntiguedadSaldosForm, EstadoCuentaForm
from consultas_administrativas.models import VAntiguedadSaldos
from mantenimientos.models import Clientes

from datetime import date, datetime


def estados_cuenta(request):
    if request.method == 'POST':
        form = EstadoCuentaForm(request.POST)
        if form.is_valid():
            tipo_consulta = form.cleaned_data['tipo_consulta']
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            moneda = form.cleaned_data['moneda']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            consolidar_moneda_nac = form.cleaned_data['consolidar_moneda_nac']

            queryset = VAntiguedadSaldos.objects.filter(fecha__range=(fecha_desde, fecha_hasta))

            if tipo_consulta == 'individual':
                cliente = form.cleaned_data['cliente']
                if cliente:
                    queryset = queryset.filter(nrocliente=cliente.codigo)

                if form.cleaned_data['todas_las_monedas']:
                    moneda_destino = None
                elif consolidar_dolares:
                    moneda_destino = 2
                elif consolidar_moneda_nac:
                    moneda_destino = 1
                else:
                    moneda_destino = moneda.codigo if moneda else None

                for f in queryset:
                    f.saldo = f.saldo_pendiente

                agrupado = agrupar_estados_cuenta(queryset, moneda_destino)

            else:  # GENERAL
                filtro_tipo = form.cleaned_data['filtro_tipo']
                omitir_saldos_cero = form.cleaned_data['omitir_saldos_cero']

                # Filtro por tipo
                if filtro_tipo == 'clientes':
                    queryset = queryset.filter(tipo='cliente')
                elif filtro_tipo == 'agentes':
                    queryset = queryset.filter(tipo='agente')
                elif filtro_tipo == 'transportistas':
                    queryset = queryset.filter(tipo='transportista')

                if moneda:
                    queryset = queryset.filter(moneda=moneda.codigo)

                for f in queryset:
                    f.saldo = f.saldo_pendiente

                if omitir_saldos_cero:
                    queryset = [f for f in queryset if f.saldo > 0]

                moneda_destino = None
                if consolidar_dolares:
                    moneda_destino = 2
                elif consolidar_moneda_nac:
                    moneda_destino = 1

                agrupado = agrupar_estados_cuenta(queryset, moneda_destino)

            return generar_excel_estados_cuenta(
                agrupado,
                fecha_desde,
                fecha_hasta,
                moneda if moneda else None,
                tipo_consulta
            )
    else:
        form = EstadoCuentaForm()

    return render(request, 'ventas_ca/estados_cuenta.html', {'form': form})



def generar_excel_antiguedad(agrupado, fecha_base, rango, moneda=None):
    try:
        nombre_moneda = moneda.nombre.upper() if moneda else "TODAS LAS MONEDAS"
        nombre_archivo = f"Antiguedad_Saldos_{fecha_base.strftime('%Y%m%d')}.xlsx"
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Antigüedad")

        # Formatos
        header_format = workbook.add_format({'bold': True, 'bg_color': '#d9d9d9', 'border': 1, 'align': 'center'})
        text_format = workbook.add_format({'border': 1})
        money_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        total_format = workbook.add_format({'bold': True, 'top': 2, 'border': 1})
        total_label_format = workbook.add_format({'bold': True, 'top': 2, 'border': 1})

        # Título
        titulo = f'Antigüedad de Saldos al {fecha_base.strftime("%d/%m/%Y")} en {nombre_moneda}'
        worksheet.merge_range('A1:G1', titulo)

        # Encabezados según rango elegido
        if rango == 'rango1':
            columnas = ['0-30', '31-60', '61-90', '91-120', '+120']
        elif rango == 'rango2':
            columnas = ['0-15', '16-30', '31-45', '46-60', '+60']
        elif rango == 'rango3':
            columnas = ['0-30', '31-90', '91-180', '181-360', '+360']
        else:
            raise ValueError("Rango de antigüedad no reconocido")

        headers = ['Código', 'Cliente'] + columnas + ['Total']
        worksheet.write_row(1, 0, headers, header_format)

        # Datos por fila
        row = 2
        total_global = [Decimal('0.00')] * 5

        for codigo, data in agrupado.items():
            nombre = data['nombre']
            saldos = data['saldos']
            total_cliente = sum(saldos)

            # Acumular totales generales
            for i in range(5):
                total_global[i] += saldos[i]

            worksheet.write(row, 0, codigo, text_format)
            worksheet.write(row, 1, nombre, text_format)
            for i in range(5):
                worksheet.write(row, i + 2, float(saldos[i]), money_format)
            worksheet.write(row, 7, float(total_cliente), money_format)
            row += 1

        # Totales al final
        worksheet.write(row, 1, 'TOTAL GENERAL', total_label_format)
        for i in range(5):
            worksheet.write(row, i + 2, float(total_global[i]), total_format)
        worksheet.write(row, 7, float(sum(total_global)), total_format)

        # Ajuste de columnas
        worksheet.set_column('A:A', 10)  # Código
        worksheet.set_column('B:B', 40)  # Cliente
        worksheet.set_column('C:H', 14)  # Rangos + Total

        workbook.close()
        output.seek(0)

        return HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
        )

    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel de antigüedad: {e}")


def agrupar_estados_cuenta(facturas, moneda_destino=None):
    """
    Agrupa facturas por cliente y consolida montos si se especifica moneda_destino.
    """
    resultado = defaultdict(lambda: {
        'nombre': '',
        'documentos': [],
        'total': Decimal('0.00')
    })

    for f in facturas:
        cliente_id = f.nrocliente
        cliente_nombre = f.cliente

        # Conversión si corresponde
        saldo = getattr(f, 'saldo', Decimal('0.00'))
        moneda_origen = f.moneda
        arbitraje = getattr(f, 'arbitraje', Decimal('1.00'))
        paridad = getattr(f, 'paridad', Decimal('1.00'))

        if moneda_destino and moneda_origen != moneda_destino:
            if moneda_origen == 1 and moneda_destino == 2:  # Peso a USD
                saldo = saldo / arbitraje if arbitraje else saldo
            elif moneda_origen == 2 and moneda_destino == 1:  # USD a Peso
                saldo = saldo * paridad if paridad else saldo

        saldo = saldo.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

        resultado[cliente_id]['nombre'] = cliente_nombre
        resultado[cliente_id]['total'] += saldo
        resultado[cliente_id]['documentos'].append({
            'fecha': f.fecha,
            'vto': f.vto,
            'total': f.total,
            'total_pagado': f.total_pagado,
            'saldo': saldo
        })

    return resultado
