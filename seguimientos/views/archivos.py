import datetime
import json
import os
import traceback
import unicodedata

import simplejson
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage, default_storage
from django.db import IntegrityError
from django.http import HttpResponse, FileResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from cargosystem import settings
from cargosystem.settings import RUTA_PROYECTO
from seguimientos.forms import archivosForm
from seguimientos.models import Cargaaerea, VCargaaerea, Attachhijo, Seguimiento

""" TABLA PUERTO """
columns_table = {
    1: 'id',
    2: 'archivo',
    3: 'detalle',
    4: 'fecha',
}


def source_archivos(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        """PROCESO FILTRO Y ORDEN BY"""
        start = int(request.GET['start'])
        numero = request.GET['numero']
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        registros = Attachhijo.objects.filter(numero=numero).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Attachhijo.objects.filter(numero=numero).count()
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
            registro_json.append('' if registro.fecha is None else str(registro.fecha.strftime("%d/%m/%Y %H:%M")))
            registro_json.append('' if registro.archivo is None else str(registro.archivo))
            registro_json.append('' if registro.detalle is None else str(registro.detalle))
            usuario = ''
            if registro.idusuario is not None:
                user = User.objects.filter(id=registro.idusuario)
                if user.count() > 0:
                    usuario = user[0].first_name + ' ' + user[0].last_name
            registro_json.append(usuario)
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

def is_ajax(request):
    try:
        req = request.META.get('HTTP_X_REQUESTED_WITH')
        # return req == 'XMLHttpRequest'
        return True
    except Exception as e:
        messages.error(request,e)
@csrf_exempt
def guardar_archivo(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        detalle = request.POST['detalle']
        myfile = request.FILES['archivo']
        registro = Attachhijo()
        registro.idusuario = request.user.id
        from django.core.files.storage import default_storage
        nombre = formatear_texto(myfile.name).replace(' ', '')
        ruta = settings.RUTA_ARCHIVOS + nombre
        ruta = default_storage.save(ruta, myfile)
        registro.archivo = ruta
        registro.numero = numero
        registro.detalle = detalle
        registro.fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        registro.save()
        resultado['resultado'] = 'exito'
        resultado['numero'] = str(registro.numero)
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
        print(e)
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        resultado['resultado'] = str(e)
        print(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)
def formatear_texto(cadena: str):
    try:
        cadena = str(unicodedata.normalize('NFKD', str(cadena)).encode('ASCII', 'ignore').upper())
        # for letra in cadena:
        #     re.match('\W', letra)
        cadena = str(cadena)[2:-1]
        return cadena.replace("  "," ")
    except Exception as e:
        raise TypeError(e)


def eliminar_archivo(request):
    resultado = {}
    try:
        id = request.POST['id']
        att = Attachhijo.objects.get(id=id)
        ruta = str(RUTA_PROYECTO) + '/' + att.archivo.url
        if os.path.isfile(ruta):
            os.remove(ruta)
        att.delete()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def descargar_archivo(request,id):
    resultado = {}
    try:
        # id = request.POST['id']
        att = Attachhijo.objects.get(id=id)
        ruta_archivo = default_storage.path(att.archivo.url[7:])
        response = FileResponse(open(ruta_archivo, 'rb'), as_attachment=True)
        archivo = att.archivo.url[25:]
        response['Content-Disposition'] = 'attachment; filename="' + archivo + '"'
        return response
    except Exception as e:
        resultado['resultado'] = str(e)
