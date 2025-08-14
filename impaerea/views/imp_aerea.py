import datetime
import json
import os
import traceback
import unicodedata
from itertools import chain

import simplejson
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import IntegrityError
from cargosystem import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from cargosystem.settings import RUTA_PROYECTO
from impaerea.forms import add_im_form, add_form, add_house, edit_form, edit_house, gastosForm, gastosFormHouse, \
    rutasFormHouse, emailsForm, embarquesFormHouse, NotasForm, edit_house_general
from impaerea.models import Master, ImportReservas, ImportEmbarqueaereo, VEmbarqueaereo, ImportAttachhijo, \
    ImportCargaaerea, \
    ImportServiceaereo, ImportConexaerea, ImportFaxes, VEmbarqueaereoDirecto
from impomarit.views.logs_general import obtener_logs_generico
from seguimientos.forms import archivosForm, pdfForm,aplicableForm


@login_required(login_url='/')
def master_importacion_maritima(request):
    try:
        print(request.user.get_all_permissions())
        if request.user.has_perms(["impaerea.view_master",]):
            opciones_busqueda = {
                'cliente__icontains': 'CLIENTE',
                'embarcador__icontains': 'EMBARCADOR',
                'consignatario__icontains': 'CONSIGNATARIO',
                'origen_text__icontains': 'ORIGEN',
                'destino_text__icontains': 'DESTINO',
                'awb__icontains': 'BL',
                'hawb__icontains': 'HBL',
                'vapor__icontains': 'Vapor',
                'posicion__icontains': 'Posicion',
            }
            return render(request, 'impaerea/grilla_datos.html',{
                'form': add_form(),
                'form_house': add_house(),
                'form_search_master': add_im_form(),
                'form_edit_master':edit_form(),
                'form_edit_house': edit_house(),
                'opciones_busqueda': opciones_busqueda,
                'form_gastos': gastosForm(),
                'form_gastos_house': gastosFormHouse(),
                'form_rutas_house': rutasFormHouse(),
                'form_emails': emailsForm(),
                'form_embarques_house': embarquesFormHouse(),
                'form_archivos': archivosForm(),
                'form_pdf': pdfForm(),
                'form_aplicable': aplicableForm(),
                'form_notas': NotasForm(initial={'fecha':datetime.datetime.now().strftime('%Y-%m-%d')}),

            })
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')

@login_required(login_url="/")
def house_importacion_maritima(request):
    try:
        if request.user.has_perms(["impaerea.view_vembarqueaereo",]):
            opciones_busqueda = {
                'cliente__icontains': 'CLIENTE',
                'embarcador__icontains': 'EMBARCADOR',
                'consignatario__icontains': 'CONSIGNATARIO',
                'origen_text__icontains': 'ORIGEN',
                'destino_text__icontains': 'DESTINO',
                'awb__icontains': 'BL',
                'hawb__icontains': 'HBL',
                'vapor__icontains': 'Vapor',
                'posicion__icontains': 'Posicion',
                # 'contenedores__icontains': 'Contenedor',
            }
            return render(request, 'impaerea/grilla_datos_hd.html',{
                'form_house': add_house(),
                'form_edit_house': edit_house(),
                'opciones_busqueda': opciones_busqueda,
                'form_gastos': gastosForm(),
                'form_gastos_house': gastosFormHouse(),
                'form_rutas_house': rutasFormHouse(),
                'form_emails': emailsForm(),
                'form_embarques_house': embarquesFormHouse(),
                'form_archivos': archivosForm(),
                'form_pdf': pdfForm(),
                'form_aplicable': aplicableForm(),
                'form_notas': NotasForm(initial={'fecha':datetime.datetime.now().strftime('%Y-%m-%d')}),

            })
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')

param_busqueda = {
    1: 'numero__icontains',
    2: 'seguimientos__icontains',
    3: 'llegada__icontains',
    4: 'awb__icontains',
    5: 'hawbs__icontains',
    6: 'embarcador__icontains',
    7: 'transportista__icontains',
    8: 'agente__icontains',
}
columns_table = {
    0: 'id',              # columna oculta para acciones
    1: 'numero',
    2: 'seguimientos',
    3: 'llegada',
    4: 'awb',
    5: 'hawbs',
    6: 'embarcador',
    7: 'transportista',
    8: 'agente',
}


def source_importacion_master(request):
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
        filtro = get_argumentos_busqueda(**args)

        # awb_filter_json = simplejson.loads(request.GET['awb_filter'])
        # if awb_filter_json:
        #     regex = '|'.join(awb_filter_json)
        #     filtro['awb__regex'] = regex
        partes = request.path.strip('/').split('/')
        modulo = partes[0] if partes else 'operaciones'

        # leer filtro desde sesión (no from GET)
        awb_filters = request.session.get("awb_filters", {})
        awb_list = awb_filters.get(modulo, [])

        if awb_list:
            regex = '|'.join(awb_list)
            filtro['awb__regex'] = regex

        """PROCESO FILTRO Y ORDEN BY"""
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        buscar = str(request.GET['buscar'])
        que_buscar = str(request.GET['que_buscar'])
        if len(buscar) > 0:
            filtro[que_buscar] = buscar
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        if filtro:
            registros = Master.objects.filter(**filtro).order_by(*order)
        else:
            registros = Master.objects.all().order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Master.objects.all().count()
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
            registro_json.append(str(registro.numero))
            registro_json.append('' if registro.numero is None else str(registro.numero))
            registro_json.append('' if registro.seguimientos is None else str(registro.seguimientos))
            registro_json.append('' if registro.llegada is None else str(registro.llegada)[:10])
            registro_json.append('' if registro.awb is None else str(registro.awb))
            registro_json.append('' if registro.hawbs is None else str(registro.hawbs))
            registro_json.append('' if registro.embarcador is None else str(registro.embarcador))
            registro_json.append('' if registro.transportista is None else str(registro.transportista))
            registro_json.append('' if registro.agente is None else str(registro.agente))
            # rutas = Conexaerea.objects.filter(numero=registro.numero).annotate(num_archivos=Count('id')).values('num_archivos').first()
            # archivos = Attachhijo.objects.filter(numero=registro.numero).count()
            # embarques = Cargaaerea.objects.filter(numero=registro.numero).count()
            # envases = Envases.objects.filter(numero=registro.numero).count()
            # gastos = Serviceaereo.objects.filter(numero=registro.numero).count()
            # rutas = Conexaerea.objects.filter(numero=registro.numero).count()
            # registro_json.append(archivos)
            # registro_json.append(embarques)
            # registro_json.append(envases)
            # registro_json.append(gastos)
            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)

def get_order(request, columns):
    try:
        result = []
        # Obtener la primera columna de ordenación
        order_column = request.GET.get('order[0][column]', None)
        order_dir = request.GET.get('order[0][dir]', 'asc')

        # Verificar si existe una columna de orden
        if order_column is not None:
            order = columns[int(order_column)]
            if order_dir == 'desc':
                order = '-' + order
            result.append(order)

        # Verificar si hay más columnas de ordenación (opcional)
        i = 1
        while True:
            order_column = request.GET.get(f'order[{i}][column]', None)
            if order_column is None:
                break
            order_dir = request.GET.get(f'order[{i}][dir]', 'asc')
            order = columns[int(order_column)]
            if order_dir == 'desc':
                order = '-' + order
            result.append(order)
            i += 1

        # Si no hay ninguna columna de orden específica, usar un valor por defecto
        if not result:
            result.append('numero')  # Cambia 'numero' por la columna predeterminada que prefieras

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

def source_embarque_aereo_full(request, master):
    if is_ajax(request):
        # Buscar todos los embarques en ExportEmbarqueaereo con el awb igual a master
        try:
            embarques = ImportEmbarqueaereo.objects.filter(awb=master)
            numeros = [embarque.numero for embarque in embarques]  # Obtener una lista de números

            # Usar los números para buscar registros en ExportCargaaerea
            registros_cargaaerea = ImportCargaaerea.objects.filter(numero__in=numeros)
            vector_registros = list(registros_cargaaerea.values()) if registros_cargaaerea.exists() else []

            # Preparar el resultado
            resultado = {
                'recordsFiltered': embarques.count(),  # Total de registros en ExportEmbarqueaereo
                'data': vector_registros
            }

            return JsonResponse(resultado)

        except ImportEmbarqueaereo.DoesNotExist:
            # Si no se encuentra el embarque, devolver mensaje de error
            return JsonResponse({
                'success': False,
                'message': 'No se encontró un embarque con ese master.'
            })

    else:
        return HttpResponse("fail", content_type="application/json")

#traer datos houses tabla
def source_embarque_aereo(request):
    if is_ajax(request):
        master = request.POST.get("master")
        start = int(request.POST.get('start', 0))  # Usa 0 como valor predeterminado si 'start' no está presente
        length = int(request.POST.get('length', 10))  # Usa 10 como valor predeterminado si 'length' no está presente
        draw = int(request.POST.get('draw', 1))
        registros = VEmbarqueaereo.objects.filter(awb=master)[start:start + length]
        data = get_data_embarque_aereo(registros)
        resultado = {
            'draw': draw,  # Enviar 'draw' para asegurarnos de que la solicitud y respuesta coincidan
            'recordsTotal': VEmbarqueaereo.objects.all().count(),  # Total de registros sin filtrar
            'recordsFiltered': registros.count(),  # Total de registros después del filtro
            'data': data  # Los datos filtrados
        }

        return JsonResponse(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

from django.db.models import Count, Q


def get_data_embarque_aereo_new(registros_filtrados):
    try:
        data = []

        # Preagregados por número
        archivos_dict = dict(ImportAttachhijo.objects.values('numero').annotate(c=Count('id')).values_list('numero', 'c'))
        embarques_dict = dict(ImportCargaaerea.objects.values('numero').annotate(c=Count('id')).values_list('numero', 'c'))
        gastos_dict = dict(ImportServiceaereo.objects.values('numero').annotate(c=Count('id')).values_list('numero', 'c'))
        rutas_dict = dict(ImportConexaerea.objects.values('numero').annotate(c=Count('id')).values_list('numero', 'c'))
        notas_dict = dict(ImportFaxes.objects.values('numero').annotate(c=Count('id')).values_list('numero', 'c'))

        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.numero or ''))  # Número
            registro_json.append(str(registro.fecha_embarque)[:10] if registro.fecha_embarque else '')
            registro_json.append(str(registro.fecha_retiro)[:10] if registro.fecha_retiro else '')
            registro_json.append(str(registro.numero or ''))
            registro_json.append(str(registro.consignatario or ''))
            registro_json.append(str(registro.origen or ''))
            registro_json.append(str(registro.destino or ''))
            registro_json.append(str(registro.status or ''))
            registro_json.append(str(registro.posicion or ''))
            registro_json.append(str(registro.operacion or ''))
            registro_json.append(str(registro.awb or ''))
            registro_json.append(str(registro.hawb or ''))
            registro_json.append(str(registro.notificar_agente)[:10] if registro.notificar_agente else '')
            registro_json.append(str(registro.notificar_cliente)[:10] if registro.notificar_cliente else '')

            numero = registro.numero
            registro_json.append(archivos_dict.get(numero, 0))
            registro_json.append(embarques_dict.get(numero, 0))
            registro_json.append(0)  # envases
            registro_json.append(gastos_dict.get(numero, 0))
            registro_json.append(rutas_dict.get(numero, 0))
            registro_json.append(notas_dict.get(numero, 0))

            registro_json.append(registro.consignatario_id)
            registro_json.append(registro.seguimiento)

            registro_json.append(bool(registro.aplicable and registro.aplicable != 0))
            registro_json.append(registro.consignatario_codigo)

            registro_json.append(str(registro.etd)[:10] if registro.etd else '')
            registro_json.append(str(registro.eta)[:10] if registro.eta else '')
            registro_json.append(registro.etd.strftime('%d/%m/%Y') if registro.etd else '')
            registro_json.append(registro.eta.strftime('%d/%m/%Y') if registro.eta else '')

            data.append(registro_json)

        return data

    except Exception as e:
        raise TypeError(e)



def get_data_embarque_aereo(registros_filtrados):
    try:
        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append('' if registro.numero is None else str(registro.numero))  # Fecha
            registro_json.append('' if registro.fecha_embarque is None else str(registro.fecha_embarque)[:10])  # Fecha
            registro_json.append('' if registro.fecha_retiro is None else str(registro.fecha_retiro)[:10])  # Fecha
            registro_json.append('' if registro.numero is None else str(registro.numero))  # N° Seguimiento
            registro_json.append('' if registro.consignatario is None else str(registro.consignatario))  # Cliente
            registro_json.append('' if registro.origen is None else str(registro.origen))  # Origen
            registro_json.append('' if registro.destino is None else str(registro.destino))  # Destino
            registro_json.append('' if registro.status is None else str(registro.status))  # Estado
            registro_json.append('' if registro.posicion is None else str(registro.posicion))  # Estado
            registro_json.append('' if registro.operacion is None else str(registro.operacion))  # Estado
            registro_json.append('' if registro.awb is None else str(registro.awb))  # Estado
            registro_json.append('' if registro.hawb is None else str(registro.hawb))  # Estado
            registro_json.append('' if registro.notificar_agente is None else str(registro.notificar_agente)[:10])  # Estado
            registro_json.append('' if registro.notificar_cliente is None else str(registro.notificar_cliente)[:10])  # Estado

            archivos = ImportAttachhijo.objects.filter(numero=registro.numero).count()
            embarques = ImportCargaaerea.objects.filter(numero=registro.numero).count()
            #envases = ImportEnvases.objects.filter(numero=registro.numero).count()
            gastos = ImportServiceaereo.objects.filter(numero=registro.numero).count()
            rutas = ImportConexaerea.objects.filter(numero=registro.numero)
            vuelo = ''
            for r in rutas:
                if r.destino == registro.destino:
                    vuelo += ' ' + str(r.vuelo or '') if r.vuelo is not None else ''

            notas = ImportFaxes.objects.filter(numero=registro.numero).count()
            registro_json.append(archivos)
            registro_json.append(embarques)
            registro_json.append(0)
            registro_json.append(gastos)
            registro_json.append(rutas.count())
            registro_json.append(notas)
            registro_json.append(registro.consignatario_id)
            registro_json.append(registro.seguimiento) #21
            llave = False
            if registro.aplicable and registro.aplicable != 0:
                llave = True

            registro_json.append(llave)
            registro_json.append(registro.consignatario_codigo)
            registro_json.append('' if registro.etd is None else str(registro.etd)[:10])  #24
            registro_json.append('' if registro.eta is None else str(registro.eta)[:10])  #25
            registro_json.append('' if registro.etd is None else str(registro.etd.strftime('%d/%m/%Y')))  #26
            registro_json.append('' if registro.eta is None else str(registro.eta.strftime('%d/%m/%Y')))  #27
            registro_json.append(vuelo)
            registro_json.append('' if registro.agente is None else str(registro.agente))  # 29
            registro_json.append('' if registro.transportista is None else str(registro.transportista))  # 30
            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)


def source_embarque_consolidado(request):
    try:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            draw = int(request.GET.get('draw', 1))

            # Mapeo de columnas
            columnas = [
            '',
                'seguimiento',  # 1 - N° Seguimiento
                'etd',  # 2 - ETD
                'numero',  # 3 - N° Embarque
                'vuelo',  # 4 - Vapor
                'awb',  # 5 - Master
                'hawb',  # 6 - House
                'consignatario',  # 7 - Embarcador
                'transportista',  # 8 - Transportista
                'agente',  # 9 - Agente
            ]

            filtros = {}
            # Aplicar búsqueda por columna
            for index, column in enumerate(columnas):
                search_value = request.GET.get(f'columns[{index}][search][value]', '').strip()
                if search_value:
                    filtros[f"{column}__icontains"] = search_value

            partes = request.path.strip('/').split('/')
            modulo = partes[0] if partes else 'operaciones'

            directos_filters = request.session.get("directos_filters", {})
            numeros_list = directos_filters.get(modulo, [])
            if numeros_list:
                filtros['numero__in'] = numeros_list

            if len(filtros) > 0:
                registros = VEmbarqueaereoDirecto.objects.filter(**filtros)
            else:
                registros = VEmbarqueaereoDirecto.objects.all()

            # Ordenar registros (aplicamos el orden enviado por DataTables)
            order_column_index = int(request.GET.get('order[0][column]', 0))  # Índice de la columna
            order_dir = request.GET.get('order[0][dir]', 'asc')  # Dirección del orden

            if order_column_index < len(columnas):
                order_column = columnas[order_column_index]  # Obtener el nombre de la columna
                if order_dir == 'desc':
                    order_column = f"-{order_column}"  # Prefijar con '-' para orden descendente
                registros = registros.order_by(order_column)

            # Obtener el número total de registros y registros filtrados
            total_records = VEmbarqueaereoDirecto.objects.all().count()
            filtered_records = registros.count()

            # Paginación
            registros = registros[start:start + length]

            # Preparar los datos
            data = get_data_embarque_aereo(registros)

            resultado = {
                'draw': draw,
                'recordsTotal': total_records,
                'recordsFiltered': filtered_records,
                'data': data
            }

            return JsonResponse(resultado)
        else:
            return JsonResponse({"error": "Invalid request"}, status=400)
    except Exception as e:
        return JsonResponse({'error':str(e)})
#mails archivo
def guardar_archivo_im(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        detalle = request.POST['detalle']
        myfile = request.FILES['archivo']
        registro = ImportAttachhijo()
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

def add_archivo_importado(request):
    resultado = {}
    try:
        # Recibir el número desde el POST o desde los datos JSON
        data = json.loads(request.body)
        archivos_data = data.get('data', [])#

        if isinstance(archivos_data, list):
            for envase_data in archivos_data:
                # Crear el registro del modelo Envases
                registro = ImportAttachhijo()

                # Obtener los campos disponibles del modelo
                campos = [f.name for f in ImportAttachhijo._meta.fields]

                # Iterar sobre el diccionario y asignar los valores al modelo
                for nombre_campo, valor_campo in envase_data.items():
                    if nombre_campo in campos:  # Verificar si el campo existe en el modelo
                        if valor_campo is not None and len(str(valor_campo)) > 0:
                            setattr(registro, nombre_campo, valor_campo)
                        else:
                            setattr(registro, nombre_campo, None)

                # Guardar el registro en la base de datos
                registro.save()

            # Retornar el resultado de éxito
            resultado['resultado'] = 'exito'
        else:
            resultado['resultado'] = 'Los datos enviados no son una lista válida.'

    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = f'Ocurrió un error: {str(e)}'

    # Devolver el resultado en formato JSON
    return JsonResponse(resultado)

def formatear_texto(cadena: str):
    try:
        cadena = str(unicodedata.normalize('NFKD', str(cadena)).encode('ASCII', 'ignore').upper())
        # for letra in cadena:
        #     re.match('\W', letra)
        cadena = str(cadena)[2:-1]
        return cadena.replace("  "," ")
    except Exception as e:
        raise TypeError(e)

def source_archivos(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        """PROCESO FILTRO Y ORDEN BY"""
        start = int(request.GET['start'])
        numero = request.GET['numero']
        length = int(request.GET['length'])
        end = start + length
        order = get_order_a(request, columns_table)
        """FILTRO REGISTROS"""
        registros = ImportAttachhijo.objects.filter(numero=numero).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data_a(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = ImportAttachhijo.objects.filter(numero=numero).count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def get_data_a(registros_filtrados):
    try:
        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.fecha is None else str(registro.fecha.strftime("%d/%m/%Y %H:%M")))
            registro_json.append('' if registro.archivo is None else str(registro.archivo))
            registro_json.append('' if registro.detalle is None else str(registro.detalle))
            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)

def get_order_a(request, columns):
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

def eliminar_archivo(request):
    resultado = {}
    try:
        id = request.POST['id']
        att = ImportAttachhijo.objects.get(id=id)
        ruta = str(RUTA_PROYECTO) + '/' + att.archivo
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
        att = ImportAttachhijo.objects.get(id=id)
        ruta_archivo = default_storage.path(att.archivo)
        response = FileResponse(open(ruta_archivo, 'rb'), as_attachment=True)
        archivo = att.archivo[25:]
        response['Content-Disposition'] = 'attachment; filename="' + archivo + '"'
        return response
    except Exception as e:
        resultado['resultado'] = str(e)

def modificar_fecha_retiro(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            master = data.get('master')
            fecha = data.get('fecha')

            registros = ImportEmbarqueaereo.objects.filter(awb=master)

            if not registros.exists():
                return JsonResponse({'status': 'error', 'message': 'No se encontraron registros con el master especificado.'}, status=404)

            for registro in registros:
                registro.fecharetiro = fecha
                registro.save()

            return JsonResponse({'status': 'success', 'message': f'Se actualizaron {registros.count()} registros correctamente.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

def source_logs(request):
    modelos_secundarios = [ImportConexaerea, ImportCargaaerea,ImportServiceaereo,ImportAttachhijo]
    return obtener_logs_generico(request, ImportEmbarqueaereo, 'numero', modelos_secundarios)

def buscar_registros_old(request):
    if request.method == "POST":
        seguimiento = request.POST.get("seguimiento", "")
        embarque = request.POST.get("embarque", "")
        reserva = request.POST.get("reserva", "")
        master = request.POST.get("master", "")
        house = request.POST.get("house", "")
        consignatario = request.POST.get("consignatario", "")
        transportista = request.POST.get("transportista", "")
        origen = request.POST.get("origen", "")
        posicion = request.POST.get("posicion", "")
        if reserva:
            resultados = Master.objects.filter(numero=reserva).values_list("awb", flat=True)
        else:
            resultados = VEmbarqueaereo.objects.all()

            if seguimiento:
                resultados = resultados.filter(seguimiento__icontains=seguimiento)
            if embarque:
                resultados = resultados.filter(numero__icontains=embarque)
            if master:
                resultados = resultados.filter(awb__icontains=master)
            if house:
                resultados = resultados.filter(hawb__icontains=house)
            if consignatario:
                resultados = resultados.filter(consignatario__icontains=consignatario)
            if transportista:
                resultados = resultados.filter(transportista__icontains=transportista)
            if posicion:
                resultados = resultados.filter(posicion__icontains=posicion)
            if origen:
                resultados = resultados.filter(origen__icontains=origen.upper())
            resultados = resultados.values_list("awb", flat=True)

        return JsonResponse({"resultados": list(resultados)}, safe=False)

    return JsonResponse({"error": "Método no permitido"}, status=400)

def buscar_registros(request):
    if request.method == "POST":
        seguimiento    = (request.POST.get("seguimiento") or "").strip()
        embarque       = (request.POST.get("embarque") or "").strip()
        reserva        = (request.POST.get("reserva") or "").strip()
        master         = (request.POST.get("master") or "").strip()
        house          = (request.POST.get("house") or "").strip()
        consignatario  = (request.POST.get("consignatario") or "").strip()
        transportista  = (request.POST.get("transportista") or "").strip()
        origen         = (request.POST.get("origen") or "").strip()
        posicion       = (request.POST.get("posicion") or "").strip()

        if reserva:
            resultados_qs = Master.objects.filter(numero=reserva).values_list("awb", flat=True)
        else:
            resultados_qs = VEmbarqueaereo.objects.all()
            if seguimiento:   resultados_qs = resultados_qs.filter(seguimiento__icontains=seguimiento)
            if embarque:      resultados_qs = resultados_qs.filter(numero__icontains=embarque)
            if master:        resultados_qs = resultados_qs.filter(awb__icontains=master)
            if house:         resultados_qs = resultados_qs.filter(hawb__icontains=house)
            if consignatario: resultados_qs = resultados_qs.filter(consignatario__icontains=consignatario)
            if transportista: resultados_qs = resultados_qs.filter(transportista__icontains=transportista)
            if posicion:      resultados_qs = resultados_qs.filter(posicion__icontains=posicion)
            if origen:        resultados_qs = resultados_qs.filter(origen__icontains=origen.upper())
            resultados_qs = resultados_qs.values_list("awb", flat=True)

        # normalizar/deduplicar y convertir a lista (para sesión)
        awb_list = list({(awb or "").strip() for awb in resultados_qs if awb})

        # módulo desde la ruta (/importacion_maritima/buscar_registros/ -> "importacion_maritima")
        partes = request.path.strip('/').split('/')
        modulo = partes[0] if partes else 'operaciones'

        # guardar en sesión, namespaced por módulo
        filters = request.session.get("awb_filters", {})
        filters[modulo] = awb_list
        request.session["awb_filters"] = filters
        request.session.modified = True

        return JsonResponse({"resultados": awb_list}, safe=False)

    return JsonResponse({"error": "Método no permitido"}, status=400)


def get_datos_aplicables(request):
    numero = request.GET.get('numero')

    try:
        embarque = ImportEmbarqueaereo.objects.get(numero=numero)
        cargas = ImportCargaaerea.objects.filter(numero=numero)

        total_bruto = 0
        total_volumen = 0

        for c in cargas:
            total_bruto += c.bruto or 0

            if c.medidas:
                partes = str(c.medidas).split('*')
                if len(partes) == 3:
                    try:
                        largo = float(partes[0]) or 0
                        ancho = float(partes[1]) or 0
                        alto = float(partes[2]) or 0
                        cbm = largo * ancho * alto
                        total_volumen += cbm
                    except ValueError:
                        pass

        data = {
            'tarifacompra': float(embarque.tarifacompra or 0),
            'tarifaventa': float(embarque.tarifaventa or 0),
            'aplicable': float(embarque.aplicable or 0),
            'muestroflete': 0,
            'bruto': round(total_bruto, 2),
            'volumen': round(total_volumen, 2),
            'status': 'ok'
        }

    except ImportEmbarqueaereo.DoesNotExist:
        data = {'status': 'error', 'mensaje': 'Embarque no encontrado'}

    return JsonResponse(data)
def guardar_aplicable(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            numero = data.get('numero')

            seg = ImportEmbarqueaereo.objects.get(numero=numero)
            seg.tarifacompra = data.get('tarifacompra') or None
            seg.tarifaventa = data.get('tarifaventa') or None
            seg.aplicable = data.get('aplicable') or None
            #seg.muestroflete = data.get('muestroflete') or None

            seg.save()

            return JsonResponse({'status': 'ok'})
        except ImportEmbarqueaereo.DoesNotExist:
            return JsonResponse({'status': 'error', 'mensaje': 'Embarque no encontrado'})

    return JsonResponse({'status': 'error', 'mensaje': 'Método no permitido'})


def buscar_registros_directos(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=400)

    seguimiento    = (request.POST.get("seguimiento") or "").strip()
    master         = (request.POST.get("master") or "").strip()
    house          = (request.POST.get("house") or "").strip()
    consignatario  = (request.POST.get("consignatario") or "").strip()
    transportista  = (request.POST.get("transportista") or "").strip()
    origen         = (request.POST.get("origen") or "").strip()
    posicion       = (request.POST.get("posicion") or "").strip()

    qs = VEmbarqueaereoDirecto.objects.all()
    if seguimiento:   qs = qs.filter(seguimiento__icontains=seguimiento)
    if master:        qs = qs.filter(awb__icontains=master)
    if house:         qs = qs.filter(hawb__icontains=house)
    if consignatario: qs = qs.filter(consignatario__icontains=consignatario)
    if transportista: qs = qs.filter(transportista__icontains=transportista)
    if posicion:      qs = qs.filter(posicion__icontains=posicion)
    if origen:        qs = qs.filter(origen__icontains=origen.upper())

    # Tomamos los NÚMEROS (no AWB) y deduplicamos
    numeros_list = list(set(qs.values_list("numero", flat=True)))

    # Namespace por módulo (primer segmento de la ruta)
    partes = request.path.strip('/').split('/')
    modulo = partes[0] if partes else 'operaciones'

    # Guardar en sesión bajo otra key para no pisar AWB
    directos_filters = request.session.get("directos_filters", {})
    directos_filters[modulo] = numeros_list
    request.session["directos_filters"] = directos_filters
    request.session.modified = True

    # Podés devolver la lista (si tu front la usa) o solo métricas
    return JsonResponse({"resultados": numeros_list, "count": len(numeros_list)}, safe=False)

#grilla de embarques general
@login_required(login_url='/')
def embarques_importacion_aerea(request):
    try:

        if request.user.has_perms(["impaerea.view_master", ]):

            return render(request, 'impaerea/grilla_datos_general.html', {
                'form': add_form(),
                'form_house': add_house(),
                'form_search_master': add_im_form(),
                'form_edit_master': edit_form(),
                'form_edit_house': edit_house(),
                'form_edit_house_general': edit_house_general(),
                'form_gastos': gastosForm(),
                'form_gastos_house': gastosFormHouse(),
                'form_rutas_house': rutasFormHouse(),
                'form_emails': emailsForm(),
                'form_embarques_house': embarquesFormHouse(),
                'form_archivos': archivosForm(),
                'form_pdf': pdfForm(),
                'form_notas': NotasForm(initial={'fecha':datetime.datetime.now().strftime('%Y-%m-%d')}),
                'form_aplicable': aplicableForm(),
            })

        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')

param_busqueda_general = {
    0: 'numero',
    1: 'seguimiento__icontains',
    2: 'eta__icontains',
    3: 'vuelo__icontains',
    4: 'awb__icontains',
    5: 'hawb__icontains',
    6: 'consignatario__icontains',
    7: 'transportista__icontains',
    8: 'agente__icontains',
    9: 'posicion__icontains',
    10: 'numero_embarque__icontains',
    11: 'numero_reserva__icontains',
    12: 'id_reserva__icontains',
}
columns_table_general = {
    0: 'numero',
    1: 'seguimiento',
    2: 'eta',
    3: 'vuelo',
    4: 'awb',
    5: 'hawb',
    6: 'consignatario',
    7: 'transportista',
    8: 'agente',
    9: 'posicion',
    10: 'numero_embarque',
    11: 'numero_reserva',
    12: 'id_reserva',
}

def source_embarques_general(request):
    if is_ajax(request):
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
            '12': request.GET['columns[12][search][value]'],
        }
        filtro = get_argumentos_busqueda_general(**args)

        start = int(request.GET['start'])
        length = int(request.GET['length'])

        # nums_raw = request.GET.get('numeros')
        # try:
        #     numeros_json = json.loads(nums_raw) if nums_raw else []
        # except (TypeError, ValueError):
        #     numeros_json = []
        #
        # if numeros_json:  # solo si hay algo
        #     filtro['numero__in'] = numeros_json
        partes = request.path.strip('/').split('/')
        modulo = partes[0] if partes else 'operaciones'

        general_filters = request.session.get("general_filters", {})
        numeros_list = general_filters.get(modulo, [])

        if numeros_list:
            filtro['numero__in'] = numeros_list

        end = start + length
        order = get_order(request, columns_table_general)

        # Obtener registros de ambas vistas
        if filtro:
            registros1 = VEmbarqueaereo.objects.filter(**filtro).order_by(*order)
            registros2 = VEmbarqueaereoDirecto.objects.filter(**filtro).order_by(*order)
        else:
            registros1 = VEmbarqueaereo.objects.all().order_by(*order)
            registros2 = VEmbarqueaereoDirecto.objects.all().order_by(*order)

        # Eliminar duplicados por ID
        ids_vistos = set()
        registros = []
        for r in chain(registros1, registros2):
            if r.numero not in ids_vistos:
                registros.append(r)
                ids_vistos.add(r.numero)

        reservas = ImportReservas.objects.all().values_list('awb', 'numero')

        mapa_reservas = {
            (awb or '').strip(): {
                'numero_reserva': numero_reserva,
                'reserva_id': numero_reserva
            }
            for awb, numero_reserva in reservas if awb
        }

        # Construir respuesta
        resultado = {
            'data': get_data_general(registros[start:end], mapa_reservas),
            'length': length,
            'draw': request.GET['draw'],
            'recordsTotal': len(registros),
            'recordsFiltered': len(registros),
        }
        data_json = json.dumps(resultado)

    else:
        data_json = 'fail'

    return HttpResponse(data_json, content_type="application/json")

def get_argumentos_busqueda_general(**kwargs):
    try:
        result = {}
        for row in kwargs:
            if len(kwargs[row]) > 0:
                result[param_busqueda_general[int(row)]] = kwargs[row]
        return result
    except Exception as e:
        raise TypeError(e)

def get_data_general(registros_filtrados,mapa_reservas):
    try:
        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.numero))
            registro_json.append('' if registro.seguimiento is None else str(registro.seguimiento))
            registro_json.append('' if registro.eta is None else str(registro.eta)[:10])
            rutas = ImportConexaerea.objects.filter(numero=registro.numero)
            vuelo = ''
            for r in rutas:
                if r.destino == registro.destino:
                    vuelo += ' ' + str(r.vuelo or '') if r.vuelo is not None else ''
            registro_json.append('' if vuelo is None else str(vuelo))
            registro_json.append('' if registro.awb is None else str(registro.awb))
            registro_json.append('' if registro.hawb is None else str(registro.hawb))
            registro_json.append('' if registro.consignatario is None else str(registro.consignatario))
            registro_json.append('' if registro.transportista is None else str(registro.transportista))
            registro_json.append('' if registro.agente is None else str(registro.agente))
            registro_json.append('' if registro.posicion is None else str(registro.posicion))
            registro_json.append('' if registro.numero is None else str(registro.numero))
            awb = (registro.awb or '').strip()
            reserva_data = mapa_reservas.get(awb, {})
            nro_reserva = reserva_data.get('numero_reserva', '')
            id_reserva = reserva_data.get('reserva_id', '')

            registro_json.append('' if nro_reserva is None else str(nro_reserva))
            registro_json.append('' if id_reserva is None else str(id_reserva))

            archivos = ImportAttachhijo.objects.filter(numero=registro.numero).count()
            embarques = ImportCargaaerea.objects.filter(numero=registro.numero).count()
            gastos = ImportServiceaereo.objects.filter(numero=registro.numero).count()
            rutas = ImportConexaerea.objects.filter(numero=registro.numero).count()
            notas = ImportFaxes.objects.filter(numero=registro.numero).count()

            registro_json.append(archivos) #12
            registro_json.append(embarques) #13
            registro_json.append(gastos) #14
            registro_json.append(rutas) #15
            registro_json.append(notas) #16
            llave = False
            if registro.aplicable and registro.aplicable != 0:
                llave = True

            registro_json.append(llave)#17
            if id_reserva:
                registro_json.append('MASTER')
            else:
                registro_json.append('DIRECTO')

            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)

def buscar_registros_general(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=400)

    seguimiento    = (request.POST.get("seguimiento") or "").strip()
    master         = (request.POST.get("master") or "").strip()
    house          = (request.POST.get("house") or "").strip()
    consignatario  = (request.POST.get("consignatario") or "").strip()
    transportista  = (request.POST.get("transportista") or "").strip()
    origen         = (request.POST.get("origen") or "").strip()
    posicion       = (request.POST.get("posicion") or "").strip()

    q = Q()
    if seguimiento:   q &= Q(seguimiento__icontains=seguimiento)
    if master:        q &= Q(awb__icontains=master)
    if house:         q &= Q(hawb__icontains=house)
    if consignatario: q &= Q(consignatario__icontains=consignatario)
    if transportista: q &= Q(transportista__icontains=transportista)
    if posicion:      q &= Q(posicion__icontains=posicion)
    if origen:        q &= Q(origen__icontains=origen)

    # Query de números (enteros) en ambas vistas y unión sin duplicados
    qs1 = VEmbarqueaereo.objects.filter(q).values_list("numero", flat=True)
    qs2 = VEmbarqueaereoDirecto.objects.filter(q).values_list("numero", flat=True)
    resultados_qs = qs1.union(qs2)

    # A lista (serializable) y sin None
    numeros_list = [n for n in resultados_qs if n is not None]

    # Módulo por primer segmento de la ruta (ej: "importacion_maritima")
    partes = request.path.strip('/').split('/')
    modulo = partes[0] if partes else 'operaciones'

    # Guardar en sesión bajo un namespace propio para “general”
    general_filters = request.session.get("general_filters", {})
    general_filters[modulo] = numeros_list
    request.session["general_filters"] = general_filters
    request.session.modified = True

    return JsonResponse({"resultados": numeros_list, "count": len(numeros_list)}, safe=False)

#grilla de embarques general