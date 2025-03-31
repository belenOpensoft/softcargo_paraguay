import json

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
import base64
from django.views.decorators.csrf import csrf_exempt
from impomarit.models import VEmbarqueaereo, Cargaaerea, Envases, Serviceaereo, VGastosHouse, Embarqueaereo, Conexaerea
from mantenimientos.models import Productos, Clientes, Monedas, Servicios, Vapores
from mantenimientos.views.bancos import is_ajax
import locale
from datetime import datetime
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
            master = request.POST['master']
            gastos_boolean = request.POST['gastos']
            #9155
            embarque=Embarqueaereo.objects.get(numero=row_number)
            row = VEmbarqueaereo.objects.get(numero=row_number)
            row2 = Cargaaerea.objects.filter(numero=row_number)
            row3 = Envases.objects.filter(numero=row_number)
            gastos =VGastosHouse.objects.filter(numero=row_number)
            email_cliente = Clientes.objects.get(codigo=embarque.consignatario).emailim if embarque.consignatario is not None else 'S/I'
            email_agente = Clientes.objects.get(codigo=embarque.agente).emailim if embarque.agente is not None else 'S/I'

            if embarque.vapor is not None and embarque.vapor.isdigit():
                vapor = Vapores.objects.get(codigo=embarque.vapor).nombre
            elif embarque.vapor is not None:
                vapor = embarque.vapor
            else:
                vapor = 'S/I'

            try:
                seguimiento = VGrillaSeguimientos.objects.get(numero=row.seguimiento)
            except VGrillaSeguimientos.DoesNotExist:
                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='',deposito='', pago='', vendedor='')

            texto = ''
            texto += f'<br>'
            texto, resultado = get_data_html(row_number, row, row2, row3, title, texto, resultado,seguimiento,gastos,embarque,transportista,master,gastos_boolean,vapor)
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


def get_data_html(row_number, row, row2, row3, title, texto, resultado,seguimiento,gastos,embarque,transportista_boolean,master_boolean,gastos_boolean,vapor):
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
            ("Vapor: ", str(vapor)),
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
                            <td style="padding: 8px;">{str(vapor)}</td>
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
            ("Vapor: ", str(vapor)),
            ("H B/L: ", str(row.hawb) if row.hawb is not None else "S/I"),
            ("Embarcador: ", str(row.embarcador) if row.embarcador is not None else "S/I"),
            ("Consignatario: ", str(row.consignatario) if row.consignatario is not None else "S/I"),
        ])


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
                                                                                               '' + str(
            row.consignatario) + '; Vapor: ' + str(vapor)
        # # TEXTO DE CUERPO DEL MENSAJE
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

        consigna = Clientes.objects.get(codigo=embarque.consignatario)
        conex = Conexaerea.objects.filter(numero=embarque.numero).order_by('-id').last()
        carga = Cargaaerea.objects.filter(numero=embarque.numero)
        gastos = Serviceaereo.objects.filter(numero=embarque.numero)


        texto += fecha_formateada + '<br>'
        texto += '<p>Att. </p><br>'
        texto += formatear_linea("Notificar a", row.consignatario)
        texto += formatear_linea("Dirección", consigna.direccion if consigna else "")
        texto += formatear_linea("Teléfono", consigna.telefono if consigna else "")

        texto +='<br>'

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
                #ap1 = float(c.cbm) * 166.67
                ap1 = float(c.cbm) if c.cbm is not None else 0 * 166.67
                aplicable = round(ap1, 2) if ap1 > float(c.bruto) else float(c.bruto)

                texto += formatear_linea("Mercadería", c.producto.nombre)
                texto += formatear_linea("Bultos", str(c.bultos))
                texto += formatear_linea("Peso", str(c.bruto))
                texto += formatear_linea("Aplicable", str(aplicable))

            texto += '<br>'

        if gastos_boolean == 'true':
            if gastos:
                texto += '<p>Detalle de gastos en Dólares U.S.A </p>'
                total_gastos=0
                total_iva=0
                for g in gastos:
                    servicio = Servicios.objects.get(codigo=g.servicio)
                    total_gastos+= float(g.precio)
                    iva = True if servicio.tasa == 'B' else False
                    if iva:
                        total_iva+=float(g.precio) * 0.22
                    if g.precio !=0:
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
        texto+='Agradeciendo vuestra preferencia, le saludamos muy atentamente. <br><br>'


        return texto, resultado

    elif title == 'Release documentacion':

        try:

            resultado['asunto'] = 'RELEASE DOCUMENTACION - FCR.: ' + str(row.hawb or '') + ' - SEGUIMIENTO' + str(
                row.seguimiento or '')

            # TEXTO DE CUERPO DEL MENSAJE

            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Revisa si este ajuste de idioma causa problemas

            fecha_actual = datetime.now()

            fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

            texto += fecha_formateada + '<br><br>'

            texto += '<p>Estimados, </p><br>'

            texto += '<p>Informamos a Uds. que se encuentra a vuestra disposición para ser retirada en nuestras oficinas la documentación correspondiente a la libreación </p>'

            texto += '<p>del siguiente embarque: </p><br>'

            texto += f'<p>FCR: {row.hawb or ""} </p>'

            texto += f'<p>BUQUE: {vapor or ""} </p>'

            texto += '<p>Favor presentar para dicha liberación de los FCR correspondientes a este embarque. </p>'

            texto += '<p>Nuestro horario para transferencias es de lunes a viernes de 08.30 a 12.00 y de 13.00 a 16.30 hrs. </p>'

            texto += '<p>Saludos, </p><br>'

            return texto, resultado

        except Exception as e:
            return None, {"resultado": "error", "mensaje": f"Error en 'Relese documentación': {e}"}

    elif title == 'Instruccion de embarque':
        embarcador = Clientes.objects.get(codigo=embarque.embarcador)
        consignatario = Clientes.objects.get(codigo=embarque.consignatario)
        cliente = Clientes.objects.get(codigo=embarque.cliente)
        mercaderia=Cargaaerea.objects.filter(numero=row.numero)
        moneda=Monedas.objects.get(codigo=embarque.moneda)

        try:
            if seguimiento.embarcador is not None and seguimiento.embarcador.isdigit():
                proveedor = Clientes.objects.get(codigo=seguimiento.embarcador)
                direccion = proveedor.direccion
                empresa = proveedor.empresa
                ciudad = proveedor.ciudad
                pais = proveedor.pais
            else:
                direccion = ''
                empresa = ''
                ciudad = ''
                pais = ''

        except Clientes.DoesNotExist:
            direccion = ''
            empresa = ''
            ciudad = ''
            pais = ''

        resultado['asunto'] = 'INSTRUCCIÓN DE EMBARQUE - Ref.: ' + str(seguimiento.numero) + ' - Shipper: ' + str(
            embarcador.empresa) + ' - Consignee: ' + str(consignatario.empresa)

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()
        if isinstance(seguimiento.eta, datetime):
            llegada = str(seguimiento.eta.strftime("%d/%m/%Y"))
        else:
            llegada = ''
        tabla_html = "<table style='width:40%'>"
        tabla_html += f"<tr><th align='left'>Fecha: </th><td>{fecha_formateada}</td></tr>"
        tabla_html += f"<tr><th align='left'>A: </th><td>{str(cliente.empresa)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Departamento: </th><td>MARITIMO</td></tr>"
        tabla_html += f"<tr><th align='left'>Envíado: </th><td>...</td></tr>"
        tabla_html += "</table><br>"
        tabla_html+="<p>Estimados Seres.:</p><br>"
        tabla_html+="<p>Por favor, contactar a la siguiente compañía para coordinar la operación referenciada:</p>"
        tabla_html += "<table style='width:40%'>"
        tabla_html += f"<tr><th align='left'>Proveedor: </th><td>{str(empresa)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Dirección: </th><td>{str(direccion)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Ciudad: </th><td>{str(ciudad)}</td></tr>"
        tabla_html += f"<tr><th align='left'>País: </th><td>{str(pais)}</td></tr><br><br>"
        tabla_html += f"<tr><th align='left'>Consignatario: </th><td>{str(consignatario.empresa)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Dirección: </th><td>{str(consignatario.direccion)}</td></tr>"
        tabla_html += f"<tr><th align='left'>País: </th><td>{str(consignatario.pais)}</td></tr>"
        tabla_html += f"<tr><th align='left'>RUC: </th><td>{str(consignatario.ruc)}</td></tr><br><br>"
        tabla_html += f"<tr><th align='left'>Referencia interna: </th><td>{seguimiento.refproveedor}/{row.numero}</td></tr>"
        tabla_html += f"<tr><th align='left'>Posición: </th><td>{str(row.posicion)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Recepcion estimada de mercaderia </th><td>{str(llegada)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Puerto de carga: </th><td>{str(embarque.loading)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Puerto de descarga: </th><td>{str(embarque.discharge)}</td></tr>"
        tabla_html += "</table><br>"

        for m in mercaderia:
            tabla_html += "<table style='width:40%'>"
            tabla_html += f"<tr><th align='left'>Mercaderia: </th><td>{m.producto}</td></tr>"
            tabla_html += f"<tr><th align='left'>Bultos: </th><td>{m.bultos}</td></tr>"
            tabla_html += f"<tr><th align='left'>Kilos: </th><td>{m.bruto}</td></tr>"
            tabla_html += f"<tr><th align='left'>Volúmen: </th><td>{m.cbm}</td></tr>"

        envase_text=''
        if row3:
            for e in row3:
                cantidad = e.cantidad if e.cantidad is not None else 0
                tipo = e.tipo if e.tipo is not None else 'S/I'
                unidad = e.unidad if e.unidad is not None else 'S/I'
                nrocontenedor=e.nrocontenedor if e.nrocontenedor is not None else 'S/I'
                envase_text+=str(cantidad)+'x'+str(unidad)+' '+str(tipo)+': '+str(nrocontenedor)
                if len(row3) > 1:
                    envase_text+='<br>'

        condicion_pago = "Collect" if row.pago_flete == "C" else "Prepaid" if row.pago_flete == "P" else ""
        tabla_html += f"<tr><th align='left'>Condiciones de pago: </th><td>{condicion_pago}</td></tr>"
        tabla_html += f"<tr><th align='left'>Términos de compra: </th><td>{row.terminos}</td></tr>"
        tabla_html += f"<tr><th align='left'>Modo de embarque: </th><td>MARITIMO</td></tr>"
        tabla_html += f"<tr><th align='left'>Envase: </th><td>{envase_text}</td></tr>"
        tabla_html += f"<tr><th align='left'>Moneda: </th><td>{moneda.nombre}</td></tr>"
        tabla_html += "</table><br>"

        return tabla_html, resultado

    elif title == 'Liberacion':

        resultado['asunto'] = 'LIBERACIÓN: ' + str(row.awb) + ' - seguimiento: ' + str(
            row.seguimiento)

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

        tabla_html = fecha_formateada+"<br><br>"
        tabla_html += f"<p>ESTIMADOS, SOLICITAMOS LA LIBERACIÓN DEL SIGUIENTE BL:{row.awb}</p><br>"
        tabla_html += f"<p>ADJUNTAMOS:</p>"
        tabla_html += f"<p>*BL {row.awb} ENDOSADO</p>"
        tabla_html += f"<p>*ARRIVAL NOTICE ENDOSADO</p>"
        tabla_html += f"<p>*CONTRATO DE RESPONSABILIDAD</p>"
        tabla_html += f"<p>*COMPROBANTE DE PAGO</p><br>"
        tabla_html += f"<p>SALUDOS,</p><br>"



        return tabla_html, resultado

    elif title == 'Aviso de embarque':

        resultado['asunto'] = 'AVISO DE EMBARQUE / Ref: ' + str(row.seguimiento) + ' ' \
         \
                                                                              '- HB/l: ' + str(

            row.hawb) + ' - Shipper: ' + str(row.embarcador) + ' - Consig: ' \
         \
                                                               '' + str(row.consignatario) + '; Vapor: ' + str(

            vapor)

        fecha_actual = datetime.now()

        fecha_formateada = fecha_actual.strftime(

            f'{DIAS_SEMANA[fecha_actual.weekday()]}, %d de {MESES[fecha_actual.month - 1]} del %Y')

        texto = fecha_formateada.capitalize() + '<br><br>'

        texto += 'Sres.: <br>'

        texto += str(row.consignatario) + '<br>'

        texto += '<b>DEPARTAMENTO DE COMERCIO EXTERIOR </b><br><br>'

        if isinstance(seguimiento.etd, datetime):

            salida = str(seguimiento.etd.strftime("%d/%m/%Y"))

        else:

            salida = ''

        if isinstance(seguimiento.eta, datetime):

            llegada = str(seguimiento.eta.strftime("%d/%m/%Y"))

        else:

            llegada = ''

        # Campos con valores formateados

        ref = str(row.seguimiento) + "/" + str(row.numero)

        texto += formatear_linea("Referencia", ref)

        texto += formatear_linea("Posición", str(row.posicion) if row.posicion else "")

        #texto += formatear_linea("Proveedor", str(row.cliente) if row.cliente else "")

        texto += formatear_linea("Consignatario", str(row.consignatario) if row.consignatario else "")

        texto += formatear_linea("Orden Cliente", str(embarque.ordencliente) if embarque.ordencliente else "")

        texto += formatear_linea("Ref. Proveedor", str(embarque.refproveedor) if embarque.refproveedor else "")

        texto += formatear_linea("Términos de Compra", str(row.terminos) if row.terminos else "")

        texto += formatear_linea("Vapor", str(vapor) if vapor else "")

        texto += '<br>'

        texto += formatear_linea("Origen", str(row.origen) if row.origen else "")

        texto += formatear_linea("Destino", str(row.destino) if row.destino else "")

        texto += formatear_linea("Salida", salida)

        texto += formatear_linea("Llegada", llegada)

        texto += '<br>'

        texto += formatear_linea("Agente", str(row.agente) if row.agente else "")

        # Datos de contenedores

        cantidad_cntr = ""

        contenedores = ""

        mercaderias = ""

        precintos = ""

        bultos = 0

        peso = 0

        volumen = 0

        cant_cntr = Envases.objects.filter(numero=row.numero).values('tipo', 'nrocontenedor', 'precinto', 'bultos', 'peso',
                                                                     'unidad', 'volumen').annotate(total=Count('id'))
        carga = Cargaaerea.objects.filter(numero=row.numero).values('producto__nombre')

        if cant_cntr.count() > 0:

            for cn in cant_cntr:
                cantidad_cntr += f' {cn["total"]} x {cn["tipo"]} - {cn["unidad"]} - '
                contenedores += f' {cn["nrocontenedor"]} - '

                if cn['precinto']:
                    precintos += f'{cn["precinto"]} - '

                bultos += cn['bultos']

                peso += cn['peso'] if cn['peso'] else 0

                volumen += cn['volumen'] if cn['volumen'] else 0

            if carga.count() > 0:
                for c in carga:
                    mercaderias+= c['producto__nombre'] + ' - '

        texto += formatear_linea("Contenedores", cantidad_cntr[:-3])

        texto += formatear_linea("Nro. Contenedor/es", contenedores[:-3])

        texto += formatear_linea("Precintos/Sellos", precintos[:-3])

        texto += formatear_linea("House", str(row.hawb) if row.hawb else "")

        if master_boolean == 'true':
            texto += formatear_linea("AWB", str(row.awb) if row.awb else "")
        if transportista_boolean == 'true':
            texto += formatear_linea("Transportista", str(row.transportista) if row.transportista else "")

        texto += formatear_linea("Peso", f"{peso} KGS")

        texto += formatear_linea("Bultos", str(bultos))

        texto += formatear_linea("CBM", f"{volumen} M³")

        texto += '<br>'

        texto += formatear_linea("Mercadería", mercaderias[:-3])

        texto += formatear_linea("Depósito", str(seguimiento.deposito) if seguimiento.deposito else "")

        texto += formatear_linea("Doc. Originales", 'SI' if seguimiento.originales and seguimiento.originales == True else 'NO')

        # Agregar información en 6 columnas

        texto += "<br>"

        texto += "<table style='width:100%; text-align:center;'>"

        texto += "<tr><th>Origen</th><th>Destino</th><th>Vapor/Vuelo</th><th>Viaje</th><th>Salida</th><th>Llegada</th></tr>"

        texto += f"<tr><td>{row.origen}</td><td>{row.destino}</td><td>{vapor}</td><td>{row.viaje}</td><td>{salida}</td><td>{llegada}</td></tr>"

        texto += "</table>"

        texto += '<br>'

        # Agregar mensaje final

        texto += 'Los buques y las fechas pueden variar sin previo aviso y son siempre a confirmar. <br>' \
         \
                 'Agradeciendo vuestra preferencia, le saludamos muy atentamente.<br><br>'

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

        carga = Cargaaerea.objects.get(numero=row.numero)
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


def formatear_linea_old(titulo, valor, ancho_fijo=30):
    max_titulo = ancho_fijo - 1

    if len(titulo) < max_titulo:
        puntos = '.' * (max_titulo - len(titulo))
        linea = titulo + puntos
    else:
        linea = titulo[:max_titulo]

    return f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>{linea}: {valor}</p>"


def formatear_linea(titulo, valor, ancho_total=50):
    linea = f"{titulo}"
    puntos = '.' * (30 - len(titulo))
    linea += puntos

    # Calcular espacios hasta llegar al ancho total
    espacio_restante = ancho_total - len(linea) - len(str(valor))
    if espacio_restante < 1:
        espacio_restante = 1

    espacios = ' ' * espacio_restante
    texto = f"<pre style='font-family: Courier New, monospace; font-size: 13px;'>{linea}{espacios}{valor}</pre>"
    return texto








