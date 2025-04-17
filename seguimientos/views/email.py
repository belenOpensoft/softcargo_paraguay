import datetime
import json
import locale

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.http import HttpResponse
import base64

from reportlab.lib.validators import isNumber

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
            directo_boolean = request.POST['directo']
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
                if row.modo=='IMPORT MARITIMO' or row.modo == 'EXPORT MARITIMO':
                    if str(row.vapor).isdigit():
                        vapor = Vapores.objects.get(codigo=row.vapor).nombre

                    else:
                        vapor = row.vapor
                else:
                    vapor='S/I'
                resultado[
                    'asunto'] = f'AVISO DE EMBARQUE / Ref: {row.numero} - HB/l: {row.hawb} - Shipper: {row.embarcador} - Consig: {row.consignatario}; Vapor: {vapor}'

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

                texto += formatear_linea("Proveedor", row.embarcador or "")

                texto += formatear_linea("Consignatario", row.consignatario or "")

                texto += formatear_linea("Orden Cliente", row.refcliente or "")

                texto += formatear_linea("Ref. Proveedor", row.refproveedor or "")

                texto += formatear_linea("Términos Compra", row.terminos or "")



                texto += formatear_linea("Vuelo", vapor or "") if row.modo=='IMPORT AEREO' or row.modo == 'EXPORT AEREO' else formatear_linea("Vapor", vapor or "")

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
                tipo = ''

                volumen = 0
                gastos = Serviceaereo.objects.filter(numero=row.numero)

                cant_cntr = Envases.objects.filter(numero=row.numero).values('tipo', 'nrocontenedor', 'precinto',
                                                                             'bultos', 'peso', 'unidad',
                                                                             'volumen').annotate(total=Count('id'))

                carga = Cargaaerea.objects.filter(numero=row.numero).values('producto__nombre')

                if cant_cntr.count() > 0:

                    for cn in cant_cntr:

                        cantidad_cntr += f'{cn["total"]} x {cn["unidad"]} - {cn["tipo"]} - '

                        contenedores += f'{cn["nrocontenedor"]} - '

                        if cn['precinto']:
                            precintos += f'{cn["precinto"]} - '

                        bultos += cn['bultos'] if cn['bultos'] else 0
                        tipo= cn["tipo"]
                        peso += cn['peso'] or 0

                        volumen += cn['volumen'] or 0

                if carga.count() > 0:

                    for c in carga:
                        mercaderias += c['producto__nombre'] + ' - '

                texto += formatear_linea("Contenedores", cantidad_cntr[:-3])

                texto += formatear_linea("Nro. Contenedor/es", contenedores[:-3])

                texto += formatear_linea("Precintos/Sellos", precintos[:-3])

                texto += formatear_linea("HBL", row.hawb or "") if row.modo  == 'IMPORT MARITIMO' or row.modo == 'EXPORT MARITIMO' else formatear_linea("HAWB", row.hawb or "")

                if master == 'true':
                    if row.modo in ['IMPORT MARITIMO', 'EXPORT MARITIMO']:
                        texto += formatear_linea("MBL", row.awb or "")
                    elif row.modo in ['IMPORT AEREO', 'EXPORT AEREO']:
                        texto += formatear_linea("AWB", row.hawb or "")
                    else:
                        texto += formatear_linea("CRT", row.hawb or "")

                if transportista == 'true':
                    texto += formatear_linea("Transportista", row.transportista or "")

                if row.modo in ['IMPORT AEREO','EXPORT AEREO']:
                    conex = Conexaerea.objects.filter(numero=row.numero)
                    if conex:
                        for i, ruta in enumerate(conex):
                            if ruta.llegada:
                                fecha = ruta.llegada.strftime("%d/%m")
                            else:
                                fecha = '??/??'
                            tramo = f"({ruta.origen}/{ruta.destino})  {ruta.cia}{ruta.viaje}/{fecha}" if transportista == 'true' else f"({ruta.origen}/{ruta.destino}) {ruta.viaje}/{fecha}"
                            texto += formatear_linea("Vuelo", tramo)

                texto += formatear_linea("Peso", f"{peso} KGS")

                texto += formatear_linea("Bultos", str(bultos)+' '+str(tipo))

                texto += formatear_linea("CBM", f"{volumen} M³")

                texto += "<br>"

                texto += formatear_linea("Mercadería", mercaderias[:-3])

                texto += formatear_linea("Depósito", row.deposito or "")

                texto += formatear_linea("Doc. Originales", 'SI' if row.originales else 'NO')

                texto += "<br>"
                if gastos_boolean == 'true':

                    if gastos:

                        texto += '<p style="font-family: Courier New, monospace; font-size: 12px; line-height: 1;"> Detalle de gastos en Dólares U.S.A </p>'

                        total_gastos = 0

                        total_iva = 0

                        for g in gastos:

                            #codigo = g.servicio.split(" - ")[0]
                            codigo = int(g.servicio) if isNumber(g.servicio) else None
                            if codigo is None:
                                raise TypeError('No se encontró el código del servicio')
                            servicio = Servicios.objects.get(codigo=codigo)

                            if servicio is not None:

                                if g.precio != 0 and g.precio is not None:
                                    total_gastos += float(g.precio)
                                elif g.costo is not None and g.costo != 0:
                                    total_gastos += float(g.costo)
                                else:
                                    total_gastos += 0

                                iva = True if servicio.tasa == 'B' else False

                                if iva:
                                    if g.precio is not None:
                                        total_iva += float(g.precio) * 0.22
                                    elif g.costo is not None:
                                        total_iva += float(g.costo) * 0.22
                                    else:
                                        total_iva += 0

                                if g.precio is not None:
                                    texto += formatear_linea(servicio.nombre, f"{g.precio:.2f}", 1)
                                elif g.costo is not None:
                                    texto += formatear_linea(servicio.nombre, f"{g.costo:.2f}", 1)
                                else:
                                    texto += formatear_linea("Problema con los gastos cargados", 0)

                        texto += "<br>"

                        texto += formatear_linea("TOTAL DE GASTOS", f"{total_gastos:.2f}", 1)

                        texto += formatear_linea("I.V.A", f"{total_iva:.2f}", 1)

                        texto += formatear_linea("TOTAL A PAGAR", f"{total_gastos + total_iva:.2f}", 1)

                        texto += "<br>"

                texto += "<table style='border: none; font-family: Courier New, monospace; font-size: 12px; border-collapse: collapse; width: 100%;'>"

                # Fila de títulos (encabezados)
                texto += "<tr>"
                texto += "<th style='padding: 2px 10px; text-align: left;'>Origen</th>"
                texto += "<th style='padding: 2px 10px; text-align: left;'>Destino</th>"
                texto += "<th style='padding: 2px 10px; text-align: left;'>Vapor/Vuelo</th>"
                texto += "<th style='padding: 2px 10px; text-align: left;'>Viaje</th>"
                texto += "<th style='padding: 2px 10px; text-align: left;'>Salida</th>"
                texto += "<th style='padding: 2px 10px; text-align: left;'>Llegada</th>"
                texto += "</tr>"

                # Fila de valores

                texto += "<tr>"
                texto += f"<td style='padding: 2px 10px;'>{row.origen_text or ''}</td>"
                texto += f"<td style='padding: 2px 10px;'>{row.destino_text or ''}</td>"
                texto += f"<td style='padding: 2px 10px;'>{str(vapor) }</td>"
                texto += f"<td style='padding: 2px 10px;'>{str(row.viaje) or ''}</td>"
                texto += f"<td style='padding: 2px 10px;'>{salida}</td>"
                texto += f"<td style='padding: 2px 10px;'>{llegada}</td>"
                texto += "</tr>"

                texto += "</table><br>"

                texto += "<pre style='font-family: Courier New, monospace; font-size: 12px;'>"

                texto += "Los buques, vuelos y las llegadas al puerto de Montevideo son siempre a CONFIRMAR, ya que puede haber trasbordos y/o alteraciones en las fechas estimadas de llegada\n"
                texto+="sin previo aviso, por lo cual le sugerimos consultarnos por la fecha de arribo que aparece en este aviso.\n"
                texto += "Agradeciendo vuestra preferencia, le saludamos muy atentamente."
                texto += "</pre>"
            elif title == 'Notificacion llegada de carga':

                consigna = Clientes.objects.get(codigo=row.consignatario_codigo)

                conex = Conexaerea.objects.filter(numero=row.numero)

                carga = Cargaaerea.objects.filter(numero=row.numero)

                gastos = Serviceaereo.objects.filter(numero=row.numero)

                if row.modo in ['IMPORT AEREO','EXPORT AEREO']:
                    vapor = conex[0].vapor if conex and conex[0].vapor else 'S/I'
                else:
                    if row.vapor is not None and row.vapor.isdigit():
                        vapor = Vapores.objects.get(codigo=row.vapor).nombre
                    elif row.vapor is not None:
                        vapor = row.vapor
                    else:
                        vapor = 'S/I'
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
                salida = row.etd.strftime("%d/%m/%Y") if isinstance(row.etd, datetime.datetime) else ''

                llegada = row.eta.strftime("%d/%m/%Y") if isinstance(row.eta, datetime.datetime) else ''

                texto += formatear_linea("Salida", salida )

                texto += formatear_linea("Llegada",llegada)

                texto += formatear_linea("Origen", row.origen if conex else "")

                texto += formatear_linea("Destino", row.destino if conex else "")
                texto += formatear_linea("Vapor", vapor) if row.modo in ['IMPORT MARITIMO','EXPORT MARITIMO'] else formatear_linea("Vuelo", vapor)

                texto += formatear_linea("HAWB", row.hawb) if row.modo in ['IMPORT AEREO','EXPORT AEREO'] else  formatear_linea("HBL", row.hawb)

                if master == 'true':
                    texto += formatear_linea("AWB", row.awb) if row.modo in ['IMPORT AEREO','EXPORT AEREO'] else formatear_linea("MBL", row.awb)

                texto += formatear_linea("Referencia", row.embarque)

                texto += formatear_linea("Posición", row.posicion)

                texto += formatear_linea("Seguimiento", row.numero)

                if row.modo in ['IMPORT AEREO', 'EXPORT AEREO']:
                    if conex:
                        for i, ruta in enumerate(conex):
                            if ruta.llegada:
                                fecha = ruta.llegada.strftime("%d/%m")
                            else:
                                fecha = '??/??'
                            tramo = f"({ruta.origen}/{ruta.destino})  {ruta.cia}{ruta.viaje}/{fecha}"
                            texto += formatear_linea("Vuelo", tramo)

                texto += formatear_linea("Embarcador", row.embarcador)

                texto += formatear_linea("Ref. Proveedor", row.refproveedor)

                if row.modo not in ['IMPORT AEREO','EXPORT AEREO']:
                    cant_cntr = Envases.objects.filter(numero=row.numero).values(

                        'tipo', 'nrocontenedor', 'precinto', 'bultos', 'peso', 'unidad', 'volumen','movimiento'

                    ).annotate(total=Count('id'))

                    cantidad_cntr = contenedores = precintos = movimiento= ''
                    peso = volumen = bultos = 0
                    if cant_cntr.exists():

                        for cn in cant_cntr:

                            cantidad_cntr += f'{cn["total"]} x {cn["unidad"]} - {cn["tipo"]} - '

                            contenedores += f'{cn["nrocontenedor"]} - '

                            if cn['precinto']:
                                precintos += f'{cn["precinto"]} - '

                            bultos += cn['bultos'] if cn['bultos'] else 0
                            peso += cn['peso'] if cn['peso'] else 0
                            volumen += cn['volumen'] if cn['volumen'] else 0
                            movimiento= cn['movimiento']

                    texto += formatear_linea("Movimiento", movimiento)
                    texto += formatear_linea("Contenedores", cantidad_cntr.rstrip(' -'))

                    texto += formatear_linea("Nro. Contenedor/es", contenedores.rstrip(' -'))

                    texto += formatear_linea("Precintos/Sellos", precintos.rstrip(' -'))


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

                        texto += '<p style="font-family: Courier New, monospace; font-size: 12px; line-height: 1;"> Detalle de gastos en Dólares U.S.A </p>'

                        total_gastos = 0

                        total_iva = 0

                        for g in gastos:

                            servicio = Servicios.objects.get(codigo=g.servicio)

                            total_gastos += float(g.precio) if g.precio !=0 else float(g.costo)

                            iva = True if servicio.tasa == 'B' else False

                            if iva:
                                total_iva += float(g.precio) * 0.22 if g.precio !=0 else float(g.costo) * 0.22

                            if g.precio != 0:
                                texto += formatear_linea(servicio.nombre, f"{g.precio:.2f}",1)
                            elif g.costo !=0:
                                texto += formatear_linea(servicio.nombre, f"{g.costo:.2f}",1)
                            else:
                                texto += formatear_linea("Problema con los gastos cargados",0)


                        texto += "<br>"

                        texto += formatear_linea("TOTAL DE GASTOS", f"{total_gastos:.2f}",1)

                        texto += formatear_linea("I.V.A", f"{total_iva:.2f}",1)

                        texto += formatear_linea("TOTAL A PAGAR", f"{total_gastos + total_iva:.2f}",1)

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

                fecha_actual = datetime.datetime.now()

                fecha_formateada = fecha_actual.strftime(
                    f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y')

                resultado['asunto'] = (

                    f'AVISO DE DESCONSOLIDACION - Ref.: {row.numero} - CS: {row.embarque} - HB/l: {row.hawb} - Ship: {row.embarcador}'

                )

                texto += formatear_linea("Fecha", fecha_formateada.upper())

                texto += "<br>"
                texto += formatear_linea("Cliente", str(row.cliente))

                texto += formatear_linea("Dirección", row.direccion_cliente or "")

                texto += formatear_linea("Teléfono", row.telefono_cliente or "")

                texto += formatear_linea("Att.", "DEPARTAMENTO DE OPERACIONES")


                if row.modo == 'IMPORT MARITIMO' or row.modo == 'EXPORT MARITIMO':
                    if row.vapor is not None and row.vapor.isdigit():
                        vapor = Vapores.objects.get(codigo=row.vapor).nombre
                    elif row.vapor is not None:
                        vapor = row.vapor
                    else:
                        vapor = 'S/I'
                else:
                    vapor = row.vapor

                texto += formatear_linea("Vapor", vapor or "") #cambiar esto
                texto += formatear_linea("HBL",
                                         row.hawb or "") if row.modo == 'IMPORT MARITIMO' or row.modo == 'EXPORT MARITIMO' else formatear_linea(
                    "HAWB", row.hawb or "")

                if isinstance(row.eta, datetime.datetime):
                    texto += formatear_linea("Llegada", row.eta.strftime("%d/%m/%Y"))

                texto += formatear_linea("Referencia", row.numero or "")
                texto += formatear_linea("Posición", row.posicion or "")

                texto += formatear_linea("Seguimiento", row.numero)

                texto += formatear_linea("Embarcador", row.embarcador)

                texto += formatear_linea("Consignatario", row.consignatario)
                texto += formatear_linea("Origen", row.origen)
                texto += formatear_linea("Destino", row.destino)

                texto += formatear_linea("Orden cliente", row.refcliente)

                texto += formatear_linea("Referencia proveedor", row.refproveedor)

                if row.modo not in ['IMPORT AEREO','EXPORT AEREO']:
                    # Datos de contenedores
                    cantidad_cntr = ""
                    contenedores = ""
                    precintos = ""
                    movimiento = ""
                    mercaderias = Cargaaerea.objects.filter(numero=row.numero).values('producto__nombre')
                    bultos = 0
                    peso = 0
                    volumen = 0
                    cant_cntr = Envases.objects.filter(numero=row.numero).values(
                        'tipo', 'nrocontenedor', 'precinto', 'bultos',
                        'peso', 'envase', 'movimiento', 'volumen'
                    ).annotate(total=Count('id'))
                    if cant_cntr.count() > 0:
                        for cn in cant_cntr:
                            cantidad_cntr += f' {cn["total"]} x {cn["tipo"]} - '
                            contenedores += f' {cn["nrocontenedor"]} - '
                            if cn['precinto']:
                                precintos += f'{cn["precinto"]} - '
                            bultos += cn['bultos'] if cn['bultos'] else 0
                            if cn['peso']:
                                peso += cn['peso']
                            if cn['volumen']:
                                volumen += cn['volumen']
                            movimiento += f'{cn["movimiento"]} - '

                    mercaderia = ''
                    if mercaderias:
                        for m in mercaderias:
                            mercaderia += str(m['producto__nombre'])+'-'

                    texto += formatear_linea("Contenedores", cantidad_cntr.strip(' -'))
                    texto += formatear_linea("Nro. Contenedor/es", contenedores.strip(' -'))
                    texto += formatear_linea("Precintos/sellos", precintos.strip(' -'))
                    texto += formatear_linea("Bultos", str(bultos))
                    texto += formatear_linea("Peso", f"{peso} KGS")
                    texto += formatear_linea("CBM", f"{volumen} M³")
                    texto += formatear_linea("Mercadería", mercaderia)
                else:
                    contenedores = ""
                    mercaderia = ""
                    bultos = 0
                    peso = 0
                    volumen = 0
                    cant_cntr = Cargaaerea.objects.filter(numero=row.numero).values(
                        'producto__nombre', 'nrocontenedor', 'bultos',
                        'bruto', 'cbm'
                    ).annotate(total=Count('id'))
                    if cant_cntr.count() > 0:
                        for cn in cant_cntr:
                            contenedores += f' {cn["nrocontenedor"]} - '
                            bultos += cn['bultos'] if cn['bultos'] else 0
                            if cn['bruto']:
                                peso += cn['bruto']
                            if cn['cbm']:
                                volumen += cn['cbm']
                            mercaderia += f'{cn["producto__nombre"]} - '

                    texto += formatear_linea("Nro. Contenedor/es", contenedores.strip(' -'))
                    texto += formatear_linea("Bultos", str(bultos))
                    texto += formatear_linea("Peso", f"{peso} KGS")
                    texto += formatear_linea("CBM", f"{volumen} M³")
                    texto += formatear_linea("Mercadería", mercaderia)
                texto += formatear_linea("Entrega en gate", "")

                texto += formatear_linea("Depósito", str(row.deposito))
                texto += formatear_linea("WR", str(row.wreceipt))

                texto += "<br>"

                texto += "<b>ATENCION!</b><br><br>"

                texto += "DETALLE DE DESCONSOLIDACION<br><br>"
            elif title == 'Cargo release':

                fecha_actual = datetime.datetime.now()

                fecha_formateada = fecha_actual.strftime(
                    f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y')

                resultado['asunto'] = (

                    f'CARGO RELEASE - Seg.: {row.numero} - HB/l: {row.hawb} - Shipper: {row.embarcador} - CNEE: {row.consignatario}'

                )

                texto = ""

                texto += formatear_linea("SEG", row.numero)

                texto += formatear_linea("HBL", row.hawb)

                texto += formatear_linea("DATE", fecha_formateada.upper())

                texto += "<br>"

                texto += "<pre style='font-family: Courier New, monospace; font-size: 12px;'>"

                texto += "PLEASE NOTE THAT WE RELEASED DOCS TO CONSIGNEE.\n"

                texto += "THANK YOU VERY MUCH FOR YOUR ASSISTANCE.\n\n"

                texto += "BEST REGARDS,\n"

                texto += "OCEANLINK\n"

                texto += "</pre>"
            elif title == 'Release documentacion':

                resultado['asunto'] = (

                    f'RELEASE DOCUMENTACION - FCR.: {row.hawb or ""} - SEGUIMIENTO {row.numero or ""}'

                )

                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

                fecha_actual = datetime.datetime.now()

                if str(row.vapor).isdigit():
                    vapor = Vapores.objects.get(codigo=row.vapor).nombre
                else:
                    vapor = row.vapor

                fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

                texto = formatear_linea("Fecha", fecha_formateada)

                texto += "<br>"

                texto += "<pre style='font-family: Courier New, monospace; font-size: 12px;'>"

                texto += "Estimados,\n\n"

                texto += "Informamos a Uds. que se encuentra a vuestra disposición para ser retirada en nuestras oficinas\n"

                texto += "la documentación correspondiente a la liberación del siguiente embarque:\n\n"

                texto += f"{'FCR:':<20} {row.hawb or ''}\n"

                texto += f"{'BUQUE:':<20} {vapor or ''}\n\n"

                texto += "Favor presentar para dicha liberación los FCR correspondientes a este embarque.\n"

                texto += "Nuestro horario para transferencias es de lunes a viernes de 08:30 a 12:00 y de 13:00 a 16:30 hrs.\n\n"

                texto += "</pre>"
            elif title == 'Liberacion':

                resultado['asunto'] = f'LIBERACIÓN: {row.awb} - seguimiento: {row.numero}'

                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

                fecha_actual = datetime.datetime.now()

                fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

                texto = ""

                texto += formatear_linea("Fecha", fecha_formateada)

                texto += "<br>"

                texto += "<pre style='font-family: Courier New, monospace; font-size: 12px;'>"

                texto += f"ESTIMADOS,\n\n"

                texto += f"SOLICITAMOS LA LIBERACIÓN DEL SIGUIENTE BL: {row.awb}\n\n"

                texto += "ADJUNTAMOS:\n"

                texto += f" * BL {row.awb} ENDOSADO\n"

                texto += " * ARRIVAL NOTICE ENDOSADO\n"

                texto += " * CONTRATO DE RESPONSABILIDAD\n"

                texto += " * COMPROBANTE DE PAGO\n\n"

                texto += "SALUDOS,\n\n"

                texto += "OCEANLINK\n"

                texto += "</pre>"
            elif title == 'Notificacion cambio de linea':

                resultado['asunto'] = 'NOTIFICACIÓN CAMBIO DE LÍNEA / NVOCC / CÍA AEREA'

                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

                fecha_actual = datetime.datetime.now()

                fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

                texto = ""

                texto += formatear_linea("Fecha", fecha_formateada)

                texto += "<br>"

                texto += "<pre style='font-family: Courier New, monospace; font-size: 12px;'>"

                texto += f"SEG: {row.numero}\n\n"

                texto += "CONFIRMO CAMBIO DE LÍNEA / NVOCC / CÍA AEREA DE ESTE SEGUIMIENTO\n\n"

                texto += "ANTERIOR:\n"

                texto += f"ACTUAL: {row.transportista}\n\n"

                texto += "OCEANLINK\n"

                texto += "</pre>"
            elif title == 'Orden de facturacion':
                resultado['asunto'] = f'ORDEN DE FACTURACION: - seguimiento: {row.numero}'

                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                fecha_actual = datetime.datetime.now()
                fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

                if isinstance(row.eta, datetime.datetime):
                    llegada = row.eta.strftime("%d/%m/%Y")
                else:
                    llegada = ''

                texto = ""
                texto += formatear_linea("Fecha", fecha_formateada)
                texto += "<br>"

                texto += "<pre style='font-family: Courier New, monospace; font-size: 12px;'>"
                texto += f"ORDEN DE FACTURACIÓN - SEGUIMIENTO: {row.numero}\n\n"
                texto += f"{'Posición:':<15} {row.posicion}\n"
                texto += f"{'Master:':<15} {row.awb}\n"
                texto += f"{'ETA:':<15} {llegada}\n"
                texto += f"{'Cliente:':<15} {row.cliente}\n\n"
                texto += "OCEANLINK\n"
                texto += "</pre>"
            elif title == 'Novedades sobre la carga':

                fecha_actual = datetime.datetime.now()

                resultado['asunto'] = 'NOVEDADES SOBRE LA CARGA - Ref.: ' + str(row.numero) + \
 \
                                      '/ CS: ' + str(row.embarque) if row.embarque else '' + '- Shipper: ' + str(row.embarcador) + \
 \
                                      '; Consignee: ' + str(row.consignatario)

                fecha_formateada = fecha_actual.strftime(

                    f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y'

                )

                texto += fecha_formateada.capitalize().upper() + '<br><br>'

                # Mercaderías

                mercaderia = Cargaaerea.objects.filter(numero=row.numero).values('producto__nombre','bultos','bruto','cbm')
                if mercaderia.exists():
                    for m in mercaderia:
                        texto += formatear_linea(f"Mercadería", str(m['producto__nombre']) if m['producto__nombre'] is not None else "S/I")
                        texto += formatear_linea(f"Bultos", m['bultos'] if m['bultos'] is not None else "S/I")
                        texto += formatear_linea(f"Peso", m['bruto'] if m['bruto'] is not None else "S/I")
                        texto += formatear_linea(f"CBM", round(float(m['cbm']),2) if m['cbm'] is not None else "S/I")

                if row.modo not in ['IMPORT AEREO','EXPORT AEREO']:
                    envases=Envases.objects.filter(numero=row.numero).values('nrocontenedor','precinto')
                    if envases.exists():
                        for e in envases:
                            texto += formatear_linea(f"Nro. Contenedor",
                                                     str(e['nrocontenedor']) if e['nrocontenedor'] is not None else "S/I")
                            texto += formatear_linea(f"Precinto", str(e['precinto']) if e['precinto'] is not None else "S/I")

                # Datos generales

                texto += formatear_linea("Embarque", str(row.embarque) if row.embarque is not None else "S/I")

                texto += formatear_linea("Posición", str(row.posicion) if row.posicion is not None else "S/I")

                texto += formatear_linea("Salida", row.etd.strftime('%Y-%m-%d'))

                texto += formatear_linea("Llegada", row.eta.strftime('%Y-%m-%d'))

                texto += formatear_linea("Origen", str(row.origen) if row.origen is not None else "S/I")

                texto += formatear_linea("Destino", str(row.destino) if row.destino is not None else "S/I")

                if row.modo=='IMPORT MARITIMO' or row.modo == 'EXPORT MARITIMO':
                    if str(row.vapor).isdigit():
                        vapor = Vapores.objects.get(codigo=row.vapor).nombre

                    else:
                        vapor = row.vapor
                else:
                    vapor='S/I'

                texto += formatear_linea("Vapor", str(vapor)) if row.modo in ['IMPORT MARITIMO','EXPORT MARITIMO'] else formatear_linea("Vuelo", str(vapor))

                texto += formatear_linea("H B/L", str(row.hawb) if row.hawb is not None else "S/I") if row.modo in ['IMPORT MARITIMO','EXPORT MARITIMO'] else formatear_linea("HAWB", str(row.hawb) if row.hawb is not None else "S/I")

                texto += formatear_linea("Embarcador", str(row.embarcador) if row.embarcador is not None else "S/I")

                texto += formatear_linea("Consignatario",
                                         str(row.consignatario) if row.consignatario is not None else "S/I")

                texto += "<br>"

            # falta el completo
            elif title == 'Shipping instruction':
                embarcador = Clientes.objects.get(codigo=row.embarcador_codigo)
                if row.modo != 'IMPORT AEREO' and row.modo != 'EXPORT AEREO':
                    row3 = Envases.objects.filter(numero=row.numero)

                direccion = embarcador.direccion if embarcador else ''
                empresa = embarcador.empresa if embarcador else ''
                ciudad = embarcador.ciudad if embarcador else ''
                pais = embarcador.pais if embarcador else ''
                email = embarcador.emailim if embarcador else ''
                contactos = embarcador.contactos if embarcador else ''

                consignatario = Clientes.objects.get(
                    codigo=row.consignatario_codigo) if row.consignatario_codigo else None
                cliente = Clientes.objects.get(codigo=row.cliente_codigo) if row.cliente_codigo else None
                agente = Clientes.objects.get(codigo=row.agente_codigo) if row.agente_codigo else None

                mercaderia = Cargaaerea.objects.filter(numero=row.numero)
                moneda = Monedas.objects.get(codigo=row.moneda)
                moneda_nombre = moneda.nombre if moneda else 'N/A'

                resultado[
                    'asunto'] = f"SHIPPING INSTRUCTION - Ref.: {row.numero} - Shipper: {empresa} - Consignee: {consignatario.empresa if consignatario else ''}"

                locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
                fecha_actual = datetime.datetime.now()
                fecha_formateada = fecha_actual.strftime('%A, %B %d, %Y').upper()
                llegada = row.eta.strftime("%d/%m/%Y") if isinstance(row.eta, datetime.datetime) else ''
                nombre = str(request.user.first_name) + ' ' + str(request.user.last_name)
                texto = ''
                texto += formatear_linea("Date", fecha_formateada)
                texto += formatear_linea("To", agente.empresa if agente else "")
                texto += formatear_linea("Department", row.modo)
                texto += formatear_linea("Sent by", nombre)

                texto += "<br><p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>Dear colleagues:</p><br>"
                texto += "<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>Please contact the following company to coordinate the referenced shipment:</p><br>"

                texto += formatear_linea("Shipper", empresa)
                texto += formatear_linea("Address", direccion)
                texto += formatear_linea("City", ciudad)
                texto += formatear_linea("Country", pais)
                texto += formatear_linea("E-mail", email)
                texto += formatear_linea("Contacts", contactos)

                texto += "<br>"
                if consignatario:
                    texto += formatear_linea("Consignee", consignatario.empresa)
                    texto += formatear_linea("Address", consignatario.direccion)
                    texto += formatear_linea("Country", consignatario.pais)
                    texto += formatear_linea("Tax ID", consignatario.ruc)
                    texto += formatear_linea("Phone", consignatario.telefono)

                texto += "<br>"
                texto += formatear_linea("Internal Reference", f"{row.numero}/{row.embarque}")
                texto += formatear_linea("Position", row.posicion)
                texto += formatear_linea("Estimated delivery date", llegada)
                texto += formatear_linea("Port of loading", row.loading)
                texto += formatear_linea("Port of discharge", row.discharge)

                texto += "<br>"
                for m in mercaderia:
                    vol = m.cbm if m.cbm is not None else 0
                    pes = m.bruto if m.bruto is not None else 0
                    calculado = vol * 166.67
                    toneladas = round(float(m.bruto) / 1000, 2) if m.bruto else 0
                    calculado2 = str(vol) + ' AS VOL' if toneladas < vol else pes
                    calculado = pes if calculado < pes else str(calculado) + ' AS VOL'
                    aplicable = calculado2 if row.modo not in ['IMPORT AEREO', 'EXPORT AEREO'] else calculado

                    texto += formatear_linea("Commodity", m.producto)
                    texto += formatear_linea("Pieces", m.bultos)
                    texto += formatear_linea("Weight", str(m.bruto) + ' KGS')
                    texto += formatear_linea("Chargable weight", aplicable)
                    texto += formatear_linea("Volume", str(m.cbm) + ' CBM')

                texto += formatear_linea("Payment Condition", row.pago)
                texto += formatear_linea("Terms of purchase", row.terminos)
                if transportista == 'true':
                    texto += formatear_linea("Carrier", row.transportista)
                texto += formatear_linea("Transport contract", row.contratotra)
                texto += formatear_linea("Mode of shipment", row.modo)
                texto += formatear_linea("Currency", moneda_nombre)
                texto += "<br>"

            # falta el completo
            elif title == 'Instruccion de embarque':
                embarcador = Clientes.objects.get(codigo=row.embarcador_codigo)
                if row.modo != 'IMPORT AEREO' and row.modo != 'EXPORT AEREO':
                    row3 = Envases.objects.filter(numero=row.numero)

                direccion = embarcador.direccion if embarcador else ''
                empresa = embarcador.empresa if embarcador else ''
                ciudad = embarcador.ciudad if embarcador else ''
                pais = embarcador.pais if embarcador else ''
                email = embarcador.emailim if embarcador else ''
                contactos = embarcador.contactos if embarcador else ''

                consignatario = Clientes.objects.get(
                    codigo=row.consignatario_codigo) if row.consignatario_codigo else None
                cliente = Clientes.objects.get(codigo=row.cliente_codigo) if row.cliente_codigo else None
                agente = Clientes.objects.get(codigo=row.agente_codigo) if row.agente_codigo else None

                mercaderia = Cargaaerea.objects.filter(numero=row.numero)
                moneda = Monedas.objects.get(codigo=row.moneda)
                if moneda is not None:
                    moneda_nombre=moneda.nombre
                else:
                    moneda_nombre = 'S/I'

                resultado[
                    'asunto'] = f"INSTRUCCIÓN DE EMBARQUE - Ref.: {row.numero} - Shipper: {empresa} - Consignee: {consignatario.empresa if consignatario else ''}"

                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                fecha_actual = datetime.datetime.now()
                fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()
                llegada = row.eta.strftime("%d/%m/%Y") if isinstance(row.eta, datetime.datetime) else ''
                nombre = str(request.user.first_name)+' '+str( request.user.last_name)
                texto = ''
                texto += formatear_linea("Fecha", fecha_formateada)
                texto += formatear_linea("A", agente.empresa if agente else "")
                texto += formatear_linea("Departamento", row.modo)
                texto += formatear_linea("Envíado", nombre)

                texto += "<br><p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>Estimados Sres.:</p><br>"
                texto += "<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>Por favor, contactar a la siguiente compañía para coordinar la operación referenciada:</p><br>"

                texto += formatear_linea("Proveedor", empresa)
                texto += formatear_linea("Dirección", direccion)
                texto += formatear_linea("Ciudad", ciudad)
                texto += formatear_linea("País", pais)
                texto += formatear_linea("E-mail", email)
                texto += formatear_linea("Contactos", contactos)

                texto += "<br>"
                if consignatario:
                    texto += formatear_linea("Consignatario", consignatario.empresa)
                    texto += formatear_linea("Dirección", consignatario.direccion)
                    texto += formatear_linea("País", consignatario.pais)
                    texto += formatear_linea("RUC", consignatario.ruc)
                    texto += formatear_linea("Teléfono", consignatario.telefono)

                texto += "<br>"
                texto += formatear_linea("Referencia interna", f"{row.numero}/{row.embarque}")
                texto += formatear_linea("Posición", row.posicion)
                texto += formatear_linea("Recepción estimada de mercadería", llegada)
                texto += formatear_linea("Puerto de carga", row.loading)
                texto += formatear_linea("Puerto de descarga", row.discharge)


                texto += "<br>"
                for m in mercaderia:
                    vol = m.cbm if m.cbm is not None else 0
                    pes = m.bruto if m.bruto is not None else 0
                    calculado = vol * 166.67
                    toneladas = round(float(m.bruto) / 1000, 2) if m.bruto else 0
                    if toneladas < vol:
                        calculado2=str(vol) + ' AS VOL'
                    else:
                        calculado2=pes

                    if calculado < pes:
                        calculado= pes
                    else:
                        calculado = str(calculado)+' AS VOL'

                    aplicable = calculado2 if row.modo !='IMPORT AEREO' and row.modo!='EXPORT AEREO' else calculado
                    texto += formatear_linea("Mercadería", m.producto)
                    texto += formatear_linea("Bultos", m.bultos)
                    texto += formatear_linea("Peso", str(m.bruto) + ' KGS')
                    texto += formatear_linea("Aplicable", aplicable)
                    texto += formatear_linea("Volumen", str(m.cbm)+ ' CBM')

                #condicion_pago = "Collect" if row.pago == "C" else "Prepaid" if row.pago == "P" else ""
                texto += formatear_linea("Condiciones de pago", row.pago)
                texto += formatear_linea("Términos de compra", row.terminos)
                if transportista == 'true':
                    texto += formatear_linea("Transportista", row.transportista)
                texto += formatear_linea("Contrato transport.", row.contratotra)
                texto += formatear_linea("Modo de Embarque", row.modo)
                texto += formatear_linea("Moneda", moneda_nombre)
                texto += "<br>"


            texto += "<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>SALUDOS,</p>"
            texto += "<b><p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>OCEANLINK,</p></b>"
            texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>DEPARTAMENTO DE {tipos_operativa[row.modo]},</p>"
            texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>{request.user.first_name} {request.user.last_name}</p>"
            texto += "<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>OPERACIONES</p>"
            texto += "<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>PH: +598 26052332</p>"

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


