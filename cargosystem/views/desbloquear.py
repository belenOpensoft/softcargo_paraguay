# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from impomarit.models import BloqueoEdicion


@login_required
@require_POST
def desbloquear(request):
    numero_embarque = request.POST.get('numero_embarque', '').strip()
    numero_master = request.POST.get('numero_master', '').strip()
    id_seguimiento = request.POST.get('id_seguimiento', '').strip()
    ruta_actual = request.POST.get('ruta', '').strip()

    # Extraer módulo de la ruta
    partes = ruta_actual.strip('/').split('/')
    modulo = partes[0] if len(partes) >= 2 else None

    if not numero_master and not numero_master and not id_seguimiento:
        return JsonResponse({'status': 'error', 'message': 'Parámetros faltantes'})

    desbloqueados = 0

    if numero_embarque and modulo:
        desbloqueados += BloqueoEdicion.objects.filter(
            referencia=numero_embarque,
            fecha_expiracion__gt=now(),
            activo=True,
            modulo=modulo,
            usuario=request.user
        ).update(activo=False)

    if numero_master and modulo:
        desbloqueados += BloqueoEdicion.objects.filter(
            referencia=numero_master,
            fecha_expiracion__gt=now(),
            activo=True,
            modulo=modulo,
            usuario=request.user
        ).update(activo=False)

    if id_seguimiento and not modulo:
        desbloqueados += BloqueoEdicion.objects.filter(
            referencia=id_seguimiento,
            fecha_expiracion__gt=now(),
            activo=True,
            modulo='seguimientos',
            usuario=request.user
        ).update(activo=False) # desbloqueo todos los bloqueos asociados al seguimiento

    return JsonResponse({'status': 'ok', 'desbloqueados': desbloqueados})
