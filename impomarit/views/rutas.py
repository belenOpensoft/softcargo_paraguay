import json
from datetime import datetime

import simplejson
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from impomarit.models import Conexaerea, Embarqueaereo
from seguimientos.models import Seguimiento

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
}


def source_rutas_house(request):
    if is_ajax(request):
        start = int(request.GET['start'])
        numero = request.GET['numero']
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        registros = Conexaerea.objects.filter(numero=numero).order_by(*order)

        resultado = {}
        data = get_data(registros[start:end])
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

        eta = next(item['value'] for item in data if item['name'] == 'llegada')
        etd = next(item['value'] for item in data if item['name'] == 'salida')

        actualizar_fechas(etd,eta,numero)

        resultado['resultado'] = 'exito'
        resultado['numero'] = str(registro.numero)
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def actualizar_fechas(etd, eta, numero):
    try:
        etd = datetime.strptime(etd, "%Y-%m-%d")
        eta = datetime.strptime(eta, "%Y-%m-%d")
        resultado = {}
        num=Embarqueaereo.objects.get(numero=numero).seguimiento
        seg=Seguimiento.objects.get(numero=num)
        seg.etd=etd
        seg.eta=eta
        seg.save()
    except Exception as e:
        resultado['resultado'] = f'Ocurrió un error: {str(e)}'
    return JsonResponse(resultado)

def add_ruta_importado(request):
    resultado = {}
    try:
        # Recibir el número desde el POST o desde los datos JSON
        data = json.loads(request.body)  # Carga los datos del cuerpo de la solicitud como JSON

        if isinstance(data, list):
            for envase_data in data:
                # Crear el registro del modelo Envases
                registro = Conexaerea()

                # Obtener los campos disponibles del modelo
                campos = [f.name for f in Conexaerea._meta.fields]

                # Iterar sobre el diccionario y asignar los valores al modelo
                for nombre_campo, valor_campo in envase_data.items():
                    if nombre_campo in campos:  # Verificar si el campo existe en el modelo
                        if valor_campo is not None and len(str(valor_campo)) > 0:
                            setattr(registro, nombre_campo, valor_campo)
                        else:
                            setattr(registro, nombre_campo, None)

                # Guardar el registro en la base de datos
                registro.save()

            # Retornar el resultado de éxito
            resultado['resultado'] = 'exito'
        else:
            resultado['resultado'] = 'Los datos enviados no son una lista válida.'

    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = f'Ocurrió un error: {str(e)}'

    # Devolver el resultado en formato JSON
    return JsonResponse(resultado)


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


