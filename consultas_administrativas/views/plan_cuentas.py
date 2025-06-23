import io
from django.http import HttpResponse
import xlsxwriter
from decimal import Decimal

from administracion_contabilidad.models import Cuentas


def plan_cuentas(request):
    try:
        nombre_archivo = "Plan_de_Cuentas.xlsx"
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Plan de cuentas")

        # Formatos
        header_format = workbook.add_format({'bold': True, 'bg_color': '#d9d9d9', 'border': 1, 'align': 'center'})
        text_format = workbook.add_format({'border': 1})
        decimal_format = workbook.add_format({'border': 1, 'num_format': '#,##0.00'})

        # Título
        worksheet.merge_range('A1:I1', "Plan de Cuentas", header_format)

        # Encabezados (ajustá los campos a los que realmente querés mostrar)
        headers = [
            'Código', 'Nombre', 'Tipo', 'Depende de', 'Moneda','Activa'
        ]
        worksheet.write_row(1, 0, headers, header_format)
        row = 2

        cuentas = Cuentas.objects.all().order_by('xcodigo')

        for cuenta in cuentas:
            tipo = 'OTRAS' if cuenta.xtipo == 2 else 'CAJA' if cuenta.xtipo==1 else 'BANCO'
            moneda = 'MIXTO' if cuenta.xmoneda == 0 else 'M/NACIONAL' if cuenta.xmoneda==1 else 'DOLAR' if cuenta.xmoneda==2 else 'EURO' if cuenta.xmoneda==3 else 'Desconocido'
            data = [
                cuenta.xcodigo,
                cuenta.xnombre or '',
                tipo,
                cuenta.xnivel1 or '',
                moneda,
                cuenta.activo if cuenta.activo is not None else '',
            ]
            worksheet.write(row, 0, data[0], text_format)  # Código
            worksheet.write(row, 1, data[1], text_format)  # Nombre
            worksheet.write(row, 2, data[2], text_format)  # Tipo
            worksheet.write(row, 3, data[3], text_format)  # depende de
            worksheet.write(row, 4, data[4], text_format)  # Moneda
            worksheet.write(row, 5, data[5], text_format)  # activa
            row += 1

        # Ajustar columnas
        worksheet.set_column('A:A', 12)  # Código
        worksheet.set_column('B:B', 35)  # Nombre
        worksheet.set_column('C:C', 8)   # Tipo
        worksheet.set_column('D:D', 12)  # Grupo
        worksheet.set_column('E:E', 8)   # Moneda
        worksheet.set_column('F:G', 10)  # Calculo dif
        worksheet.set_column('H:J', 14)  # Presupuesto, Objetivo, Sobregiro

        workbook.close()
        output.seek(0)

        return HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
        )

    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel del plan de cuentas: {e}")
