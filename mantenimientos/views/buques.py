import datetime
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from mantenimientos.forms import add_buque_form, edit_buque_form
from mantenimientos.models import Vapores as Buques, Paises


@login_required(login_url='/')
def grilla_buques(request):
    try:
        if request.user.has_perms(["mantenimientos.view_vapores", ]):
            return render(request, 'buques/grilla_datos.html',{'title_page':'Mantenimiento de buques',})
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')


""" VISTA """

""" TABLA PUERTO """
columns_table = {
    0: 'id',
    1: 'codigo',
    2: 'nombre',
    3: 'bandera',
    4: 'observaciones',
}
param_busqueda = {
    1: 'codigo__icontains',
    2: 'nombre__icontains',
    3: 'bandera__icontains',
    4: 'observaciones__icontains',
}


def source_buques(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        args = {
            '1': request.GET['columns[1][search][value]'],
            '2': request.GET['columns[2][search][value]'],
            '3': request.GET['columns[3][search][value]'],
            '4': request.GET['columns[4][search][value]'],
        }
        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        if filtro:
            registros = Buques.objects.filter(**filtro).order_by(*order)
        else:
            registros = Buques.objects.all().order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Buques.objects.all().count()
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
            registro_json.append('' if registro.codigo is None else str(registro.codigo))
            registro_json.append('' if registro.nombre is None else str(registro.nombre))
            registro_json.append('' if registro.bandera is None else str(registro.bandera))
            registro_json.append('' if registro.observaciones is None else str(registro.observaciones))
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
def agregar_buque(request):
    try:
        if request.user.has_perms(["mantenimientos.add_vapores", ]):
            ctx = {'form': add_buque_form(),'title_page':'Agregar buque',}
            if request.method == 'POST':
                form = add_buque_form(request.POST)
                if form.is_valid():
                    buque = Buques()
                    buque.codigo = buque.get_codigo()
                    buque.nombre = form.cleaned_data['nombre']
                    buque.bandera = form.cleaned_data['bandera']
                    if buque.bandera is None:
                        buque.bandera = 'S/I'
                    if buque.observaciones is None:
                        buque.observaciones = 'S/I'
                    buque.observaciones = form.cleaned_data['observaciones']
                    buque.save()
                    messages.success(request, 'Buque agregada con èxito')
                    return HttpResponseRedirect('/buques')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/agregar_buque')
            return render(request, "buques/agregar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/buques")


@login_required(login_url='/')
def modificar_buque(request, id_buque):
    try:
        if request.user.has_perms(["mantenimientos.change_vapores", ]):
            buque = Buques.objects.get(id=id_buque)
            ctx = {'form': edit_buque_form({
                'codigo': buque.codigo,
                'nombre': buque.nombre,
                'bandera': buque.bandera,
                'observaciones': buque.observaciones,
            },
            ),'title_page':'Modificar buque',}
            if request.method == 'POST':
                form = edit_buque_form(request.POST)
                if form.is_valid():
                    buque.codigo = form.cleaned_data['codigo']
                    buque.nombre = form.cleaned_data['nombre']
                    # if isinstance(Paises,form.cleaned_data['bandera']):
                    #     buque.bandera = form.cleaned_data['bandera'].nombre
                    # else:
                    #     buque.bandera = None
                    buque.bandera = form.cleaned_data['bandera']
                    buque.observaciones = form.cleaned_data['observaciones']
                    buque.save()
                    messages.success(request, 'Buque modificado con èxito')
                    return HttpResponseRedirect('/buques')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/modificar_buque')
            return render(request, "buques/modificar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/buques")


@login_required(login_url='/')
def eliminar_buque(request):
    resultado = {}
    if request.user.has_perms(["mantenimientos.delete_vapores", ]):
        if is_ajax(request):
            try:
                id = request.GET['id']
                buque = Buques.objects.get(id=id)
                # buque.estado = 1
                buque.delete()
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
