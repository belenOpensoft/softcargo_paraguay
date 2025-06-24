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
                        fecha__gte=fecha_desde,
                        fecha__lte=fecha_hasta,
                        cuenta=cuenta.xcodigo,
                        moneda=moneda.codigo
                    )
                else:
                    asientos= Asientos.objects.filter(
                        fecha__gte=fecha_desde,
                        fecha__lte=fecha_hasta,
                        cuenta=cuenta.xcodigo,
                    )
            elif cuenta_desde and cuenta_hasta:
                if not consolidar_dolares and not consolidar_moneda_nac and moneda:
                    asientos = Asientos.objects.filter(
                        fecha__gte=fecha_desde,
                        fecha__lte=fecha_hasta,
                        cuenta__gte=cuenta_desde,
                        cuenta__lte=cuenta_hasta,
                        moneda=moneda.codigo
                    )
                else:
                    asientos = Asientos.objects.filter(
                        fecha__gte=fecha_desde,
                        fecha__lte=fecha_hasta,
                        cuenta__gte=cuenta_desde,
                        cuenta__lte=cuenta_hasta,
                    )
            else:
                pass
                #retornar error

            return generar_excel_mayores_analiticos(
                asientos,
                cuenta_desde,
               cuenta_hasta,
                fecha_desde,
                fecha_hasta,
                moneda,
                consolidar_dolares,
                consolidar_moneda_nac,
                cuenta
            )
    else:
        form = MayoresAnaliticosForm()
    print("Errores del formulario:", form.errors)


    return render(request, 'contabilidad_ca/mayores_analiticos.html', {'form': form})


def generar_excel_mayores_analiticos(
    asientos, cuenta_desde, cuenta_hasta, fecha_desde, fecha_hasta,
    moneda, consolidar_dolares, consolidar_moneda_nac, cuenta=None
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
            if a.tipo == 'Z':
                debe = float(monto) if a.imputacion == 2 else 0.0
                haber = float(monto) if a.imputacion == 1 else 0.0
            elif a.tipo == 'G':
                debe = float(monto) if a.imputacion == 1 else 0.0
                haber = float(monto) if a.imputacion == 2 else 0.0
            elif a.tipo == 'V':
                debe = float(monto) if a.imputacion == 2 else 0.0
                haber = float(monto) if a.imputacion == 1 else 0.0
            elif a.tipo == 'P':
                debe = float(monto) if a.imputacion == 1 else 0.0
                haber = float(monto) if a.imputacion == 2 else 0.0
            elif a.tipo in ['D', 'T', 'I']:
                debe = float(monto) if a.imputacion == 1 else 0.0
                haber = float(monto) if a.imputacion == 2 else 0.0
            elif a.tipo == 'C':
                debe = float(monto) if a.imputacion == 2 else 0.0
                haber = float(monto) if a.imputacion == 1 else 0.0
            elif a.tipo == 'B':
                debe = float(monto) if a.imputacion == 1 else 0.0
                haber = float(monto) if a.imputacion == 2 else 0.0
            else:
                debe = haber = 0.0

            saldos[cuenta_actual] += Decimal(debe) - Decimal(haber)

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
