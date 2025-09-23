import re
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.db import IntegrityError
from expaerea.forms import add_form, edit_form
from expaerea.models import ExportReservas, ExportEmbarqueaereo
from expterrestre.models import ExpterraEmbarqueaereo
from seguimientos.models import Seguimiento
from mantenimientos.models import Clientes, Guias
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
                reserva = ExportReservas()

                # Validar y asignar valores numéricos, asegurando que se asignen '0' si los campos están vacíos

                reserva.transportista = int(form.cleaned_data.get('transportista_i', 0)) if form.cleaned_data.get('transportista_i') else 0
                reserva.agente = int(form.cleaned_data.get('agente_i', 0)) if form.cleaned_data.get('agente_i') else 0
                reserva.consignatario = int(form.cleaned_data.get('consignatario_i', 0)) if form.cleaned_data.get('consignatario_i') else 0
                # Asignar campos de texto y numéricos, rellenando con '' o 0 cuando sea necesario
                reserva.numero = reserva.get_number()
                reserva.awb = form.cleaned_data.get('awb', "")  # Si vacío, asignar ""
                reserva.aduana = form.cleaned_data.get('aduana', "")  # Si vacío, asignar ""
                reserva.tarifaawb = form.cleaned_data.get('tarifa', 0)  # Si vacío, asignar 0
                reserva.moneda = form.cleaned_data.get('moneda', "")  # Si vacío, asignar ""
                reserva.arbitraje = form.cleaned_data.get('arbitraje', "")  # Si vacío, asignar ""
                reserva.kilos = form.cleaned_data.get('kilos', 0)  # Si vacío, asignar 0
                reserva.pagoflete = form.cleaned_data.get('pagoflete', "")  # Si vacío, asignar ""
                reserva.trafico = form.cleaned_data.get('trafico', "")  # Si vacío, asignar ""
                reserva.origen = form.cleaned_data.get('origen', "")  # Si vacío, asignar ""
                reserva.destino = form.cleaned_data.get('destino', "")  # Si vacío, asignar ""
                reserva.fecha = form.cleaned_data.get('fecha', None).strftime("%Y-%m-%d") if form.cleaned_data.get('fecha') else None
                reserva.cotizacion = form.cleaned_data.get('cotizacion', 0)  # Si vacío, asignar 0
                reserva.status = form.cleaned_data.get('status', "")  # Si vacío, asignar ""
                reserva.operacion = form.cleaned_data.get('operacion', "")  # Si vacío, asignar ""
                reserva.volumen = form.cleaned_data.get('volumen',0)
                reserva.aplicable = form.cleaned_data.get('aplicable',0)
                reserva.fechaingreso = datetime.now()
                reserva.posicion = generar_posicion()
                numero=form.cleaned_data.get('numero_guia',0)
                prefijo = form.cleaned_data.get('prefijo_guia', 0)
                reserva.notas = form.cleaned_data.get('radio', "")

                if reserva.status != 'CANCELADO':
                    try:
                        guia = Guias.objects.get(numero=numero, prefijo=prefijo)
                    except Guias.DoesNotExist:
                        # Manejar el caso en que no se encuentra la guía
                        guia = None

                    guia.estado = 1
                    guia.save()
                else:
                    reserva.awb+='singuia'
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

        ultima_reserva = ExportReservas.objects.filter(fechaingreso__year=anio_actual).order_by('-numero').first()

        if ultima_reserva and ultima_reserva.posicion:
            ultima_posicion = ultima_reserva.posicion
            match = re.match(rf"EA{mes_actual}-(\d+)-\d{{4}}", ultima_posicion)

            if match:
                # Incrementar el código numérico
                ultimo_codigo = int(match.group(1))
                nuevo_codigo = str(ultimo_codigo + 1).zfill(5)
            else:
                nuevo_codigo = "00001"
        else:
            nuevo_codigo = "00001"

        nueva_posicion = f"EA{mes_actual}-{nuevo_codigo}-{anio_actual}"
        return nueva_posicion

def master_detail(request):
    if request.method == 'GET':
        master_id = request.GET.get('id', None)
        if master_id:
            try:
                master = ExportReservas.objects.get(numero=master_id)
                # Convierte el objeto en un diccionario
                data = {
                    'id': master.numero,
                    'transportista_e': master.transportista,
                    'agente_e': master.agente,
                    'consignatario_e': master.consignatario,
                    'aduana_e': master.aduana,
                    'tarifa_e': round(float(master.tarifaawb),2) if master.tarifaawb else 0,
                    'moneda_e': master.moneda,
                    'arbitraje_e': master.arbitraje,
                    'kilos_e': master.kilos,
                    'aplicable_e':master.aplicable,
                    'volumen_e':master.volumen,
                    'radio':master.notas,
                    'pagoflete_e': master.pagoflete,
                    'trafico_e': master.trafico,
                    'fecha_e': master.fecha,
                    'cotizacion_e': master.cotizacion,
                    'destino_e': master.destino,
                    'origen_e': master.origen,
                    'status_e': master.status,
                    'posicion_e': master.posicion,
                    'operacion_e': master.operacion,
                    'awd_e': master.awb,
                }
                return JsonResponse(data)
            except ExportReservas.DoesNotExist:
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
    master = ExportReservas.objects.get(numero=id_master)

    if request.method == 'POST':
        form = edit_form(request.POST)
        try:
            if form.is_valid():
                # Asignar campos numéricos y de texto, asegurando valores predeterminados en caso de estar vacíos
                master.transportista = form.cleaned_data.get('transportista_ie', 0)
                master.agente = form.cleaned_data.get('agente_ie', 0)
                master.consignatario = form.cleaned_data.get('consignatario_ie', 0)

                master.aduana = form.cleaned_data.get('aduana_e', 'S/I')
                master.moneda = form.cleaned_data.get('moneda_e', "")
                master.tarifaawb = form.cleaned_data.get('tarifa_e', 0) if form.cleaned_data.get('tarifa_e') not in [None, ''] else 0
                master.arbitraje = form.cleaned_data.get('arbitraje_e', 0) if form.cleaned_data.get('arbitraje_e') not in [None, ''] else 0
                master.kilos = form.cleaned_data.get('kilos_e', 0) if form.cleaned_data.get('kilos_e') not in [None, ''] else 0
                master.trafico = form.cleaned_data.get('trafico_e', 0) if form.cleaned_data.get('trafico_e') not in [None, ''] else 0
                master.cotizacion = form.cleaned_data.get('cotizacion_e', 0) if form.cleaned_data.get('cotizacion_e') not in [None, ''] else 0

                # Otros campos con texto
                master.pagoflete = form.cleaned_data.get('pagoflete_e', "")  # Asignar "" si está vacío
                master.fecha = form.cleaned_data.get('fecha_e', None)  # Si la fecha está vacía, asignar None
                master.destino = form.cleaned_data.get('destino_e', "")  # Asignar "" si está vacío
                master.origen = form.cleaned_data.get('origen_e', "")  # Asignar "" si está vacío
                master.status = form.cleaned_data.get('status_e', "")  # Asignar "" si está vacío
                master.posicion = form.cleaned_data.get('posicion_e', "")  # Asignar "" si está vacío
                master.operacion = form.cleaned_data.get('operacion_e', "")  # Asignar "" si está vacío
                master.awb = form.cleaned_data.get('awd_e', "")  # Asignar "" si está vacío
                master.volumen = form.cleaned_data.get('volumen',0)
                master.aplicable = form.cleaned_data.get('aplicable',0)
                numero=form.cleaned_data.get('numero_guia',0)
                prefijo = form.cleaned_data.get('prefijo_guia', 0)
                numero_old=form.cleaned_data.get('numero_old',0)
                prefijo_old = form.cleaned_data.get('prefijo_old', 0)
                master.notas=form.cleaned_data.get('radio',"")

                if numero_old != numero or prefijo_old !=prefijo:
                    #si cambio el master
                    try:
                        guia = Guias.objects.get(numero=numero, prefijo=prefijo)
                    except Guias.DoesNotExist:
                        guia = None

                    guia.estado = 1
                    guia.save()

                    try:
                        guia_old = Guias.objects.get(numero=numero_old, prefijo=prefijo_old)
                    except Guias.DoesNotExist:
                        guia_old = None

                    guia_old.estado = 0
                    guia_old.save()

                if master.status == 'CANCELADO':
                    # si cambio el master a cancelado
                    try:
                        guia = Guias.objects.get(numero=numero, prefijo=prefijo)
                    except Guias.DoesNotExist:
                        guia = None

                    guia.estado = 0
                    guia.save()

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
            else:
                # Devolver los errores del formulario
                return JsonResponse({
                    'success': False,
                    'message': 'Formulario inválido.',
                    'errors': form.errors  # Mostrar los errores del formulario
                })
        except Exception as e:
            messages.error(request, str(e))
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}',
                'errors': {}
            })

def edit_master(request, id_master):
    if request is None:
        return JsonResponse({
            'success': False,
            'message': "El objeto request es None",
            'errors': {}
        })

    master = ExportReservas.objects.get(numero=id_master)

    if request.method == 'POST':
        form = edit_form(request.POST)
        try:
            if form.is_valid():
                # Guardar valores originales
                awb_original = master.awb
                transportista_original = master.transportista

                # Nuevos datos del formulario
                transportista_nuevo = form.cleaned_data.get('transportista_ie', 0)
                numero = str(form.cleaned_data.get('numero_guia', 0))
                prefijo = str(form.cleaned_data.get('prefijo_guia', 0))
                numero_old = str(form.cleaned_data.get('numero_old', 0))
                prefijo_old = str(form.cleaned_data.get('prefijo_old', 0))

                awb_nuevo = prefijo + '-' + numero
                awb_anterior = prefijo_old + '-' + numero_old

                # Asignación de datos
                master.transportista = transportista_nuevo
                master.agente = form.cleaned_data.get('agente_ie', 0)
                master.consignatario = form.cleaned_data.get('consignatario_ie', 0)
                master.aduana = form.cleaned_data.get('aduana_e', 'S/I')
                master.moneda = form.cleaned_data.get('moneda_e', "")
                master.tarifaawb = form.cleaned_data.get('tarifa_e', 0) if form.cleaned_data.get('tarifa_e') not in [None, ''] else 0
                master.arbitraje = form.cleaned_data.get('arbitraje_e', 0) if form.cleaned_data.get('arbitraje_e') not in [None, ''] else 0
                master.kilos = form.cleaned_data.get('kilos_e', 0) if form.cleaned_data.get('kilos_e') not in [None, ''] else 0
                master.trafico = form.cleaned_data.get('trafico_e', 0) if form.cleaned_data.get('trafico_e') not in [None, ''] else 0
                master.cotizacion = form.cleaned_data.get('cotizacion_e', 0) if form.cleaned_data.get('cotizacion_e') not in [None, ''] else 0
                master.pagoflete = form.cleaned_data.get('pagoflete_e', "")
                master.fecha = form.cleaned_data.get('fecha_e', None)
                master.destino = form.cleaned_data.get('destino_e', "")
                master.origen = form.cleaned_data.get('origen_e', "")
                master.status = form.cleaned_data.get('status_e', "")
                master.posicion = form.cleaned_data.get('posicion_e', "")
                master.operacion = form.cleaned_data.get('operacion_e', "")
                master.awb = awb_nuevo
                master.volumen = form.cleaned_data.get('volumen', 0)
                master.aplicable = form.cleaned_data.get('aplicable', 0)
                master.notas = form.cleaned_data.get('radio', "")

                # Si cambió la guía
                if numero_old != numero or prefijo_old != prefijo:
                    try:
                        guia = Guias.objects.get(numero=numero, prefijo=prefijo)
                        guia.estado = 1
                        guia.save()
                    except Guias.DoesNotExist:
                        pass

                    try:
                        guia_old = Guias.objects.get(numero=numero_old, prefijo=prefijo_old)
                        guia_old.estado = 0
                        guia_old.save()
                    except Guias.DoesNotExist:
                        pass

                # Si se cancela el master
                if master.status == 'CANCELADO':
                    try:
                        guia = Guias.objects.get(numero=numero, prefijo=prefijo)
                        guia.estado = 0
                        guia.save()
                    except Guias.DoesNotExist:
                        pass

                try:
                    with transaction.atomic():
                        master.save()

                        # Si cambia transportista o awb, actualizar los houses
                        if awb_nuevo != awb_original or transportista_nuevo != transportista_original:
                            houses = ExportEmbarqueaereo.objects.filter(awb=awb_anterior)
                            for house in houses:
                                if awb_nuevo != awb_original:
                                    house.awb = awb_nuevo
                                if transportista_nuevo != transportista_original:
                                    house.transportista = transportista_nuevo
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
                    'message': 'Formulario inválido.',
                    'errors': form.errors.as_json()
                })
        except Exception as e:
            messages.error(request, str(e))
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}',
                'errors': {}
            })

