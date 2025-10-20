import json
import os
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from administracion_contabilidad.forms import IngresarAsiento
from administracion_contabilidad.models import Asientos, Cuentas, Cheques
from administracion_contabilidad.views.preventa import generar_autogenerado
from cargosystem import settings

from reportlab.lib.colors import grey

from mantenimientos.models import Monedas, Clientes


def ingresar_asiento(request):
    form = IngresarAsiento({'fecha':datetime.now().strftime('%Y-%m-%d')})
    return render(request, 'contabilidad/ingresar_asientos.html', {'form': form})

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
            fecha_str = data.get('fecha')
            asientos = data.get("asientos", [])
            numero = generar_numero()
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            autogen= generar_autogenerado()

            movimientos_pdf = []
            for asiento in asientos:
                cuenta_cod = asiento.get("cuenta").split(" - ")[0].strip() if asiento.get("cuenta") else None
                cuenta_nombre = asiento.get("cuenta").split(" - ")[1].strip() if asiento.get("cuenta") and " - " in asiento.get("cuenta") else ""
                imputacion = 1 if asiento.get("debe") else 2
                monto = asiento.get("debe") or asiento.get("haber") or 0

                a = Asientos()
                a.id = a.get_id()
                a.fecha = fecha_str
                a.asiento = numero
                a.cuenta = cuenta_cod
                a.imputacion = imputacion
                a.autogenerado = autogen
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
            return generar_pdf_contable(pdf_data, request,fecha)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def reimprimir_asiento(request):
    autogenerado = request.GET.get('autogenerado')
    if not autogenerado:
        return JsonResponse({"success": False, "error": "Número de asiento no proporcionado."}, status=400)

    try:
        registros = Asientos.objects.filter(autogenerado=autogenerado).order_by('id')
        if not registros.exists():
            return JsonResponse({"success": False, "error": f"No se encontraron registros para el asiento {autogenerado}."}, status=404)
        flag = False
        movimientos_pdf = []
        fecha = None
        for a in registros:
            modo = a.enviado
            if modo == 'D':
                flag = True

            fecha = a.fecha.strftime('%d-%m-%Y')
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
            "asiento": autogenerado,
            "movimientos": movimientos_pdf
        }

        if flag:
            return generar_comprobante_deposito_pdf(autogenerado)
        else:
            return generar_pdf_contable(pdf_data, request,fecha)

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

def generar_pdf_contable(pdf_data, request,fecha):
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
        c.drawString(20 * mm, y, f"Fecha .............. : {fecha}")
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
        c.drawString(20 * mm, y, "Asiento contable:")
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

def generar_comprobante_deposito_pdf(autogenerado):
    try:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="comprobante_deposito.pdf"; filename*=UTF-8\'\'comprobante_deposito.pdf'

        c = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 30 * mm

        # Logo
        logo_path = os.path.join(settings.PACKAGE_ROOT, 'static', 'images', 'oceanlink.png')
        c.drawImage(logo_path, 20 * mm, y, width=40 * mm, preserveAspectRatio=True, mask='auto')
        y -= 10 * mm

        asiento = Asientos.objects.filter(autogenerado=autogenerado).first()
        moneda = Monedas.objects.filter(codigo=asiento.moneda).first()
        if not asiento:
            return response
        # Encabezado

        nro = asiento.documento if asiento.documento else ''
        fecha = asiento.fecha.strftime('%d/%m/%Y') if asiento.fecha else ''
        # try:
        #     fecha = datetime.strptime(fecha_str, "%Y-%m-%d")  # o el formato en que venga tu fecha
        #     fecha = fecha.strftime('%Y/%m/%d')
        # except (ValueError, TypeError):
        #     fecha = fecha_str

        c.setFont("Courier", 12)
        c.drawString(20 * mm, y, f"Depósito ..........: {nro}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Fecha ..............: {fecha}")
        y -= 10 * mm

        # Moneda y monto
        moneda = moneda.nombre if moneda else ''
        monto = asiento.monto
        banco_destino = asiento.banco
        detalle = asiento.detalle

        c.setFont("Courier-Bold", 10)
        c.drawString(20 * mm, y, f"Moneda .............: {moneda}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Monto depositado ...: {monto}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Banco destino ......: {banco_destino}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Detalle ......: {detalle}")

        # Línea de sección
        y -= 12 * mm
        c.setFont("Courier", 10)
        titulo = "Valores depositados"
        c.drawString(20 * mm, y, titulo)
        y -= 8 * mm

        # cheques = Cheques.objects.filter(cnrodepos=nro,ccliente=asiento.cliente,cmoneda=asiento.moneda,cmonto=asiento.monto)
        asientos = Asientos.objects.filter(autogenerado=autogenerado)
        if asientos:
            c.setFont("Courier", 9)
            c.drawString(20 * mm, y, "Cheque")
            c.drawString(50 * mm, y, "Banco")
            c.drawString(100 * mm, y, "Cliente")
            c.drawString(170 * mm, y, "Importe")
            c.line(20 * mm, y - 1.5 * mm, 200 * mm, y - 1.5 * mm)
            y -= 6 * mm

            try:
                for chq in asientos:
                    cheque = str(chq.documento)
                    banco = str(chq.cuenta)
                    cli = Clientes.objects.filter(codigo=chq.cliente).only('empresa').first()
                    cliente = str(cli.empresa) if cli else ''
                    monto = str(chq.monto)

                    # Calcular líneas por campo
                    lineas_cheque = dividir_lineas(cheque, c, "Courier", 9, 28 * mm)
                    lineas_banco = dividir_lineas(banco, c, "Courier", 9, 45 * mm)
                    lineas_cliente = dividir_lineas(cliente, c, "Courier", 9, 65 * mm)

                    # Determinar la cantidad de líneas necesarias
                    max_lineas = max(len(lineas_cheque), len(lineas_banco), len(lineas_cliente))

                    for i in range(max_lineas):
                        c.setFont("Courier", 9)
                        if i < len(lineas_cheque):
                            c.drawString(20 * mm, y, lineas_cheque[i])
                        if i < len(lineas_banco):
                            c.drawString(50 * mm, y, lineas_banco[i])
                        if i < len(lineas_cliente):
                            c.drawString(100 * mm, y, lineas_cliente[i])
                        if i == 0:
                            c.drawRightString(184 * mm, y, monto)
                        y -= 6 * mm
            except Exception as e:
                c.setFont("Courier", 9)
                c.drawString(20 * mm, y, f"[Error al procesar cheques: {str(e)}]")
                y -= 6 * mm

        c.showPage()
        c.save()
        return response
        return None
    except Exception as e:
        return JsonResponse({'error': str(e)})

def dividir_lineas(texto, c, fuente, tamano, max_width):
    c.setFont(fuente, tamano)
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    for palabra in palabras:
        prueba = (linea_actual + " " + palabra).strip()
        if c.stringWidth(prueba, fuente, tamano) <= max_width:
            linea_actual = prueba
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        lineas.append(linea_actual)
    return lineas
