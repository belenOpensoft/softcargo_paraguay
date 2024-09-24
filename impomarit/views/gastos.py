import json

import simplejson
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from seguimientos.models import VGrillaServiceaereo as Serviceaereo,Serviceaereo as ServiceaereoReal
from impomarit.models import Servireserva, VGastosMaster
import json

""" TABLA PUERTO """
columns_table = {
    1: 'servicio',
    2: 'moneda',
    3: 'precio',
    4: 'costo',
    5: 'detalle',
    6: 'modo',
    7: 'tipogasto',
    8: 'arbitraje',
    9: 'notomaprofit',
    10: 'secomparte',
    11: 'pinformar',
    12: 'socio',
    13: 'notas',
}
def source_gastos(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        """PROCESO FILTRO Y ORDEN BY"""
        start = int(request.GET['start'])
        numero = request.GET['numero']
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        registros = VGastosMaster.objects.filter(numero=numero).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = VGastosMaster.objects.filter(numero=numero).count()
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
            registro_json.append('' if registro.servicio is None else str(registro.servicio))
            registro_json.append('' if registro.moneda is None else str(registro.moneda))
            registro_json.append('' if registro.precio is None else str(registro.precio))
            registro_json.append('' if registro.costo is None else str(registro.costo))
            registro_json.append('' if registro.detalle is None else str(registro.detalle))
            registro_json.append('' if registro.modo is None else str(registro.modo))
            registro_json.append('' if registro.tipogasto is None else str(registro.tipogasto))
            registro_json.append('' if registro.arbitraje is None else str(registro.arbitraje))
            registro_json.append('' if registro.notomaprofit is None else str(registro.notomaprofit))
            registro_json.append('' if registro.secomparte is None else str(registro.secomparte))
            registro_json.append('' if registro.pinformar is None else str(registro.pinformar))
            registro_json.append('' if registro.socio is None else str(registro.socio))
            registro_json.append('' if registro.notas is None else str(registro.notas))
            registro_json.append('' if registro.id_servicio is None else str(registro.id_servicio))
            registro_json.append('' if registro.id_moneda is None else str(registro.id_moneda))
            registro_json.append('' if registro.id_socio is None else str(registro.id_socio))
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

def add_gasto_master_o(request):
    resultado = {}
    try:
        # Recibir los datos JSON enviados por AJAX
        data = json.loads(request.POST.get('data'))

        # Crear un diccionario para acceder fácilmente a los valores
        form_data = {item['name']: item['value'] for item in data}

        # Acceder a los valores del formulario usando el diccionario
        numero = form_data.get('numero')
        servicio = form_data.get('servicio')
        secomparte = form_data.get('secomparte')
        moneda = form_data.get('moneda')
        costo = form_data.get('costo')
        arbitraje = form_data.get('arbitraje', 0)  # valor opcional
        tipogasto = form_data.get('tipogasto')
        pinformar = form_data.get('pinformar', 0)  # valor opcional
        notomaprofit = form_data.get('notomaprofit') == 'on'
        modo = form_data.get('modo')
        socio = form_data.get('socio')
        detalle = form_data.get('detalle')
        prorrateo = form_data.get('prorrateo')
        empresa = form_data.get('empresa')
        reembolsable = form_data.get('reembolsable')


        # Crear un nuevo registro sin intentar actualizar
        registro = Servireserva(
            numero=numero,
            servicio=servicio,
            secomparte=secomparte,
            moneda=moneda,
            costo=costo if costo else 0,
            arbitraje=arbitraje,
            tipogasto=tipogasto,
            pinformar=pinformar,
            notomaprofit=notomaprofit,
            modo=modo,
            socio=socio,
            detalle=detalle,
            prorrateo=prorrateo,
            empresa=empresa,
            reembolsable=reembolsable
        )

        # Guardar el nuevo registro en la base de datos
        registro.save()

        # Devolver el resultado de éxito
        resultado['resultado'] = 'exito'
        resultado['numero'] = registro.numero

    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)

    # Retornar el resultado en formato JSON
    return JsonResponse(resultado)


def add_gasto_master(request):
    resultado = {}
    try:
        # Recibir los datos JSON enviados por AJAX
        data = json.loads(request.POST.get('data'))

        # Crear un diccionario para acceder fácilmente a los valores
        form_data = {item['name']: item['value'] for item in data}

        # Acceder a los valores del formulario usando el diccionario
        numero = form_data.get('numero')
        servicio = form_data.get('servicio')
        secomparte = form_data.get('secomparte')
        moneda = form_data.get('moneda')
        costo = form_data.get('costo')
        arbitraje = form_data.get('arbitraje', 0)  # valor opcional
        tipogasto = form_data.get('tipogasto')
        pinformar = form_data.get('pinformar', 0)  # valor opcional
        notomaprofit = form_data.get('notomaprofit') == 'on'
        modo = form_data.get('modo')
        socio = form_data.get('socio')
        detalle = form_data.get('detalle')
        prorrateo = form_data.get('prorrateo')
        empresa = form_data.get('empresa')
        reembolsable = form_data.get('reembolsable')

        # Verificar si el registro ya existe
        if 'id_gasto_id' in form_data and form_data['id_gasto_id']:
            # Modificar el registro existente
            registro = Servireserva.objects.get(id=form_data['id_gasto_id'])
        else:
            # Crear un nuevo registro si no existe
            registro = Servireserva()

        # Actualizar o crear el registro con los datos del formulario
        registro.numero = numero
        registro.servicio = servicio
        registro.secomparte = secomparte
        registro.moneda = moneda
        registro.costo = costo if costo else 0
        registro.arbitraje = arbitraje
        registro.tipogasto = tipogasto
        registro.pinformar = pinformar
        registro.notomaprofit = notomaprofit
        registro.modo = modo
        registro.socio = socio
        registro.detalle = detalle
        registro.prorrateo = prorrateo
        registro.empresa = empresa
        registro.reembolsable = reembolsable

        # Guardar el registro en la base de datos
        registro.save()

        # Devolver el resultado de éxito
        resultado['resultado'] = 'exito'
        resultado['numero'] = registro.numero

    except Servireserva.DoesNotExist:
        resultado['resultado'] = 'Registro no encontrado.'
    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)

    # Retornar el resultado en formato JSON
    return JsonResponse(resultado)


def eliminar_gasto_master(request):
    resultado = {}
    try:
        id = request.POST['id']
        Servireserva.objects.get(id=id).delete()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)
