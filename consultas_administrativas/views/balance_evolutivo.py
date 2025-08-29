from django.shortcuts import render
from datetime import datetime
from administracion_contabilidad.models import Asientos, Cuentas
from consultas_administrativas.forms import LibroDiarioForm, BalanceEvolutivoForm
from mantenimientos.models import Clientes, Monedas

import io
import calendar
from decimal import Decimal
from collections import OrderedDict
from django.http import HttpResponse
import xlsxwriter


# Mapa de cuentas a incluir (como pasaste)
CUENTAS_MAP = OrderedDict([
    ('VENTAS DE EXPORTACION Y ASIMIL', 411),
    ('VENTAS TASA BASICA', 412),
    ('VENTAS EXENTAS', 414),
    ('DIFERENCIA DE CAMBIO', 422),

    ('GASTOS BANCARIOS', 535),
    ('SERV CONTRATADOS GRAV Y EXENTOS', 5161),
    ('SERV CONTR FLETES MARITIMOS', 5162),
    ('SERV CONTR FLETES AEREO', 5163),
    ('SERV. CONTRAT. EXTERIOR', 5165),
    ('SUELDOS Y JORNALES', 5211),
    ('CARGAS SOCIALES', 5212),
    ('HONORARIOS PROFESIONALES', 5214),
    ('ARRENDAMIENTOS INMUEBLES', 5241),
    ('GASTOS COMUNES', 5242),
    ('UTE,OSE,ANTEL', 52303),
    ('GASTOS GENERALES', 52304),
    ('GASTOS DE VIAJES', 52307),
    ('GASTOS DE PAPELERIA', 52312),
])

# Determinación de grupo (Ganancias vs Pérdidas)
def es_ganancia(cuenta_numero: int) -> bool:
    """
    Ganancias: todas <421 y también la 422 (diferencia de cambio).
    """
    return cuenta_numero < 421 or cuenta_numero == 422

def _meses_jan_dec_labels(anio: int):
    # Etiquetas fijas Ene..Dic (el Excel muestra todos los meses)
    return [(m, calendar.month_name[m]) for m in range(1, 13)]


def balance_evolutivo(request):
    try:
        if request.method == 'POST':
            form = BalanceEvolutivoForm(request.POST)
            if form.is_valid():
                fecha_desde = form.cleaned_data.get('desde')
                fecha_hasta = datetime.now().date()   # hasta hoy

                consolidar_dolares = form.cleaned_data.get('consolidar_dolares', False)
                consolidar_moneda_nac = form.cleaned_data.get('consolidar_moneda_nac', False)

                # Moneda de destino (conversión)
                destino_moneda = None
                if consolidar_moneda_nac and not consolidar_dolares:
                    destino_moneda = 1   # moneda nacional
                    titulo_moneda = "Cons. Moneda Nacional"
                elif consolidar_dolares and not consolidar_moneda_nac:
                    destino_moneda = 2   # dólares
                    titulo_moneda = "Cons. USD"
                else:
                    titulo_moneda = "Sin conversión"

                # Meses (siempre Ene..Dic del año de fecha_hasta)
                anio = fecha_hasta.year
                meses = _meses_jan_dec_labels(anio)

                # Traer asientos relevantes
                qs = (
                    Asientos.objects
                    .filter(
                        fecha__date__gte=fecha_desde,
                        fecha__date__lte=fecha_hasta,
                        cuenta__in=list(CUENTAS_MAP.values())
                    )
                    .values('cuenta', 'fecha', 'monto', 'moneda', 'cambio', 'paridad','tipo')
                )

                # Estructura base
                data = {}
                for nombre, numero in CUENTAS_MAP.items():
                    data[numero] = {
                        'nombre': nombre,
                        'por_mes': {m: {'debe': Decimal('0.00'), 'haber': Decimal('0.00')} for m, _ in meses},
                        'tot_debe': Decimal('0.00'),
                        'tot_haber': Decimal('0.00'),
                    }

                # Procesar asientos con conversión
                for row in qs:
                    numero = row['cuenta']
                    nombre = next((k for k, v in CUENTAS_MAP.items() if v == numero), str(numero))
                    mes_num = row['fecha'].month

                    monto = Decimal(row['monto'] or 0)
                    origen = row['moneda']       # int: 1 = MN, 2 = USD, otros
                    arbitraje = row['cambio']    # tipo de cambio
                    paridad = row['paridad']     # paridad (ej: EUR/USD)

                    # Conversión si corresponde
                    if destino_moneda:
                        monto = Decimal(convertir_monto(monto, origen, destino_moneda, arbitraje, paridad))

                    # Inicialización por si aparece una cuenta no listada
                    if numero not in data:
                        data[numero] = {
                            'nombre': nombre,
                            'por_mes': {m: {'debe': Decimal('0.00'), 'haber': Decimal('0.00')} for m, _ in meses},
                            'tot_debe': Decimal('0.00'),
                            'tot_haber': Decimal('0.00'),
                        }

                    # Reglas de acumulación:
                    # - Ganancias comunes (411, 412, 414): sumar en HABER.
                    # - Cuenta 422: es de DEBER, pero se muestra en bloque de Ganancias; cargar en DEBE.
                    # - Pérdidas (>=500): sumar en DEBE.
                    if es_ganancia(numero):
                        if numero == 422:
                            # Solo DEBE (después se mostrará negativo en columnas mensuales)
                            if row['tipo']=='G' or row['tipo']=='V':
                                data[numero]['por_mes'][mes_num]['debe'] += monto
                                data[numero]['tot_debe'] += monto
                        else:
                            data[numero]['por_mes'][mes_num]['haber'] += monto
                            data[numero]['tot_haber'] += monto
                    else:
                        data[numero]['por_mes'][mes_num]['debe'] += monto
                        data[numero]['tot_debe'] += monto

                # Totales (globales y por mes)
                tot_gan_debe = Decimal('0.00')
                tot_gan_haber = Decimal('0.00')
                tot_perd_debe = Decimal('0.00')
                tot_perd_haber = Decimal('0.00')

                # Para la fila "TOTALES DE GANANCIAS" queremos:
                # suma(mensual de 411/412/414 en +) + suma(mensual de 422 en negativo)
                tot_mes_gan = {m: Decimal('0.00') for m, _ in meses}
                # Para "TOTALES DE PERDIDAS": Debe - Haber (usualmente solo Debe)
                tot_mes_perd = {m: Decimal('0.00') for m, _ in meses}

                for numero, info in data.items():
                    if es_ganancia(numero):
                        tot_gan_debe += info['tot_debe']
                        tot_gan_haber += info['tot_haber']
                        for m, _ in meses:
                            pm = info['por_mes'][m]
                            # Ganancias:
                            # - Cuentas normales: usar HABER (positivo)
                            # - 422: usar -DEBE (negativo)
                            val_mes = (pm['haber'] if numero != 422 else -pm['debe'])
                            tot_mes_gan[m] += val_mes
                    else:
                        tot_perd_debe += info['tot_debe']
                        tot_perd_haber += info['tot_haber']
                        for m, _ in meses:
                            pm = info['por_mes'][m]
                            tot_mes_perd[m] += (pm['debe'] - pm['haber'])

                # Resultados por mes = Ganancias (netas) - Pérdidas (netas)
                resultados_mes = {m: (tot_mes_gan[m] - tot_mes_perd[m]) for m, _ in meses}
                resultado_total = (tot_gan_haber - tot_gan_debe) - (tot_perd_debe - tot_perd_haber)

                titulo = (
                    f"Balance de resultados entre el {fecha_desde.strftime('%d/%m/%Y')} "
                    f"y el {fecha_hasta.strftime('%d/%m/%Y')} en {titulo_moneda}"
                )

                output = _generar_excel_balance_evolutivo(
                    titulo, meses, data,
                    tot_gan_debe, tot_gan_haber,
                    tot_perd_debe, tot_perd_haber,
                    tot_mes_gan, tot_mes_perd,
                    resultados_mes, resultado_total
                )

                resp = HttpResponse(
                    output.getvalue(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                resp['Content-Disposition'] = (
                    f"attachment; filename=Balance_Evolutivo_{fecha_desde.strftime('%d%m%Y')}_a_{fecha_hasta.strftime('%d%m%Y')}.xlsx"
                )
                return resp
        else:
            form = BalanceEvolutivoForm()

        return render(request, 'contabilidad_ca/balance_evolutivo.html', {'form': form})

    except Exception:
        # En producción podrías loggear el error
        return render(request, 'contabilidad_ca/balance_evolutivo.html', {'form': BalanceEvolutivoForm()})


def _generar_excel_balance_evolutivo(
    titulo,
    meses,               # [(1,'January'),...,(12,'December')]
    data,                # dict por cuenta
    tot_gan_debe, tot_gan_haber,
    tot_perd_debe, tot_perd_haber,
    tot_mes_gan, tot_mes_perd,
    resultados_mes, resultado_total
):
    output = io.BytesIO()
    wb = xlsxwriter.Workbook(output, {'in_memory': True})
    ws = wb.add_worksheet("Balance Evolutivo")

    fmt_title = wb.add_format({'bold': True, 'font_size': 11})
    fmt_hdr = wb.add_format({'bold': True, 'bg_color': '#F2F2F2', 'border': 1})
    fmt_num = wb.add_format({'num_format': '#,##0.00', 'border': 1})
    fmt_txt = wb.add_format({'border': 1})
    fmt_sub = wb.add_format({'bold': True, 'border': 1})
    fmt_total = wb.add_format({'bold': True, 'bg_color': '#E8F5E9', 'border': 1, 'num_format': '#,##0.00'})
    fmt_total_txt = wb.add_format({'bold': True, 'bg_color': '#E8F5E9', 'border': 1})

    # Título
    ws.merge_range(0, 0, 0, 3 + 12, titulo, fmt_title)

    # Encabezados
    headers_base = ["Cuenta", "Nombre", "Debe", "Haber"]
    meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"]
    headers = headers_base + meses_es
    for col, h in enumerate(headers):
        ws.write(2, col, h, fmt_hdr)

    row = 3

    # Bloque: Ganancias (incluye 422)
    for numero in [n for n in data.keys() if es_ganancia(n)]:
        info = data[numero]
        ws.write(row, 0, numero, fmt_txt)
        ws.write(row, 1, info['nombre'], fmt_txt)
        ws.write_number(row, 2, float(info['tot_debe']), fmt_num)
        ws.write_number(row, 3, float(info['tot_haber']), fmt_num)

        for i, (m, _) in enumerate(meses, start=0):
            pm = info['por_mes'][m]
            # Para mostrar en las columnas mensuales:
            # - Ganancias comunes: HABER (positivo)
            # - 422: -DEBE (negativo)
            val = (pm['haber'] if numero != 422 else -pm['debe'])
            ws.write_number(row, 4 + i, float(val), fmt_num)
        row += 1

    # Totales de Ganancias (mensual = suma de filas de arriba, con 422 negativa)
    ws.write(row, 0, "", fmt_total_txt)
    ws.write(row, 1, "TOTALES DE GANANCIAS", fmt_total_txt)
    ws.write_number(row, 2, float(tot_gan_debe), fmt_total)
    ws.write_number(row, 3, float(tot_gan_haber), fmt_total)
    for i, (m, _) in enumerate(meses, start=0):
        ws.write_number(row, 4 + i, float(tot_mes_gan[m]), fmt_total)
    row += 2

    # Bloque: Pérdidas
    for numero in [n for n in data.keys() if not es_ganancia(n)]:
        info = data[numero]
        ws.write(row, 0, numero, fmt_txt)
        ws.write(row, 1, info['nombre'], fmt_txt)
        ws.write_number(row, 2, float(info['tot_debe']), fmt_num)
        ws.write_number(row, 3, float(info['tot_haber']), fmt_num)
        for i, (m, _) in enumerate(meses, start=0):
            pm = info['por_mes'][m]
            val = pm['debe']  # mostramos Debe mensual de cada cuenta de gasto
            ws.write_number(row, 4 + i, float(val), fmt_num)
        row += 1

    # Totales de Pérdidas (mensual neto = Debe - Haber)
    ws.write(row, 0, "", fmt_total_txt)
    ws.write(row, 1, "TOTALES DE PERDIDAS", fmt_total_txt)
    ws.write_number(row, 2, float(tot_perd_debe), fmt_total)
    ws.write_number(row, 3, float(tot_perd_haber), fmt_total)
    for i, (m, _) in enumerate(meses, start=0):
        ws.write_number(row, 4 + i, float(tot_mes_perd[m]), fmt_total)
    row += 2

    # Resultados (Ganancias - Pérdidas)
    ws.write(row, 0, "", fmt_sub)
    ws.write(row, 1, "RESULTADOS (+ GANANCIAS - PERDIDAS)", fmt_sub)
    ws.write(row, 2, "", fmt_sub)
    ws.write(row, 3, "", fmt_sub)
    for i, (m, _) in enumerate(meses, start=0):
        ws.write_number(row, 4 + i, float(resultados_mes[m]), fmt_total)
    row += 1

    # Ajuste ancho
    ws.set_column(0, 0, 10)
    ws.set_column(1, 1, 42)
    ws.set_column(2, 3, 14)
    ws.set_column(4, 4 + 11, 12)

    wb.close()
    output.seek(0)
    return output


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
