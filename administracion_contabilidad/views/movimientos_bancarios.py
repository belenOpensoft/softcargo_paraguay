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

from administracion_contabilidad.forms import MovimientoBancarioForm
from administracion_contabilidad.models import Cheques, Asientos, Chequeras, Movims, Ordenes, Chequeorden
from administracion_contabilidad.views.ingresar_asientos import generar_numero
from administracion_contabilidad.views.preventa import generar_autogenerado
from cargosystem import settings
from mantenimientos.models import Clientes


def movimientos_bancarios(request):
    form = MovimientoBancarioForm({'fecha':datetime.now().strftime('%Y-%m-%d'),'vto_cheque':datetime.now().strftime('%Y-%m-%d'),'tipo_movimiento': 'depositar'})
    return render(request, 'contabilidad/movimientos_bancarios.html', {'form': form})

def cheques_disponibles_clientes(request):
    try:
        """ cheques = Cheques.objects.filter(
            Q(cestado=0) | Q(cestado=None),
            Q(cestadobco=0) | Q(cestadobco=None) ,
            Q(cnrodepos=0) | Q(cnrodepos=None) ,
            Q(cpago=None) | Q(cpago='')
        ).order_by('-id')"""
        cheques = Cheques.objects.filter(cestado=0,cestadobco=0,cnrodepos=0,cpago=None).order_by('-id')
        clientes_dict = dict(Clientes.objects.filter(codigo__in=cheques.values_list('ccliente', flat=True).distinct())
                             .values_list('codigo', 'empresa'))

        if not cheques.exists():
            return JsonResponse({'mensaje': 'No hay cheques disponibles.', })

        data = []
        for c in cheques:
            cliente_nombre = clientes_dict.get(c.ccliente, '')
            data.append({
                'vencimiento': c.cvto.strftime('%d/%m/%Y') if c.cvto else '',
                'emision': c.cfecha.strftime('%d/%m/%Y') if c.cfecha else '',
                'banco': c.cbanco if c.cbanco else '',
                'numero': c.cnumero,
                'cliente': cliente_nombre,
                'total': f"{c.cmonto:.2f}" if c.cmonto else 0,
                'id': c.id if c.id else '',
                'moneda': c.cmoneda if c.cmoneda else ''
            })

        return JsonResponse({'success':True,'cheques': data})
    except Exception as e:
        return JsonResponse({'success': False, 'cheques':[],'error':str(e)})

def guardar_movimiento_bancario(request):
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
                tipo_asiento=general.get('tipo')

                if tipo_asiento=='cheque_comun' or tipo_asiento=='cheque_diferido':
                    modo_asiento = 'CHEQUE'
                elif tipo_asiento == 'depositar':
                    modo_asiento = 'DEPOSITO'
                elif tipo_asiento == 'transferencia':
                    modo_asiento='TRANSFER'
                elif tipo_asiento == 'egresos':
                    modo_asiento='EGRESO'
                elif tipo_asiento=='ingresos':
                    modo_asiento='INGRESO'

                if general.get('orden')==1:
                    numero_orden=crear_orden_pago(general,autogenerado,tipo_asiento)

                cheque = general.get('cheque')
                tipo_adentro = 'S/I'
                tipo='S/I'
                if tipo_asiento == 'cheque_comun' or tipo_asiento=='cheque_diferido' or tipo_asiento=='egresos':
                    tipo='C'
                elif tipo_asiento=='depositar' or tipo_asiento=='ingresos' or tipo_asiento=='transferencia':
                    tipo='B'

                if cheque == '1':
                    tipo_adentro = 'B'
                    tipo='B'
                    modo_asiento = 'CHEQUE'
                    #hacer los asientos de cheques, 1 haber y 1 deber por cheque

                    for asiento in asientos:
                        # asiento general
                        a = Asientos()
                        a.id = a.get_id()
                        a.fecha = general.get('fecha') or None
                        a.asiento = numero
                        a.cuenta = general.get("banco").split(" - ")[0].strip() if general.get("banco") else None
                        a.imputacion = 1
                        a.tipo = tipo
                        a.autogenerado = autogenerado
                        a.paridad = general.get('paridad') or None
                        a.cambio = general.get('arbitraje') or None
                        a.monto = asiento.get("monto") or None
                        a.detalle = general.get('detalle') or None
                        a.documento = general.get('documento') or None
                        a.banco = general.get('banco') or None
                        a.save()

                        a = Asientos()
                        a.id = a.get_id()
                        a.fecha = general.get('fecha') or None
                        a.asiento = numero
                        a.cuenta = asiento.get("cuenta").split(" - ")[0].strip() if asiento.get("cuenta") else None
                        a.imputacion = 2
                        a.autogenerado = autogenerado
                        a.tipo = tipo_adentro
                        a.paridad = general.get("paridad") or None
                        a.cambio = general.get("arbitraje") or None
                        a.monto = asiento.get("monto") or None
                        a.detalle = asiento.get("detalle") or None
                        a.documento = general.get("documento") or None
                        a.banco = general.get('banco') or None
                        a.modo = modo_asiento
                        a.save()

                        if asiento.get('autogen'):
                            cheque = Cheques.objects.filter(id=asiento.get('autogen')).first()
                            if cheque:
                                cheque.cestado=2
                                cheque.cnrodepos=general.get("documento") or None
                                cheque.save()

                else:
                    if tipo_asiento == 'depositar':
                        tipo_adentro='C'
                    else:
                        tipo_adentro='B'

                    #asiento general
                    a=Asientos()
                    a.id=a.get_id()
                    a.fecha=general.get('fecha') or None
                    a.asiento=numero
                    a.cuenta = general.get("banco").split(" - ")[0].strip() if general.get("banco") else None
                    a.imputacion=1
                    a.tipo=tipo
                    a.autogenerado = autogenerado
                    a.paridad = general.get('paridad') or None
                    a.cambio=general.get('arbitraje') or None
                    a.monto=general.get('acumulado') or None
                    a.detalle=general.get('detalle') or None
                    a.documento=general.get('documento') or None
                    a.banco = general.get('banco') or None

                    a.save()

                    for asiento in asientos:
                        a = Asientos()
                        a.id = a.get_id()
                        a.fecha = general.get('fecha') or None
                        a.asiento = numero
                        a.cuenta = asiento.get("cuenta").split(" - ")[0].strip() if asiento.get("cuenta") else None
                        a.imputacion = 2
                        a.tipo = tipo_adentro
                        a.paridad = general.get("paridad") or None
                        a.cambio = general.get("arbitraje") or None
                        a.monto = asiento.get("monto")  or None
                        a.detalle = asiento.get("detalle") or None
                        a.documento = general.get("documento") or None
                        a.modo=modo_asiento
                        a.banco = general.get('banco') or None
                        a.autogenerado = autogenerado
                        a.save()

                    if general.get('chequera')=='1':
                        chequera=Chequeras.objects.filter(cheque=general.get("documento")).first()
                        if chequera:
                            chequera.estado=2
                            chequera.save()

            return JsonResponse({"success": True,'numero_orden':numero_orden})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def cheques_disponibles_listado(request):
    cheques = Chequeras.objects.filter(estado=0,diferido='N').order_by('-id')
    resultado = []

    for c in cheques:
        resultado.append({
            'numero': c.cheque,
            'fecha': c.fecha.strftime('%Y-%m-%d') if c.fecha else '',
        })

    return JsonResponse(resultado, safe=False)

def cheques_disponibles_listado_diferidos(request):
    cheques = Chequeras.objects.filter(estado=0,diferido='S').order_by('-id')
    resultado = []

    for c in cheques:
        resultado.append({
            'numero': c.cheque,
            'fecha': c.fecha.strftime('%Y-%m-%d') if c.fecha else '',
        })

    return JsonResponse(resultado, safe=False)

def crear_orden_pago(general,autogenerado_impuventa,tipo):
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

        if tipo == 'cheque_comun' or tipo == 'cheque_diferido':
            chequera = Chequeras.objects.filter(cheque=general.get('documento')).first()
            if chequera:
                chequera.estado = 2
                chequera.save()
                cheque = Chequeorden()
                cheque.cnumero = general.get('documento')
                cheque.cbanco = chequera.banco
                cheque.cfecha = chequera.fecha
                cheque.cvto = chequera.fecha
                cheque.corden = numero
                cheque.cmonto = general.get('acumulado')
                cheque.save()


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
        lista.mactivo = 'S'
        lista.marbitraje = movimiento['arbitraje']
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
                fecha_pago = fecha_pago.strftime('%d/%m/%Y')
                vto = vto.strftime('%d/%m/%Y')

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

def monto_a_letras(monto, moneda):
    try:
        monto = float(str(monto).replace(",", ""))  # Asegura formato numérico
        enteros = int(monto)
        decimales = int(round((monto - enteros) * 100))
        letras = num2words(enteros, lang='es').upper()
        return f"SON {moneda} {letras} CON {decimales:02d}/100."
    except:
        return "SON MONEDA NACIONAL S/I"

def generar_comprobante_deposito_pdf(request):
    try:
        if request.method == 'POST':
            data = request.POST
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="comprobante_deposito.pdf"; filename*=UTF-8\'\'comprobante_deposito.pdf'

            c = canvas.Canvas(response, pagesize=A4)
            width, height = A4
            y = height - 30 * mm

            # Logo
            logo_path = os.path.join(settings.PACKAGE_ROOT, 'static', 'images', 'oceanlink.png')
            c.drawImage(logo_path, 20 * mm, y, width=40 * mm, preserveAspectRatio=True, mask='auto')
            y -= 10 * mm

            # Encabezado
            nro = data.get("numero")
            fecha_str = data.get("fecha", datetime.now().strftime('%d/%m/%Y'))
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d")  # o el formato en que venga tu fecha
                fecha = fecha.strftime('%Y/%m/%d')
            except (ValueError, TypeError):
                fecha = fecha_str

            c.setFont("Courier", 12)
            c.drawString(20 * mm, y, f"Depósito ..........: {nro}")
            y -= 6 * mm
            c.drawString(20 * mm, y, f"Fecha ..............: {fecha}")
            y -= 10 * mm

            # Moneda y monto
            moneda = data.get("moneda")
            monto = data.get("monto_total")
            banco_destino = data.get("banco")

            c.setFont("Courier-Bold", 10)
            c.drawString(20 * mm, y, f"Moneda .............: {moneda}")
            y -= 6 * mm
            c.drawString(20 * mm, y, f"Monto depositado ...: {monto}")
            y -= 6 * mm
            c.drawString(20 * mm, y, f"Banco destino ......: {banco_destino}")

            # Línea de sección
            y -= 12 * mm
            c.setFont("Courier", 10)
            titulo = "Valores depositados"
            c.drawString(20 * mm, y, titulo)
            y -= 8 * mm

            cheques = json.loads(data.get('data', '[]'))
            if cheques:
                c.setFont("Courier", 9)
                c.drawString(20 * mm, y, "Cheque")
                c.drawString(50 * mm, y, "Banco")
                c.drawString(100 * mm, y, "Cliente")
                c.drawString(170 * mm, y, "Importe")
                c.line(20 * mm, y - 1.5 * mm, 200 * mm, y - 1.5 * mm)
                y -= 6 * mm

                try:
                    for chq in cheques:
                        cheque = str(chq.get('numero', ''))
                        banco = str(chq.get('banco', ''))
                        cliente = str(chq.get('cliente', ''))
                        monto = str(chq.get('monto', ''))

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

