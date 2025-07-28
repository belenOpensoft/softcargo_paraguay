import datetime
import json
import os
import traceback
import unicodedata

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
from expaerea.forms import add_im_form, add_form, add_house, edit_form, edit_house, gastosForm, gastosFormHouse, \
    rutasFormHouse, emailsForm, embarquesFormHouse, NotasForm, rutasFormMaster
from expaerea.models import Master, ExportEmbarqueaereo, VEmbarqueaereo,VEmbarqueaereoDirecto, ExportAttachhijo, ExportCargaaerea, \
    ExportServiceaereo, ExportConexaerea, ExportFaxes
from impomarit.views.logs_general import obtener_logs_generico
from seguimientos.forms import archivosForm, pdfForm


@login_required(login_url='/')
def master_expo_aerea(request):
    try:
        if request.user.has_perms(["expaerea.view_master",]):
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
            return render(request, 'expaerea/grilla_datos.html',{
                'form': add_form(),
                'form_house': add_house(),
                'form_search_master': add_im_form(),
                'form_edit_master':edit_form(),
                'form_edit_house': edit_house(),
                'opciones_busqueda': opciones_busqueda,
                'form_gastos': gastosForm(),
                'form_gastos_house': gastosFormHouse(),
                'form_rutas_house': rutasFormHouse(),
                'form_rutas_master': rutasFormMaster(),
                'form_emails': emailsForm(),
                'form_embarques_house': embarquesFormHouse(),
                'form_archivos': archivosForm(),
                'form_pdf': pdfForm(),
                'form_notas': NotasForm(initial={'fecha':datetime.datetime.now().strftime('%Y-%m-%d')}),


            })
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')

@login_required(login_url='/login')
def house_importacion_maritima(request):
    try:
        if request.user.has_perms(["expaerea.view_vembarqueaereo",]):
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
            return render(request, 'expaerea/grilla_datos_hd.html',{
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
                'form_notas': NotasForm(initial={'fecha':datetime.datetime.now().strftime('%Y-%m-%d')}),


            })
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')

param_busqueda = {
    1: 'numero__icontains',
    2: 'llegada__icontains',
    3: 'seguimientos__icontains',
    4: 'transportista__icontains',
    5: 'awb__icontains',
    6: 'agente__icontains',
    7: 'consignatario__icontains',
    8: 'origen__icontains',
    9: 'destino__icontains',
    10: 'status__icontains',
}

columns_table = {
    0: 'numero',
    1: 'numero',
    2: 'llegada',
    3: 'seguimientos',
    4: 'transportista',
    5: 'awb',
    6: 'agente',
    7: 'consignatario',
    8: 'origen',
    9: 'destino',
    10: 'status',
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
            '9': request.GET['columns[9][search][value]'],
            '10': request.GET['columns[10][search][value]'],
        }
        filtro = get_argumentos_busqueda(**args)

        awb_filter_json = simplejson.loads(request.GET['awb_filter'])
        if awb_filter_json:
            regex = '|'.join(awb_filter_json)
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
            registro_json.append('' if registro.llegada is None else str(registro.llegada)[:10])
            registro_json.append('' if registro.seguimientos is None else str(registro.seguimientos))

            registro_json.append('' if registro.transportista is None else str(registro.transportista))
            registro_json.append('' if registro.awb is None else str(registro.awb))
            registro_json.append('' if registro.agente is None else str(registro.agente))
            registro_json.append('' if registro.embarcador is None else str(registro.embarcador))
            registro_json.append('' if registro.origen is None else str(registro.origen))
            registro_json.append('' if registro.destino is None else str(registro.destino))
            registro_json.append('' if registro.status is None else str(registro.status))
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

def source_embarque_aereo_full(request, master):
    if is_ajax(request):
        # Buscar todos los embarques en ExportEmbarqueaereo con el awb igual a master
        try:
            embarques = ExportEmbarqueaereo.objects.filter(awb=master)
            numeros = [embarque.numero for embarque in embarques]  # Obtener una lista de números

            # Usar los números para buscar registros en ExportCargaaerea
            registros_cargaaerea = ExportCargaaerea.objects.filter(numero__in=numeros)
            vector_registros = list(registros_cargaaerea.values()) if registros_cargaaerea.exists() else []

            # Preparar el resultado
            resultado = {
                'recordsFiltered': embarques.count(),  # Total de registros en ExportEmbarqueaereo
                'data': vector_registros
            }

            return JsonResponse(resultado)

        except ExportEmbarqueaereo.DoesNotExist:
            # Si no se encuentra el embarque, devolver mensaje de error
            return JsonResponse({
                'success': False,
                'message': 'No se encontró un embarque con ese master.'
            })

    else:
        return HttpResponse("fail", content_type="application/json")

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
            registro_json.append('' if registro.hawb is None else str(registro.hawb))  # Estado 11

            archivos = ExportAttachhijo.objects.filter(numero=registro.numero).count()
            embarques = ExportCargaaerea.objects.filter(numero=registro.numero).count()
            #envases = ImportEnvases.objects.filter(numero=registro.numero).count()
            gastos = ExportServiceaereo.objects.filter(numero=registro.numero).count()
            rutas = ExportConexaerea.objects.filter(numero=registro.numero)
            notas = ExportFaxes.objects.filter(numero=registro.numero).count()
            vuelo = ''
            for r in rutas:
                if r.destino == registro.destino:
                    vuelo += ' ' + r.vuelo
            registro_json.append(archivos)
            registro_json.append(embarques)
            registro_json.append(0)
            registro_json.append(gastos)
            registro_json.append(rutas.count())
            registro_json.append(notas)
            registro_json.append(registro.consignatario_id)
            registro_json.append(registro.seguimiento) #19
            registro_json.append(registro.consignatario_codigo)
            registro_json.append('' if registro.etd is None else str(registro.etd)[:10])  #21
            registro_json.append('' if registro.eta is None else str(registro.eta)[:10])  #22
            registro_json.append('' if registro.etd is None else str(registro.etd.strftime('%d/%m/%Y')))  #23
            registro_json.append('' if registro.eta is None else str(registro.eta.strftime('%d/%m/%Y')))  #24
            registro_json.append(vuelo)#25
            registro_json.append('' if registro.agente is None else str(registro.agente))  # 26
            registro_json.append('' if registro.transportista is None else str(registro.transportista))  # 27
            registro_json.append('' if registro.embarcador is None else str(registro.embarcador))  # 28
            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)

def source_embarque_consolidado_old(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        draw = int(request.GET.get('draw', 1))

        # Mapeo de columnas
        columnas = [
            'id', 'etd', 'eta', 'numero', 'seguimiento','consignatario', 'origen', 'destino',
            'status', 'posicion', 'operacion', 'awb', 'hawb', 'vapor', 'notificar_agente', 'notificar_cliente'
        ]

        # Filtrar registros en base a la búsqueda
        registros = VEmbarqueaereo.objects.filter(consolidado=1)

        # Aplicar búsqueda por columna
        for index, column in enumerate(columnas):
            search_value = request.GET.get(f'columns[{index}][search][value]', '').strip()
            if search_value:
                filtros = {f"{column}__icontains": search_value}
                registros = registros.filter(**filtros)

        # Ordenar registros (aplicamos el orden enviado por DataTables)
        order_column_index = int(request.GET.get('order[0][column]', 0))  # Índice de la columna
        order_dir = request.GET.get('order[0][dir]', 'asc')  # Dirección del orden

        if order_column_index < len(columnas):
            order_column = columnas[order_column_index]  # Obtener el nombre de la columna
            if order_dir == 'desc':
                order_column = f"-{order_column}"  # Prefijar con '-' para orden descendente
            registros = registros.order_by(order_column)

        # Obtener el número total de registros y registros filtrados
        total_records = VEmbarqueaereo.objects.filter(consolidado=1).count()
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


def source_embarque_consolidado(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        draw = int(request.GET.get('draw', 1))

        # Mapeo de columnas
        columnas = [
            'seguimiento',  # 1 - N° Seguimiento
            'etd',  # 2 - ETD
            'numero',  # 3 - N° Embarque
            'vuelo',  # 4 - Vapor
            'awb',  # 5 - Master
            'hawb',  # 6 - House
            'embarcador',  # 7 - Embarcador
            'transportista',  # 8 - Transportista
            'agente',  # 9 - Agente
        ]

        filtros = {}
        # Aplicar búsqueda por columna
        for index, column in enumerate(columnas):
            search_value = request.GET.get(f'columns[{index}][search][value]', '').strip()
            if search_value:
                filtros[f"{column}__icontains"] = search_value
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
#mails archivo
def guardar_archivo_im(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        detalle = request.POST['detalle']
        myfile = request.FILES['archivo']
        registro = ExportAttachhijo()
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
                registro = ExportAttachhijo()

                # Obtener los campos disponibles del modelo
                campos = [f.name for f in ExportAttachhijo._meta.fields]

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
        registros = ExportAttachhijo.objects.filter(numero=numero).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data_a(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = ExportAttachhijo.objects.filter(numero=numero).count()
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
        att = ExportAttachhijo.objects.get(id=id)
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
        att = ExportAttachhijo.objects.get(id=id)
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

            registros = ExportEmbarqueaereo.objects.filter(awb=master)

            if not registros.exists():
                return JsonResponse({'status': 'error', 'message': 'No se encontraron registros con el master especificado.'}, status=404)

            for registro in registros:
                registro.fecharetiro = fecha
                registro.save()

            return JsonResponse({'status': 'success', 'message': f'Se actualizaron {registros.count()} registros correctamente.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

def buscar_registros(request):
    if request.method == "POST":
        seguimiento = request.POST.get("seguimiento", "")
        embarque = request.POST.get("embarque", "")
        reserva = request.POST.get("reserva", "")
        master = request.POST.get("master", "")
        house = request.POST.get("house", "")
        consignatario = request.POST.get("consignatario", "")
        transportista = request.POST.get("transportista", "")

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

            resultados = resultados.values_list("awb", flat=True)

        return JsonResponse({"resultados": list(resultados)}, safe=False)

    return JsonResponse({"error": "Método no permitido"}, status=400)

def source_logs(request):
    modelos_secundarios = [ExportConexaerea, ExportCargaaerea,ExportServiceaereo,ExportAttachhijo]
    return obtener_logs_generico(request, ExportEmbarqueaereo, 'numero', modelos_secundarios)