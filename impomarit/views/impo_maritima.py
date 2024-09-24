import datetime
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from impomarit.forms import add_im_form, add_form, add_house, edit_form, edit_house, gastosForm
from impomarit.models import Master, Reservas, Embarqueaereo, VEmbarqueaereo
from mantenimientos.models import Clientes
from seguimientos.models import Seguimiento


@login_required(login_url='/')
def master_importacion_maritima(request):
    try:
        if request.user.has_perms(["mantenimientos.view_seguimientos",]):
            opciones_busqueda = {
                'cliente__icontains': 'CLIENTE',
                'embarcador__icontains': 'EMBARCADOR',
                'consignatario__icontains': 'CONSIGNATARIO',
                'origen_text__icontains': 'ORIGEN',
                'destino_text__icontains': 'DESTINO',
                'awb__icontains': 'BL',
                'hawb__icontains': 'HBL',
                'vapor__icontains': 'Vapor',
                'posicion__icontains': 'Posicion',
                # 'contenedores__icontains': 'Contenedor',
            }
            return render(request, 'impormarit/grilla_datos.html',{
                'form': add_form(),
                'form_house': add_house(),
                'form_search_master': add_im_form(),
                'form_edit_master':edit_form(),
                'form_edit_house': edit_house(),
                'opciones_busqueda': opciones_busqueda,
                'form_gastos': gastosForm(),
            })
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')


param_busqueda = {
    1: 'numero__icontains',
    2: 'llegada__icontains',
    3: 'transportista__icontains',
    4: 'awb__icontains',
    5: 'agente__icontains',
    6: 'consignatario__icontains',
    7: 'armador__icontains',
    8: 'vapor__icontains',
    9: 'origen__icontains',
    10: 'destino__icontains',
    11: 'status__icontains',
}

columns_table = {
    0: 'id',
    1: 'numero',
    2: 'llegada',
    3: 'transportista',
    4: 'awb',
    5: 'agente',
    6: 'consignatario',
    7: 'armador',
    8: 'vapor',
    9: 'origen',
    10: 'destino',
    11: 'status',
}

def source_importacion_master(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
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
        }
        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        buscar = str(request.GET['buscar'])
        que_buscar = str(request.GET['que_buscar'])
        if len(buscar) > 0:
            filtro[que_buscar] = buscar
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        if filtro:
            registros = Master.objects.filter(**filtro).order_by(*order)
        else:
            registros = Master.objects.all().order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Master.objects.all().count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def get_data(registros_filtrados):
    try:
        data = []
        cronologia = [
            'fecha',
            'estimadorecepcion',
            'recepcion',
            'fecemision',
            'fecseguro',
            'fecdocage',
            'loadingdate',
            'arriboreal',
            'fecaduana',
            'pagoenfirme',
            'vencimiento',
            'etd',
            'eta',
            'fechaonhand',
            'fecrecdoc',
            'recepcionprealert',
            'lugar',
            'nroseguro',
            'bltipo',
            'manifiesto',
            'credito',
            'prima',
            'observaciones',

        ]
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.numero is None else str(registro.numero))
            registro_json.append('' if registro.llegada is None else str(registro.llegada)[:10])
            registro_json.append('' if registro.transportista is None else str(registro.transportista))
            registro_json.append('' if registro.awb is None else str(registro.awb))
            registro_json.append('' if registro.agente is None else str(registro.agente))
            registro_json.append('' if registro.embarcador is None else str(registro.embarcador))
            registro_json.append('' if registro.armador is None else str(registro.armador))
            registro_json.append('' if registro.vapor is None else str(registro.vapor))
            registro_json.append('' if registro.origen is None else str(registro.origen))
            registro_json.append('' if registro.destino is None else str(registro.destino))
            registro_json.append('' if registro.status is None else str(registro.status))
            # rutas = Conexaerea.objects.filter(numero=registro.numero).annotate(num_archivos=Count('id')).values('num_archivos').first()
            # archivos = Attachhijo.objects.filter(numero=registro.numero).count()
            # embarques = Cargaaerea.objects.filter(numero=registro.numero).count()
            # envases = Envases.objects.filter(numero=registro.numero).count()
            # gastos = Serviceaereo.objects.filter(numero=registro.numero).count()
            # rutas = Conexaerea.objects.filter(numero=registro.numero).count()
            # registro_json.append(archivos)
            # registro_json.append(embarques)
            # registro_json.append(envases)
            # registro_json.append(gastos)
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

def get_argumentos_busqueda(**kwargs):
    try:
        result = {}
        for row in kwargs:
            if len(kwargs[row]) > 0:
                result[param_busqueda[int(row)]] = kwargs[row]
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



#traer datos houses tabla
def source_embarque_aereo(request, master):
    if is_ajax(request):
        start = int(request.POST.get('start', 0))  # Usa 0 como valor predeterminado si 'start' no está presente
        length = int(request.POST.get('length', 10))  # Usa 10 como valor predeterminado si 'length' no está presente
        draw = int(request.POST.get('draw', 1))
        registros = VEmbarqueaereo.objects.filter(awb=master)[start:start + length]
        data = get_data_embarque_aereo(registros)
        resultado = {
            'draw': draw,  # Enviar 'draw' para asegurarnos de que la solicitud y respuesta coincidan
            'recordsTotal': VEmbarqueaereo.objects.all().count(),  # Total de registros sin filtrar
            'recordsFiltered': registros.count(),  # Total de registros después del filtro
            'data': data  # Los datos filtrados
        }

        return JsonResponse(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def get_data_embarque_aereo(registros_filtrados):
    try:
        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append('' if registro.id is None else str(registro.id))  # Fecha
            registro_json.append('' if registro.fecha_embarque is None else str(registro.fecha_embarque)[:10])  # Fecha
            registro_json.append('' if registro.fecha_retiro is None else str(registro.fecha_retiro)[:10])  # Fecha
            registro_json.append('' if registro.numero is None else str(registro.numero))  # N° Seguimiento
            registro_json.append('' if registro.consignatario is None else str(registro.consignatario))  # Cliente
            registro_json.append('' if registro.origen is None else str(registro.origen))  # Origen
            registro_json.append('' if registro.destino is None else str(registro.destino))  # Destino
            registro_json.append('' if registro.status is None else str(registro.status))  # Estado
            registro_json.append('' if registro.posicion is None else str(registro.posicion))  # Estado
            registro_json.append('' if registro.operacion is None else str(registro.operacion))  # Estado
            registro_json.append('' if registro.awb is None else str(registro.awb))  # Estado
            registro_json.append('' if registro.hawb is None else str(registro.hawb))  # Estado
            registro_json.append('' if registro.vapor is None else str(registro.vapor))  # Estado
            registro_json.append('' if registro.notificar_agente is None else str(registro.notificar_agente)[:10])  # Estado
            registro_json.append('' if registro.notificar_cliente is None else str(registro.notificar_cliente)[:10])  # Estado


            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)



