import json
from collections import defaultdict
from datetime import datetime
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.defaultfilters import length

from administracion_contabilidad.forms import OrdenPago
from administracion_contabilidad.views.facturacion import generar_numero, modificar_numero
from administracion_contabilidad.views.preventa import generar_autogenerado
from mantenimientos.models import Clientes, Monedas
from administracion_contabilidad.models import Asientos, VistaPagos, Dolar, Cheques, Impuordenes, Ordenes, Cuentas, \
    Movims

@login_required(login_url='/login')
def orden_pago_view(request):
    #if request.user.has_perms(["administracion_contabilidad.view_vistapagos", ]):
    if request.user.has_perms(["administracion_contabilidad.view_forzarerror", ]):
        form = OrdenPago(initial={'fecha':datetime.now()})
        return render(request, 'orden_pago.html', {'form': form})
    else:
        messages.error(request,'Funcionalidad en construcción.')
        return HttpResponseRedirect('/')

param_busqueda = {
    0: 'autogenerado__icontains',
    1: 'fecha__icontains',
    2: 'cliente__icontains',
    3: 'documento__icontains',
    4: 'total__icontains',
    5: 'monto__icontains',
    6: 'iva__icontains',
    7: 'moneda__icontains',
}

columns_table = {
    0: 'autogenerado',
    1: 'fecha',
    2: 'cliente',
    3: 'documento',
    4: 'total',
    5: 'monto',
    6: 'iva',
    7: 'moneda',
}

def source_ordenes(request):
    try:
        args = {}
        for i in range(10):  # Cambia el rango según el número de columnas reales
            key = f'columns[{i}][search][value]'
            args[str(i)] = request.GET.get(key, '')  # Usa un valor predeterminado si la clave no existe

        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        buscar = request.GET.get('buscar', '')
        que_buscar = request.GET.get('que_buscar', '')
        order = get_order(request, columns_table)

        if buscar:
            filtro[que_buscar] = buscar

        end = start + length

        # Consulta a la base de datos
        if filtro:
            registros = VistaPagos.objects.filter(**filtro,tipo_factura='O/PAGO').order_by(*order)
        else:
            registros = VistaPagos.objects.all().order_by(*order)

        finales=[]

        for r in registros:

            try:
                moneda_nombre = Monedas.objects.get(codigo=r.moneda).nombre if r.moneda in [1, 2, 3, 4, 5,
                                                                                            6] else ''
            except Monedas.DoesNotExist:
                moneda_nombre = ''

            finales.append({
                'autogenerado': r.autogenerado,
                'fecha': r.fecha.strftime('%Y-%m-%d') if r.fecha else '',
                'cliente': r.cliente,
                'documento': r.documento,
                'total': r.total,
                'monto': r.monto,
                'iva': r.iva,
                'moneda': moneda_nombre,
            })

        # Preparación de la respuesta
        resultado = {
            'data': finales[start:end],
            'length': length,
            'draw': request.GET.get('draw', '1'),
            'recordsTotal': VistaPagos.objects.count(),
            'recordsFiltered': len(finales),
        }
        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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
        return result
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

def buscar_proveedor(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()  # Obtener y limpiar el término de búsqueda
        proveedores = Clientes.objects.filter(empresa__icontains=query)[:10]  # Limitar resultados a 10
        results = [{'id': proveedor.id, 'text': proveedor.empresa} for proveedor in proveedores]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def buscar_proveedores(request):
    if request.method == "GET":
        proveedor_id = request.GET.get("codigo")
        proveedor = Clientes.objects.filter(codigo=proveedor_id).first()

        if proveedor:
            data = {
                'codigo': proveedor.codigo,
                'empresa': proveedor.empresa,
                'ruc': proveedor.ruc,
                'direccion': proveedor.direccion,
                'localidad': proveedor.localidad,
                'telefono': proveedor.telefono,
            }
            return JsonResponse(data)

    return JsonResponse({'error': 'Cliente no encontrado'}, status=404)


def obtener_imputables_old(request):
    proveedor_id = request.GET.get('codigo')

    # Obtener los parámetros de paginación
    start = int(request.GET.get('start', 0))  # Inicio de la página (offset)
    length = int(request.GET.get('length', 5))  # Número de registros por página
    # Filtrar los registros según el proveedor
    registros_totales = VistaPagos.objects.filter(nrocliente=proveedor_id)

    filtrados=[]
    for r in registros_totales:
        if r.tipo_factura!='anticipo':
            saldo = r.total - r.pago if r.pago is not None else r.total
            if saldo <0:
                saldo='error'
        else:
            saldo = -r.saldo

        pago = r.pago if r.pago is not None else 0
        if pago != r.total and saldo !='error':
            try:
                moneda_nombre = Monedas.objects.get(codigo=r.moneda).nombre if r.moneda in [1, 2, 3, 4, 5,6] else ''
            except Monedas.DoesNotExist:
                moneda_nombre = ''

            filtrados.append({
                'autogenerado': r.autogenerado,
                'fecha': r.fecha.strftime('%Y-%m-%d') if r.fecha else '',
                'documento': r.documento,
                'total': r.total,
                'monto': r.monto,
                'iva': r.iva,
                'tipo': r.tipo_factura,
                'moneda': moneda_nombre,
                'saldo': saldo,
                'imputado': 0
            })

    # Aplicar la paginación: [start:start+length] para obtener solo los registros de la página solicitada
    registros = filtrados[start:start + length]


    # Estructura de respuesta para DataTable
    response_data = {
        'draw': request.GET.get('draw', 0),  # Para mantener la coherencia con DataTable
        'recordsTotal': registros_totales.count(),  # Total de registros sin filtros
        'recordsFiltered': len(filtrados),
        # Total de registros después del filtrado (aplica el filtro de 'nrocliente')
        'data': registros  # Datos que se mostrarán en la tabla
    }

    return JsonResponse(response_data, safe=False)

def obtener_imputables(request):
    proveedor_id = request.GET.get('codigo')

    # Obtener los parámetros de paginación
    start = int(request.GET.get('start', 0))  # Inicio de la página (offset)
    length = int(request.GET.get('length', 5))  # Número de registros por página
    # Filtrar los registros según el proveedor
    registros_totales = VistaPagos.objects.filter(nrocliente=proveedor_id)

    filtrados=[]
    for r in registros_totales:

        try:
            moneda_nombre = Monedas.objects.get(codigo=r.moneda).nombre if r.moneda in [1, 2, 3, 4, 5,6] else ''
        except Monedas.DoesNotExist:
            moneda_nombre = ''

        filtrados.append({
            'autogenerado': r.autogenerado,
            'fecha': r.fecha,
            'documento': r.documento,
            'total': r.total,
            'monto': r.monto,
            'iva': r.iva,
            'tipo': r.tipo_factura,
            'moneda': moneda_nombre,
            'saldo': r.saldo,
            'imputado': 0
        })

    # Aplicar la paginación: [start:start+length] para obtener solo los registros de la página solicitada
    registros = filtrados[start:start + length]


    # Estructura de respuesta para DataTable
    response_data = {
        'draw': request.GET.get('draw', 0),  # Para mantener la coherencia con DataTable
        'recordsTotal': registros_totales.count(),  # Total de registros sin filtros
        'recordsFiltered': len(filtrados),
        # Total de registros después del filtrado (aplica el filtro de 'nrocliente')
        'data': registros  # Datos que se mostrarán en la tabla
    }

    return JsonResponse(response_data, safe=False)

@transaction.atomic
def guardar_impuorden(request):
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

                    boleta = VistaPagos.objects.filter(documento=item['nroboleta'],tipo_factura=item['source'])
                    if boleta.count() == 1:
                        monto = float(item['imputado']) #if boleta.tipo == 20 else -float(item['imputado']) if boleta.tipo == 21  else 0
                        impuordenes = Impuordenes()
                        impuordenes.autofac = boleta[0].autogenerado
                        impuordenes.numero = item['nroboleta']
                        impuordenes.prefijo = boleta[0].prefijo
                        impuordenes.serie = boleta[0].serie
                        impuordenes.orden = cobranza[0]['numero']
                        impuordenes.cliente = cobranza[0]['nrocliente']
                        impuordenes.monto = monto
                        impuordenes.save()
                    elif boleta.count() > 1:
                        raise TypeError('Error: mas de una boleta encontrada.')
                    else:
                        raise TypeError('Error: boleta no encontrada.')

            try:
                cliente_data = Clientes.objects.get(codigo=cobranza[0]['nrocliente'])
            except Exception as _:
                cliente_data = None

            orden = Ordenes()
            orden.mmonto=cobranza[0]['total']
            orden.mboleta=cobranza[0]['numero']
            orden.mfechamov=fecha
            orden.mmoneda=cobranza[0]['nromoneda']
            orden.mdetalle=movimiento[0]['boletas']
            orden.mcliente=cobranza[0]['nrocliente']
            orden.mactiva='N' if cobranza[0]['definitivo'] == True else 'S'
            orden.mcaja=11112 if cobranza[0]['nromoneda'] !=1 else 11111
            orden.mautogenmovims=autogenerado_impuventa if cobranza[0]['definitivo'] == True else None
            if cliente_data:
                orden.mnombre=cliente_data.empresa
            else:
                orden.mnombre=''
            orden.save()

            if cobranza[0]['definitivo'] == True:
                if cliente_data:
                    for asiento in asientos:
                        fechaj = datetime.now().strftime("%Y-%m-%d")
                        fecha_obj = datetime.strptime(fechaj, '%Y-%m-%d')
                        nroasiento = generar_numero()
                        movimiento_num = modificar_numero(nroasiento)

                        detalle_asiento = 'O/PAGO' +'-'+ str(cobranza[0]['numero']) +'-'+ cliente_data.empresa
                        asiento_vector_1 = {
                            'detalle': detalle_asiento,
                            'monto': asiento['total_pago'],
                            'moneda': cobranza[0]['nromoneda'],
                            'cambio': cobranza[0]['arbitraje'],
                            'asiento': nroasiento,
                            'conciliado': 'N',
                            'clearing': fecha_obj,
                            'fecha': fecha_obj,
                            'imputacion': 2,
                            'modo': asiento['modo'],
                            'tipo': 'G',
                            'cuenta': asiento['cuenta'],
                            'documento': cobranza[0]['numero'],
                            'vencimiento': fecha_obj,
                            'pasado': 1,
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
                        elif asiento.get('modo') == 'CHEQUE TERCEROS':
                            cheque=Cheques.objects.get(id=asiento['cuenta'])
                            cheque.cestado=2
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
                        'imputacion': 1,
                        'modo': None,
                        'tipo': 'G',
                        'cuenta': cliente_data.ctavta,
                        'documento': cobranza[0]['numero'],
                        'vencimiento': fecha_obj,
                        'pasado': 1,
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
                        'tipo': 45,
                        'fecha': fecha_obj,
                        'boleta': cobranza[0]['numero'],
                        'monto': 0,
                        'paridad': cobranza[0]['paridad'],
                        'iva': boleta[0].iva,
                        'total': cobranza[0]['total'],
                        'saldo': movimiento[0]['saldo'],
                        'moneda': cobranza[0]['nromoneda'],
                        'detalle': movimiento[0]['boletas'],
                        'cliente': cliente_data.codigo,
                        'nombre': cliente_data.empresa,
                        'nombremov': 'O/PAGO',
                        'cambio': cobranza[0]['arbitraje'],
                        'autogenerado': autogenerado_impuventa,
                        'serie': None,
                        'prefijo': None,
                        'posicion':None,
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
        lista.centro = asiento['centro']
        lista.mov = asiento['mov']
        lista.anoimpu = asiento['anio']
        lista.mesimpu = asiento['mes']
        lista.fechacheque = asiento['fechacheque']
        lista.paridad = asiento['paridad']
        lista.monto = asiento['monto']
        lista.detalle = asiento['detalle']
        lista.cambio = asiento['cambio']
        lista.moneda = asiento['moneda']
        lista.save()

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

def obtener_cheques_disponibles(request):

    # Obtener los parámetros de paginación
    start = int(request.GET.get('start', 0))  # Inicio de la página (offset)
    length = int(request.GET.get('length', 10))  # Número de registros por página
    cliente = int(request.GET.get('cliente', 0))  # Número de registros por página
    # Filtrar los registros según el proveedor
    if cliente and cliente!=0:
        cheques = Cheques.objects.filter(cestado=0,ccliente=cliente)
    else:
        cheques = Cheques.objects.filter(cestado=0)

    resultado=[]
    registros = cheques[start:start + length]
    for r in registros:
        try:
            cliente = Clientes.objects.get(codigo=r.ccliente).empresa if r.ccliente else ''
        except Clientes.DoesNotExist:
            cliente = ''

        resultado.append({
            'id': r.id,
            'vto': r.cvto.strftime('%Y-%m-%d') if r.cvto else '',
            'emision': r.cfecha.strftime('%Y-%m-%d') if r.cfecha else '',
            'banco': r.cbanco,
            'numero': r.cnumero,
            'cliente': cliente,
            'total': r.cmonto,
            'moneda':r.cmoneda
        })

    # Estructura de respuesta para DataTable
    response_data = {
        'draw': request.GET.get('draw', 0),  # Para mantener la coherencia con DataTable
        'recordsTotal': cheques.count(),  # Total de registros sin filtros
        'recordsFiltered': cheques.count(),
        # Total de registros después del filtrado (aplica el filtro de 'nrocliente')
        'data': resultado  # Datos que se mostrarán en la tabla
    }

    return JsonResponse(response_data, safe=False)

def guardar_anticipo_orden(request):
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
                orden = Ordenes()
                orden.mmonto = cobranza[0]['total']
                orden.mboleta = cobranza[0]['numero']
                orden.mfechamov = fecha
                orden.mmoneda = cobranza[0]['nromoneda']
                orden.mdetalle = None
                orden.mcliente = cobranza[0]['nrocliente']
                orden.mactiva = 'N' if cobranza[0]['definitivo'] == True else 'S'
                orden.mcaja = 11112 if cobranza[0]['nromoneda'] != 1 else 11111
                orden.mautogenmovims = autogenerado_impuventa if cobranza[0]['definitivo'] == True else None


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
                    detalle_asiento = 'O/PAGO' + '-' + str(cobranza[0]['numero']) + '-' + cliente_data.empresa
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
                        'pasado': 1,
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
                    'tipo': 'G',
                    'cuenta': cliente_data.ctavta,
                    'documento': cobranza[0]['numero'],
                    'vencimiento': fecha_obj,
                    'pasado': 1,
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