import json

import simplejson
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse

from mantenimientos.models import Vapores
from seguimientos.models import Conexaerea, VGrillaSeguimientos, Seguimiento

""" TABLA PUERTO """
columns_table = {
    1: 'origen',
    2: 'destino',
    3: 'vapor',
    4: 'salida',
    5: 'llegada',
    6: 'viaje',
    7: 'cia',
    8: 'modo',
    9: 'accion',
}


def source_rutas(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        """PROCESO FILTRO Y ORDEN BY"""
        start = int(request.GET['start'])
        numero = request.GET['numero']
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        registros = Conexaerea.objects.filter(numero=numero).order_by(*order)

        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data

        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Conexaerea.objects.filter(numero=numero).count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def get_data(registros_filtrados):
    try:

        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.origen is None else str(registro.origen))
            registro_json.append('' if registro.destino is None else str(registro.destino))
            registro_json.append('' if registro.vapor is None else str(registro.vapor))
            registro_json.append('' if registro.salida is None else str(registro.salida)[:10])
            registro_json.append('' if registro.llegada is None else str(registro.llegada)[:10])
            registro_json.append('' if registro.viaje is None else str(registro.viaje))
            registro_json.append('' if registro.cia is None else str(registro.cia))
            registro_json.append('' if registro.modo is None else str(registro.modo))
            registro_json.append('' if registro.accion is None else str(registro.accion))
            data.append(registro_json)
        return data
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

def is_ajax(request):
    try:
        req = request.META.get('HTTP_X_REQUESTED_WITH')
        # return req == 'XMLHttpRequest'
        return True
    except Exception as e:
        messages.error(request,e)


def guardar_ruta(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        data = simplejson.loads(request.POST['data'])
        if len(data[0]['value']) > 0:
            registro = Conexaerea.objects.get(id=data[0]['value'])
        else:
            registro = Conexaerea()
        campos = vars(registro)
        for x in data:
            k = x['name']
            v = x['value']
            for name in campos:
                if name == k:
                    if v is not None and len(v) > 0:
                        if v is not None:
                            setattr(registro, name, v)
                        else:
                            if len(v) > 0:
                                setattr(registro, name, v)
                    else:
                        setattr(registro, name, None)
                    continue
        registro.numero = numero
        registro.save()
        resultado['resultado'] = 'exito'
        resultado['numero'] = str(registro.numero)
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def eliminar_ruta(request):
    resultado = {}
    try:
        id = request.POST['id']
        Conexaerea.objects.get(id=id).delete()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def datos_seguimiento(request):
    resultado = {}
    try:
        numero = request.POST.get('numero')  # Evita errores si el número no está en la petición
        seguimiento = Seguimiento.objects.get(numero=numero)
        transportista = VGrillaSeguimientos.objects.get(numero=numero).transportista
        if str(seguimiento.vapor).isdigit():
            vapor = Vapores.objects.get(codigo=seguimiento.vapor).nombre
        else:
            vapor = seguimiento.vapor

        data = {
            'salida': seguimiento.etd.strftime('%Y-%m-%d') if seguimiento.etd else None,
            'llegada': seguimiento.eta.strftime('%Y-%m-%d') if seguimiento.eta else None,
            'origen': seguimiento.origen if seguimiento.origen else None,
            'destino': seguimiento.destino if seguimiento.destino else None,
            'cia': transportista if transportista else None,
            'modo': seguimiento.modo if seguimiento.modo else None,
            'viaje': seguimiento.viaje if seguimiento.viaje else None,
            'vapor': vapor
        }

        resultado['datos'] = data
        resultado['resultado'] = 'exito'

    except Seguimiento.DoesNotExist:
        resultado['resultado'] = 'No se encontró el seguimiento con ese número.'
    except Exception as e:
        resultado['resultado'] = str(e)

    return JsonResponse(resultado)
