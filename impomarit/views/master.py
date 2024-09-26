import re
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.db import IntegrityError
from impomarit.forms import add_form, edit_form
from impomarit.models import Reservas
from seguimientos.models import Seguimiento
from mantenimientos.models import Clientes


def consultar_seguimientos(request):
    if request.method == 'POST':
        awb_number = request.POST.get('awb_number')
        seguimientos = Seguimiento.objects.filter(awb=awb_number).values('fecha', 'numero', 'cliente', 'origen', 'destino', 'status')
        data = list(seguimientos)
        return JsonResponse({'data': data})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
@login_required(login_url="/")
def add_importacion_maritima(request):

    try:
        if request.method == 'POST':
            form = add_form(request.POST)
            if form.is_valid():

                reserva = Reservas()
                try:
                    reserva.transportista = int(form.cleaned_data.get('transportista_i', 0))
                    reserva.agente = int(form.cleaned_data.get('agente_i', 0))
                    reserva.consignatario = int(form.cleaned_data.get('consignatario_i', 0))
                    reserva.armador = int(form.cleaned_data.get('armador_i', 0))
                except ValueError:
                    return JsonResponse({
                        'success': False,
                        'message': 'Uno o más campos tienen un formato incorrecto.',
                        'errors': {}
                    })

                reserva.numero = reserva.get_number()
                reserva.awb = form.cleaned_data['awb']
                reserva.vapor = form.cleaned_data['vapor']
                reserva.viaje = form.cleaned_data['viaje']
                reserva.aduana = form.cleaned_data['aduana']
                reserva.tarifa = form.cleaned_data['tarifa']
                reserva.moneda = form.cleaned_data['moneda']
                reserva.arbitraje = form.cleaned_data['arbitraje']
                reserva.kilosmadre = form.cleaned_data['kilosmadre']
                reserva.bultosmadre = form.cleaned_data['bultosmadre']
                reserva.pagoflete = form.cleaned_data['pagoflete']
                reserva.trafico = form.cleaned_data['trafico']
                reserva.origen = form.cleaned_data['origen']
                reserva.loading = form.cleaned_data['loading']
                reserva.destino = form.cleaned_data['destino']
                reserva.discharge = form.cleaned_data['discharge']
                reserva.fecha = form.cleaned_data['fecha'].strftime("%Y-%m-%d")
                reserva.cotizacion = form.cleaned_data['cotizacion']
                reserva.status = form.cleaned_data['status']
                reserva.operacion = form.cleaned_data['operacion']
                reserva.fechaingreso = datetime.now()
                reserva.posicion=generar_posicion()
                reserva.save()
                messages.success(request, 'Master agregado con éxito.')
               # return JsonResponse({'success': True, 'message': 'Master agregado con éxito.'})
                return JsonResponse({'success': True, 'posicion': reserva.posicion})

            else:
                if 'awb' in form.errors:
                    return JsonResponse({
                        'success': False,
                        'code': 'DUPLICATE_AWB',
                        'message': 'Ya existe un registro con el Master digitado.',
                        'errors': form.errors.as_json()
                    })
                return JsonResponse({
                    'success': False,
                    'message': 'Formulario inválido, intente nuevamente.',
                    'errors': form.errors.as_json()
                })

    except Exception as e:
        messages.error(request, str(e))
        return JsonResponse({
            'success': False,
            'message': f'Ocurrió un error: {str(e)}',
            'errors': {}
        })

def generar_posicion():
        fecha_actual = datetime.now()
        anio_actual = fecha_actual.year
        mes_actual = fecha_actual.strftime('%m')

        ultima_reserva = Reservas.objects.filter(fechaingreso__year=anio_actual).order_by('-id').first()

        if ultima_reserva and ultima_reserva.posicion:
            ultima_posicion = ultima_reserva.posicion
            match = re.match(rf"IM{mes_actual}-(\d+)-\d{{4}}", ultima_posicion)

            if match:
                # Incrementar el código numérico
                ultimo_codigo = int(match.group(1))
                nuevo_codigo = str(ultimo_codigo + 1).zfill(5)
            else:
                nuevo_codigo = "00001"
        else:
            nuevo_codigo = "00001"

        nueva_posicion = f"IM{mes_actual}-{nuevo_codigo}-{anio_actual}"
        return nueva_posicion

def master_detail(request):
    if request.method == 'GET':
        master_id = request.GET.get('id', None)
        if master_id:
            try:
                master = Reservas.objects.get(id=master_id)
                # Convierte el objeto en un diccionario
                data = {
                    'id': master.id,
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
                    'kilosmadre_e': master.kilosmadre,
                    'bultosmadre_e': master.bultosmadre,
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
            except Reservas.DoesNotExist:
                raise Http404("Master does not exist")
        else:
            return JsonResponse({'error': 'No ID provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
def get_name_by_id(request):
    if request.method == 'GET':
        client_id = request.GET.get('id')

        if client_id:
            cliente = Clientes.objects.get(id=client_id)
            name = cliente.empresa

            return JsonResponse({'name': name})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def edit_master(request, id_master):
    if request is None:
        return JsonResponse({
            'success': False,
            'message': "El objeto request es None",
            'errors': {}
        })

    master = Reservas.objects.get(id=id_master)
    if request.method == 'POST':
        form = edit_form(request.POST)
        if form.is_valid():
            master.transportista = form.cleaned_data['transportista_ie']
            master.agente = form.cleaned_data['agente_ie']
            master.consignatario = form.cleaned_data['consignatario_ie']
            master.armador = form.cleaned_data['armador_ie']
            master.vapor = form.cleaned_data['vapor_e']

            master.viaje = form.cleaned_data.get('viaje_e', 0) if form.cleaned_data.get('viaje_e') not in [None,''] else 0
            master.aduana = form.cleaned_data.get('aduana_e', 'S/I')
            master.moneda = form.cleaned_data['moneda_e']
            master.tarifa = form.cleaned_data.get('tarifa_e', 0) if form.cleaned_data.get('tarifa_e') not in [None,''] else 0
            master.arbitraje = form.cleaned_data.get('arbitraje_e', 0) if form.cleaned_data.get('arbitraje_e') not in [None, ''] else 0
            master.bultosmadre = form.cleaned_data.get('bultosmadre_e', 0) if form.cleaned_data.get('bultosmadre_e') not in [None, ''] else 0
            master.kilosmadre = form.cleaned_data.get('kilosmadre_e', 0) if form.cleaned_data.get('kilosmadre_e') not in [None, ''] else 0
            master.trafico = form.cleaned_data.get('trafico_e', 0) if form.cleaned_data.get('trafico_e') not in [None,''] else 0
            master.cotizacion = form.cleaned_data.get('cotizacion_e', 0) if form.cleaned_data.get('cotizacion_e') not in [None, ''] else 0

            master.pagoflete = form.cleaned_data['pagoflete_e']
            master.fecha = form.cleaned_data['fecha_e']
            master.destino = form.cleaned_data['destino_e']
            master.origen = form.cleaned_data['origen_e']
            master.loading = form.cleaned_data['loading_e']
            master.discharge = form.cleaned_data['discharge_e']
            master.status = form.cleaned_data['status_e']
            master.posicion = form.cleaned_data['posicion_e']
            master.operacion = form.cleaned_data['operacion_e']
            master.awd = form.cleaned_data['awd_e']


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