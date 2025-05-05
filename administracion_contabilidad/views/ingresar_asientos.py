import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from administracion_contabilidad.forms import IngresarAsiento
from administracion_contabilidad.models import Asientos


def ingresar_asiento(request):
    form = IngresarAsiento({'fecha':datetime.now().strftime('%Y-%m-%d')})
    return render(request, 'contabilidad/ingresar_asientos.html', {'form': form})


def guardar_asientos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            asientos = data.get("asientos", [])

            for asiento in asientos:
                a = Asientos()
                a.id = a.get_id()
                a.fecha = datetime.now().strftime('%Y-%m-%d')
                a.asiento = generar_numero()
                a.cuenta = asiento.get("cuenta").split(" - ")[0].strip() if asiento.get("cuenta") else None
                a.imputacion = 1 if asiento.get("debe") else 2
                a.tipo = 'D'
                a.paridad = asiento.get("paridad") or None
                a.cambio = asiento.get("tipo_cambio") or None
                a.monto = asiento.get("debe") or asiento.get("haber") or 0
                a.detalle = asiento.get("detalle") or None
                a.posicion = asiento.get("posicion") or None
                a.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def generar_numero():
    # Obtener la fecha y hora actual
    ahora = datetime.now()

    # Tomar los dos últimos dígitos del año
    año = str(ahora.year)[-2:]

    # Mes, día, hora, minutos y segundos
    mes = f"{ahora.month:02}"
    dia = f"{ahora.day:02}"
    hora = f"{ahora.hour:02}"
    minutos = f"{ahora.minute:02}"
    segundos = f"{ahora.second:02}"

    # Concatenar para formar el número (ejemplo: 11051019041186)
    numero = f"{año}{mes}{dia}{hora}{minutos}{segundos}"

    return numero


