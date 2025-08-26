import json
from datetime import datetime
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.db import transaction
from django.shortcuts import render
from django.utils.dateformat import DateFormat
from num2words import num2words

from administracion_contabilidad.forms import Cobranza, CobranzasDetalleTabla, emailsForm
from administracion_contabilidad.models import Boleta, Impuvtas, Asientos, Movims, Cheques, Cuentas, VistaCobranza, \
    Dolar, ListaCobranzas
from administracion_contabilidad.views.facturacion import generar_numero, modificar_numero
from administracion_contabilidad.views.orden_pago import convertir_monto
from administracion_contabilidad.views.preventa import generar_autogenerado
from impomarit.views.mails import formatear_linea
from login.models import AccountEmail
from mantenimientos.models import Clientes, Monedas

from collections import defaultdict
from django.http import JsonResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist


param_busqueda = {
    1: 'autogenerado__icontains',
    2: 'fecha__icontains',
    3: 'numero__icontains',
    4: 'cliente__icontains',
    5: 'posicion__icontains',
    6: 'monto__icontains',
    7: 'iva__icontains',
    8: 'total__icontains',
}

columns_table = {
    0:'vacia',
    1: 'autogenerado',
    2: 'fecha',
    3: 'numero',
    4: 'cliente',
    5: 'posicion',
    6: 'monto',
    7: 'iva',
    8: 'total',
}




@login_required(login_url='/login')
def cobranza_view(request):
    if request.user.has_perms(["administracion_contabilidad.view_listacobranzas", ]):
        form = Cobranza(initial={'fecha':datetime.now().strftime('%Y-%m-%d') })
        detalle = CobranzasDetalleTabla()
        form_email = emailsForm()
        return render(request, 'cobranza.html', {'form': form,'detalle':detalle,'form_email':form_email})
    else:
        messages.error(request, 'No tiene permisos para realizar esta accion.')
        return HttpResponseRedirect('/')

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

        order = get_order(request, columns_table)
        if filtro:
            registros = ListaCobranzas.objects.filter(**filtro).order_by(*order)
        else:
            registros = ListaCobranzas.objects.all().order_by(*order)

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
        result.append('fecha')
        return result
    except Exception as e:
        raise TypeError(e)

def get_data(registros_filtrados):
    try:
        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str('COBRO'))
            registro_json.append('' if registro.autogenerado is None else str(registro.autogenerado))
            registro_json.append('' if registro.fecha is None else registro.fecha.strftime('%Y-%m-%d'))
            registro_json.append('' if registro.numero is None else str(registro.numero))
            registro_json.append('' if registro.cliente is None else str(registro.cliente))
            registro_json.append('' if registro.posicion is None else str(registro.posicion))
            registro_json.append(f"{float(registro.monto):.2f}" if registro.monto is not None else '')
            registro_json.append(f"{float(registro.iva):.2f}" if registro.iva is not None else '')
            registro_json.append(f"{float(registro.total):.2f}" if registro.total is not None else '')
            registro_json.append('' if registro.nrocliente is None else str(registro.nrocliente))
            registro_json.append('' if registro.numero is None else str(registro.numero))

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
        moneda_objetivo = request.GET.get('moneda')

        # Filtrar registros por cliente
        pendientes = VistaCobranza.objects.filter(nrocliente=cliente)

        # Paginación
        total_registros = pendientes.count()
        pendientes = pendientes[start:start + length]

        # Convertir los resultados en lista de diccionarios
        data = []
        for pendiente in pendientes:
            try:
                moneda_nombre = Monedas.objects.get(codigo=pendiente.moneda).nombre
            except ObjectDoesNotExist:
                moneda_nombre = "Desconocida"

            try:
                arbitraje, paridad = Movims.objects.filter(mautogen=pendiente.autogenerado).values_list('mcambio','mparidad').first() or (0, 0)
            except Exception:
                arbitraje, paridad = 0, 0

            total = float(pendiente.total or 0)
            saldo = float(pendiente.saldo or 0)

            arbitraje = float(arbitraje or 0)
            paridad = float(paridad or 0)

            total_convertido = convertir_monto(total, int(pendiente.moneda or 0), int(moneda_objetivo or 0), arbitraje, paridad)
            saldo_convertido = convertir_monto(saldo, int(pendiente.moneda or 0), int(moneda_objetivo or 0), arbitraje, paridad)

            data.append({
                'id': 0,
                'vencimiento': pendiente.vencimiento.strftime('%Y-%m-%d') if pendiente.vencimiento is not None else '',
                'emision': pendiente.emision.strftime('%Y-%m-%d') if pendiente.emision is not None else '',
                'documento': pendiente.documento,
                'total': total_convertido,
                'saldo': saldo_convertido,
                'imputado': pendiente.pago if pendiente.pago is not None else 0,
                'tipo_cambio': pendiente.arbitraje,
                'embarque': pendiente.embarque,
                'detalle': pendiente.detalle,
                'posicion': pendiente.posicion,
                'moneda': moneda_nombre,
                'paridad': pendiente.paridad,
                'tipo_doc': pendiente.tipo_doc,
                'source': pendiente.source,
            })

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': total_registros,
            'recordsFiltered': total_registros,
            'data': data,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})

def source_facturas_pendientes(request):
    try:
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        cliente = int(request.GET.get('cliente'))
        moneda_objetivo = request.GET.get('moneda')

        # Filtrar registros por cliente
        pendientes = Movims.objects.filter(mcliente=cliente,mactivo='S').exclude(msaldo=0)

        # Paginación
        total_registros = pendientes.count()
        pendientes = pendientes[start:start + length]

        # Convertir los resultados en lista de diccionarios
        data = []
        for pendiente in pendientes:


            total = float(pendiente.mtotal or 0)
            saldo = float(pendiente.msaldo or 0)

            arbitraje = float(pendiente.marbitraje or 0)
            paridad = float(pendiente.mparidad or 0)

            try:

                if arbitraje !=0:
                    total_convertido = convertir_monto(total, int(pendiente.mmoneda or 0), int(moneda_objetivo or 0), arbitraje, paridad)
                    saldo_convertido = convertir_monto(saldo, int(pendiente.mmoneda or 0), int(moneda_objetivo or 0), arbitraje, paridad)
                    moneda_nombre = Monedas.objects.get(codigo=moneda_objetivo).nombre
                else:
                    total_convertido=total
                    saldo_convertido=saldo
                    moneda_nombre = Monedas.objects.get(codigo=pendiente.mmoneda).nombre

            except ObjectDoesNotExist:
                moneda_nombre = "Desconocida"

            nro_completo = ""
            if pendiente.mserie and pendiente.mprefijo and pendiente.mboleta:
                s = str(pendiente.mserie)
                p = str(pendiente.mprefijo)

                tz = len(s) - len(s.rstrip('0'))
                lz = len(p) - len(p.lstrip('0'))

                sep = '0' * max(0, 3 - (tz + lz))

                nro_completo = f"{s}{sep}{p}-{pendiente.mboleta}"


            total_convertido = - total_convertido if pendiente.mtipo in [40,45,21,23] else total_convertido
            saldo_convertido = - saldo_convertido if pendiente.mtipo in [40,45,21,23] else saldo_convertido

            source = 'VERDE' if pendiente.mtipo in [20,21,23,24,25] else 'AZUL'

            data.append({
                'id': pendiente.mautogen,
                'vencimiento': pendiente.mfechamov.strftime('%d-%m-%Y') if pendiente.mfechamov is not None else '',
                'emision': pendiente.mfechamov.strftime('%d-%m-%Y') if pendiente.mfechamov is not None else '',
                'documento': nro_completo,
                'total': total_convertido,
                'saldo': saldo_convertido,
                'imputado': 0 ,
                'tipo_cambio': arbitraje,
                'embarque': pendiente.mposicion,
                'detalle': pendiente.mdetalle,
                'posicion': pendiente.mposicion,
                'moneda': moneda_nombre,
                'paridad': paridad,
                'tipo_doc': pendiente.mnombremov,
                'tipo': pendiente.mtipo,
                'source': source,
            })

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': total_registros,
            'recordsFiltered': total_registros,
            'data': data,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})


def guardar_impuventa(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                vector = body_data.get('vector', {})
                imputaciones = vector.get('imputaciones', [])
                asientos = vector.get('asiento', [])
                movimiento = vector.get('movimiento', [])
                cobranza = vector.get('cobranza', [])

                verificar_num=int(cobranza[0]['numero'])
                verif= Movims.objects.filter(mboleta=verificar_num,mnombremov='COBRO')
                if verif.exists():
                    return JsonResponse({'status': 'Error: ' + 'El número ingresado para la cobranza, ya existe.'})

                autogenerado_impuventa = generar_autogenerado(datetime.now().strftime("%Y-%m-%d"))
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if vector and imputaciones:
                    for item in imputaciones:

                        try:
                            #nro = item['nroboleta'].split('-')[1]
                            boleta = Boleta.objects.filter(autogenerado=item['nroboleta']).order_by('-id').first()
                        except Exception as _:
                            boleta = None
                            return JsonResponse({'status': 'Error: Boleta no encontrada.' })

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

                            movimiento_fac=Movims.objects.filter(mautogen=boleta.autogenerado).first()
                            if movimiento_fac:
                                movimiento_fac.msaldo=float(movimiento_fac.msaldo)-float(item['imputado'])
                                movimiento_fac.save()

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
                            'posicion': boleta.posicion if boleta else None

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
                            cheque.cestado=0
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

                return JsonResponse({'status': 'exito', 'autogenerado': autogenerado_impuventa})
            return None
    except Exception as e:
        return JsonResponse({'status': 'Error: ' + str(e)})

def guardar_anticipo(request):
    try:
        with transaction.atomic():
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
                        'saldo': total if saldo == 0 else saldo,
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
        lista.mactivo = 'S'
        lista.mmontooriginal = movimiento['montooriginal']
        lista.save()

    except Exception as e:
        raise

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
        lista.modo = asiento['modo']
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
        raise

def cargar_arbitraje(request):
    try:
        fecha_str = request.GET.get('fecha')
        if not fecha_str:
            return JsonResponse({'error': 'Fecha no proporcionada'}, status=400)

        # Convertir string a objeto date
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()

        dolar_hoy = Dolar.objects.filter(ufecha__date=fecha).first()

        if dolar_hoy:
            return JsonResponse({
                'arbitraje': dolar_hoy.uvalor,
                'paridad': dolar_hoy.paridad,
                'pizarra': dolar_hoy.upizarra,
                'moneda': dolar_hoy.umoneda,
                'contenido': True
            })
        else:
            return JsonResponse({
                'arbitraje': 0.0,
                'paridad': 0.0,
                'pizarra': 0.0,
                'moneda': 2,
                'contenido': False
            })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def obtener_proximo_mboleta(request):
    try:
        ultima = Movims.objects.filter(mtipo=25).order_by('-id').first()
        proximo = int(ultima.mboleta) + 1 if ultima and ultima.mboleta.isdigit() else 1
        return JsonResponse({'proximo_mboleta': str(proximo)})
    except Exception as e:
        return JsonResponse({'error': f'Error al obtener mboleta: {str(e)}'}, status=500)

def get_email_recibo_cobranza(request):
    try:
        autogenerado = request.POST.get("autogenerado")
        cobro = Movims.objects.filter(mautogen=autogenerado).first()
        if not cobro:
            return JsonResponse({'resultado': 'error', 'detalle': 'Cobro no encontrado'})

        fecha = cobro.mfechamov.strftime("%d/%m/%Y")
        nombre = f"{request.user.first_name} {request.user.last_name}"
        cliente = Clientes.objects.filter(codigo=cobro.mcliente).first()
        email_cliente = cliente.emailim if cliente and cliente.emailim else ""
        moneda = Monedas.objects.filter(codigo=cobro.mmoneda).first()

        texto = ""
        texto += "<p style='font-family: Courier New, monospace; font-size: 14px; font-weight: bold;'>OCEANLINK LTDA</p>"
        texto += '<br><span style="display: block; border-top: 0.5pt solid #CCC; margin: 6px 0;"></span><br>'
        texto += formatear_linea("Comprobante", "Recibo confirmado")
        texto += formatear_linea("Número", cobro.mboleta or "S/I")
        texto += formatear_linea("Fecha emisión", fecha)
        texto += formatear_linea("Emitido por", nombre)
        texto += '<br>'
        texto += formatear_linea("Cliente", cobro.mnombre or "S/I")
        texto += '<br><span style="display: block; border-top: 0.5pt solid #CCC; margin: 6px 0;"></span><br>'
        texto += formatear_linea("Moneda", moneda.nombre)
        texto += formatear_linea("Cotización", cobro.mcambio)
        texto += formatear_linea("Monto a cobrar", cobro.mtotal)
        texto += formatear_linea("Detalle", cobro.mdetalle or "S/I")
        texto += '<br>'

        texto += "<p style='font-family: Courier New, monospace; font-size: 12px;'>Facturas canceladas:</p>"
        texto += """
        <table style='border:none;font-family: Courier New, monospace; font-size: 12px; border-collapse: collapse; width: auto;'>
            <thead>
                <tr>
                    <th style='padding: 0 10px; text-align: left;'>Factura</th>
                    <th style='padding: 0 10px; text-align: left;'>Detalle</th>
                    <th style='padding: 0 10px; text-align: right;'>Monto</th>
                </tr>
            </thead>
            <tbody>
        """
        imputaciones = Impuvtas.objects.filter(autogen=autogenerado)
        for imp in imputaciones:
            boleta = Movims.objects.filter(mautogen=imp.autofac).first()
            if boleta:
                num_completo = f"{boleta.mserie}{boleta.mprefijo}{boleta.mboleta}"
                texto += f"""
                <tr>
                    <td style='padding: 0 10px;'>{num_completo}</td>
                    <td style='padding: 0 10px;'>{boleta.mdetalle or ''}</td>
                    <td style='padding: 0 10px; text-align: right;'>{boleta.mtotal:.2f}</td>
                </tr>
                """
        texto += "</tbody></table><br>"

        texto += '<br><span style="display: block; border-top: 0.5pt solid #CCC; margin: 6px 0;"></span><br>'

        texto += "<p style='font-family: Courier New, monospace; font-size: 12px;'>Formas de cobro:</p>"
        texto += """
        <table style='border:none;font-family: Courier New, monospace; font-size: 12px; border-collapse: collapse; width: auto;'>
            <thead>
                <tr>
                    <th style='padding: 0 10px; text-align: left;'>Banco</th>
                    <th style='padding: 0 10px; text-align: right;'>Monto</th>
                    <th style='padding: 0 10px; text-align: left;'>Medio</th>
                </tr>
            </thead>
            <tbody>
        """
        formas = Asientos.objects.filter(autogenerado=autogenerado, imputacion=1)
        for f in formas:
            texto += f"""
            <tr>
                <td style='padding: 0 10px;'>{f.banco or ''}</td>
                <td style='padding: 0 10px; text-align: right;'>{f.monto:.2f}</td>
                <td style='padding: 0 10px;'>{f.modo or ''}</td>
            </tr>
            """
        texto += "</tbody></table><br>"

        texto += '<br><span style="display: block; border-top: 0.5pt solid #CCC; margin: 6px 0;"></span><br>'

        texto += f"<p style='font-family: Courier New, monospace; font-size: 12px;'>{monto_a_letras(cobro.mtotal, cobro.mmoneda)}</p>"
        emails_disponibles = list(AccountEmail.objects.filter(user=request.user).values_list('email', flat=True))
        return JsonResponse({
            'resultado': 'exito',
            'mensaje': texto,
            'asunto': f"RECIBO DE COBRANZA - {cobro.mnombre}",
            'email_cliente': email_cliente,
            'emails_disponibles': emails_disponibles
        })

    except Exception as e:
        return JsonResponse({'resultado': 'error', 'detalle': str(e)})

def monto_a_letras(monto, moneda):
    try:
        monto = float(str(monto).replace(",", ""))  # Asegura formato numérico
        enteros = int(monto)
        decimales = int(round((monto - enteros) * 100))
        letras = num2words(enteros, lang='es').upper()
        return f"SON {moneda} {letras} CON {decimales:02d}/100."
    except:
        return f"SON {moneda} S/I"