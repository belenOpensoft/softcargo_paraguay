import locale
from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import base64
from django.views.decorators.csrf import csrf_exempt
from expterrestre.models import VEmbarqueaereo, ExpterraCargaaerea, ExpterraEnvases, ExpterraServiceaereo, VGastosHouse, \
    ExpterraEmbarqueaereo, ExpterraConexaerea
from impomarit.views.mails import formatear_linea
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
            embarque = ExpterraEmbarqueaereo.objects.get(numero=row_number)
            row = VEmbarqueaereo.objects.get(numero=row_number)
            row2 = ExpterraCargaaerea.objects.filter(numero=row_number)
            row3 = ExpterraEnvases.objects.filter(numero=row_number)
            gastos = VGastosHouse.objects.filter(numero=row_number)
            email_cliente = Clientes.objects.get(codigo=embarque.consignatario).emailet


            try:
                seguimiento = VGrillaSeguimientos.objects.get(numero=row.seguimiento)
            except VGrillaSeguimientos.DoesNotExist:
                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='', deposito='', pago='',vendedor='')
            texto = ''
            texto += f'<br>'
            texto, resultado = get_data_html(row_number, row, row2, row3, title, texto, resultado,seguimiento,gastos,embarque)
            texto += '<b>OCEANLINK,</b><br>'
            texto += 'DEPARTAMENTO DE IMPORTACION MARITIMA, <br>'
            texto += 'Bolonia 2280 LATU, Edificio Los Álamos, Of.103 <br>'
            texto += 'OPERACIONES <br>'
            texto += 'EMAIL: <br>'
            texto += 'TEL: 598 2917 0501 <br>'
            texto += 'FAX: 598 2916 8215 <br><br><br><br>'
            texto += '</table>'

            resultado['email_cliente'] = email_cliente
            resultado['resultado'] = 'exito'
            resultado['mensaje'] = texto
        except Exception as e:
            resultado['resultado'] = str(e)
    else:
        resultado['resultado'] = 'Ha ocurrido un error.'
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)



def get_data_html(row_number, row, row2, row3, title, texto, resultado,seguimiento,gastos,embarque):
    # merca = Productos.objects.get(codigo=row2.producto.codigo)
    if row2 is not None:
        merca = []
        for m in row2:
            merca.append(m.producto)

    fecha_actual = datetime.now()
    if title == 'Notificación de transbordo de carga':
        fecha_actual = datetime.now()
        # ASUNTO DEL MENSAJE
        resultado['asunto'] = 'NOTIFICACIÓN DE TRABSBORDO DE CARGA - Ref.: ' + str(row.referencia) + \
                              '/ CS: ' + str(row.seguimiento) + '- H B/L: ' + str(row.hawb) + '- Shipper: '
        # CUERPO DEL MENSAJE
        fecha_formateada = fecha_actual.strftime(
            f'{DIAS_SEMANA[fecha_actual.weekday()]}, %d de {MESES[fecha_actual.month - 1]} del %Y')
        texto += fecha_formateada.capitalize().upper() + '<br><br>'
        tabla_html = "<table border= '1' style='width: 40%; border-collapse: collapse;'>"

        campos = []

        cont = 1
        for b in row2:
            campos.append((f"Bultos {cont}: ", b.bultos if b.bultos is not None else "S/I"))
            campos.append((f"Peso {cont}: ", b.bruto if b.bruto is not None else "S/I"))
            cont = cont + 1

        cont = 1
        for e in row3:
            campos.append((f"Nro. Contenedor {cont}: ", str(e.nrocontenedor) if e.nrocontenedor is not None else "S/I"))
            cont = cont + 1

        campos.extend([
            ("Vapor: ", str(row.vapor) if row.vapor is not None else "S/I"),
            ("Viaje: ", str(row.viaje) if row.viaje is not None else "S/I"),
            ("Llegada estimada: ", format_fecha(row.fecha_retiro)),
            ("Origen: ", str(row.origen) if row.origen is not None else "S/I"),
            ("B/L: ", str(row.awb) if row.awb is not None else "S/I"),
            ("H B/L: ", str(row.hawb) if row.hawb is not None else "S/I"),
            ("Referencia: ", str(row_number) if row_number is not None else "S/I"),
            ("Posición: ", str(row.posicion) if row.posicion is not None else "S/I"),
            ("Seguimiento: ", str(row.seguimiento) if row.seguimiento is not None else "S/I"),
            ("Consignatario: ", str(row.consignatario) if row.consignatario is not None else "S/I"),
            ("Embarcador: ", str(row.embarcador) if row.embarcador is not None else "S/I"),
            ("Orden cliente: ", str(row.orden_cliente) if row.orden_cliente is not None else "S/I"),
            ("Ref. proveedor: ", str(row.ref_proveedor) if row.ref_proveedor is not None else "S/I"),
            ("Mercadería: ", str(merca) if merca is not None else "S/I"),
        ])

        for campo, valor in campos:
            tabla_html += f"<tr><th align='left'>{campo}</th><td>{valor}</td></tr>"

        tabla_html += "</table> <br><br>"
        texto += tabla_html

        mini_tabla_html = f"""
                <table border= "1" style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr>
                            <th style="padding: 8px; text-align: left;">Origen</th>
                            <th style="padding: 8px; text-align: left;">Destino</th>
                            <th style="padding: 8px; text-align: left;">Vapor/Vuelo</th>
                            <th style="padding: 8px; text-align: left;">Viaje</th>
                            <th style="padding: 8px; text-align: left;">Salida</th>
                            <th style="padding: 8px; text-align: left;">Llegada</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style='padding: 8px;'>{str(row.origen) if row.origen is not None else "S/I"}</td>
                            <td style="padding: 8px;">{str(row.destino) if row.destino is not None else "S/I"}</td>
                            <td style="padding: 8px;">{str(row.vapor) if row.vapor is not None else "S/I"}</td>
                            <td style="padding: 8px;">{str(row.viaje) if row.viaje is not None else "S/I"}</td>
                            <td style="padding: 8px;">{format_fecha(row.fecha_embarque)}</td>
                            <td style="padding: 8px;">{format_fecha(row.fecha_retiro)}</td>
                        </tr>
                    </tbody>
                </table>
                <br>
                """

        texto += mini_tabla_html

        return texto, resultado

    elif title == 'Novedades sobre la carga':

        fecha_actual = datetime.now()
        # ASUNTO DEL MENSAJE
        resultado['asunto'] = 'NOVEDADES SOBRE LA CARGA - Ref.: ' + str(row.referencia) + \
                              '/ CS: ' + str(row.seguimiento) + '- Shipper: ' + str(row.embarcador) + \
                              '; Consignee: ' + str(row.consignatario)
        # CUERPO DEL MENSAJE
        fecha_formateada = fecha_actual.strftime(
            f'{DIAS_SEMANA[fecha_actual.weekday()]}, %d de {MESES[fecha_actual.month - 1]} del %Y')
        texto += fecha_formateada.capitalize().upper() + '<br><br>'
        tabla_html = "<table border= '1' style='width: 40%; border-collapse: collapse;'>"

        campos = []

        cont = 1
        for m in merca:
            campos.append((f"Mercadería {cont}: ", str(m.nombre) if m.nombre is not None else "S/I"))
            cont = cont + 1

        cont = 1
        for b in row2:
            campos.append((f"Bultos {cont}: ", b.bultos if b.bultos is not None else "S/I"))
            campos.append((f"Peso {cont}: ", b.bruto if b.bruto is not None else "S/I"))
            campos.append((f"CBM {cont}: ", b.cbm if b.cbm is not None else "S/I"))
            cont = cont + 1

        cont = 1
        for e in row3:
            campos.append((f"Nro. Contenedor {cont}: ", str(e.nrocontenedor) if e.nrocontenedor is not None else "S/I"))
            campos.append((f"Precintos {cont}: ", str(e.precinto) if e.precinto is not None else "S/I"))
            cont = cont + 1

        campos.extend([
            ("Embarque: ", str(row_number) if row_number is not None else "S/I"),
            ("Posición: ", str(row.posicion) if row.posicion is not None else "S/I"),
            ("Salida: ", format_fecha(row.fecha_embarque)),
            ("LLegada: ", format_fecha(row.fecha_retiro)),
            ("Origen: ", str(row.origen) if row.origen is not None else "S/I"),
            ("Destino: ", str(row.destino) if row.destino is not None else "S/I"),
            ("Vapor: ", str(row.vapor) if row.vapor is not None else "S/I"),
            ("H B/L: ", str(row.hawb) if row.hawb is not None else "S/I"),
            ("Embarcador: ", str(row.embarcador) if row.embarcador is not None else "S/I"),
            ("Consignatario: ", str(row.consignatario) if row.consignatario is not None else "S/I"),
        ])


        # campos = [
        #     ("Embarque: ", str(row_number) if row_number is not None else "S/I"),
        #     ("Posición: ", str(row.posicion) if row.posicion is not None else "S/I"),
        #     ("Salida: ", format_fecha(row.fecha_embarque)),
        #     ("LLegada: ", format_fecha(row.fecha_retiro)),
        #     ("Origen: ", str(row.origen) if row.origen is not None else "S/I"),
        #     ("Destino: ", str(row.destino) if row.destino is not None else "S/I"),
        #     ("Vapor: ", str(row.vapor) if row.vapor is not None else "S/I"),
        #     ("H B/L: ", str(row.hawb) if row.hawb is not None else "S/I"),
        #     ("Embarcador: ", str(row.embarcador) if row.embarcador is not None else "S/I"),
        #     ("Consignatario: ", str(row.consignatario) if row.consignatario is not None else "S/I"),
        #     #("Depósito: ", str() if  is not None else "S/I"),
        #
        #
        # ]

        for campo, valor in campos:
            tabla_html += f"<tr><th align='left'>{campo}</th><td>{valor}</td></tr>"

        tabla_html += "</table> <br><br>"
        texto += tabla_html

        return texto, resultado

    elif title == 'Routing Order':
        hora_actual = datetime.now().strftime("%H:%M")
        # ASUNTO DEL MENSAJE
        resultado['asunto'] = 'ROUTING ORDER - Ref.: ' + str(row.referencia) + \
                              '/ CS: ' + str(row.seguimiento) + '- Shipper: ' + str(row.embarcador) + \
                              '; Consignee: ' + str(row.consignatario)
        # CUERPO DEL MENSAJE
        texto += f'{hora_actual} <br>'
        tabla_html1 = "<table border= '1' style='width: 40%; border-collapse: collapse;'>"
        campos1 = [
            ("Fecha: ", format_fecha(fecha_actual)),
            ("A: ", str(row.agente) if row.agente is not None else "S/I"),
            ("Departamento: ", "MARITIMO"),
            #("Enviado: ", str(request.user.first_name) + ' ' + str(request.user.last_name) + ' <br>')
        ]

        for campo, valor in campos1:
            tabla_html1 += f"<tr><th align='left'>{campo}</th><td>{valor}</td></tr>"

        tabla_html1 += "</table> <br><br>"
        texto += tabla_html1
        texto += ("Estimados Sres.: <br>"
                  "Por favor, contactar la siguiente compañía para coordinar la operación referenciada: <br><br>")

        tabla_html2 = "<table border= '1' style='width: 40%; border-collapse: collapse;'>"
        campos2 = [
            ("Proveedor: ", str(row.embarcador) if row.embarcador is not None else "S/I"),
            ("Direccion: ", str(row.direccion_embarcador) if row.direccion_embarcador is not None else "S/I"),
            ("Ciudad: ", str(row.ciudad_embarcador) if row.ciudad_embarcador is not None else "S/I"),
            ("Pais: ", str(row.pais_embarcador) if row.pais_embarcador is not None else "S/I"),
        ]

        for campo, valor in campos2:
            tabla_html2 += f"<tr><th align='left'>{campo}</th><td>{valor}</td></tr>"

        tabla_html2 += "</table> <br><br>"
        texto += tabla_html2

        tabla_html3 = "<table border= '1' style='width: 40%; border-collapse: collapse;'>"
        campos3 = [
            ("Proveedor: ", str(row.consignatario) if row.consignatario is not None else "S/I"),
            ("Direccion: ", str(row.direccion_consignatario) if row.direccion_consignatario is not None else "S/I"),
            ("Ciudad: ", str(row.ciudad_consignatario) if row.ciudad_consignatario is not None else "S/I"),
            ("Pais: ", str(row.pais_consignatario) if row.pais_consignatario is not None else "S/I"),
        ]

        for campo, valor in campos3:
            tabla_html3 += f"<tr><th align='left'>{campo}</th><td>{valor}</td></tr>"

        tabla_html3 += "</table> <br><br>"
        texto += tabla_html3

        tabla_html4 = "<table border= '1' style='width: 40%; border-collapse: collapse;'>"
        campos4 = [
            ("Referencia interna: ", str(row_number) if row_number is not None else "S/I"),
            ("Orden cliente: ", str(row.orden_cliente) if row.orden_cliente is not None else "S/I"),
            ("Origen: ", str(row.origen) if row.origen is not None else "S/I"),
            ("Destino: ", str(row.destino) if row.destino is not None else "S/I"),
        ]

        for campo, valor in campos4:
            tabla_html4 += f"<tr><th align='left'>{campo}</th><td>{valor}</td></tr>"

        tabla_html4 += "</table> <br><br>"
        texto += tabla_html4

        tabla_html5 = "<table border= '1' style='width: 40%; border-collapse: collapse;'>"
        campos5 = []
        cont = 1
        for m in merca:
            campos5.append((f"Mercadería {cont}: ", str(m.nombre) if m.nombre is not None else "S/I"))
            cont = cont + 1

        cont = 1
        for b in row2:
            campos5.append((f"Bultos {cont}: ", b.bultos if b.bultos is not None else "S/I"))
            campos5.append((f"Peso {cont}: ", b.bruto if b.bruto is not None else "S/I"))
            cont = cont + 1

        campos5.append(("Condiciones de pago: ", str(row.pago_flete) if row.pago_flete is not None else "S/I"))
        campos5.append(("Términos de compra: ", str(row.terminos) if row.terminos is not None else "S/I"))
        campos5.append(("Modo de embarque: ", "MARITIMO"))

        for campo, valor in campos5:
            tabla_html5 += f"<tr><th align='left'>{campo}</th><td>{valor}</td></tr>"

        tabla_html5 += "</table> <br><br>"
        texto += tabla_html5

        return texto, resultado


    elif title == 'Notificación de llegada de carga':

        resultado['asunto'] = 'NOTIFICACION DE LLEGADA DE CARGA - Ref.: ' + str(embarque.numero) + ' - CS: ' + str(

            row.seguimiento) + '- HB/l: ' + str(row.hawb) + ' - Ship: ' + str(row.embarcador) + ' - Consig: ' \
 \
                                                                                                '' + str(

            row.consignatario) + '; Vapor: ' + str(row.transportista)

        # # TEXTO DE CUERPO DEL MENSAJE

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        fecha_actual = datetime.now()

        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

        consigna = Clientes.objects.get(codigo=embarque.consignatario)

        conex = ExpterraConexaerea.objects.filter(numero=embarque.numero).order_by('-id').last()

        carga = ExpterraCargaaerea.objects.filter(numero=embarque.numero)

        gastos = ExpterraServiceaereo.objects.filter(numero=embarque.numero)

        texto += fecha_formateada + '<br>'

        texto += '<p>Att. </p><br>'

        texto += formatear_linea("Notificar a", row.consignatario)

        texto += formatear_linea("Dirección", consigna.direccion if consigna else "")

        texto += formatear_linea("Teléfono", consigna.telefono if consigna else "")

        texto += '<br>'

        texto += formatear_linea("Salida", conex.salida if conex else "")

        texto += formatear_linea("Llegada", conex.llegada if conex else "")

        texto += formatear_linea("Origen", conex.origen if conex else "")

        texto += formatear_linea("Destino", conex.destino if conex else "")

        texto += formatear_linea("HAWB", embarque.hawb)

        texto += formatear_linea("Referencia", embarque.numero)

        texto += formatear_linea("Posición", embarque.posicion)

        texto += formatear_linea("Seguimiento", row.seguimiento)

        texto += formatear_linea("Embarcador", row.embarcador)

        texto += formatear_linea("Ref. Proveedor", row.embarcador)

        if carga:

            for c in carga:
                ap1 = float(c.cbm) * 166.67

                aplicable = round(ap1, 2) if ap1 > float(c.bruto) else float(c.bruto)

                texto += formatear_linea("Mercadería", c.producto.nombre)

                texto += formatear_linea("Bultos", str(c.bultos))

                texto += formatear_linea("Peso", str(c.bruto))

                texto += formatear_linea("Aplicable", str(aplicable))

            texto += '<br>'

        if gastos:

            texto += '<p>Detalle de gastos en Dólares U.S.A </p>'

            total_gastos = 0

            total_iva = 0

            for g in gastos:

                servicio = Servicios.objects.get(codigo=g.servicio)

                total_gastos += float(g.precio)

                iva = True if servicio.tasa == 'B' else False

                if iva:
                    total_iva += float(g.precio) * 0.22

                if g.precio != 0:
                    texto += formatear_linea(servicio.nombre, f"${g.precio:.2f}")

            texto += '<br>'

            texto += formatear_linea("TOTAL DE GASTOS", f"${total_gastos:.2f}")

            texto += formatear_linea("I.V.A", f"${total_iva:.2f}")

            texto += formatear_linea("TOTAL A PAGAR", f"${total_gastos + total_iva:.2f}")

            texto += '<br>'

        texto += 'Les informamos que por razones de seguridad los pagos solo pueden hacerse por transferencia bancaria a la siguiente cuenta: <br><br>'

        texto += 'BBVA URUGUAY S.A.<br>'

        texto += '25 de Mayo 401 <br>'

        texto += 'Cuenta Número: 5207347 <br>'

        texto += 'OCEANLINK Ltda. <br><br>'

        texto += 'Los buques, vuelos y las fechas pueden variar sin previo aviso y son siempre a CONFIRMAR. <br>'

        texto += 'Agradeciendo vuestra preferencia, le saludamos muy atentamente. <br><br>'

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

        carga = ExpterraCargaaerea.objects.get(numero=row.numero)
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


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data).decode("utf-8")
        return base64_data
