import datetime
import io
import time
from collections import defaultdict
from decimal import Decimal

import xlsxwriter
from MySQLdb.constants.FIELD_TYPE import DATETIME
from django.http import HttpResponse
from django.shortcuts import render

from administracion_contabilidad.models import Movims
from consultas_administrativas.forms import ReporteMovimientosForm, BalanceCuentasCobrarForm, BalanceMixtasForm
from consultas_administrativas.models import VReporteSubdiarioVentas, VCuentasCobrarBalance
from mantenimientos.models import Clientes

from decimal import Decimal
from collections import defaultdict
from datetime import datetime


def balance_mixtas_funciona(request):
    if request.method == 'POST':
        form = BalanceMixtasForm(request.POST)
        if form.is_valid():
            fecha_hasta = form.cleaned_data['fecha_hasta']
            moneda = form.cleaned_data['moneda']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            consolidar_moneda_nac = form.cleaned_data['consolidar_moneda_nac']

            # Tipos de movimientos
            tipos_ventas  = (20, 21, 23, 24, 25, 29)
            tipos_compras = (40, 41, 45, 42, 26)

            nombres = {}
            socios = {}
            saldos = defaultdict(Decimal)

            clientes = Clientes.objects.only(
                'codigo', 'empresa', 'fechadenegado', 'tipo', 'socio'
            ).order_by('empresa')

            for cli in clientes:
                cliente = cli.codigo
                nombres[cliente] = cli.empresa
                socios[cliente] = getattr(cli, 'socio', None)

                # ------------------- VENTAS -------------------
                filtro_v = {
                    'mcliente': cli.codigo,
                    'mactivo': 'S',
                    'mtipo__in': tipos_ventas,
                    'mfechamov__lte': fecha_hasta,
                }
                if moneda:
                    filtro_v['mmoneda'] = moneda.codigo
                if isinstance(cli.fechadenegado, datetime) and cli.tipo != 1:
                    filtro_v['mfechamov__gt'] = cli.fechadenegado

                movimientos_v = (
                    Movims.objects
                    .only('mfechamov', 'mtipo', 'mtotal', 'mmoneda', 'mcambio', 'marbitraje')
                    .filter(**filtro_v)
                    .order_by('mfechamov', 'id')
                )

                saldo_v = Decimal('0.00')
                if movimientos_v.exists():
                    for m in movimientos_v:
                        total = Decimal(m.mtotal or 0)
                        if m.mtipo in (20, 24, 29):
                            saldo_v += total
                        elif m.mtipo in (21, 25, 23):
                            saldo_v -= total

                # ------------------- COMPRAS -------------------
                filtro_c = {
                    'mcliente': cli.codigo,
                    'mactivo': 'S',
                    'mtipo__in': tipos_compras,
                    'mfechamov__lte': fecha_hasta,
                }
                if moneda:
                    filtro_c['mmoneda'] = moneda.codigo
                if isinstance(cli.fechadenegado, datetime) and cli.tipo != 1 and getattr(cli, 'socio', '') != 'T':
                    filtro_c['mfechamov__gt'] = cli.fechadenegado

                movimientos_c = (
                    Movims.objects
                    .only('mfechamov', 'mtipo', 'mtotal', 'mmoneda', 'mcambio', 'marbitraje', 'mserie')
                    .filter(**filtro_c)
                    .order_by('mfechamov', 'id')
                )

                saldo_c = Decimal('0.00')
                if movimientos_c.exists():
                    for m in movimientos_c:
                        if getattr(m, 'mserie', None) == 'P':
                            continue
                        total = Decimal(m.mtotal or 0)
                        if m.mtipo in (41, 45):
                            saldo_c += total
                        elif m.mtipo in (40, 42, 26):
                            saldo_c -= total

                # ------------------- SALDO MIXTO -------------------
                saldo = saldo_v + saldo_c

                if saldo != 0:
                    # Tomamos el último movimiento válido de cualquiera
                    movimiento = (
                        Movims.objects
                        .filter(mcliente=cli.codigo, mactivo='S', mfechamov__lte=fecha_hasta)
                        .order_by('-mfechamov', '-id')
                        .first()
                    )

                    if 'resultados' not in locals():
                        resultados = []

                    resultados.append({
                        "codigo": cliente,
                        "nombre": nombres[cliente],
                        "moneda": movimiento.mmoneda if movimiento else (moneda.codigo if moneda else None),
                        "saldo": saldo,
                        "arbitraje": movimiento.mcambio if movimiento else Decimal("1.0"),
                        "paridad": movimiento.marbitraje if movimiento else Decimal("1.0"),
                        "fecha": movimiento.mfechamov if movimiento else None
                    })

            if 'resultados' not in locals():
                resultados = []

            return generar_excel_balance_mixtas(
                resultados, fecha_hasta, moneda,
                consolidar_dolares, consolidar_moneda_nac
            )

    else:
        form = BalanceMixtasForm()

    return render(request, 'agentes_ca/balance_mixtas.html', {'form': form})


def generar_excel_balance_mixtas_funciona(queryset, fecha_hasta, moneda,
                                 consolidar_dolares=False,
                                 consolidar_moneda_nac=False):
    """
    Genera el Excel de Balance para MIXTAS (Ventas+Compras)
    - queryset: lista de dicts con keys: codigo, nombre, saldo, moneda, arbitraje, paridad
    - Usa convertir_monto(...) si hay consolidación de moneda
    """
    try:
        if consolidar_dolares:
            nombre_moneda = "DOLARES USA"
            moneda_destino = 2
        elif consolidar_moneda_nac:
            nombre_moneda = "MONEDA NACIONAL"
            moneda_destino = 1
        else:
            nombre_moneda = moneda.nombre.upper() if moneda else "TODAS LAS MONEDAS"
            moneda_destino = None

        fecha_formateada = fecha_hasta.strftime('%d/%m/%Y')
        titulo = f'Balance de Cuentas MIXTAS al {fecha_formateada} - {nombre_moneda}'
        nombre_archivo = f'Balance_Cuentas_Mixtas_{fecha_hasta}.xlsx'

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        ws = workbook.add_worksheet("Balance")

        # Formatos
        header_format = workbook.add_format({
            'bold': True, 'bg_color': '#d9d9d9',
            'border': 1, 'align': 'center'
        })
        title_format = workbook.add_format({'bold': True, 'font_size': 12})
        money_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        total_format = workbook.add_format({
            'bold': True, 'num_format': '#,##0.00',
            'top': 2, 'border': 1
        })
        total_label_format = workbook.add_format({'bold': True, 'top': 2, 'border': 1})
        text_format = workbook.add_format({'border': 1})

        # Título
        ws.merge_range('A1:C1', titulo, title_format)

        # Encabezados
        headers = ['Código', 'Nombre', 'Saldo']
        for col, h in enumerate(headers):
            ws.write(1, col, h, header_format)

        row = 2
        total_general = Decimal('0.00')

        # Orden por código ascendente (robusto ante str/int)
        def _as_int(v):
            try:
                return int(v)
            except Exception:
                return float('inf')

        queryset_sorted = sorted(
            queryset,
            key=lambda o: (
                _as_int(o.get("codigo") if isinstance(o, dict)
                        else getattr(o, "codigo", None)),
                str(o.get("codigo") if isinstance(o, dict)
                    else getattr(o, "codigo", ""))
            )
        )

        for obj in queryset_sorted:
            get = obj.get if isinstance(obj, dict) else lambda k, default=None: getattr(obj, k, default)

            saldo = Decimal(get("saldo") or 0)
            moneda_origen = get("moneda")

            arbitraje_val = get("arbitraje") or Decimal("1.0")
            paridad_val = get("paridad") or Decimal("1.0")

            arbitraje = Decimal(arbitraje_val)
            paridad = Decimal(paridad_val)

            if moneda_destino and moneda_origen != moneda_destino:
                saldo = convertir_monto(saldo, moneda_origen, moneda_destino, arbitraje, paridad)

            ws.write(row, 0, get("codigo"), text_format)
            ws.write(row, 1, get("nombre"), text_format)
            ws.write(row, 2, float(saldo), money_format)

            total_general += saldo
            row += 1

        # Total
        ws.write(row, 1, 'TOTAL GENERAL', total_label_format)
        ws.write(row, 2, float(total_general), total_format)

        # Anchos de columna
        ws.set_column('A:A', 10)
        ws.set_column('B:B', 40)
        ws.set_column('C:C', 18)

        workbook.close()
        output.seek(0)

        resp = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        resp['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
        return resp

    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel de balance mixtas: {e}")


def balance_mixtas_completo(request):
    if request.method == 'POST':
        form = BalanceMixtasForm(request.POST)
        if form.is_valid():
            fecha_hasta = form.cleaned_data['fecha_hasta']
            moneda = form.cleaned_data['moneda']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            consolidar_moneda_nac = form.cleaned_data['consolidar_moneda_nac']

            # Tipos de movimientos
            tipos_ventas  = (20, 21, 23, 24, 25, 29)
            tipos_compras = (40, 41, 45, 42, 26)

            resultados = []

            clientes = Clientes.objects.only(
                'codigo', 'empresa', 'fechadenegado', 'tipo', 'socio'
            ).order_by('empresa')

            for cli in clientes:
                cliente = cli.codigo
                nombre_cli = cli.empresa

                # ------------------- VENTAS -------------------
                filtro_v = {
                    'mcliente': cli.codigo,
                    'mactivo': 'S',
                    'mtipo__in': tipos_ventas,
                    'mfechamov__lte': fecha_hasta,
                }
                if moneda:
                    filtro_v['mmoneda'] = moneda.codigo
                if isinstance(cli.fechadenegado, datetime) and cli.tipo != 1:
                    filtro_v['mfechamov__gt'] = cli.fechadenegado

                movimientos_v = (
                    Movims.objects
                    .only('mfechamov', 'mtipo', 'mtotal', 'mmoneda', 'mcambio', 'marbitraje')
                    .filter(**filtro_v)
                    .order_by('mfechamov', 'id')
                )

                # deudor: suma de TODOS los movimientos de ventas (20,21,23,24,25,29)
                deudor = Decimal('0.00')
                saldo_v = Decimal('0.00')
                for m in movimientos_v:
                    total = Decimal(m.mtotal or 0)
                    deudor += total  # columna Deudor según tu definición
                    # saldo ventas (debe - haber)
                    if m.mtipo in (20, 24, 29):
                        saldo_v += total
                    elif m.mtipo in (21, 25, 23):
                        saldo_v -= total

                # ------------------- COMPRAS -------------------
                filtro_c = {
                    'mcliente': cli.codigo,
                    'mactivo': 'S',
                    'mtipo__in': tipos_compras,
                    'mfechamov__lte': fecha_hasta,
                }
                if moneda:
                    filtro_c['mmoneda'] = moneda.codigo
                if isinstance(cli.fechadenegado, datetime) and cli.tipo != 1 and getattr(cli, 'socio', '') != 'T':
                    filtro_c['mfechamov__gt'] = cli.fechadenegado

                movimientos_c = (
                    Movims.objects
                    .only('mfechamov', 'mtipo', 'mtotal', 'mmoneda', 'mcambio', 'marbitraje', 'mserie')
                    .filter(**filtro_c)
                    .order_by('mfechamov', 'id')
                )

                # acreedor: suma de TODOS los movimientos de compras (40,41,45,42,26)
                acreedor = Decimal('0.00')
                saldo_c = Decimal('0.00')
                for m in movimientos_c:
                    # Para saldo se excluye 'P'; para columna acreedor mantenemos misma exclusión por consistencia
                    if getattr(m, 'mserie', None) == 'P':
                        continue
                    total = Decimal(m.mtotal or 0)
                    acreedor += total  # columna Acreedor según tu definición
                    # saldo compras (debe - haber), excluyendo 'P'
                    if m.mtipo in (41, 45):
                        saldo_c += total
                    elif m.mtipo in (40, 42, 26):
                        saldo_c -= total

                # ------------------- SALDO MIXTO -------------------
                saldo = saldo_v + saldo_c

                if saldo !=0:

                    # Tomamos el último movimiento válido de cualquiera para moneda/cambios
                    movimiento = (
                        Movims.objects
                        .filter(mcliente=cli.codigo, mactivo='S', mfechamov__lte=fecha_hasta)
                        .order_by('-mfechamov', '-id')
                        .first()
                    )

                    resultados.append({
                        "codigo": cliente,
                        "nombre": nombre_cli,
                        "moneda": movimiento.mmoneda if movimiento else (moneda.codigo if moneda else None),
                        "deudor": deudor,
                        "acreedor": acreedor,
                        "saldo": saldo,
                        "arbitraje": (getattr(movimiento, 'mcambio', None) or Decimal("1.0")) if movimiento else Decimal("1.0"),
                        "paridad": (getattr(movimiento, 'marbitraje', None) or Decimal("1.0")) if movimiento else Decimal("1.0"),
                        "fecha": getattr(movimiento, 'mfechamov', None) if movimiento else None
                    })

            return generar_excel_balance_mixtas(
                resultados, fecha_hasta, moneda,
                consolidar_dolares, consolidar_moneda_nac
            )

    else:
        form = BalanceMixtasForm()

    return render(request, 'agentes_ca/balance_mixtas.html', {'form': form})


def generar_excel_balance_mixtas_completo(queryset, fecha_hasta, moneda,
                                 consolidar_dolares=False,
                                 consolidar_moneda_nac=False):
    """
    Genera el Excel de Balance para MIXTAS (Ventas+Compras)
    - queryset: lista de dicts con keys: codigo, nombre, deudor, acreedor, saldo, moneda, arbitraje, paridad
    - Usa convertir_monto(...) si hay consolidación de moneda para las 3 columnas
    """
    try:
        if consolidar_dolares:
            nombre_moneda = "DOLARES USA"
            moneda_destino = 2
        elif consolidar_moneda_nac:
            nombre_moneda = "MONEDA NACIONAL"
            moneda_destino = 1
        else:
            nombre_moneda = moneda.nombre.upper() if moneda else "TODAS LAS MONEDAS"
            moneda_destino = None

        fecha_formateada = fecha_hasta.strftime('%d/%m/%Y')
        titulo = f'Balance de Cuentas MIXTAS al {fecha_formateada} - {nombre_moneda}'
        nombre_archivo = f'Balance_Cuentas_Mixtas_{fecha_hasta}.xlsx'

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        ws = workbook.add_worksheet("Balance")

        # Formatos
        header_format = workbook.add_format({
            'bold': True, 'bg_color': '#d9d9d9',
            'border': 1, 'align': 'center'
        })
        title_format = workbook.add_format({'bold': True, 'font_size': 12})
        money_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        total_format = workbook.add_format({
            'bold': True, 'num_format': '#,##0.00',
            'top': 2, 'border': 1
        })
        total_label_format = workbook.add_format({'bold': True, 'top': 2, 'border': 1})
        text_format = workbook.add_format({'border': 1})

        # Título
        ws.merge_range('A1:E1', titulo, title_format)

        # Encabezados
        headers = ['Código', 'Nombre', 'Deudor', 'Acreedor', 'Saldo']
        for col, h in enumerate(headers):
            ws.write(1, col, h, header_format)

        row = 2
        total_deudor = Decimal('0.00')
        total_acreedor = Decimal('0.00')
        total_saldo = Decimal('0.00')

        # Orden por código ascendente (robusto ante str/int)
        def _as_int(v):
            try:
                return int(v)
            except Exception:
                return float('inf')

        queryset_sorted = sorted(
            queryset,
            key=lambda o: (
                _as_int(o.get("codigo") if isinstance(o, dict)
                        else getattr(o, "codigo", None)),
                str(o.get("codigo") if isinstance(o, dict)
                    else getattr(o, "codigo", ""))
            )
        )

        for obj in queryset_sorted:
            get = obj.get if isinstance(obj, dict) else (lambda k, default=None: getattr(obj, k, default))

            # Valores base
            deudor   = Decimal(get("deudor")   or 0)
            acreedor = Decimal(get("acreedor") or 0)
            saldo    = Decimal(get("saldo")    or 0)

            moneda_origen = get("moneda")
            arbitraje = Decimal(get("arbitraje") or "1.0")
            paridad   = Decimal(get("paridad")   or "1.0")

            # Conversión si corresponde (por columna)
            if moneda_destino and moneda_origen != moneda_destino:
                deudor   = convertir_monto(deudor,   moneda_origen, moneda_destino, arbitraje, paridad)
                acreedor = convertir_monto(acreedor, moneda_origen, moneda_destino, arbitraje, paridad)
                saldo    = convertir_monto(saldo,    moneda_origen, moneda_destino, arbitraje, paridad)

            # Escribir fila
            ws.write(row, 0, get("codigo"), text_format)
            ws.write(row, 1, get("nombre"), text_format)
            ws.write(row, 2, float(deudor),   money_format)
            ws.write(row, 3, float(acreedor), money_format)
            ws.write(row, 4, float(saldo),    money_format)

            total_deudor   += deudor
            total_acreedor += acreedor
            total_saldo    += saldo
            row += 1

        # Totales
        ws.write(row, 1, 'TOTAL GENERAL', total_label_format)
        ws.write(row, 2, float(total_deudor),   total_format)
        ws.write(row, 3, float(total_acreedor), total_format)
        ws.write(row, 4, float(total_saldo),    total_format)

        # Anchos de columna
        ws.set_column('A:A', 10)
        ws.set_column('B:B', 40)
        ws.set_column('C:E', 18)

        workbook.close()
        output.seek(0)

        resp = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        resp['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
        return resp

    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel de balance mixtas: {e}")


from decimal import Decimal
from collections import defaultdict
from datetime import datetime
import io
import xlsxwriter
from django.http import HttpResponse

def balance_mixtas(request):
    if request.method == 'POST':
        form = BalanceMixtasForm(request.POST)
        if form.is_valid():
            fecha_hasta = form.cleaned_data['fecha_hasta']
            moneda = form.cleaned_data['moneda']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            consolidar_moneda_nac = form.cleaned_data['consolidar_moneda_nac']

            # Tipos de movimientos
            tipos_ventas  = (20, 21, 23, 24, 25, 29)
            tipos_compras = (40, 41, 45, 42, 26)

            resultados = []

            clientes = Clientes.objects.only(
                'codigo', 'empresa', 'fechadenegado', 'tipo', 'socio'
            ).order_by('empresa')

            for cli in clientes:
                cliente = cli.codigo
                nombre_cli = cli.empresa

                # ------------------- VENTAS -------------------
                filtro_v = {
                    'mcliente': cli.codigo,
                    'mactivo': 'S',
                    'mtipo__in': tipos_ventas,
                    'mfechamov__lte': fecha_hasta,
                }
                if moneda:
                    filtro_v['mmoneda'] = moneda.codigo
                if isinstance(cli.fechadenegado, datetime) and cli.tipo != 1:
                    filtro_v['mfechamov__gt'] = cli.fechadenegado

                movimientos_v = (
                    Movims.objects
                    .only('mfechamov', 'mtipo', 'mtotal', 'mmoneda', 'mcambio', 'marbitraje')
                    .filter(**filtro_v)
                    .order_by('mfechamov', 'id')
                )

                # deudor_firmado: con el mismo signo que aporta al saldo
                deudor_firmado = Decimal('0.00')
                saldo_v = Decimal('0.00')
                for m in movimientos_v:
                    total = Decimal(m.mtotal or 0)
                    if m.mtipo in (20, 24, 29):
                        saldo_v += total
                        deudor_firmado += total     # suma al saldo => positivo
                    elif m.mtipo in (21, 25, 23):
                        saldo_v -= total
                        deudor_firmado -= total     # resta al saldo => negativo

                # ------------------- COMPRAS -------------------
                filtro_c = {
                    'mcliente': cli.codigo,
                    'mactivo': 'S',
                    'mtipo__in': tipos_compras,
                    'mfechamov__lte': fecha_hasta,
                }
                if moneda:
                    filtro_c['mmoneda'] = moneda.codigo
                if isinstance(cli.fechadenegado, datetime) and cli.tipo != 1 and getattr(cli, 'socio', '') != 'T':
                    filtro_c['mfechamov__gt'] = cli.fechadenegado

                movimientos_c = (
                    Movims.objects
                    .only('mfechamov', 'mtipo', 'mtotal', 'mmoneda', 'mcambio', 'marbitraje', 'mserie')
                    .filter(**filtro_c)
                    .order_by('mfechamov', 'id')
                )

                # acreedor_firmado: con el mismo signo que aporta al saldo (excluye 'P')
                acreedor_firmado = Decimal('0.00')
                saldo_c = Decimal('0.00')
                for m in movimientos_c:
                    if getattr(m, 'mserie', None) == 'P':
                        continue
                    total = Decimal(m.mtotal or 0)
                    if m.mtipo in (41, 45):
                        saldo_c += total
                        acreedor_firmado += total   # suma al saldo => positivo
                    elif m.mtipo in (40, 42, 26):
                        saldo_c -= total
                        acreedor_firmado -= total   # resta al saldo => negativo

                # ------------------- SALDO MIXTO -------------------
                saldo = saldo_v + saldo_c

                # Mostrar solo si saldo ≠ 0 (manteniendo tu criterio previo)
                if saldo != 0:
                    movimiento = (
                        Movims.objects
                        .filter(mcliente=cli.codigo, mactivo='S', mfechamov__lte=fecha_hasta)
                        .order_by('-mfechamov', '-id')
                        .first()
                    )

                    resultados.append({
                        "codigo": cliente,
                        "nombre": nombre_cli,
                        "moneda": movimiento.mmoneda if movimiento else (moneda.codigo if moneda else None),
                        "deudor": deudor_firmado,
                        "acreedor": acreedor_firmado,
                        "saldo": saldo,
                        "arbitraje": (getattr(movimiento, 'mcambio', None) or Decimal("1.0")) if movimiento else Decimal("1.0"),
                        "paridad": (getattr(movimiento, 'marbitraje', None) or Decimal("1.0")) if movimiento else Decimal("1.0"),
                        "fecha": getattr(movimiento, 'mfechamov', None) if movimiento else None
                    })

            return generar_excel_balance_mixtas(
                resultados, fecha_hasta, moneda,
                consolidar_dolares, consolidar_moneda_nac
            )

    else:
        form = BalanceMixtasForm()

    return render(request, 'agentes_ca/balance_mixtas.html', {'form': form})


def generar_excel_balance_mixtas(queryset, fecha_hasta, moneda,
                                 consolidar_dolares=False,
                                 consolidar_moneda_nac=False):
    """
    Genera el Excel de Balance para MIXTAS (Ventas+Compras)
    - queryset: lista de dicts con keys: codigo, nombre, deudor, acreedor, saldo, moneda, arbitraje, paridad
    - Convierte moneda (si aplica) para las 3 columnas, preservando el signo.
    """
    try:
        if consolidar_dolares:
            nombre_moneda = "DOLARES USA"
            moneda_destino = 2
        elif consolidar_moneda_nac:
            nombre_moneda = "MONEDA NACIONAL"
            moneda_destino = 1
        else:
            nombre_moneda = moneda.nombre.upper() if moneda else "TODAS LAS MONEDAS"
            moneda_destino = None

        fecha_formateada = fecha_hasta.strftime('%d/%m/%Y')
        titulo = f'Balance de Cuentas MIXTAS al {fecha_formateada} - {nombre_moneda}'
        nombre_archivo = f'Balance_Cuentas_Mixtas_{fecha_hasta}.xlsx'

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        ws = workbook.add_worksheet("Balance")

        # Formatos
        header_format = workbook.add_format({'bold': True, 'bg_color': '#d9d9d9',
                                             'border': 1, 'align': 'center'})
        title_format = workbook.add_format({'bold': True, 'font_size': 12})
        money_format = workbook.add_format({
            'num_format': '#,##0.00;[Blue]-#,##0.00',
            'border': 1
        })
        total_format = workbook.add_format({
            'bold': True,
            'num_format': '#,##0.00;[Blue]-#,##0.00',
            'top': 2, 'border': 1
        })

        total_label_format = workbook.add_format({'bold': True, 'top': 2, 'border': 1})
        text_format = workbook.add_format({'border': 1})

        # Título
        ws.merge_range('A1:E1', titulo, title_format)

        # Encabezados
        headers = ['Código', 'Nombre', 'Deudor', 'Acreedor', 'Saldo']
        for col, h in enumerate(headers):
            ws.write(1, col, h, header_format)

        row = 2
        total_deudor = Decimal('0.00')
        total_acreedor = Decimal('0.00')
        total_saldo = Decimal('0.00')

        # Ordenar por código (ascendente, robusto)
        def _as_int(v):
            try:
                return int(v)
            except Exception:
                return float('inf')

        queryset_sorted = sorted(
            queryset,
            key=lambda o: (
                _as_int(o.get("codigo") if isinstance(o, dict) else getattr(o, "codigo", None)),
                str(o.get("codigo") if isinstance(o, dict) else getattr(o, "codigo", ""))
            )
        )

        for obj in queryset_sorted:
            get = obj.get if isinstance(obj, dict) else (lambda k, default=None: getattr(obj, k, default))

            deudor   = Decimal(get("deudor")   or 0)
            acreedor = Decimal(get("acreedor") or 0)
            saldo    = Decimal(get("saldo")    or 0)

            moneda_origen = get("moneda")
            arbitraje = Decimal(get("arbitraje") or "1.0")
            paridad   = Decimal(get("paridad")   or "1.0")

            # Conversión (mantiene signo)
            if moneda_destino and moneda_origen != moneda_destino:
                deudor   = convertir_monto(deudor,   moneda_origen, moneda_destino, arbitraje, paridad)
                acreedor = convertir_monto(acreedor, moneda_origen, moneda_destino, arbitraje, paridad)
                saldo    = convertir_monto(saldo,    moneda_origen, moneda_destino, arbitraje, paridad)

            # Escribir fila
            ws.write(row, 0, get("codigo"), text_format)
            ws.write(row, 1, get("nombre"), text_format)
            ws.write(row, 2, float(deudor),   money_format)
            ws.write(row, 3, float(acreedor), money_format)
            ws.write(row, 4, float(saldo),    money_format)

            total_deudor   += deudor
            total_acreedor += acreedor
            total_saldo    += saldo
            row += 1

        # Totales
        ws.write(row, 1, 'TOTAL GENERAL', total_label_format)
        ws.write(row, 2, float(total_deudor),   total_format)
        ws.write(row, 3, float(total_acreedor), total_format)
        ws.write(row, 4, float(total_saldo),    total_format)

        # Anchos
        ws.set_column('A:A', 10)
        ws.set_column('B:B', 40)
        ws.set_column('C:E', 18)

        workbook.close()
        output.seek(0)

        return HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
        )

    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel de balance mixtas: {e}")



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



