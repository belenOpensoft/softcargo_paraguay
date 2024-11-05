from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from administracion_contabilidad.models import Infofactura

@csrf_exempt  # Usa csrf_exempt o asegúrate de pasar el token CSRF en el frontend
def guardar_infofactura(request):
    if request.method == "POST":
        try:
            # Decodifica el JSON enviado
            datos = json.loads(request.body)

            for fila in datos:
                # Crea una nueva instancia de Infofactura
                infofactura = Infofactura(
                    id=Infofactura.get_id(),
                    referencia=fila.get("referencia"),
                    seguimiento=fila.get("seguimiento"),
                    transportista=fila.get("transportista"),
                    vuelo=fila.get("vuelo"),
                    master=fila.get("master"),
                    house=fila.get("house"),
                    fecha=fila.get("fecha"),
                    commodity=fila.get("commodity"),
                    kilos=fila.get("kilos"),
                    volumen=fila.get("volumen"),
                    bultos=fila.get("bultos"),
                    origen=fila.get("origen"),
                    destino=fila.get("destino"),
                    consigna=fila.get("consigna"),
                    embarca=fila.get("embarca"),
                    agente=fila.get("agente"),
                    posicion=fila.get("posicion"),
                    terminos=fila.get("terminos"),
                    pagoflete=fila.get("pagoflete")
                )
                # Guarda la instancia en la base de datos
                infofactura.save()

            return JsonResponse({"resultado": "exito"})
        except Exception as e:
            return JsonResponse({"resultado": "error", "mensaje": str(e)}, status=500)
    else:
        return JsonResponse({"resultado": "error", "mensaje": "Método no permitido"}, status=405)
