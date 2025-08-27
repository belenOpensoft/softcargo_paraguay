from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime

from administracion_contabilidad.models import Asientos, Cuentas
from consultas_administrativas.forms import LibroDiarioForm, MayoresAnaliticosForm
from mantenimientos.models import Clientes, Monedas

import io
import datetime
from decimal import Decimal
from django.http import HttpResponse
import xlsxwriter

def mayores_analiticos(request):
    if request.method == 'POST':
        form = MayoresAnaliticosForm(request.POST)
        if form.is_valid():
            cuenta = form.cleaned_data['banco']
            cuenta_desde = form.cleaned_data['cuenta_desde']
            cuenta_hasta = form.cleaned_data['cuenta_hasta']
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            moneda = form.cleaned_data['moneda']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            consolidar_moneda_nac = form.cleaned_data['consolidar_moneda_nac']

            # Filtro base
            if cuenta:
                if not consolidar_dolares and not consolidar_moneda_nac and moneda:
                    asientos= Asientos.objects.filter(
                        fecha__date__gte=fecha_desde,
                        fecha__date__lte=fecha_hasta,
                        cuenta=cuenta.xcodigo,
                        moneda=moneda.codigo
                    )
                else:
                    asientos= Asientos.objects.filter(
                        fecha__date__gte=fecha_desde,
                        fecha__date__lte=fecha_hasta,
                        cuenta=cuenta.xcodigo,
                    )
            elif cuenta_desde and cuenta_hasta:
                if not consolidar_dolares and not consolidar_moneda_nac and moneda:
                    asientos = Asientos.objects.filter(
                        fecha__date__gte=fecha_desde,
                        fecha__date__lte=fecha_hasta,
                        cuenta__gte=cuenta_desde,
                        cuenta__lte=cuenta_hasta,
                        moneda=moneda.codigo
                    )
                else:
                    asientos = Asientos.objects.filter(
                        fecha__date__gte=fecha_desde,
                        fecha__date__lte=fecha_hasta,
                        cuenta__gte=cuenta_desde,
                        cuenta__lte=cuenta_hasta,
                    )
            else:
                pass
                #retornar error

            saldo = calcular_saldo_anterior(cuenta.xcodigo,fecha_desde, consolidar_dolares=consolidar_dolares, consolidar_moneda_nac=consolidar_moneda_nac,moneda=moneda.codigo)

            return generar_excel_mayores_analiticos(
                asientos,
                cuenta_desde,
               cuenta_hasta,
                fecha_desde,
                fecha_hasta,
                moneda,
                consolidar_dolares,
                consolidar_moneda_nac,
                cuenta,
                saldo
            )
    else:
        form = MayoresAnaliticosForm()
    print("Errores del formulario:", form.errors)


    return render(request, 'contabilidad_ca/mayores_analiticos.html', {'form': form})


def generar_excel_mayores_analiticos_old(
    asientos, cuenta_desde, cuenta_hasta, fecha_desde, fecha_hasta,
    moneda, consolidar_dolares, consolidar_moneda_nac, cuenta=None, saldo=None
):
    try:
        nombre_archivo = f"Mayores_Analiticos_{fecha_desde}_al_{fecha_hasta}.xlsx"
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Mayores Analiticos")

        # Formatos
        titulo_format = workbook.add_format({'bold': True, 'align': 'left'})
        encabezado_format = workbook.add_format({'bold': True, 'bg_color': '#d9d9d9', 'border': 1})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})  # sin borde
        decimal_format = workbook.add_format({'num_format': '#,##0.00'})  # sin borde
        normal_format = workbook.add_format({})  # sin borde

        columnas = [
            'Fecha', 'Asiento', 'Detalle', 'Moneda', 'Documento', 'T.C.',
            'Debe', 'Haber', 'Saldo', 'Posicion', 'Monto Origen',
            'Tipo', 'Socio comercial', 'Paridad', 'Cliente', 'Autogenerado'
        ]

        row = 0
        saldos = {}

        asientos = asientos.order_by('cuenta', 'fecha', 'asiento')
        cuenta_actual = None

        total_debe = Decimal('0.00')
        total_haber = Decimal('0.00')
        ultimo_saldo = Decimal('0.00')

        for a in asientos:
            if cuenta_actual != a.cuenta:
                cuenta_actual = a.cuenta
                saldos[cuenta_actual] = Decimal('0.00')

                nombre_cuenta = cuenta.xnombre if cuenta else Cuentas.objects.get(xcodigo=a.cuenta).xnombre
                worksheet.write(row, 0, f"Asientos desde {fecha_desde} a {fecha_hasta} - Cuenta: {a.cuenta} - {nombre_cuenta}", titulo_format)
                row += 1

                for col_num, header in enumerate(columnas):
                    worksheet.write(row, col_num, header, encabezado_format)
                row += 1

            monto = Decimal(a.monto or 0)
            arbitraje = Decimal(a.cambio or 1)
            paridad = Decimal(a.paridad or 1)
            moneda_origen = a.moneda

            if consolidar_dolares:
                monto = convertir_monto(monto, moneda_origen, 2, arbitraje, paridad)
            elif consolidar_moneda_nac:
                monto = convertir_monto(monto, moneda_origen, 1, arbitraje, paridad)

            # Calcular debe y haber según tipo e imputación
            # if a.tipo == 'Z':
            #     debe = float(monto) if a.imputacion == 2 else 0.0
            #     haber = float(monto) if a.imputacion == 1 else 0.0
            # elif a.tipo == 'G':
            #     debe = float(monto) if a.imputacion == 1 else 0.0
            #     haber = float(monto) if a.imputacion == 2 else 0.0
            # elif a.tipo == 'V':
            #     debe = float(monto) if a.imputacion == 2 else 0.0
            #     haber = float(monto) if a.imputacion == 1 else 0.0
            # elif a.tipo == 'P':
            #     debe = float(monto) if a.imputacion == 1 else 0.0
            #     haber = float(monto) if a.imputacion == 2 else 0.0
            # elif a.tipo in ['D', 'T', 'I']:
            #     debe = float(monto) if a.imputacion == 1 else 0.0
            #     haber = float(monto) if a.imputacion == 2 else 0.0
            # elif a.tipo == 'C':
            #     debe = float(monto) if a.imputacion == 2 else 0.0
            #     haber = float(monto) if a.imputacion == 1 else 0.0
            # elif a.tipo == 'B':
            #     debe = float(monto) if a.imputacion == 1 else 0.0
            #     haber = float(monto) if a.imputacion == 2 else 0.0
            # else:
            #     debe = haber = 0.0

            haber=debe=0

            if a.tipo == 'Z':
                debe = float(monto)
            elif a.tipo == 'G':
                haber = float(monto)
            elif a.tipo == 'V':
                debe = float(monto)
            elif a.tipo == 'P':
                haber = float(monto)
            elif a.tipo in ['D', 'T', 'I']:
                haber = float(monto)
            elif a.tipo == 'C':
                haber = float(monto)
            elif a.tipo == 'B':
                haber = float(monto)
            else:
                debe = haber = 0.0

            saldos[cuenta_actual] += Decimal(debe) - Decimal(haber)
            ultimo_saldo = saldos[cuenta_actual]

            total_debe += Decimal(debe)
            total_haber += Decimal(haber)

            moneda_nombre = Monedas.objects.filter(codigo=a.moneda).values_list('nombre', flat=True).first() or ''

            fila = [
                a.fecha, a.asiento, a.detalle or '', moneda_nombre, a.documento or '', float(a.cambio or 0),
                debe, haber, float(saldos[cuenta_actual]), a.posicion or '', float(a.monto or 0), a.tipo or '',
                a.cliente or '', float(a.paridad or 0), a.cliente or '', a.autogenerado
            ]

            for col_num, valor in enumerate(fila):
                if isinstance(valor, (datetime.date, datetime.datetime)):
                    worksheet.write(row, col_num, valor, date_format)
                elif isinstance(valor, (float, Decimal)):
                    worksheet.write(row, col_num, valor, decimal_format)
                else:
                    worksheet.write(row, col_num, valor, normal_format)

            row += 1

        row += 1
        worksheet.write(row, 0, "Neto periodo:", titulo_format)
        worksheet.write(row, 8, float(ultimo_saldo), decimal_format)  # Columna saldo
        row += 2
        worksheet.write(row, 5, "TOTAL", encabezado_format)
        worksheet.write(row, 6, float(total_debe), decimal_format)   # Total debe
        worksheet.write(row, 7, float(total_haber), decimal_format)  # Total haber
        worksheet.write(row, 8, float(ultimo_saldo), decimal_format) # Total saldo

        worksheet.set_column('A:P', 14)
        workbook.close()
        output.seek(0)

        return HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
        )
    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel de mayores analíticos: {e}")

def generar_excel_mayores_analiticos(
    asientos, cuenta_desde, cuenta_hasta, fecha_desde, fecha_hasta,
    moneda, consolidar_dolares, consolidar_moneda_nac, cuenta=None, saldo=None
):
    try:
        nombre_archivo = f"Mayores_Analiticos_{fecha_desde}_al_{fecha_hasta}.xlsx"
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Mayores Analiticos")

        # Formatos
        titulo_format = workbook.add_format({'bold': True, 'align': 'left'})
        encabezado_format = workbook.add_format({'bold': True, 'bg_color': '#d9d9d9', 'border': 1})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        decimal_format = workbook.add_format({'num_format': '#,##0.00'})
        normal_format = workbook.add_format({})

        columnas = [
            'Fecha', 'Asiento', 'Detalle', 'Moneda', 'Documento', 'T.C.',
            'Debe', 'Haber', 'Saldo', 'Posicion', 'Monto Origen',
            'Tipo', 'Socio comercial', 'Paridad', 'Cliente', 'Autogenerado'
        ]

        row = 0
        saldos = {}
        cuenta_actual = None

        total_debe = Decimal('0.00')
        total_haber = Decimal('0.00')
        saldo_periodo = Decimal('0.00')   # saldo desde 0
        ultimo_saldo = Decimal('0.00')    # saldo real con saldo anterior

        asientos = asientos.order_by('cuenta', 'fecha', 'asiento')

        for a in asientos:
            if cuenta_actual != a.cuenta:
                cuenta_actual = a.cuenta

                # Inicializar con saldo anterior recibido
                saldo_inicial = Decimal(saldo or 0)
                saldos[cuenta_actual] = saldo_inicial
                saldo_periodo = Decimal('0.00')

                nombre_cuenta = cuenta.xnombre if cuenta else Cuentas.objects.get(xcodigo=a.cuenta).xnombre
                worksheet.write(row, 0, f"Asientos desde {fecha_desde} a {fecha_hasta} - Cuenta: {a.cuenta} - {nombre_cuenta}", titulo_format)
                row += 1

                for col_num, header in enumerate(columnas):
                    worksheet.write(row, col_num, header, encabezado_format)
                row += 1

                # Fila de saldo anterior
                worksheet.write(row, 0, "Saldo anterior", titulo_format)
                worksheet.write(row, 8, float(saldo_inicial), decimal_format)
                row += 1

            # ======= Lógica de cálculo =======
            monto = Decimal(a.monto or 0)
            arbitraje = Decimal(a.cambio or 1)
            paridad = Decimal(a.paridad or 1)
            moneda_origen = a.moneda

            if consolidar_dolares:
                monto = convertir_monto(monto, moneda_origen, 2, arbitraje, paridad)
            elif consolidar_moneda_nac:
                monto = convertir_monto(monto, moneda_origen, 1, arbitraje, paridad)

            haber = debe = 0.0
            if a.tipo == 'Z':
                debe = float(monto)
            elif a.tipo == 'C':
                if a.imputacion == 1:
                    debe = float(monto)
                else:
                    haber = float(monto)
            elif a.tipo == 'G':
                haber = float(monto)
            elif a.tipo == 'V':
                if 'DEV/' in a.detalle:
                    haber = float(monto)
                else:
                    debe = float(monto)
            elif a.tipo == 'P':
                if 'DEV/' in a.detalle:
                    debe = float(monto)
                else:
                    haber = float(monto)
            elif a.tipo == 'B':
                if a.imputacion==2:
                    haber = float(monto)
                else:
                    debe = float(monto)
            elif a.tipo in ['D', 'T', 'I']:
                if a.imputacion == 1:
                    debe = float(monto)
                else:
                    haber = float(monto)

            saldos[cuenta_actual] += Decimal(debe) - Decimal(haber)  # saldo real
            saldo_periodo        += Decimal(debe) - Decimal(haber)  # saldo desde 0
            ultimo_saldo = saldos[cuenta_actual]

            total_debe += Decimal(debe)
            total_haber += Decimal(haber)

            moneda_nombre = Monedas.objects.filter(codigo=a.moneda).values_list('nombre', flat=True).first() or ''

            fila = [
                a.fecha, a.asiento, a.detalle or '', moneda_nombre, a.documento or '', float(a.cambio or 0),
                debe, haber, float(saldos[cuenta_actual]), a.posicion or '', float(a.monto or 0), a.tipo or '',
                a.cliente or '', float(a.paridad or 0), a.cliente or '', a.autogenerado
            ]

            for col_num, valor in enumerate(fila):
                if isinstance(valor, (datetime.date, datetime.datetime)):
                    worksheet.write(row, col_num, valor, date_format)
                elif isinstance(valor, (float, Decimal)):
                    worksheet.write(row, col_num, valor, decimal_format)
                else:
                    worksheet.write(row, col_num, valor, normal_format)
            row += 1

        # ==== Totales y cierres ====
        row += 1
        worksheet.write(row, 0, "Neto período:", titulo_format)
        worksheet.write(row, 8, float(saldo_periodo), decimal_format)

        row += 1
        worksheet.write(row, 0, "Saldo final:", titulo_format)
        worksheet.write(row, 8, float(ultimo_saldo), decimal_format)

        row += 2
        worksheet.write(row, 5, "TOTAL", encabezado_format)
        worksheet.write(row, 6, float(total_debe), decimal_format)
        worksheet.write(row, 7, float(total_haber), decimal_format)
        worksheet.write(row, 8, float(ultimo_saldo), decimal_format)

        worksheet.set_column('A:P', 14)
        workbook.close()
        output.seek(0)

        return HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
        )
    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel de mayores analíticos: {e}")


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

from decimal import Decimal
import datetime

def calcular_saldo_anterior(cuenta_codigo, fecha_desde, *, consolidar_dolares=False, consolidar_moneda_nac=False,moneda=None):
    """
    Devuelve el saldo anterior (Decimal) de una cuenta hasta justo ANTES de `fecha_desde`.
    Usa la misma lógica de debe/haber por `tipo` que tu reporte.
    """

    qs = Asientos.objects.filter(cuenta=cuenta_codigo, fecha__date__lt=fecha_desde)
    if moneda:
        qs=qs.filter(moneda=moneda)

    saldo = Decimal('0.00')

    for a in qs:
        monto = a.monto
        arbitraje = a.cambio
        paridad = a.paridad
        moneda_origen = a.moneda

        # Misma conversión que en tu excel
        if consolidar_dolares:
            monto = convertir_monto(monto, moneda_origen, 2, arbitraje, paridad)
        elif consolidar_moneda_nac:
            monto = convertir_monto(monto, moneda_origen, 1, arbitraje, paridad)

        haber = debe = 0

        if a.tipo == 'Z':
            debe = float(monto)
        elif a.tipo == 'G':
            haber = float(monto)
        elif a.tipo == 'V':
            if 'DEV/' in a.detalle:
                haber = float(monto)
            else:
                debe = float(monto)
        elif a.tipo == 'P':
            if 'DEV/' in a.detalle:
                debe = float(monto)
            else:
                haber = float(monto)
        elif a.tipo in ['D', 'T', 'I']:
            if a.imputacion==1:
                debe = float(monto)
            else:
                haber = float(monto)
        elif a.tipo == 'C':
            if a.imputacion == 1:
                debe = float(monto)
            else:
                haber = float(monto)
        elif a.tipo == 'B':
            if a.imputacion == 2:
                haber = float(monto)
            else:
                debe = float(monto)
        else:
            debe = haber = 0.0

        saldo += Decimal(debe) - Decimal(haber)
    return saldo
