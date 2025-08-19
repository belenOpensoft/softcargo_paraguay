import re
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.db import IntegrityError
from expmarit.forms import add_form, edit_form
from expmarit.models import ExpmaritReservas, ExpmaritEmbarqueaereo
from seguimientos.models import Seguimiento
from mantenimientos.models import Clientes
from django.db import transaction

def consultar_seguimientos(request):
    if request.method == 'POST':
        awb_number = request.POST.get('awb_number')
        seguimientos = Seguimiento.objects.filter(awb=awb_number,nroreferedi__isnull=True).values('fecha', 'numero', 'cliente', 'origen', 'destino', 'status')
        data = list(seguimientos)
        return JsonResponse({'data': data})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def add_importacion_maritima(request):
    try:
        if request.method == 'POST':
            form = add_form(request.POST)
            if form.is_valid():
                reserva = ExpmaritReservas()

                # Validar y asignar valores numéricos, asegurando que se asignen '0' si los campos están vacíos
                try:
                    reserva.transportista = int(form.cleaned_data.get('transportista_i', 0)) if form.cleaned_data.get('transportista_i') else 0
                    reserva.agente = int(form.cleaned_data.get('agente_i', 0)) if form.cleaned_data.get('agente_i') else 0
                    reserva.consignatario = int(form.cleaned_data.get('consignatario_i', 0)) if form.cleaned_data.get('consignatario_i') else 0
                    reserva.armador = int(form.cleaned_data.get('armador_i', 0)) if form.cleaned_data.get('armador_i') else 0
                except ValueError:
                    return JsonResponse({
                        'success': False,
                        'message': 'Uno o más campos tienen un formato incorrecto.',
                        'errors': {}
                    })

                # Asignar campos de texto y numéricos, rellenando con '' o 0 cuando sea necesario
                reserva.numero = reserva.get_number()
                reserva.awb = form.cleaned_data.get('awb', "")  # Si vacío, asignar ""
                reserva.vapor = form.cleaned_data.get('vapor', "")  # Si vacío, asignar ""
                reserva.viaje = form.cleaned_data.get('viaje', "")  # Si vacío, asignar ""
                reserva.aduana = form.cleaned_data.get('aduana', "")  # Si vacío, asignar ""
                reserva.tarifa = form.cleaned_data.get('tarifa', 0)  # Si vacío, asignar 0
                reserva.moneda = form.cleaned_data.get('moneda', "")  # Si vacío, asignar ""
                reserva.arbitraje = form.cleaned_data.get('arbitraje', "")  # Si vacío, asignar ""
                # reserva.kilosmadre = form.cleaned_data.get('kilosmadre', 0)  # Si vacío, asignar 0
                # reserva.bultosmadre = form.cleaned_data.get('bultosmadre', 0)  # Si vacío, asignar 0
                reserva.pagoflete = form.cleaned_data.get('pagoflete', "")  # Si vacío, asignar ""
                reserva.trafico = form.cleaned_data.get('trafico', "")  # Si vacío, asignar ""
                reserva.origen = form.cleaned_data.get('origen', "")  # Si vacío, asignar ""
                reserva.loading = form.cleaned_data.get('loading', "")  # Si vacío, asignar ""
                reserva.destino = form.cleaned_data.get('destino', "")  # Si vacío, asignar ""
                reserva.discharge = form.cleaned_data.get('discharge', "")  # Si vacío, asignar ""
                reserva.fecha = form.cleaned_data.get('fecha', None).strftime("%Y-%m-%d") if form.cleaned_data.get('fecha') else None
                reserva.cotizacion = form.cleaned_data.get('cotizacion', 0)  # Si vacío, asignar 0
                reserva.status = form.cleaned_data.get('status', "")  # Si vacío, asignar ""
                reserva.operacion = form.cleaned_data.get('operacion', "")  # Si vacío, asignar ""
                reserva.fechaingreso = datetime.now()
                reserva.posicion = generar_posicion()

                # Guardar el registro
                reserva.save()

                return JsonResponse({'success': True, 'posicion': reserva.posicion})

            else:
                # Validación del formulario fallida
                if 'awb' in form.errors:
                    return JsonResponse({
                        'success': False,
                        'code': 'DUPLICATE_AWB',
                        'message': 'Ya existe un registro con el AWB digitado.',
                        'errors': form.errors.as_json()
                    })
                return JsonResponse({
                    'success': False,
                    'message': 'Formulario inválido, intente nuevamente.',
                    'errors': form.errors.as_json()
                })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Ocurrió un error: {str(e)}',
            'errors': {}
        })

def generar_posicion():
        fecha_actual = datetime.now()
        anio_actual = fecha_actual.year
        mes_actual = fecha_actual.strftime('%m')

        ultima_reserva = ExpmaritReservas.objects.filter(fechaingreso__year=anio_actual).order_by('-numero').first()

        if ultima_reserva and ultima_reserva.posicion:
            ultima_posicion = ultima_reserva.posicion
            match = re.match(rf"EM{mes_actual}-(\d+)-\d{{4}}", ultima_posicion)

            if match:
                # Incrementar el código numérico
                ultimo_codigo = int(match.group(1))
                nuevo_codigo = str(ultimo_codigo + 1).zfill(5)
            else:
                nuevo_codigo = "00001"
        else:
            nuevo_codigo = "00001"

        nueva_posicion = f"EM{mes_actual}-{nuevo_codigo}-{anio_actual}"
        return nueva_posicion

def master_detail(request):
    if request.method == 'GET':
        master_id = request.GET.get('id', None)
        if master_id:
            try:
                master = ExpmaritReservas.objects.get(numero=master_id)
                # Convierte el objeto en un diccionario
                data = {
                    'id': master.numero,
                    'transportista_e': master.transportista,
                    'agente_e': master.agente,
                    'consignatario_e': master.consignatario,
                    'armador_e': master.armador,
                    'vapor_e': master.vapor,
                    'viaje_e': master.viaje,
                    'aduana_e': master.aduana,
                    'tarifa_e': master.tarifa,
                    'moneda_e': master.moneda,
                    'arbitraje_e': master.arbitraje,
                    'pagoflete_e': master.pagoflete,
                    'trafico_e': master.trafico,
                    'fecha_e': master.fecha,
                    'cotizacion_e': master.cotizacion,
                    'destino_e': master.destino,
                    'discharge_e': master.discharge,
                    'origen_e': master.origen,
                    'loading_e': master.loading,
                    'status_e': master.status,
                    'posicion_e': master.posicion,
                    'operacion_e': master.operacion,
                    'awd_e': master.awb,
                }
                return JsonResponse(data)
            except ExpmaritReservas.DoesNotExist:
                raise Http404("Master does not exist")
        else:
            return JsonResponse({'error': 'No ID provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
def get_name_by_id(request):
    if request.method == 'GET':
        client_id = request.GET.get('id')

        if client_id:
            cliente = Clientes.objects.get(codigo=client_id)
            name = cliente.empresa

            return JsonResponse({'name': name})

    return JsonResponse({'error': 'Invalid request'}, status=400)
def edit_master_old(request, id_master):
    if request is None:
        return JsonResponse({
            'success': False,
            'message': "El objeto request es None",
            'errors': {}
        })

    # Obtener el registro del master por id
    master = ExpmaritReservas.objects.get(numero=id_master)

    if request.method == 'POST':
        form = edit_form(request.POST)
        if form.is_valid():
            # Asignar campos numéricos y de texto, asegurando valores predeterminados en caso de estar vacíos
            master.transportista = form.cleaned_data.get('transportista_ie', 0)
            master.agente = form.cleaned_data.get('agente_ie', 0)
            master.consignatario = form.cleaned_data.get('consignatario_ie', 0)
            master.armador = form.cleaned_data.get('armador_ie', 0)
            master.vapor = form.cleaned_data.get('vapor_e', "")  # Asignar "" si está vacío

            # Manejar campos con valores predeterminados numéricos o de texto
            master.viaje = form.cleaned_data.get('viaje_e', 0) if form.cleaned_data.get('viaje_e') not in [None, ''] else 0
            master.aduana = form.cleaned_data.get('aduana_e', 'S/I')
            master.moneda = form.cleaned_data.get('moneda_e', "")
            master.tarifa = form.cleaned_data.get('tarifa_e', 0) if form.cleaned_data.get('tarifa_e') not in [None, ''] else 0
            master.arbitraje = form.cleaned_data.get('arbitraje_e', 0) if form.cleaned_data.get('arbitraje_e') not in [None, ''] else 0
            # master.bultosmadre = form.cleaned_data.get('bultosmadre_e', 0) if form.cleaned_data.get('bultosmadre_e') not in [None, ''] else 0
            # master.kilosmadre = form.cleaned_data.get('kilosmadre_e', 0) if form.cleaned_data.get('kilosmadre_e') not in [None, ''] else 0
            master.trafico = form.cleaned_data.get('trafico_e', 0) if form.cleaned_data.get('trafico_e') not in [None, ''] else 0
            master.cotizacion = form.cleaned_data.get('cotizacion_e', 0) if form.cleaned_data.get('cotizacion_e') not in [None, ''] else 0

            # Otros campos con texto
            master.pagoflete = form.cleaned_data.get('pagoflete_e', "")  # Asignar "" si está vacío
            master.fecha = form.cleaned_data.get('fecha_e', None)  # Si la fecha está vacía, asignar None
            master.destino = form.cleaned_data.get('destino_e', "")  # Asignar "" si está vacío
            master.origen = form.cleaned_data.get('origen_e', "")  # Asignar "" si está vacío
            master.loading = form.cleaned_data.get('loading_e', "")  # Asignar "" si está vacío
            master.discharge = form.cleaned_data.get('discharge_e', "")  # Asignar "" si está vacío
            master.status = form.cleaned_data.get('status_e', "")  # Asignar "" si está vacío
            master.posicion = form.cleaned_data.get('posicion_e', "")  # Asignar "" si está vacío
            master.operacion = form.cleaned_data.get('operacion_e', "")  # Asignar "" si está vacío
            master.awd = form.cleaned_data.get('awd_e', "")  # Asignar "" si está vacío

            # Guardar los cambios en la base de datos
            try:
                master.save()
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

def edit_master(request, id_master):
    try:
        if request is None:
            return JsonResponse({
                'success': False,
                'message': "El objeto request es None",
                'errors': {}
            })

        master = ExpmaritReservas.objects.get(numero=id_master)

        if request.method == 'POST':
            form = edit_form(request.POST)
            if form.is_valid():
                # Guardar valores originales antes de la modificación
                awb_original = master.awb
                transportista_original = master.transportista
                vapor_original = master.vapor

                # Nuevos valores del formulario
                awb_nuevo = form.cleaned_data.get('awd_e', "")
                transportista_nuevo = form.cleaned_data.get('transportista_ie', 0)
                vapor_nuevo = form.cleaned_data.get('vapor_e', "")

                # Asignar valores al master
                master.transportista = transportista_nuevo
                master.agente = form.cleaned_data.get('agente_ie', 0)
                master.consignatario = form.cleaned_data.get('consignatario_ie', 0)
                master.armador = form.cleaned_data.get('armador_ie', 0)
                master.vapor = vapor_nuevo

                master.viaje = form.cleaned_data.get('viaje_e', 0) if form.cleaned_data.get('viaje_e') not in [None, ''] else 0
                master.aduana = form.cleaned_data.get('aduana_e', 'S/I')
                master.moneda = form.cleaned_data.get('moneda_e', "")
                master.tarifa = form.cleaned_data.get('tarifa_e', 0) if form.cleaned_data.get('tarifa_e') not in [None, ''] else 0
                master.arbitraje = form.cleaned_data.get('arbitraje_e', 0) if form.cleaned_data.get('arbitraje_e') not in [None, ''] else 0
                master.trafico = form.cleaned_data.get('trafico_e', 0) if form.cleaned_data.get('trafico_e') not in [None, ''] else 0
                master.cotizacion = form.cleaned_data.get('cotizacion_e', 0) if form.cleaned_data.get('cotizacion_e') not in [None, ''] else 0

                master.pagoflete = form.cleaned_data.get('pagoflete_e', "")
                master.fecha = form.cleaned_data.get('fecha_e', None)
                master.destino = form.cleaned_data.get('destino_e', "")
                master.origen = form.cleaned_data.get('origen_e', "")
                master.loading = form.cleaned_data.get('loading_e', "")
                master.discharge = form.cleaned_data.get('discharge_e', "")
                master.status = form.cleaned_data.get('status_e', "")
                master.posicion = form.cleaned_data.get('posicion_e', "")
                master.operacion = form.cleaned_data.get('operacion_e', "")
                master.awb = awb_nuevo

                # Guardar cambios y actualizar los houses si corresponde
                try:
                    with transaction.atomic():
                        master.save()

                        if (
                            awb_nuevo != awb_original or
                            transportista_nuevo != transportista_original or
                            vapor_nuevo != vapor_original
                        ):
                            houses = ExpmaritEmbarqueaereo.objects.filter(awb=awb_original)
                            for house in houses:
                                if awb_nuevo != awb_original:
                                    house.awb = awb_nuevo
                                if transportista_nuevo != transportista_original:
                                    house.transportista = transportista_nuevo
                                if vapor_nuevo != vapor_original:
                                    house.vapor = vapor_nuevo
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
    except Exception as e:
        messages.error(request, str(e))
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}',
            'errors': {}
        })
