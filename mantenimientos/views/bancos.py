import datetime
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from mantenimientos.forms import add_banco_form, edit_banco_form
from mantenimientos.models import Bancos, Paises


@login_required(login_url='/')
def grilla_bancos(request):
    try:
        if request.user.has_perms(["mantenimientos.view_bancos",]):
            return render(request, 'bancos/grilla_datos.html',{'title_page':'Mantenimiento de bancos',})
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')


""" VISTA """

param_busqueda = {
    1: 'codigo__icontains',
    2: 'nombre__icontains',
    3: 'edi__icontains',
    4: 'pais__icontains',
    5: 'rut__icontains',
}
""" TABLA PUERTO """
columns_table = {
    0: 'id',
    1: 'codigo',
    2: 'nombre',
    3: 'edi',
    4: 'pais',
    5: 'rut',
}


def source_bancos(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        args = {
            '1': request.GET['columns[1][search][value]'],
            '2': request.GET['columns[2][search][value]'],
            '3': request.GET['columns[3][search][value]'],
            '4': request.GET['columns[4][search][value]'],
            '5': request.GET['columns[5][search][value]'],
        }
        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        if filtro:
            registros = Bancos.objects.filter(**filtro).order_by(*order)
        else:
            registros = Bancos.objects.all().order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Bancos.objects.all().count()
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
            registro_json.append('' if registro.edi is None else str(registro.edi))
            registro_json.append('' if registro.pais is None else str(registro.pais))
            registro_json.append('' if registro.rut is None else str(registro.rut))
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
def agregar_banco(request):
    try:
        if request.user.has_perms(["mantenimientos.add_bancos",]):
            ctx = {'form': add_banco_form(),'title_page':'Agregar bancos',}
            if request.method == 'POST':
                form = add_banco_form(request.POST)
                if form.is_valid():
                    banco = Bancos()
                    banco.codigo = form.cleaned_data['codigo']
                    banco.nombre = form.cleaned_data['nombre']
                    banco.edi = form.cleaned_data['edi']
                    banco.pais = form.cleaned_data['pais']
                    banco.rut = form.cleaned_data['rut']
                    banco.save()
                    messages.success(request, 'Banco agregada con èxito')
                    return HttpResponseRedirect('/bancos')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/agregar_banco')
            else:
                form = add_banco_form()
                paises = Paises.objects.all()  # Obtén la lista de países
                ctx = {'form': form, 'title_page': 'Agregar banco', 'paises': paises}
                return render(request, "bancos/agregar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/bancos")

@login_required(login_url='/')
def modificar_banco(request, id_banco):
    try:
        if request.user.has_perms(["mantenimientos.change_bancos", ]):
            banco = Bancos.objects.get(id=id_banco)
            paises = Paises.objects.all()  # Obtén la lista de países
            ctx = {'form': edit_banco_form({
                'codigo': banco.codigo,
                'nombre': banco.nombre,
                'pais': banco.pais,
                'edi': banco.edi,
                'rut': banco.rut,
            },

            ),
                'title_page': 'Modificar banco',
                'paises':paises,
            }
            if request.method == 'POST':
                form = edit_banco_form(request.POST)
                if form.is_valid():
                    banco.codigo = form.cleaned_data['codigo']
                    banco.nombre = form.cleaned_data['nombre']
                    banco.edi = form.cleaned_data['edi']
                    banco.pais = form.cleaned_data['pais']
                    banco.rut = form.cleaned_data['rut']
                    banco.save()
                    messages.success(request, 'Banco modificado con èxito')
                    return HttpResponseRedirect('/bancos')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/modificar_banco')

            return render(request, "bancos/modificar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/bancos")


@login_required(login_url='/')
def eliminar_banco(request):

    resultado = {}
    if request.user.has_perms(["mantenimientos.delete_bancos", ]):
        if is_ajax(request):
            try:
                id = request.GET['id']
                banco = Bancos.objects.get(id=id)
                #banco.estado = 1
                banco.delete()
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


