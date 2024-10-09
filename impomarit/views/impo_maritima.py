import datetime
import json
import os
import traceback
import unicodedata

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
from impomarit.forms import add_im_form, add_form, add_house, edit_form, edit_house, gastosForm, gastosFormHouse, \
    rutasFormHouse, emailsForm, envasesFormHouse, embarquesFormHouse
from impomarit.models import Master, Reservas, Embarqueaereo, VEmbarqueaereo, Attachhijo
from seguimientos.forms import archivosForm


@login_required(login_url='/')
def master_importacion_maritima(request):
    try:
        if request.user.has_perms(["mantenimientos.view_seguimientos",]):
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
            return render(request, 'impormarit/grilla_datos.html',{
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

            })
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')
def house_importacion_maritima(request):
    try:
        if request.user.has_perms(["mantenimientos.view_seguimientos",]):
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
            return render(request, 'impormarit/grilla_datos_hd.html',{
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
            })
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')

param_busqueda = {
    1: 'numero__icontains',
    2: 'llegada__icontains',
    3: 'transportista__icontains',
    4: 'awb__icontains',
    5: 'agente__icontains',
    6: 'consignatario__icontains',
    7: 'armador__icontains',
    8: 'vapor__icontains',
    9: 'origen__icontains',
    10: 'destino__icontains',
    11: 'status__icontains',
}

columns_table = {
    0: 'id',
    1: 'numero',
    2: 'llegada',
    3: 'transportista',
    4: 'awb',
    5: 'agente',
    6: 'consignatario',
    7: 'armador',
    8: 'vapor',
    9: 'origen',
    10: 'destino',
    11: 'status',
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
            '11': request.GET['columns[11][search][value]'],
        }
        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
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
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.numero is None else str(registro.numero))
            registro_json.append('' if registro.llegada is None else str(registro.llegada)[:10])
            registro_json.append('' if registro.transportista is None else str(registro.transportista))
            registro_json.append('' if registro.awb is None else str(registro.awb))
            registro_json.append('' if registro.agente is None else str(registro.agente))
            registro_json.append('' if registro.embarcador is None else str(registro.embarcador))
            registro_json.append('' if registro.armador is None else str(registro.armador))
            registro_json.append('' if registro.vapor is None else str(registro.vapor))
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



#traer datos houses tabla
def source_embarque_aereo(request, master):
    if is_ajax(request):
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
            registro_json.append('' if registro.id is None else str(registro.id))  # Fecha
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
            registro_json.append('' if registro.vapor is None else str(registro.vapor))  # Estado
            registro_json.append('' if registro.notificar_agente is None else str(registro.notificar_agente)[:10])  # Estado
            registro_json.append('' if registro.notificar_cliente is None else str(registro.notificar_cliente)[:10])  # Estado


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
            'id', 'fecha_embarque', 'fecha_retiro', 'numero', 'consignatario', 'origen', 'destino',
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

#mails archivo
def guardar_archivo_im(request):
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

def add_archivo_importado(request):
    resultado = {}
    try:
        # Recibir el número desde el POST o desde los datos JSON
        data = json.loads(request.body)
        archivos_data = data.get('data', [])#

        if isinstance(archivos_data, list):
            for envase_data in archivos_data:
                # Crear el registro del modelo Envases
                registro = Attachhijo()

                # Obtener los campos disponibles del modelo
                campos = [f.name for f in Attachhijo._meta.fields]

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
        registros = Attachhijo.objects.filter(numero=numero).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data_a(registros[start:end])
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
        att = Attachhijo.objects.get(id=id)
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
        att = Attachhijo.objects.get(id=id)
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

            registros = Embarqueaereo.objects.filter(awb=master)

            if not registros.exists():
                return JsonResponse({'status': 'error', 'message': 'No se encontraron registros con el master especificado.'}, status=404)

            for registro in registros:
                registro.fecharetiro = fecha
                registro.save()

            return JsonResponse({'status': 'success', 'message': f'Se actualizaron {registros.count()} registros correctamente.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)