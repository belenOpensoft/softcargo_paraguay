import json
from datetime import datetime
from os import times

from click import DateTime
from django.db.models import Q, OuterRef, Subquery
from django.db.transaction import atomic
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from administracion_contabilidad.forms import Cobranza
from administracion_contabilidad.models import Boleta, Impuvtas, Asientos, Movims, Cheques, Cuentas
from administracion_contabilidad.views.facturacion import generar_numero, modificar_numero
from administracion_contabilidad.views.preventa import generar_autogenerado
from mantenimientos.models import Clientes, Monedas, Bancos

param_busqueda = {
    1: 'autogenerado__icontains',
    2: 'serie__icontains',
    3: 'prefijo__icontains',
    4: 'numero__icontains',
    5: 'cliente__icontains',
    6: 'master__icontains',
    7: 'house__icontains',
    8: 'concepto__icontains',
    9: 'monto__icontains',
    10: 'iva__icontains',
    11: 'totiva__icontains',
    12: 'total__icontains',
}

columns_table = {
    0: 'autogenerado',
    1: 'serie',
    2: 'prefijo',
    3: 'numero',
    4: 'cliente',
    5: 'master',
    6: 'house',
    7: 'concepto',
    8: 'monto',
    9: 'iva',
    10: 'totiva',
    11: 'total',
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
    args = {
        '1': request.GET['columns[1][search][value]'],
        '2': request.GET['columns[2][search][value]'],
        '3': request.GET['columns[3][search][value]'],
        '4': request.GET['columns[4][search][value]'],
        '5': request.GET['columns[5][search][value]'],
        '6': request.GET['columns[6][search][value]'],
        '7': request.GET['columns[7][search][value]'],
        '8': request.GET['columns[8][search][value]'],
        '9': request.GET['columns[9][search][value]'],
        '10': request.GET['columns[10][search][value]'],
        '11': request.GET['columns[11][search][value]'],
        '12': request.GET['columns[12][search][value]'],
    }
    filtro = get_argumentos_busqueda(**args)
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    buscar = str(request.GET['buscar'])
    que_buscar = str(request.GET['que_buscar'])
    if len(buscar) > 0:
        filtro[que_buscar] = buscar
    end = start + length
    order = get_order(request, columns_table)
    if filtro:
        registros = Boleta.objects.filter(**filtro).order_by(*order)
    else:
        registros = Boleta.objects.all().order_by(*order)
    resultado = {}
    data = get_data(registros[start:end])
    resultado['data'] = data
    resultado['length'] = length
    resultado['draw'] = request.GET['draw']
    resultado['recordsTotal'] = Boleta.objects.all().count()
    resultado['recordsFiltered'] = str(registros.count())
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def get_data(registros_filtrados):
    try:
        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.autogenerado is None else str(registro.autogenerado))
            registro_json.append('' if registro.prefijo is None else str(registro.prefijo))
            registro_json.append('' if registro.serie is None else str(registro.serie))
            registro_json.append('' if registro.numero is None else str(registro.numero))
            registro_json.append('' if registro.cliente is None else str(registro.cliente))
            registro_json.append('' if registro.master is None else str(registro.master))
            registro_json.append('' if registro.house is None else str(registro.house))
            registro_json.append('' if registro.concepto is None else str(registro.concepto))
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


def get_order(request, columns):
    try:
        result = []
        order_column = request.GET['order[0][column]']
        order_dir = request.GET['order[0][dir]']
        order = columns[int(order_column)]
        if order_dir == 'desc':
            order = '-' + columns[int(order_column)]
        result.append(order)
        i = 1
        while i > 0:
            try:
                order_column = request.GET['order[' + str(i) + '][column]']
                order_dir = request.GET['order[' + str(i) + '][dir]']
                order = columns[int(order_column)]
                if order_dir == 'desc':
                    order = '-' + columns[int(order_column)]
                result.append(order)
                i += 1
            except Exception as e:
                i = 0
        result.append('id')
        return result
    except Exception as e:
        raise TypeError(e)

def source_facturas_pendientes(request):
    try:
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        cliente = int(request.GET.get('cliente'))

        anio_limite = 2010

        infofacturas_qs = Boleta.objects.all()


        subquery = infofacturas_qs.filter(numero=OuterRef('numero')).order_by('id').values('id')[:1]

        infofacturas_qs = infofacturas_qs.filter(
            Q(autogenerado__gte=str(anio_limite)) &
            Q(nrocliente=cliente) &
            Q(tipo=20)
        ).exclude(
            autogenerado__in=Impuvtas.objects.values('autofac')
        ).filter(
            id=Subquery(subquery)  # Filtra solo los registros con el ID devuelto por la subconsulta
        )

        total_registros = infofacturas_qs.count()

        infofacturas_paginated = infofacturas_qs[start:start + length]

        data = [{
            'id':boleta.id,
            'vencimiento':boleta.vto,
            'emision':boleta.fecha,
            'documento':boleta.numero,
            'total': boleta.total,
            'saldo':boleta.total,
            'imputado':0,
            'tipo_cambio':boleta.cambio,
            'embarque':boleta.refer,
            'detalle':boleta.detalle,
            'posicion':boleta.posicion,
            'moneda': Monedas.objects.get(codigo=boleta.moneda).nombre,
            'paridad':boleta.paridad,
            'tipo_doc':"FACTURA",
        } for boleta in infofacturas_paginated]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': total_registros,
            'recordsFiltered': total_registros,
            'data': data,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})

@atomic
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
                for nroboleta in imputaciones:

                    try:
                        boleta = Boleta.objects.filter(numero=nroboleta['nroboleta']).order_by('-id').first()
                    except Exception as _:
                        boleta = None

                    if boleta:
                        autofac = boleta.autogenerado
                        parteiva=boleta.totiva
                        monto=boleta.total
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
                    #total_pago total indiviual de cada medio de pago (ver si se genera un asiento por cada medio de pago)
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

            autogenerado_impuventa = generar_autogenerado(datetime.now().strftime("%Y-%m-%d"))
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if vector:
                monto=cobranza[0]['total']
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
                    'total': cobranza[0]['total'],
                    'saldo': 0,
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
                    'montooriginal': cobranza[0]['total'],
                    'arbitraje': cobranza[0]['arbitraje'],

                }
                crear_movimiento(movimiento_vec)

            return JsonResponse({'status': 'exito'})
    except Exception as e:
        return JsonResponse({'status': 'Error: ' + str(e)})

#sin hacer
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