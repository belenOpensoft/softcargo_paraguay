import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from administracion_contabilidad.forms import Cobranza
from administracion_contabilidad.models import Boleta
from mantenimientos.models import Clientes


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

def cobranza_view(request):
    form = Cobranza(request.POST or None)
    return render(request, 'cobranza.html', {'form': form})


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