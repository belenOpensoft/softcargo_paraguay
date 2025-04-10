import datetime
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from mantenimientos.forms import add_buque_form, edit_buque_form, add_guia_form
from mantenimientos.models import VGrillaGuias, Guias
from seguimientos.models import Seguimiento


@login_required(login_url='/')
def grilla_guias(request):
    try:
        if request.user.has_perms(["mantenimientos.view_guias", ]):
            return render(request, 'guias/grilla_datos.html')
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')


""" VISTA """

""" TABLA PUERTO """
columns_table = {
    0: 'id',
    1: 'empresa',
    2: 'guia',
    3: 'estado',
    4: 'refmaster',
    5: 'tipo',
    6: 'destino',
    7: 'fecha',
    8: 'posicion',
}
param_busqueda = {
    1: 'empresa__icontains',
    2: 'guia__icontains',
    3: 'estado__icontains',
    4: 'refmaster__icontains',
    5: 'tipo__icontains',
    6: 'destino__icontains',
    7: 'fecha__icontains',
    8: 'posicion__icontains',
}


def source_guias(request):
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
        }
        vertodo = request.GET['vertodo']

        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        if vertodo == 'false':
            filtro['estado'] = 'DISPONIBLE'
        """FILTRO REGISTROS"""
        if filtro:
            registros = VGrillaGuias.objects.filter(**filtro).order_by(*order)
        else:
            registros = VGrillaGuias.objects.all().order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = VGrillaGuias.objects.all().count()
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
            registro_json.append('' if registro.empresa is None else str(registro.empresa))
            registro_json.append('' if registro.guia is None else str(registro.guia))
            registro_json.append('' if registro.estado is None else str(registro.estado))
            registro_json.append('' if registro.refmaster is None else str(registro.refmaster))
            registro_json.append('' if registro.tipo is None else str(registro.tipo))
            registro_json.append('' if registro.destino is None else str(registro.destino))
            registro_json.append('' if registro.fecha is None else str(registro.fecha))
            registro_json.append('' if registro.posicion is None else str(registro.posicion))
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
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/")
def agregar_guias(request):
    try:
        if request.user.has_perms(["mantenimientos.add_guias", ]):
            ctx = {
                'form': add_guia_form()
            }
            if request.method == 'POST':
                form = add_guia_form(request.POST)
                if form.is_valid():
                    empresa = form.cleaned_data['empresa']
                    numeracion = form.cleaned_data['numeracion']
                    cantidad = form.cleaned_data['cantidad']
                    numeracion = int(numeracion/10)
                    for number in range(1,cantidad + 1):
                        guia = Guias()
                        guia.transportista = empresa.codigo
                        guia.estado = 0
                        guia.fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        guia.prefijo = empresa.prefijoguia
                        check = numeracion % 7
                        guia.numero = numeracion * 10 + check
                        numeracion += 1
                        verif = Guias.objects.filter(prefijo=empresa.prefijoguia,numero=guia.numero,estado=0)
                        if verif.count() == 0:
                            guia.save()
                        else:
                            messages.error(request,"El numero de guia " + str(guia.numero) + " ya se encuentra registrado" )
                    messages.success(request, 'Guias ingresadas con èxito')
                    return HttpResponseRedirect('/guias')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/agregar_buque')
            return render(request, "guias/agregar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/guias")



@login_required(login_url='/')
def anular_guia(request):
    resultado = {}
    if request.user.has_perms(["mantenimientos.delete_guias", ]):
        if is_ajax(request):
            try:
                id = request.GET['id']
                guia = Guias.objects.get(id=id)
                guia.estado = 2
                guia.save()
                resultado['resultado'] = 'exito'
            except Exception as e:
                resultado['resultado'] = str(e)
        else:
            resultado['resultado'] = 'Ha ocurrido un error.'
    else:
        resultado['resultado'] = 'No tiene permisos para realizar esta accion.'
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

@login_required(login_url='/')
def asignar_guia_aerea(request):
    resultado = {}
    if request.user.has_perms(["mantenimientos.add_guias", ]):
        if is_ajax(request):
            try:
                id = request.POST['id']
                row = Seguimiento.objects.get(id=id)
                if row.awb is not None and len(row.awb) > 0:
                    resultado['resultado'] = 'Ya existe una guia asignada para el seguimiento actual'
                    resultado['numero'] = ''
                else:
                    vguia = VGrillaGuias.objects.filter(transportista=row.transportista,estado='DISPONIBLE').order_by('numero')
                    if vguia.count() > 0:
                        guia = Guias.objects.get(id=vguia[0].id)
                        guia.estado = 1
                        guia.save()
                        row.awb = str(vguia[0].guia)
                        row.save()
                        resultado['resultado'] = 'exito'
                        resultado['numero'] = str(vguia[0].guia)
                    else:
                        resultado['resultado'] = 'No se encontraron guias disponibles para el transportista'
                        resultado['numero'] = ''
            except Exception as e:
                resultado['resultado'] = str(e)
        else:
            resultado['resultado'] = 'Ha ocurrido un error.'
    else:
        resultado['resultado'] = 'No tiene permisos para realizar esta accion.'
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def obtener_guias_transportista(request, transportista_id):
    # Obtener las guías filtradas por transportista con estado = 1, ordenadas por fecha (o número)
    guias = Guias.objects.filter(transportista=transportista_id, estado=0).order_by('-fecha')  # O por número si es más adecuado

    # Preparar la respuesta JSON
    guias_data = [{'id': guia.id, 'prefijo': guia.prefijo, 'numero': guia.numero} for guia in guias]

    return JsonResponse(guias_data, safe=False)

