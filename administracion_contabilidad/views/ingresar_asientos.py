import json
import os
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from administracion_contabilidad.forms import IngresarAsiento
from administracion_contabilidad.models import Asientos, Cuentas
from cargosystem import settings

from reportlab.lib.colors import grey

def ingresar_asiento(request):
    form = IngresarAsiento({'fecha':datetime.now().strftime('%Y-%m-%d')})
    return render(request, 'contabilidad/ingresar_asientos.html', {'form': form})

def guardar_asientos_old(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            asientos = data.get("asientos", [])
            numero=generar_numero()

            for asiento in asientos:
                a = Asientos()
                a.id = a.get_id()
                a.fecha = datetime.now().strftime('%Y-%m-%d')
                a.asiento = numero
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

def guardar_asientos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            asientos = data.get("asientos", [])
            numero = generar_numero()

            movimientos_pdf = []

            for asiento in asientos:
                cuenta_cod = asiento.get("cuenta").split(" - ")[0].strip() if asiento.get("cuenta") else None
                cuenta_nombre = asiento.get("cuenta").split(" - ")[1].strip() if asiento.get("cuenta") and " - " in asiento.get("cuenta") else ""
                imputacion = 1 if asiento.get("debe") else 2
                monto = asiento.get("debe") or asiento.get("haber") or 0

                a = Asientos()
                a.id = a.get_id()
                a.fecha = datetime.now().strftime('%Y-%m-%d')
                a.asiento = numero
                a.cuenta = cuenta_cod
                a.imputacion = imputacion
                a.tipo = 'D'
                a.paridad = asiento.get("paridad") or None
                a.cambio = asiento.get("tipo_cambio") or None
                a.moneda = asiento.get("moneda") or None
                a.monto = monto
                a.detalle = asiento.get("detalle") or None
                a.posicion = asiento.get("posicion") or None
                a.save()

                movimientos_pdf.append({
                    "cuenta": f"{cuenta_cod} - {cuenta_nombre}",
                    "debe": float(asiento.get("debe", 0)),
                    "haber": float(asiento.get("haber", 0)),
                    "moneda": int(asiento.get("moneda") or None),
                    "detalle": asiento.get("detalle"),
                    "arbitraje": float(asiento.get("tipo_cambio")),
                    "paridad": float(asiento.get("paridad")),
                })

            # Preparar datos para el PDF
            pdf_data = {
                "asiento": numero,
                "movimientos": movimientos_pdf
            }

            # Generar y devolver el PDF directamente
            return generar_pdf_contable(pdf_data, request)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def reimprimir_asiento(request):
    nro_asiento = request.GET.get('asiento')
    if not nro_asiento:
        return JsonResponse({"success": False, "error": "Número de asiento no proporcionado."}, status=400)

    try:
        registros = Asientos.objects.filter(asiento=nro_asiento).order_by('id')
        if not registros.exists():
            return JsonResponse({"success": False, "error": f"No se encontraron registros para el asiento {nro_asiento}."}, status=404)

        movimientos_pdf = []
        for a in registros:
            cuenta_obj = Cuentas.objects.filter(xcodigo=a.cuenta).values_list('xnombre', flat=True).first()
            cuenta_nombre = cuenta_obj or 'S/I'
            movimientos_pdf.append({
                "cuenta": f"{a.cuenta} - {cuenta_nombre}",
                "debe": float(a.monto if a.imputacion == 1 else 0),
                "haber": float(a.monto if a.imputacion == 2 else 0),
                "moneda": int(a.moneda or 1),  # o donde tengas guardada la moneda
                "detalle": a.detalle or '',
                "arbitraje": float(a.cambio or 1),
                "paridad": float(a.paridad or 1),
            })

        pdf_data = {
            "asiento": nro_asiento,
            "movimientos": movimientos_pdf
        }

        return generar_pdf_contable(pdf_data, request)

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

def generar_pdf_contable(pdf_data, request):
    try:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="asiento_contable.pdf"; filename*=UTF-8\'\'asiento_contable.pdf'

        c = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 35 * mm

        logo_path = os.path.join(settings.PACKAGE_ROOT, 'static', 'images', 'oceanlink.png')
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 20 * mm, y, width=45 * mm, preserveAspectRatio=True, mask='auto')

        movimientos = pdf_data.get('movimientos', [])
        moneda = None
        detalle = ""

        monedas_encontradas = set()
        detalle_mas_largo = ""

        for i in movimientos:
            monedas_encontradas.add(i.get('moneda'))
            d = i.get('detalle') or ""
            if len(d) > len(detalle_mas_largo):
                detalle_mas_largo = d

        if len(monedas_encontradas) == 1:
            moneda = int(list(monedas_encontradas)[0])
        detalle = detalle_mas_largo

        # Ajuste visual
        c.setLineWidth(0.25)
        c.setStrokeColor(grey)

        y -= 10 * mm
        c.setFont("Courier-Bold", 10)
        c.line(20 * mm, y, 190 * mm, y)
        y -= 6 * mm
        c.drawString(20 * mm, y, "ASIENTO CONTABLE .. : INGRESO DIRECTO")
        y -= 6 * mm
        c.setFont("Courier", 10)
        c.drawString(20 * mm, y, f"Fecha .............. : {datetime.now().strftime('%d/%m/%Y')}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Emitido por ........ : {request.user.first_name.upper()} {request.user.last_name.upper()}")
        y -= 10 * mm
        c.line(20 * mm, y, 190 * mm, y)
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Detalle ............ : {detalle}")
        y -= 6 * mm
        c.line(20 * mm, y, 190 * mm, y)
        y -= 6 * mm

        # ====== MONEDA NACIONAL ======
        c.setFont("Courier-Bold", 10)
        c.drawString(20 * mm, y, "Asiento contable en Moneda Nacional:")
        y -= 6 * mm
        c.line(20 * mm, y, 190 * mm, y)
        y -= 6 * mm
        c.setFont("Courier", 10)

        total_debe = 0
        total_haber = 0

        for item in movimientos:
            cuenta = item.get('cuenta', '')[:30]
            texto = None
            debe_valor = float(item.get('debe') or 0)
            haber_valor = float(item.get('haber') or 0)

            if moneda == 2 and item.get('arbitraje'):
                debe_valor *= float(item.get('arbitraje'))
                haber_valor *= float(item.get('arbitraje'))
            elif moneda == 3 and item.get('arbitraje') and item.get('paridad'):
                factor = float(item.get('arbitraje')) * float(item.get('paridad'))
                debe_valor *= factor
                haber_valor *= factor

            total_debe += debe_valor
            total_haber += haber_valor

            debe = f"{debe_valor:,.2f}" if debe_valor else ""
            haber = f"{haber_valor:,.2f}" if haber_valor else ""

            c.drawString(22 * mm, y, cuenta)
            c.drawRightString(145 * mm, y, debe)
            c.drawRightString(185 * mm, y, haber)
            y -= 6 * mm

        y -= 2 * mm
        c.line(20 * mm, y, 190 * mm, y)
        y -= 4 * mm
        c.setFont("Courier-Bold", 10)
        c.drawRightString(145 * mm, y, f"{total_debe:,.2f}")
        c.drawRightString(185 * mm, y, f"{total_haber:,.2f}")
        y -= 6 * mm
        c.line(20 * mm, y, 190 * mm, y)
        y -= 10 * mm

        # ====== MONEDA ORIGEN ======
        c.setFont("Courier-Bold", 10)
        c.drawString(20 * mm, y, "Asiento contable en Moneda Origen:")
        y -= 6 * mm
        c.line(20 * mm, y, 190 * mm, y)
        y -= 6 * mm
        c.setFont("Courier", 10)

        simbolo_moneda = "$"
        if moneda == 2:
            simbolo_moneda = "U$S"
        elif moneda == 3:
            simbolo_moneda = "€"

        total_debe = total_haber = 0
        for item in movimientos:
            cuenta = item.get('cuenta', '')[:30]
            debe_valor = float(item.get('debe') or 0)
            haber_valor = float(item.get('haber') or 0)

            total_debe += debe_valor
            total_haber += haber_valor

            debe = f"{simbolo_moneda} {debe_valor:,.2f}" if debe_valor else ""
            haber = f"{simbolo_moneda} {haber_valor:,.2f}" if haber_valor else ""

            c.drawString(22 * mm, y, cuenta)
            c.drawRightString(145 * mm, y, debe)
            c.drawRightString(185 * mm, y, haber)
            y -= 6 * mm

        y -= 2 * mm
        c.line(20 * mm, y, 190 * mm, y)
        y -= 4 * mm
        c.setFont("Courier-Bold", 10)
        c.drawRightString(145 * mm, y, f"{simbolo_moneda} {total_debe:,.2f}")
        c.drawRightString(185 * mm, y, f"{simbolo_moneda} {total_haber:,.2f}")
        y -= 6 * mm
        c.line(20 * mm, y, 190 * mm, y)
        y -= 10 * mm

        c.setFont("Courier", 10)
        c.drawString(20 * mm, y, f"Id. interno : {pdf_data.get('asiento', 'S/I')}")

        c.showPage()
        c.save()
        return response

    except Exception as e:
        return HttpResponse(f"Error al generar PDF: {str(e)}", content_type='text/plain')
