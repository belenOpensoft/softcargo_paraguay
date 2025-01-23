import datetime
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from mantenimientos.forms import add_producto_form, edit_producto_form
from mantenimientos.models import Productos


@login_required(login_url='/')
def grilla_productos(request):
    try:
        if request.user.has_perms(["mantenimientos.view_productos",]):
            return render(request, 'productos/grilla_datos.html',{'title_page':'Mantenimiento de productos',})
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')


""" VISTA """

param_busqueda = {
    1: 'codigo__icontains',
    2: 'nombre__icontains',
    3: 'descripcion__icontains',
}
""" TABLA PUERTO """
columns_table = {
    0: 'id',
    1: 'codigo',
    2: 'nombre',
    3: 'descripcion',
}


def source_productos(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        args = {
            '1': request.GET['columns[1][search][value]'],
            '2': request.GET['columns[2][search][value]'],
            '3': request.GET['columns[3][search][value]'],
        }
        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        if filtro:
            registros = Productos.objects.filter(**filtro).order_by(*order)
        else:
            registros = Productos.objects.all().order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Productos.objects.all().count()
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
            registro_json.append('' if registro.descripcion is None else str(registro.descripcion))
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


@login_required(login_url="/")
def agregar_producto(request):
    try:
        if request.user.has_perms(["mantenimientos.add_productos",]):
            ctx = {'form': add_producto_form(),'title_page':'Agregar producto'}
            if request.method == 'POST':
                form = add_producto_form(request.POST)
                if form.is_valid():
                    producto = Productos()
                    producto.nombre = form.cleaned_data['nombre']
                    producto.descripcion = form.cleaned_data['descripcion']
                    producto.save()
                    messages.success(request, 'Producto agregada con èxito')
                    return HttpResponseRedirect('/productos')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/agregar_producto')
            return render(request, "productos/agregar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/productos")

@login_required(login_url='/')
def modificar_producto(request, id_producto):
    try:
        if request.user.has_perms(["mantenimientos.change_productos", ]):
            producto = Productos.objects.get(id=id_producto)
            ctx = {'form': edit_producto_form({
                'codigo': producto.codigo,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
            },

            ),'title_page':'Modificar producto'}
            if request.method == 'POST':
                form = edit_producto_form(request.POST)
                if form.is_valid():
                    producto.codigo = form.cleaned_data['codigo']
                    producto.nombre = form.cleaned_data['nombre']
                    producto.descripcion = form.cleaned_data['descripcion']
                    producto.save()
                    messages.success(request, 'Producto modificado con èxito')
                    return HttpResponseRedirect('/productos')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/modificar_producto')
            return render(request, "productos/modificar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/productos")

@login_required(login_url='/')
def eliminar_producto(request):
    resultado = {}
    if request.user.has_perms(["mantenimientos.delete_productos", ]):
        if is_ajax(request):
            try:
                id = request.GET['id']
                producto = Productos.objects.get(id=id)
                #producto.estado = 1
                producto.delete()
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


