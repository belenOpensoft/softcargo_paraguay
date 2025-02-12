import datetime
import json
import locale

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.http import HttpResponse
import base64

from cargosystem import settings
from mantenimientos.models import Clientes
from mantenimientos.views.bancos import is_ajax
from seguimientos.models import VGrillaSeguimientos, Envases, Cargaaerea


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
            row_number = request.POST['row_number']
            row = VGrillaSeguimientos.objects.get(numero=row_number)

            texto = ''
            # image_path = str(settings.BASE_DIR) +  "/cargosystem/static/images/oceanlink.png"  # Cambia esto a la ruta de tu imagen
            # base64_string = image_to_base64(image_path)
            # texto += f'<img src="data:image/jpeg;base64,{base64_string}" alt="Imagen Base64">' + '<br><br><br><br>'
            texto += f'<br>'
            if row.modo == 'IMPORT MARITIMO':
                email_cliente = row.emailim
            elif row.modo == 'EXPORT MARITIMO':
                email_cliente = row.emailem
            elif row.modo == 'IMPORT AEREO':
                email_cliente = row.emailia
            elif row.modo == 'EXPORT AEREO':
                email_cliente = row.emailea
            elif row.modo == 'IMPORT TERRESTRE':
                email_cliente = row.emailit
            elif row.modo == 'EXPORT TERRESTRE':
                email_cliente = row.emailet
            if title == 'Traspaso a operaciones':
                texto += 'SEGUIMIENTO: ' + str(row.numero) + '<br>'
                texto += 'CLIENTE: ' + str(row.cliente) + '<br>'
                texto += 'BL: ' + str(row.awb) + '<br>'
                texto += 'HBL: ' + str(row.hawb) + '<br><br><br>'
                texto += 'EMBARQUE TRASPASADO A DEPARTAMENTO DE OPERACIONES <br><br>'
                # Obtener la fecha actual
                fecha_actual = datetime.datetime.now()
                # Formatear la fecha en español
                fecha_formateada = fecha_actual.strftime(f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y')
                texto += 'FECHA: ' + fecha_formateada.capitalize() + '<br><br>'
                texto += 'CONDICION MBL: <br>'
                texto += 'CONDICION HBL: <br>'
                texto += 'COURRIER CON DOCUMENTOS ENVIADO: <br>'
                texto += 'COURRIER/GUIA: <br><br><br><br>'
                texto += 'SALUDOS, <br><br>'
                texto += '<b>OCEANLINK,</b> <br>'
                texto += 'DEPARTAMENTO DE ' + str(tipos_operativa[row.modo]) + ', <br>'
                texto += str(request.user.first_name) + ' ' + str(request.user.last_name) + ' <br>'
                texto += 'OPERACIONES <br>'
                texto += 'PH: 59829170501 <br>'
                resultado['asunto'] = 'SEGUIMIENTO ' + str(row.numero) + ' // TRASPASO A OPERACIONES'
            elif title == 'Aviso de embarque':
                tabla_html = "<table style='width:40%'>"
                # Definir los campos y sus respectivos valores
                resultado['asunto'] = 'AVISO DE EMBARQUE / CS: ' + str(row.numero) + ' ' \
                                          '- HB/l: ' + str(row.hawb) + ' - Shipper: ' + str(row.embarcador) + ' - Consig: ' \
                                      '' + str(row.consignatario) + '; Vapor: ' + str(row.vapor)
                fecha_actual = datetime.datetime.now()
                fecha_formateada = fecha_actual.strftime(
                    f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y')
                texto += fecha_formateada.capitalize() + '<br><br>'
                texto += 'Sres.: <br>'
                texto += str(row.cliente) + '<br>'
                texto += '<b>DEPARTAMENTO DE COMERCIO EXTERIOR </b><br><br>'
                if isinstance(row.etd,datetime.datetime):
                    salida = str(row.etd.strftime("%d/%m/%Y"))
                else:
                    salida = ''
                if isinstance(row.eta,datetime.datetime):
                    llegada = str(row.eta.strftime("%d/%m/%Y"))
                else:
                    llegada = ''
                campos = [
                    ("Referencia", ""),
                    ("Embarcador", str(row.embarcador) if row.embarcador is not None else ""),
                    ("Consignatario", str(row.consignatario) if row.consignatario is not None else ""),
                    ("Ref.Proveedor", str(row.refproveedor) if row.refproveedor is not None else ""),
                    ("Términos", str(row.terminos) if row.terminos is not None else ""),
                    ("Transportista", str(row.transportista) if row.transportista is not None else ""),
                    ("Vapor", str(row.vapor) if row.vapor is not None else ""),
                    ("Origen", str(row.origen_text) if row.origen_text is not None else ""),
                    ("Destino", str(row.destino_text) if row.destino_text is not None else ""),
                    #("Destino", str(row.destino_text)),
                    ("Salida", str(salida) if salida is not None else ""),
                    ("Llegada", str(llegada) if llegada is not None else ""),
                    ("Llegada estimadas", str(llegada) if llegada is not None else ""),
                    ("Posicion", str(row.posicion) if row.posicion is not None else ""),
                    ("Agente", str(row.agente) if row.agente is not None else ""),
                    ("H B/L", str(row.hawb) if row.hawb is not None else ""),
                    ("B/L", str(row.awb) if row.awb is not None else ""),
                    ("Seguimiento", str(row.numero) if row.numero is not None else ""),
                ]
                # Agregar campos a la tabla
                for campo, valor in campos:
                    tabla_html += f"<tr><th>{campo}</th><td>{valor}</td></tr>"
                # Agregar más filas con los otros detalles, como Contenedores
                cantidad_cntr = ""
                contenedores = ""
                mercaderias = ""
                precintos = ""
                bultos = 0
                peso = 0
                volumen = 0
                # Obtener datos de los contenedores y calcular los valores
                cant_cntr = Envases.objects.filter(numero=row.numero).values('tipo', 'nrocontenedor', 'precinto',
                                                                             'bultos', 'peso','envase','volumen').annotate(
                    total=Count('id'))
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
                        mercaderias += cn['envase'] + ' - '
                tabla_html += f"<tr><th>Contenedores</th><td>{cantidad_cntr[:-3]}</td></tr>"
                tabla_html += f"<tr><th>Nro.Contenedor/es</th><td>{contenedores[:-3]}</td></tr>"
                tabla_html += f"<tr><th>Precintos/sellos</th><td>{precintos[:-3]}</td></tr>"
                tabla_html += f"<tr><th>Peso</th><td>{peso} KGS</td></tr>"
                tabla_html += f"<tr><th>Bultos</th><td>{bultos}</td></tr>"
                tabla_html += f"<tr><th>CBM</th><td>{volumen} M³</td></tr>"
                tabla_html += f"<tr><th>Mercaderia</th><td>" + str(mercaderias)[:-3] + "</td></tr>"
                # Agregar más campos de contenedores aquí

                # Cerrar la etiqueta de la tabla
                tabla_html += "</table><br><br>"
                texto += tabla_html
                texto += 'Detalle de gastos <br><br>'
                texto += 'Los buques y las fechas pueden variar sin previo aviso y son siempre a confirmar. <br>' \
                         'Agradeciendo vuestra preferencia, le saludamos muy atentamente.<br><br>'
                texto += '<b>OCEANLINK,</b><br>'
                texto += str(request.user.first_name) + ' ' + str(request.user.last_name) + ' <br>'
                texto += 'DEPARTAMENTO DE ' + str(tipos_operativa[row.modo]) + ', <br>'
                texto += 'Bolonia 2280 LATU, Edificio Los Álamos, Of.103 <br>'
                texto += 'OPERACIONES <br>'
                texto += 'EMAIL: <br>'
                texto += 'TEL: 598 2917 0501 <br>'
                texto += 'FAX: 598 2916 8215 <br><br><br><br>'

            elif title == 'Notificacion llegada de carga':
                # cantidad_cntr = ''
                # contenedores = ''
                # precintos = ''
                # movimiento = ''
                # mercaderias = ''
                # bultos = 0
                # peso = 0
                fecha_actual = datetime.datetime.now()
                resultado['asunto'] = 'NOTIFICACION DE LLEGADA DE CARGA - Ref.: ' + str(row.refproveedor) + ' - CS: ' + str(row.numero) + \
                                      '- HB/l: ' + str(row.hawb) + ' - Ship: ' + str(row.embarcador) + ' - Consig: ' \
                                                                                                       '' + str(row.consignatario) + '; Vapor: ' + str(row.vapor)
                # # TEXTO DE CUERPO DEL MENSAJE
                fecha_formateada = fecha_actual.strftime(f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y')
                texto += fecha_formateada.capitalize().upper() + '<br><br>'
                tabla_html = "<table style='width:40%'>"
                campos = [
                    ("Att.", ""),
                    ("Cliente", str(row.cliente)),
                    ("Vapor", str(row.vapor) if row.vapor is not None else ""),
                    ("Viaje", str(row.viaje) if row.viaje is not None else ""),
                    ("Embarque", str(row.etd.strftime("%d/%m/%Y")) if isinstance(row.etd, datetime.datetime) else ""),
                    ("Llegada", str(row.eta.strftime("%d/%m/%Y")) if isinstance(row.eta, datetime.datetime) else ""),
                ]
                for campo, valor in campos:
                    tabla_html += f"<tr><th align='left'>{campo}</th><td>{valor}</td></tr>"
                tabla_html += f"<tr><th align='left'>Origen</th><td>{str(row.origen_text)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Loading</th><td>{str(row.loading)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Discharge</th><td>{str(row.discharge)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Destino</th><td>{str(row.destino_text)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Transportista</th><td>{str(row.transportista)}</td></tr>"
                tabla_html += f"<tr><th align='left'>B/L</th><td>{str(row.awb)}</td></tr>"
                tabla_html += f"<tr><th align='left'>H B/L</th><td>{str(row.hawb)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Referencia</th><td>{str(row.refproveedor)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Posicion</th><td>{str(row.posicion)}</td></tr>"
                tabla_html += f"<tr><th align='left'>Seguimiento</th><td>{str(row.numero)}</td></tr>"
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
                tabla_html += f"<tr><th align='left'>Movimiento</th><td>{movimiento[:-3]}</td></tr>"
                tabla_html += f"<tr><th align='left'>Mercaderia</th><td>{mercaderias[:-3]}</td></tr>"
                tabla_html += f"<tr><th align='left'>Bultos</th><td>{bultos}</td></tr>"
                tabla_html += f"<tr><th align='left'>Peso</th><td>{peso} KGS</td></tr>"
                tabla_html += f"<tr><th align='left'>CBM</th><td>{volumen} M³</td></tr>"
                tabla_html += "</table><br><br>"
                texto += tabla_html

                texto += '<b>Detalle de gastos  en Dólares</b><br><br>'
                texto += 'Los buques y las fechas pueden variar sin previo aviso y son siempre a confirmar. <br>' \
                         'Agradeciendo vuestra preferencia, le saludamos muy atentamente.<br><br>'
                texto += '<b>OCEANLINK,</b><br>'
                texto += str(request.user.first_name) + ' ' + str(request.user.last_name) + ' <br>'
                texto += 'DEPARTAMENTO DE ' + str(tipos_operativa[row.modo]) + ', <br>'
                texto += 'Bolonia 2280 LATU, Edificio Los Álamos, Of.103 <br>'
                texto += 'OPERACIONES <br>'
                texto += 'EMAIL: <br>'
                texto += 'TEL: 598 2917 0501 <br>'
                texto += 'FAX: 598 2916 8215 <br><br><br><br>'
                texto += '</table>'
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
                texto += 'TEL: 598 2917 0501 <br>'
                texto += 'FAX: 598 2916 8215 <br><br><br><br>'
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



def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data).decode("utf-8")
        return base64_data