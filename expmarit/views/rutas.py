import json
from datetime import datetime

import simplejson
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from expmarit.models import ExpmaritConexaerea, ExpmaritEmbarqueaereo, VEmbarqueaereo
from mantenimientos.models import Vapores
from seguimientos.models import Seguimiento, Conexaerea
from django.db import transaction


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
        registros = ExpmaritConexaerea.objects.filter(numero=numero).order_by(*order)

        resultado = {}
        data = get_data(registros[start:end])
        resultado['data'] = data

        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = ExpmaritConexaerea.objects.filter(numero=numero).count()
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


def guardar_ruta_old(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        data = simplejson.loads(request.POST['data'])
        if len(data[0]['value']) > 0:
            registro = ExpmaritConexaerea.objects.get(id=data[0]['value'])
        else:
            registro = ExpmaritConexaerea()
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
        eta = next(item['value'] for item in data if item['name'] == 'llegada')
        etd = next(item['value'] for item in data if item['name'] == 'salida')
        vapor = next(item['value'] for item in data if item['name'] == 'vapor')
        viaje = next(item['value'] for item in data if item['name'] == 'viaje')

        actualizar_fechas(etd, eta, numero, viaje,vapor)

    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def actualizar_fechas_old(etd, eta, numero,viaje,vapor):
    try:
        etd = datetime.strptime(etd, "%Y-%m-%d")
        eta = datetime.strptime(eta, "%Y-%m-%d")
        resultado = {}
        num=ExpmaritEmbarqueaereo.objects.get(numero=numero).seguimiento
        seg=Seguimiento.objects.get(numero=num)
        if seg is not None:
            if etd is not None:
                seg.etd=etd
            if eta is not None:
                seg.eta=eta
            if viaje is not None:
                seg.viaje=viaje
            if vapor is not None:
                seg.vapor=vapor
            seg.save()
    except Exception as e:
        resultado['resultado'] = f'Ocurrió un error: {str(e)}'
    return JsonResponse(resultado)

def guardar_ruta(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        data = simplejson.loads(request.POST['data'])

        if len(data[0]['value']) > 0:
            registro = ExpmaritConexaerea.objects.get(id=data[0]['value'])
            salida_original = registro.salida
            llegada_original = registro.llegada
            editando = True
        else:
            registro = ExpmaritConexaerea()
            salida_original = None
            llegada_original = None
            editando = False

        campos = vars(registro)
        for x in data:
            k = x['name']
            v = x['value']
            for name in campos:
                if name == k:
                    setattr(registro, name, v if v else None)
                    break

        registro.numero = numero
        registro.save()

        resultado['numero'] = str(registro.numero)

        if editando:
            eta = next(item['value'] for item in data if item['name'] == 'llegada')
            etd = next(item['value'] for item in data if item['name'] == 'salida')
            vapor = next(item['value'] for item in data if item['name'] == 'vapor')
            viaje = next(item['value'] for item in data if item['name'] == 'viaje')

            r = actualizar_fechas(etd, eta, numero, viaje, vapor, salida_original, llegada_original)

            if r.get('resultado') != 'ok':
                resultado['resultado'] = r
            else:
                resultado['resultado'] = 'exito'
        else:
            resultado['resultado'] = 'exito'

    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)

    return JsonResponse(resultado)

def actualizar_fechas_2(etd, eta, numero, viaje, vapor, salida_original, llegada_original):
    resultado = {}

    try:
        embarque = ExpmaritEmbarqueaereo.objects.get(numero=numero)
        awb = embarque.awb

        # Actualizar seguimiento del embarque actual
        seguimiento = Seguimiento.objects.get(numero=embarque.seguimiento)
        if etd:
            seguimiento.etd = etd
        if eta:
            seguimiento.eta = eta
        if viaje:
            seguimiento.viaje = viaje
        if vapor:
            seguimiento.vapor = vapor
        seguimiento.save()

        # Buscar otros embarques con el mismo AWB
        embarques_iguales = ExpmaritEmbarqueaereo.objects.filter(awb=awb).exclude(numero=numero)

        for e in embarques_iguales:
            rutas = ExpmaritConexaerea.objects.filter(numero=e.numero)
            for ruta in rutas:
                if ruta.salida == salida_original and ruta.llegada == llegada_original:
                    if etd:
                        ruta.salida = etd
                    if eta:
                        ruta.llegada = eta
                    ruta.save()

                    try:
                        seg = Seguimiento.objects.get(numero=e.seguimiento)
                        if etd:
                            seg.etd = etd
                        if eta:
                            seg.eta = eta
                        seg.save()
                    except Seguimiento.DoesNotExist:
                        continue
                    break  # solo actualizamos una ruta coincidente por embarque

        resultado['resultado'] = 'ok'

    except Exception as e:
        resultado['resultado'] = f'Ocurrió un error: {str(e)}'

    return resultado


def actualizar_fechas(etd, eta, numero, viaje, vapor, salida_original, llegada_original):
    resultado = {}

    try:
        with transaction.atomic():
            embarque = ExpmaritEmbarqueaereo.objects.get(numero=numero)
            awb = embarque.awb

            # Actualizar seguimiento del embarque actual
            seguimiento = Seguimiento.objects.get(numero=embarque.seguimiento)
            if etd:
                seguimiento.etd = etd
            if eta:
                seguimiento.eta = eta
            if viaje:
                seguimiento.viaje = viaje
            if vapor:
                seguimiento.vapor = vapor
            seguimiento.save()

            # Actualizar la ruta del seguimiento actual si coincide
            try:
                ruta_actual = Conexaerea.objects.get(
                    numero=seguimiento.numero,
                    salida=salida_original,
                    llegada=llegada_original
                )
                if etd:
                    ruta_actual.salida = etd
                if eta:
                    ruta_actual.llegada = eta
                ruta_actual.save()
            except Conexaerea.DoesNotExist:
                pass

            # Buscar y actualizar otros embarques con el mismo AWB
            embarques_iguales = ExpmaritEmbarqueaereo.objects.filter(awb=awb).exclude(numero=numero)

            for e in embarques_iguales:
                rutas = ExpmaritConexaerea.objects.filter(numero=e.numero)
                for ruta in rutas:
                    if ruta.salida == salida_original and ruta.llegada == llegada_original:
                        if etd:
                            ruta.salida = etd
                        if eta:
                            ruta.llegada = eta
                        ruta.save()

                        try:
                            seg = Seguimiento.objects.get(numero=e.seguimiento)
                            if etd:
                                seg.etd = etd
                            if eta:
                                seg.eta = eta
                            seg.save()

                            # También actualizar ruta del seguimiento si coincide
                            ruta_seg = Conexaerea.objects.filter(
                                numero=seg.numero,
                                salida=salida_original,
                                llegada=llegada_original
                            ).first()
                            if ruta_seg:
                                if etd:
                                    ruta_seg.salida = etd
                                if eta:
                                    ruta_seg.llegada = eta
                                ruta_seg.save()

                        except Seguimiento.DoesNotExist:
                            continue
                        except Conexaerea.DoesNotExist:
                            continue
                        break  # solo una ruta por embarque

        resultado['resultado'] = 'ok'

    except Exception as e:
        resultado['resultado'] = f'Ocurrió un error: {str(e)}'

    return resultado


def add_ruta_importado(request):
    resultado = {}
    try:
        # Recibir el número desde el POST o desde los datos JSON
        data = json.loads(request.body)  # Carga los datos del cuerpo de la solicitud como JSON

        if isinstance(data, list):
            for envase_data in data:
                # Crear el registro del modelo Envases
                registro = ExpmaritConexaerea()

                # Obtener los campos disponibles del modelo
                campos = [f.name for f in ExpmaritConexaerea._meta.fields]

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
        ExpmaritConexaerea.objects.get(id=id).delete()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def datos_embarque_ruta(request):
    resultado = {}
    try:
        numero = request.POST.get('numero')
        embarque = ExpmaritEmbarqueaereo.objects.get(numero=numero)
        transportista = VEmbarqueaereo.objects.get(numero=numero).transportista
        if str(embarque.vapor).isdigit():
            vapor = Vapores.objects.get(codigo=embarque.vapor).nombre
        else:
            vapor = embarque.vapor
        data = {
            'salida': embarque.fechaembarque.strftime('%Y-%m-%d') if embarque.fechaembarque else None,
            'llegada': embarque.fecharetiro.strftime('%Y-%m-%d') if embarque.fecharetiro else None,
            'origen': embarque.origen if embarque.origen else None,
            'destino': embarque.destino if embarque.destino else None,
            'cia': transportista if transportista else None,
            'codigo_cia': embarque.transportista if embarque.transportista else None,
            'modo': 'MARITIMO',
            'viaje': embarque.viaje if embarque.viaje else None,
            'vapor': vapor
        }

        resultado['datos'] = data
        resultado['resultado'] = 'exito'

    except ExpmaritEmbarqueaereo.DoesNotExist:
        resultado['resultado'] = 'No se encontró el seguimiento con ese número.'
    except Exception as e:
        resultado['resultado'] = str(e)

    return JsonResponse(resultado)