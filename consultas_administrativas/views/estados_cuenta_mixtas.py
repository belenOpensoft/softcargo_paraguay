from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
import io

import xlsxwriter
from django.db.models import OuterRef, Sum, Subquery, ExpressionWrapper, F, DecimalField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render

from administracion_contabilidad.models import Movims, Asientos, Impuvtas, Boleta, Impucompras
from consultas_administrativas.forms import ReporteCobranzasForm, AntiguedadSaldosForm, EstadoCuentaForm, \
    EstadoCuentaMixtasForm
from consultas_administrativas.models import VAntiguedadSaldos
from mantenimientos.models import Clientes

from datetime import date, datetime

def estados_cuenta_mixtas(request):
    if request.method == 'POST':
        form = EstadoCuentaMixtasForm(request.POST)
        if form.is_valid():
            tipo_consulta = form.cleaned_data['tipo_consulta']
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            moneda = form.cleaned_data['moneda']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            consolidar_moneda_nac = form.cleaned_data['consolidar_moneda_nac']
            omitir_saldos_cero = form.cleaned_data['omitir_saldos_cero']
            cliente = None

            if tipo_consulta == 'individual':
                cliente = form.cleaned_data['cliente_codigo']
                datos = obtener_estado_individual(form,fecha_desde, fecha_hasta, moneda)
            else:
                datos = obtener_estado_general(form,fecha_desde, fecha_hasta, moneda)

            return generar_excel_estados_cuenta_mixto(
                datos,
                fecha_desde,
                fecha_hasta,
                moneda,
                consolidar_dolares,
                consolidar_moneda_nac,
                omitir_saldos_cero,
                cliente
            )
    else:
        form = EstadoCuentaMixtasForm()

    return render(request, 'agentes_ca/estados_cuenta.html', {'form': form})

# Conjuntos por claridad
TIPOS_VENTAS  = (20, 21, 23, 24, 25, 29)
TIPOS_COMPRAS = (40, 41, 42, 45, 26)
TIPOS_MIXTAS  = TIPOS_VENTAS + TIPOS_COMPRAS


def obtener_estado_individual(form, fecha_desde, fecha_hasta, moneda):
    """
    Estado de cuenta mixto (ventas + compras) para un cliente específico.
    - Estructura igual a tus funciones actuales (ventas/compras).
    - Excluye mserie == 'P' SOLO en movimientos de COMPRAS.
    """
    cliente = form.cleaned_data['cliente_codigo']
    cliente_nombre = form.cleaned_data['cliente']
    todas_monedas = form.cleaned_data.get('todas_las_monedas', False)

    if not cliente:
        return {}

    cliente_ob = Clientes.objects.only('fechadenegado', 'tipo', 'socio').filter(codigo=cliente).first()
    if not cliente_ob:
        return {}

    filtro_base = {
        'mfechamov__lte': fecha_hasta,
        'mfechamov__gte': fecha_desde,
        'mcliente': cliente,
        'mactivo': 'S',
        'mtipo__in': TIPOS_MIXTAS
    }

    # Ventana por fecha de negado (igual criterio que ventas; si querés incluir socio!='T', lo agregamos)
    if cliente_ob.tipo != 1 and isinstance(cliente_ob.fechadenegado, datetime):
        filtro_base['mfechamov__gt'] = cliente_ob.fechadenegado

    movimientos = Movims.objects.filter(**filtro_base).only(
        'mcliente', 'mfechamov', 'mnombre', 'mtotal', 'msaldo', 'mnombremov',
        'mtipo', 'mserie', 'mboleta', 'mprefijo', 'mautogen', 'mdetalle', 'mmoneda'
    ).order_by('mfechamov')

    if not todas_monedas and moneda:
        movimientos = movimientos.filter(mmoneda=moneda.codigo)

    autogen_list = movimientos.values_list('mautogen', flat=True).distinct()
    asientos = Asientos.objects.filter(
        autogenerado__in=autogen_list,
        imputacion=2
    ).only('autogenerado', 'vto', 'posicion', 'cuenta')
    asientos_dict = {a.autogenerado: a for a in asientos}
    # Ventas → Impuvtas
    impuvtas = Impuvtas.objects.filter(autofac__in=autogen_list).values('autofac', 'autogen')
    pagos_ids_vta = [i['autogen'] for i in impuvtas]
    pagos_movs_vta = Movims.objects.filter(mautogen__in=pagos_ids_vta).only(
        'mautogen', 'mboleta', 'mserie', 'mprefijo', 'mfechamov'
    )
    pagos_dict_vta = {m.mautogen: m for m in pagos_movs_vta}
    pagos_por_factura_vta = {}
    for i in impuvtas:
        pagos_por_factura_vta.setdefault(i['autofac'], []).append(i['autogen'])

    # Compras → Impucompras
    impucompras = Impucompras.objects.filter(autofac__in=autogen_list).values('autofac', 'autogen')
    pagos_ids_cmp = [i['autogen'] for i in impucompras]
    pagos_movs_cmp = Movims.objects.filter(mautogen__in=pagos_ids_cmp).only(
        'mautogen', 'mboleta', 'mserie', 'mprefijo', 'mfechamov'
    )
    pagos_dict_cmp = {m.mautogen: m for m in pagos_movs_cmp}
    pagos_por_factura_cmp = {}
    for i in impucompras:
        pagos_por_factura_cmp.setdefault(i['autofac'], []).append(i['autogen'])

    datos = {
        cliente: {
            'datos_cliente': [{
                'nombre': cliente_nombre,
                'codigo': cliente,
            }],
            'movimientos': []
        }
    }

    # for m in movimientos:
    #     # Excluir 'P' SOLO para movimientos de compras
    #     if m.mtipo in TIPOS_COMPRAS and getattr(m, 'mserie', None) == 'P':
    #         continue
    #
    #     asiento = asientos_dict.get(m.mautogen)
    #     datos[cliente]['movimientos'].append({
    #         'fecha': m.mfechamov,
    #         'tipo': m.mnombremov,
    #         'numero_tipo': m.mtipo,
    #         'documento': f"{m.mserie or ''}{m.mprefijo or ''}{m.mboleta or ''}",
    #         'vencimiento': asiento.vto if asiento else None,
    #         'detalle': m.mdetalle,
    #         'total': m.mtotal,
    #         'saldo': m.msaldo,
    #         'posicion': asiento.posicion if asiento else None,
    #         'cuenta': asiento.cuenta if asiento else None,
    #     })

    for m in movimientos:
        # Excluir 'P' SOLO para movimientos de compras
        if m.mtipo in TIPOS_COMPRAS and getattr(m, 'mserie', None) == 'P':
            continue

        asiento = asientos_dict.get(m.mautogen)

        pago = ''
        signo = ''
        numero_pago = ''
        fecha_pago = ''

        # Según tipo → buscamos en ventas o compras
        if m.mtipo in TIPOS_VENTAS:
            pagos_ids = pagos_por_factura_vta.get(m.mautogen, [])
            pagos_dict = pagos_dict_vta
        elif m.mtipo in TIPOS_COMPRAS:
            pagos_ids = pagos_por_factura_cmp.get(m.mautogen, [])
            pagos_dict = pagos_dict_cmp
        else:
            pagos_ids = []
            pagos_dict = {}

        if pagos_ids:
            if m.msaldo == 0:
                pago, signo = 'OK', '(*)'
            else:
                pago, signo = 'Parcial', '(+)'

            for pid in pagos_ids:
                mov = pagos_dict.get(pid)
                if not mov:
                    continue

                numero_pago += str(mov.mboleta) + ';'

                if mov.mfechamov:
                    fecha = mov.mfechamov.strftime('%d/%m/%Y')
                    fecha_pago += str(fecha) + ';'

        else:
            pago = 'No' if m.mtipo != 25 and m.mtipo!=45 else ''
        # Documento principal
        numero_completo = ''
        if m.mserie and m.mprefijo and m.mboleta:
            s = str(m.mserie)
            p = str(m.mprefijo)
            tz = len(s) - len(s.rstrip('0'))
            lz = len(p) - len(p.lstrip('0'))
            sep = '0' * max(0, 3 - (tz + lz))
            numero_completo = f"{s}{sep}{p}-{m.mboleta} "

        datos[cliente]['movimientos'].append({
            'fecha': m.mfechamov,
            'tipo': m.mnombremov,
            'numero_tipo': m.mtipo,
            'documento': numero_completo + signo,
            'vencimiento': asiento.vto if asiento else None,
            'detalle': m.mdetalle,
            'total': m.mtotal,
            'saldo': m.msaldo,
            'numero_pago': numero_pago,
            'pago': pago,
            'fecha_pago': fecha_pago,
            'posicion': asiento.posicion if asiento else None,
            'cuenta': asiento.cuenta if asiento else None,
        })

    return datos

def obtener_estado_general(form, fecha_desde, fecha_hasta, moneda):
    """
    Estado de cuenta mixto (ventas + compras) para TODOS los clientes (según filtro_tipo),
    con misma estructura que tus funciones actuales.
    - Excluye mserie == 'P' SOLO en tipos de compras.
    """
    filtro_tipo = form.cleaned_data.get('filtro_tipo')  # 'clientes', 'agentes', 'transportistas' (según tu uso en ventas)
    omitir_saldos_cero = form.cleaned_data.get('omitir_saldos_cero', False)  # por si luego lo usás
    todas_monedas = form.cleaned_data.get('todas_las_monedas', False)

    datos = {}
    clientes = Clientes.objects.only('codigo', 'empresa', 'fechadenegado', 'tipo', 'socio').order_by('empresa')

    for cli in clientes:
        # Respeta los mismos filtros que usás en ventas (ajustá si querés otros)
        if filtro_tipo == 'clientes' and cli.tipo != 1:
            continue
        elif filtro_tipo == 'agentes' and cli.tipo != 6:
            continue
        elif filtro_tipo == 'transportistas' and cli.tipo != 5:
            continue

        cliente_id = cli.codigo

        filtro_base = {
            'mfechamov__lte': fecha_hasta,
            'mfechamov__gte': fecha_desde,
            'mcliente': cliente_id,
            'mactivo': 'S',
            'mtipo__in': TIPOS_MIXTAS
        }

        if not todas_monedas and moneda:
            filtro_base['mmoneda'] = moneda.codigo

        # Ventana por fecha de negado (igual criterio que ventas; si querés incluir socio!='T', lo agregamos)
        if isinstance(cli.fechadenegado, datetime) and cli.tipo != 1:
            filtro_base['mfechamov__gt'] = cli.fechadenegado

        movimientos = Movims.objects.filter(**filtro_base).only(
            'mcliente', 'mfechamov', 'mnombre', 'mtotal', 'msaldo', 'mnombremov',
            'mtipo', 'mserie', 'mboleta', 'mprefijo', 'mautogen', 'mdetalle', 'mmoneda'
        ).order_by('mfechamov')

        if not movimientos.exists():
            continue

        autogen_list = movimientos.values_list('mautogen', flat=True).distinct()
        asientos = Asientos.objects.filter(
            autogenerado__in=autogen_list,
            imputacion=2
        ).only('autogenerado', 'vto', 'posicion', 'cuenta')
        asientos_dict = {a.autogenerado: a for a in asientos}

        datos[cliente_id] = {
            'datos_cliente': [{
                'nombre': cli.empresa,
                'codigo': cliente_id,
            }],
            'movimientos': []
        }

        # Ventas → Impuvtas
        impuvtas = Impuvtas.objects.filter(autofac__in=autogen_list).values('autofac', 'autogen')
        pagos_ids_vta = [i['autogen'] for i in impuvtas]
        pagos_movs_vta = Movims.objects.filter(mautogen__in=pagos_ids_vta).only(
            'mautogen', 'mboleta', 'mserie', 'mprefijo', 'mfechamov'
        )
        pagos_dict_vta = {m.mautogen: m for m in pagos_movs_vta}
        pagos_por_factura_vta = {}
        for i in impuvtas:
            pagos_por_factura_vta.setdefault(i['autofac'], []).append(i['autogen'])

        # Compras → Impucompras
        impucompras = Impucompras.objects.filter(autofac__in=autogen_list).values('autofac', 'autogen')
        pagos_ids_cmp = [i['autogen'] for i in impucompras]
        pagos_movs_cmp = Movims.objects.filter(mautogen__in=pagos_ids_cmp).only(
            'mautogen', 'mboleta', 'mserie', 'mprefijo', 'mfechamov'
        )
        pagos_dict_cmp = {m.mautogen: m for m in pagos_movs_cmp}
        pagos_por_factura_cmp = {}
        for i in impucompras:
            pagos_por_factura_cmp.setdefault(i['autofac'], []).append(i['autogen'])
        #
        # for m in movimientos:
        #     # Excluir 'P' SOLO para movimientos de compras
        #     if m.mtipo in TIPOS_COMPRAS and getattr(m, 'mserie', None) == 'P':
        #         continue
        #
        #     asiento = asientos_dict.get(m.mautogen)
        #     datos[cliente_id]['movimientos'].append({
        #         'fecha': m.mfechamov,
        #         'tipo': m.mnombremov,
        #         'numero_tipo': m.mtipo,
        #         'documento': f"{m.mserie or ''}{m.mprefijo or ''}{m.mboleta or ''}",
        #         'vencimiento': asiento.vto if asiento else None,
        #         'detalle': m.mdetalle,
        #         'total': m.mtotal,
        #         'saldo': m.msaldo,
        #         'posicion': asiento.posicion if asiento else None,
        #         'cuenta': asiento.cuenta if asiento else None,
        #     })

        for m in movimientos:
            # Excluir 'P' SOLO para movimientos de compras
            if m.mtipo in TIPOS_COMPRAS and getattr(m, 'mserie', None) == 'P':
                continue

            asiento = asientos_dict.get(m.mautogen)

            pago = ''
            signo = ''
            numero_pago = ''
            fecha_pago = ''

            # ---------------------------
            # Ventas → usar Impuvtas
            # ---------------------------
            if m.mtipo in TIPOS_VENTAS:
                pagos_ids = pagos_por_factura_vta.get(m.mautogen, [])
                pagos_dict = pagos_dict_vta

            # ---------------------------
            # Compras → usar Impucompras
            # ---------------------------
            elif m.mtipo in TIPOS_COMPRAS:
                pagos_ids = pagos_por_factura_cmp.get(m.mautogen, [])
                pagos_dict = pagos_dict_cmp

            else:
                pagos_ids = []
                pagos_dict = {}

            if pagos_ids:
                if m.msaldo == 0:
                    pago, signo = 'OK', '(*)'
                else:
                    pago, signo = 'Parcial', '(+)'

                for pid in pagos_ids:
                    mov = pagos_dict.get(pid)
                    if not mov:
                        continue

                    numero_pago += str(mov.mboleta) + ';'

                    if mov.mfechamov:
                        fecha = m.mfechamov.strftime('%d/%m/%Y')
                        fecha_pago += str(fecha) + ';'
            else:
                pago = 'No' if m.mtipo != 25 and m.mtipo!=45 else ''
            # Documento de la factura/nota
            numero_completo = ''
            if m.mserie and m.mprefijo and m.mboleta:
                s = str(m.mserie)
                p = str(m.mprefijo)
                tz = len(s) - len(s.rstrip('0'))
                lz = len(p) - len(p.lstrip('0'))
                sep = '0' * max(0, 3 - (tz + lz))
                numero_completo = f"{s}{sep}{p}-{m.mboleta} "

            datos[cliente_id]['movimientos'].append({
                'fecha': m.mfechamov,
                'tipo': m.mnombremov,
                'numero_tipo': m.mtipo,
                'documento': numero_completo + signo,
                'vencimiento': asiento.vto if asiento else None,
                'detalle': m.mdetalle,
                'total': m.mtotal,
                'saldo': m.msaldo,
                'numero_pago': numero_pago,
                'pago': pago,
                'fecha_pago': fecha_pago,
                'posicion': asiento.posicion if asiento else None,
                'cuenta': asiento.cuenta if asiento else None,
            })

    return datos


def calcular_saldos_anteriores_mixto(fecha_desde, moneda=None, cliente_id=None):
    """
    Devuelve un diccionario con el saldo acumulado (VENTAS + COMPRAS) anterior a fecha_desde.
    - Respeta reglas de cada módulo:
        * Ventas: no excluye mserie='P'; ventana por negado si cli.tipo != 1.
        * Compras: excluye mserie='P'; ventana por negado si cli.tipo != 1 y cli.socio != 'T'.
    - Si cliente_id es None → devuelve todos los clientes.
    - Si cliente_id está definido → devuelve solo ese cliente.
    Formato: { codigo: { 'saldo': Decimal, 'nombre': str } }
    """
    TIPOS_VENTAS  = (20, 21, 23, 24, 25, 29)
    TIPOS_COMPRAS = (40, 41, 45, 42, 26)

    clientes_qs = Clientes.objects.only('codigo', 'empresa', 'fechadenegado', 'tipo', 'socio').order_by('empresa')
    if cliente_id:
        clientes_qs = clientes_qs.filter(codigo=cliente_id)

    saldos = {}

    for cli in clientes_qs:
        # ------- VENTAS -------
        filtro_ventas = {
            'mfechamov__lt': fecha_desde,
            'mcliente': cli.codigo,
            'mactivo': 'S',
            'mtipo__in': TIPOS_VENTAS,
        }
        if moneda:
            filtro_ventas['mmoneda'] = moneda.codigo
        if isinstance(cli.fechadenegado, datetime) and cli.tipo != 1:
            filtro_ventas['mfechamov__gt'] = cli.fechadenegado

        mov_ventas = Movims.objects.filter(**filtro_ventas).only('mtipo', 'mtotal')  # no excluye mserie='P'

        saldo_v = Decimal('0.00')
        for m in mov_ventas:
            total = Decimal(m.mtotal or 0)
            if m.mtipo in (20, 24, 29):
                saldo_v += total
            elif m.mtipo in (21, 25, 23):
                saldo_v -= total

        # ------- COMPRAS -------
        filtro_compras = {
            'mfechamov__lt': fecha_desde,
            'mcliente': cli.codigo,
            'mactivo': 'S',
            'mtipo__in': TIPOS_COMPRAS,
        }
        if moneda:
            filtro_compras['mmoneda'] = moneda.codigo
        if isinstance(cli.fechadenegado, datetime) and cli.tipo != 1 and getattr(cli, 'socio', '') != 'T':
            filtro_compras['mfechamov__gt'] = cli.fechadenegado

        mov_compras = Movims.objects.filter(**filtro_compras).only('mtipo', 'mtotal', 'mserie')

        saldo_c = Decimal('0.00')
        for m in mov_compras:
            # Compras excluye 'P'
            if getattr(m, 'mserie', None) == 'P':
                continue
            total = Decimal(m.mtotal or 0)
            if m.mtipo in (41, 45):
                saldo_c += total
            elif m.mtipo in (40, 42, 26):
                saldo_c -= total

        saldo_total = saldo_v + saldo_c
        if saldo_total != 0:
            saldos[cli.codigo] = {
                'saldo': saldo_total,
                'nombre': cli.empresa
            }

    return saldos


# Mapas de tipos
TIPOS_VENTAS_DEBE  = (20, 24, 29)
TIPOS_VENTAS_HABER = (21, 25, 23)
TIPOS_COMPRAS_DEBE  = (41, 45)
TIPOS_COMPRAS_HABER = (40, 42, 26)

TIPOS_VENTAS  = TIPOS_VENTAS_DEBE + TIPOS_VENTAS_HABER
TIPOS_COMPRAS = TIPOS_COMPRAS_DEBE + TIPOS_COMPRAS_HABER

def generar_excel_estados_cuenta_mixto(datos, fecha_desde, fecha_hasta, moneda,
                                       consolidar_dolares=False,
                                       consolidar_moneda_nac=False,
                                       omitir_saldos_cero=False,
                                       cliente=None):
    """
    Genera Excel de Estado de Cuenta Mixto (Ventas + Compras).
    - datos: dict { cliente_id: {'datos_cliente': [{'codigo','nombre'}], 'movimientos': [ ... ] } }
    - Usa calcular_saldos_anteriores_mixto para saldo inicial.
    - Reglas:
        * Ventas  -> Debe: (20,24,29), Haber: (21,25,23)
        * Compras -> Debe: (41,45),    Haber: (40,42,26)
    """
    try:
        # --- Nombre de moneda en título ---
        if consolidar_dolares:
            nombre_moneda = "DÓLARES USA"
        elif consolidar_moneda_nac:
            nombre_moneda = "MONEDA NACIONAL"
        else:
            nombre_moneda = moneda.nombre.upper() if moneda else "TODAS LAS MONEDAS"

        # --- Saldo anterior (mixto) ---
        saldos_anteriores = calcular_saldos_anteriores_mixto(fecha_desde, moneda, cliente_id=cliente)

        # --- Unificar clientes (con y sin movimientos) ---
        clientes_dict = {}

        # 1) Clientes con movimientos recibidos en `datos`
        for cliente_id, info in datos.items():
            cliente_id_int = int(cliente_id)
            cli = info['datos_cliente'][0]
            saldo_anterior = saldos_anteriores.get(cliente_id_int, {}).get('saldo', Decimal('0.00'))
            clientes_dict[cliente_id_int] = {
                'codigo': int(cli.get('codigo')),
                'nombre': cli.get('nombre'),
                'saldo_anterior': saldo_anterior,
                'movimientos': info['movimientos'],
            }

        # 2) Clientes SOLO con saldo anterior ≠ 0
        for cliente_id, info in saldos_anteriores.items():
            cliente_id_int = int(cliente_id)
            if cliente_id_int not in clientes_dict and info['saldo'] != 0:
                clientes_dict[cliente_id_int] = {
                    'codigo': cliente_id_int,
                    'nombre': info['nombre'],
                    'saldo_anterior': info['saldo'],
                    'movimientos': [],
                }

        # --- Omitir saldos en cero (evaluando saldo final) ---
        if omitir_saldos_cero:
            filtrados = {}
            for cliente_id, info in clientes_dict.items():
                saldo_final = Decimal(info['saldo_anterior'] or 0)
                for m in info['movimientos']:
                    tipo = m.get('numero_tipo')
                    total = Decimal(m.get('total') or 0)

                    if tipo in TIPOS_VENTAS_DEBE or tipo in TIPOS_COMPRAS_DEBE:
                        saldo_final += total
                    elif tipo in TIPOS_VENTAS_HABER or tipo in TIPOS_COMPRAS_HABER:
                        saldo_final -= total

                if saldo_final != 0:
                    filtrados[cliente_id] = info
            clientes_dict = filtrados

        # --- Ordenar clientes (por codigo) ---
        clientes_ordenados = sorted(
            clientes_dict.values(),
            key=lambda x: (int((x['codigo'])), str(x['codigo']))
        )

        # --- Crear Excel ---
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("EstadoCuentaMixto")

        # Formatos
        title_format  = workbook.add_format({'bold': True, 'font_size': 12})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#d9d9d9', 'border': 1, 'align': 'center'})
        money_format  = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        date_format   = workbook.add_format({'num_format': 'dd/mm/yyyy', 'border': 1})
        text_format   = workbook.add_format({'border': 1})
        bold_format   = workbook.add_format({'bold': True, 'border': 1})
        total_format  = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#FFF2CC'})

        # Título
        row = 0
        if cliente and len(clientes_ordenados) == 1:
            # Tomamos el nombre del único cliente presente
            cli_name = clientes_ordenados[0]['nombre']
            titulo = f"Estado de cuenta de {cli_name} del {fecha_desde:%d/%m/%Y} al {fecha_hasta:%d/%m/%Y} en {nombre_moneda}"
        else:
            titulo = f"Estado de cuenta MIXTO al {fecha_hasta:%d/%m/%Y} en {nombre_moneda}"

        worksheet.merge_range(row, 0, row, 12, titulo, title_format)
        row += 2

        # Encabezados
        headers = ['Fecha', 'Tipo', 'Documento', 'Vto.', 'Detalle',
                   'Debe', 'Haber', 'Saldo', 'Posición', 'Cuenta',
                   'Cobro/Pago', 'Fecha Cobro/Pago', 'Documento Cobro/Pago']

        worksheet.write_row(row, 0, headers, header_format)
        row += 1

        total_general = Decimal('0.00')

        # --- Iterar clientes ---
        for cli in clientes_ordenados:
            # Encabezado cliente
            worksheet.write(row, 2, "1")
            worksheet.write(row, 4, cli['codigo'], text_format)
            worksheet.write(row, 5, cli['nombre'], text_format)
            row += 1

            # Saldo anterior
            saldo_acumulado = Decimal(cli['saldo_anterior'] or 0)
            worksheet.write(row, 6, "Saldo anterior", bold_format)
            worksheet.write(row, 7, float(saldo_acumulado), bold_format)
            row += 1

            # Detalle de movimientos
            if cli['movimientos']:
                for m in cli['movimientos']:
                    tipo  = m.get('numero_tipo')
                    total = Decimal(m.get('total') or 0)

                    debe = haber = Decimal('0.00')
                    if tipo in TIPOS_VENTAS_DEBE or tipo in TIPOS_COMPRAS_DEBE:
                        debe = total
                    elif tipo in TIPOS_VENTAS_HABER or tipo in TIPOS_COMPRAS_HABER:
                        haber = total

                    saldo_acumulado += (debe - haber)

                    worksheet.write(row, 0, m.get('fecha'),
                                    date_format if isinstance(m.get('fecha'), datetime) else text_format)
                    worksheet.write(row, 1, m.get('tipo'), text_format)
                    worksheet.write(row, 2, m.get('documento'), text_format)
                    worksheet.write(row, 3, m.get('vencimiento'),
                                    date_format if isinstance(m.get('vencimiento'), datetime) else text_format)
                    worksheet.write(row, 4, m.get('detalle') or "Sin movimientos en el período", text_format)
                    worksheet.write(row, 5, float(debe),  money_format)
                    worksheet.write(row, 6, float(haber), money_format)
                    worksheet.write(row, 7, float(saldo_acumulado), money_format)
                    worksheet.write(row, 8, m.get('posicion'), text_format)
                    worksheet.write(row, 9, m.get('cuenta'),   text_format)

                    worksheet.write(row, 10, m.get('pago'), text_format)
                    worksheet.write(row, 11, m.get('fecha_pago'), text_format)
                    worksheet.write(row, 12, m.get('numero_pago'), text_format)

                    row += 1
            else:
                worksheet.write(row, 4, "Sin movimientos en el período", text_format)
                row += 1

            # Saldo actual del cliente
            worksheet.write(row, 6, "Actual", bold_format)
            worksheet.write(row, 7, float(saldo_acumulado), bold_format)
            row += 2

            total_general += saldo_acumulado

        # Total general
        worksheet.write(row, 6, "TOTAL GENERAL", total_format)
        worksheet.write(row, 7, float(total_general), total_format)

        workbook.close()
        output.seek(0)

        nombre_archivo = f"estado_cuenta_mixto_{fecha_desde:%Y-%m-%d}_{fecha_hasta:%Y-%m-%d}.xlsx"
        return HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
        )

    except Exception as e:
        raise RuntimeError(f"Error al generar Excel mixto: {e}")



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



def obtener_estado_individual_old(form, fecha_desde, fecha_hasta, moneda):
    """
    Estado de cuenta mixto (ventas + compras) para un cliente específico.
    - Estructura igual a tus funciones actuales (ventas/compras).
    - Excluye mserie == 'P' SOLO en movimientos de COMPRAS.
    """
    cliente = form.cleaned_data['cliente_codigo']
    cliente_nombre = form.cleaned_data['cliente']
    todas_monedas = form.cleaned_data.get('todas_las_monedas', False)

    if not cliente:
        return {}

    cliente_ob = Clientes.objects.only('fechadenegado', 'tipo', 'socio').filter(codigo=cliente).first()
    if not cliente_ob:
        return {}

    filtro_base = {
        'mfechamov__lte': fecha_hasta,
        'mfechamov__gte': fecha_desde,
        'mcliente': cliente,
        'mactivo': 'S',
        'mtipo__in': TIPOS_MIXTAS
    }

    # Ventana por fecha de negado (igual criterio que ventas; si querés incluir socio!='T', lo agregamos)
    if cliente_ob.tipo != 1 and isinstance(cliente_ob.fechadenegado, datetime):
        filtro_base['mfechamov__gt'] = cliente_ob.fechadenegado

    movimientos = Movims.objects.filter(**filtro_base).only(
        'mcliente', 'mfechamov', 'mnombre', 'mtotal', 'msaldo', 'mnombremov',
        'mtipo', 'mserie', 'mboleta', 'mprefijo', 'mautogen', 'mdetalle', 'mmoneda'
    ).order_by('mfechamov')

    if not todas_monedas and moneda:
        movimientos = movimientos.filter(mmoneda=moneda.codigo)

    autogen_list = movimientos.values_list('mautogen', flat=True).distinct()
    asientos = Asientos.objects.filter(
        autogenerado__in=autogen_list,
        imputacion=2
    ).only('autogenerado', 'vto', 'posicion', 'cuenta')
    asientos_dict = {a.autogenerado: a for a in asientos}

    datos = {
        cliente: {
            'datos_cliente': [{
                'nombre': cliente_nombre,
                'codigo': cliente,
            }],
            'movimientos': []
        }
    }

    for m in movimientos:
        # Excluir 'P' SOLO para movimientos de compras
        if m.mtipo in TIPOS_COMPRAS and getattr(m, 'mserie', None) == 'P':
            continue

        asiento = asientos_dict.get(m.mautogen)
        datos[cliente]['movimientos'].append({
            'fecha': m.mfechamov,
            'tipo': m.mnombremov,
            'numero_tipo': m.mtipo,
            'documento': f"{m.mserie or ''}{m.mprefijo or ''}{m.mboleta or ''}",
            'vencimiento': asiento.vto if asiento else None,
            'detalle': m.mdetalle,
            'total': m.mtotal,
            'saldo': m.msaldo,
            'posicion': asiento.posicion if asiento else None,
            'cuenta': asiento.cuenta if asiento else None,
        })

    return datos

def obtener_estado_general_old(form, fecha_desde, fecha_hasta, moneda):
    """
    Estado de cuenta mixto (ventas + compras) para TODOS los clientes (según filtro_tipo),
    con misma estructura que tus funciones actuales.
    - Excluye mserie == 'P' SOLO en tipos de compras.
    """
    filtro_tipo = form.cleaned_data.get('filtro_tipo')  # 'clientes', 'agentes', 'transportistas' (según tu uso en ventas)
    omitir_saldos_cero = form.cleaned_data.get('omitir_saldos_cero', False)  # por si luego lo usás
    todas_monedas = form.cleaned_data.get('todas_las_monedas', False)

    datos = {}
    clientes = Clientes.objects.only('codigo', 'empresa', 'fechadenegado', 'tipo', 'socio').order_by('empresa')

    for cli in clientes:
        # Respeta los mismos filtros que usás en ventas (ajustá si querés otros)
        if filtro_tipo == 'clientes' and cli.tipo != 1:
            continue
        elif filtro_tipo == 'agentes' and cli.tipo != 6:
            continue
        elif filtro_tipo == 'transportistas' and cli.tipo != 5:
            continue

        cliente_id = cli.codigo

        filtro_base = {
            'mfechamov__lte': fecha_hasta,
            'mfechamov__gte': fecha_desde,
            'mcliente': cliente_id,
            'mactivo': 'S',
            'mtipo__in': TIPOS_MIXTAS
        }

        if not todas_monedas and moneda:
            filtro_base['mmoneda'] = moneda.codigo

        # Ventana por fecha de negado (igual criterio que ventas; si querés incluir socio!='T', lo agregamos)
        if isinstance(cli.fechadenegado, datetime) and cli.tipo != 1:
            filtro_base['mfechamov__gt'] = cli.fechadenegado

        movimientos = Movims.objects.filter(**filtro_base).only(
            'mcliente', 'mfechamov', 'mnombre', 'mtotal', 'msaldo', 'mnombremov',
            'mtipo', 'mserie', 'mboleta', 'mprefijo', 'mautogen', 'mdetalle', 'mmoneda'
        ).order_by('mfechamov')

        if not movimientos.exists():
            continue

        autogen_list = movimientos.values_list('mautogen', flat=True).distinct()
        asientos = Asientos.objects.filter(
            autogenerado__in=autogen_list,
            imputacion=2
        ).only('autogenerado', 'vto', 'posicion', 'cuenta')
        asientos_dict = {a.autogenerado: a for a in asientos}

        datos[cliente_id] = {
            'datos_cliente': [{
                'nombre': cli.empresa,
                'codigo': cliente_id,
            }],
            'movimientos': []
        }

        for m in movimientos:
            # Excluir 'P' SOLO para movimientos de compras
            if m.mtipo in TIPOS_COMPRAS and getattr(m, 'mserie', None) == 'P':
                continue

            asiento = asientos_dict.get(m.mautogen)
            datos[cliente_id]['movimientos'].append({
                'fecha': m.mfechamov,
                'tipo': m.mnombremov,
                'numero_tipo': m.mtipo,
                'documento': f"{m.mserie or ''}{m.mprefijo or ''}{m.mboleta or ''}",
                'vencimiento': asiento.vto if asiento else None,
                'detalle': m.mdetalle,
                'total': m.mtotal,
                'saldo': m.msaldo,
                'posicion': asiento.posicion if asiento else None,
                'cuenta': asiento.cuenta if asiento else None,
            })

    return datos