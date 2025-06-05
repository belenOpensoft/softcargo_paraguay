import json
from datetime import datetime, date, time

from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render

from administracion_contabilidad.forms import ChequerasForm
from administracion_contabilidad.models import Cuentas, Chequeras


def mantenimiento_chequeras(request):
    form = ChequerasForm({ })
    return render(request, 'contabilidad/mantenimiento_chequeras.html', {'form': form})

def guardar_stock_cheques(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            banco_id = data.get("bancoNumero")
            primer_cheque = int(data.get("primer_cheque", 0))
            total_cheques = int(data.get("total_cheques", 0))
            diferido = data.get("diferido", 'N')

            if not banco_id or not primer_cheque or not total_cheques:
                return JsonResponse({"error": "Datos incompletos"}, status=400)

            cheques_creados = []
            for i in range(total_cheques):
                numero = primer_cheque + i
                cheque, created = Chequeras.objects.get_or_create(
                    banco=banco_id,
                    cheque=numero,
                    diferido=diferido,
                    estado=0,
                    fecha=datetime.combine(date.today(), time.min)
                )
                if created:
                    cheques_creados.append(numero)

            return JsonResponse({"success": True, "cheques": cheques_creados})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return None

def buscar_cheques(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            banco_id = data.get("banco_id")
            ver_utilizados = data.get("ver_utilizados", False)
            cheque_desde = data.get("cheque_desde")
            cheque_hasta = data.get("cheque_hasta")

            # Construir filtros
            filtros = Q(banco=banco_id)

            # Filtro de estado
            if ver_utilizados:
                filtros &= Q(estado__in=[1, 2])
            else:
                filtros &= Q(estado=0)

            # Filtro por rango de cheques
            if cheque_desde:
                filtros &= Q(cheque__gte=cheque_desde)
            if cheque_hasta:
                filtros &= Q(cheque__lte=cheque_hasta)


            # Ejecutar consulta con todos los filtros juntos
            cheques = Chequeras.objects.filter(filtros).order_by("-fecha")

            # Serializar resultados
            resultado = [{
                "numero": c.cheque,
                "estado": c.get_estado_display() if hasattr(c, 'get_estado_display') else c.estado,
                "referencia": c.referencia or "",
                "fecha": c.fecha.strftime("%Y-%m-%d") if c.fecha else "",
                "sucursal": c.sucursal or "",
                "diferido": "Sí" if c.diferido == 'S' else "No",
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

def eliminar_cheque(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            numero = data.get("numero")

            if not numero:
                return JsonResponse({"status": "error", "mensaje": "Número de cheque no recibido."})

            cheque = Chequeras.objects.filter(cheque=numero).first()

            if not cheque:
                return JsonResponse({"status": "error", "mensaje": "Cheque no encontrado."})

            cheque.delete()

            return JsonResponse({"status": "ok", "mensaje": "Cheque eliminado correctamente."})

        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)})

    return JsonResponse({"status": "error", "mensaje": "Método no permitido."}, status=405)

def habilitar_deshabilitar(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            numero = data.get("numero")
            habilitar_deshabilitar = data.get("habilitar_deshabilitar")

            if not numero:
                return JsonResponse({"status": "error", "mensaje": "Número de cheque no recibido."})

            cheque = Chequeras.objects.filter(cheque=numero).first()

            if not cheque:
                return JsonResponse({"status": "error", "mensaje": "Cheque no encontrado."})

            cheque.estado=habilitar_deshabilitar
            cheque.save()

            return JsonResponse({"status": "ok", "mensaje": "Cheque eliminado correctamente."})

        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)})

    return JsonResponse({"status": "error", "mensaje": "Método no permitido."}, status=405)