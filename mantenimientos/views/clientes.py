import datetime
import json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

from administracion_contabilidad.models import Cuentas
from mantenimientos.forms import add_cliente_form
from mantenimientos.models import Clientes as SociosComerciales, VSociosComerciales, Vendedores


@login_required(login_url='/')
def grilla_clientes(request):
    try:
        if request.user.has_perms(["mantenimientos.view_clientes",]):
            form = add_cliente_form(initial={'fecalta':datetime.datetime.now().strftime('%Y-%m-%d')})
            return render(request, 'clientes/grilla_datos.html',{'form': form,'title_page':'Mantenimiento de socios comerciales'})
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
        if request.user.has_perms(["mantenimientos.add_clientes"]):
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



@login_required(login_url="/")
def agregar_socio_comercial(request, id_socio=None):
    try:
        if not request.user.has_perms(["mantenimientos.add_clientes"]):
            raise PermissionDenied('No tiene permisos para realizar esta acción.')
        if request.method == 'GET':
            cliente = None
            if id_socio:
                cliente = get_object_or_404(SociosComerciales, id=id_socio)
                form = add_cliente_form(initial={
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
                    'emailad': cliente.emailad,
                    'emailem': cliente.emailem,
                    'emailea': cliente.emailea,
                    'emailet': cliente.emailet,
                    'emailim': cliente.emailim,
                    'emailia': cliente.emailia,
                    'emailit': cliente.emailit,
                    'activo': cliente.activo,
                    'prefijoguia': cliente.prefijoguia,
                    'tipo': cliente.tipo,
                    'vendedor': Vendedores.objects.get(codigo=cliente.vendedor).nombre if cliente.vendedor else None,
                    'vendedor_input': cliente.vendedor,
                    'plazo': cliente.plazo,
                    'limite': cliente.limite,
                    'ctavta': cliente.ctavta if cliente.ctavta else '',
                    'ctacomp': cliente.ctacomp if cliente.ctacomp else '',
                })
                tipo_accion = "Modificar"
                return JsonResponse({'status': 'success', 'form_data': form.initial})

        form = add_cliente_form()
        tipo_accion = "Agregar"

        if request.method == 'POST':
            form = add_cliente_form(request.POST)
            if form.is_valid():
                try:
                    if id_socio:
                        cliente = get_object_or_404(SociosComerciales, id=id_socio)
                        # **Actualizar cliente existente**
                        cliente.tipo = form.cleaned_data['tipo']
                        cliente.empresa = form.cleaned_data['empresa'] if form.cleaned_data['empresa'] else 'S/I'
                        cliente.razonsocial = form.cleaned_data['razonsocial'] if form.cleaned_data['razonsocial'] else 'S/I'
                        cliente.direccion = form.cleaned_data['direccion'] if form.cleaned_data['direccion'] else 'S/I'
                        cliente.localidad = form.cleaned_data['localidad'] if form.cleaned_data['localidad'] else 'S/I'
                        cliente.cpostal = form.cleaned_data['cpostal'] if form.cleaned_data['cpostal'] else 0
                        cliente.ruc = form.cleaned_data['ruc'] if form.cleaned_data['ruc'] else 0
                        cliente.telefono = form.cleaned_data['telefono'] if form.cleaned_data['telefono'] else 0
                        cliente.fecalta = form.cleaned_data['fecalta'] if form.cleaned_data['fecalta'] else None
                        cliente.contactos = form.cleaned_data['contactos'] if form.cleaned_data['contactos'] else 'S/I'
                        cliente.observaciones = form.cleaned_data['observaciones'] if form.cleaned_data['observaciones'] else 'S/I'
                        cliente.ciudad = form.cleaned_data['ciudad'] if form.cleaned_data['ciudad'] else 0
                        cliente.pais = form.cleaned_data['pais'] if form.cleaned_data['pais'] else 0
                        cliente.emailad = form.cleaned_data['emailad'] if form.cleaned_data['emailad'] else 'S/I'
                        cliente.emailem = form.cleaned_data['emailem'] if form.cleaned_data['emailem'] else 'S/I'
                        cliente.emailea = form.cleaned_data['emailea'] if form.cleaned_data['emailea'] else 'S/I'
                        cliente.emailet = form.cleaned_data['emailet'] if form.cleaned_data['emailet'] else 'S/I'
                        cliente.emailim = form.cleaned_data['emailim'] if form.cleaned_data['emailim'] else 'S/I'
                        cliente.emailia = form.cleaned_data['emailia'] if form.cleaned_data['emailia'] else 'S/I'
                        cliente.emailit = form.cleaned_data['emailit'] if form.cleaned_data['emailit'] else 'S/I'
                        cliente.activo = 0 if form.cleaned_data['activo'] == False else 1
                        cliente.tipo = form.cleaned_data['tipo'] if form.cleaned_data['tipo'] else 'S/I'
                        cliente.vendedor = form.cleaned_data['vendedor_input'] if form.cleaned_data['vendedor_input'] else 0
                        cliente.plazo = form.cleaned_data['plazo'] if form.cleaned_data['plazo'] else 0
                        cliente.limite= form.cleaned_data['limite'] if form.cleaned_data['limite'] else 0
                        cliente.ctavta =form.cleaned_data['ctavta'] if form.cleaned_data['ctavta'] else 0
                        cliente.ctacomp = form.cleaned_data['ctacomp'] if form.cleaned_data['ctacomp'] else 0
                        cliente.prefijoguia = form.cleaned_data['prefijoguia'] if form.cleaned_data['prefijoguia'] else 0

                    else:
                        # **Crear un nuevo cliente**
                        cliente = SociosComerciales(
                            tipo=form.cleaned_data['tipo'],
                            prefijoguia=form.cleaned_data['prefijoguia'],
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
                            emailad=form.cleaned_data['emailad'],
                            emailem=form.cleaned_data['emailem'],
                            emailea=form.cleaned_data['emailea'],
                            emailet=form.cleaned_data['emailet'],
                            emailim=form.cleaned_data['emailim'],
                            emailia=form.cleaned_data['emailia'],
                            emailit=form.cleaned_data['emailit'],
                            activo=0 if form.cleaned_data['activo'] == False else 1,
                            vendedor=form.cleaned_data['vendedor_input'],
                            plazo=form.cleaned_data['plazo'],
                            limite=form.cleaned_data['limite'],
                            ctavta=form.cleaned_data['ctavta'],
                            ctacomp=form.cleaned_data['ctacomp'],
                        )
                        cliente.codigo = SociosComerciales().get_codigo()

                    cliente.save()

                    return JsonResponse({'status': 'success', 'message': f'Socio comercial {tipo_accion} con éxito'})

                except IntegrityError:
                    return JsonResponse({'status': 'error', 'message': 'Error: Ya existe un socio comercial con el mismo código'})

            return JsonResponse({'status': 'error', 'message': 'Formulario inválido', 'errors': form.errors})

        return render(request, "clientes/agregar.html", {'form': form, 'title_page': f'{tipo_accion} socio comercial', 'tipo': tipo_accion})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})



@login_required(login_url='/')
def eliminar_socio_comercial(request):

    resultado = {}
    if request.user.has_perms(["mantenimientos.delete_clientes", ]):
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

