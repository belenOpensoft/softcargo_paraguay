from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from impomarit.models import Embarqueaereo
from mantenimientos.models import Vendedores
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from impomarit.forms import add_house, edit_house
from seguimientos.models import Seguimiento


@login_required(login_url="/")
def add_house_impmarit(request):
    try:
        if request.method == 'POST':
            form = add_house(request.POST)
            if form.is_valid():
                reserva = Embarqueaereo()

                reserva.numero = reserva.get_number()
                reserva.awb = form.cleaned_data['awb']
                reserva.notifcliente = form.cleaned_data['notificar_cliente']
                reserva.notifagente = form.cleaned_data['notificar_agente']
                reserva.fecharetiro = form.cleaned_data['fecha_retiro']
                reserva.fechaembarque = form.cleaned_data['fecha_embarque']
                reserva.origen = form.cleaned_data['origen']
                reserva.destino = form.cleaned_data['destino']
                reserva.moneda = form.cleaned_data['moneda']
                reserva.loading = form.cleaned_data['loading']
                reserva.discharge = form.cleaned_data['discharge']
                reserva.pago = form.cleaned_data['pago']
                reserva.vapor = form.cleaned_data['vapor']
                reserva.viaje = form.cleaned_data['viaje']
                reserva.hawb = form.cleaned_data['house']
                reserva.demora = form.cleaned_data['demora']
                reserva.operacion = form.cleaned_data['operacion']
                reserva.arbitraje = form.cleaned_data['arbitraje']
                reserva.trackid = form.cleaned_data['trackid']
                reserva.wreceipt = form.cleaned_data['wreceipt']
                reserva.posicion = form.cleaned_data['posicion_h']
                reserva.status = form.cleaned_data['status_h']

                reserva.transportista = form.cleaned_data.get('transportista', None)
                reserva.agente = form.cleaned_data.get('agente', None)
                reserva.consignatario = form.cleaned_data.get('consignatario', None)
                reserva.armador = form.cleaned_data.get('armador', None)
                reserva.cliente = form.cleaned_data.get('cliente', None)
                try:
                    reserva.vendedor = int(form.cleaned_data.get('vendedor_i', 0)) if form.cleaned_data.get('vendedor_i', 0) is not None else 0
                    reserva.transportista = int(form.cleaned_data.get('transportista_i', 0)) if form.cleaned_data.get('transportista_i', 0) is not None else 0
                    reserva.agente = int(form.cleaned_data.get('agente_i', 0)) if form.cleaned_data.get('agente_i', 0) is not None else 0
                    reserva.consignatario = int(form.cleaned_data.get('consignatario_i', 0)) if form.cleaned_data.get('consignatario_i', 0) is not None else 0
                    reserva.armador = int(form.cleaned_data.get('armador_i', 0)) if form.cleaned_data.get('armador_i', 0) is not None else 0
                    reserva.cliente = int(form.cleaned_data.get('cliente_i', 0)) if form.cleaned_data.get('cliente_i', 0) is not None else 0
                    reserva.agecompras = int(form.cleaned_data.get('agcompras_i', 0)) if form.cleaned_data.get('agcompras_i', 0) is not None else 0
                    reserva.embarcador = int(form.cleaned_data.get('embarcador_i', 0)) if form.cleaned_data.get('embarcador_i', 0) is not None else 0
                    agev = form.cleaned_data.get('agventas_i', 0)
                    if agev is not None and len(agev) > 0:
                        reserva.ageventas = int(agev)

                except ValueError as e:
                    return JsonResponse({
                        'success': False,
                        'message': 'Uno o más campos tienen un formato incorrecto.',
                        'errors': {}
                    })

                reserva.save()
                if reserva.pk:
                    return JsonResponse({'success': True, 'message': 'house agregado'})
                else:
                    return JsonResponse({'success': False, 'message': 'no'})

            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Formulario inválido, por favor revise los campos.',
                    'errors': form.errors.as_json()
                })

    except Exception as e:
        messages.error(request, str(e))
        return JsonResponse({
            'success': False,
            'message': f'Ocurrió un error: {str(e)}',
            'errors': {}
        })

def add_house_importado(request):
    try:
        if request.method == 'POST':
            # Asumimos que el array de datos llega en formato JSON
            data = json.loads(request.body)

            if isinstance(data, list):
                # Iteramos sobre cada elemento en la lista
                for house_data in data:
                    # Crear la instancia de Embarqueaereo para cada registro
                    reserva = Embarqueaereo()

                    reserva.numero = reserva.get_number()
                    reserva.awb = house_data.get('awb')
                    reserva.notifcliente = house_data.get('notificar_cliente')
                    reserva.notifagente = house_data.get('notificar_agente')
                    reserva.fecharetiro = house_data.get('fecha_retiro')
                    reserva.fechaembarque = house_data.get('fecha_embarque')
                    reserva.origen = house_data.get('origen')
                    reserva.destino = house_data.get('destino')
                    reserva.moneda = house_data.get('moneda')
                    reserva.loading = house_data.get('loading')
                    reserva.discharge = house_data.get('discharge')
                    reserva.vapor = house_data.get('vapor')
                    reserva.viaje = house_data.get('viaje')
                    reserva.hawb = house_data.get('house')
                    reserva.demora = house_data.get('demora')
                    reserva.operacion = house_data.get('operacion')
                    reserva.arbitraje = house_data.get('arbitraje')
                    reserva.trackid = house_data.get('trackid')
                    reserva.wreceipt = house_data.get('wreceipt')
                    reserva.posicion = house_data.get('posicion_h')
                    reserva.status = house_data.get('status_h')

                    reserva.transportista = house_data.get('transportista')
                    reserva.agente = house_data.get('agente')
                    reserva.consignatario = house_data.get('consignatario')
                    reserva.armador = house_data.get('armador')
                    reserva.cliente = house_data.get('cliente')
                    reserva.vendedor = house_data.get('vendedor')
                    reserva.agecompras = house_data.get('agcompras')
                    reserva.ageventas = house_data.get('agventas')
                    reserva.embarcador = house_data.get('embarcador')

                    reserva.save()

                return JsonResponse({'success': True, 'message': 'Todos los houses agregados con éxito'})
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

def source_seguimientos_importado(request):

        try:
            data = json.loads(request.body)
            ids = data.get('ids', [])

            registros = Seguimiento.objects.filter(id__in=ids)


            resultado = []
            for registro in registros:
                resultado.append({
                    "awb": 0,
                    "posicion": 0,
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
                    "trackid": registro.trackid,
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
                    "agventas": registro.ageventas
                })

            return JsonResponse({"data": resultado}, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


def house_detail(request):
    if request.method == 'GET':
        numero = request.GET.get('id', None)
        if numero:
            try:
                house = Embarqueaereo.objects.get(numero=numero)
                data = {
                    'id': house.id,
                    'cliente_e': house.cliente,
                    'vendedor_e': house.vendedor,
                    'transportista_e': house.transportista,
                    'agente_e': house.agente,
                    'consignatario_e': house.consignatario,
                    'origen_e': house.origen,
                    'loading_e': house.loading,
                    'destino_e': house.destino,
                    'discharge_e': house.discharge,
                    'posicion_e': house.posicion,
                    'operacion_e': house.operacion,
                    'awb_e': house.awb,
                    'hawb_e': house.hawb,
                    'vapor_e': house.vapor,
                    'viaje_e': house.viaje,
                    'pagoflete_e': house.pago,
                    'moneda_e': house.moneda,
                    'arbitraje_e': house.arbitraje,
                    'demora_e': house.demora,
                    'embarcador_e': house.embarcador,
                    'armador_e': house.armador,
                    'agventas_e': house.ageventas,
                    'agcompras_e': house.arbitraje,
                    'notifcliente_e': house.notifcliente,
                    'notifagente_e': house.notifagente,
                    'fecharetiro_e': house.fecharetiro,
                    'fechaembarque_e': house.fechaembarque,
                    'status_e': house.status,
                    'wreceipt_e': house.wreceipt,
                    'trackid_e': house.trackid,
                }
                return JsonResponse(data)
            except Embarqueaereo.DoesNotExist:
                raise Http404("House does not exist")
        else:
            return JsonResponse({'error': 'No ID provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_name_by_id_vendedores(request):
    if request.method == 'GET':
        client_id = request.GET.get('id')

        if client_id:
            vendedor = Vendedores.objects.get(id=client_id)
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

    house = Embarqueaereo.objects.get(numero=numero)
    if request.method == 'POST':
        form = edit_house(request.POST)
        if form.is_valid():
            #30 campos
            house.transportista = form.cleaned_data['transportista_i']
            house.agente = form.cleaned_data['agente_i']
            house.consignatario = form.cleaned_data['consignatario_i']
            house.armador = form.cleaned_data['armador_i']
            house.transportista = form.cleaned_data['embarcador_i']
            house.agente = form.cleaned_data['cliente_i']
            house.consignatario = form.cleaned_data['vendedor_i']
            house.ageventas = form.cleaned_data['agventas_i']
            house.agecompras = form.cleaned_data['agcompras_i']

            house.vapor = form.cleaned_data['vapor']
            house.viaje = form.cleaned_data.get('viaje', 0) if form.cleaned_data.get('viaje') not in [None,''] else 0
            house.moneda = form.cleaned_data['moneda']
            house.arbitraje = form.cleaned_data.get('arbitraje', 0) if form.cleaned_data.get('arbitraje') not in [None, ''] else 0
            house.pago = form.cleaned_data['pago']
            house.destino = form.cleaned_data['destino']
            house.origen = form.cleaned_data['origen']
            house.loading = form.cleaned_data['loading']
            house.discharge = form.cleaned_data['discharge']
            house.status = form.cleaned_data['status_h']
            house.posicion = form.cleaned_data['posicion_h']
            house.operacion = form.cleaned_data['operacion']
            house.awd = form.cleaned_data['awb']
            house.hawd = form.cleaned_data['house']
            house.demora = form.cleaned_data['demora']
            house.wreceipt = form.cleaned_data['wreceipt']
            house.trackid = form.cleaned_data['trackid']
            house.fecharetiro = form.cleaned_data['fecha_retiro']
            house.fechaembarque = form.cleaned_data['fecha_embarque']
            house.notifagente = form.cleaned_data['notificar_agente']
            house.notifcliente = form.cleaned_data['notificar_cliente']

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