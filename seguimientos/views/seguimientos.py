import json
from copy import deepcopy
import simplejson as simplejson
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from datetime import datetime

from impomarit.models import Embarqueaereo
from mantenimientos.models import Vapores
from seguimientos.forms import NotasForm, seguimientoForm, cronologiaForm, envasesForm, embarquesForm, gastosForm, \
    pdfForm, archivosForm, rutasForm, emailsForm, clonarForm,aplicableForm
from seguimientos.models import VGrillaSeguimientos as Seguimiento, Seguimiento as SeguimientoReal, Envases, Cargaaerea, \
    Attachhijo, Serviceaereo, Conexaerea, Faxes
from auditlog.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DataError
import json
import simplejson

@login_required(login_url='/')
def grilla_seguimientos(request):
    try:
        if request.user.has_perms(["seguimientos.view_seguimiento", ]):
            opciones_busqueda = {
                'numero__icontains': 'SEGUIMIENTO',
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
            return render(request, 'seguimientos/grilla_datos.html', {
                'form_notas': NotasForm(initial={'fecha':datetime.now().strftime('%Y-%m-%d')}),
                'form_emails': emailsForm(),
                'form': seguimientoForm(initial={'fecha':datetime.now().strftime('%Y-%m-%d'),'vencimiento':datetime.now().strftime('%Y-%m-%d')}),
                'form_cronologia': cronologiaForm(),
                'form_envases': envasesForm(),
                'form_embarques': embarquesForm(),
                'form_gastos': gastosForm(),
                'form_pdf': pdfForm(),
                'form_archivos': archivosForm(),
                'form_rutas': rutasForm(),
                'form_clonar': clonarForm(),
                'form_aplicable': aplicableForm(),
                'title_page': 'Seguimientos',
                'opciones_busqueda': opciones_busqueda,
            })
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')


""" VISTA """

param_busqueda = {
    1: 'numero__icontains',
    2: 'modo__icontains',
    3: 'eta__icontains',
    4: 'etd__icontains',
    5: 'buque_viaje__icontains',   # si lo definiste como campo en la vista
    6: 'awb__icontains',
    7: 'hawb__icontains',
    8: 'embarcador__icontains',
    9: 'consignatario__icontains',
    10: 'origen_text__icontains',   # si usás descripción, si no, 'origen'
    11: 'destino_text__icontains',  # idem
    12: 'posicion__icontains',  # idem
}

""" TABLA PUERTO """
columns_table = {
    0: 'id',  # acciones (no usado en búsquedas)
    1: 'numero',
    2: 'modo',
    3: 'eta',
    4: 'etd',
    5: 'buque_viaje',  # o 'vapor' si no usás alias
    6: 'awb',
    7: 'hawb',
    8: 'embarcador',
    9: 'consignatario',
    10: 'origen_text',
    11: 'destino_text',
    12: 'posicion',
}



def source_seguimientos(request):
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
        filtro['nroreferedi__isnull'] = True
        registros = Seguimiento.objects.filter(**filtro).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Seguimiento.objects.all().count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def source_seguimientos_modo(request, modo):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        """ BUSCO ORDEN """
        args = {
            '1': request.GET['columns[1][search][value]'],
            '2': request.GET['columns[2][search][value]'],
            '3': request.GET['columns[3][search][value]'],
            '4': request.GET['columns[4][search][value]'],
            '5': request.GET['columns[5][search][value]'],
            '6': request.GET['columns[6][search][value]'],
            '7': request.GET['columns[7][search][value]'],
        }

        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])

        # Agrega el filtro de modo
        filtro['modo'] = modo

        end = start + length
        order = get_order(request, columns_table)

        # Obtener el array de IDs agregados desde la solicitud
        ids_agregados = request.GET.getlist('ids_agregados[]')

        """FILTRO REGISTROS"""
        filtro['nroreferedi__isnull'] = True
        registros = Seguimiento.objects.filter(**filtro).order_by(*order)


        # Excluir los registros que están en el array de 'agregados', solo si no está vacío
        if ids_agregados:
            registros = registros.exclude(id__in=ids_agregados)

        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])

        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Seguimiento.objects.all().count()
        resultado['recordsFiltered'] = registros.count()

        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'

    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def get_datos_embarque(numero):
    try:
        resultado=[]
        envases = Envases.objects.filter(numero=numero).values_list('unidad','cantidad','nrocontenedor','precinto','peso','volumen','bultos')
        if envases.count()>0:
            for registro in envases:
                txt=('<b>'+ str(registro[0] if registro[0] is not None else '').upper() +'</b>: '+
                     str('{:.3f}'.format(registro[1]) if registro[1] is not None else ''))
                txt += ' <b>CNTR:</b> ' + str(registro[2] if registro[2] is not None else '')
                txt += ' <b>SEAL:</b> ' + str(registro[3] if registro[3] is not None else '')
                txt += ' <b>WT:</b> ' + str(registro[4] if registro[4] is not None else '')
                txt += ' <b>VOL:</b> ' + str(registro[5] if registro[5] is not None else '')
                txt += ' <b>BULTOS:</b> ' + str(registro[6] if registro[6] is not None else '')
                resultado.append(txt)

        return resultado
    except Exception as e:
        raise TypeError(e)


def get_data(registros_filtrados):
    try:
        data = []
        cronologia = [
            'fecha',
            'originales',
            'etd',
            'eta',

        ]
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.numero is None else str(registro.numero))
            registro_json.append('' if registro.modo is None else str(registro.modo))
            registro_json.append('' if registro.cliente is None else str(registro.cliente)) #3
            registro_json.append('' if registro.origen is None else str(registro.origen))#4
            registro_json.append('' if registro.destino is None else str(registro.destino))#5
            registro_json.append('' if registro.fecha is None else str(registro.fecha)[:10])
            registro_json.append('' if registro.status is None else str(registro.status))
            """ EXTRAS """
            registro_json.append('' if registro.notas is None else str(registro.notas))
            """ PRIMER COLUMNA """
            registro_json.append('' if registro.cliente is None else str(registro.cliente))
            registro_json.append('' if registro.embarcador is None else str(registro.embarcador)) #10
            registro_json.append('' if registro.consignatario is None else str(registro.consignatario)) #11
            registro_json.append('' if registro.notificar is None else str(registro.notificar))
            registro_json.append('' if registro.agente is None else str(registro.agente))
            registro_json.append('' if registro.transportista is None else str(registro.transportista))
            registro_json.append('' if registro.armador is None else str(registro.armador))
            registro_json.append('' if registro.agecompras is None else str(registro.agecompras))
            registro_json.append('' if registro.ageventas is None else str(registro.ageventas))
            registro_json.append('' if registro.despachante is None else str(registro.despachante))
            """ SEGUNDA COLUMNA """
            registro_json.append('' if registro.nroreferedi is None else str(registro.nroreferedi))
            registro_json.append('' if registro.moneda is None else str(registro.moneda))
            registro_json.append('' if registro.vendedor is None else str(registro.vendedor))
            registro_json.append('' if registro.deposito is None else str(registro.deposito))
            try:
                if registro.modo in ['IMPORT MARITIMO', 'EXPORT MARITIMO']:
                    nombre_vapor = Vapores.objects.get(codigo=registro.vapor).nombre
                else:
                    nombre_vapor = registro.vapor
            except:
                nombre_vapor = registro.vapor

            registro_json.append('' if nombre_vapor is None else str(nombre_vapor)) #23

            registro_json.append('' if registro.viaje is None else str(registro.viaje)) #24
            registro_json.append('' if registro.awb is None else str(registro.awb)) #25
            registro_json.append('' if registro.hawb is None else str(registro.hawb)) #26
            registro_json.append('' if registro.operacion is None else str(registro.operacion))
            registro_json.append('' if registro.refcliente is None else str(registro.refcliente))
            """ TERCER COLUMNA """
            registro_json.append('' if registro.loading is None else str(registro.loading))
            registro_json.append('' if registro.discharge is None else str(registro.discharge))
            registro_json.append('' if registro.posicion is None else str(registro.posicion))
            registro_json.append('' if registro.pago is None else str(registro.pago))
            registro_json.append('' if registro.arbitraje is None else str(registro.arbitraje))
            registro_json.append('' if registro.ubicacion is None else str(registro.ubicacion))
            registro_json.append('' if registro.booking is None else str(registro.booking))
            registro_json.append('' if registro.trackid is None else str(registro.trackid))
            registro_json.append('' if registro.proyecto is None else str(registro.proyecto))
            registro_json.append('' if registro.trafico is None else str(registro.trafico))
            registro_json.append('' if registro.actividad is None else str(registro.actividad))
            registro_json.append('' if registro.demora is None else str(registro.demora))
            registro_json.append('' if registro.diasalmacenaje is None else str(registro.diasalmacenaje))
            registro_json.append('' if registro.wreceipt is None else str(registro.wreceipt))
            registro_json.append('' if registro.valor is None else str(registro.valor))
            # archivos = Attachhijo.objects.filter(numero=registro.numero).annotate(num_archivos=Count('id')).values('num_archivos').first()
            # embarques = Cargaaerea.objects.filter(numero=registro.numero).annotate(num_archivos=Count('id')).values('num_archivos').first()
            # envases = Envases.objects.filter(numero=registro.numero).annotate(num_archivos=Count('id')).values('num_archivos').first()
            # gastos = Serviceaereo.objects.filter(numero=registro.numero).annotate(num_archivos=Count('id')).values('num_archivos').first()
            # rutas = Conexaerea.objects.filter(numero=registro.numero).annotate(num_archivos=Count('id')).values('num_archivos').first()
            archivos = Attachhijo.objects.filter(numero=registro.numero).count()
            embarques = Cargaaerea.objects.filter(numero=registro.numero).count()
            envases = Envases.objects.filter(numero=registro.numero).count()
            gastos = Serviceaereo.objects.filter(numero=registro.numero).count()
            rutas = Conexaerea.objects.filter(numero=registro.numero).count()
            notas = Faxes.objects.filter(numero=registro.numero).count()


            #falta historial
            registro_json.append(archivos)
            registro_json.append(embarques)
            registro_json.append(envases)
            registro_json.append(gastos)
            crono = False
            registro2 = SeguimientoReal()
            campos = vars(registro2)
            for c in campos:
                if c in cronologia:
                    aux = getattr(registro2, c)
                    if aux is not None:
                        crono = True
            registro_json.append(crono)
            registro_json.append(rutas)
            """ cargo emails segun el tipo de seguimiento """
            if registro.modo == 'IMPORT MARITIMO':
                registro_json.append(registro.emailim)
            elif registro.modo == 'IMPORT AEREO':
                registro_json.append(registro.emailia)
            elif registro.modo == 'IMPORT TERRESTRE':
                registro_json.append(registro.emailit)
            elif registro.modo == 'EXPORT MARITIMO':
                registro_json.append(registro.emailem)
            elif registro.modo == 'EXPORT AEREO':
                registro_json.append(registro.emailea)
            elif registro.modo == 'EXPORT TERRESTRE':
                registro_json.append(registro.emailet)
            else:
                registro_json.append('')

            registro_json.append(get_datos_embarque(registro.numero))
            registro_json.append(notas)

            llave = False
            if registro.aplicable and registro.aplicable !=0 and registro.modo == 'IMPORT AEREO':
                llave = True

            registro_json.append(llave)
            registro_json.append(registro.cliente_codigo)
            registro_json.append('' if registro.etd is None else str(registro.etd)[:10]) #55
            registro_json.append('' if registro.eta is None else str(registro.eta)[:10]) #56
            registro_json.append('' if registro.buque_viaje is None else str(registro.buque_viaje)) #57


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
        messages.error(request, e)



def source(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax:
        numero = request.GET.get('numero')
        if numero:
            notas_queryset = Faxes.objects.filter(numero=numero).values('id', 'fecha', 'asunto', 'tipo', 'notas')
        else:
            notas_queryset = Faxes.objects.all().values('id', 'fecha', 'asunto', 'tipo', 'notas')

        # Procesar resultados
        notas_list = []
        for nota in notas_queryset:
            fecha = str(nota['fecha'])[:10] if nota['fecha'] else ''
            asunto = (nota['asunto'] or '')[:40]
            notas_list.append({
                'id': nota['id'],
                'fecha': fecha,
                'asunto': asunto,
                'tipo': nota['tipo'],
                'notas': nota['notas'],
            })

        return JsonResponse({"data": notas_list})

    # Renderiza la plantilla cuando no es una solicitud AJAX
    return render(request, 'notas.html')

def guardar_notas(request):
    resultado = {}
    try:
        # Verifica que request.body contenga datos
        if not request.body:
            return JsonResponse({"resultado": "error", "mensaje": "No data received"}, status=400)

        # Carga los datos JSON desde request.body
        data = json.loads(request.body)  # Convierte JSON a diccionario

        # Extrae los valores de los campos
        id_nota = data.get('id_nota')  # ID de la nota, si existe
        numero = data.get('numero')
        fecha = data.get('fecha')
        asunto = data.get('asunto')
        tipo = data.get('tipo')
        notas = data.get('notas')

        # Si id_nota está presente, trata la solicitud como una actualización
        if id_nota:
            registro = Faxes.objects.get(id=id_nota)
            registro.numero = numero
            registro.fecha = fecha
            registro.asunto = asunto
            registro.tipo = tipo
            registro.notas = notas
            registro.save()
            resultado['resultado'] = 'exito'
            resultado['mensaje'] = 'Nota actualizada correctamente'
        else:
            # Si no hay id_nota, crea un nuevo registro
            registro = Faxes(
                numero=numero,
                fecha=fecha,
                asunto=asunto,
                tipo=tipo,
                notas=notas
            )
            registro.save()
            resultado['resultado'] = 'exito'
            resultado['mensaje'] = 'Nota creada correctamente'
            resultado['id'] = registro.id

    except Faxes.DoesNotExist:
        resultado['resultado'] = 'error'
        resultado['mensaje'] = 'Nota no encontrada para actualización.'
    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = 'error'
        resultado['mensaje'] = str(e)

    return JsonResponse(resultado)

def eliminar_nota(request):
    resultado = {}
    try:
        id = request.POST.get('id')
        Faxes.objects.get(id=id).delete()
        resultado['resultado'] = 'exito'
    except Faxes.DoesNotExist:
        resultado['resultado'] = 'La nota no existe.'
    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)

    return JsonResponse(resultado)


def guardar_envases(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        data = simplejson.loads(request.POST['data'])
        registro = Envases()
        campos = vars(registro)
        for x in data:
            k = x['name']
            v = x['value']
            for name in campos:
                if name == k:
                    if v is not None and len(v) > 0:
                        if v is not None:
                            setattr(registro, name, v)
                        else:
                            if len(v) > 0:
                                setattr(registro, name, v)
                    else:
                        setattr(registro, name, None)
                    continue
        registro.numero = numero
        registro.save()
        resultado['resultado'] = 'exito'
        resultado['numero'] = str(registro.numero)
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def eliminar_envase(request):
    resultado = {}
    try:
        id = request.POST['id']
        Envases.objects.get(id=id).delete()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def guardar_cronologia(request):
    resultado = {}
    try:
        id = request.POST['id']
        data = simplejson.loads(request.POST['data'])
        registro = SeguimientoReal.objects.get(id=id)
        campos = vars(registro)
        etd_valor = None  # Variable temporal para almacenar el valor de etd

        for name in campos:
            for d in data:
                if name in d['name']:
                    if len(d['value']) > 0:
                        setattr(registro, name, d['value'])
                        if name == "etd":  # Si estamos procesando el campo 'etd'
                            etd_valor = d['value']
                    else:
                        setattr(registro, name, None)

        if etd_valor:
            setattr(registro, "loadingdate", etd_valor)

        registro.save()
        resultado['resultado'] = 'exito'
    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)

    data_json = json.dumps(resultado)
    return HttpResponse(data_json, content_type="application/json")


def guardar_seguimiento_old(request):
    resultado = {}
    try:
        data = simplejson.loads(request.POST['form'])
        tipo = request.POST['tipo']

        # Determinar si se está modificando un registro o creando uno nuevo
        if 'id' in data and data['id'][0] != '':
            registro = SeguimientoReal.objects.get(id=data['id'][0])
            tiporeg = 'modifica'
        else:
            hawb = data.get('hawb', [''])[0]
            awb = data.get('awb', [''])[0]

            # Verificación individual y combinada
            if hawb and awb:
                existe = SeguimientoReal.objects.filter(hawb=hawb, awb=awb).exists()
                if existe:
                    resultado[
                        'resultado'] = f'Error: La combinación HAWB {hawb} y AWB {awb} ya fue ingresada previamente.'
                    return HttpResponse(json.dumps(resultado), content_type="application/json")
            elif hawb:
                existe = SeguimientoReal.objects.filter(hawb=hawb).exists()
                if existe:
                    resultado['resultado'] = f'Error: El HAWB {hawb} ya fue ingresado previamente.'
                    return HttpResponse(json.dumps(resultado), content_type="application/json")
            elif awb:
                existe = SeguimientoReal.objects.filter(awb=awb).exists()
                if existe:
                    resultado['resultado'] = f'Error: El AWB {awb} ya fue ingresado previamente.'
                    return HttpResponse(json.dumps(resultado), content_type="application/json")

            registro = SeguimientoReal()
            numero = SeguimientoReal.objects.all().values_list('numero', flat=True).order_by('-numero').first()
            registro.numero = (numero + 1) if numero else 1  # Manejo de caso si no hay registros previos
            tiporeg = 'nuevo'


        campos = vars(registro)

        # Asignar valores a los campos del modelo
        for k, v in data.items():
            for name in campos:
                if name == k:
                    if v[0] is not None and len(v[0]) > 0:
                        setattr(registro, name, v[1] if v[1] is not None else v[0])
                    else:
                        setattr(registro, name, None)
                    continue

        #registro.modo = tipo

        if 'id' in data and data['id'][0] != '':
            registro.id = data['id'][0]
            registro.save()
        else:
            # Inicializar valores por defecto
            registro.iniciales = 'S/I'
            registro.recepcionado = 'N'
            registro.tarifafija = 'N'
            registro.multimodal = 'N'
            registro.unidadpeso = 'K'
            registro.unidadvolumen = 'B'
            registro.tipobonifcli = 'P'
            registro.editado = 'S/I'
            registro.save()

        resultado['resultado'] = 'exito'
        resultado['numero'] = str(registro.numero)
        resultado['id'] = str(registro.id)
        resultado['tipo'] = tiporeg

    except IntegrityError as e:
        resultado['resultado'] = f'Error de integridad, intente nuevamente: {str(e)}'
    except Exception as e:
        resultado['resultado'] = str(e)

    return HttpResponse(json.dumps(resultado), content_type="application/json")



def guardar_seguimiento(request):
    resultado = {}
    try:
        data = simplejson.loads(request.POST['form'])
        tipo = request.POST.get('tipo')

        # ¿edito o creo?
        if 'id' in data and data['id'][0]:
            registro = SeguimientoReal.objects.get(id=data['id'][0])
            tiporeg = 'modifica'
        else:
            hawb = (data.get('hawb') or [''])[0]
            awb  = (data.get('awb')  or [''])[0]

            if hawb and awb and SeguimientoReal.objects.filter(hawb=hawb, awb=awb).exists():
                return HttpResponse(json.dumps({
                    'resultado': f'Error: La combinación HAWB {hawb} y AWB {awb} ya fue ingresada previamente.',
                    'field': 'hawb'
                }), content_type="application/json")

            if hawb and SeguimientoReal.objects.filter(hawb=hawb).exists():
                return HttpResponse(json.dumps({
                    'resultado': f'Error: El HAWB {hawb} ya fue ingresado previamente.',
                    'field': 'hawb'
                }), content_type="application/json")

            if awb and SeguimientoReal.objects.filter(awb=awb).exists():
                return HttpResponse(json.dumps({
                    'resultado': f'Error: El AWB {awb} ya fue ingresado previamente.',
                    'field': 'awb'
                }), content_type="application/json")

            registro = SeguimientoReal()
            ultimo_num = SeguimientoReal.objects.values_list('numero', flat=True).order_by('-numero').first()
            registro.numero = (ultimo_num + 1) if ultimo_num else 1
            tiporeg = 'nuevo'

        # nombres de campos del modelo (solo concretos, sin m2m ni reverse)
        field_names = {f.name for f in registro._meta.get_fields() if not f.many_to_many and not f.one_to_many}

        # asignar con detección de errores por campo
        for k, v in data.items():
            if k not in field_names:
                continue
            raw = v[1] if len(v) > 1 and v[1] is not None else (v[0] if v and v[0] is not None else None)
            val = raw if (raw not in ("",)) else None
            try:
                setattr(registro, k, val)
            except (ValidationError, ValueError, DataError) as e:
                # devolver el campo y el mensaje
                return HttpResponse(json.dumps({
                    'resultado': f'Error en el campo "{k}": {str(e)}',
                    'field': k,
                    'detail': str(e)
                }), content_type="application/json")

        if 'id' in data and data['id'][0]:
            registro.id = data['id'][0]

        if tiporeg == 'nuevo':
            # valores por defecto
            registro.iniciales = registro.iniciales or 'S/I'
            registro.recepcionado = registro.recepcionado or 'N'
            registro.tarifafija = registro.tarifafija or 'N'
            registro.multimodal = registro.multimodal or 'N'
            registro.unidadpeso = registro.unidadpeso or 'K'
            registro.unidadvolumen = registro.unidadvolumen or 'B'
            registro.tipobonifcli = registro.tipobonifcli or 'P'
            registro.editado = registro.editado or 'S/I'

        try:
            registro.full_clean()  # valida tipos/longitudes/validators de Django
            registro.save()
        except ValidationError as e:
            # e.message_dict tiene por campo -> lista de errores
            # devolvemos el primero útil
            fld = next(iter(e.message_dict.keys()), None)
            msg = '; '.join(e.message_dict.get(fld, [str(e)]))
            return HttpResponse(json.dumps({
                'resultado': f'Error en el campo "{fld}": {msg}' if fld else f'Error de validación: {msg}',
                'field': fld,
                'detail': e.message_dict
            }), content_type="application/json")
        except IntegrityError as e:
            return HttpResponse(json.dumps({
                'resultado': f'Error de integridad (BD). {str(e)}',
                'field': None
            }), content_type="application/json")
        except DataError as e:
            return HttpResponse(json.dumps({
                'resultado': f'Error de datos: {str(e)}',
                'field': None
            }), content_type="application/json")

        return HttpResponse(json.dumps({
            'resultado': 'exito',
            'numero': str(registro.numero),
            'id': str(registro.id),
            'tipo': tiporeg
        }), content_type="application/json")

    except Exception as e:
        return HttpResponse(json.dumps({
            'resultado': f'Error inesperado: {str(e)}',
            'field': None
        }), content_type="application/json")


def eliminar_seguimiento_old(request):
    resultado = {}
    try:
        id = request.POST['id']
        seguimiento = SeguimientoReal.objects.get(id=id)
        numero = seguimiento.numero  # Obtener el número antes de borrar el seguimiento
        seguimiento.nroreferedi=numero
        # Eliminar registros relacionados
        #Cargaaerea.objects.filter(numero=numero).delete()
        #Conexaerea.objects.filter(numero=numero).delete()
        #Serviceaereo.objects.filter(numero=numero).delete()
        #Envases.objects.filter(numero=numero).delete()

        # Eliminar el seguimiento
        seguimiento.save()
        resultado['resultado'] = 'exito'

    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except SeguimientoReal.DoesNotExist:
        resultado['resultado'] = 'El seguimiento no existe.'
    except Exception as e:
        resultado['resultado'] = str(e)

    return HttpResponse(json.dumps(resultado), content_type="application/json")

def eliminar_seguimiento(request):
    resultado = {}
    try:
        id = request.POST['id']
        seguimiento = SeguimientoReal.objects.get(id=id)
        numero = seguimiento.numero  # Obtener el número antes de borrar el seguimiento
        seguimiento.nroreferedi=numero
        # Eliminar registros relacionados
        #Cargaaerea.objects.filter(numero=numero).delete()
        #Conexaerea.objects.filter(numero=numero).delete()
        #Serviceaereo.objects.filter(numero=numero).delete()
        #Envases.objects.filter(numero=numero).delete()

        # Eliminar el seguimiento
        seguimiento.save()
        resultado['resultado'] = 'exito'

    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except SeguimientoReal.DoesNotExist:
        resultado['resultado'] = 'El seguimiento no existe.'
    except Exception as e:
        resultado['resultado'] = str(e)

    return HttpResponse(json.dumps(resultado), content_type="application/json")

def eliminar_seguimiento_st(request):
    resultado = {}
    try:
        id = request.POST['id']

        with transaction.atomic():
            seguimiento = SeguimientoReal.objects.get(id=id)
            numero = seguimiento.numero  # Obtener el número antes de borrar el seguimiento

            # limpiar campos en el embarque
            seguimiento.embarque = None
            seguimiento.posicion = 'S/I'
            seguimiento.awb = 'S/I'
            seguimiento.haw = 'S/I'
            seguimiento.consignatario = 0
            seguimiento.embarcador = 0
            seguimiento.agente = 0
            seguimiento.notificante = 0
            seguimiento.agcompras = 0
            seguimiento.agventas = 0
            seguimiento.vendedor = 0
            seguimiento.despachante = 0
            seguimiento.etd = None
            seguimiento.eta = None
            seguimiento.origen = '???'
            seguimiento.destino = '???'
            seguimiento.loading = '???'
            seguimiento.discharge = '???'
            seguimiento.save()


            # borrar registros relacionados
            Embarqueaereo.objects.filter(numero=numero).delete()
            Cargaaerea.objects.filter(numero=numero).delete()
            Conexaerea.objects.filter(numero=numero).delete()
            Envases.objects.filter(numero=numero).delete()
            Serviceaereo.objects.filter(numero=numero).delete()

        resultado['resultado'] = 'exito'

    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)

    return JsonResponse(resultado)


def clonar_seguimiento(request):
    resultado = {}
    try:
        data = simplejson.loads(request.POST['data'])
        original = SeguimientoReal.objects.get(id=request.POST['id'])
        key = False
        numero = SeguimientoReal.objects.all().values_list('numero').order_by('-numero')[:1][0][0]
        clonado = deepcopy(original)
        clonado.id = None
        clonado.awb = None
        clonado.hawb = None
        clonado.posicion = None
        clonado.embarque = None
        clonado.numero = numero + 1
        clonado.fecha = datetime.now().date()
        clonado.vapor = None
        clonado.awb = None
        clonado.hawb = None
        clonado.volumen = None
        clonado.loadingdate=None
        clonado.vencimiento=None
        clonado.aplicable=None

        # Revisar las opciones seleccionadas antes de clonar
        clonar_envases = clonar_embarques = clonar_gastos = clonar_rutas = False

        for row in data:
            if row['name'] == 'envases' and row['value'] == 'SI':
                clonar_envases = True
            elif row['name'] == 'embarques' and row['value'] == 'SI':
                clonar_embarques = True
            elif row['name'] == 'gastos' and row['value'] == 'SI':
                clonar_gastos = True
            elif row['name'] == 'rutas' and row['value'] == 'SI':
                clonar_rutas = True
            elif row['name'] == 'cronologia' and row['value'] == 'SI':
                key = True

        # Clonar solo lo que se seleccionó
        if clonar_envases:
            for r in Envases.objects.filter(numero=original.numero):
                aux = Envases(
                    numero=clonado.numero,
                    unidad=r.unidad,
                    tipo=r.tipo,
                    movimiento=r.movimiento,
                    terminos=r.terminos,
                    cantidad=r.cantidad
                )
                aux.id = None
                aux.save()

        if clonar_embarques:
            for r in Cargaaerea.objects.filter(numero=original.numero):
                aux = Cargaaerea(numero=clonado.numero, producto=r.producto)
                aux.id = None
                aux.save()

        if clonar_gastos:
            for r in Serviceaereo.objects.filter(numero=original.numero):
                aux = deepcopy(r)
                aux.numero = clonado.numero
                aux.id = None
                aux.save()

        if clonar_rutas:
            for r in Conexaerea.objects.filter(numero=original.numero):
                aux = deepcopy(r)
                aux.numero = clonado.numero
                aux.id = None
                aux.save()

        if not key:
            clonado.etd = None
            clonado.eta = None

        clonado.save()

        # Crear entrada extra en LogEntry que indique que esto fue un clonado
        LogEntry.objects.create(
            content_type=ContentType.objects.get_for_model(SeguimientoReal),
            object_pk=str(clonado.id),
            object_repr=str(clonado),
            action=1,  # UPDATE (para que no sea confundido con create)
            actor=request.user,
            changes='{"info": ["", "Clonado desde seguimiento %s"]}' % original.numero,
            timestamp=datetime.now()
        )
        print("Se creó log con PK:", clonado.id)

        resultado['resultado'] = 'exito'
        resultado['numero'] = str(clonado.numero)
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente:. ' + str(e)
    except Exception as e:
        resultado['resultado'] = str(e)

    data_json = json.dumps(resultado)
    return HttpResponse(data_json, content_type="application/json")

def get_datos_aplicables(request):
    numero = request.GET.get('numero')

    try:
        seguimiento = SeguimientoReal.objects.get(numero=numero)
        cargas = Cargaaerea.objects.filter(numero=numero)

        total_bruto = 0
        total_volumen = 0

        for c in cargas:
            total_bruto += c.bruto or 0

            if c.cbm:
                total_volumen += c.cbm
            elif c.medidas:
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
            'tarifacompra': float(seguimiento.tarifacompra or 0),
            'tarifaventa': float(seguimiento.tarifaventa or 0),
            'aplicable': float(seguimiento.aplicable or 0),
            'muestroflete': float(seguimiento.muestroflete or 0),
            'bruto': round(total_bruto, 2),
            'volumen': round(total_volumen, 2),
            'status': 'ok'
        }

    except Seguimiento.DoesNotExist:
        data = {'status': 'error', 'mensaje': 'Seguimiento no encontrado'}

    return JsonResponse(data)


def guardar_aplicable(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            numero = data.get('numero')

            seg = SeguimientoReal.objects.get(numero=numero)
            seg.tarifacompra = data.get('tarifacompra') or None
            seg.tarifaventa = data.get('tarifaventa') or None
            seg.aplicable = data.get('aplicable') or None
            seg.muestroflete = data.get('muestroflete') or None

            seg.save()

            return JsonResponse({'status': 'ok'})
        except Seguimiento.DoesNotExist:
            return JsonResponse({'status': 'error', 'mensaje': 'Seguimiento no encontrado'})

    return JsonResponse({'status': 'error', 'mensaje': 'Método no permitido'})