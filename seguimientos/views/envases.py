import json
from django.contrib import messages
from django.http import HttpResponse
from seguimientos.models import Envases


""" TABLA PUERTO """
columns_table = {
    1: 'unidad',
    2: 'tipo',
    3: 'movimiento',
    4: 'terminos',
    5: 'cantidad',
    6: 'precio',
    7: 'profit',
    8: 'nrocontenedor',
    9: 'marcas',
    10: 'envase',
    11: 'tara',
    12: 'peso',
    13: 'precio',
    14: 'volumen',
}


def source_envases(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        """PROCESO FILTRO Y ORDEN BY"""
        start = int(request.GET['start'])
        numero = request.GET['numero']
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        registros = Envases.objects.filter(numero=numero).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Envases.objects.filter(numero=numero).count()
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
            registro_json.append(str(registro.id))  # data[0] - ID
            registro_json.append('' if registro.numero is None else str(registro.numero))  # data[1] - Número
            registro_json.append('' if registro.unidad is None else str(registro.unidad))  # data[2] - Unidad
            registro_json.append('' if registro.tipo is None else str(registro.tipo))  # data[3] - Tipo
            registro_json.append('' if registro.movimiento is None else str(registro.movimiento))  # data[4] - Movimiento
            registro_json.append('' if registro.terminos is None else str(registro.terminos))  # data[5] - Términos
            registro_json.append('' if registro.cantidad is None else str(registro.cantidad))  # data[6] - Cantidad
            registro_json.append('' if registro.precio is None else str(registro.precio))  # data[7] - Precio
            registro_json.append('' if registro.marcas is None else str(registro.marcas))  # data[9] - Marcas
            registro_json.append('' if registro.precinto is None else str(registro.precinto))  # data[10] - Precinto
            registro_json.append('' if registro.tara is None else str(registro.tara))  # data[11] - Tara
            registro_json.append('' if registro.bonifcli is None else str(registro.bonifcli))  # data[12] - Bonificación cliente
            registro_json.append('' if registro.envase is None else str(registro.envase))  # data[13] - Envase
            registro_json.append('' if registro.bultos is None else str(registro.bultos))  # data[14] - Bultos
            registro_json.append('' if registro.peso is None else str(registro.peso))  # data[15] - Peso
            registro_json.append('' if registro.profit is None else str(registro.profit))  # data[16] - Profit
            registro_json.append('' if registro.nrocontenedor is None else str(registro.nrocontenedor))  # data[17] - Número de contenedor
            registro_json.append('' if registro.volumen is None else str(registro.volumen))  # data[18] - Volumen
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




