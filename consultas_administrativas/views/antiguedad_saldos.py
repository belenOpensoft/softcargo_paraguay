from collections import defaultdict
from decimal import Decimal
import io

import xlsxwriter
from django.db.models import OuterRef, Sum, Subquery, ExpressionWrapper, F, DecimalField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render

from administracion_contabilidad.models import Movims, Asientos, Impuvtas, Boleta
from consultas_administrativas.forms import ReporteCobranzasForm, AntiguedadSaldosForm
from consultas_administrativas.models import VAntiguedadSaldos
from mantenimientos.models import Clientes

from datetime import date, datetime


def antiguedad_saldos(request):
    if request.method == 'POST':
        form = AntiguedadSaldosForm(request.POST)
        if form.is_valid():
            moneda = form.cleaned_data['moneda']
            base_calculo = form.cleaned_data['base_calculo']
            rango = form.cleaned_data['rango']
            hoy = date.today()

            facturas = VAntiguedadSaldos.objects.all()
            if moneda:
                facturas = facturas.filter(moneda=moneda.codigo)

            for f in facturas:
                f.saldo = f.saldo_pendiente

            agrupado = agrupar_antiguedad_saldos(
                facturas,
                base_calculo=base_calculo,
                rango=rango
            )

            return generar_excel_antiguedad(
                agrupado,
                hoy,
                rango,
                moneda
            )

    else:
        form = AntiguedadSaldosForm()

    return render(request, 'ventas_ca/antiguedad_saldos.html', {'form': form})



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


def agrupar_antiguedad_saldos(facturas, base_calculo='emision', rango='rango1'):
    hoy = date.today()
    resultado = defaultdict(lambda: {'nombre': '', 'saldos': [Decimal('0.00')] * 5})

    for f in facturas:
        cliente_id = f.nrocliente
        cliente_nombre = f.cliente
        saldo = getattr(f, 'saldo', getattr(f, 'saldo_pendiente', Decimal('0.00')))

        fecha_base = f.fecha if base_calculo == 'emision' else f.vto
        if not fecha_base:
            continue

        if isinstance(fecha_base, datetime):
            fecha_base = fecha_base.date()

        dias = (hoy - fecha_base).days

        # Asignar el saldo al rango correspondiente
        for idx, (desde, hasta) in enumerate(RANGOS_DE_DIAS[rango]):
            if desde <= dias <= hasta:
                resultado[cliente_id]['nombre'] = cliente_nombre
                resultado[cliente_id]['saldos'][idx] += saldo
                break

    return resultado

RANGOS_DE_DIAS = {
    'rango1': [(0, 30), (31, 60), (61, 90), (91, 120), (121, float('inf'))],
    'rango2': [(0, 15), (16, 30), (31, 45), (46, 60), (61, float('inf'))],
    'rango3': [(0, 30), (31, 90), (91, 180), (181, 360), (361, float('inf'))]
}

