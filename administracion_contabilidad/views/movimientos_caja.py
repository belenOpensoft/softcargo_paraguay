import json
import os


from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from num2words import num2words
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import datetime

from administracion_contabilidad.forms import MovimientoCajaForm
from administracion_contabilidad.models import Cheques, Asientos, Chequeras, Movims, Ordenes, Chequeorden
from administracion_contabilidad.views.ingresar_asientos import generar_numero
from administracion_contabilidad.views.preventa import generar_autogenerado
from cargosystem import settings
from mantenimientos.models import Clientes


def movimientos_caja(request):
    form = MovimientoCajaForm({
        'fecha': datetime.now().strftime('%Y-%m-%d'),
        'tipo_movimiento': 'ingreso'
    })

    return render(request, 'contabilidad/movimientos_caja.html', {'form': form})

def guardar_movimiento_caja(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                numero_orden=0
                asientos = data.get("asientos", [])
                general = data.get("general", [])
                numero=generar_numero()
                autogenerado = generar_autogenerado(datetime.now().strftime("%Y-%m-%d"))
                autogenerado=str(autogenerado)+'NA'
                #tipo_asiento=general.get('tipo')


                if general.get('orden')==1:
                    numero_orden=crear_orden_pago(general,autogenerado)

                cheque = general.get('cheque')
                tipo_adentro = 'C'
                tipo='C'

                #asiento general
                a=Asientos()
                a.id=a.get_id()
                a.fecha=general.get('fecha') or None
                a.asiento=numero
                a.cuenta = general.get("banco").split(" - ")[0].strip() if general.get("banco") else None
                a.imputacion=2
                a.tipo=tipo
                a.autogenerado = autogenerado
                a.paridad = general.get('paridad') or None
                a.cambio=general.get('arbitraje') or None
                a.monto=general.get('acumulado') or None
                a.detalle=general.get('detalle') or None
                #a.documento=general.get('documento') or None
                #a.banco = general.get('banco') or None

                a.save()

                for asiento in asientos:
                    a = Asientos()
                    a.id = a.get_id()
                    a.fecha = general.get('fecha') or None
                    a.asiento = numero
                    a.cuenta = asiento.get("cuenta").split(" - ")[0].strip() if asiento.get("cuenta") else None
                    a.imputacion = 1
                    a.tipo = tipo_adentro
                    a.paridad = 0
                    a.cambio = general.get("arbitraje") or None
                    a.monto = asiento.get("monto")  or None
                    a.detalle = asiento.get("detalle") or None
                    a.autogenerado = autogenerado
                    a.save()

            return JsonResponse({"success": True,'numero_orden':numero_orden})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def crear_orden_pago(general,autogenerado_impuventa):
    try:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fecha_orden = datetime.now().strftime("%Y-%m-%d")
        orden = Ordenes()
        numero=orden.get_next_mboleta()
        orden.mmonto=general.get('acumulado')
        orden.mboleta=numero
        orden.mfechamov=fecha
        orden.mmoneda=general.get('moneda')
        orden.mdetalle=general.get('detalle')
        orden.mcaja=general.get("banco").split(" - ")[0].strip() if general.get("banco") else None
        orden.mautogenmovims=autogenerado_impuventa
        orden.save()

        #crear el movimiento
        movimiento_vec = {
            'tipo': 45,
            'fecha': fecha_orden,
            'boleta': numero,
            'monto': general.get('acumulado'),
            'paridad': general.get('paridad',0),
            'total': general.get('acumulado'),
            'saldo': 0,
            'moneda': general.get('moneda'),
            'detalle': general.get('detalle'),
            'nombremov': 'O/PAGO',
            'arbitraje': general.get('arbitraje',0),
            'autogenerado': autogenerado_impuventa,
        }
        crear_movimiento(movimiento_vec)
        return numero
    except Exception as e:
        raise

def crear_movimiento(movimiento):
    try:
        lista = Movims()
        lista.id = lista.get_id()
        lista.mtipo = movimiento['tipo']
        lista.mfechamov = movimiento['fecha']
        lista.mboleta = movimiento['boleta']
        lista.mmonto = movimiento['monto']
        lista.mtotal = movimiento['total']
        lista.msaldo = movimiento['saldo']
        lista.mvtomov = movimiento['fecha']
        lista.mmoneda = movimiento['moneda']
        lista.mdetalle = movimiento['detalle']
        lista.mnombremov = movimiento['nombremov']
        lista.mautogen = movimiento['autogenerado']
        lista.marbitraje = movimiento['arbitraje']
        lista.mactivo = 'S'

        lista.save()

    except Exception as e:
        raise

def generar_orden_pago_pdf(request):
    try:
        if request.method == 'POST':
            data = request.POST
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="orden_pago.pdf"; filename*=UTF-8\'\'orden_pago.pdf'

            c = canvas.Canvas(response, pagesize=A4)
            width, height = A4
            y = height - 30 * mm

            # Logo
            logo_path = os.path.join(settings.PACKAGE_ROOT, 'static', 'images', 'oceanlink.png')
            c.drawImage(logo_path, 20 * mm, y, width=40 * mm, preserveAspectRatio=True, mask='auto')
            y -= 5 * mm

            fecha_pago_str = data.get("fecha_pago")
            vto_str = data.get("vto")
            try:
                fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d")  # o el formato en que venga tu fecha
                vto = datetime.strptime(vto_str, "%Y-%m-%d")  # o el formato en que venga tu fecha
                fecha_pago = fecha_pago.strftime('%Y/%m/%d')
                vto = vto.strftime('%Y/%m/%d')
            except (ValueError, TypeError):
                fecha_pago = fecha_pago_str
                vto = fecha_pago_str

                # Datos principales
            c.setFont("Courier", 12)
            y -= 5 * mm
            c.drawString(20 * mm, y, f"Orden de pago .....: {data.get('orden')}")
            y -= 6 * mm
            c.drawString(20 * mm, y, f"Fecha de pago .....: {fecha_pago}")
            y -= 6 * mm
            nombre = str(request.user.first_name) + ' ' + str(request.user.last_name)
            c.drawString(20 * mm, y, f"Solicitada por ....: {nombre}")

            # Moneda y monto
            c.setFont("Courier-Bold", 10)
            y -= 10 * mm
            c.drawString(20 * mm, y, f"Moneda ............: {data.get('moneda')}")
            y -= 6 * mm
            c.drawString(20 * mm, y, f"Monto a pagar .....: {data.get('monto_total')}")

            # Cuentas imputadas
            y -= 12 * mm
            c.setFont("Courier-Bold", 10)
            titulo = "Cuentas imputadas en el pago:"
            c.drawString(20 * mm, y, titulo)
            c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(titulo, "Courier-Bold", 10), y - 1.5 * mm)

            y -= 8 * mm
            c.setFont("Courier", 10)
            encabezado = "Cuenta                           Monto        Detalle"
            c.drawString(20 * mm, y, encabezado)
            c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(encabezado, "Courier", 10), y - 1.5 * mm)

            y -= 6 * mm
            banco = data.get('banco', '')[:30].ljust(30)
            monto_valor = float(data.get('monto_total') or 0)
            monto = f"{monto_valor:>10.2f}"
            detalle = data.get('detalle', '')[:25]
            #c.drawString(20 * mm, y, f"{cuenta} {monto}    {detalle}")
            try:
                detalle_items = json.loads(request.POST.get('data', '[]'))
                for item in detalle_items:
                    cuenta_p = item.get('cuenta', '')[:30].ljust(30)
                    monto_p = f"{float(item.get('monto', 0)):>10.2f}"
                    detalle_p = item.get('detalle', '')[:25]  # opcional: recortar si es muy largo
                    c.drawString(20 * mm, y, f"{cuenta_p} {monto_p}    {detalle_p}")
                    y -= 6 * mm
            except Exception as e:
                c.drawString(20 * mm, y, f"[Error al procesar filas: {str(e)}]")
                y -= 6 * mm


            y -= 6 * mm
            c.setFont("Courier-Bold", 10)
            titulo_fp = "Detalle"
            c.drawString(20 * mm, y, titulo_fp)
            c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(titulo_fp, "Courier-Bold", 10), y - 1.5 * mm)
            y -= 6 * mm
            c.setFont("Courier", 10)
            c.drawString(20 * mm, y, detalle)

            # Forma de pago
            # Titulos
            y -= 12 * mm
            c.setFont("Courier-Bold", 10)
            titulo_fp = "Forma de pago:"
            c.drawString(20 * mm, y, titulo_fp)
            c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(titulo_fp, "Courier-Bold", 10), y - 1.5 * mm)

            # Encabezado
            y -= 6 * mm
            c.setFont("Courier", 10)
            c.drawString(20 * mm, y, "Tipo")
            c.drawString(40 * mm, y, "Número")
            c.drawString(70 * mm, y, "Banco")
            c.drawString(140 * mm, y, "Importe")
            c.drawString(170 * mm, y, "Vto.")
            c.line(20 * mm, y - 1.5 * mm, 200 * mm, y - 1.5 * mm)

            # Valores
            y -= 6 * mm
            tipo = data.get('modo','')
            numero = data.get("numero", "")
            banco = data.get("banco", "")[:25]
            importe = data.get("monto_total", "0")

            c.drawString(20 * mm, y, tipo)
            c.drawString(40 * mm, y, numero)
            c.drawString(70 * mm, y, banco)
            c.drawRightString(155 * mm, y, importe)
            c.drawString(170 * mm, y, vto)

            # Texto en letras
            y -= 10 * mm
            monto = data.get('monto_total', '0')
            leyenda_monto = monto_a_letras(monto,data.get('moneda'))
            c.drawString(20 * mm, y, leyenda_monto)

            # Firmas
            y -= 30 * mm
            c.drawString(40 * mm, y, "______________________")
            c.drawString(130 * mm, y, "______________________")
            y -= 6 * mm
            c.drawString(50 * mm, y, "Autorizado")
            c.drawString(140 * mm, y, "Recibido")

            c.showPage()
            c.save()
            return response
        return None
    except Exception as e:
        return JsonResponse({'error':str(e)})
def monto_a_letras(monto,moneda):
    try:
        monto = float(str(monto).replace(",", ""))  # Asegura formato numérico
        enteros = int(monto)
        decimales = int(round((monto - enteros) * 100))
        letras = num2words(enteros, lang='es').upper()
        return f"SON {moneda} {letras} CON {decimales:02d}/100."
    except:
        return "OCURRIO UN ERROR"

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

