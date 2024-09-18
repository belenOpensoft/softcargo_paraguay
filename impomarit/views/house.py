from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from impomarit.models import Embarqueaereo
from django.http import JsonResponse
from django.contrib import messages
from impomarit.forms import add_house

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
                reserva.hawb = form.cleaned_data['house']
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