from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime

from administracion_contabilidad.models import Asientos, Cuentas
from consultas_administrativas.forms import LibroDiarioForm
from mantenimientos.models import Clientes, Monedas

import io
import datetime
from decimal import Decimal
from django.http import HttpResponse
import xlsxwriter


def libro_diario(request):
    if request.method == 'POST':
        form = LibroDiarioForm(request.POST)
        if form.is_valid():
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            moneda = form.cleaned_data['moneda']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            consolidar_moneda_nac = form.cleaned_data['consolidar_moneda_nac']
            tipo_consulta = form.cleaned_data['tipo_consulta']

            tipos=[]

            if tipo_consulta=='ventas':
                tipos.append('V')
            elif tipo_consulta == 'compras':
                tipos.append('P')
            elif tipo_consulta == 'pagos':
                tipos.append('G')
            elif tipo_consulta=='cobros':
                tipos.append('Z')
            elif tipo_consulta == 'sin_ventas_compras':
                tipos.append('G')
                tipos.append('Z')

            if not consolidar_dolares and not consolidar_moneda_nac and moneda:
                if tipos:
                    asientos = Asientos.objects.filter(
                        fecha__gte=fecha_desde,
                        fecha__lte=fecha_hasta,
                        moneda=moneda.codigo,
                        tipo__in=tipos
                    )
                else:
                    asientos = Asientos.objects.filter(
                        fecha__gte=fecha_desde,
                        fecha__lte=fecha_hasta,
                        moneda=moneda.codigo
                    )
            else:
                if tipos:
                    asientos = Asientos.objects.filter(
                        fecha__gte=fecha_desde,
                        fecha__lte=fecha_hasta,
                        tipo__in=tipos
                    )
                else:
                    asientos = Asientos.objects.filter(
                        fecha__gte=fecha_desde,
                        fecha__lte=fecha_hasta
                    )

            return generar_excel_libro_diario(asientos,moneda,fecha_desde,fecha_hasta,consolidar_dolares,consolidar_moneda_nac)

    else:
        form = LibroDiarioForm()

    return render(request, 'contabilidad_ca/libro_diario.html', {'form': form})

def generar_excel_libro_diario(asientos, moneda, fecha_desde, fecha_hasta, consolidar_dolares, consolidar_moneda_nac):
    try:
        nombre_archivo = f'Libro_Diario_{fecha_desde}_al_{fecha_hasta}.xlsx'
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Libro_diario")

        # Título
        titulo = f"Asientos entre el {fecha_desde.strftime('%d/%m/%Y')} y el {fecha_hasta.strftime('%d/%m/%Y')}"
        worksheet.merge_range('A1:O1', titulo, workbook.add_format({'bold': True, 'align': 'left'}))

        # Encabezados
        encabezados = [
            'Fecha', 'Asiento', 'Tipo', 'Número', 'Detalle', 'Cuenta', 'Nombre', 'Tipo C.',
            'Paridad', 'Debe', 'Haber', 'Mov', 'Socio Comercial', 'Moneda', 'Posición'
        ]

        for col_num, header in enumerate(encabezados):
            worksheet.write(1, col_num, header, workbook.add_format({
                'bold': True, 'bg_color': '#d9d9d9', 'border': 1
            }))

        columnas_fecha = [0]
        columnas_monto = [8, 9, 10]  # Paridad, Debe, Haber

        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        decimal_format = workbook.add_format({'num_format': '#,##0.00'})
        normal_format = workbook.add_format({'border': 1})

        row_num = 2
        for a in asientos:
            # Filtrar por moneda si no hay consolidación
            if not consolidar_dolares and not consolidar_moneda_nac and moneda:
                if a.moneda != moneda.codigo:
                    continue

            monto = Decimal(a.monto or 0)
            arbitraje = Decimal(a.cambio or 1)
            paridad = Decimal(a.paridad or 1)
            moneda_origen = a.moneda
            moneda_destino = None

            if consolidar_dolares:
                moneda_destino = 2
            elif consolidar_moneda_nac:
                moneda_destino = 1

            if moneda_destino:
                monto = convertir_monto(monto, moneda_origen, moneda_destino, arbitraje, paridad)

            # Definición de debe y haber según tipo
            if a.tipo == 'Z':  # Cobros
                debe = float(monto) if a.imputacion == 2 else 0.0
                haber = float(monto) if a.imputacion == 1 else 0.0
            elif a.tipo == 'G':  # Pagos
                debe = float(monto) if a.imputacion == 1 else 0.0
                haber = float(monto) if a.imputacion == 2 else 0.0
            elif a.tipo == 'V':  # Ventas
                debe = float(monto) if a.imputacion == 2 else 0.0
                haber = float(monto) if a.imputacion == 1 else 0.0
            elif a.tipo == 'P':  # Compras
                debe = float(monto) if a.imputacion == 1 else 0.0
                haber = float(monto) if a.imputacion == 2 else 0.0
            elif a.tipo in ['D', 'T', 'I']:  # Diversos, Traspasos, Iniciales
                debe = float(monto) if a.imputacion == 1 else 0.0
                haber = float(monto) if a.imputacion == 2 else 0.0
            elif a.tipo == 'C':  # Cierre
                debe = float(monto) if a.imputacion == 2 else 0.0
                haber = float(monto) if a.imputacion == 1 else 0.0
            elif a.tipo == 'B':  # Banco
                debe = float(monto) if a.imputacion == 1 else 0.0
                haber = float(monto) if a.imputacion == 2 else 0.0
            else:
                debe = 0.0
                haber = 0.0

            nombre_cta = Cuentas.objects.only('xnombre').filter(xcodigo=a.cuenta).first()
            nombre = nombre_cta.xnombre if nombre_cta else ''

            socio = Clientes.objects.only('empresa').filter(codigo=a.cliente).first()
            socio_comercial = socio.empresa if socio else ''

            if moneda_destino:
                nombre_moneda = "DOLARES USA" if moneda_destino == 2 else "MONEDA NACIONAL"
            else:
                nombre_moneda= Monedas.objects.only('nombre').filter(codigo=a.moneda).first()

            fila = [
                a.fecha,
                a.asiento,
                a.tipo,
                a.documento,
                a.detalle or '',
                a.cuenta,
                nombre,
                a.cambio,
                float(a.paridad or 0),
                debe,
                haber,
                a.mov,
                socio_comercial,
                nombre_moneda,
                a.posicion
            ]

            for col_num, valor in enumerate(fila):
                if col_num in columnas_fecha and isinstance(valor, (datetime.date, datetime.datetime)):
                    worksheet.write(row_num, col_num, valor, date_format)
                elif col_num in columnas_monto:
                    worksheet.write(row_num, col_num, valor, decimal_format)
                else:
                    worksheet.write(row_num, col_num, valor, normal_format)
            row_num += 1

        worksheet.set_column('A:A', 10)  # Fecha
        worksheet.set_column('B:B', 10)  # Asiento
        worksheet.set_column('C:D', 8)   # Tipo, Número
        worksheet.set_column('E:E', 30)  # Detalle
        worksheet.set_column('F:F', 10)  # Cuenta
        worksheet.set_column('G:G', 35)  # Nombre
        worksheet.set_column('H:H', 10)  # Tipo C.
        worksheet.set_column('I:I', 10)  # Paridad
        worksheet.set_column('J:K', 14)  # Debe, Haber
        worksheet.set_column('L:L', 10)  # Mov
        worksheet.set_column('M:M', 25)  # Socio
        worksheet.set_column('N:N', 20)  # Moneda
        worksheet.set_column('O:O', 15)  # Posición

        workbook.close()
        output.seek(0)

        return HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
        )

    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel del libro diario: {e}")


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
