import json

import simplejson
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from seguimientos.models import VGrillaServiceaereo as Serviceaereo,Serviceaereo as ServiceaereoReal

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
        registros = Serviceaereo.objects.filter(numero=numero).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Serviceaereo.objects.filter(numero=numero).count()
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



def guardar_gasto(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        data = simplejson.loads(request.POST['data'])
        if data[0]['value'] != '':
            registro = ServiceaereoReal.objects.get(id=data[0]['value'])
        else:
            registro = ServiceaereoReal()
        registro.numero = numero
        compra_venta = data[1]['value']
        registro.servicio = data[2]['value']
        registro.moneda = data[3]['value']
        if compra_venta == 'C':
            registro.precio = data[4]['value']
            registro.costo = 0
        else:
            registro.costo = data[4]['value']
            registro.precio = 0
        if len(data[5]['value']) > 0:
            registro.arbitraje = data[5]['value']
        else:
            registro.arbitraje = 0
        registro.tipogasto = data[6]['value']
        if len(data[7]['value']) > 0:
            registro.pinformar = data[7]['value']
        else:
            registro.pinformar = 0
        registro.secomparte = data[8]['value']
        registro.modo = data[9]['value']
        registro.socio = data[10]['value']
        if data[11]['value'] == 'on':
            registro.notomaprofit = True
        else:
            registro.notomaprofit = False
        #registro.detalle = data[12]['value']
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

def eliminar_gasto(request):
    resultado = {}
    try:
        id = request.POST['id']
        ServiceaereoReal.objects.get(id=id).delete()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


