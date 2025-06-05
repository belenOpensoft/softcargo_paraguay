import json

from django.http import JsonResponse
from django.shortcuts import render

from administracion_contabilidad.forms import BajaChequesForm
from administracion_contabilidad.models import Chequeras, Asientos


def bajar_cheques(request):
    form = BajaChequesForm()
    return render(request, 'contabilidad/bajar_cheques.html', {'form': form})

#terminar
def buscar_cheques_bajar(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            banco_id = data.get("banco_id")
            fecha = data.get("fecha",None)

            cheques = Asientos.objects.filter(fecha=fecha,banco=banco_id,cuenta__in=[21351,21352])

            # Serializar resultados
            resultado = [{
                'vto': c.vto.strftime('%d/%m/%Y') if c.vto else '',
                'emision': c.fecha.strftime('%d/%m/%Y'),
                'numero': c.cheque,
                'detalle': c.detalle,
                'total': float(c.monto),  # asegurate que sea serializable
                'bajar': False,
                'mov': c.mov if c.mov else '',
                'tipo_cambio': c.tipo_cambio if hasattr(c, 'tipo_cambio') else '',
                'paridad': c.paridad if hasattr(c, 'paridad') else '',
            } for c in cheques]

            # Calcular resumen total para ese banco
            resumen_queryset = Chequeras.objects.filter(banco=banco_id).values("estado").annotate(total=Count("id"))
            resumen_dict = {r["estado"]: r["total"] for r in resumen_queryset}

            resumen = {
                "disponibles": resumen_dict.get(0, 0),
                "utilizados": resumen_dict.get(1, 0),
                "anulados": resumen_dict.get(2, 0),
                "total": sum(resumen_dict.values()),
            }

            return JsonResponse({
                "status": "ok",
                "cheques": resultado,
                "resumen": resumen
            })

        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)})
    return None