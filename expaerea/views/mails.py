import locale
from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import base64
from django.views.decorators.csrf import csrf_exempt
from expaerea.models import VEmbarqueaereo, ExportCargaaerea, ExportServiceaereo, VGastosHouse, ExportEmbarqueaereo as Embarqueaereo
from mantenimientos.views.bancos import is_ajax
from mantenimientos.models import Productos, Clientes, Monedas
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
            #9155
            embarque=Embarqueaereo.objects.get(numero=row_number)
            row = VEmbarqueaereo.objects.get(numero=row_number)
            row2 = ExportCargaaerea.objects.filter(numero=row_number)
            gastos = VGastosHouse.objects.filter(numero=row_number)
            email_cliente = Clientes.objects.get(codigo=embarque.consignatario).emailea

            try:
                seg = VGrillaSeguimientos.objects.get(numero=row.seguimiento)
                seguimiento = VGrillaSeguimientos.objects.get(numero=row.seguimiento)
            except VGrillaSeguimientos.DoesNotExist:
                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='', deposito='', pago='',vendedor='')
                seg = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='', deposito='', pago='',vendedor='')

            texto = ''

            texto += f'<br>'
            texto, resultado = get_data_html(row_number, row, row2,seg, title, texto, resultado,seguimiento,gastos,embarque)
            texto += '<b>OCEANLINK,</b><br>'
            # texto += str(request.user.first_name) + ' ' + str(request.user.last_name) + ' <br>'
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


def get_data_html(row_number, row, row2,seg, title, texto, resultado,seguimiento,gastos,embarque):
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


        campos.extend([
            ("Vapor: ", str(seg.vapor) if seg.vapor is not None else "S/I"),
            ("Viaje: ", str(seg.viaje) if seg.viaje is not None else "S/I"),
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
                            <td style="padding: 8px;">{str(seg.vapor) if seg.vapor is not None else "S/I"}</td>
                            <td style="padding: 8px;">{str(seg.viaje) if seg.viaje is not None else "S/I"}</td>
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
            cont = cont + 1


        campos.extend([
            ("Embarque: ", str(row_number) if row_number is not None else "S/I"),
            ("Posición: ", str(row.posicion) if row.posicion is not None else "S/I"),
            ("Salida: ", format_fecha(row.fecha_embarque)),
            ("LLegada: ", format_fecha(row.fecha_retiro)),
            ("Origen: ", str(row.origen) if row.origen is not None else "S/I"),
            ("Destino: ", str(row.destino) if row.destino is not None else "S/I"),
            ("Vapor: ", str(seg.vapor) if seg.vapor is not None else "S/I"),
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

        resultado['asunto'] = 'NOTIFICACION DE LLEGADA DE CARGA - Ref.: ' + str(seguimiento.refproveedor) + ' - CS: ' + str(
            row.seguimiento) + \
                              '- HB/l: ' + str(row.hawb) + ' - Ship: ' + str(row.embarcador) + ' - Consig: ' \
                                                                                               '' + str(
            row.consignatario)
        # # TEXTO DE CUERPO DEL MENSAJE
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

        texto += fecha_formateada + '<br><br>'
        tabla_html = "<table style='width:40%'>"
        campos = [
            ("Att.", ""),
            ("Cliente", str(seguimiento.cliente)),
            ("Embarque", str(row.fecha_embarque.strftime("%d/%m/%Y")) if isinstance(row.fecha_embarque, datetime) else ""),
            ("Llegada", str(row.fecha_retiro.strftime("%d/%m/%Y")) if isinstance(row.fecha_retiro, datetime) else ""),
        ]
        for campo, valor in campos:
            tabla_html += f"<tr><th align='left'>{campo}</th><td>{valor}</td></tr>"
        tabla_html += f"<tr><th align='left'>Origen</th><td>{str(row.origen)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Destino</th><td>{str(row.destino)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Transportista</th><td>{str(row.transportista)}</td></tr>"
        tabla_html += f"<tr><th align='left'>B/L</th><td>{str(row.awb)}</td></tr>"
        tabla_html += f"<tr><th align='left'>H B/L</th><td>{str(row.hawb)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Referencia</th><td>{str(seguimiento.refproveedor)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Posicion</th><td>{str(row.posicion)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Nro embarque</th><td>{str(row.numero)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Embarcador</th><td>{str(row.embarcador)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Consignatario</th><td>{str(row.consignatario)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Notificante</th><td>{str(row.consignatario)}</td></tr>"

        # Detalles de los contenedores
        cantidad_cntr = ""
        contenedores = ""
        precintos = ""
        movimiento = ""
        mercaderias = ""
        bultos = 0
        peso = 0
        volumen = 0


        texto += '<b>Detalle de gastos  en Dólares</b><br>'
        tabla_html = "<table border='1'>"

        # Definimos los campos de gasto con sus respectivos valores
        for g in gastos:
            if str(g.modo)=='C':
                modo='Collect'
            else:
                modo='Prepaid'

            tabla_html += f"<tr><th align='left'>Servicio</th><td>{str(g.servicio)}</td></tr>"
            tabla_html += f"<tr><th align='left'>Moneda</th><td>{str(g.moneda)}</td></tr>"
            tabla_html += f"<tr><th align='left'>Modo</th><td>{modo}</td></tr>"
            tabla_html += f"<tr><th align='left'>Precio</th><td>{str(g.precio)}</td></tr>"
            tabla_html += f"<tr><th align='left'>Costo</th><td>{str(g.costo)}</td></tr>"
            tabla_html += f"<tr><th align='left'>Tipo de Gasto</th><td>{str(g.tipogasto)}</td></tr>"
            tabla_html +="<tr><th></th><td></td></tr>"

        tabla_html += "</table><br>"
        texto += tabla_html

        texto += 'Les informamos que por razones de seguridad los pagos solo pueden hacerse por transferencia bancaria a la siguiente cuenta: <br><br>'
        texto += 'BBVA URUGUAY S.A.<br>'
        texto += '25 de Mayo 401 <br>'
        texto += 'Cuenta Número: 5207347 <br>'
        texto += 'OCEANLINK Ltda. <br><br>'
        texto += 'Los buques, vuelos y las fechas pueden variar sin previo aviso y son siempre a CONFIRMAR. <br>'
        texto+='Agradeciendo vuestra preferencia, le saludamos muy atentamente. <br><br>'

        texto += '</table>'

        return texto, resultado

    elif title == 'Instruccion de embarque':
        embarcador = Clientes.objects.get(codigo=embarque.embarcador)
        consignatario = Clientes.objects.get(codigo=embarque.consignatario)
        cliente = Clientes.objects.get(codigo=embarque.cliente)
        mercaderia=ExportCargaaerea.objects.filter(numero=row.numero)
        moneda=Monedas.objects.get(codigo=embarque.moneda)

        try:
            if seguimiento.refproveedor.isdigit():
                proveedor = Clientes.objects.get(codigo=seguimiento.refproveedor)
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

        resultado['asunto'] = 'INSTRUCCIÓN DE EMBARQUE - Ref.: ' + str(seguimiento.refproveedor) + ' - Shipper: ' + str(
            embarcador.empresa) + ' - Consignee: ' + str(consignatario.empresa)

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

        texto += '<br><br>'
        tabla_html = "<table style='width:40%'>"
        tabla_html += f"<tr><th align='left'>Fecha: </th><td>{fecha_formateada}</td></tr>"
        tabla_html += f"<tr><th align='left'>A: </th><td>{str(cliente.empresa)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Departamento: </th><td>MARITIMO</td></tr>"
        tabla_html += f"<tr><th align='left'>Envíado: </th><td>...</td></tr>"
        tabla_html += "</table><br>"
        tabla_html+="<p>Estimados Seres.:</p><br>"
        tabla_html+="<p>Por favor, contactar a la siguiente compañía para coordinar la operación referenciada:</p><br>"
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
        tabla_html += f"<tr><th align='left'>Puerto de carga: </th><td>{str(embarque.origen)}</td></tr>"
        tabla_html += f"<tr><th align='left'>Puerto de descarga: </th><td>{str(embarque.destino)}</td></tr>"
        tabla_html += "</table><br>"

        for m in mercaderia:
            tabla_html += "<table style='width:40%'>"
            tabla_html += f"<tr><th align='left'>Mercaderia: </th><td>{m.producto}</td></tr>"
            tabla_html += f"<tr><th align='left'>Bultos: </th><td>{m.bultos}</td></tr>"
            tabla_html += f"<tr><th align='left'>Kilos: </th><td>{m.bruto}</td></tr>"

        condicion_pago = "Collect" if row.pago_flete == "C" else "Prepaid" if row.pago_flete == "P" else ""
        tabla_html += f"<tr><th align='left'>Condiciones de pago: </th><td>{condicion_pago}</td></tr>"
        tabla_html += f"<tr><th align='left'>Términos de compra: </th><td>{row.terminos}</td></tr>"
        tabla_html += f"<tr><th align='left'>Modo de embarque: </th><td>MARITIMO</td></tr>"
        tabla_html += f"<tr><th align='left'>Moneda: </th><td>{moneda.nombre}</td></tr>"
        tabla_html += "</table><br>"

        return tabla_html, resultado

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

        carga = ExportCargaaerea.objects.get(numero=row.numero)
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
