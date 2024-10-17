from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from impomarit.models import VistaEventosCalendario


@login_required(login_url='/')
def calendario(request):
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
            return render(request, 'impormarit/calendar_general.html',{

            })
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')


def eventos_calendario(request):
    eventos = VistaEventosCalendario.objects.all()

    eventos_formateados = []
    for evento in eventos:
        titulo = f"{evento.posicion} - {evento.hawb}"

        if evento.source == 'impmarit':
            titulo += " (IMPORT MARÍTIMO)"
            color = '#ADD8E6'  # Azul claro para marítimo
            source_formatted = "IMPO MARÍTIMO"
        elif evento.source == 'import':
            titulo += " (IMPORT AÉREO)"
            color = '#90EE90'  # Verde claro para aéreo
            source_formatted = "IMPO AÉREO"

        if evento.fecharetiro is not None:
            fecha_evento = evento.fecharetiro.strftime('%Y-%m-%d')
        else:
            fecha_evento = None

        if fecha_evento:
            # Agregar todos los campos relevantes al evento formateado
            eventos_formateados.append({
                'title': titulo,
                'start': fecha_evento,
                'color': color,
                'awb': evento.awb,
                'hawb': evento.hawb,
                'status': evento.status,
                'origen': evento.origen,
                'destino': evento.destino,
                'transportista': evento.transportista,
                'consignatario': evento.consignatario,
                'source_formatted': source_formatted,
                'posicion': evento.posicion,
            })

    return JsonResponse(eventos_formateados, safe=False)



