import datetime
import json
import os
import traceback
import unicodedata

import simplejson
from django.core.files.storage import default_storage
from django.db import IntegrityError
from cargosystem import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404, FileResponse
from django.shortcuts import render

from cargosystem.settings import RUTA_PROYECTO
from impomarit.views.logs_general import obtener_logs_generico
from impterrestre.forms import add_im_form, add_form, add_house, edit_form, edit_house, gastosForm, gastosFormHouse, \
    rutasFormHouse, emailsForm, envasesFormHouse, embarquesFormHouse, NotasForm
from impterrestre.models import Master, ImpterraReservas, ImpterraEmbarqueaereo, VEmbarqueaereo, ImpterraAttachhijo, \
    ImpterraCargaaerea, ImpterraEnvases, \
    ImpterraServiceaereo, ImpterraConexaerea, ImpterraFaxes, VEmbarqueaereoDirecto
from seguimientos.forms import archivosForm, pdfForm


@login_required(login_url='/')
def master_importacion_maritima(request):
    try:
        if request.user.has_perms(["impterrestre.view_master",]):
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
            return render(request, 'impoterrestre/grilla_datos.html',{
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
                'form_envases_house': envasesFormHouse(),
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

@login_required(login_url="/")
def house_importacion_maritima(request):
    try:
        if request.user.has_perms(["impterrestre.view_vembarqueaereo",]):
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
            return render(request, 'impoterrestre/grilla_datos_hd.html',{
                'form_house': add_house(),
                'form_edit_house': edit_house(),
                'opciones_busqueda': opciones_busqueda,
                'form_gastos': gastosForm(),
                'form_gastos_house': gastosFormHouse(),
                'form_rutas_house': rutasFormHouse(),
                'form_emails': emailsForm(),
                'form_envases_house': envasesFormHouse(),
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
        cronologia = [
            'fecha',
            'estimadorecepcion',
            'recepcion',
            'fecemision',
            'fecseguro',
            'fecdocage',
            'loadingdate',
            'arriboreal',
            'fecaduana',
            'pagoenfirme',
            'vencimiento',
            'etd',
            'eta',
            'fechaonhand',
            'fecrecdoc',
            'recepcionprealert',
            'lugar',
            'nroseguro',
            'bltipo',
            'manifiesto',
            'credito',
            'prima',
            'observaciones',

        ]
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
            embarques = ImpterraEmbarqueaereo.objects.filter(awb=master)
            numeros = [embarque.numero for embarque in embarques]  # Obtener una lista de números

            # Usar los números para buscar registros en ExportCargaaerea
            registros_cargaaerea = ImpterraCargaaerea.objects.filter(numero__in=numeros)
            vector_registros = list(registros_cargaaerea.values()) if registros_cargaaerea.exists() else []

            # Preparar el resultado
            resultado = {
                'recordsFiltered': embarques.count(),  # Total de registros en ExportEmbarqueaereo
                'data': vector_registros
            }

            return JsonResponse(resultado)

        except ImpterraEmbarqueaereo.DoesNotExist:
            # Si no se encuentra el embarque, devolver mensaje de error
            return JsonResponse({
                'success': False,
                'message': 'No se encontró un embarque con ese master.'
            })

    else:
        return HttpResponse("fail", content_type="application/json")

def source_logs(request):
    modelos_secundarios = [ImpterraConexaerea, ImpterraCargaaerea,ImpterraServiceaereo,ImpterraAttachhijo,ImpterraEnvases]
    return obtener_logs_generico(request, ImpterraEmbarqueaereo, 'numero', modelos_secundarios)

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

            archivos = ImpterraAttachhijo.objects.filter(numero=registro.numero).count() #14
            embarques = ImpterraCargaaerea.objects.filter(numero=registro.numero).count()
            envases = ImpterraEnvases.objects.filter(numero=registro.numero).count()
            gastos = ImpterraServiceaereo.objects.filter(numero=registro.numero).count()
            rutas = ImpterraConexaerea.objects.filter(numero=registro.numero).count() #18
            notas = ImpterraFaxes.objects.filter(numero=registro.numero).count() #18
            registro_json.append(archivos)
            registro_json.append(embarques)
            registro_json.append(0)
            registro_json.append(gastos)
            registro_json.append(rutas)
            registro_json.append(notas)
            registro_json.append(registro.consignatario_id)
            registro_json.append(registro.seguimiento) #20
            registro_json.append(registro.consignatario_codigo)
            registro_json.append('' if registro.etd is None else str(registro.etd)[:10])  #23
            registro_json.append('' if registro.eta is None else str(registro.eta)[:10])  #24
            registro_json.append('' if registro.etd is None else str(registro.etd.strftime('%d/%m/%Y')))  #25
            registro_json.append('' if registro.eta is None else str(registro.eta.strftime('%d/%m/%Y')))  #26

            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)


def source_embarque_consolidado(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        draw = int(request.GET.get('draw', 1))

        # Mapeo de columnas
        columnas = [
            'id', 'etd', 'eta', 'numero', 'seguimiento', 'consignatario', 'origen', 'destino',
            'status', 'posicion', 'operacion', 'awb', 'hawb', 'vapor', 'notificar_agente', 'notificar_cliente'
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

#mails archivo
def guardar_archivo_im(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        detalle = request.POST['detalle']
        myfile = request.FILES['archivo']
        registro = ImpterraAttachhijo()
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
                registro = ImpterraAttachhijo()

                # Obtener los campos disponibles del modelo
                campos = [f.name for f in ImpterraAttachhijo._meta.fields]

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
        registros = ImpterraAttachhijo.objects.filter(numero=numero).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data_a(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = ImpterraAttachhijo.objects.filter(numero=numero).count()
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
        result.append('numero')
        return result
    except Exception as e:
        raise TypeError(e)

def eliminar_archivo(request):
    resultado = {}
    try:
        id = request.POST['id']
        att = ImpterraAttachhijo.objects.get(id=id)
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
        att = ImpterraAttachhijo.objects.get(id=id)
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

            registros = ImpterraEmbarqueaereo.objects.filter(awb=master)

            if not registros.exists():
                return JsonResponse({'status': 'error', 'message': 'No se encontraron registros con el master especificado.'}, status=404)

            for registro in registros:
                registro.fecharetiro = fecha
                registro.save()

            return JsonResponse({'status': 'success', 'message': f'Se actualizaron {registros.count()} registros correctamente.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

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

def buscar_registros_directos_old(request):
    if request.method == "POST":
        seguimiento = request.POST.get("seguimiento", "")
        master = request.POST.get("master", "")
        house = request.POST.get("house", "")
        consignatario = request.POST.get("consignatario", "")
        transportista = request.POST.get("transportista", "")
        origen = request.POST.get("origen", "")
        posicion = request.POST.get("posicion", "")

        resultados = VEmbarqueaereoDirecto.objects.all()

        if seguimiento:
            resultados = resultados.filter(seguimiento__icontains=seguimiento)
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
        resultados = resultados.values_list("numero", flat=True)

        return JsonResponse({"resultados": list(resultados)}, safe=False)

    return JsonResponse({"error": "Método no permitido"}, status=400)

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
