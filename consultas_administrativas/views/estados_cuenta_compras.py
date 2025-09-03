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

def estados_cuenta_compras(request):
    if request.method == 'POST':
        form = EstadoCuentaForm(request.POST)
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
                datos = obtener_estado_general(form, fecha_desde,fecha_hasta, moneda)

            return generar_excel_estados_cuenta(
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
        form = EstadoCuentaForm()

    return render(request, 'compras_ca/estados_cuenta.html', {'form': form})

def obtener_estado_individual(form,fecha_desde, fecha_hasta, moneda):
    cliente = form.cleaned_data['cliente_codigo']
    cliente_nombre = form.cleaned_data['cliente']
    todas_monedas = form.cleaned_data['todas_las_monedas']
    tipos_mov = (40,41,45,42,26)

    if not cliente:
        return {}
    cliente_ob=Clientes.objects.only('fechadenegado','tipo','socio').filter(codigo=cliente).first()
    if not cliente_ob:
        return {}

    filtro_base = {
            'mfechamov__lte': fecha_hasta,
            'mfechamov__gte': fecha_desde,
            'mcliente': cliente,
            'mactivo': 'S',
            'mtipo__in': tipos_mov
        }

    if cliente_ob.tipo !=1 and cliente_ob.socio!='T':
        if isinstance(cliente_ob.fechadenegado, datetime):
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
        if m.mserie !='P':
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

def obtener_estado_general(form,fecha_desde, fecha_hasta, moneda):
    filtro_tipo = form.cleaned_data['filtro_tipo']
    omitir_saldos_cero = form.cleaned_data['omitir_saldos_cero']
    todas_monedas = form.cleaned_data['todas_las_monedas']

    tipos_mov = (40, 41, 45,42,26)

    clientes = Clientes.objects.only('codigo', 'empresa', 'fechadenegado', 'tipo').order_by('empresa')
    datos = {}

    for cli in clientes:
        # if filtro_tipo == 'clientes' and cli.tipo != 1:
        #     continue
        # elif filtro_tipo == 'agentes' and cli.tipo != 6:
        #     continue
        # elif filtro_tipo == 'transportistas' and cli.tipo != 5:
        #     continue

        cliente_id = cli.codigo

        filtro_base = {
            'mfechamov__lte': fecha_hasta,
            'mfechamov__gte': fecha_desde,
            'mcliente': cliente_id,
            'mactivo': 'S',
            'mtipo__in': tipos_mov
        }

        if not todas_monedas and moneda:
            filtro_base['mmoneda'] = moneda.codigo

        if isinstance(cli.fechadenegado, datetime) and cli.tipo != 1 and cli.socio!='T':
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
            if m.mserie != 'P':
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

def calcular_saldos_anteriores(fecha_desde, moneda=None, cliente_id=None):
    """
    Devuelve un diccionario con el saldo acumulado anterior a fecha_desde.
    - Si cliente_id es None → devuelve todos los clientes.
    - Si cliente_id está definido → devuelve solo ese cliente.
    """
    tipos_mov = (40, 41, 45,42,26)

    clientes_qs = Clientes.objects.only('codigo', 'empresa', 'fechadenegado', 'tipo','socio').order_by('empresa')
    if cliente_id:
        clientes_qs = clientes_qs.filter(codigo=cliente_id)

    saldos = {}
    for cli in clientes_qs:
        filtro_base = {
            'mfechamov__lt': fecha_desde,
            'mcliente': cli.codigo,
            'mactivo': 'S',
            'mtipo__in': tipos_mov
        }

        if moneda:
            filtro_base['mmoneda'] = moneda.codigo

        # Verificación de fecha de negado
        if isinstance(cli.fechadenegado, datetime) and cli.tipo != 1 and cli.socio!='T':
            filtro_base['mfechamov__gt'] = cli.fechadenegado

        movimientos = Movims.objects.filter(**filtro_base).only('mtipo', 'mtotal','mserie')

        if not movimientos.exists():
            continue

        saldo = Decimal('0.00')
        for m in movimientos:
            if m.mserie !='P':
                total = Decimal(m.mtotal or 0)
                if m.mtipo in (41, 45):
                    saldo += total
                elif m.mtipo in(40,42,26):
                    saldo -= total

        if saldo != 0:
            saldos[cli.codigo] = {
                'saldo': saldo,
                'nombre': cli.empresa
            }

    return saldos

def generar_excel_estados_cuenta(datos, fecha_desde, fecha_hasta, moneda,
                                  consolidar_dolares=False,
                                  consolidar_moneda_nac=False,
                                  omitir_saldos_cero=False,
                                  cliente=None):
    try:
        if consolidar_dolares:
            nombre_moneda = "DOLARES USA"
        elif consolidar_moneda_nac:
            nombre_moneda = "MONEDA NACIONAL"
        else:
            nombre_moneda = moneda.nombre.upper() if moneda else "TODAS LAS MONEDAS"

        # --- Calcular saldos anteriores por cliente ---
        saldos_anteriores = calcular_saldos_anteriores(fecha_desde, moneda, cliente_id=cliente)

        # --- Unificar todos los clientes ---
        clientes_dict = {}

        # clientes con movimientos
        for cliente_id, info in datos.items():
            cliente_id_int = int(cliente_id)  # 🔑 normalizamos la clave
            cli = info['datos_cliente'][0]
            saldo_anterior = saldos_anteriores.get(cliente_id_int, {}).get('saldo', Decimal('0.00'))
            clientes_dict[cliente_id_int] = {
                'codigo': int(cli.get('codigo')),   # por si viene string
                'nombre': cli.get('nombre'),
                'saldo_anterior': saldo_anterior,
                'movimientos': info['movimientos']
            }

        # clientes solo con saldo anterior distinto de 0
        for cliente_id, info in saldos_anteriores.items():
            cliente_id_int = int(cliente_id)  # 🔑 normalizamos
            if cliente_id_int not in clientes_dict and info['saldo'] != 0:
                clientes_dict[cliente_id_int] = {
                    'codigo': cliente_id_int,
                    'nombre': info['nombre'],
                    'saldo_anterior': info['saldo'],
                    'movimientos': []
                }

        # --- Filtrado opcional de saldos en cero ---
        if omitir_saldos_cero:
            clientes_filtrados = {}
            for cliente_id, info in clientes_dict.items():
                saldo_final = info['saldo_anterior']
                for m in info['movimientos']:
                    tipo = m.get('numero_tipo')
                    total = Decimal(m.get('total') or 0)
                    if tipo in (41, 45):
                        saldo_final += total
                    elif tipo in (40,42,26):
                        saldo_final -= total
                if saldo_final != 0:
                    clientes_filtrados[cliente_id] = info
            clientes_dict = clientes_filtrados

        # --- Ordenar clientes alfabéticamente por nombre ---
        clientes_ordenados = sorted(clientes_dict.values(), key=lambda x: x['nombre'].lower())

        # --- Crear Excel ---
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("EstadoCuenta")

        # Formatos
        title_format = workbook.add_format({'bold': True, 'font_size': 12})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#d9d9d9', 'border': 1, 'align': 'center'})
        money_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'border': 1})
        text_format = workbook.add_format({'border': 1})
        bold_format = workbook.add_format({'bold': True, 'border': 1})
        total_format = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#FFF2CC'})  # amarillo

        row = 0
        titulo = f"Cuentas a cobrar desde 0 a Z al {fecha_hasta:%d/%m/%Y} en {nombre_moneda}"
        worksheet.merge_range(row, 0, row, 9, titulo, title_format)
        row += 2

        headers = ['Fecha', 'Tipo', 'Documento', 'Vto.', 'Detalle',
                   'Debe', 'Haber', 'Saldo', 'Posición', 'Cta. Ventas']
        worksheet.write_row(row, 0, headers, header_format)
        row += 1

        total_general = Decimal('0.00')

        # --- Iterar clientes ya ordenados ---
        for cli in clientes_ordenados:
            worksheet.write(row, 2, "1")
            worksheet.write(row, 4, cli['codigo'], text_format)
            worksheet.write(row, 5, cli['nombre'], text_format)
            row += 1

            saldo_acumulado = cli['saldo_anterior']
            worksheet.write(row, 6, "Saldo anterior", bold_format)
            worksheet.write(row, 7, float(saldo_acumulado), bold_format)
            row += 1

            if cli['movimientos']:
                for m in cli['movimientos']:
                    tipo = m.get('numero_tipo')
                    total = Decimal(m.get('total') or 0)
                    debe = haber = Decimal('0.00')

                    if tipo in (41, 45):
                        debe = total
                    elif tipo in (40,42,26):
                        haber = total

                    saldo_acumulado += debe - haber

                    worksheet.write(row, 0, m.get('fecha'),
                                    date_format if isinstance(m.get('fecha'), datetime) else text_format)
                    worksheet.write(row, 1, m.get('tipo'), text_format)
                    worksheet.write(row, 2, m.get('documento'), text_format)
                    worksheet.write(row, 3, m.get('vencimiento'),
                                    date_format if isinstance(m.get('vencimiento'), datetime) else text_format)
                    worksheet.write(row, 4, m.get('detalle') or "Sin movimientos en el período", text_format)
                    worksheet.write(row, 5, float(debe), money_format)
                    worksheet.write(row, 6, float(haber), money_format)
                    worksheet.write(row, 7, float(saldo_acumulado), money_format)
                    worksheet.write(row, 8, m.get('posicion'), text_format)
                    worksheet.write(row, 9, m.get('cuenta'), text_format)

                    row += 1
            else:
                worksheet.write(row, 4, "Sin movimientos en el período", text_format)
                row += 1

            worksheet.write(row, 6, "Actual", bold_format)
            worksheet.write(row, 7, float(saldo_acumulado), bold_format)
            row += 2

            total_general += saldo_acumulado

        # --- Total general ---
        worksheet.write(row, 6, "TOTAL GENERAL", total_format)
        worksheet.write(row, 7, float(total_general), total_format)

        workbook.close()
        output.seek(0)

        nombre_archivo = f"estado_cuenta_{fecha_desde:%Y-%m-%d}_{fecha_hasta:%Y-%m-%d}.xlsx"

        return HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
        )

    except Exception as e:
        raise RuntimeError(f"Error al generar Excel: {e}")


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


