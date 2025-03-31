import locale
from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
import base64
from django.views.decorators.csrf import csrf_exempt

from impomarit.views.mails import formatear_linea
from impterrestre.models import VEmbarqueaereo, ImpterraCargaaerea, ImpterraEnvases, ImpterraServiceaereo, VGastosHouse, \
    ImpterraEmbarqueaereo, ImpterraReservas, ImpterraConexaerea
from mantenimientos.views.bancos import is_ajax
from mantenimientos.models import Productos, Clientes, Servicios
from seguimientos.models import VGrillaSeguimientos

DIAS_SEMANA = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre',
         'octubre', 'noviembre', 'diciembre']
TIPOS_OPERATIVA = {
    'IMPORT MARITIMO': 'IMPORTACION MARITIMA',
    'EXPORT MARITIMO': 'EXPORTACION MARITIMA',
    'IMPORT AEREO': 'IMPORTACION AEREA',
    'EXPORT AEREO': 'EXPORTACION AEREA',
    'IMPORT TERRESTRE': 'IMPORTACION TERRESTRE',
    'EXPORT TERRESTRE': 'EXPORTACION TERRESTRE',
}


# Formateamos las fechas con strftime para mostrar en dd/mm/YY
def format_fecha(fecha):
    return fecha.strftime('%d/%m/%Y') if fecha is not None else "S/I"


@csrf_exempt
@login_required(login_url='/')
def get_data_email_op(request):
    resultado = {}
    if is_ajax(request):
        try:
            title = request.POST['title']
            row_number = request.POST['row_number']
            transportista = request.POST['transportista']
            master_boolean = request.POST['master']
            gastos_boolean = request.POST['gastos']
            #9155
            embarque = ImpterraEmbarqueaereo.objects.get(numero=row_number)
            row = VEmbarqueaereo.objects.get(numero=row_number)
            row2 = ImpterraCargaaerea.objects.filter(numero=row_number)
            row3 = ImpterraEnvases.objects.filter(numero=row_number)
            gastos = VGastosHouse.objects.filter(numero=row_number)
            email_cliente = Clientes.objects.get(codigo=embarque.consignatario).emailit if embarque.consignatario is not None else 'S/I'
            email_agente = Clientes.objects.get(codigo=embarque.agente).emailit if embarque.agente is not None else 'S/I'
            conex = ImpterraConexaerea.objects.filter(numero=embarque.numero).order_by('-id').last()
            if conex:
                viaje = conex.viaje if conex.viaje else 'S/I'
            else:
                viaje = 'S/I'
            try:
                seguimiento = VGrillaSeguimientos.objects.get(numero=row.seguimiento)
            except VGrillaSeguimientos.DoesNotExist:
                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='', deposito='', pago='',
                                                  vendedor='')
            texto = ''
            texto += f'<br>'
            texto, resultado = get_data_html(row_number, row, row2, row3, title, texto, resultado,seguimiento,gastos,embarque,conex,viaje,transportista,master_boolean,gastos_boolean)
            texto += "<b><p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>OCEANLINK,</p></b>"
            texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>DEPARTAMENTO DE IMPORTACIÓN MARITIMA,</p>"
            texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>{request.user.first_name} {request.user.last_name}</p>"
            texto += "<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>OPERACIONES</p>"
            texto += "<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>PH: 59829170501</p>"
            resultado['email_cliente'] = email_cliente
            resultado['email_agente'] = email_agente

            resultado['resultado'] = 'exito'
            resultado['mensaje'] = texto
        except Exception as e:
            resultado['resultado'] = str(e)
    else:
        resultado['resultado'] = 'Ha ocurrido un error.'
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def get_data_html(row_number, row, row2, row3, title, texto, resultado,seguimiento,gastos,embarque,conex,viaje,transportista_boolean,master_boolean,gastos_boolean):
    # merca = Productos.objects.get(codigo=row2.producto.codigo)
    if row2 is not None:
        merca = []
        for m in row2:
            merca.append(m.producto)

    fecha_actual = datetime.now()
    #formateado listo
    if title == 'Notificación de transbordo de carga':
        fecha_actual = datetime.now()

        resultado['asunto'] = 'NOTIFICACIÓN DE TRABSBORDO DE CARGA - Ref.: ' + str(row.referencia) + \
                              '/ CS: ' + str(row.seguimiento) + '- H B/L: ' + str(row.hawb) + '- Shipper: '

        fecha_formateada = fecha_actual.strftime(
            f'{DIAS_SEMANA[fecha_actual.weekday()]}, %d de {MESES[fecha_actual.month - 1]} del %Y'
        )
        texto += fecha_formateada.capitalize().upper() + '<br><br>'

        cont = 1
        for b in row2:
            texto += formatear_linea(f"Bultos {cont}", b.bultos if b.bultos is not None else "S/I")
            texto += formatear_linea(f"Peso {cont}", b.bruto if b.bruto is not None else "S/I")
            cont += 1

        cont = 1
        for e in row3:
            texto += formatear_linea(f"Nro. Contenedor {cont}",
                                     str(e.nrocontenedor) if e.nrocontenedor is not None else "S/I")
            cont += 1

        texto += formatear_linea("Viaje", str(viaje))
        texto += formatear_linea("Llegada estimada", format_fecha(row.fecha_retiro))
        texto += formatear_linea("Origen", str(row.origen) if row.origen is not None else "S/I")
        texto += formatear_linea("B/L", str(row.awb) if row.awb is not None else "S/I")
        texto += formatear_linea("H B/L", str(row.hawb) if row.hawb is not None else "S/I")
        texto += formatear_linea("Referencia", str(row_number) if row_number is not None else "S/I")
        texto += formatear_linea("Posición", str(row.posicion) if row.posicion is not None else "S/I")
        texto += formatear_linea("Seguimiento", str(row.seguimiento) if row.seguimiento is not None else "S/I")
        texto += formatear_linea("Consignatario", str(row.consignatario) if row.consignatario is not None else "S/I")
        texto += formatear_linea("Embarcador", str(row.embarcador) if row.embarcador is not None else "S/I")
        texto += formatear_linea("Orden cliente", str(row.orden_cliente) if row.orden_cliente is not None else "S/I")
        texto += formatear_linea("Ref. proveedor", str(row.ref_proveedor) if row.ref_proveedor is not None else "S/I")
        texto += formatear_linea("Mercadería", str(merca) if merca is not None else "S/I")

        # Mini tabla como bloque visual horizontal (si es imprescindible mantenerla)
        texto += "<br><b>Resumen del viaje:</b><br><br>"
        texto += formatear_linea("Origen", str(row.origen) if row.origen else "S/I")
        texto += formatear_linea("Destino", str(row.destino) if row.destino else "S/I")
        texto += formatear_linea("Vuelo/Viaje", str(row.vapor) if row.vapor else "S/I")
        texto += formatear_linea("Viaje", str(row.viaje) if row.viaje else "S/I")
        texto += formatear_linea("Salida", format_fecha(row.fecha_embarque))
        texto += formatear_linea("Llegada", format_fecha(row.fecha_retiro))

        return texto, resultado


    #hacer de nuevo y falta en español
    elif title == 'Shipping instruction':
        tabla_html = "<table style='width:40%'>"
        # Definir los campos y sus respectivos valores
        resultado['asunto'] = 'LCC SHIPPING INSTRUCTION: Ref: ' + str(row.numero) + ' ' \
                                                                                    ' - Shipper: ' + str(
            row.embarcador) + ' - Consig: ' \
                              '' + str(row.consignatario)
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()
        texto += 'Date: ' + fecha_formateada.capitalize() + ' <br>'
        texto += 'To: ' + str(row.agente) + ' <br><br>'

        cons = Clientes.objects.get(codigo=embarque.consignatario)
        if cons:
            direccion = cons.direccion
            pais_c = cons.pais
            tel = cons.telefono
            rut = cons.ruc
        else:
            direccion = None
            pais_c = None
            tel = None
            rut = None

        embarcador = Clientes.objects.get(codigo=embarque.embarcador)
        if embarcador:
            pais = embarcador.pais
            ciudad = embarcador.ciudad
            contacto = embarcador.contactos
        else:
            pais = None
            ciudad = None
            contacto = None

        texto += str(row.embarcador) + ',<br>'
        texto += str(ciudad) + ',' + str(pais) + '<br>'
        texto += 'Contactos: ' + str(contacto) + '<br><br>'

        texto += '<p> Dear colleagues: </p>'
        texto += '<p> Please find bellow coordination details for a shipment to ' + row.destino + '</p><br>'
        texto += '<p>CARGO DETAILS</p><br><br>'

        if isinstance(seguimiento.etd, datetime):
            salida = str(seguimiento.etd.strftime("%d/%m/%Y"))
        else:
            salida = ''
        if isinstance(seguimiento.eta, datetime):
            llegada = str(seguimiento.eta.strftime("%d/%m/%Y"))
        else:
            llegada = ''

        carga = ImpterraCargaaerea.objects.get(numero=row.numero)
        if carga:
            producto = carga.producto
            bultos = carga.bultos
            peso = carga.bruto
            volumen = carga.medidas
        else:
            producto = None
            bultos = None
            peso = None
            volumen = None

        campos = [
            ("Internal Reference", row.numero),
            ("Delivery date", llegada if llegada is not None else ""),
            ("Port of Loading", str(row.origen) if row.origen is not None else ""),
            ("Port of Discharge", str(row.destino) if row.destino is not None else ""),
            ("Payment Condition", str(row.pago_flete) if row.pago_flete is not None else ""),
            ("Incoterm", str(row.terminos) if row.terminos is not None else ""),
            ("Commodity", str(producto.nombre) if producto.nombre is not None else ""),
            ("Pieces", str(bultos) if bultos is not None else ""),
            ("Weight", peso if peso is not None else ""),
            ("Volume", str(volumen) if volumen is not None else ""),
        ]
        # Agregar campos a la tabla

        for campo, valor in campos:
            tabla_html += f"<tr><th>{campo}</th><td>{valor}</td></tr>"

        tabla_html += "</table><br><br>"
        texto += tabla_html
        texto += '<p>HBL INFO <br><br>'
        texto += 'Please note HS Code is MANDATORY on HBL body.</p> <br>'
        texto += str(row.embarcador) + ',<br>'
        texto += str(ciudad) + ',' + str(pais) + '<br>'
        texto += 'Contactos: ' + str(contacto) + '<br><br><br>'

        campos2 = [
            ("Consignee", row.consignatario),
            ("Address", direccion if direccion is not None else ""),
            ("Country", pais if pais is not None else ""),
            ("Ph", tel if tel is not None else ""),
            ("RUT", rut if rut is not None else ""),
        ]
        # Agregar campos a la tabla
        tabla_html = "<table style='width:40%'>"
        for campo, valor in campos2:
            tabla_html += f"<tr><th>{campo}</th><td>{valor}</td></tr>"

        tabla_html += "</table><br><br>"
        texto += tabla_html

        texto += '<p>MBL INFO <br><br>'
        texto += 'Please consign MBL EXACTLY as shown bellow. <br>'
        texto += 'Please note HS Code is MANDATORY on MBL body.</p> <br>'
        campos3 = [
            ("Shipper", row.embarcador),
        ]
        # Agregar campos a la tabla
        tabla_html = "<table style='width:40%'>"
        for campo, valor in campos3:
            tabla_html += f"<tr><th>{campo}</th><td>{valor}</td></tr>"

        tabla_html += "</table><br><br>"
        texto += tabla_html

        texto += '<p>MBL/HBL information must include: <br><br>'
        texto += (
            '  - Container number, seal(s) number(s), quantity of pieces, kind od units (packages, pieces, crates, tec), <br>'
            ' weight, volume (LCL), port of loading, port of discharge, and description of goods, HS tariff Code/NCM number, <br>'
            '(first four digits are mandatory), <br>')
        texto += (
            '  -Information on both documents must match. Any discrepancies between MBL/HBL are likely to incur fines and shipment blocked <br>'
            'by Uruguayan Customs. <br> ')
        texto += '  -Telex Release / Express Release / Seawaybill wil generate extra issuing charges at destination depending on Shipping Line. <br>'
        texto += '  -Consignee on MBL/HBL must include detailed information: <br>'
        texto += (
            '  -Full name, address, phone number, contact person or e-mail address, Tax ID (RUT) or passport number if consignee <br>'
            'is an individual. <br>')
        texto += (
            '  -Pre-alert notice must be sent at least 5 days before vessel arrival. This will allow sufficient time for eventual br>'
            'amendments as needed and prevent additional fees from the steamship line. <br><br>')


        return texto, resultado

    elif title == 'Novedades sobre la carga':
        fecha_actual = datetime.now()

        resultado['asunto'] = 'NOVEDADES SOBRE LA CARGA - Ref.: ' + str(row.referencia) + \
                              '/ CS: ' + str(row.seguimiento) + '- Shipper: ' + str(row.embarcador) + \
                              '; Consignee: ' + str(row.consignatario)

        fecha_formateada = fecha_actual.strftime(
            f'{DIAS_SEMANA[fecha_actual.weekday()]}, %d de {MESES[fecha_actual.month - 1]} del %Y'
        )
        texto += fecha_formateada.capitalize().upper() + '<br><br>'

        cont = 1
        for m in merca:
            texto += formatear_linea(f"Mercadería {cont}", str(m.nombre) if m.nombre is not None else "S/I")
            cont += 1

        cont = 1
        for b in row2:
            texto += formatear_linea(f"Bultos {cont}", b.bultos if b.bultos is not None else "S/I")
            texto += formatear_linea(f"Peso {cont}", b.bruto if b.bruto is not None else "S/I")
            texto += formatear_linea(f"CBM {cont}", b.cbm if b.cbm is not None else "S/I")
            cont += 1

        cont = 1
        for e in row3:
            texto += formatear_linea(f"Nro. Contenedor {cont}",
                                     str(e.nrocontenedor) if e.nrocontenedor is not None else "S/I")
            texto += formatear_linea(f"Precintos {cont}", str(e.precinto) if e.precinto is not None else "S/I")
            cont += 1

        texto += formatear_linea("Embarque", str(row_number) if row_number is not None else "S/I")
        texto += formatear_linea("Posición", str(row.posicion) if row.posicion is not None else "S/I")
        texto += formatear_linea("Salida", format_fecha(row.fecha_embarque))
        texto += formatear_linea("LLegada", format_fecha(row.fecha_retiro))
        texto += formatear_linea("Origen", str(row.origen) if row.origen is not None else "S/I")
        texto += formatear_linea("Destino", str(row.destino) if row.destino is not None else "S/I")
        texto += formatear_linea("Viaje", str(viaje))
        texto += formatear_linea("H B/L", str(row.hawb) if row.hawb is not None else "S/I")
        texto += formatear_linea("Embarcador", str(row.embarcador) if row.embarcador is not None else "S/I")
        texto += formatear_linea("Consignatario", str(row.consignatario) if row.consignatario is not None else "S/I")

        return texto, resultado
    elif title == 'Routing Order':
        hora_actual = datetime.now().strftime("%H:%M")
        fecha_actual = datetime.now()

        resultado['asunto'] = 'ROUTING ORDER - Ref.: ' + str(row.referencia) + \
                              '/ CS: ' + str(row.seguimiento) + '- Shipper: ' + str(row.embarcador) + \
                              '; Consignee: ' + str(row.consignatario)

        texto += f'{hora_actual} <br><br>'

        texto += formatear_linea("Fecha", format_fecha(fecha_actual))
        texto += formatear_linea("A", str(row.agente) if row.agente is not None else "S/I")
        texto += formatear_linea("Departamento", "MARITIMO")

        texto += "<br>Estimados Sres.: <br>"
        texto += "Por favor, contactar la siguiente compañía para coordinar la operación referenciada: <br><br>"

        # Proveedor
        texto += formatear_linea("Proveedor", str(row.embarcador) if row.embarcador is not None else "S/I")
        texto += formatear_linea("Dirección",
                                 str(row.direccion_embarcador) if row.direccion_embarcador is not None else "S/I")
        texto += formatear_linea("Ciudad", str(row.ciudad_embarcador) if row.ciudad_embarcador is not None else "S/I")
        texto += formatear_linea("País", str(row.pais_embarcador) if row.pais_embarcador is not None else "S/I")

        texto += "<br>"

        # Consignee
        texto += formatear_linea("Consignee", str(row.consignatario) if row.consignatario is not None else "S/I")
        texto += formatear_linea("Dirección",
                                 str(row.direccion_consignatario) if row.direccion_consignatario is not None else "S/I")
        texto += formatear_linea("Ciudad",
                                 str(row.ciudad_consignatario) if row.ciudad_consignatario is not None else "S/I")
        texto += formatear_linea("País", str(row.pais_consignatario) if row.pais_consignatario is not None else "S/I")

        texto += "<br>"

        # Detalles de la operación
        texto += formatear_linea("Referencia interna", str(row_number) if row_number is not None else "S/I")
        texto += formatear_linea("Orden cliente", str(row.orden_cliente) if row.orden_cliente is not None else "S/I")
        texto += formatear_linea("Origen", str(row.origen) if row.origen is not None else "S/I")
        texto += formatear_linea("Destino", str(row.destino) if row.destino is not None else "S/I")

        texto += "<br>"

        # Mercadería y detalles de envío
        cont = 1
        for m in merca:
            texto += formatear_linea(f"Mercadería {cont}", str(m.nombre) if m.nombre is not None else "S/I")
            cont += 1

        cont = 1
        for b in row2:
            texto += formatear_linea(f"Bultos {cont}", b.bultos if b.bultos is not None else "S/I")
            texto += formatear_linea(f"Peso {cont}", b.bruto if b.bruto is not None else "S/I")
            cont += 1

        texto += formatear_linea("Condiciones de pago", str(row.pago_flete) if row.pago_flete is not None else "S/I")
        texto += formatear_linea("Términos de compra", str(row.terminos) if row.terminos is not None else "S/I")
        texto += formatear_linea("Modo de embarque", "TERRESTRE")

        texto += "<br>"

        return texto, resultado
    elif title == 'Notificación de llegada de carga':

        resultado['asunto'] = (

            f'NOTIFICACION DE LLEGADA DE CARGA - Ref.: {embarque.numero} - CS: {row.seguimiento} - '

            f'HB/l: {row.hawb} - Ship: {row.embarcador} - Consig: {row.consignatario}; Viaje: {viaje}'

        )

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        fecha_actual = datetime.now()

        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

        consigna = Clientes.objects.get(codigo=embarque.consignatario)

        carga = ImpterraCargaaerea.objects.filter(numero=embarque.numero)

        gastos = ImpterraServiceaereo.objects.filter(numero=embarque.numero)

        texto = formatear_linea("Fecha", fecha_formateada)

        texto += "<br>"

        texto += formatear_linea("Att.", "")

        texto += formatear_linea("Notificar a", row.consignatario)

        texto += formatear_linea("Dirección", consigna.direccion if consigna else "")

        texto += formatear_linea("Teléfono", consigna.telefono if consigna else "")

        texto += "<br>"

        texto += formatear_linea("Salida", conex.salida if conex else "")

        texto += formatear_linea("Llegada", conex.llegada if conex else "")

        texto += formatear_linea("Origen", conex.origen if conex else "")

        texto += formatear_linea("Destino", conex.destino if conex else "")

        texto += formatear_linea("HAWB", embarque.hawb)

        if master_boolean == 'true':
            texto += formatear_linea("AWB", embarque.awb)

        texto += formatear_linea("Referencia", embarque.numero)

        texto += formatear_linea("Posición", embarque.posicion)

        texto += formatear_linea("Seguimiento", row.seguimiento)

        texto += formatear_linea("Embarcador", row.embarcador)

        texto += formatear_linea("Ref. Proveedor", row.embarcador)

        if carga:

            for c in carga:
                ap1 = float(c.cbm) if c.cbm is not None else 0

                aplicable = round(ap1, 2) if ap1 > float(c.bruto) else float(c.bruto)

                texto += formatear_linea("Mercadería", c.producto.nombre)

                texto += formatear_linea("Bultos", str(c.bultos))

                texto += formatear_linea("Peso", str(c.bruto))

                texto += formatear_linea("Aplicable", str(aplicable))

            texto += "<br>"

        if gastos_boolean == 'true' and gastos:

            texto += formatear_linea("Detalle", "Gastos en Dólares U.S.A")

            total_gastos = 0

            total_iva = 0

            for g in gastos:

                servicio = Servicios.objects.get(codigo=g.servicio)

                total_gastos += float(g.precio)

                if servicio.tasa == 'B':
                    total_iva += float(g.precio) * 0.22

                if g.precio != 0:
                    texto += formatear_linea(servicio.nombre, f"${g.precio:.2f}")

            texto += "<br>"

            texto += formatear_linea("TOTAL DE GASTOS", f"${total_gastos:.2f}")

            texto += formatear_linea("I.V.A", f"${total_iva:.2f}")

            texto += formatear_linea("TOTAL A PAGAR", f"${total_gastos + total_iva:.2f}")

            texto += "<br>"

        texto += "<pre style='font-family: Courier New, monospace; font-size: 12px;'>"

        texto += "Les informamos que por razones de seguridad los pagos solo pueden hacerse por transferencia bancaria a la siguiente cuenta:\n\n"

        texto += "BBVA URUGUAY S.A.\n"

        texto += "25 de Mayo 401\n"

        texto += "Cuenta Número: 5207347\n"

        texto += "OCEANLINK Ltda.\n\n"

        texto += "Los buques, vuelos y las fechas pueden variar sin previo aviso y son siempre a CONFIRMAR.\n"

        texto += "Agradeciendo vuestra preferencia, le saludamos muy atentamente."

        texto += "</pre>"

        return texto, resultado
    elif title == 'Aviso de embarque':

        resultado[
            'asunto'] = f'AVISO DE EMBARQUE / Ref: {row.seguimiento} - HB/l: {row.hawb} - Shipper: {row.embarcador} - Consig: {row.consignatario}'

        fecha_actual = datetime.now()

        fecha_formateada = fecha_actual.strftime(

            f'{DIAS_SEMANA[fecha_actual.weekday()]}, %d de {MESES[fecha_actual.month - 1]} del %Y')

        texto = formatear_linea("Fecha", fecha_formateada.capitalize())

        texto += "<br>"

        texto += formatear_linea("Sres.", str(row.consignatario))

        texto += formatear_linea("Depto.", "COMERCIO EXTERIOR")

        texto += "<br>"

        salida = seguimiento.etd.strftime("%d/%m/%Y") if isinstance(seguimiento.etd, datetime) else ""

        llegada = seguimiento.eta.strftime("%d/%m/%Y") if isinstance(seguimiento.eta, datetime) else ""

        ref = f"{row.seguimiento}/{row.numero}"

        texto += formatear_linea("Referencia", ref)

        texto += formatear_linea("Posición", row.posicion or "")

        texto += formatear_linea("Consignatario", row.consignatario or "")

        texto += formatear_linea("Orden Cliente", embarque.ordencliente or "")

        texto += formatear_linea("Ref. Proveedor", embarque.refproveedor or "")

        texto += formatear_linea("Términos de Compra", row.terminos or "")

        if master_boolean == 'true':
            texto += formatear_linea("AWB", row.awb or "")

        if transportista_boolean == 'true':
            texto += formatear_linea("Transportista", row.transportista or "")

        texto += "<br>"

        texto += formatear_linea("Origen", row.origen or "")

        texto += formatear_linea("Destino", row.destino or "")

        texto += formatear_linea("Salida", salida)

        texto += formatear_linea("Llegada", llegada)

        texto += "<br>"

        texto += formatear_linea("Agente", row.agente or "")

        # Datos de contenedores

        mercaderias = ""

        bultos = 0

        peso = 0

        volumen = 0

        cant_cntr = ImpterraCargaaerea.objects.filter(numero=row.numero).values(

            'cbm', 'bruto', 'bultos', 'producto'

        ).annotate(total=Count('id'))

        if cant_cntr.exists():

            for cn in cant_cntr:
                bultos += cn['bultos']

                peso += cn['bruto'] if cn['bruto'] else 0

                volumen += cn['cbm'] if cn['cbm'] else 0

                producto = Productos.objects.get(codigo=int(cn['producto'])).nombre

                mercaderias += producto + ' - '

        texto += formatear_linea("House", row.hawb or "")

        texto += formatear_linea("Peso", f"{peso} KGS")

        texto += formatear_linea("Bultos", str(bultos))

        texto += formatear_linea("CBM", f"{volumen:.3f} M³")

        texto += "<br>"

        texto += formatear_linea("Mercadería", mercaderias.rstrip(' -'))

        texto += formatear_linea("Depósito", seguimiento.deposito or "")

        texto += formatear_linea("Doc. Originales", "SI" if seguimiento.originales else "NO")

        texto += "<br>"

        # Reemplazo de tabla por líneas alineadas

        texto += formatear_linea("Origen", row.origen or "")

        texto += formatear_linea("Destino", row.destino or "")

        texto += formatear_linea("Viaje/Vuelo", row.transportista or "")

        texto += formatear_linea("Salida", salida)

        texto += formatear_linea("Llegada", llegada)

        texto += "<br>"

        texto += "<pre style='font-family: Courier New, monospace; font-size: 12px;'>"

        texto += "Los buques y las fechas pueden variar sin previo aviso y son siempre a confirmar.\n"

        texto += "Agradeciendo vuestra preferencia, le saludamos muy atentamente."

        texto += "</pre>"

        return texto, resultado
    elif title == 'Orden de facturacion':

        resultado['asunto'] = 'ORDEN DE FACTURACION: - seguimiento: ' + str(
            row.seguimiento)

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()
        if isinstance(seguimiento.eta, datetime):
            llegada = str(seguimiento.eta.strftime("%d/%m/%Y"))
        else:
            llegada = ''
        tabla_html = fecha_formateada+"<br><br>"
        tabla_html += f"<p>ORDEN DE FACTURACIÓN SEGUIMIENTO: {row.seguimiento}</p><br>"
        tabla_html += f"<p>POSICIÓN: {row.posicion}</p><br>"
        tabla_html += f"<p>MASTER: {row.awb}</p><br>"
        tabla_html += f"<p>ETA {llegada} </p><br>"
        tabla_html += f"<p>CLIENTE: {seguimiento.cliente}</p><br>"

        return tabla_html, resultado
    elif title == 'Traspaso a operaciones':

        texto += formatear_linea("SEGUIMIENTO", row.numero)

        texto += formatear_linea("CLIENTE", row.consignatario)

        texto += formatear_linea("BL", row.awb)

        texto += formatear_linea("HBL", row.hawb)

        texto += "<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>EMBARQUE TRASPASADO A DEPARTAMENTO DE OPERACIONES</p>"

        fecha_actual = datetime.now()

        fecha_formateada = fecha_actual.strftime(

            f'{DIAS_SEMANA[fecha_actual.weekday()]}, %d de {MESES[fecha_actual.month - 1]} del %Y')

        texto += formatear_linea("FECHA", fecha_formateada.capitalize())

        texto += formatear_linea("CONDICION MBL", "")

        texto += formatear_linea("CONDICION HBL", "")

        texto += formatear_linea("COURIER CON DOCS", "")

        texto += formatear_linea("COURIER/GUIA", "")

        resultado['asunto'] = f'SEGUIMIENTO {row.numero} // TRASPASO A OPERACIONES'

        return texto, resultado

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data).decode("utf-8")
        return base64_data
