from django.contrib.auth.decorators import login_required
import json
from expterrestre.models import ExpterraEmbarqueaereo, ExpterraCargaaerea, ExpterraConexaerea, ExpterraServiceaereo, \
    ExpterraEnvases
from mantenimientos.models import Vendedores
from django.http import JsonResponse, Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.db import IntegrityError, transaction
from expterrestre.forms import add_house, edit_house
from seguimientos.models import Seguimiento, Serviceaereo, Envases, Conexaerea, Cargaaerea, Attachhijo
import re
from datetime import datetime


@login_required(login_url="/")

def add_house_impmarit(request):
    try:
        if request.method == 'POST':
            form = add_house(request.POST)
            if form.is_valid():
                reserva = ExpterraEmbarqueaereo()
                reserva.fechaingreso = datetime.now()
                reserva.numero = reserva.get_number()

                # Para campos de texto o numéricos, se asegura de proporcionar valores predeterminados.
                reserva.consolidado = request.POST.get('consolidado', 0)
                reserva.awb = form.cleaned_data.get('awb', "")
                reserva.notifcliente = form.cleaned_data.get('notificar_cliente', None)
                reserva.notifagente = form.cleaned_data.get('notificar_agente', None)
                reserva.fecharetiro = form.cleaned_data.get('fecha_retiro', None)
                reserva.fechaembarque = form.cleaned_data.get('fecha_embarque', None)
                reserva.origen = form.cleaned_data.get('origen', "")
                reserva.destino = form.cleaned_data.get('destino', "")
                reserva.moneda = form.cleaned_data.get('moneda', 0)
                reserva.pago = form.cleaned_data.get('pago', 0)
                reserva.hawb = form.cleaned_data.get('house', "")
                reserva.localint = form.cleaned_data.get('tipo', "")
                reserva.terminos = form.cleaned_data.get('terminos', "")
                reserva.demora = form.cleaned_data.get('demora', 0)
                reserva.operacion = form.cleaned_data.get('operacion', "")
                reserva.arbitraje = form.cleaned_data.get('arbitraje', "")
                reserva.wreceipt = form.cleaned_data.get('wreceipt', "")
                reserva.posicion = form.cleaned_data.get('posicion_h', 0)
                reserva.status = form.cleaned_data.get('status_h', "")
                #
                # # Para los campos relacionales o numéricos
                # reserva.transportista = form.cleaned_data.get('transportista', None)
                # reserva.agente = form.cleaned_data.get('agente', None)
                # reserva.consignatario = form.cleaned_data.get('consignatario', None)
                # reserva.armador = form.cleaned_data.get('armador', None)
                # reserva.cliente = form.cleaned_data.get('cliente', None)

                try:
                    # Validar campos numéricos con valores predeterminados
                    reserva.vendedor = int(form.cleaned_data.get('vendedor_i', 0)) if form.cleaned_data.get('vendedor_i') else 0
                    reserva.transportista = int(form.cleaned_data.get('transportista_i', 0)) if form.cleaned_data.get('transportista_i') else 0
                    reserva.agente = int(form.cleaned_data.get('agente_i', 0)) if form.cleaned_data.get('agente_i') else 0
                    reserva.consignatario = int(form.cleaned_data.get('consignatario_i', 0)) if form.cleaned_data.get('consignatario_i') else 0
                    reserva.cliente = int(form.cleaned_data.get('cliente_i', 0)) if form.cleaned_data.get('cliente_i') else 0
                    reserva.agecompras = int(form.cleaned_data.get('agcompras_i', 0)) if form.cleaned_data.get('agcompras_i') else 0
                    reserva.ageventas = int(form.cleaned_data.get('agventas_i', 0)) if form.cleaned_data.get('agventas_i') else 0
                    reserva.embarcador = int(form.cleaned_data.get('embarcador_i', 0)) if form.cleaned_data.get('embarcador_i') else 0


                except ValueError as e:
                    return JsonResponse({
                        'success': False,
                        'message': 'Uno o más campos tienen un formato incorrecto.',
                        'errors': {}
                    })

                # Guardar el registro
                reserva.save()

                if reserva.pk:
                    return JsonResponse({'success': True, 'message': 'House agregado'})
                else:
                    return JsonResponse({'success': False, 'message': 'No se pudo agregar el house'})

            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Formulario inválido, por favor revise los campos.',
                    'errors': form.errors.as_json()
                })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Ocurrió un error: {str(e)}',
            'errors': {}
        })


def generar_posicion(request):
    fecha_actual = datetime.now()
    anio_actual = fecha_actual.year
    mes_actual = fecha_actual.strftime('%m')

    ultima_reserva = ExpterraEmbarqueaereo.objects.filter(fechaingreso__year=anio_actual).order_by('-numero').first()

    if ultima_reserva and ultima_reserva.posicion:
        ultima_posicion = ultima_reserva.posicion
        match = re.match(rf"IT{mes_actual}-(\d+)-\d{{4}}", ultima_posicion)

        if match:
            # Incrementar el código numérico
            ultimo_codigo = int(match.group(1))
            nuevo_codigo = str(ultimo_codigo + 1).zfill(5)
        else:
            nuevo_codigo = "00001"
    else:
        nuevo_codigo = "00001"

    nueva_posicion = f"IT{mes_actual}-{nuevo_codigo}-{anio_actual}"

    # Devolver la posición generada como JSON
    return JsonResponse({'posicion': nueva_posicion})

#importados#
def add_house_importado(request):
    try:
        if request.method == 'POST':
            # Asumimos que el array de datos llega en formato JSON
            data = json.loads(request.body)

            if isinstance(data, list):
                numeros_guardados = []
                # Iteramos sobre cada elemento en la lista
                for house_data in data:
                    # Crear la instancia de Embarqueaereo para cada registro
                    reserva = ExpterraEmbarqueaereo()
                    reserva.fechaingreso = datetime.now()
                    reserva.numero = reserva.get_number()
                    reserva.consolidado = house_data.get('consolidado', 0)
                    reserva.seguimiento = house_data.get('seguimiento')
                    reserva.awb = house_data.get('awb')
                    reserva.origen = house_data.get('origen')
                    reserva.destino = house_data.get('destino')
                    reserva.moneda = house_data.get('moneda')
                    reserva.hawb = house_data.get('house')
                    reserva.demora = house_data.get('demora')
                    reserva.operacion = house_data.get('operacion')
                    reserva.arbitraje = house_data.get('arbitraje')
                    reserva.wreceipt = house_data.get('wreceipt')
                    reserva.posicion = house_data.get('posicion')
                    reserva.status = house_data.get('status_h')

                    reserva.transportista = house_data.get('transportista')
                    reserva.agente = house_data.get('agente')
                    reserva.consignatario = house_data.get('consignatario')
                    reserva.cliente = house_data.get('cliente')
                    reserva.vendedor = house_data.get('vendedor')
                    reserva.agecompras = house_data.get('agcompras')
                    reserva.ageventas = house_data.get('agventas')
                    reserva.embarcador = house_data.get('embarcador')
                    reserva.fechaembarque=house_data.get('fechaembarque')
                    reserva.fecharetiro=house_data.get('fecharetiro')
                    reserva.pagoflete=house_data.get('pagoflete')
                    reserva.status=house_data.get('estado')
                    reserva.refproveedor = house_data.get('refproveedor')
                    reserva.ordencliente = house_data.get('refcliente')
                    reserva.terminos = house_data.get('terminos')
                    reserva.fechaingreso=datetime.now()
                    reserva.eta = house_data.get('eta')
                    reserva.etd = house_data.get('etd')
                    #reserva.aplicable = house_data.get('aplicable')
                    reserva.tarifaventa = house_data.get('tarifaventa')
                    reserva.tarifacompra = house_data.get('tarifacompra')
                    reserva.save()

                    numero = reserva.get_number()
                    consolidado = house_data.get('consolidado', 0)
                    awb = house_data.get('awb')
                    hawb = house_data.get('house')
                    seguimiento = house_data.get('seguimiento')
                    posicion = house_data.get('posicion')

                    actualizar_seguimiento(request, awb, hawb, numero, consolidado, seguimiento, posicion)

                    numeros_guardados.append({
                        "numero": reserva.numero,
                        "seguimiento": reserva.seguimiento
                    })

                return JsonResponse({'success': True, 'message': 'Todos los houses agregados con éxito','numeros_guardados': numeros_guardados})
            else:
                return JsonResponse({'success': False, 'message': 'Los datos enviados no son una lista válida.'})

        else:
            return JsonResponse({
                'success': False,
                'message': 'Método no permitido.'
            })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Ocurrió un error: {str(e)}',
            'errors': {}
        })

def actualizar_seguimiento(request,awb,hawb,embarque,consolidado,seguimiento,posicion):

    seg = Seguimiento.objects.get(numero=seguimiento)
    seg.awb=awb
    seg.hawb=hawb
    seg.embarque=embarque
    seg.consolidado=consolidado
    seg.posicion=posicion
    seg.save()


def source_seguimientos_importado(request):

        try:
            data = json.loads(request.body)
            ids = data.get('ids', [])

            registros = Seguimiento.objects.filter(id__in=ids)


            resultado = []
            for registro in registros:
                resultado.append({
                    "awb": registro.awb,
                    "posicion": 0,
                    "seguimiento":registro.numero,
                    "origen": registro.origen,
                    "destino": registro.destino,
                    "moneda": registro.moneda,
                    "loading": registro.loading,
                    "discharge": registro.discharge,
                    "vapor": registro.vapor,
                    "viaje": registro.viaje,
                    "house": registro.hawb,
                    "demora": registro.demora,
                    "operacion": registro.operacion,
                    "arbitraje": registro.arbitraje,
                    "wreceipt": registro.wreceipt,
                    "status": registro.status,
                    "vendedor": registro.vendedor,
                    "transportista": registro.transportista,
                    "agente": registro.agente,
                    "consignatario": registro.consignatario,
                    "armador": registro.armador,
                    "cliente": registro.cliente,
                    "agcompras": registro.agecompras,
                    "embarcador": registro.embarcador,
                    "agventas": registro.ageventas,
                    "pagoflete": 'C' if registro.pago == 'Collect' else 'P',
                    "estado": registro.status,
                    "fechaembarque":registro.etd,
                    "fecharetiro":registro.eta,
                    "refproveedor": registro.refproveedor,
                    "refcliente": registro.refcliente,
                    "terminos": registro.terminos,
                    "etd": registro.etd,
                    "eta": registro.eta,
                    "aplicable": registro.aplicable,
                    "tarifaventa": registro.tarifaventa,
                    "tarifacompra": registro.tarifacompra,
                })

            return JsonResponse({"data": resultado}, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def source_gastos_importado(request):
    try:
        data = json.loads(request.body)
        #numeros de los seguimientos
        ids = data.get('ids', [])

        registros = Serviceaereo.objects.filter(numero__in=ids)

        if not registros.exists():
            # Si no hay registros, devolver un array vacío
            return JsonResponse({"data": []}, safe=False)

        resultado = []
        for registro in registros:
            resultado.append({
                "numero": 0,
                "seguimiento_control":registro.numero,
                "servicio": registro.servicio,
                "secomparte": registro.secomparte,
                "moneda": registro.moneda,
                "costo": registro.costo,
                "precio": registro.precio,
                "arbitraje": registro.arbitraje,
                "tipogasto": registro.tipogasto,
                "pinformar": registro.pinformar,
                "notomaprofit": registro.notomaprofit,
                "modo": registro.modo,
                "socio": registro.socio,
                "detalle": registro.detalle,
            })

        return JsonResponse({"data": resultado}, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def source_envases_importado(request):
    try:
        data = json.loads(request.body)
        #numeros de los seguimientos
        ids = data.get('ids', [])

        registros = Envases.objects.filter(numero__in=ids)

        if not registros.exists():
            # Si no hay registros, devolver un array vacío
            return JsonResponse({"data": []}, safe=False)

        resultado = []
        for registro in registros:
            resultado.append({
                "numero": 0,
                "seguimiento_control": registro.numero,
                "unidad": registro.unidad,
                "tipo": registro.tipo,
                "movimiento": registro.movimiento,
                "precio": registro.precio,
                "costo": registro.costo,
                "marcas": registro.marcas,
                "precinto": registro.precinto,
                "tara": registro.tara,
                "envase": registro.envase,
                "terminos": registro.terminos,
                "cantidad": registro.cantidad,
                "bultos": registro.bultos,
                "peso": registro.peso,
                "profit": registro.profit,
                "volumen": registro.volumen,
                "nrocontenedor": registro.nrocontenedor,
            })

        #field_names = [field.name for field in Envases._meta.fields]
       # resultado = list(registros.values(*field_names))

        return JsonResponse({"data": resultado}, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def source_rutas_importado(request):
    try:
        data = json.loads(request.body)
        #numeros de los seguimientos
        ids = data.get('ids', [])

        registros = Conexaerea.objects.filter(numero__in=ids)

        if not registros.exists():
            # Si no hay registros, devolver un array vacío
            return JsonResponse({"data": []}, safe=False)

        resultado = []
        for registro in registros:
            resultado.append({
                "numero": 0,
                "seguimiento_control": registro.numero,
                "origen": registro.origen,
                "destino": registro.destino,
                "vapor": registro.vapor,
                "salida": registro.salida,
                "llegada": registro.llegada,
                "ciavuelo": registro.cia,
                "viaje": registro.viaje,
                "modo": registro.modo,
            })

        # field_names = [field.name for field in Conexaerea._meta.fields]
        # resultado = list(registros.values(*field_names))

        return JsonResponse({"data": resultado}, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def source_embarque_importado(request):
    try:
        data = json.loads(request.body)
        #numeros de los seguimientos
        ids = data.get('ids', [])

        registros = Cargaaerea.objects.filter(numero__in=ids)

        if not registros.exists():
            # Si no hay registros, devolver un array vacío
            return JsonResponse({"data": []}, safe=False)

        resultado = []
        for registro in registros:
            resultado.append({
                "numero": 0,
                "seguimiento_control": registro.numero,
                "producto": registro.producto.codigo,
                "bultos": registro.bultos,
                "bruto": registro.bruto,
                "tipo": registro.tipo,
                "medidas": registro.medidas,
                "cbm": registro.cbm,
                "nrocontenedor": registro.nrocontenedor,

            })

        # field_names = [field.name for field in Cargaaerea._meta.fields]
        # resultado = list(registros.values(*field_names))

        return JsonResponse({"data": resultado}, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def source_archivos_importado(request):
    try:
        data = json.loads(request.body)
        # Números de los seguimientos
        ids = data.get('ids', [])

        registros = Attachhijo.objects.filter(numero__in=ids)

        if not registros.exists():
            # Si no hay registros, devolver un array vacío
            return JsonResponse({"data": []}, safe=False)

        resultado = []
        for registro in registros:
            resultado.append({
                "numero": 0,
                "seguimiento_control": registro.numero,
                "archivo": str(registro.archivo),
                "fecha": registro.fecha
            })

        return JsonResponse({"data": resultado}, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

###

def house_detail(request):
    if request.method == 'GET':
        numero = request.GET.get('id', None)
        if numero:
            try:
                house = ExpterraEmbarqueaereo.objects.get(numero=numero)
                data = {
                    'id': house.numero,
                    'cliente_e': house.cliente,
                    'vendedor_e': house.vendedor,
                    'transportista_e': house.transportista,
                    'agente_e': house.agente,
                    'consignatario_e': house.consignatario,
                    'origen_e': house.origen,
                    'destino_e': house.destino,
                    'posicion_e': house.posicion,
                    'operacion_e': house.operacion,
                    'awb_e': house.awb,
                    'hawb_e': house.hawb,
                    'terminos_e': house.terminos,
                    'tipo_e': house.localint,
                    'pagoflete_e': house.pagoflete,
                    'moneda_e': house.moneda,
                    'arbitraje_e': house.arbitraje,
                    'embarcador_e': house.embarcador,
                    'agventas_e': house.ageventas,
                    'agcompras_e': house.agecompras,
                    'notifcliente_e': house.notifcliente,
                    'notifagente_e': house.notifagente,
                    'fecharetiro_e': house.fecharetiro,
                    'fechaembarque_e': house.fechaembarque,
                    'status_e': house.status,
                    'wreceipt_e': house.wreceipt,
                    'eta_e': house.eta,
                    'etd_e': house.etd,
                }
                return JsonResponse(data)
            except ExpterraEmbarqueaereo.DoesNotExist:
                raise Http404("House does not exist")
        else:
            return JsonResponse({'error': 'No ID provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_name_by_id_vendedores(request):
    if request.method == 'GET':
        client_id = request.GET.get('id')

        if client_id:
            vendedor = Vendedores.objects.get(codigo=client_id)
            name = vendedor.nombre

            return JsonResponse({'name': name})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def edit_house_function(request, numero):
    if request is None:
        return JsonResponse({
            'success': False,
            'message': "El objeto request es None",
            'errors': {}
        })

    house = ExpterraEmbarqueaereo.objects.get(numero=numero)
    if request.method == 'POST':
        form = edit_house(request.POST)
        if form.is_valid():
            # Asignar valores predeterminados para campos de texto o numéricos
            house.vendedor = int(form.cleaned_data.get('vendedor_i', 0)) if form.cleaned_data.get('vendedor_i') else 0
            house.transportista = int(form.cleaned_data.get('transportista_i', 0)) if form.cleaned_data.get('transportista_i') else 0
            house.agente = int(form.cleaned_data.get('agente_i', 0)) if form.cleaned_data.get('agente_i') else 0
            house.consignatario = int(form.cleaned_data.get('consignatario_i', 0)) if form.cleaned_data.get('consignatario_i') else 0
            house.cliente = int(form.cleaned_data.get('cliente_i', 0)) if form.cleaned_data.get('cliente_i') else 0
            house.agecompras = int(form.cleaned_data.get('agcompras_i', 0)) if form.cleaned_data.get('agcompras_i') else 0
            house.ageventas = int(form.cleaned_data.get('agventas_i', 0)) if form.cleaned_data.get('agventas_i') else 0
            house.embarcador = int(form.cleaned_data.get('embarcador_i', 0)) if form.cleaned_data.get('embarcador_i') else 0
            house.localint = form.cleaned_data.get('tipo', "")
            house.terminos = form.cleaned_data.get('terminos', "")
            #house.consolidado = request.POST.get('consolidado', 0)
            house.moneda = form.cleaned_data.get('moneda', 0)
            house.arbitraje = form.cleaned_data.get('arbitraje', 0) if form.cleaned_data.get('arbitraje') not in [None, ''] else 0
            house.pagoflete = form.cleaned_data.get('pago', 0)
            house.destino = form.cleaned_data.get('destino', "")
            house.origen = form.cleaned_data.get('origen', "")
            house.status = form.cleaned_data.get('status_h', "")
            house.posicion = form.cleaned_data.get('posicion_h', 0)
            house.operacion = form.cleaned_data.get('operacion', "")
            house.awd = form.cleaned_data.get('awb', "")
            house.hawb = form.cleaned_data.get('house', "")
            house.demora = form.cleaned_data.get('demora', 0) if form.cleaned_data.get('demora') else 0
            house.wreceipt = form.cleaned_data.get('wreceipt', "")
            house.etd = form.cleaned_data.get('etd', None)
            house.eta = form.cleaned_data.get('eta', None)
            house.notifagente = form.cleaned_data.get('notificar_agente', None)
            house.notifcliente = form.cleaned_data.get('notificar_cliente', None)

            try:
                house.save()
                messages.success(request, 'Datos actualizados con éxito.')
                return JsonResponse({
                    'success': True,
                    'message': 'Datos actualizados con éxito.',
                })
            except IntegrityError:
                messages.error(request, 'Error: No se pudo actualizar los datos.')
                return HttpResponseRedirect(request.path_info)

            except Exception as e:
                messages.error(request, str(e))
                return JsonResponse({
                    'success': False,
                    'message': f'Error: {str(e)}',
                    'errors': {}
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Formulario inválido, por favor revise los campos.',
                'errors': form.errors.as_json()
            })

def eliminar_house(request):
    resultado = {}
    try:
        id = request.POST['id']

        with transaction.atomic():
            embarque = ExpterraEmbarqueaereo.objects.filter(numero=id).first()
            if not embarque:
                return JsonResponse({'resultado': 'No se encontró el embarque'}, status=404)

            # guardamos el nro de seguimiento antes de limpiar
            seguimiento_num = embarque.seguimiento

            # limpiar campos en el embarque
            embarque.seguimiento = None
            embarque.posicion = 'S/I'
            embarque.consignatario = 0
            embarque.embarcador = 0
            embarque.agente = 0
            embarque.notificante = 0
            embarque.despachante = 0
            embarque.save()

            # limpiar seguimiento si existe
            if seguimiento_num:
                seguimiento = Seguimiento.objects.filter(numero=seguimiento_num).first()
                if seguimiento:
                    seguimiento.embarque = None
                    seguimiento.posicion = 'S/I'
                    seguimiento.save()

            # borrar registros relacionados
            ExpterraEmbarqueaereo.objects.filter(numero=id).delete()
            ExpterraCargaaerea.objects.filter(numero=id).delete()
            ExpterraEnvases.objects.filter(numero=id).delete()
            ExpterraConexaerea.objects.filter(numero=id).delete()
            ExpterraServiceaereo.objects.filter(numero=id).delete()

        resultado['resultado'] = 'exito'

    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)

    return JsonResponse(resultado)


def source_embarque_id(request):
    try:
        if request.method == 'POST':
            id_embarque = request.POST.get('id')

            if not id_embarque:
                return JsonResponse({'error': 'ID no proporcionada'}, status=400)

            try:
                embarque = ExpterraEmbarqueaereo.objects.get(numero=id_embarque)
                seguimiento = embarque.seguimiento
                return JsonResponse({'seguimiento': seguimiento})

            except ExpterraEmbarqueaereo.DoesNotExist:
                return JsonResponse({'error': 'Embarque no encontrado'}, status=404)

        else:
            return JsonResponse({'error': 'Método no permitido'}, status=405)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def source_seguimiento_id(request):
    try:
        if request.method == 'POST':
            numero_seg = request.POST.get('id')

            if not numero_seg:
                return JsonResponse({'error': 'ID no proporcionada'}, status=400)

            try:
                seguimiento = Seguimiento.objects.get(numero=numero_seg)
                id = seguimiento.id
                return JsonResponse({'id': id})

            except ExpterraEmbarqueaereo.DoesNotExist:
                return JsonResponse({'error': 'Embarque no encontrado'}, status=404)

        else:
            return JsonResponse({'error': 'Método no permitido'}, status=405)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)