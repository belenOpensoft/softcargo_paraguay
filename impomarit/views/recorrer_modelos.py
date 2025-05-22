

from django.utils.timezone import make_aware
from datetime import datetime

from seguimientos.models import Seguimiento
from impaerea.models import ImportEmbarqueaereo as ImportEmbarque
from expaerea.models import ExportEmbarqueaereo as ExportEmbarque
from impomarit.models import Embarqueaereo as ImpmaritEmbarque
from expmarit.models import ExpmaritEmbarqueaereo as ExpmaritEmbarque
# Fecha límite
fecha_limite = make_aware(datetime(2025, 1, 13))

# Obtener seguimientos válidos
seguimientos = Seguimiento.objects.filter(fecha__gte=fecha_limite)

# Contadores
total_actualizados = {
    'IMPORT AEREO': 0,
    'EXPORT AEREO': 0,
    'IMPORT MARITIMO': 0,
    'EXPORT MARITIMO': 0
}

for seg in seguimientos:
    if not (seg.etd or seg.eta):
        continue  # No hay datos para actualizar

    filtros = {'seguimiento': seg.numero}

    if seg.modo == 'IMPORT AEREO':
        updated = ImportEmbarque.objects.filter(**filtros).update(etd=seg.etd, eta=seg.eta)
        total_actualizados['IMPORT AEREO'] += updated
    elif seg.modo == 'EXPORT AEREO':
        updated = ExportEmbarque.objects.filter(**filtros).update(etd=seg.etd, eta=seg.eta)
        total_actualizados['EXPORT AEREO'] += updated
    elif seg.modo == 'IMPORT MARITIMO':
        updated = ImpmaritEmbarque.objects.filter(**filtros).update(etd=seg.etd, eta=seg.eta)
        total_actualizados['IMPORT MARITIMO'] += updated
    elif seg.modo == 'EXPORT MARITIMO':
        updated = ExpmaritEmbarque.objects.filter(**filtros).update(etd=seg.etd, eta=seg.eta)
        total_actualizados['EXPORT MARITIMO'] += updated

print("Actualizaciones completadas:")
for modo, cantidad in total_actualizados.items():
    print(f"{modo}: {cantidad} registros actualizados")
