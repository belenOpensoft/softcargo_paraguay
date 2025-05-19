import json
import simplejson
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from expmarit.models import ExpmaritCargaaerea
from mantenimientos.models import Productos

""" TABLA PUERTO """
columns_table = {
    1: 'id',
    2: 'producto',
    3: 'bultos',
    4: 'tipo',
    5: 'bruto',
    6: 'medidas',
    7: 'cbm',
    8: 'mercaderia',
    9: 'materialreceipt',
}

def source_embarques(request):
    if is_ajax(request):
        start = int(request.GET['start'])
        numero = request.GET['numero']
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        registros = ExpmaritCargaaerea.objects.filter(numero=numero).order_by(*order)

        resultado = {}
        data = get_data(registros[start:end])
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = ExpmaritCargaaerea.objects.filter(numero=numero).count()
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
            registro_json.append('' if registro.producto is None else str(registro.producto))
            registro_json.append('' if registro.bultos is None else str(registro.bultos))
            registro_json.append('' if registro.tipo is None else str(registro.tipo))
            registro_json.append('' if registro.bruto is None else str(registro.bruto))
            registro_json.append('' if registro.medidas is None else str(registro.medidas))
            registro_json.append('' if registro.cbm is None else str(registro.cbm))
            registro_json.append('' if registro.mercaderia is None else str(registro.mercaderia))
            registro_json.append('' if registro.producto is None else str(registro.producto.codigo))
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


@login_required(login_url='/login/')
def guardar_embarques(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        data = simplejson.loads(request.POST['data'])

        # Verificar si el registro ya existe, utilizando el identificador si está presente
        if 'id_embarque' in data and data['id_embarque']:
            # Modificar el registro existente
            try:
                registro = ExpmaritCargaaerea.objects.get(id=data['id_embarque'])
            except ExpmaritCargaaerea.DoesNotExist:
                resultado['resultado'] = 'El embarque no existe.'
                data_json = json.dumps(resultado)
                mimetype = "application/json"
                return HttpResponse(data_json, mimetype)
        else:
            # Crear un nuevo registro si no existe
            registro = ExpmaritCargaaerea()

        campos = vars(registro)

        for x in data:
            k = x['name']
            v = x['value']

            # Procesar el campo 'producto' de manera especial
            if k == 'cod_producto' and v:
                try:
                    # Buscar el producto en la base de datos usando el valor proporcionado (código del producto)
                    producto = Productos.objects.get(codigo=v)
                    setattr(registro, 'producto', producto)  # Asignar la instancia del producto
                except Productos.DoesNotExist:
                    resultado['resultado'] = 'El producto con ese código no existe.'
                    data_json = json.dumps(resultado)
                    mimetype = "application/json"
                    return HttpResponse(data_json, mimetype)
                continue  # Saltar al siguiente campo, ya que hemos manejado 'producto'

            # Para otros campos, continuar con el proceso habitual
            for name in campos:
                if name == k:
                    if v is not None and len(v) > 0:
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

def add_embarque_importado(request):
    resultado = {}
    try:
        # Recibir el número desde el POST o desde los datos JSON
        data = json.loads(request.body)  # Carga los datos del cuerpo de la solicitud como JSON

        if isinstance(data, list):
            for envase_data in data:
                # Crear el registro del modelo Cargaaerea
                registro = ExpmaritCargaaerea()

                # Obtener los campos disponibles del modelo
                campos = [f.name for f in ExpmaritCargaaerea._meta.fields]

                # Iterar sobre el diccionario y asignar los valores al modelo
                for nombre_campo, valor_campo in envase_data.items():
                    if nombre_campo == 'producto' and valor_campo:
                        # Procesar el campo 'producto' de manera especial
                        try:
                            # Buscar el producto en la base de datos usando el valor proporcionado (código del producto)
                            producto = Productos.objects.get(codigo=valor_campo)
                            setattr(registro, 'producto', producto)  # Asignar la instancia del producto
                        except Productos.DoesNotExist:
                            resultado['resultado'] = f'El producto con el código {valor_campo} no existe.'
                            return JsonResponse(resultado)
                        continue  # Saltar al siguiente campo, ya que hemos manejado 'producto'

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

def redondear_a_05_o_0(numero):
    # Redondea el número a 1 decimal
    numero_redondeado = round(numero, 1)

    # Calcula la parte decimal
    parte_decimal = numero_redondeado - int(numero_redondeado)

    # Redondea al valor más cercano a 0.5 o 0
    if parte_decimal < 0.25:
        return int(numero_redondeado)
    elif parte_decimal < 0.75:
        return int(numero_redondeado) + 0.5
    else:
        return int(numero_redondeado) + 1

# def actualizo_datos_embarque(request):
#     resultado = {}
#     try:
#         numero = request.POST['numero']
#         data = simplejson.loads(request.POST['data'])
#         seg = Seguimiento.objects.get(numero=numero)
#         seg.volumen = data[0]['value']
#         seg.muestroflete = data[2]['value']
#         seg.aplicable = data[4]['value']
#         seg.tomopeso = data[1]['value']
#         seg.tarifaprofit = data[8]['value']
#         seg.tarifacompra = data[5]['value']
#         # seg.numero = data_extra[7]['value']
#         seg.tarifaventa = data[3]['value']
#         seg.save()
#         resultado['resultado'] = 'exito'
#         resultado['numero'] = str(numero)
#     except IntegrityError as e:
#         resultado['resultado'] = 'Error de integridad, intente nuevamente.'
#     except Exception as e:
#         resultado['resultado'] = str(e)
#     data_json = json.dumps(resultado)
#     mimetype = "application/json"
#     return HttpResponse(data_json, mimetype)
def get_sugerencias_envases(request, numero):
    try:
        carga = ExpmaritCargaaerea.objects.filter(numero=numero).first()

        data = {
            'bultos': carga.bultos,
            'bruto': carga.bruto,
            'nrocontenedor': carga.nrocontenedor,
            'cbm': carga.cbm
        }

        return JsonResponse({'status': 'success', 'data': data})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
def eliminar_embarque(request):
    resultado = {}
    try:
        id = request.POST['id']
        ExpmaritCargaaerea.objects.get(id=id).delete()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)