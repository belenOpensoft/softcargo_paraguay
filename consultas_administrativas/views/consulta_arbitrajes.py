from django.shortcuts import render

from administracion_contabilidad.models import Dolar
from consultas_administrativas.forms import ConsultaArbitrajesForm

import io
from decimal import Decimal
from django.http import HttpResponse
import xlsxwriter


def consulta_arbitrajes(request):
    if request.method == 'POST':
        form = ConsultaArbitrajesForm(request.POST)
        if form.is_valid():
            fecha_hasta = form.cleaned_data['fecha_hasta']
            fecha_desde = form.cleaned_data['fecha_desde']
            moneda = form.cleaned_data['moneda']

            cotizaciones = Dolar.objects.filter(umoneda=moneda.codigo,ufecha__gte=fecha_desde,ufecha__lte=fecha_hasta)

            return generar_excel_cotizaciones(cotizaciones, fecha_desde, moneda, fecha_hasta)

    else:
        form = ConsultaArbitrajesForm()

    return render(request, 'contabilidad_ca/consulta_arbitrajes.html', {'form': form})



def generar_excel_cotizaciones(cotizaciones, fecha_desde, moneda, fecha_hasta):
    try:
        nombre_moneda = moneda.nombre.upper() if moneda else "MONEDA"

        nombre_archivo = f"Cotizaciones de moneda {fecha_desde}_al_{fecha_hasta}.xlsx"
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Cotizaciones")

        # Formatos
        header_format = workbook.add_format({
            'bold': True, 'bg_color': '#d9d9d9', 'border': 1, 'align': 'center'
        })
        text_format = workbook.add_format({'border': 1})
        decimal_format = workbook.add_format({'border': 1, 'num_format': '#,##0.0000'})

        # Título
        titulo = f'Cotizaciones de moneda entre el {fecha_desde.strftime("%d/%m/%Y")} y el {fecha_hasta.strftime("%d/%m/%Y")} para {nombre_moneda}'
        worksheet.merge_range('A1:F1', titulo, header_format)

        # Encabezados
        headers = ['Fecha', 'Moneda', 'Paridad', 'Arbitraje', 'Pizarra', 'Usuario']
        worksheet.write_row(1, 0, headers, header_format)
        row = 2

        for cot in cotizaciones:
            data = [
                cot.ufecha.strftime("%d/%m/%Y %H:%M") if cot.ufecha else '',
                nombre_moneda,
                float(cot.paridad or Decimal('0.0')),
                float(cot.uvalor or Decimal('0.0')),
                float(cot.upizarra or Decimal('0.0')),
                cot.usuario or ''
            ]
            worksheet.write(row, 0, data[0], text_format)  # Fecha
            worksheet.write(row, 1, data[1], text_format)  # Moneda
            worksheet.write(row, 2, data[2], decimal_format)  # Paridad
            worksheet.write(row, 3, data[3], decimal_format)  # Arbitraje
            worksheet.write(row, 4, data[4], decimal_format)  # Pizarra
            worksheet.write(row, 5, data[5], text_format)  # Usuario
            row += 1

        # Ancho de columnas
        worksheet.set_column('A:A', 20)  # Fecha
        worksheet.set_column('B:B', 15)  # Moneda
        worksheet.set_column('C:E', 12)  # Paridad, Arbitraje, Pizarra
        worksheet.set_column('F:F', 10)  # Usuario

        workbook.close()
        output.seek(0)

        return HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
        )

    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel de cotizaciones: {e}")
