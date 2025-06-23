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


def estados_cuenta_sinop(request):
    if request.method == 'POST':
        form = EstadoCuentaForm(request.POST)
        if form.is_valid():
            tipo_consulta = form.cleaned_data['tipo_consulta']
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            moneda = form.cleaned_data['moneda']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            consolidar_moneda_nac = form.cleaned_data['consolidar_moneda_nac']

            movimientos = Movims.objects.filter(
                mfechamov__range=(fecha_desde, fecha_hasta),
                mtipo__in=(20, 21, 24, 23, 25, 29)
            ).only(
                'mcliente', 'mfechamov', 'mnombre', 'mtotal', 'msaldo', 'mnombremov', 'mtipo',
                'mserie', 'mboleta', 'mprefijo'
            ).order_by('mcliente', 'mfechamov')

            if tipo_consulta == 'individual':
                cliente = form.cleaned_data['cliente']
                if cliente:
                    movimientos = movimientos.filter(nrocliente=cliente.codigo)

                if form.cleaned_data['todas_las_monedas']:
                    moneda_destino = None
                elif consolidar_dolares:
                    moneda_destino = 2
                elif consolidar_moneda_nac:
                    moneda_destino = 1
                else:
                    moneda_destino = moneda.codigo if moneda else None


            else:  # GENERAL
                filtro_tipo = form.cleaned_data['filtro_tipo']
                omitir_saldos_cero = form.cleaned_data['omitir_saldos_cero']

                # Filtro por tipo
                if filtro_tipo == 'clientes':
                    movimientos = movimientos.filter(tipo='cliente')
                elif filtro_tipo == 'agentes':
                    movimientos = movimientos.filter(tipo='agente')
                elif filtro_tipo == 'transportistas':
                    movimientos = movimientos.filter(tipo='transportista')
                if moneda:
                    movimientos = movimientos.filter(mmoneda=moneda.codigo)

                datos = {}
                for m in movimientos:
                    asiento = Asientos.objects.filter(autogenerado=m.mautogen, imputacion=2).only('vto', 'posicion',
                                                                                                  'cuenta').first()
                    lista_movimientos = []
                    datos_cliente = []

                    cli = {
                        'nombre': m.mnombre,
                        'codigo': m.mcliente,
                    }

                    mov = {
                        'fecha': m.mfechamov,
                        'tipo': m.mnombremov,
                        'numero_tipo': m.mtipo,
                        'documento': str(m.mserie or '') + str(m.mprefijo or '') + str(m.mboleta or ''),
                        'vencimiento': asiento.vto if asiento else None,
                        'detalle': m.mdetalle,
                        'total': m.mtotal,
                        'saldo': m.msaldo,
                        'posicion': asiento.posicion if asiento else None,
                        'cuenta': asiento.cuenta if asiento else None,
                    }
                    lista_movimientos.append(mov)
                    datos_cliente.append(cli)

                    datos[m.mautogen] = {
                        'datos_cliente': datos_cliente,
                        'movimientos': lista_movimientos
                    }

                if omitir_saldos_cero:
                    datos_filtrados = {}
                    for autogen, info in datos.items():
                        movimientos = info.get('movimientos', [])
                        if any(Decimal(m.get('saldo') or 0) > 0 for m in movimientos):
                            datos_filtrados[autogen] = info
                    datos = datos_filtrados

                moneda_destino = None
                if consolidar_dolares:
                    moneda_destino = 2
                elif consolidar_moneda_nac:
                    moneda_destino = 1

            return generar_excel_estados_cuenta(
                datos,
                fecha_desde,
                fecha_hasta,
                moneda if moneda else None,
                tipo_consulta,
                consolidar_dolares, consolidar_moneda_nac
            )
    else:
        form = EstadoCuentaForm()

    return render(request, 'ventas_ca/estados_cuenta.html', {'form': form})

def estados_cuenta_old(request):
    if request.method == 'POST':
        form = EstadoCuentaForm(request.POST)
        if form.is_valid():
            tipo_consulta = form.cleaned_data['tipo_consulta']
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            moneda = form.cleaned_data['moneda']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            consolidar_moneda_nac = form.cleaned_data['consolidar_moneda_nac']

            # Tipos relevantes
            tipos_mov = (20, 21, 24, 23, 25, 29)

            movimientos = Movims.objects.filter(
                mfechamov__range=(fecha_desde, fecha_hasta),
                mtipo__in=tipos_mov
            ).only(
                'mcliente', 'mfechamov', 'mnombre', 'mtotal', 'msaldo', 'mnombremov',
                'mtipo', 'mserie', 'mboleta', 'mprefijo', 'mautogen', 'mdetalle', 'mmoneda'
            ).order_by('mcliente', 'mfechamov')

            if tipo_consulta == 'individual':
                cliente = form.cleaned_data['cliente']
                if cliente:
                    movimientos = movimientos.filter(nrocliente=cliente.codigo)

                if form.cleaned_data['todas_las_monedas']:
                    moneda_destino = None
                elif consolidar_dolares:
                    moneda_destino = 2
                elif consolidar_moneda_nac:
                    moneda_destino = 1
                else:
                    moneda_destino = moneda.codigo if moneda else None


            else:  # GENERAL

                filtro_tipo = form.cleaned_data['filtro_tipo']
                omitir_saldos_cero = form.cleaned_data['omitir_saldos_cero']
                clientes = Clientes.objects.only('codigo', 'empresa', 'fechadenegado', 'tipo').order_by('empresa')
                datos = {}
                tipos_mov = (20, 21, 24, 23, 25, 29)

                for cli in clientes:

                    if filtro_tipo == 'clientes' and cli.tipo != 1:
                        continue
                    elif filtro_tipo == 'agentes' and cli.tipo != 6:
                        continue
                    elif filtro_tipo == 'transportistas' and cli.tipo != 5:
                        continue

                    cliente_id = cli.codigo

                    if moneda:
                        filtro_base = {
                            'mmoneda': moneda.codigo,
                            'mfechamov__lte': fecha_hasta,
                            'mcliente': cliente_id,
                            'mactivo': 'S',
                            'mtipo__in': tipos_mov
                        }

                    else:

                        filtro_base = {
                            'mfechamov__lte': fecha_hasta,
                            'mcliente': cliente_id,
                            'mactivo': 'S',
                            'mtipo__in': tipos_mov
                        }

                    if isinstance(cli.fechadenegado, datetime.datetime) and cli.tipo != 1:
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

                if consolidar_dolares:
                    moneda_destino = 2
                elif consolidar_moneda_nac:
                    moneda_destino = 1
                else:
                    moneda_destino = None

            # Obtener todos los asientos relacionados en una sola query
            autogen_list = movimientos.values_list('mautogen', flat=True).distinct()
            asientos = Asientos.objects.filter(
                autogenerado__in=autogen_list,
                imputacion=2
            ).only('autogenerado', 'vto', 'posicion', 'cuenta')

            asientos_dict = {a.autogenerado: a for a in asientos}

            # Agrupar movimientos por cliente
            datos = {}
            for m in movimientos:
                cliente_id = m.mcliente
                if cliente_id not in datos:
                    datos[cliente_id] = {
                        'datos_cliente': [{
                            'nombre': m.mnombre,
                            'codigo': cliente_id,
                        }],
                        'movimientos': []
                    }

                asiento = asientos_dict.get(m.mautogen)

                mov = {
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
                }

                datos[cliente_id]['movimientos'].append(mov)

            # Omitir saldos cero si corresponde
            if tipo_consulta == 'general' and omitir_saldos_cero:
                datos = {
                    cli_id: info
                    for cli_id, info in datos.items()
                    if any(Decimal(m.get('saldo') or 0) > 0 for m in info['movimientos'])
                }

            # Generar Excel final
            return generar_excel_estados_cuenta(
                datos,
                fecha_desde,
                fecha_hasta,
                moneda if moneda else None,
                consolidar_dolares,
                consolidar_moneda_nac
            )
    else:
        form = EstadoCuentaForm()

    return render(request, 'ventas_ca/estados_cuenta.html', {'form': form})




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

            if tipo_consulta == 'individual':
                datos = obtener_estado_individual(form, fecha_hasta, moneda)
            else:
                datos = obtener_estado_general(form, fecha_hasta, moneda)

            return generar_excel_estados_cuenta(
                datos,
                fecha_desde,
                fecha_hasta,
                moneda,
                consolidar_dolares,
                consolidar_moneda_nac,
                omitir_saldos_cero
            )
    else:
        form = EstadoCuentaForm()

    return render(request, 'compras_ca/estados_cuenta.html', {'form': form})

def obtener_estado_individual(form, fecha_hasta, moneda):
    cliente = form.cleaned_data['cliente_codigo']
    cliente_nombre = form.cleaned_data['cliente']
    todas_monedas = form.cleaned_data['todas_las_monedas']

    if not cliente:
        return {}

    tipos_mov = (20, 21, 24, 23, 25, 29)

    movimientos = Movims.objects.filter(
        mcliente=cliente,
        mfechamov__lte=fecha_hasta,
        mactivo='S',
        mtipo__in=tipos_mov
    ).only(
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

def obtener_estado_general(form, fecha_hasta, moneda):
    filtro_tipo = form.cleaned_data['filtro_tipo']
    omitir_saldos_cero = form.cleaned_data['omitir_saldos_cero']
    tipos_mov = (20, 21, 24, 23, 25, 29)

    clientes = Clientes.objects.only('codigo', 'empresa', 'fechadenegado', 'tipo').order_by('empresa')
    datos = {}

    for cli in clientes:
        if filtro_tipo == 'clientes' and cli.tipo != 1:
            continue
        elif filtro_tipo == 'agentes' and cli.tipo != 6:
            continue
        elif filtro_tipo == 'transportistas' and cli.tipo != 5:
            continue

        cliente_id = cli.codigo

        filtro_base = {
            'mfechamov__lte': fecha_hasta,
            'mcliente': cliente_id,
            'mactivo': 'S',
            'mtipo__in': tipos_mov
        }

        if moneda:
            filtro_base['mmoneda'] = moneda.codigo

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


def generar_excel_estados_cuenta(datos, fecha_desde, fecha_hasta, moneda,
                                  consolidar_dolares=False,
                                  consolidar_moneda_nac=False,
                                  omitir_saldos_cero=False):
    try:
        if consolidar_dolares:
            nombre_moneda = "DOLARES USA"
        elif consolidar_moneda_nac:
            nombre_moneda = "MONEDA NACIONAL"
        else:
            nombre_moneda = moneda.nombre.upper() if moneda else "TODAS LAS MONEDAS"

        # Aplicar filtro de clientes con saldo final distinto de 0
        if omitir_saldos_cero:
            datos_filtrados = {}
            for cliente_id, info in datos.items():
                saldo_final = Decimal('0.00')
                for m in info['movimientos']:
                    tipo = m.get('numero_tipo')
                    total = Decimal(m.get('total') or 0)
                    if tipo in (20, 23, 24, 29):  # Débito
                        saldo_final += total
                    elif tipo in (21, 25):       # Crédito
                        saldo_final -= total
                if saldo_final != 0:
                    datos_filtrados[cliente_id] = info
            datos = datos_filtrados

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

        row = 0
        titulo = f"Cuentas a cobrar desde 0 a Z al {fecha_hasta:%d/%m/%Y} en {nombre_moneda}"
        worksheet.merge_range(row, 0, row, 9, titulo, title_format)
        row += 2

        headers = ['Fecha', 'Tipo', 'Documento', 'Vto.', 'Detalle', 'Debe', 'Haber', 'Saldo', 'Posición', 'Cta. Ventas']
        worksheet.write_row(row, 0, headers, header_format)
        row += 1

        for cliente_id, info in datos.items():
            cli = info['datos_cliente'][0]

            worksheet.write(row, 2, "1")
            worksheet.write(row, 4, cli.get('codigo'), text_format)
            worksheet.write(row, 5, cli.get('nombre'), text_format)
            row += 1

            saldo_acumulado = Decimal('0.00')

            for m in info['movimientos']:
                tipo = m.get('numero_tipo')
                total = Decimal(m.get('total') or 0)
                debe = haber = Decimal('0.00')

                if tipo in [20, 23, 24, 29]:
                    debe = total
                elif tipo in [21, 25]:
                    haber = total

                saldo_acumulado += debe - haber

                worksheet.write(row, 0, m.get('fecha'), date_format if isinstance(m.get('fecha'), datetime) else text_format)
                worksheet.write(row, 1, m.get('tipo'), text_format)
                worksheet.write(row, 2, m.get('documento'), text_format)
                worksheet.write(row, 3, m.get('vencimiento'), date_format if isinstance(m.get('vencimiento'), datetime) else text_format)
                worksheet.write(row, 4, m.get('detalle'), text_format)
                worksheet.write(row, 5, float(debe), money_format)
                worksheet.write(row, 6, float(haber), money_format)
                worksheet.write(row, 7, float(saldo_acumulado), money_format)
                worksheet.write(row, 8, m.get('posicion'), text_format)
                worksheet.write(row, 9, m.get('cuenta'), text_format)

                row += 1

            worksheet.write(row, 6, "Actual", bold_format)
            worksheet.write(row, 7, float(saldo_acumulado), bold_format)
            row += 2

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