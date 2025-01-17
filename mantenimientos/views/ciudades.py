import datetime
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from mantenimientos.forms import add_ciudad_form, edit_ciudad_form
from mantenimientos.models import Ciudades, Paises


@login_required(login_url='/')
def grilla_ciudades(request):
    try:
        if request.user.has_perms(["mantenimientos.view_ciudades",]):
            return render(request, 'ciudades/grilla_datos.html',{'title_page': 'Mantenimiento de ciudades',})
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
    3: 'pais',
    4: 'codedi',
    5: 'codaduana',
    6: 'paises_idinternacional',
    7: 'fechaactualizado',
}
param_busqueda = {
    1: 'codigo__icontains',
    2: 'nombre__icontains',
    3: 'pais__icontains',
    4: 'codedi__icontains',
    5: 'codaduana__icontains',
    6: 'paises_idinternacional__icontains',
    7: 'fechaactualizado__icontains',
}


def source_ciudades(request):
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
        }
        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        if filtro:
            registros = Ciudades.objects.filter(**filtro).exclude(estado=1).order_by(*order)
        else:
            registros = Ciudades.objects.all().exclude(estado=1).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Ciudades.objects.all().exclude(estado=1).count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def get_data(puertos_filtrados):
    try:
        data = []
        for puerto in puertos_filtrados:
            puerto_json = []
            puerto_json.append(str(puerto.id))
            puerto_json.append('' if puerto.codigo is None else str(puerto.codigo))
            puerto_json.append('' if puerto.nombre is None else str(puerto.nombre))
            puerto_json.append('' if puerto.pais is None else str(puerto.pais))
            puerto_json.append('' if puerto.codedi is None else str(puerto.codedi))
            puerto_json.append('' if puerto.codaduana is None else str(puerto.codaduana))
            puerto_json.append('' if puerto.paises_idinternacional is None else str(puerto.paises_idinternacional))
            puerto_json.append('' if puerto.fechaactualizado is None else str(puerto.fechaactualizado))
            data.append(puerto_json)
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
def agregar_ciudad(request):
    try:
        if request.user.has_perms(["mantenimientos.add_ciudades",]):
            ctx = {'form': add_ciudad_form(),'title_page': 'Agregar ciudad',}
            if request.method == 'POST':
                form = add_ciudad_form(request.POST)
                if form.is_valid():
                    try:
                        ciudad = Ciudades()
                        ciudad.codigo = form.cleaned_data['codigo']
                        ciudad.nombre = form.cleaned_data['nombre']
                        ciudad.pais = form.cleaned_data['pais']
                        ciudad.codedi = form.cleaned_data['codedi']
                        ciudad.codaduana = form.cleaned_data['codaduana']
                        ciudad.paises_idinternacional = form.cleaned_data['paises_idinternacional']
                        ciudad.fechaactualizado = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        ciudad.save()
                        messages.success(request, 'Ciudad agregada con èxito')
                        return HttpResponseRedirect('/ciudades')
                    except IntegrityError:
                        messages.error(request, 'Error: Ya existe una ciudad con el mismo código.')

                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/agregar_ciudad')
            else:
                form = add_ciudad_form()
            paises = Paises.objects.all()  # Obtén la lista de países
            ctx = {'form': form, 'title_page': 'Agregar ciudad', 'paises': paises}
            return render(request, "ciudades/agregar.html", ctx)

        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/ciudades")

@login_required(login_url='/')
def modificar_ciudad(request, id_ciudad):
    try:
        if request.user.has_perms(["mantenimientos.change_ciudades", ]):
            ciudad = Ciudades.objects.get(id=id_ciudad)
            if request.method == 'POST':
                form = edit_ciudad_form(request.POST)
                if form.is_valid():
                    try:
                        ciudad.codigo = form.cleaned_data['codigo']
                        ciudad.nombre = form.cleaned_data['nombre']
                        ciudad.pais = form.cleaned_data['pais']
                        ciudad.codedi = form.cleaned_data['codedi']
                        ciudad.codaduana = form.cleaned_data['codaduana']
                        ciudad.paises_idinternacional = form.cleaned_data['paises_idinternacional']
                        ciudad.fechaactualizado = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        ciudad.save()
                        messages.success(request, 'Ciudad modificada con èxito')
                        return HttpResponseRedirect('/ciudades')
                    except IntegrityError:
                        messages.error(request, 'Error: Ya existe una ciudad con el mismo código.')

                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/modificar_ciudad')
            else:
                form = add_ciudad_form()
            paises = Paises.objects.all()  # Obtén la lista de países
            ctx = {'form': edit_ciudad_form({
                'codigo': ciudad.codigo,
                'nombre': ciudad.nombre,
                'pais': ciudad.pais,
                'codedi': ciudad.codedi,
                'codaduana': ciudad.codaduana,
                'paises_idinternacional': ciudad.paises_idinternacional,
            }, ),
                'title_page': 'Modificar ciudad',
                'paises': paises,
                'nomprepais': ciudad.pais,
            }
            return render(request, "ciudades/modificar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/ciudades")

@login_required(login_url='/')
def eliminar_ciudad(request):

    resultado = {}
    if request.user.has_perms(["mantenimientos.delete_ciudades", ]):
        if is_ajax(request):
            try:
                id = request.GET['id']
                ciudad = Ciudades.objects.get(id=id)
                ciudad.estado = 1
                ciudad.save()
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


