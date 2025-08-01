from django.utils.timezone import now
from impomarit.models import BloqueoEdicion

def liberar_bloqueos_expirados():
    expirados = BloqueoEdicion.objects.filter(activo=True, fecha_expiracion__lt=now())
    total = expirados.update(activo=False)
