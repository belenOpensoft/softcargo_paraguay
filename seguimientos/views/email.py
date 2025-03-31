import datetime
import json
import locale

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.http import HttpResponse
import base64

from cargosystem import settings
from impomarit.views.mails import formatear_linea
from mantenimientos.models import Clientes, Servicios, Vapores, Monedas
from mantenimientos.views.bancos import is_ajax
from seguimientos.models import VGrillaSeguimientos, Envases, Cargaaerea, Conexaerea, Serviceaereo


@login_required(login_url='/')
def get_data_email(request):
    resultado = {}
    if is_ajax(request):
        try:
            dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
            meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre',
                     'octubre', 'noviembre', 'diciembre']
            tipos_operativa = {
                'IMPORT MARITIMO':'IMPORTACION MARITIMA',
                'EXPORT MARITIMO':'EXPORTACION MARITIMA',
                'IMPORT AEREO':'IMPORTACION AEREA',
                'EXPORT AEREO': 'EXPORTACION AEREA',
                'IMPORT TERRESTRE':'IMPORTACION TERRESTRE',
                'EXPORT TERRESTRE': 'EXPORTACION TERRESTRE',
            }
            title = request.POST['title']
            transportista = request.POST['transportista']
            master = request.POST['master']
            gastos_boolean = request.POST['gastos']
            row_number = request.POST['row_number']
            row = VGrillaSeguimientos.objects.get(numero=row_number)

            texto = ''
            # image_path = str(settings.BASE_DIR) +  "/cargosystem/static/images/oceanlink.png"  # Cambia esto a la ruta de tu imagen
            # base64_string = image_to_base64(image_path)
            # texto += f'<img src="data:image/jpeg;base64,{base64_string}" alt="Imagen Base64">' + '<br><br><br><br>'
            texto += f'<br>'
            if row.modo == 'IMPORT MARITIMO':
                email_cliente = row.emailim
                email_agente = Clientes.objects.get(codigo=row.agente_codigo).emailim if row.agente_codigo is not None else 'S/I'
            elif row.modo == 'EXPORT MARITIMO':
                email_cliente = row.emailem
                email_agente = Clientes.objects.get(codigo=row.agente_codigo).emailem if row.agente_codigo is not None else 'S/I'

            elif row.modo == 'IMPORT AEREO':
                email_cliente = row.emailia
                email_agente = Clientes.objects.get(codigo=row.agente_codigo).emailia if row.agente_codigo is not None else 'S/I'

            elif row.modo == 'EXPORT AEREO':
                email_cliente = row.emailea
                email_agente = Clientes.objects.get(codigo=row.agente_codigo).emailea if row.agente_codigo is not None else 'S/I'

            elif row.modo == 'IMPORT TERRESTRE':
                email_cliente = row.emailit
                email_agente = Clientes.objects.get(codigo=row.agente_codigo).emailit if row.agente_codigo is not None else 'S/I'

            elif row.modo == 'EXPORT TERRESTRE':
                email_cliente = row.emailet
                email_agente = Clientes.objects.get(codigo=row.agente_codigo).emailet if row.agente_codigo is not None else 'S/I'

            if title == 'Traspaso a operaciones':
                texto += formatear_linea("SEGUIMIENTO", row.numero)
                texto += formatear_linea("CLIENTE", row.consignatario)
                texto += formatear_linea("BL", row.awb)
                texto += formatear_linea("HBL", row.hawb)
                texto += "<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>EMBARQUE TRASPASADO A DEPARTAMENTO DE OPERACIONES</p>"

                fecha_actual = datetime.datetime.now()
                fecha_formateada = fecha_actual.strftime(
                    f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y')
                texto += formatear_linea("FECHA", fecha_formateada.capitalize())
                texto += formatear_linea("CONDICION MBL", "")
                texto += formatear_linea("CONDICION HBL", "")
                texto += formatear_linea("COURIER CON DOCS", "")
                texto += formatear_linea("COURIER/GUIA", "")

                resultado['asunto'] = f'SEGUIMIENTO {row.numero} // TRASPASO A OPERACIONES'

            elif title == 'Aviso de embarque':

                resultado[
                    'asunto'] = f'AVISO DE EMBARQUE / Ref: {row.numero} - HB/l: {row.hawb} - Shipper: {row.embarcador} - Consig: {row.consignatario}; Vapor: {row.vapor}'

                fecha_actual = datetime.datetime.now()

                fecha_formateada = fecha_actual.strftime(
                    f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y')

                texto = formatear_linea("Fecha", fecha_formateada.capitalize())

                texto += "<br>"

                texto += formatear_linea("Sres.", str(row.cliente))

                texto += formatear_linea("Depto.", "COMERCIO EXTERIOR")

                texto += "<br>"

                salida = row.etd.strftime("%d/%m/%Y") if isinstance(row.etd, datetime.datetime) else ''

                llegada = row.eta.strftime("%d/%m/%Y") if isinstance(row.eta, datetime.datetime) else ''

                ref = f"{row.numero}/{row.embarque}"

                texto += formatear_linea("Referencia", ref)

                texto += formatear_linea("Posición", row.posicion or "")

                texto += formatear_linea("Proveedor", row.cliente or "")

                texto += formatear_linea("Consignatario", row.consignatario or "")

                texto += formatear_linea("Orden Cliente", row.refcliente or "")

                texto += formatear_linea("Ref. Proveedor", row.refproveedor or "")

                texto += formatear_linea("Términos Compra", row.terminos or "")

                if str(row.vapor).isdigit():

                    vapor = Vapores.objects.get(codigo=row.vapor).nombre

                else:

                    vapor = row.vapor

                texto += formatear_linea("Vapor", vapor or "")

                texto += "<br>"

                texto += formatear_linea("Origen", row.origen_text or "")

                texto += formatear_linea("Destino", row.destino_text or "")

                texto += formatear_linea("Salida", salida)

                texto += formatear_linea("Llegada", llegada)

                texto += "<br>"

                texto += formatear_linea("Agente", row.agente or "")

                # Contenedores y carga

                cantidad_cntr = ""

                contenedores = ""

                mercaderias = ""

                precintos = ""

                bultos = 0

                peso = 0

                volumen = 0

                cant_cntr = Envases.objects.filter(numero=row.numero).values('tipo', 'nrocontenedor', 'precinto',
                                                                             'bultos', 'peso', 'unidad',
                                                                             'volumen').annotate(total=Count('id'))

                carga = Cargaaerea.objects.filter(numero=row.numero).values('producto__nombre')

                if cant_cntr.count() > 0:

                    for cn in cant_cntr:

                        cantidad_cntr += f'{cn["total"]} x {cn["tipo"]} - {cn["unidad"]} - '

                        contenedores += f'{cn["nrocontenedor"]} - '

                        if cn['precinto']:
                            precintos += f'{cn["precinto"]} - '

                        bultos += cn['bultos']

                        peso += cn['peso'] or 0

                        volumen += cn['volumen'] or 0

                if carga.count() > 0:

                    for c in carga:
                        mercaderias += c['producto__nombre'] + ' - '

                texto += formatear_linea("Contenedores", cantidad_cntr[:-3])

                texto += formatear_linea("Nro. Contenedor/es", contenedores[:-3])

                texto += formatear_linea("Precintos/Sellos", precintos[:-3])

                texto += formatear_linea("House", row.hawb or "")

                if master == 'true':
                    texto += formatear_linea("Master", row.awb or "")

                if transportista == 'true':
                    texto += formatear_linea("Transportista", row.transportista or "")

                texto += formatear_linea("Peso", f"{peso} KGS")

                texto += formatear_linea("Bultos", str(bultos))

                texto += formatear_linea("CBM", f"{volumen} M³")

                texto += "<br>"

                texto += formatear_linea("Mercadería", mercaderias[:-3])

                texto += formatear_linea("Depósito", row.deposito or "")

                texto += formatear_linea("Doc. Originales", 'SI' if row.originales else 'NO')

                texto += "<br>"

                texto += formatear_linea("Origen", row.origen_text or "")

                texto += formatear_linea("Destino", row.destino_text or "")

                texto += formatear_linea("Vapor/Vuelo", str(row.vapor) or "")

                texto += formatear_linea("Viaje", str(row.viaje) or "")

                texto += formatear_linea("Salida", salida)

                texto += formatear_linea("Llegada", llegada)

                texto += "<br>"

                texto += "<pre style='font-family: Courier New, monospace; font-size: 12px;'>"

                texto += "Los buques y las fechas pueden variar sin previo aviso y son siempre a confirmar.\n"

                texto += "Agradeciendo vuestra preferencia, le saludamos muy atentamente."

                texto += "</pre>"

            elif title == 'Notificacion llegada de carga':

                consigna = Clientes.objects.get(codigo=row.consignatario_codigo)

                conex = Conexaerea.objects.filter(numero=row.numero).order_by('-id').last()

                carga = Cargaaerea.objects.filter(numero=row.numero)

                gastos = Serviceaereo.objects.filter(numero=row.numero)

                vapor = conex.vapor if conex and conex.vapor else 'S/I'

                resultado[
                    'asunto'] = f'NOTIFICACION DE LLEGADA DE CARGA - Ref.: {row.embarque} - CS: {row.numero} - HB/l: {row.hawb} - Ship: {row.embarcador} - Consig: {row.consignatario}; Vapor/vuelo: {vapor}'

                # Fecha formateada

                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

                fecha_actual = datetime.datetime.now()

                fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

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

                texto += formatear_linea("HAWB", row.hawb)

                if master == 'true':
                    texto += formatear_linea("AWB", row.awb)

                texto += formatear_linea("Referencia", row.embarque)

                texto += formatear_linea("Posición", row.posicion)

                texto += formatear_linea("Seguimiento", row.numero)

                texto += formatear_linea("Embarcador", row.embarcador)

                texto += formatear_linea("Ref. Proveedor", row.embarcador)

                if carga:

                    for c in carga:
                        ap1 = float(c.cbm) if c.cbm is not None else 0 * 166.67

                        aplicable = round(ap1, 2) if ap1 > float(c.bruto) else float(c.bruto)

                        texto += formatear_linea("Mercadería", c.producto.nombre)

                        texto += formatear_linea("Bultos", str(c.bultos))

                        texto += formatear_linea("Peso", str(c.bruto))

                        texto += formatear_linea("Aplicable", str(aplicable))

                    texto += "<br>"

                if gastos_boolean == 'true':

                    if gastos:

                        texto += formatear_linea("Detalle", "Gastos en Dólares U.S.A")

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

            elif title == 'Aviso de desconsolidacion':
                # cantidad_cntr = ''
                # contenedores = ''
                # precintos = ''
                # movimiento = ''
                # mercaderias = ''
                # bultos = 0
                # peso = 0
                fecha_actual = datetime.datetime.now()
                resultado['asunto'] = 'AVISO DE DESCONSOLIDACION - Ref.: ' + str(row.refproveedor) + ' - CS: ' + str(row.numero) + \
                                      '- HB/l: ' + str(row.hawb) + ' - Ship: ' + str(row.embarcador)
                # # TEXTO DE CUERPO DEL MENSAJE
                fecha_formateada = fecha_actual.strftime(f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y')
                texto += fecha_formateada.capitalize().upper() + '<br><br>'
                tabla_html = "<table style='width:40%'>"
                campos = [
                    ("Att.", str("Departamento de operaciones").upper()),
                    ("Cliente", str(row.cliente)),
                    ("Direccion", str(row.direccion_cliente) if row.direccion_cliente is not None else ""),
                    ("Telefono", str(row.telefono_cliente) if row.telefono_cliente is not None else ""),
                    ("Vapor", str(row.vapor) if row.vapor is not None else ""),
                    ("Viaje", str(row.viaje) if row.viaje is not None else ""),
                    # ("Embarque", str(row.etd.strftime("%d/%m/%Y")) if isinstance(row.etd, datetime.datetime) else ""),
                    ("Llegada", str(row.eta.strftime("%d/%m/%Y")) if isinstance(row.eta, datetime.datetime) else ""),
                    ("Posicion", str(row.posicion) if row.posicion is not None else ""),
                ]
                for campo, valor in campos:
                    tabla_html += f"<tr><th align='left'>{campo}</th><td>{valor}</td></tr>"
                tabla_html += f"<tr><th align='left'>Seguimiento</th><td>{str(row.numero)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Embarcador</th><td>{str(row.embarcador)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Consignatario</th><td>{str(row.consignatario)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Orden cliente</th><td></td></tr>"
                tabla_html += f"<tr><th align='left'>Referencia proveedor</th><td>{str(row.refproveedor)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Origen</th><td>{str(row.origen_text)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Destino</th><td>{str(row.destino_text)}</td></tr>"
                # tabla_html += f"<tr><th align='left'>Loading</th><td>{str(row.loading)}</td></tr>"
                # tabla_html += f"<tr><th align='left'>Discharge</th><td>{str(row.discharge)}</td></tr>"
                # tabla_html += f"<tr><th align='left'>Transportista</th><td>{str(row.transportista)}</td></tr>"
                # tabla_html += f"<tr><th align='left'>B/L</th><td>{str(row.awb)}</td></tr>"
                # tabla_html += f"<tr><th align='left'>H B/L</th><td>{str(row.hawb)}</td></tr>"
                # tabla_html += f"<tr><th align='left'>Posicion</th><td>{str(row.posicion)}</td></tr>"
                # tabla_html += f"<tr><th align='left'>Notificante</th><td>{str(row.consignatario)}</td></tr>"
                # Detalles de los contenedores
                cantidad_cntr = ""
                contenedores = ""
                precintos = ""
                movimiento = ""
                mercaderias = ""
                bultos = 0
                peso = 0
                volumen = 0
                cant_cntr = Envases.objects.filter(numero=row.numero).values('tipo', 'nrocontenedor', 'precinto',
                                                                             'bultos', 'peso', 'envase',
                                                                             'movimiento','volumen').annotate(total=Count('id'))
                if cant_cntr.count() > 0:
                    for cn in cant_cntr:
                        cantidad_cntr += f' {cn["total"]} x {cn["tipo"]} - '
                        contenedores += f' {cn["nrocontenedor"]} - '
                        if cn['precinto'] is not None and len(cn['precinto']) > 0:
                            precintos += f'{cn["precinto"]} - '
                        bultos += cn['bultos']
                        if cn['peso'] is not None:
                            peso += cn['peso']
                        if cn['volumen'] is not None:
                            volumen += cn['volumen']
                        movimiento += cn['movimiento'] + ' - '
                        mercaderias += cn['envase'] + ' - '
                tabla_html += f"<tr><th align='left'>Contenedores</th><td>{cantidad_cntr[:-3]}</td></tr>"
                tabla_html += f"<tr><th align='left'>Nro.Contenedor/es</th><td>{contenedores[:-3]}</td></tr>"
                tabla_html += f"<tr><th align='left'>Precintos/sellos</th><td>{precintos[:-3]}</td></tr>"
                tabla_html += f"<tr><th align='left'>Bultos</th><td>{bultos}</td></tr>"
                tabla_html += f"<tr><th align='left'>Peso</th><td>{peso} KGS</td></tr>"
                tabla_html += f"<tr><th align='left'>CBM</th><td>{volumen} M³</td></tr>"
                tabla_html += f"<tr><th align='left'>Mercaderia</th><td>{mercaderias[:-3]}</td></tr>"
                tabla_html += f"<tr><th align='left'>Entrega en gate</th><td></td></tr>"
                tabla_html += f"<tr><th align='left'>Deposito</th><td>{str(row.deposito)}</td></tr>"
                # tabla_html += f"<tr><th align='left'>Movimiento</th><td>{movimiento[:-3]}</td></tr>"
                tabla_html += "</table><br><br>"
                texto += tabla_html

                texto += '<b>ATENCION!</b><br><br>'
                texto += 'DETALLE DE DESCONSOLIDACION<br><br>'
                texto += '<b>OCEANLINK,</b><br>'
                texto += str(request.user.first_name) + ' ' + str(request.user.last_name) + ' <br>'
                texto += 'DEPARTAMENTO DE ' + str(tipos_operativa[row.modo]) + ', <br>'
                texto += 'Bolonia 2280 LATU, Edificio Los Álamos, Of.103 <br>'
                texto += 'OPERACIONES <br>'
                texto += 'EMAIL: <br>'
                texto += 'TEL: +5982 2605 2332 <br>'
                texto += '</table>'
            elif title == 'Cargo release':
                fecha_actual = datetime.datetime.now()
                resultado['asunto'] = 'CARGO RELEASE - Seg.: ' + str(row.numero) +'- HB/l: ' + str(row.hawb) + ' - Shipper: ' + str(row.embarcador) + ' - CNEE: ' + str(row.consignatario)
                # # TEXTO DE CUERPO DEL MENSAJE
                fecha_formateada = fecha_actual.strftime(f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y')

                texto='<p> SEG: '+ str(row.numero) + '<br>'
                texto+='HBL: '+ str(row.hawb) + '<br>'
                texto+='Date: '+ fecha_formateada.capitalize().upper() + '<br>'
                texto+='PLEASE NOTE THAT WE REALEASED DOCS TO CONSIGNEE. <br>'
                texto+='THANK YOU VERY MUCH FOR YOUR ASSISTANCE.<br>'
                texto+='BEST REGARDS,<br>'
                texto+='OCEANLINK<br></p>'
            elif title == 'Release documentacion':
                try:
                    resultado['asunto'] = 'RELEASE DOCUMENTACION - FCR.: ' + str(
                        row.hawb or '') + ' - SEGUIMIENTO' + str(
                        row.numero or '')

                    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Revisa si este ajuste de idioma causa problemas

                    fecha_actual = datetime.datetime.now()

                    fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

                    texto = fecha_formateada + '<br><br>'

                    texto += '<p>Estimados, </p><br>'

                    texto += '<p>Informamos a Uds. que se encuentra a vuestra disposición para ser retirada en nuestras oficinas la documentación correspondiente a la libreación </p>'

                    texto += '<p>del siguiente embarque: </p><br>'

                    texto += f'<p>FCR: {row.hawb or ""} </p>'

                    texto += f'<p>BUQUE: {row.vapor or ""} </p>'

                    texto += '<p>Favor presentar para dicha liberación de los FCR correspondientes a este embarque. </p>'

                    texto += '<p>Nuestro horario para transferencias es de lunes a viernes de 08.30 a 12.00 y de 13.00 a 16.30 hrs. </p>'

                    texto += '<p>Saludos, </p><br>'
                    texto += '<p>OCEANLINK </p><br>'

                except Exception as e:
                    return None, {"resultado": "error", "mensaje": f"Error en 'Relese documentación': {e}"}
            elif title == 'Liberacion':
                resultado['asunto'] = 'LIBERACIÓN: ' + str(row.awb) + ' - seguimiento: ' + str(
                    row.numero)
                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                fecha_actual = datetime.datetime.now()
                fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

                texto = fecha_formateada + "<br><br>"
                texto += f"<p>ESTIMADOS, SOLICITAMOS LA LIBERACIÓN DEL SIGUIENTE BL:{row.awb}</p><br>"
                texto += f"<p>ADJUNTAMOS:</p>"
                texto += f"<p>*BL {row.awb} ENDOSADO</p>"
                texto += f"<p>*ARRIVAL NOTICE ENDOSADO</p>"
                texto += f"<p>*CONTRATO DE RESPONSABILIDAD</p>"
                texto += f"<p>*COMPROBANTE DE PAGO</p><br>"
                texto += f"<p>SALUDOS,</p><br>"
                texto += f"<p>OCEANLINK</p><br>"
            elif title == 'Notificacion cambio de linea':
                resultado['asunto'] = 'NOTIFICACIÓN CAMBIO DE LÍNEA / NVOCC / CÍA AEREA '
                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                fecha_actual = datetime.datetime.now()
                fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

                texto = fecha_formateada + "<br><br>"
                texto += f"<p>SEG: {row.numero}</p><br>"
                texto += f"<p>CONFIRMO CAMBIO DE LÍNEA / NVOCC / CÍA AEREA DE ESTE SEGUIMIENTO</p><br>"
                texto += f"<p>ANTERIOR: </p><br>"
                texto += f"<p>ACTUAL: {row.transportista}</p><br><br>"
                texto += f"<p>OCEANLINK</p><br>"
            elif title == 'Shipping instruction':
                tabla_html = "<table style='width:40%'>"
                # Definir los campos y sus respectivos valores
                resultado['asunto'] = 'LCC SHIPPING INSTRUCTION: Ref: ' + str(row.numero) + ' ' \
                                           ' - Shipper: ' + str(row.embarcador) + ' - Consig: ' \
                                      '' + str(row.consignatario)
                fecha_actual = datetime.datetime.now()
                fecha_formateada = fecha_actual.strftime(
                    f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y')
                texto += 'Date: '+fecha_formateada.capitalize()+' <br>'
                texto += 'To: '+str(row.agente)+' <br><br>'

                cons = Clientes.objects.get(codigo=row.consignatario_codigo)
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

                embarcador = Clientes.objects.get(codigo=row.embarcador_codigo)
                if embarcador:
                    pais = embarcador.pais
                    ciudad = embarcador.ciudad
                    contacto = embarcador.contactos
                else:
                    pais = None
                    ciudad = None
                    contacto = None


                texto += str(row.embarcador)+',<br>'
                texto += str(ciudad)+','+str(pais)+'<br>'
                texto += 'Contactos: '+str(contacto)+'<br><br>'

                texto+='<p> Dear colleagues: </p>'
                texto+='<p> Please find bellow coordination details for a shipment to '+row.destino_text+'</p><br>'
                texto+='<p>CARGO DETAILS</p><br><br>'


                if isinstance(row.etd,datetime.datetime):
                    salida = str(row.etd.strftime("%d/%m/%Y"))
                else:
                    salida = ''
                if isinstance(row.eta,datetime.datetime):
                    llegada = str(row.eta.strftime("%d/%m/%Y"))
                else:
                    llegada = ''

                carga = Cargaaerea.objects.get(numero=row.numero)
                if carga:
                    producto = carga.producto
                    bultos = carga.bultos
                    peso=carga.bruto
                    volumen=carga.cbm
                else:
                    producto = None
                    bultos = None
                    peso = None
                    volumen = None

                campos = [
                    ("Internal Reference", row.numero),
                    ("Delivery date", llegada if llegada is not None else ""),
                    ("Port of Loading", str(row.loading) if row.loading is not None else ""),
                    ("Port of Discharge", str(row.discharge) if row.discharge is not None else ""),
                    ("Payment Condition", str(row.pago) if row.pago is not None else ""),
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
                texto += ('  - Container number, seal(s) number(s), quantity of pieces, kind od units (packages, pieces, crates, tec), <br>'
                          ' weight, volume (LCL), port of loading, port of discharge, and description of goods, HS tariff Code/NCM number, <br>'
                          '(first four digits are mandatory), <br>')
                texto+=('  -Information on both documents must match. Any discrepancies between MBL/HBL are likely to incur fines and shipment blocked <br>'
                        'by Uruguayan Customs. <br> ')
                texto+='  -Telex Release / Express Release / Seawaybill wil generate extra issuing charges at destination depending on Shipping Line. <br>'
                texto+='  -Consignee on MBL/HBL must include detailed information: <br>'
                texto+=('  -Full name, address, phone number, contact person or e-mail address, Tax ID (RUT) or passport number if consignee <br>'
                        'is an individual. <br>')
                texto += ('  -Pre-alert notice must be sent at least 5 days before vessel arrival. This will allow sufficient time for eventual br>'
                          'amendments as needed and prevent additional fees from the steamship line. <br><br>')

                texto+='OCEANLINK'
            elif title == 'Orden de facturacion':

                resultado['asunto'] = 'ORDEN DE FACTURACION: - seguimiento: ' + str(
                    row.numero)

                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                fecha_actual = datetime.datetime.now()
                fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()
                if isinstance(row.eta, datetime.datetime):
                    llegada = str(row.eta.strftime("%d/%m/%Y"))
                else:
                    llegada = ''
                texto = fecha_formateada + "<br><br>"
                texto += f"<p>ORDEN DE FACTURACIÓN SEGUIMIENTO: {row.numero}</p><br>"
                texto += f"<p>POSICIÓN: {row.posicion}</p><br>"
                texto += f"<p>MASTER: {row.awb}</p><br>"
                texto += f"<p>ETA {llegada} </p><br>"
                texto += f"<p>CLIENTE: {row.cliente}</p><br>"
                texto += 'OCEANLINK'
            elif title == 'Instruccion de embarque':
                embarcador = Clientes.objects.get(codigo=row.embarcador_codigo)
                if row.modo !='IMPORT AEREO' and row.modo !='EXPORT AEREO':
                    row3=Envases.objects.filter(numero=row.numero)

                if embarcador:
                    direccion = embarcador.direccion
                    empresa = embarcador.empresa
                    ciudad = embarcador.ciudad
                    pais = embarcador.pais
                else:
                    direccion=''
                    empresa =''
                    ciudad = ''
                    pais = ''

                if row.consignatario_codigo is not None:
                    consignatario = Clientes.objects.get(codigo=row.consignatario_codigo)
                else:
                    consignatario = None
                if row.cliente is not None:
                    cliente = Clientes.objects.get(codigo=row.cliente_codigo)
                else:
                    cliente = None

                if row.agente_codigo:
                    agente = Clientes.objects.get(codigo=row.agente_codigo)
                else:
                    agente = None

                mercaderia = Cargaaerea.objects.filter(numero=row.numero)
                #moneda = Monedas.objects.get(codigo=row.moneda)
                moneda = row.moneda

                resultado['asunto'] = 'INSTRUCCIÓN DE EMBARQUE - Ref.: ' + str(row.numero) + ' - Shipper: ' + str(
                    embarcador.empresa) + ' - Consignee: ' + str(consignatario.empresa)

                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                fecha_actual = datetime.datetime.now()
                fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()
                if isinstance(row.eta, datetime.datetime):
                    llegada = str(row.eta.strftime("%d/%m/%Y"))
                else:
                    llegada = ''

                tabla_html = "<table style='width:40%'>"
                tabla_html += f"<tr><th align='left'>Fecha: </th><td>{fecha_formateada}</td></tr>"
                tabla_html += f"<tr><th align='left'>A: </th><td>{str(agente.empresa) if agente is not None else ''}</td></tr>"
                tabla_html += f"<tr><th align='left'>Departamento: </th><td>MARITIMO</td></tr>"
                tabla_html += f"<tr><th align='left'>Envíado: </th><td>...</td></tr>"
                tabla_html += "</table><br>"
                tabla_html += "<p>Estimados Seres.:</p><br>"
                tabla_html += "<p>Por favor, contactar a la siguiente compañía para coordinar la operación referenciada:</p><br>"
                tabla_html += "<table style='width:40%'>"
                tabla_html += f"<tr><th align='left'>Proveedor: </th><td>{str(empresa)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Dirección: </th><td>{str(direccion)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Ciudad: </th><td>{str(ciudad)}</td></tr>"
                tabla_html += f"<tr><th align='left'>País: </th><td>{str(pais)}</td></tr><br><br>"
                tabla_html += f"<tr><th align='left'>Consignatario: </th><td>{str(consignatario.empresa)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Dirección: </th><td>{str(consignatario.direccion)}</td></tr>"
                tabla_html += f"<tr><th align='left'>País: </th><td>{str(consignatario.pais)}</td></tr>"
                tabla_html += f"<tr><th align='left'>RUC: </th><td>{str(consignatario.ruc)}</td></tr><br><br>"
                tabla_html += f"<tr><th align='left'>Referencia interna: </th><td>{row.numero}/{row.numero}</td></tr>"
                tabla_html += f"<tr><th align='left'>Posición: </th><td>{str(row.posicion)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Recepcion estimada de mercaderia </th><td>{str(llegada)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Puerto de carga: </th><td>{str(row.loading)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Puerto de descarga: </th><td>{str(row.discharge)}</td></tr>"
                tabla_html += "</table><br>"

                for m in mercaderia:
                    tabla_html += "<table style='width:40%'>"
                    tabla_html += f"<tr><th align='left'>Mercaderia: </th><td>{m.producto}</td></tr>"
                    tabla_html += f"<tr><th align='left'>Bultos: </th><td>{m.bultos}</td></tr>"
                    tabla_html += f"<tr><th align='left'>Kilos: </th><td>{m.bruto}</td></tr>"
                    tabla_html += f"<tr><th align='left'>Volúmen: </th><td>{m.cbm}</td></tr>"
                envase_text = ''
                if row.modo != 'IMPORT AEREO' and row.modo != 'EXPORT AEREO':
                    if row3:
                        for e in row3:
                            cantidad = e.cantidad if e.cantidad is not None else 0
                            tipo = e.tipo if e.tipo is not None else 'S/I'
                            unidad = e.unidad if e.unidad is not None else 'S/I'
                            nrocontenedor = e.nrocontenedor if e.nrocontenedor is not None else 'S/I'
                            envase_text += str(cantidad) + 'x' + str(unidad) + ' ' + str(tipo) + ': ' + str(nrocontenedor)
                            if len(row3) > 1:
                                envase_text += '<br>'

                condicion_pago = "Collect" if row.pago == "C" else "Prepaid" if row.pago == "P" else ""
                tabla_html += f"<tr><th align='left'>Condiciones de pago: </th><td>{condicion_pago}</td></tr>"
                tabla_html += f"<tr><th align='left'>Términos de compra: </th><td>{row.terminos}</td></tr>"
                tabla_html += f"<tr><th align='left'>Envase: </th><td>{envase_text}</td></tr>"
                tabla_html += f"<tr><th align='left'>Modo de Embarque: </th><td>MARITIMO</td></tr>"
                tabla_html += f"<tr><th align='left'>Moneda: </th><td>{moneda}</td></tr>"
                tabla_html += "</table><br>"
                texto = tabla_html

            texto += "<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>SALUDOS,</p>"
            texto += "<b><p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>OCEANLINK,</p></b>"
            texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>DEPARTAMENTO DE {tipos_operativa[row.modo]},</p>"
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


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data).decode("utf-8")
        return base64_data