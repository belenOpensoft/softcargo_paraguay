import json
from datetime import datetime
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from administracion_contabilidad.forms import Cobranza
from administracion_contabilidad.models import Boleta, Impuvtas, Asientos, Movims, Cheques, Cuentas, VistaCobranza, \
    Dolar, ListaCobranzas
from administracion_contabilidad.views.facturacion import generar_numero, modificar_numero
from administracion_contabilidad.views.preventa import generar_autogenerado
from mantenimientos.models import Clientes, Monedas


param_busqueda = {
    0: 'autogenerado__icontains',
    1: 'numero__icontains',
    2: 'detalle__icontains',
    4: 'master__icontains',
    5: 'house__icontains',
    6: 'monto__icontains',
    7: 'iva__icontains',
    8: 'totiva__icontains',
    9: 'total__icontains',
}

columns_table = {
    0: 'autogenerado',
    1: 'numero',
    2: 'detalle',
    3: 'master',
    4: 'house',
    5: 'monto',
    6: 'iva',
    7: 'totiva',
    8: 'total',
}

def cobranza_view(request):
    form = Cobranza(request.POST or None)
    return render(request, 'cobranza.html', {'form': form})


def buscar_cliente(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()  # Obtener y limpiar el término de búsqueda
        clientes = Clientes.objects.filter(empresa__icontains=query)[:10]  # Limitar resultados a 10
        results = [{'id': cliente.id, 'text': cliente.empresa} for cliente in clientes]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def buscar_clientes(request):
    if request.method == "GET":
        cliente_id = request.GET.get("id")
        cliente = Clientes.objects.filter(id=cliente_id).first()

        if cliente:
            data = {
                'codigo': cliente.codigo,
                'empresa': cliente.empresa,
                'ruc': cliente.ruc,
                'direccion': cliente.direccion,
                'localidad': cliente.localidad,
                'telefono': cliente.telefono,
            }
            return JsonResponse(data)

    return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

def source_cobranza_imputacion(request):
    pass


def source_cobranza(request):
    try:
        # Usar un bucle para recoger dinámicamente las columnas que existen
        args = {}
        for i in range(10):  # Cambia el rango según el número de columnas reales
            key = f'columns[{i}][search][value]'
            args[str(i)] = request.GET.get(key, '')  # Usa un valor predeterminado si la clave no existe

        # Filtros y lógica de búsqueda
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        buscar = request.GET.get('buscar', '')
        que_buscar = request.GET.get('que_buscar', '')

        if buscar:
            filtro[que_buscar] = buscar

        end = start + length

        # Consulta a la base de datos
        if filtro:
            registros = ListaCobranzas.objects.filter(**filtro).order_by()
        else:
            registros = ListaCobranzas.objects.all().order_by()

        # Preparación de la respuesta
        resultado = {
            'data': get_data(registros[start:end]),
            'length': length,
            'draw': request.GET.get('draw', '1'),
            'recordsTotal': ListaCobranzas.objects.count(),
            'recordsFiltered': registros.count(),
        }
        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_data(registros_filtrados):
    try:
        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append('' if registro.autogenerado is None else str(registro.autogenerado))
            registro_json.append('' if registro.numero is None else str(registro.numero))
            registro_json.append('' if registro.detalle is None else str(registro.detalle))
            registro_json.append('' if registro.master is None else str(registro.master))
            registro_json.append('' if registro.house is None else str(registro.house))
            registro_json.append('' if registro.monto is None else str(registro.monto))
            registro_json.append('' if registro.iva is None else str(registro.iva))
            registro_json.append('' if registro.totiva is None else str(registro.totiva))
            registro_json.append('' if registro.total is None else str(registro.total))
            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)


def get_argumentos_busqueda(**kwargs):
    try:
        result = {}
        for row in kwargs:
            if len(kwargs[row]) > 0:
                result[param_busqueda[int(row)]] = kwargs[row]
        return result
    except Exception as e:
        raise TypeError(e)



def source_facturas_pendientes_old(request):
    try:
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        cliente = int(request.GET.get('cliente'))

        # Obtener registros filtrados por cliente
        pendientes = VistaCobranza.objects.filter(nrocliente=cliente)
        #pendientes = VistaCobranza.objects.all()

        # Agrupar por `autogenerado` y recalcular `saldo` y `pago`
        agrupados = defaultdict(lambda: {
            'vencimiento': None,
            'emision': None,
            'documento': None,
            'total': 0,
            'saldo': 0,
            'pago': 0,
            'tipo_cambio': 0,
            'embarque': None,
            'detalle': None,
            'posicion': None,
            'moneda': None,
            'paridad': 0,
            'tipo_doc': None,
            'source':None
        })

        for pendiente in pendientes:
            auto = pendiente.autogenerado
            agrupados[auto]['vencimiento'] = pendiente.vencimiento
            agrupados[auto]['emision'] = pendiente.emision
            agrupados[auto]['documento'] = pendiente.documento
            agrupados[auto]['total'] = pendiente.total
            agrupados[auto]['tipo_cambio'] = pendiente.arbitraje
            agrupados[auto]['embarque'] = pendiente.embarque
            agrupados[auto]['detalle'] = pendiente.detalle
            agrupados[auto]['posicion'] = pendiente.posicion
            agrupados[auto]['paridad'] = pendiente.paridad
            agrupados[auto]['tipo_doc'] = pendiente.tipo_doc
            agrupados[auto]['source'] = pendiente.source
            try:
                agrupados[auto]['moneda'] = Monedas.objects.get(codigo=pendiente.moneda).nombre
            except ObjectDoesNotExist:
                agrupados[auto]['moneda'] = "Desconocida"
            # Sumar pago y manejar valores None
            agrupados[auto]['pago'] += pendiente.pago or 0
            agrupados[auto]['saldo'] = max(0, pendiente.total - agrupados[auto]['pago'])

        # Filtrar agrupados para excluir saldos cero
        agrupados_filtrados = {
            key: value for key, value in agrupados.items() if value['saldo'] > 0
        }

        # Convertir agrupados a una lista y paginar
        total_registros = len(agrupados)
        agrupados_paginados = list(agrupados_filtrados.values())[start:start + length]

        # Preparar datos para la respuesta
        data = [{
            'id': idx,
            'vencimiento': item['vencimiento'],
            'emision': item['emision'],
            'documento': item['documento'],
            'total': item['total'],
            'saldo': item['saldo'],
            'imputado': 0,
            'tipo_cambio': item['tipo_cambio'],
            'embarque': item['embarque'],
            'detalle': item['detalle'],
            'posicion': item['posicion'],
            'moneda': item['moneda'],
            'paridad': item['paridad'],
            'tipo_doc': item['tipo_doc'],
            'source':item['source']
        } for idx, item in enumerate(agrupados_paginados, start=1)]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': total_registros,
            'recordsFiltered': total_registros,
            'data': data,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})

def source_facturas_pendientes_oldlast(request):
    try:
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        cliente = int(request.GET.get('cliente'))

        # Obtener registros filtrados por cliente
        pendientes = VistaCobranza.objects.filter(nrocliente=cliente)

        # Agrupar por `autogenerado` y recalcular `saldo` y `pago`
        agrupados = defaultdict(lambda: {
            'vencimiento': None,
            'emision': None,
            'documento': None,
            'total': 0,
            'saldo': 0,
            'pago': 0,
            'tipo_cambio': 0,
            'embarque': None,
            'detalle': None,
            'posicion': None,
            'moneda': None,
            'paridad': 0,
            'tipo_doc': None,
            'source': None
        })

        for pendiente in pendientes:
            auto = pendiente.autogenerado
            agrupados[auto]['vencimiento'] = pendiente.vencimiento
            agrupados[auto]['emision'] = pendiente.emision
            agrupados[auto]['documento'] = pendiente.documento
            agrupados[auto]['total'] = pendiente.total
            agrupados[auto]['tipo_cambio'] = pendiente.arbitraje
            agrupados[auto]['embarque'] = pendiente.embarque
            agrupados[auto]['detalle'] = pendiente.detalle
            agrupados[auto]['posicion'] = pendiente.posicion
            agrupados[auto]['paridad'] = pendiente.paridad
            agrupados[auto]['tipo_doc'] = pendiente.tipo_doc
            agrupados[auto]['source'] = pendiente.source
            try:
                agrupados[auto]['moneda'] = Monedas.objects.get(codigo=pendiente.moneda).nombre
            except ObjectDoesNotExist:
                agrupados[auto]['moneda'] = "Desconocida"

            # Sumar pago y manejar valores None
            pago_actual = pendiente.pago if pendiente.pago is not None else 0
            agrupados[auto]['pago'] += pago_actual

            # Calcular saldo solo si tipo_doc no es 'ANTICIPO'
            if pendiente.tipo_doc != 'ANTICIPO':
                agrupados[auto]['saldo'] = agrupados[auto]['total'] - agrupados[auto]['pago']
            else:
                agrupados[auto]['saldo'] = None  # Excluir el saldo para ANTICIPO

        # Filtrar agrupados para excluir saldos exactamente cero y None
        agrupados_filtrados = {
            key: value for key, value in agrupados.items() if value['saldo'] != 0 and value['saldo'] is not None
        }

        # Convertir agrupados a una lista y paginar
        total_registros = len(agrupados_filtrados)
        agrupados_paginados = list(agrupados_filtrados.values())[start:start + length]

        # Preparar datos para la respuesta
        data = [{
            'id': idx,
            'vencimiento': item['vencimiento'],
            'emision': item['emision'],
            'documento': item['documento'],
            'total': item['total'],
            'saldo': item['saldo'],
            'imputado': 0,
            'tipo_cambio': item['tipo_cambio'],
            'embarque': item['embarque'],
            'detalle': item['detalle'],
            'posicion': item['posicion'],
            'moneda': item['moneda'],
            'paridad': item['paridad'],
            'tipo_doc': item['tipo_doc'],
            'source': item['source']
        } for idx, item in enumerate(agrupados_paginados, start=1)]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': total_registros,
            'recordsFiltered': total_registros,
            'data': data,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})

from collections import defaultdict
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

def source_facturas_pendientes(request):
    try:
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        cliente = int(request.GET.get('cliente'))
        nromoneda = int(request.GET.get('nromoneda'))

        # Filtrar registros por cliente y moneda=2
        pendientes = VistaCobranza.objects.filter(nrocliente=cliente, moneda=nromoneda)

        # Agrupar por `autogenerado` y recalcular `saldo` y `pago`
        agrupados = defaultdict(lambda: {
            'vencimiento': None,
            'emision': None,
            'documento': None,
            'total': 0,
            'saldo': 0,
            'pago': 0,
            'tipo_cambio': 0,
            'embarque': None,
            'detalle': None,
            'posicion': None,
            'moneda': None,
            'paridad': 0,
            'tipo_doc': None,
            'source': None
        })

        for pendiente in pendientes:
            auto = pendiente.autogenerado
            agrupados[auto]['vencimiento'] = pendiente.vencimiento
            agrupados[auto]['emision'] = pendiente.emision
            agrupados[auto]['documento'] = pendiente.documento
            agrupados[auto]['total'] = pendiente.total
            agrupados[auto]['tipo_cambio'] = pendiente.arbitraje
            agrupados[auto]['embarque'] = pendiente.embarque
            agrupados[auto]['detalle'] = pendiente.detalle
            agrupados[auto]['posicion'] = pendiente.posicion
            agrupados[auto]['paridad'] = pendiente.paridad
            agrupados[auto]['tipo_doc'] = pendiente.tipo_doc
            agrupados[auto]['source'] = pendiente.source

            try:
                agrupados[auto]['moneda'] = Monedas.objects.get(codigo=pendiente.moneda).nombre
            except ObjectDoesNotExist:
                agrupados[auto]['moneda'] = "Desconocida"

            # Sumar pago y manejar valores None
            pago_actual = pendiente.pago if pendiente.pago is not None else 0
            agrupados[auto]['pago'] += pago_actual

            # Calcular saldo solo si tipo_doc no es 'ANTICIPO'
            if pendiente.tipo_doc != 'ANTICIPO':
                saldo = agrupados[auto]['total'] - agrupados[auto]['pago']
                agrupados[auto]['saldo'] = saldo
            else:
                agrupados[auto]['saldo'] = None  # Excluir el saldo para ANTICIPO

        # Filtrar agrupados para excluir saldos exactamente cero y None
        agrupados_filtrados = {
            key: value for key, value in agrupados.items()
            if value['saldo'] is not None and float(value['saldo']) != 0
        }

        # Convertir agrupados a una lista y paginar
        total_registros = len(agrupados_filtrados)
        agrupados_paginados = list(agrupados_filtrados.values())[start:start + length]

        # Preparar datos para la respuesta
        data = [{
            'id': idx,
            'vencimiento': item['vencimiento'],
            'emision': item['emision'],
            'documento': item['documento'],
            'total': item['total'],
            'saldo': item['saldo'],
            'imputado': 0,
            'tipo_cambio': item['tipo_cambio'],
            'embarque': item['embarque'],
            'detalle': item['detalle'],
            'posicion': item['posicion'],
            'moneda': item['moneda'],
            'paridad': item['paridad'],
            'tipo_doc': item['tipo_doc'],
            'source': item['source']
        } for idx, item in enumerate(agrupados_paginados, start=1)]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': total_registros,
            'recordsFiltered': total_registros,
            'data': data,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})



@transaction.atomic
def guardar_impuventa_mal(request):
    try:
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            vector = body_data.get('vector', {})
            imputaciones = vector.get('imputaciones', [])
            asientos = vector.get('asiento', [])
            movimiento = vector.get('movimiento', [])
            cobranza = vector.get('cobranza', [])

            arbitraje = float(cobranza[0]['arbitraje'])
            paridad = float(cobranza[0]['paridad'])
            nromoneda = int(cobranza[0]['nromoneda'])

            autogenerado_impuventa = generar_autogenerado(datetime.now().strftime("%Y-%m-%d"))
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if vector and imputaciones:

                for item in imputaciones:

                    try:
                        boleta = Boleta.objects.filter(numero=item['nroboleta']).order_by('-id').first()
                    except Exception as _:
                        boleta = None

                    if boleta:
                        autofac = boleta.autogenerado
                        parteiva=boleta.totiva
                        #diferenciar si son acreedor o proveedor 40 va negativo
                        monto = float(item['imputado']) if boleta.tipo == 20 else -float(item['imputado']) if boleta.tipo == 21  else 0

                        if nromoneda == 2: #dolar
                            monto_convertido =monto*arbitraje
                        elif nromoneda not in [1,2]:
                            aux=monto*paridad
                            monto_convertido=aux*arbitraje
                        else:
                            monto_convertido=0

                        cliente=boleta.nrocliente
                        impuventa = Impuvtas()
                        impuventa.autogen = autogenerado_impuventa
                        impuventa.tipo = 1
                        impuventa.cliente = cliente
                        impuventa.monto = monto_convertido
                        impuventa.autofac = autofac
                        impuventa.parteiva = parteiva
                        impuventa.fechaimpu = fecha
                        impuventa.save()

            try:
                cliente_data = Clientes.objects.get(codigo=cobranza[0]['nrocliente'])
            except Exception as _:
                cliente_data = None

            if cliente_data:
                for asiento in asientos:
                    fechaj = datetime.now().strftime("%Y-%m-%d")
                    fecha_obj = datetime.strptime(fechaj, '%Y-%m-%d')
                    nroasiento = generar_numero()
                    movimiento_num = modificar_numero(nroasiento)
                    detalle_asiento = 'COBRO' + cobranza[0]['serie'] +'-'+ str(cobranza[0]['prefijo']) +'-'+ str(cobranza[0]['numero']) +'-'+ cliente_data.empresa
                    asiento_monto=asiento['total_pago']

                    if nromoneda == 2:  # dolar
                        monto_asiento = float(asiento_monto) * arbitraje
                    elif nromoneda not in [1, 2]:
                        aux = float(asiento_monto) * paridad
                        monto_asiento = aux * arbitraje
                    else:
                        monto_asiento = 0

                    asiento_vector_1 = {
                        'detalle': detalle_asiento,
                        'monto':monto_asiento ,
                        'moneda': cobranza[0]['nromoneda'],
                        'cambio': cobranza[0]['arbitraje'],
                        'asiento': nroasiento,
                        'conciliado': 'N',
                        'clearing': fecha_obj,
                        'fecha': fecha_obj,
                        'imputacion': 1,
                        'modo': asiento['modo'],
                        'tipo': 'Z',
                        'cuenta': asiento['cuenta'],
                        'documento': cobranza[0]['numero'],
                        'vencimiento': fecha_obj,
                        'pasado': 0,
                        'autogenerado': autogenerado_impuventa,
                        'cliente': cliente_data.codigo,
                        'banco': asiento['banco'] if asiento['modo'] != 'CHEQUE' else " - ".join(map(str, Cuentas.objects.filter(xcodigo=asiento['cuenta']).values_list('xcodigo', 'xnombre').first() or ('', ''))),
                        'centro': 'ADM',
                        'mov': int(movimiento_num) + 1,
                        'anio': fecha_obj.year,
                        'mes': fecha_obj.month,
                        'fechacheque': fecha_obj,
                        'paridad': cobranza[0]['paridad'],
                        'posicion': boleta.posicion if boleta.posicion else None

                    }  # haber
                    crear_asiento(asiento_vector_1)
                    if asiento.get('modo') == 'CHEQUE':
                        numero=asiento['nro_mediopago']
                        banco=asiento['banco']
                        fecha_vencimiento=asiento['vencimiento']
                        monto=monto_asiento
                        autogenerado=autogenerado_impuventa
                        detalle=detalle_asiento
                        moneda=cobranza[0]['nromoneda']
                        nrocliente=cobranza[0]['nrocliente']
                        tipo_cheque='CH'
                        cheque = Cheques()
                        cheque.cnumero=numero
                        cheque.cbanco=banco
                        cheque.cfecha=fecha_obj
                        cheque.cvto=fecha_vencimiento
                        cheque.cmonto=monto
                        cheque.cautogenerado=autogenerado
                        cheque.cdetalle=detalle
                        cheque.ccliente=nrocliente
                        cheque.cmoneda=moneda
                        cheque.ctipo=tipo_cheque
                        cheque.save()

                #asiento general
                monto_total=cobranza[0]['total']
                saldo_mov=movimiento[0]['saldo']
                if nromoneda == 2:  # dolar
                    monto_deber = float(monto_total) * arbitraje
                    saldo_convertido = float(saldo_mov) * arbitraje
                elif nromoneda not in [1, 2]:
                    aux = float(monto_total) * paridad
                    aux2 = float(saldo_mov) * paridad
                    monto_deber = aux * arbitraje
                    saldo_convertido = aux2 * arbitraje
                else:
                    saldo_convertido = 0

                asiento_vector_2 = {  # deber
                    'detalle': detalle_asiento,
                    'monto': monto_deber,
                    'moneda': cobranza[0]['nromoneda'],
                    'cambio': cobranza[0]['arbitraje'],
                    'asiento': nroasiento,
                    'conciliado': 'N',
                    'clearing': fecha_obj,
                    'fecha': fecha_obj,
                    'imputacion': 2,
                    'modo': None,
                    'tipo': 'Z',
                    'cuenta': cliente_data.ctavta,
                    'documento': cobranza[0]['numero'],
                    'vencimiento': fecha_obj,
                    'pasado': 0,
                    'autogenerado': autogenerado_impuventa,
                    'cliente': cliente_data.codigo,
                    'banco': 'S/I',
                    'centro': 'S/I',
                    'mov': movimiento_num,
                    'anio': fecha_obj.year,
                    'mes': fecha_obj.month,
                    'fechacheque': fecha_obj,
                    'paridad': cobranza[0]['paridad'],
                    'posicion': boleta.posicion if boleta.posicion else None
                }  # deber general
                crear_asiento(asiento_vector_2)
                #crear el movimiento
                movimiento_vec = {
                    'tipo': 25,
                    'fecha': fecha_obj,
                    'boleta': cobranza[0]['numero'],
                    'monto': 0,
                    'paridad': cobranza[0]['paridad'],
                    'iva': boleta.totiva,
                    'total': monto_total,
                    'saldo': saldo_convertido,
                    'moneda': cobranza[0]['nromoneda'],
                    'detalle': movimiento[0]['boletas'],
                    'cliente': cliente_data.codigo,
                    'nombre': cliente_data.empresa,
                    'nombremov': 'COBRO',
                    'cambio': cobranza[0]['arbitraje'],
                    'autogenerado': autogenerado_impuventa,
                    'serie': cobranza[0]['serie'],
                    'prefijo': cobranza[0]['prefijo'],
                    'posicion': boleta.posicion if boleta else None,
                    'anio': fecha_obj.year,
                    'mes': fecha_obj.month,
                    'monedaoriginal': cobranza[0]['nromoneda'],
                    'montooriginal': monto_total,
                    'arbitraje': cobranza[0]['arbitraje'],

                }
                crear_movimiento(movimiento_vec)

            return JsonResponse({'status': 'exito'})
    except Exception as e:
        return JsonResponse({'status': 'Error: ' + str(e)})

@transaction.atomic
def guardar_impuventa(request):
    try:
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            vector = body_data.get('vector', {})
            imputaciones = vector.get('imputaciones', [])
            asientos = vector.get('asiento', [])
            movimiento = vector.get('movimiento', [])
            cobranza = vector.get('cobranza', [])

            autogenerado_impuventa = generar_autogenerado(datetime.now().strftime("%Y-%m-%d"))
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if vector and imputaciones:
                for item in imputaciones:

                    try:
                        boleta = Boleta.objects.filter(numero=item['nroboleta']).order_by('-id').first()
                    except Exception as _:
                        boleta = None

                    if boleta:
                        autofac = boleta.autogenerado
                        parteiva=boleta.totiva
                        #diferenciar si son acreedor o proveedor 40 va negativo
                        monto = float(item['imputado']) if boleta.tipo == 20 else -float(item['imputado']) if boleta.tipo == 21  else 0
                        cliente=boleta.nrocliente
                        impuventa = Impuvtas()
                        impuventa.autogen = autogenerado_impuventa
                        impuventa.tipo = 1
                        impuventa.cliente = cliente
                        impuventa.monto = monto
                        impuventa.autofac = autofac
                        impuventa.parteiva = parteiva
                        impuventa.fechaimpu = fecha
                        impuventa.save()

            try:
                cliente_data = Clientes.objects.get(codigo=cobranza[0]['nrocliente'])
            except Exception as _:
                cliente_data = None

            if cliente_data:
                for asiento in asientos:
                    fechaj = datetime.now().strftime("%Y-%m-%d")
                    fecha_obj = datetime.strptime(fechaj, '%Y-%m-%d')
                    nroasiento = generar_numero()
                    movimiento_num = modificar_numero(nroasiento)

                    detalle_asiento = 'COBRO' + cobranza[0]['serie'] +'-'+ str(cobranza[0]['prefijo']) +'-'+ str(cobranza[0]['numero']) +'-'+ cliente_data.empresa
                    asiento_vector_1 = {
                        'detalle': detalle_asiento,
                        'monto': asiento['total_pago'],
                        'moneda': cobranza[0]['nromoneda'],
                        'cambio': cobranza[0]['arbitraje'],
                        'asiento': nroasiento,
                        'conciliado': 'N',
                        'clearing': fecha_obj,
                        'fecha': fecha_obj,
                        'imputacion': 1,
                        'modo': asiento['modo'],
                        'tipo': 'Z',
                        'cuenta': asiento['cuenta'],
                        'documento': cobranza[0]['numero'],
                        'vencimiento': fecha_obj,
                        'pasado': 0,
                        'autogenerado': autogenerado_impuventa,
                        'cliente': cliente_data.codigo,
                        'banco': asiento['banco'] if asiento['modo'] != 'CHEQUE' else " - ".join(map(str, Cuentas.objects.filter(xcodigo=asiento['cuenta']).values_list('xcodigo', 'xnombre').first() or ('', ''))),
                        'centro': 'ADM',
                        'mov': int(movimiento_num) + 1,
                        'anio': fecha_obj.year,
                        'mes': fecha_obj.month,
                        'fechacheque': fecha_obj,
                        'paridad': cobranza[0]['paridad'],
                        'posicion': boleta.posicion if boleta.posicion else None

                    }  # haber
                    crear_asiento(asiento_vector_1)
                    if asiento.get('modo') == 'CHEQUE':
                        numero=asiento['nro_mediopago']
                        banco=asiento['banco']
                        fecha_vencimiento=asiento['vencimiento']
                        monto=asiento['total_pago']
                        autogenerado=autogenerado_impuventa
                        detalle=detalle_asiento
                        moneda=cobranza[0]['nromoneda']
                        nrocliente=cobranza[0]['nrocliente']
                        tipo_cheque='CH'
                        cheque = Cheques()
                        cheque.cnumero=numero
                        cheque.cbanco=banco
                        cheque.cfecha=fecha_obj
                        cheque.cvto=fecha_vencimiento
                        cheque.cmonto=monto
                        cheque.cautogenerado=autogenerado
                        cheque.cdetalle=detalle
                        cheque.ccliente=nrocliente
                        cheque.cmoneda=moneda
                        cheque.ctipo=tipo_cheque
                        cheque.save()

                #asiento general
                asiento_vector_2 = {  # deber
                    'detalle': detalle_asiento,
                    'monto': cobranza[0]['total'],
                    'moneda': cobranza[0]['nromoneda'],
                    'cambio': cobranza[0]['arbitraje'],
                    'asiento': nroasiento,
                    'conciliado': 'N',
                    'clearing': fecha_obj,
                    'fecha': fecha_obj,
                    'imputacion': 2,
                    'modo': None,
                    'tipo': 'Z',
                    'cuenta': cliente_data.ctavta,
                    'documento': cobranza[0]['numero'],
                    'vencimiento': fecha_obj,
                    'pasado': 0,
                    'autogenerado': autogenerado_impuventa,
                    'cliente': cliente_data.codigo,
                    'banco': 'S/I',
                    'centro': 'S/I',
                    'mov': movimiento_num,
                    'anio': fecha_obj.year,
                    'mes': fecha_obj.month,
                    'fechacheque': fecha_obj,
                    'paridad': cobranza[0]['paridad'],
                    'posicion': boleta.posicion if boleta.posicion else None
                }  # deber general
                crear_asiento(asiento_vector_2)
                #crear el movimiento
                movimiento_vec = {
                    'tipo': 25,
                    'fecha': fecha_obj,
                    'boleta': cobranza[0]['numero'],
                    'monto': 0,
                    'paridad': cobranza[0]['paridad'],
                    'iva': boleta.totiva,
                    'total': cobranza[0]['total'],
                    'saldo': movimiento[0]['saldo'],
                    'moneda': cobranza[0]['nromoneda'],
                    'detalle': movimiento[0]['boletas'],
                    'cliente': cliente_data.codigo,
                    'nombre': cliente_data.empresa,
                    'nombremov': 'COBRO',
                    'cambio': cobranza[0]['arbitraje'],
                    'autogenerado': autogenerado_impuventa,
                    'serie': cobranza[0]['serie'],
                    'prefijo': cobranza[0]['prefijo'],
                    'posicion': boleta.posicion if boleta else None,
                    'anio': fecha_obj.year,
                    'mes': fecha_obj.month,
                    'monedaoriginal': cobranza[0]['nromoneda'],
                    'montooriginal': cobranza[0]['total'],
                    'arbitraje': cobranza[0]['arbitraje'],

                }
                crear_movimiento(movimiento_vec)

            return JsonResponse({'status': 'exito'})
    except Exception as e:
        return JsonResponse({'status': 'Error: ' + str(e)})



def guardar_anticipo(request):
    try:
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            vector = body_data.get('vector', {})
            # imputaciones = vector.get('imputaciones', []) #pasar el numero de cliente
            asientos = vector.get('asiento', [])
           # movimiento = vector.get('movimiento', [])
            cobranza = vector.get('cobranza', [])

            autogenerado_impuventa = generar_autogenerado(datetime.now().strftime("%Y-%m-%d"))+'111'

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            arbitraje = float(cobranza[0]['arbitraje'])
            paridad = float(cobranza[0]['paridad'])
            nromoneda = int(cobranza[0]['nromoneda'])
            total = float(cobranza[0]['total'])
            saldo = float(cobranza[0].get('saldo', 0))


            if vector:
                monto=total
                cliente=cobranza[0]['nrocliente']
                impuventa = Impuvtas()
                impuventa.autogen = autogenerado_impuventa
                impuventa.tipo = 1
                impuventa.cliente = cliente
                impuventa.monto = monto
                impuventa.anticipo='S'
                impuventa.fechaimpu = fecha
                impuventa.save()

            try:
                cliente_data = Clientes.objects.get(codigo=cobranza[0]['nrocliente'])
            except Exception as _:
                cliente_data = None

            if cliente_data:
                for asiento in asientos:
                    fechaj = datetime.now().strftime("%Y-%m-%d")
                    fecha_obj = datetime.strptime(fechaj, '%Y-%m-%d')
                    nroasiento = generar_numero()
                    movimiento_num = modificar_numero(nroasiento)

                    detalle_asiento = 'COBRO' + cobranza[0]['serie'] +'-'+ str(cobranza[0]['prefijo']) +'-'+ str(cobranza[0]['numero']) +'-'+ cliente_data.empresa
                    asiento_monto = asiento['total_pago']

                    if nromoneda == 2:  # dolar
                        monto_asiento = float(asiento_monto) * arbitraje
                    elif nromoneda not in [1, 2]:
                        aux = float(asiento_monto) * paridad
                        monto_asiento = aux * arbitraje
                    else:
                        monto_asiento = 0

                    asiento_vector_1 = {
                        'detalle': detalle_asiento,
                        'monto': monto_asiento,
                        'moneda': cobranza[0]['nromoneda'],
                        'cambio': cobranza[0]['arbitraje'],
                        'asiento': nroasiento,
                        'conciliado': 'N',
                        'clearing': fecha_obj,
                        'fecha': fecha_obj,
                        'imputacion': 1,
                        'modo': asiento['modo'],
                        'tipo': 'Z',
                        'cuenta': asiento['cuenta'],
                        'documento': cobranza[0]['numero'],
                        'vencimiento': fecha_obj,
                        'pasado': 0,
                        'autogenerado': autogenerado_impuventa,
                        'cliente': cliente_data.codigo,
                        'banco': asiento['banco'] if asiento['modo'] != 'CHEQUE' else " - ".join(map(str, Cuentas.objects.filter(xcodigo=asiento['cuenta']).values_list('xcodigo', 'xnombre').first() or ('', ''))),
                        'centro': 'ADM',
                        'mov': int(movimiento_num) + 1,
                        'anio': fecha_obj.year,
                        'mes': fecha_obj.month,
                        'fechacheque': fecha_obj,
                        'paridad': cobranza[0]['paridad'],
                        'posicion': None

                    }  # haber
                    crear_asiento(asiento_vector_1)

                    if asiento.get('modo') == 'CHEQUE':
                        numero=asiento['nro_mediopago']
                        banco=asiento['banco']
                        fecha_vencimiento=asiento['vencimiento']
                        monto=asiento['total_pago']
                        autogenerado=autogenerado_impuventa
                        detalle=detalle_asiento
                        moneda=cobranza[0]['nromoneda']
                        nrocliente=cobranza[0]['nrocliente']
                        tipo_cheque='CH'
                        cheque = Cheques()
                        cheque.cnumero=numero
                        cheque.cbanco=banco
                        cheque.cfecha=fecha_obj
                        cheque.cvto=fecha_vencimiento
                        cheque.cmonto=monto
                        cheque.cautogenerado=autogenerado
                        cheque.cdetalle=detalle
                        cheque.ccliente=nrocliente
                        cheque.cmoneda=moneda
                        cheque.ctipo=tipo_cheque
                        cheque.cestado=2
                        cheque.save()

                #asiento general
                asiento_vector_2 = {  # deber
                    'detalle': detalle_asiento,
                    'monto': total,
                    'moneda': cobranza[0]['nromoneda'],
                    'cambio': cobranza[0]['arbitraje'],
                    'asiento': nroasiento,
                    'conciliado': 'N',
                    'clearing': fecha_obj,
                    'fecha': fecha_obj,
                    'imputacion': 2,
                    'modo': None,
                    'tipo': 'Z',
                    'cuenta': cliente_data.ctavta,
                    'documento': cobranza[0]['numero'],
                    'vencimiento': fecha_obj,
                    'pasado': 0,
                    'autogenerado': autogenerado_impuventa,
                    'cliente': cliente_data.codigo,
                    'banco': 'S/I',
                    'centro': 'S/I',
                    'mov': movimiento_num,
                    'anio': fecha_obj.year,
                    'mes': fecha_obj.month,
                    'fechacheque': fecha_obj,
                    'paridad': cobranza[0]['paridad'],
                    'posicion': None
                }  # deber general
                crear_asiento(asiento_vector_2)
                #crear el movimiento
                movimiento_vec = {
                    'tipo': 25,
                    'fecha': fecha_obj,
                    'boleta': cobranza[0]['numero'],
                    'monto': 0,
                    'paridad': cobranza[0]['paridad'],
                    'iva': 0,
                    'total': total,
                    'saldo': saldo,
                    'moneda': cobranza[0]['nromoneda'],
                    'detalle': 0,
                    'cliente': cliente_data.codigo,
                    'nombre': cliente_data.empresa,
                    'nombremov': 'COBRO',
                    'cambio': cobranza[0]['arbitraje'],
                    'autogenerado': autogenerado_impuventa,
                    'serie': cobranza[0]['serie'],
                    'prefijo': cobranza[0]['prefijo'],
                    'posicion': None,
                    'anio': fecha_obj.year,
                    'mes': fecha_obj.month,
                    'monedaoriginal': cobranza[0]['nromoneda'],
                    'montooriginal': total,
                    'arbitraje': cobranza[0]['arbitraje'],

                }
                crear_movimiento(movimiento_vec)

            return JsonResponse({'status': 'exito'})
    except Exception as e:
        return JsonResponse({'status': 'Error: ' + str(e)})

def crear_movimiento(movimiento):
    try:
        lista = Movims()
        lista.id = lista.get_id()
        lista.mtipo = movimiento['tipo']
        lista.mfechamov = movimiento['fecha']
        lista.mboleta = movimiento['boleta']
        lista.mmonto = movimiento['monto']
        lista.miva = movimiento['iva']
        lista.mtotal = movimiento['total']
        lista.msobretasa = 0
        lista.msaldo = movimiento['saldo']
        lista.mparidad = movimiento['paridad']
        lista.mvtomov = movimiento['fecha']
        lista.mmoneda = movimiento['moneda']
        lista.mdetalle = movimiento['detalle']
        lista.mcliente = movimiento['cliente']
        lista.mnombre = movimiento['nombre']
        lista.mnombremov = movimiento['nombremov']
        lista.mcambio = movimiento['cambio']
        lista.mautogen = movimiento['autogenerado']
        lista.mserie = movimiento['serie']
        lista.mprefijo = movimiento['prefijo']
        lista.mposicion = movimiento['posicion']
        lista.mmesimpu = movimiento['mes']
        lista.manoimpu = movimiento['anio']
        lista.mmonedaoriginal = movimiento['monedaoriginal']
        lista.marbitraje = movimiento['arbitraje']
        lista.mmontooriginal = movimiento['montooriginal']
        lista.save()

    except Exception as e:
        return JsonResponse({'status': 'Error:' + str(e)})

def crear_asiento(asiento):
    try:
        lista = Asientos()
        id = lista.get_id()
        lista.id = lista.get_id()
        lista.fecha = asiento['fecha']
        lista.asiento = asiento['asiento']
        lista.cuenta = asiento['cuenta']
        lista.imputacion = asiento['imputacion']
        lista.tipo = asiento['tipo']
        lista.documento = asiento['documento']
        lista.vto = asiento['vencimiento']
        lista.pasado = asiento['pasado']
        lista.autogenerado = asiento['autogenerado']
        lista.cliente = asiento['cliente']
        lista.banco = asiento['banco']
        lista.centro = "ADM"
        lista.mov = asiento['mov']
        lista.anoimpu = asiento['anio']
        lista.mesimpu = asiento['mes']
        lista.fechacheque = asiento['fechacheque']
        lista.paridad = asiento['paridad']
        lista.posicion = asiento['posicion']
        lista.monto = asiento['monto']
        lista.detalle = asiento['detalle']
        lista.cambio = asiento['cambio']
        lista.moneda = asiento['moneda']
        lista.save()

    except Exception as e:
        return JsonResponse({'status': 'Error: ' + str(e)})

def cargar_arbitraje(request):
    try:
        fecha_hoy = datetime.today().date()

        dolar_hoy = Dolar.objects.filter(ufecha__date=fecha_hoy).first()

        if dolar_hoy:
            return JsonResponse({
                'arbitraje': dolar_hoy.uvalor,
                'paridad': dolar_hoy.paridad,
                'contenido': True
            })
        else:
            return JsonResponse({
                'arbitraje': 0.0,
                'paridad': 0.0,
                'contenido': False
            })
    except Exception as e:
        # Manejar errores inesperados
        return JsonResponse({'error': str(e)}, status=500)