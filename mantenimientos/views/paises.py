import datetime
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db.models import Q

from mantenimientos.forms import add_pais_form, edit_pais_form
from mantenimientos.models import Paises


@login_required(login_url='/')
def grilla_paises(request):
    try:
        if request.user.has_perms(["mantenimientos.view_paises", ]):
            return render(request, 'paises/grilla_datos.html',{'title_page': 'Mantenimiento de paises',})
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')


""" VISTA """

""" TABLA PUERTO """
columns_table = {
    0: 'id',
    1: 'nombre',
    2: 'continente',
    3: 'iata',
    4: 'idinternacional',
    5: 'cuit',
    6: 'edi',
}
param_busqueda = {
    1: 'nombre__icontains',
    2: 'continente',
    3: 'iata__icontains',
    4: 'idinternacional__icontains',
    5: 'cuit__icontains',
    6: 'edi__icontains',
}


def source_paises(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        args = {
            '1': request.GET['columns[1][search][value]'],
            '2': request.GET['columns[2][search][value]'],
            '3': request.GET['columns[3][search][value]'],
            '4': request.GET['columns[4][search][value]'],
            '5': request.GET['columns[5][search][value]'],
            '6': request.GET['columns[6][search][value]'],
        }
        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        if filtro:
            registros = Paises.objects.filter(**filtro).order_by(*order)
        else:
            registros = Paises.objects.all().order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Paises.objects.all().count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def get_data(registros_filtrados):
    try:
        data = []
        continente_map = {
            '1': 'Sudamérica',
            '2': 'Norteamérica',
            '3': 'Centroamérica',
            '4': 'Europa',
            '5': 'Asia',
            '6': 'África',
            '7': 'Oceanía'
        }


        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.nombre is None else str(registro.nombre))
            continente = '' if registro.continente is None else continente_map.get(str(registro.continente),'Desconocido')
            registro_json.append(continente)
            # registro_json.append('' if registro.iata is None else str(registro.continente))
            registro_json.append('' if registro.iata is None else str(registro.iata))
            registro_json.append('' if registro.idinternacional is None else str(registro.idinternacional))
            registro_json.append('' if registro.cuit is None else str(registro.cuit))
            registro_json.append('' if registro.edi is None else str(registro.edi))
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


def get_argumentos_busqueda_old(**kwargs):
    try:
        result = {}
        for row in kwargs:
            if len(kwargs[row]) > 0:
                result[param_busqueda[int(row)]] = kwargs[row]
        return result
    except Exception as e:
        raise TypeError(e)

def get_argumentos_busqueda(**kwargs):
    try:
        result = {}

        continente_map = {
            '1': 'Sudamérica',
            '2': 'Norteamérica',
            '3': 'Centroamérica',
            '4': 'Europa',
            '5': 'Asia',
            '6': 'África',
            '7': 'Oceanía'
        }

        for row in kwargs:
            valor = kwargs[row].strip()
            if not valor:
                continue

            if int(row) == 2:  # Columna continente
                valor_normalizado = normalizar(valor)
                coincidencias = [
                    k for k, v in continente_map.items()
                    if valor_normalizado in normalizar(v)
                ]
                if coincidencias:
                    result['continente__in'] = coincidencias
            else:
                campo = param_busqueda[int(row)]
                result[campo] = valor

        return result
    except Exception as e:
        raise TypeError(f"Error en get_argumentos_busqueda: {e}")


import unicodedata

def normalizar(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    ).lower()


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/")
def agregar_pais_old(request):
    try:
        if request.user.has_perms(["mantenimientos.add_paises", ]):
            ctx = {'form': add_pais_form(),'title_page': 'Agregar pais'}
            if request.method == 'POST':
                form = add_pais_form(request.POST)
                if form.is_valid():
                    pais = Paises()
                    pais.nombre = form.cleaned_data['nombre']
                    pais.continente = int(form.cleaned_data['continente'])
                    pais.iata = form.cleaned_data['iata']
                    pais.idinternacional = form.cleaned_data['idinternacional']
                    pais.cuit = form.cleaned_data['cuit']
                    pais.edi = form.cleaned_data['edi']
                    pais.save()
                    messages.success(request, 'Pais agregada con èxito')
                    return HttpResponseRedirect('/paises')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/agregar_pais')
            return render(request, "paises/agregar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/paises")


@login_required(login_url="/")
def agregar_pais(request):
    try:
        if request.user.has_perms(["mantenimientos.add_paises", ]):

            ctx = {'form': add_pais_form(), 'title_page': 'Agregar país'}
            if request.method == 'POST':
                form = add_pais_form(request.POST)
                if form.is_valid():
                    nombre = form.cleaned_data['nombre']
                    idinternacional = form.cleaned_data['idinternacional']

                    if Paises.objects.filter(Q(nombre__iexact=nombre) | Q(idinternacional__iexact=idinternacional)).exists():
                        messages.error(request, 'Ya existe un país con ese nombre o código internacional.')
                        return HttpResponseRedirect('/agregar_pais')

                    pais = Paises(
                        nombre=nombre,
                        continente=int(form.cleaned_data['continente']),
                        iata=form.cleaned_data['iata'],
                        idinternacional=idinternacional,
                        cuit=form.cleaned_data['cuit'],
                        edi=form.cleaned_data['edi']
                    )
                    pais.save()
                    messages.success(request, 'País agregado con éxito.')
                    return HttpResponseRedirect('/paises')
                else:
                    messages.error(request, 'Formulario inválido, intente nuevamente.')
                    return HttpResponseRedirect('/agregar_pais')
            return render(request, "paises/agregar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta acción.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/paises")


@login_required(login_url='/')
def modificar_pais(request, id_pais):
    try:
        if request.user.has_perms(["mantenimientos.change_paises", ]):
            pais = Paises.objects.get(id=id_pais)
            ctx = {'form': edit_pais_form({
                'nombre': pais.nombre,
                'continente': pais.continente,
                'iata': pais.iata,
                'idinternacional': pais.idinternacional,
                'cuit': pais.cuit,
                'edi': pais.edi,
            },

            ),'title_page': 'Modificar pais'}
            if request.method == 'POST':
                form = edit_pais_form(request.POST)
                if form.is_valid():
                    pais.nombre = form.cleaned_data['nombre']
                    pais.continente = int(form.cleaned_data['continente'])
                    pais.iata = form.cleaned_data['iata']
                    pais.idinternacional = form.cleaned_data['idinternacional']
                    pais.cuit = form.cleaned_data['cuit']
                    pais.edi = form.cleaned_data['edi']
                    pais.save()
                    messages.success(request, 'País modificado con èxito')
                    return HttpResponseRedirect('/paises')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/modificar_pais')
            return render(request, "paises/modificar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/paises")


@login_required(login_url='/')
def eliminar_pais(request):
    resultado = {}
    if request.user.has_perms(["mantenimientos.delete_paises", ]):
        if is_ajax(request):
            try:
                id = request.GET['id']
                pais = Paises.objects.get(id=id)
                # pais.estado = 1
                pais.delete()
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
