import datetime
import json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from mantenimientos.forms import add_cliente_form
from mantenimientos.models import Clientes as SociosComerciales,VSociosComerciales


@login_required(login_url='/')
def grilla_clientes(request):
    try:
        if request.user.has_perms(["mantenimientos.view_socioscomerciales",]):
            return render(request, 'clientes/grilla_datos.html',{'title_page':'Mantenimiento de socios comerciales'})
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')

""" TABLA PUERTO """
columns_table = {
    0: 'id',
    1: 'codigo',
    2: 'empresa',
    3: 'razonsocial',
    4: 'ruc',
    5: 'direccion',
    6: 'localidad',
    7: 'pais',
    8: 'ciudad',
    9: 'tipo',
}
param_busqueda = {
    1: 'codigo__icontains',
    2: 'empresa__icontains',
    3: 'razonsocial__icontains',
    4: 'ruc__icontains',
    5: 'direccion__icontains',
    6: 'localidad__icontains',
    7: 'pais__icontains',
    8: 'ciudad__icontains',
    9: 'tipo__icontains',
}

def source_socios_comerciales(request):
    if is_ajax(request):
        args = {
            '1': request.GET.get('columns[1][search][value]', ''),
            '2': request.GET.get('columns[2][search][value]', ''),
            '3': request.GET.get('columns[3][search][value]', ''),
            '4': request.GET.get('columns[4][search][value]', ''),
            '5': request.GET.get('columns[5][search][value]', ''),
            '6': request.GET.get('columns[6][search][value]', ''),
            '7': request.GET.get('columns[7][search][value]', ''),
            '8': request.GET.get('columns[8][search][value]', ''),
            '9': request.GET.get('columns[9][search][value]', ''),
        }
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        if filtro:
            registros = VSociosComerciales.objects.filter(**filtro).order_by(*order)
        else:
            registros = VSociosComerciales.objects.all().exclude(estado=1).order_by(*order)
        resultado = {}
        data = get_data(registros[start:end])
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = VSociosComerciales.objects.all().count()
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
            registro_json.append('' if registro.empresa is None else str(registro.empresa))
            registro_json.append('' if registro.razonsocial is None else str(registro.razonsocial))
            registro_json.append('' if registro.ruc is None else str(registro.ruc))
            registro_json.append('' if registro.direccion is None else str(registro.direccion))
            registro_json.append('' if registro.localidad is None else str(registro.localidad))
            registro_json.append('' if registro.pais is None else str(registro.pais))
            registro_json.append('' if registro.ciudad is None else str(registro.ciudad))
            registro_json.append('' if registro.tipo is None else str(registro.tipo))
            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)

def source_socios_comerciales_old(request):
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
        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        if filtro:
            registros = SociosComerciales.objects.filter(**filtro).order_by(*order)
        else:
            registros = SociosComerciales.objects.all().exclude(estado=1).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = SociosComerciales.objects.all().count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)
def get_data_old(registros_filtrados):
    try:
        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.codigo is None else str(registro.codigo))
            registro_json.append('' if registro.empresa is None else str(registro.empresa))
            registro_json.append('' if registro.razonsocial is None else str(registro.razonsocial))
            registro_json.append('' if registro.ruc is None else str(registro.ruc))
            registro_json.append('' if registro.direccion is None else str(registro.direccion))
            registro_json.append('' if registro.localidad is None else str(registro.localidad))
            registro_json.append('' if registro.pais is None else str(registro.pais))
            registro_json.append('' if registro.ciudad is None else str(registro.ciudad))
            registro_json.append('' if registro.tipo is None else str(registro.tipo))
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

def get_argumentos_busqueda_old(**kwargs):
    try:
        result = {}
        for row in kwargs:
            if len(kwargs[row]) > 0:
                result[param_busqueda[int(row)]] = kwargs[row]
        return result
    except Exception as e:
        raise TypeError(e)
def is_ajax(request):
    # return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    return True


@login_required(login_url="/")
def agregar_socio_comercial_old(request, id_socio=None):
    try:
        if request.user.has_perms(["mantenimientos.add_basicosocioscomerciales"]):
            if id_socio:
                cliente = get_object_or_404(SociosComerciales, id=id_socio)
                ctx = {'form': add_cliente_form(instance=cliente),
                       'title_page': 'Modificar socio comercial',
                       'tipo':'Modificar'
                       }
            else:
                ctx = {'form': add_cliente_form(),
                       'title_page': 'Agregar socio comercial',
                       'tipo': 'Agregar'
                       }
            if request.method == 'POST':
                form = add_cliente_form(request.POST, instance=cliente if id_socio else None)
                if form.is_valid():
                    cliente = form.save(commit=False)
                    cliente.tipo = 1
                    if ctx['tipo'] == 'Agregar':
                        cliente.codigo = SociosComerciales().get_codigo()
                    cliente.save()
                    messages.success(request, 'Socio comercial ' + str(ctx['tipo']) + ' con éxito')
                    return HttpResponseRedirect('/socios_comerciales')
                else:
                    messages.error(request, 'Formulario inválido, intente nuevamente.')
                    return HttpResponseRedirect('/agregar_socio_comercial')

            return render(request, "clientes/agregar.html", ctx)
        else:
            raise PermissionDenied('No tiene permisos para realizar esta acción.')
    except Exception as e:
        messages.error(request, str(e))
        #return HttpResponseRedirect("/clientes")

def agregar_socio_comercial(request, id_socio=None):
    try:
        if request.user.has_perms(["mantenimientos.add_basicosocioscomerciales"]):
            if id_socio:
                cliente = get_object_or_404(SociosComerciales, id=id_socio)
                form = add_cliente_form(initial={
                    'tipo': cliente.tipo,
                    'empresa': cliente.empresa,
                    'razonsocial': cliente.razonsocial,
                    'direccion': cliente.direccion,
                    'localidad': cliente.localidad,
                    'cpostal': cliente.cpostal,
                    'ruc': cliente.ruc,
                    'telefono': cliente.telefono,
                    'fecalta': cliente.fecalta.strftime('%Y-%m-%d') if cliente.fecalta else '',
                    'contactos': cliente.contactos,
                    'observaciones': cliente.observaciones,
                    'ciudad': cliente.ciudad,
                    'pais': cliente.pais,
                })
                ctx = {
                    'form': form,
                    'title_page': 'Modificar socio comercial',
                    'tipo': 'Modificar'
                }
            else:
                form = add_cliente_form()
                ctx = {
                    'form': form,
                    'title_page': 'Agregar socio comercial',
                    'tipo': 'Agregar'
                }

            if request.method == 'POST':
                form = add_cliente_form(request.POST)
                if form.is_valid():
                    try:
                        if id_socio:
                            cliente.tipo = form.cleaned_data['tipo']
                            cliente.empresa = form.cleaned_data['empresa']
                            cliente.razonsocial = form.cleaned_data['razonsocial']
                            cliente.direccion = form.cleaned_data['direccion']
                            cliente.localidad = form.cleaned_data['localidad']
                            cliente.cpostal = form.cleaned_data['cpostal']
                            cliente.ruc = form.cleaned_data['ruc']
                            cliente.telefono = form.cleaned_data['telefono']
                            cliente.fecalta = form.cleaned_data['fecalta']
                            cliente.contactos = form.cleaned_data['contactos']
                            cliente.observaciones = form.cleaned_data['observaciones']
                            cliente.ciudad = form.cleaned_data['ciudad']
                            cliente.pais = form.cleaned_data['pais']
                        else:
                            cliente = SociosComerciales(
                                tipo=form.cleaned_data['tipo'],
                                empresa=form.cleaned_data['empresa'],
                                razonsocial=form.cleaned_data['razonsocial'],
                                direccion=form.cleaned_data['direccion'],
                                localidad=form.cleaned_data['localidad'],
                                cpostal=form.cleaned_data['cpostal'],
                                ruc=form.cleaned_data['ruc'],
                                telefono=form.cleaned_data['telefono'],
                                fecalta=form.cleaned_data['fecalta'],
                                contactos=form.cleaned_data['contactos'],
                                observaciones=form.cleaned_data['observaciones'],
                                ciudad=form.cleaned_data['ciudad'],
                                pais=form.cleaned_data['pais'],
                            )
                            if ctx['tipo'] == 'Agregar':
                                cliente.codigo = SociosComerciales().get_codigo()

                        cliente.save()
                        messages.success(request, 'Socio comercial ' + str(ctx['tipo']) + ' con éxito')
                        return HttpResponseRedirect('/socios_comerciales')
                    except IntegrityError:
                        messages.error(request, 'Error: Ya existe un socio comercial con el mismo código.')
                else:
                    messages.error(request, 'Formulario inválido, intente nuevamente.')
                    return HttpResponseRedirect('/agregar_socio_comercial')

            return render(request, "clientes/agregar.html", ctx)
        else:
            raise PermissionDenied('No tiene permisos para realizar esta acción.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/socios_comerciales")


@login_required(login_url='/')
def eliminar_socio_comercial(request):

    resultado = {}
    if request.user.has_perms(["mantenimientos.delete_basicosocioscomerciales", ]):
        if is_ajax(request):
            try:
                id = request.GET['id']
                cliente = SociosComerciales.objects.get(id=id)
                cliente.delete()
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

