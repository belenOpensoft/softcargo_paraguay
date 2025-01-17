import datetime
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from mantenimientos.forms import add_moneda_form, edit_moneda_form
from mantenimientos.models import Monedas, Paises


@login_required(login_url='/')
def grilla_monedas(request):
    try:
        if request.user.has_perms(["mantenimientos.view_monedas",]):
            return render(request, 'monedas/grilla_datos.html',{'title_page':'Mantenimiento de monedas',})
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
    4: 'simbolo',
    5: 'solicitar',
    6: 'alias',
    7: 'valorminimo',
    8: 'valormaximo',
    9: 'paridadminima',
    10: 'paridadmaxima',
    11: 'corporativo',
}
param_busqueda = {
    1: 'codigo__icontains',
    2: 'nombre__icontains',
    3: 'pais__icontains',
    4: 'simbolo__icontains',
    5: 'solicitar__icontains',
    6: 'alias__icontains',
    7: 'valorminimo__icontains',
    8: 'valormaximo__icontains',
    9: 'paridadminima__icontains',
    10: 'paridadmaxima__icontains',
    11: 'corporativo__icontains',
}


def source_monedas(request):
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
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        if filtro:
            registros = Monedas.objects.filter(**filtro).order_by(*order)
        else:
            registros = Monedas.objects.all().order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Monedas.objects.all().count()
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
            registro_json.append('' if registro.pais is None else str(registro.pais))
            registro_json.append('' if registro.simbolo is None else str(registro.simbolo))
            registro_json.append('' if registro.solicitar is None else str(registro.solicitar))
            registro_json.append('' if registro.alias is None else str(registro.alias))
            registro_json.append('' if registro.valorminimo is None else str(registro.valorminimo))
            registro_json.append('' if registro.valormaximo is None else str(registro.valormaximo))
            registro_json.append('' if registro.paridadminima is None else str(registro.paridadminima))
            registro_json.append('' if registro.paridadmaxima is None else str(registro.paridadmaxima))
            registro_json.append('' if registro.corporativo is None else str(registro.corporativo))
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
def agregar_moneda(request):
    try:
        if request.user.has_perms(["mantenimientos.add_monedas",]):
            ctx = {'form': add_moneda_form(),'title_page':'Agregar moneda',}
            if request.method == 'POST':
                form = add_moneda_form(request.POST)
                if form.is_valid():
                    moneda = Monedas()
                    moneda.codigo = form.cleaned_data['codigo']
                    moneda.nombre = form.cleaned_data['nombre']
                    moneda.pais = form.cleaned_data['pais']
                    moneda.simbolo = form.cleaned_data['simbolo']
                    moneda.solicitar = form.cleaned_data['solicitar']
                    moneda.alias = form.cleaned_data['alias']
                    moneda.valorminimo = form.cleaned_data['valorminimo']
                    moneda.valormaximo = form.cleaned_data['valormaximo']
                    moneda.paridadminima = form.cleaned_data['paridadminima']
                    moneda.paridadmaxima = form.cleaned_data['paridadmaxima']
                    moneda.corporativo = form.cleaned_data['corporativo']
                    aux = Monedas.objects.filter(codigo = moneda.codigo)
                    if aux.count() == 0:
                        moneda.save()
                        messages.success(request, 'Moneda agregada con èxito')
                        return HttpResponseRedirect('/monedas')
                    else:
                        ctx['form'] = form
                        messages.warning(request, 'Código de moneda ya existente')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/agregar_moneda')
            return render(request, "monedas/agregar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/monedas")

@login_required(login_url='/')
def modificar_moneda(request, id_moneda):
    try:
        if request.user.has_perms(["mantenimientos.change_monedas", ]):
            moneda = Monedas.objects.get(id=id_moneda)
            pais = Paises.objects.get(nombre=moneda.pais)

            ctx = {'form': edit_moneda_form({
                'codigo': moneda.codigo,
                'nombre': moneda.nombre,
                'pais': pais.id,
                'simbolo': moneda.simbolo,
                'solicitar': moneda.solicitar,
                'alias': moneda.alias,
                'valorminimo': moneda.valorminimo,
                'valormaximo': moneda.valormaximo,
                'paridadminima': moneda.paridadminima,
                'paridadmaxima': moneda.paridadmaxima,
                'corporativo': moneda.corporativo,
            },

            ),'title_page':'Modificar moneda',}

            if request.method == 'POST':
                form = edit_moneda_form(request.POST)
                if form.is_valid():
                    moneda.codigo = form.cleaned_data['codigo']
                    moneda.nombre = form.cleaned_data['nombre']
                    moneda.pais = form.cleaned_data['pais']
                    moneda.simbolo = form.cleaned_data['simbolo']
                    moneda.solicitar = form.cleaned_data['solicitar']
                    moneda.alias = form.cleaned_data['alias']
                    moneda.valorminimo = form.cleaned_data['valorminimo']
                    moneda.valormaximo = form.cleaned_data['valormaximo']
                    moneda.paridadminima = form.cleaned_data['paridadminima']
                    moneda.paridadmaxima = form.cleaned_data['paridadmaxima']
                    moneda.corporativo = form.cleaned_data['corporativo']
                    moneda.save()
                    messages.success(request, 'Moneda modificada con èxito')
                    return HttpResponseRedirect('/monedas')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/modificar_moneda')
            return render(request, "monedas/modificar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/monedas")


@login_required(login_url='/')
def eliminar_moneda(request):
    resultado = {}
    if request.user.has_perms(["mantenimientos.delete_monedas", ]):
        if is_ajax(request):
            try:
                id = request.GET['id']
                moneda = Monedas.objects.get(id=id)
                # moneda.estado = 1
                moneda.delete()
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


