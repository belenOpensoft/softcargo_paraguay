import json

from django.http import JsonResponse
from django.shortcuts import render

from administracion_contabilidad.forms import BajaChequesForm
from administracion_contabilidad.models import Chequeras, Asientos, VChequesDiferidosBajar


def bajar_cheques(request):
    form = BajaChequesForm()
    return render(request, 'contabilidad/bajar_cheques.html', {'form': form})

#terminar
def buscar_cheques_bajar(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            banco_id = data.get("bancoText")
            fecha = data.get("fecha",None)

            filtros={}

            if fecha:
                filtros['fecha']=fecha

            filtros['banco']=banco_id



            cheques = VChequesDiferidosBajar.objects.filter(**filtros)

            # Serializar resultados
            resultado = [{
                'vto': c.vto.strftime('%d/%m/%Y') if c.vto else '',
                'emision': c.fecha.strftime('%d/%m/%Y'),
                'numero': c.documento,
                'detalle': c.detalle,
                'total': float(c.monto),  # asegurate que sea serializable
                'bajar': False,
                'mov': c.mov if c.mov else '',
                'tipo_cambio': c.cambio ,
                'paridad': c.paridad ,
            } for c in cheques]

            return JsonResponse({
                "status": "ok",
                "cheques": resultado,
            })

        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)})
    return None