
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from impomarit.forms import add_form
from impomarit.models import Reservas
from seguimientos.models import Seguimiento


def consultar_seguimientos(request):
    if request.method == 'POST':
        awb_number = request.POST.get('awb_number')
        seguimientos = Seguimiento.objects.filter(awb=awb_number).values('fecha', 'numero', 'cliente', 'origen', 'destino', 'status')
        data = list(seguimientos)
        return JsonResponse({'data': data})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def calcular_acumulados(request):
    pass


@login_required(login_url="/")
def add_importacion_maritima(request):

    try:
        if request.method == 'POST':
            form = add_form(request.POST)
            if form.is_valid():

                reserva = Reservas()
                reserva.numero = reserva.get_number()
                reserva.awb = form.cleaned_data['awb']
                reserva.transportista = form.cleaned_data['transportista']
                reserva.agente = form.cleaned_data['agente']
                reserva.consignatario = form.cleaned_data['consignatario']
                reserva.armador = form.cleaned_data['armador']
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
                reserva.posicion = form.cleaned_data['posicion']
                reserva.operacion = form.cleaned_data['operacion']
                reserva.save()
                messages.success(request, 'Master agregado con éxito.')
                return JsonResponse({'success': True, 'message': 'Master agregado con éxito.'})

            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Formulario invalido, intente nuevamente.',
                    'errors': form.errors.as_json()
                })

    except Exception as e:
        messages.error(request, str(e))
        return JsonResponse({
            'success': False,
            'message': f'Ocurrió un error: {str(e)}',
            'errors': {}
        })