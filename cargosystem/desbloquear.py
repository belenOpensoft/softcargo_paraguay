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
    ruta_actual = request.POST.get('ruta', '').strip()

    # Extraer módulo de la ruta
    partes = ruta_actual.strip('/').split('/')
    modulo = partes[0] if len(partes) >= 2 else 'operaciones'

    if not modulo or (not numero_embarque and not numero_master):
        return JsonResponse({'status': 'error', 'message': 'Parámetros faltantes'})

    desbloqueados = 0

    if numero_embarque:
        bloqueo = BloqueoEdicion.objects.filter(
            referencia=numero_embarque,
            formulario='embarque',
            fecha_expiracion__gt=now(),
            activo=True,
            modulo=modulo,
            usuario=request.user
        ).first()
        if bloqueo:
            bloqueo.activo = False
            bloqueo.save()
            desbloqueados += 1

    if numero_master:
        bloqueo = BloqueoEdicion.objects.filter(
            referencia=numero_master,
            formulario='master',
            fecha_expiracion__gt=now(),
            activo=True,
            modulo=modulo,
            usuario=request.user
        ).first()
        if bloqueo:
            bloqueo.activo = False
            bloqueo.save()
            desbloqueados += 1

    return JsonResponse({'status': 'ok', 'desbloqueados': desbloqueados})
