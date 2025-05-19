import json
import os
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from login.models import CorreoEnviado
from cargosystem import settings

@login_required(login_url='/login/')
def correos(request):
    try:
        if request.user.has_perms(["seguimientos.view_seguimiento", ]):
            return render(request,'correos.html',{'title_page':'Correos enviados'})
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request,str(e))
        return HttpResponseRedirect('/')

""" TABLA BUQUE """
columns_table = {
    0: 'id',
    1: 'fecha',
    2: 'tipo',
    3: 'seguimiento',
    4: 'emisor',
    5: 'correo',
    6: 'enviado_a',
    7: 'estado',
    8: 'usuario',
}
param_busqueda = {
    1: 'fecha__icontains',
    2: 'tipo__icontains',
    3: 'seguimiento__icontains',
    4: 'emisor__icontains',
    5: 'correo__icontains',
    6: 'enviado_a__icontains',
    7: 'estado__icontains',
    8: 'usuario__icontains',
}

def source_correo(request):
    if is_ajax:
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
            registros = CorreoEnviado.objects.filter(**filtro).order_by(*order)
        else:
            registros = CorreoEnviado.objects.all().order_by(*order)
        emails_filtrados = registros[start:end]
        """PREPARO DATOS"""
        resultado = {}
        data = __get_data(emails_filtrados)
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = CorreoEnviado.objects.all().count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def __get_data(emails_filtrados):
    try:
        data = []
        for email in emails_filtrados:
            email_json = []
            email_json.append(str(email.id))
            email_json.append('' if email.fecha is None else str(email.fecha))
            email_json.append('' if email.tipo is None else str(email.tipo))
            email_json.append('' if email.seguimiento is None else str(email.seguimiento))
            email_json.append('' if email.emisor is None else str(email.emisor))
            email_json.append('' if email.enviado_a is None else str(email.enviado_a)[:60])
            email_json.append('' if email.correo is None else str(email.correo))
            email_json.append('' if email.estado is None else str(email.estado))
            email_json.append('' if email.usuario is None else str(email.usuario))
            email_json.append('' if email.error is None else str(email.error))
            email_json.append('' if email.mensaje is None else str(email.mensaje))
            email_json.append('' if email.modulo is None else str(email.modulo))
            data.append(email_json)
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