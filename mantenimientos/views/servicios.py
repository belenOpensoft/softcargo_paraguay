import datetime
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from mantenimientos.forms import add_banco_form, edit_banco_form, edit_servicio_form, add_servicio_form
from mantenimientos.models import Bancos, Paises, Servicios


@login_required(login_url='/')
def grilla_servicios(request):
    try:
        if request.user.has_perms(["mantenimientos.view_servicios",]):
            return render(request, 'servicios/grilla_datos.html',{'title_page':'Mantenimiento de servicios',})
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')


""" VISTA """

param_busqueda = {
    1: 'codigo__icontains',
    2: 'nombre__icontains',
    3: 'contable__icontains',
    4: 'tipo_gasto__icontains',
}
""" TABLA PUERTO """
columns_table = {
    0: 'id',
    1: 'codigo',
    2: 'nombre',
    3: 'contable',
    4: 'tipo',
}


def source_servicios(request):
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
            registros = Servicios.objects.filter(**filtro).order_by(*order)
        else:
            registros = Servicios.objects.all().order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Servicios.objects.all().count()
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
            registro_json.append('' if registro.contable is None else str(registro.contable))
            registro_json.append('' if registro.tipogasto is None else str(registro.tipogasto))
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
def agregar_servicio(request):
    try:
        if request.user.has_perms(["mantenimientos.add_servicios",]):
            ctx = {'form': add_servicio_form(),'title_page':'Agregar servicio',}
            if request.method == 'POST':
                form = add_servicio_form(request.POST)
                if form.is_valid():
                    servicio = Servicios()
                    servicio.codigo = servicio.get_codigo()
                    servicio.nombre = form.cleaned_data['nombre']
                    servicio.contable = form.cleaned_data['contable']
                    servicio.tipogasto = form.cleaned_data['tipo_gasto']
                    servicio.nombreingles = form.cleaned_data['nombreingles']
                    servicio.activa = 0 if form.cleaned_data['activa'] == False else 1
                    servicio.imputar = form.cleaned_data['imputable']
                    servicio.tasa = form.cleaned_data['tasa']
                    servicio.save()
                    messages.success(request, 'Servicio agregado con èxito')
                    return HttpResponseRedirect('/servicios')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/agregar_servicio')
            return render(request, "servicios/agregar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/servicios")


@login_required(login_url='/')
def modificar_servicio(request, id_servicio):
    try:
        if request.user.has_perms(["mantenimientos.change_servicios", ]):
            servicio = Servicios.objects.get(id=id_servicio)

            ctx = {'form': edit_servicio_form({
                'nombre': servicio.nombre,
                'codigo': servicio.codigo,
                'contable': servicio.contable,
                'tipo_gasto': servicio.tipogasto,
                'nombreingles': servicio.nombreingles,
                'activa': servicio.activa,
                'tasa': servicio.tasa,
                'imputable':servicio.imputar
            },

            ),
                'title_page': 'Modificar servicio',
            }
            if request.method == 'POST':
                form = edit_servicio_form(request.POST)
                if form.is_valid():
                    servicio.nombre = form.cleaned_data['nombre']
                    servicio.contable = form.cleaned_data['contable']
                    servicio.tipogasto = form.cleaned_data['tipo_gasto']
                    servicio.nombreingles = form.cleaned_data['nombreingles']
                    servicio.activa = 0 if form.cleaned_data['activa'] == False else 1
                    servicio.imputar = form.cleaned_data['imputable']
                    servicio.tasa = form.cleaned_data['tasa']
                    servicio.save()
                    messages.success(request, 'Servicio modificado con èxito')
                    return HttpResponseRedirect('/servicios')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/servicios')

            return render(request, "servicios/modificar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/servicios")


@login_required(login_url='/')
def eliminar_servicio(request):

    resultado = {}
    if request.user.has_perms(["mantenimientos.delete_servicios", ]):
        if is_ajax(request):
            try:
                id = request.GET['id']
                servicio = Servicios.objects.get(id=id)
                servicio.delete()
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


@login_required(login_url="/")
def clonar_servicio(request, id_servicio):
    try:
        resultado = {}
        if not request.user.has_perms(["mantenimientos.add_servicios"]):
            resultado['resultado'] = 'No tiene permisos para realizar esta accion.'

        servicio_original = get_object_or_404(Servicios, id=id_servicio)
        ser = Servicios()
        opuesto = request.POST.get('opuesto')
        tipo = servicio_original.tipogasto
        if opuesto==True:
            if tipo == 'V':
                tipo='C'
            else:
                tipo = 'V'

        nuevo_servicio = Servicios.objects.create(
            nombre=servicio_original.nombre,
            codigo=ser.get_codigo(),
            contable=servicio_original.contable,
            tipogasto=tipo,
            nombreingles=servicio_original.nombreingles,
            activa=servicio_original.activa,
            tasa=servicio_original.tasa,
            imputar=servicio_original.imputar,
        )

        return JsonResponse({'status': 'success', 'message': 'Servicio clonado con éxito'})

    except IntegrityError:
        return JsonResponse({'status': 'error', 'message': 'Error: No se pudo clonar el servicio (posible código duplicado)'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
