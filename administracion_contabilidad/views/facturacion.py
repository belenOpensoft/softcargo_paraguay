import json
import re

from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from administracion_contabilidad.views.facturacion_electronica import Uruware
from expaerea.models import ExportEmbarqueaereo
from expmarit.models import ExpmaritEmbarqueaereo
from expterrestre.models import ExpterraEmbarqueaereo
from impaerea.models import ImportEmbarqueaereo
from impterrestre.models import ImpterraEmbarqueaereo
from mantenimientos.models import Clientes, Servicios, Monedas
from administracion_contabilidad.forms import Factura
from administracion_contabilidad.models import Boleta, PendienteFacturar, Asientos, Movims, Infofactura, \
    VistaGastosPreventa, Dolar, Factudif, VPreventas
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.db import transaction
from django.db.models import F
from impomarit.models import VGastosHouse, Envases, Cargaaerea, Embarqueaereo
from decimal import Decimal
from administracion_contabilidad.forms import pdfForm

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


def source_facturacion(request):
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

@login_required(login_url='/login')
def facturacion_view(request):
    if request.user.has_perms(["administracion_contabilidad.view_boleta", ]):
        form = Factura(request.POST or None)
        return render(request, 'facturacion.html', {'form': form,'form_pdf': pdfForm(),})
    else:
        messages.error(request, 'No tiene permisos para realizar esta accion.')
        return HttpResponseRedirect('/')

def buscar_cliente(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()  # Obtener y limpiar el término de búsqueda
        clientes = Clientes.objects.filter(empresa__icontains=query)[:10]  # Limitar resultados a 10
        results = [{'id': cliente.codigo, 'text': cliente.empresa} for cliente in clientes]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def buscar_clientes(request):
    if request.method == "GET":
        cliente_id = request.GET.get("id")
        cliente = Clientes.objects.filter(codigo=cliente_id).first()

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


def buscar_item_v(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()

        servicios = Servicios.objects.filter(nombre__icontains=query, tipogasto='V')[:10]

        results = [{'id': servicio.id, 'text': servicio.nombre} for servicio in servicios]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def buscar_items_v(request):
    if request.method == "GET":
        servicio_id = request.GET.get("id")
        servicio = Servicios.objects.filter(id=servicio_id, tipogasto='V').first()

        if servicio:
            iva_texto = "Exento" if servicio.tasa == "X" else "Basico" if servicio.tasa == "B" else "Desconocido"

            data = {
                'item': servicio.codigo,
                'nombre': servicio.nombre,
                'iva': iva_texto,
                'cuenta': servicio.contable,
            }
            return JsonResponse(data)

    return JsonResponse({'error': 'Servicio no encontrado'}, status=404)


def generar_autogenerado(tipo, hora, fecha, numero):
    fecha = fecha.replace('-', '')
    fecha_hora = fecha + hora
    tipo = tipo
    autogenerado = f"{fecha_hora}{tipo}{numero}"

    return autogenerado

@transaction.atomic
def procesar_factura(request):
    try:
        if request.method == 'POST':
            lista = Boleta.objects.last()
            numero = int(lista.numero) + 1
            hora = datetime.now().strftime('%H%M%S%f')
            fecha = request.POST.get('fecha')
            tipo = request.POST.get('tipoFac', 0)

            preventa = json.loads(request.POST.get('preventa'))
            if preventa:
                autogenerado=preventa.get('autogenerado')
                master=preventa.get('master')
                house=preventa.get('house')
                posicion=preventa.get('posicion')
                kilos=preventa.get('kilos')
                bultos=preventa.get('bultos')
                terminos=preventa.get('incoterms')
                pagoflete=preventa.get('pago')
                origen=preventa.get('origen')
                destino=preventa.get('destino')
                seguimiento=preventa.get('seguimiento')

                reg=Factudif.objects.filter(znumero=autogenerado)
                for r in reg:
                    r.zfacturado='S'
                    r.save()


            else:
                autogenerado=generar_autogenerado(tipo, hora, fecha, numero)
                master=None
                house=None
                posicion=None
                kilos=None
                bultos=None
                terminos=None
                pagoflete=None
                origen=None
                destino=None
                seguimiento=None


            serie = request.POST.get('serie', "")
            prefijo = request.POST.get('prefijo', 0)
            moneda = request.POST.get('moneda', "")
            arbitraje = request.POST.get('arbitraje', 0)
            paridad = request.POST.get('paridad', 0)
            cliente_data = json.loads(request.POST.get('clienteData'))
            codigo_cliente = cliente_data['codigo']
            cliente = Clientes.objects.get(codigo=codigo_cliente)
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')

            precio_total = request.POST.get('total', 0)
            neto = request.POST.get('neto', 0)
            iva = request.POST.get('iva', 0)

            items_data = json.loads(request.POST.get('items'))

            tipo_mov = tipo
            tipo_asiento = 'V'
            detalle1 = 'S/I'
            detalle_mov = "detallemov"  #si viene de la preventa, sino vacio
            nombre_mov = ""
            asiento = generar_numero()
            movimiento_num = modificar_numero(asiento)

            if int(tipo) == 23:
                detalle1 = 'e-VTA/CRED'
                nombre_mov = 'CONTADO'
            elif int(tipo) == 24:
                detalle1 = 'e-NOT/CRED'
                tipo_asiento = 'V'
                nombre_mov = 'CONTADO'
            elif int(tipo) == 11:
                detalle1 = 'DEV/CTDO'
                nombre_mov = 'DEVOLUCION'
            elif int(tipo) == 21:
                detalle1 = 'NOT/CRED'
                tipo_asiento = 'V'
                nombre_mov = 'NOTA CRED.'
            elif int(tipo) == 20:
                detalle1 = 'VTA/CRED'
                tipo_asiento = 'V'
                nombre_mov = 'FACTURA'

           # detalle_asiento = detalle1 + serie + str(prefijo) + str(numero) + cliente.empresa
            detalle_asiento = detalle1 + '-' + serie + '-' + str(prefijo) + '-' + str(numero) + '-' + cliente.empresa


            movimiento = {
                'tipo': tipo_mov,
                'fecha': fecha_obj,
                'boleta': numero,
                'monto': neto,
                'iva': iva,
                'total': precio_total,
                'saldo': precio_total,
                'moneda': moneda,
                'detalle': detalle_mov,
                'cliente': cliente.codigo,
                'nombre': cliente.empresa,
                'nombremov': nombre_mov,
                'cambio': arbitraje,
                'autogenerado': autogenerado,
                'serie': serie,
                'prefijo': prefijo,
                'posicion': posicion,
                'anio': fecha_obj.year,
                'mes': fecha_obj.month,
                'monedaoriginal': moneda,
                'montooriginal': precio_total,
                'arbitraje': arbitraje
            }
            asiento_general = {
                'detalle': detalle_asiento,
                'asiento': asiento,
                'monto': precio_total,
                'moneda': moneda,
                'cambio': arbitraje,
                'conciliado': 'N',
                'clearing': fecha_obj,
                'fecha': fecha_obj,
                'imputacion': 1,
                'tipo': tipo_asiento,
                'cuenta': cliente.ctavta,
                'documento': str(numero),
                'vencimiento': fecha_obj,
                'pasado': 0,
                'autogenerado': autogenerado,
                'cliente': cliente.codigo,
                'banco': 'S/I',
                'centro': 'S/I',
                'mov': movimiento_num,
                'anio': fecha_obj.year,
                'mes': fecha_obj.month,
                'fechacheque': fecha_obj,
                'paridad': paridad
            }
            crear_movimiento(movimiento)
            crear_asiento(asiento_general)

            for item_data in items_data:
                aux = int(movimiento_num) + 1
                precio = float(item_data.get('precio'))
                coniva = 0
                totaliva = 0
                if item_data.get('iva') == 'Basico':
                    coniva = precio * 1.22
                    totaliva = precio * 0.22
                else:
                    coniva = precio
                    totaliva = 0

                boleta = Boleta()
                numero = numero
                boleta.autogenerado = autogenerado
                boleta.tipo = tipo
                boleta.fecha = fecha
                boleta.vto = fecha
                boleta.tipofactura = serie
                boleta.serie = serie
                boleta.prefijo = prefijo
                boleta.numero = numero
                boleta.nrocliente = cliente.codigo
                boleta.cliente = cliente.empresa
                boleta.direccion = cliente.direccion
                boleta.direccion2 = cliente.direccion2
                boleta.localidad = cliente.localidad
                boleta.ciudad = cliente.ciudad
                boleta.pais = cliente.pais
                boleta.telefax = cliente.telefono
                boleta.ruc = cliente.ruc
                boleta.condiciones = 'S/I'
                boleta.corporativo = 'S/I'
                boleta.moneda = moneda
                boleta.cambio = arbitraje
                boleta.paridad = paridad
                boleta.tipocliente = 'RESPONSABLE INSCRIPTO'
                boleta.nroservicio = item_data.get('id')
                boleta.descripcion = item_data.get('descripcion')
                boleta.precio = item_data.get('precio')
                boleta.iva = item_data.get('iva')
                boleta.cuenta = item_data.get('cuenta')
                boleta.monto = item_data.get('precio')
                boleta.totiva = totaliva
                boleta.total = coniva
                boleta.master=master
                boleta.house=house
                boleta.posicion=posicion
                boleta.kilos=kilos
                boleta.bultos=bultos
                boleta.terminos=terminos
                boleta.pagoflete=pagoflete
                boleta.origen=origen
                boleta.destino=destino
                boleta.seguimiento=seguimiento
                boleta.save()

                asiento_vector = {
                    'detalle': detalle_asiento,
                    'monto': item_data.get('precio'),
                    'moneda': moneda,
                    'cambio': arbitraje,
                    'asiento': asiento,
                    'conciliado': 'N',
                    'clearing': fecha_obj,
                    'fecha': fecha_obj,
                    'imputacion': 2,
                    'tipo': tipo_asiento,
                    'cuenta': item_data.get('cuenta'),
                    'documento': str(numero),
                    'vencimiento': fecha_obj,
                    'pasado': 0,
                    'autogenerado': autogenerado,
                    'cliente': cliente.codigo,
                    'banco': 'S/I',
                    'centro': 'S/I',
                    'mov': aux,
                    'anio': fecha_obj.year,
                    'mes': fecha_obj.month,
                    'fechacheque': fecha_obj,
                    'paridad': paridad
                }
                crear_asiento(asiento_vector)
                movimiento_num = aux

            return JsonResponse({'status': 'Factura procesada correctamente N° ' + str(numero)})
    except Exception as e:
        return JsonResponse({'status': 'Error: ' + str(e)})
# @transaction.atomic
# def procesar_factura(request):
#     try:
#         if request.method == 'POST':
#             lista = Boleta.objects.last()
#             numero = int(lista.numero) + 1
#             hora = datetime.now().strftime('%H%M%S%f')
#             fecha = request.POST.get('fecha')
#             tipo = request.POST.get('tipoFac', 0)
#
#             preventa = json.loads(request.POST.get('preventa'))
#             if preventa!=0:
#                 autogenerado=preventa.get('autogenerado')
#                 master=preventa.get('master')
#                 house=preventa.get('house')
#                 posicion=preventa.get('posicion')
#                 kilos=preventa.get('kilos')
#                 bultos=preventa.get('bultos')
#                 terminos=preventa.get('incoterms')
#                 pagoflete=preventa.get('pago')
#                 origen=preventa.get('origen')
#                 destino=preventa.get('destino')
#                 seguimiento=preventa.get('seguimiento')
#             else:
#                 autogenerado=generar_autogenerado(tipo, hora, fecha, numero)
#                 master=None
#                 house=None
#                 posicion=None
#                 kilos=None
#                 bultos=None
#                 terminos=None
#                 pagoflete=None
#                 origen=None
#                 destino=None
#                 seguimiento=None
#
#
#             serie = request.POST.get('serie', "")
#             prefijo = request.POST.get('prefijo', 0)
#             moneda = request.POST.get('moneda', "")
#             arbitraje = request.POST.get('arbitraje', 0)
#             paridad = request.POST.get('paridad', 0)
#             cliente_data = json.loads(request.POST.get('clienteData'))
#             codigo_cliente = cliente_data['codigo']
#             cliente = Clientes.objects.get(codigo=codigo_cliente)
#             fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
#
#             precio_total = request.POST.get('total', 0)
#             neto = request.POST.get('neto', 0)
#             iva = request.POST.get('iva', 0)
#
#             if moneda == 2:  # dolar
#                 total_convertido = precio_total * arbitraje
#                 neto_convertido = neto * arbitraje
#             elif moneda not in [1, 2]:
#                 aux = precio_total * paridad
#                 total_convertido = aux * arbitraje
#                 aux1 = neto * paridad
#                 neto_convertido = aux1 * arbitraje
#             else:
#                 total_convertido = 0
#                 neto_convertido = 0
#
#             items_data = json.loads(request.POST.get('items'))
#
#             tipo_mov = tipo
#             tipo_asiento = 'V'
#             detalle1 = 'S/I'
#             detalle_mov = "detallemov"  #si viene de la preventa, sino vacio
#             nombre_mov = ""
#             asiento = generar_numero()
#             movimiento_num = modificar_numero(asiento)
#
#             if int(tipo) == 23:
#                 detalle1 = 'e-VTA/CRED'
#                 nombre_mov = 'CONTADO'
#             elif int(tipo) == 24:
#                 detalle1 = 'e-NOT/CRED'
#                 tipo_asiento = 'V'
#                 nombre_mov = 'CONTADO'
#             elif int(tipo) == 11:
#                 detalle1 = 'DEV/CTDO'
#                 nombre_mov = 'DEVOLUCION'
#             elif int(tipo) == 21:
#                 detalle1 = 'NOT/CRED'
#                 tipo_asiento = 'V'
#                 nombre_mov = 'NOTA CRED.'
#             elif int(tipo) == 20:
#                 detalle1 = 'VTA/CRED'
#                 tipo_asiento = 'V'
#                 nombre_mov = 'FACTURA'
#
#             detalle_asiento = detalle1 + serie + str(prefijo) + str(numero) + cliente.empresa
#
#             movimiento = {
#                 'tipo': tipo_mov,
#                 'fecha': fecha_obj,
#                 'boleta': numero,
#                 'monto': neto_convertido,
#                 'iva': iva,
#                 'total': total_convertido,
#                 'saldo': total_convertido,
#                 'moneda': moneda,
#                 'detalle': detalle_mov,
#                 'cliente': cliente.codigo,
#                 'nombre': cliente.empresa,
#                 'nombremov': nombre_mov,
#                 'cambio': arbitraje,
#                 'autogenerado': autogenerado,
#                 'serie': serie,
#                 'prefijo': prefijo,
#                 'posicion': posicion,
#                 'anio': fecha_obj.year,
#                 'mes': fecha_obj.month,
#                 'monedaoriginal': moneda,
#                 'montooriginal': total_convertido,
#                 'arbitraje': arbitraje
#             }
#             asiento_general = {
#                 'detalle': detalle_asiento,
#                 'asiento': asiento,
#                 'monto': total_convertido,
#                 'moneda': moneda,
#                 'cambio': arbitraje,
#                 'conciliado': 'N',
#                 'clearing': fecha_obj,
#                 'fecha': fecha_obj,
#                 'imputacion': None,
#                 'tipo': tipo_asiento,
#                 'cuenta': 0,
#                 'documento': str(numero),
#                 'vencimiento': fecha_obj,
#                 'pasado': 0,
#                 'autogenerado': autogenerado,
#                 'cliente': cliente.codigo,
#                 'banco': 'S/I',
#                 'centro': 'S/I',
#                 'mov': movimiento_num,
#                 'anio': fecha_obj.year,
#                 'mes': fecha_obj.month,
#                 'fechacheque': fecha_obj,
#                 'paridad': paridad
#             }
#             crear_movimiento(movimiento)
#             crear_asiento(asiento_general)
#
#             for item_data in items_data:
#                 aux = int(movimiento_num) + 1
#                 precio = float(item_data.get('precio'))
#                 coniva = 0
#                 totaliva = 0
#                 if item_data.get('iva') == 'Basico':
#                     coniva = precio * 1.22
#                     totaliva = precio * 0.22
#                 else:
#                     coniva = precio
#                     totaliva = 0
#
#                 if moneda == 2:  # dolar
#                     precio_c=precio*arbitraje
#                     iva_total_c = totaliva * arbitraje
#                     total_coniva_c = coniva * arbitraje
#                 elif moneda not in [1, 2]:
#                     aux = totaliva * paridad
#                     iva_total_c = aux * arbitraje
#                     aux1 = coniva * paridad
#                     total_coniva_c = aux1 * arbitraje
#                     aux2 = precio * paridad
#                     precio_c = aux2 * arbitraje
#                 else:
#                     iva_total_c = 0
#                     total_coniva_c = 0
#                     precio_c=0
#
#                 boleta = Boleta()
#                 numero = numero
#                 boleta.autogenerado = autogenerado
#                 boleta.tipo = tipo
#                 boleta.fecha = fecha
#                 boleta.vto = fecha
#                 boleta.tipofactura = serie
#                 boleta.serie = serie
#                 boleta.prefijo = prefijo
#                 boleta.numero = numero
#                 boleta.nrocliente = cliente.codigo
#                 boleta.cliente = cliente.empresa
#                 boleta.direccion = cliente.direccion
#                 boleta.direccion2 = cliente.direccion2
#                 boleta.localidad = cliente.localidad
#                 boleta.ciudad = cliente.ciudad
#                 boleta.pais = cliente.pais
#                 boleta.telefax = cliente.telefono
#                 boleta.ruc = cliente.ruc
#                 boleta.condiciones = 'S/I'
#                 boleta.corporativo = 'S/I'
#                 boleta.moneda = moneda
#                 boleta.cambio = arbitraje
#                 boleta.paridad = paridad
#                 boleta.tipocliente = 'RESPONSABLE INSCRIPTO'
#                 boleta.item = item_data.get('id')
#                 boleta.descripcion = item_data.get('descripcion')
#                 boleta.precio = item_data.get('precio')
#                 boleta.iva = item_data.get('iva')
#                 boleta.cuenta = item_data.get('cuenta')
#                 boleta.monto = item_data.get('precio')
#                 boleta.totiva = iva_total_c
#                 boleta.total = total_coniva_c
#                 boleta.master=master
#                 boleta.house=house
#                 boleta.posicion=posicion
#                 boleta.kilos=kilos
#                 boleta.bultos=bultos
#                 boleta.terminos=terminos
#                 boleta.pagoflete=pagoflete
#                 boleta.origen=origen
#                 boleta.destino=destino
#                 boleta.seguimiento=seguimiento
#                 boleta.save()
#
#                 asiento_vector = {
#                     'detalle': detalle_asiento,
#                     'monto': precio_c,
#                     'moneda': moneda,
#                     'cambio': arbitraje,
#                     'asiento': asiento,
#                     'conciliado': 'N',
#                     'clearing': fecha_obj,
#                     'fecha': fecha_obj,
#                     'imputacion': None,
#                     'tipo': tipo_asiento,
#                     'cuenta': item_data.get('cuenta'),
#                     'documento': str(numero),
#                     'vencimiento': fecha_obj,
#                     'pasado': 0,
#                     'autogenerado': autogenerado,
#                     'cliente': cliente.codigo,
#                     'banco': 'S/I',
#                     'centro': 'S/I',
#                     'mov': aux,
#                     'anio': fecha_obj.year,
#                     'mes': fecha_obj.month,
#                     'fechacheque': fecha_obj,
#                     'paridad': paridad
#                 }
#                 crear_asiento(asiento_vector)
#                 movimiento_num = aux
#
#             return JsonResponse({'status': 'Factura procesada correctamente N° ' + str(numero)})
#     except Exception as e:
#         return JsonResponse({'status': 'Error: ' + str(e)})



def generar_numero():
    # Obtener la fecha y hora actual
    ahora = datetime.now()

    # Tomar los dos últimos dígitos del año
    año = str(ahora.year)[-2:]

    # Mes, día, hora, minutos y segundos
    mes = f"{ahora.month:02}"
    dia = f"{ahora.day:02}"
    hora = f"{ahora.hour:02}"
    minutos = f"{ahora.minute:02}"
    segundos = f"{ahora.second:02}"

    # Concatenar para formar el número (ejemplo: 11051019041186)
    numero = f"{año}{mes}{dia}{hora}{minutos}{segundos}"

    return numero

def modificar_numero(numero):
    # Quitar el primer dígito y los últimos dos dígitos
    numero_modificado = numero[1:-2]
    return numero_modificado


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


def source_infofactura(request):
    try:
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))

        registros=VPreventas.objects.all()

        total_registros = len(registros)

        # Paginación
        registros_paginated = registros[start:start + length]

        # Construir los datos para la tabla
        data = [{
            'numero': item.znumero,
            'cliente': item.zconsignatario,
            'posicion': item.zposicion,
            'master': item.zmaster,
            'house': item.zhouse,
            'vapor_vuelo': item.zcarrier,
            'contenedor': (
                Envases.objects.filter(numero=item.zrefer).order_by('id').first().nrocontenedor
                if Envases.objects.filter(numero=item.zrefer).exists() else 0
            ),
            'clase': item.zclase,
            'referencia': item.zrefer,
            'fecha': item.zllegasale.strftime('%Y-%m-%d') if item.zllegasale else None,
        } for item in registros_paginated]

        # Respuesta JSON
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': total_registros,
            'recordsFiltered': total_registros,
            'data': data,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})


def source_infofactura_cliente(request):
    try:
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 5))
        cliente = str(request.GET.get('cliente'))

        registros = VPreventas.objects.filter(zcliente=cliente)

        total_registros = len(registros)

        # Paginación
        registros_paginated = registros[start:start + length]

        # Construir los datos para la tabla
        data = [{
            'numero': item.znumero,
            'cliente': item.zconsignatario,
            'posicion': item.zposicion,
            'master': item.zmaster,
            'house': item.zhouse,
            'vapor_vuelo': item.zcarrier,
            'contenedor': (
                Envases.objects.filter(numero=item.zrefer).order_by('id').first().nrocontenedor
                if Envases.objects.filter(numero=item.zrefer).exists() else 0
            ),
            'clase': item.zclase,
            'referencia': item.zrefer,
            'fecha': item.zllegasale.strftime('%Y-%m-%d') if item.zllegasale else None,
        } for item in registros_paginated]
        # Respuesta JSON
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': total_registros,
            'recordsFiltered': total_registros,
            'data': data,
        })


    except Exception as e:
        return JsonResponse({'error': str(e)})

def cargar_preventa_infofactura(request):
    if request.method == 'POST':
        clase = request.POST.get('clase')
        referencia = int(request.POST.get('referencia'))
        preventa = int(request.POST.get('preventa'))
        gastos_data_list = []
        total_sin_iva = Decimal('0.00')
        total_con_iva = Decimal('0.00')

        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))

        try:
            prev = VPreventas.objects.get(znumero=preventa)
            gastos = VistaGastosPreventa.objects.filter(numero=referencia)

            total_gastos = gastos.count()
            gastos_paginated = gastos[start:start + length]

            if total_gastos > 0:
                for gasto in gastos_paginated:
                    gasto_data = {
                        'descripcion': gasto.servicio,
                        'total': float(gasto.precio),
                        'iva': gasto.iva,
                        'original': float(gasto.pinformar),
                        'moneda': gasto.moneda,
                    }
                    total_sin_iva += gasto.precio
                    if gasto.iva == 'Basico':
                        total_con_iva += gasto.precio * Decimal('1.22')
                    else:
                        total_con_iva += gasto.precio

                    gastos_data_list.append(gasto_data)

            ref = prev.zrefer
            try:
                if clase == "IM":
                    embarque = Embarqueaereo.objects.get(numero=ref)
                    cliente = Clientes.objects.get(codigo=embarque.cliente)
                    moneda = Monedas.objects.get(codigo=embarque.moneda).nombre
                elif clase == "IA":
                    embarque = ImportEmbarqueaereo.objects.get(numero=ref)
                    cliente = Clientes.objects.get(codigo=embarque.cliente)
                    moneda = embarque.moneda
                elif clase == "EA":
                    embarque = ExportEmbarqueaereo.objects.get(numero=ref)
                    cliente = Clientes.objects.get(codigo=embarque.cliente)
                    moneda = embarque.moneda
                elif clase == "EM":
                    embarque = ExpmaritEmbarqueaereo.objects.get(numero=ref)
                    cliente = Clientes.objects.get(codigo=embarque.cliente)
                    moneda = embarque.moneda
                elif clase == "IT":
                    embarque = ImpterraEmbarqueaereo.objects.get(numero=ref)
                    cliente = Clientes.objects.get(codigo=embarque.cliente)
                    moneda = embarque.moneda
                elif clase == "ET":
                    embarque = ExpterraEmbarqueaereo.objects.get(numero=ref)
                    cliente = Clientes.objects.get(codigo=embarque.cliente)
                    moneda = embarque.moneda

            except Embarqueaereo.DoesNotExist:
                embarque=None
                moneda = None
                cliente = None

            llegada_salida = (
                prev.zllegasale.strftime('%Y-%m-%d') if prev.zllegasale else None
            )

            data_preventa = {
                'autogenerado':prev.znumero,
                'house':prev.zhouse,
                'master':prev.zmaster,
                'moneda': moneda if moneda else None,
                'total_con_iva': str(total_con_iva),
                'total_sin_iva': str(total_sin_iva),
                'cliente_i': cliente.empresa if cliente else None,
                'peso': prev.zkilos,
                'direccion': cliente.direccion if cliente else None,
                'localidad': cliente.localidad if cliente else None,
                'bultos': prev.zbultos,
                'volumen': prev.zvolumen,
                'commodity': prev.zcommodity,
                'inconterms': prev.zterminos,
                'flete': prev.zpagoflete,
                'deposito': "S/I",
                'wr': prev.zwr,
                'referencia': prev.zrefer,
                'llegada_salida': llegada_salida,
                'origen': prev.zorigen,
                'destino': prev.zdestino,
                'transportista': prev.zcarrier,
                'consignatario': prev.zconsignatario,
                'embarcador': prev.zembarcador,
                'agente': prev.zagente,
                'vuelo_vapor': prev.zcarrier,
                'seguimiento': prev.zseguimiento,
                'mawb_mbl_mcrt': prev.zmaster,
                'hawb_hbl_hcrt': prev.zhouse,
                'posicion': prev.zposicion,
                'status': 'PARA FACTURAR',
                'orden': "S/I",
                'modo': prev.ztransporte,
            }

            data = {
                "draw": int(request.GET.get('draw', 1)),
                "recordsTotal": total_gastos,
                "recordsFiltered": total_gastos,
                "data": gastos_data_list,
                "data_preventa": data_preventa,
            }

            return JsonResponse(data, safe=False)

        except VPreventas.DoesNotExist:
            return JsonResponse({'error': 'Infofactura no encontrada'}, safe=False)
        except Clientes.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, safe=False)

def cargar_preventa_infofactura_multiple(request):
    if request.method == 'POST':
        try:
            seleccionados = json.loads(request.POST.get('seleccionados', '[]'))

            resultado = []

            for item in seleccionados:
                preventa = item.get('numero')
                referencia = item.get('referencia')
                clase = item.get('clase')

                gastos_data_list = []
                total_sin_iva = Decimal('0.00')
                total_con_iva = Decimal('0.00')

                try:
                    prev = VPreventas.objects.get(znumero=preventa)
                    gastos = VistaGastosPreventa.objects.filter(numero=referencia)

                    llegada_salida = (
                        prev.zllegasale.strftime('%Y-%m-%d') if prev.zllegasale else None
                    )

                    total_gastos = gastos.count()

                    for gasto in gastos:
                        gasto_data = {
                            'descripcion': gasto.servicio,
                            'total': float(gasto.precio),
                            'iva': gasto.iva,
                            'original': float(gasto.pinformar),
                            'moneda': gasto.moneda,
                        }
                        total_sin_iva += gasto.precio
                        if gasto.iva == 'Basico':
                            total_con_iva += gasto.precio * Decimal('1.22')
                        else:
                            total_con_iva += gasto.precio

                        gastos_data_list.append(gasto_data)

                    ref = prev.zrefer

                    if clase == "IM":
                        embarque = Embarqueaereo.objects.get(numero=ref)
                        cliente = Clientes.objects.get(codigo=embarque.cliente)
                        moneda = Monedas.objects.get(codigo=embarque.moneda).nombre
                    elif clase == "IA":
                        embarque = ImportEmbarqueaereo.objects.get(numero=ref)
                        cliente = Clientes.objects.get(codigo=embarque.cliente)
                        moneda = embarque.moneda
                    elif clase == "EA":
                        embarque = ExportEmbarqueaereo.objects.get(numero=ref)
                        cliente = Clientes.objects.get(codigo=embarque.cliente)
                        moneda = embarque.moneda
                    elif clase == "EM":
                        embarque = ExpmaritEmbarqueaereo.objects.get(numero=ref)
                        cliente = Clientes.objects.get(codigo=embarque.cliente)
                        moneda = embarque.moneda
                    elif clase == "IT":
                        embarque = ImpterraEmbarqueaereo.objects.get(numero=ref)
                        cliente = Clientes.objects.get(codigo=embarque.cliente)
                        moneda = embarque.moneda
                    elif clase == "ET":
                        embarque = ExpterraEmbarqueaereo.objects.get(numero=ref)
                        cliente = Clientes.objects.get(codigo=embarque.cliente)
                        moneda = embarque.moneda


                    data_preventa_old = {
                        'autogenerado': prev.autogenerado,
                        'house': prev.house,
                        'master': prev.master,
                        'moneda': moneda,
                        'total_con_iva': str(total_con_iva),
                        'total_sin_iva': str(total_sin_iva),
                        'cliente_i': cliente.empresa,
                        'peso': prev.kilos,
                        'direccion': cliente.direccion,
                        'localidad': cliente.localidad,
                        'aplic': Cargaaerea.objects.filter(numero=ref).values('aplicable').first().get('aplicable', 'S/I') if clase == "IA" else 'S/I',
                        'bultos': prev.bultos,
                        'volumen': prev.volumen,
                        'commodity': prev.commodity,
                        'inconterms': prev.terminos,
                        'flete': prev.pagoflete,
                        'deposito': "S/I",
                        'wr': prev.wr,
                        'referencia': prev.referencia,
                        'llegada_salida': embarque.fecharetiro,
                        'origen': prev.destino,
                        'destino': prev.origen,
                        'transportista': prev.transportista,
                        'consignatario': prev.consigna,
                        'embarcador': prev.embarca,
                        'agente': prev.agente,
                        'vuelo_vapor': prev.vuelo,
                        'seguimiento': prev.seguimiento,
                        'mawb_mbl_mcrt': prev.master,
                        'hawb_hbl_hcrt': prev.house,
                        'posicion': prev.posicion,
                        'status': 'PARA FACTURAR',
                        'orden': "S/I",
                        'modo': 'MARITIMO',
                    }
                    data_preventa = {
                        'autogenerado': prev.znumero,
                        'house': prev.zhouse,
                        'master': prev.zmaster,
                        'moneda': moneda if moneda else None,
                        'total_con_iva': str(total_con_iva),
                        'total_sin_iva': str(total_sin_iva),
                        'cliente_i': cliente.empresa if cliente else None,
                        'peso': prev.zkilos,
                        'direccion': cliente.direccion if cliente else None,
                        'localidad': cliente.localidad if cliente else None,
                        # 'aplic': 0 if int(ref)<0 else Cargaaerea.objects.filter(numero=ref).values('aplicable').first().get('aplicable','S/I') if clase == "IA" else 'S/I',
                        'bultos': prev.zbultos,
                        'volumen': prev.zvolumen,
                        'commodity': prev.zcommodity,
                        'inconterms': prev.zterminos,
                        'flete': prev.zpagoflete,
                        'deposito': "S/I",
                        'wr': prev.zwr,
                        'referencia': prev.zrefer,
                        'llegada_salida': llegada_salida,
                        'origen': prev.zorigen,
                        'destino': prev.zdestino,
                        'transportista': prev.zcarrier,
                        'consignatario': prev.zconsignatario,
                        'embarcador': prev.zembarcador,
                        'agente': prev.zagente,
                        'vuelo_vapor': prev.zcarrier,
                        'seguimiento': prev.zseguimiento,
                        'mawb_mbl_mcrt': prev.zmaster,
                        'hawb_hbl_hcrt': prev.zhouse,
                        'posicion': prev.zposicion,
                        'status': 'PARA FACTURAR',
                        'orden': "S/I",
                        'modo': prev.ztransporte,
                    }

                    resultado.append({
                        "numero": preventa,
                        "referencia": referencia,
                        "clase": clase,
                        "gastos": gastos_data_list,
                        "data_preventa": data_preventa
                    })

                except Infofactura.DoesNotExist:
                    resultado.append({'error': f'Infofactura con número {preventa} no encontrada'})
                except Embarqueaereo.DoesNotExist:
                    resultado.append({'error': f'Embarque con referencia {referencia} no encontrado'})
                except Clientes.DoesNotExist:
                    resultado.append({'error': f'Cliente relacionado con referencia {referencia} no encontrado'})

            return JsonResponse({"data": resultado}, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al procesar los datos enviados'}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, safe=False)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


def guardar_arbitraje(request):
    if request.method == "POST":
        try:
            # Obtener datos del POST
            arb_dolar = request.POST.get('arbDolar', '0')
            par_dolar = request.POST.get('parDolar', '0')
            tipo_moneda = request.POST.get('tipoMoneda', '0')
            piz_dolar = request.POST.get('pizDolar', '0')
            fecha_cliente = request.POST.get('fecha', '')

            # Validar y formatear la fecha
            if fecha_cliente:
                fecha_cliente = datetime.strptime(fecha_cliente, '%Y-%m-%d')  # Convertir a datetime
            else:
                fecha_cliente = datetime.today()

            # Formatear la fecha con la hora actual
            fecha_final = fecha_cliente.replace(
                hour=datetime.now().hour,
                minute=datetime.now().minute,
                second=datetime.now().second,
                microsecond=datetime.now().microsecond
            )

            # Comprobar si ya existe un registro para la fecha
            registro_existente = Dolar.objects.filter(
                ufecha__date=fecha_final.date()
            ).first()

            if registro_existente:
                # Modificar el registro existente
                registro_existente.upizarra = float(piz_dolar)
                registro_existente.paridad = float(par_dolar)
                registro_existente.uvalor = float(arb_dolar)
                registro_existente.umoneda = float(tipo_moneda)
                registro_existente.ufecha = fecha_final
                registro_existente.save()
            else:
                # Crear un nuevo registro
                dolar = Dolar()
                dolar.upizarra = float(piz_dolar)
                dolar.paridad = float(par_dolar)
                dolar.uvalor = float(arb_dolar)
                dolar.umoneda = float(tipo_moneda)
                dolar.ufecha = fecha_final
                dolar.save()

            return JsonResponse({'status': 'Registro guardado correctamente.'})

        except Exception as e:
            return JsonResponse({'status': f'Error al guardar los datos: {str(e)}'}, status=500)

    else:
        return JsonResponse({'status': 'Método no permitido.'}, status=405)

"""
data_preventa = {
                'autogenerado':prev.autogenerado,
                'house':prev.house,
                'master':prev.master,
                'moneda': moneda if moneda else None,
                'total_con_iva': str(total_con_iva),
                'total_sin_iva': str(total_sin_iva),
                'cliente_i': cliente.empresa if cliente else None,
                'peso': prev.kilos,
                'direccion': cliente.direccion if cliente else None,
                'localidad': cliente.localidad if cliente else None,
                #'aplic': 0 if int(ref)<0 else Cargaaerea.objects.filter(numero=ref).values('aplicable').first().get('aplicable','S/I') if clase == "IA" else 'S/I',
                'bultos': prev.bultos,
                'volumen': prev.volumen,
                'commodity': prev.commodity,
                'inconterms': prev.terminos,
                'flete': prev.pagoflete,
                'deposito': "S/I",
                'wr': prev.wr,
                'referencia': prev.referencia,
                'llegada_salida': llegada_salida,
                'origen': prev.destino,
                'destino': prev.origen,
                'transportista': prev.transportista,
                'consignatario': prev.consigna,
                'embarcador': prev.embarca,
                'agente': prev.agente,
                'vuelo_vapor': prev.vuelo,
                'seguimiento': prev.seguimiento,
                'mawb_mbl_mcrt': prev.master,
                'hawb_hbl_hcrt': prev.house,
                'posicion': prev.posicion,
                'status': 'PARA FACTURAR',
                'orden': "S/I",
                'modo': 'MARITIMO',
            }

data = {
                "draw": int(request.GET.get('draw', 1)),
                "recordsTotal": total_gastos,
                "recordsFiltered": total_gastos,
                "data": gastos_data_list,
                "data_preventa": data_preventa,
            }
"""



