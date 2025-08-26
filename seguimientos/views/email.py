import datetime
import json
import locale

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.http import HttpResponse
import base64

from reportlab.lib.validators import isNumber, isInstanceOf

from cargosystem import settings
from impomarit.views.mails import formatear_linea, format_fecha
from login.models import AccountEmail
from mantenimientos.models import Clientes, Servicios, Vapores, Monedas, Ciudades
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
            elif title == 'Notificación de transbordo de carga':

                if row.modo=='IMPORT MARITIMO' or row.modo == 'EXPORT MARITIMO':
                    if str(row.vapor).isdigit():
                        vapor = Vapores.objects.get(codigo=row.vapor).nombre

                    else:
                        vapor = row.vapor
                else:
                    conex = Conexaerea.objects.filter(numero=row.numero).first()
                    if conex:
                        vapor=conex.vapor if conex.vapor else 'S/I'

                fecha_actual = datetime.datetime.now()

                resultado['asunto'] = 'Ref.: ' + str(row.numero) + '- H B/L: ' + str(row.hawb) + '- Shipper: '+str(row.embarcador)+'- Consignee: '+str(row.consignatario)
                if row.modo == 'IMPORT MARITIMO' or row.modo == 'EXPORT MARITIMO':
                    resultado['asunto'] += '- Vessel: '+str(row.vapor or '')
                fecha_formateada = fecha_actual.strftime(
                    f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y'
                )

                texto += fecha_formateada.capitalize().upper() + '<br><br>'

                # Bultos, peso y CBM agrupados
                carga = Cargaaerea.objects.filter(numero=row.numero)
                merca = []
                if carga is not None:
                    for m in carga:
                        merca.append(m.producto)

                    bultos = [str(b.bultos) if b.bultos is not None else "S/I" for b in carga]
                    pesos = [str(b.bruto) if b.bruto is not None else "S/I" for b in carga]
                    cbms = [str(b.cbm) if b.cbm is not None else "S/I" for b in carga]

                    texto += formatear_linea("Bultos", ", ".join(bultos))
                    texto += formatear_linea("Peso", ", ".join(pesos))
                    texto += formatear_linea("CBM", ", ".join(cbms))

                # Contenedores y precintos agrupados
                envase=Envases.objects.filter(numero=row.numero)
                if envase:
                    contenedores = [str(e.nrocontenedor) if e.nrocontenedor is not None else "S/I" for e in envase]
                    precintos = [str(e.precinto) if e.precinto is not None else "S/I" for e in envase]

                    texto += formatear_linea("Nro. Contenedores", ", ".join(contenedores))
                    texto += formatear_linea("Precintos", ", ".join(precintos))

                # Datos generales
                if row.modo == 'IMPORT MARITIMO' or row.modo == 'EXPORT MARITIMO':
                    texto += formatear_linea("Vapor", str(vapor))
                else:
                    texto += formatear_linea("Vuelo", str(vapor))
                # origen y destino nombre entero

                texto += formatear_linea("Viaje", str(row.viaje) if row.viaje is not None else "S/I")
                texto += formatear_linea("Llegada estimada", format_fecha(row.eta))
                texto += formatear_linea("Origen", str(row.origen_text) if row.origen_text is not None else "S/I")
                texto += formatear_linea("B/L", str(row.awb) if row.awb is not None else "S/I")
                texto += formatear_linea("H B/L", str(row.hawb) if row.hawb is not None else "S/I")
                texto += formatear_linea("Referencia", str(row.embarque) if row.embarque is not None else "S/I")
                texto += formatear_linea("Posición", str(row.posicion) if row.posicion is not None else "S/I")
                texto += formatear_linea("Seguimiento", str(row.numero) if row.numero is not None else "S/I")
                texto += formatear_linea("Consignatario",
                                         str(row.consignatario) if row.consignatario is not None else "S/I")
                texto += formatear_linea("Embarcador", str(row.embarcador) if row.embarcador is not None else "S/I")
                texto += formatear_linea("Orden cliente",
                                         str(row.refcliente) if row.refcliente is not None else "S/I")
                texto += formatear_linea("Ref. proveedor",
                                         str(row.refproveedor) if row.refproveedor is not None else "S/I")
                if merca:
                    nombres_merc = [m.nombre if m.nombre else "S/I" for m in merca]
                    texto += formatear_linea("Mercadería", ", ".join(nombres_merc))

                texto += "<br>"

                # Mini tabla como líneas
                texto += formatear_linea("Origen", str(row.origen_text) if row.origen_text is not None else "S/I")
                texto += formatear_linea("Destino", str(row.destino_text) if row.destino_text is not None else "S/I")
                texto += formatear_linea("Vapor/Vuelo", str(vapor))
                texto += formatear_linea("Viaje", str(row.viaje) if row.viaje is not None else "S/I")
                texto += formatear_linea("Salida", format_fecha(row.etd))
                texto += formatear_linea("Llegada", format_fecha(row.eta))

                texto += "<br>"
            elif title == 'Aviso de embarque':
                if row.modo=='IMPORT MARITIMO' or row.modo == 'EXPORT MARITIMO':
                    if str(row.vapor).isdigit():
                        vapor = Vapores.objects.get(codigo=row.vapor).nombre

                    else:
                        vapor = row.vapor
                else:
                    vapor='S/I'

                refcliente = row.refcliente if row.refcliente else "S/I"
                resultado[
                    'asunto'] = f'Ref: {row.numero} - HB/l: {row.hawb} - Shipper: {row.embarcador} - Consig: {row.consignatario}; Vapor: {vapor}; Ord. Cliente: {refcliente}'

                fecha_actual = datetime.datetime.now()

                fecha_formateada = fecha_actual.strftime(
                    f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y')

                texto = formatear_linea("Fecha", fecha_formateada.capitalize())


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

                if row.modo != 'IMPORT AEREO' and row.modo != 'EXPORT AEREO':
                    texto += formatear_linea("Vapor", vapor or "")

                texto += "<br>"

                texto += formatear_linea("Origen", row.origen_text or "")

                texto += formatear_linea("Destino", row.destino_text or "")

                texto += formatear_linea("Salida", salida)

                texto += formatear_linea("Llegada", llegada)


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
                cant=0
                gastos = Serviceaereo.objects.filter(numero=row.numero)

                if row.modo not in ['IMPORT AEREO','EXPORT AEREO']:

                    cant_cntr = Envases.objects.filter(numero=row.numero).values('tipo', 'nrocontenedor', 'precinto',
                                                                                 'bultos', 'peso', 'unidad',
                                                                                 'volumen','cantidad').annotate(total=Count('id'))

                    carga = Cargaaerea.objects.filter(numero=row.numero).values('producto__nombre','tipo')

                    if cant_cntr.count() > 0:

                        for cn in cant_cntr:
                            cant=cn['cantidad'] if cn['cantidad'] else 0
                            cant = int(cant or 0)
                            cantidad_cntr += f'{cant} x {cn["unidad"]} - {cn["tipo"]} - ' if cant !=0 else f'{cn["unidad"]} - {cn["tipo"]} - '

                            contenedores += f'{cn["nrocontenedor"]} - '

                            if cn['precinto']:
                                precintos += f'{cn["precinto"]} - '

                            bultos += cn['bultos'] if cn['bultos'] else 0

                            peso += cn['peso'] or 0

                            volumen += cn['volumen'] or 0

                    if carga.count() > 0:

                        for c in carga:
                            mercaderias += c['producto__nombre'] + ' - '
                            tipo = c["tipo"]

                    texto += formatear_linea("Contenedores", cantidad_cntr[:-3])

                    texto += formatear_linea("Nro. Contenedor/es", contenedores[:-3])

                    texto += formatear_linea("Precintos/Sellos", precintos[:-3])
                else:
                    carga = Cargaaerea.objects.filter(numero=row.numero).values('producto__nombre', 'tipo','bultos','bruto','cbm')

                    if carga.count() > 0:

                        for c in carga:
                            mercaderias += c['producto__nombre'] + ' - '
                            tipo = c["tipo"]
                            bultos += c['bultos'] if c['bultos'] else 0
                            peso += c['bruto'] or 0
                            volumen += c['cbm'] or 0

                if row.modo and row.modo.strip().upper() in ['IMPORT MARITIMO', 'EXPORT MARITIMO']:
                    texto += formatear_linea("HBL", row.hawb or "")
                else:
                    texto += formatear_linea("HAWB", row.hawb or "")

                if master == 'true':
                    if row.modo in ['IMPORT MARITIMO', 'EXPORT MARITIMO']:
                        texto += formatear_linea("MBL", row.awb or "")
                    elif row.modo in ['IMPORT AEREO', 'EXPORT AEREO']:
                        texto += formatear_linea("AWB", row.awb or "")
                    else:
                        texto += formatear_linea("CRT", row.awb or "")

                if transportista == 'true':
                    texto += formatear_linea("Transportista", row.transportista or "")

                conex = Conexaerea.objects.filter(numero=row.numero)

                if row.modo in ['IMPORT AEREO','EXPORT AEREO']:

                    if conex:
                        for i, ruta in enumerate(conex):
                            if ruta.salida:
                                fecha = ruta.salida.strftime("%d-%m")
                            else:
                                fecha = '??/??'
                            tramo = f"({ruta.origen}/{ruta.destino})  {ruta.cia}{ruta.viaje}/{fecha}" if transportista == 'true' else f"({ruta.origen}/{ruta.destino}) {ruta.viaje}/{fecha}"
                            texto += formatear_linea("Vuelo", tramo)

                    texto += formatear_linea("Aplicable", str(row.aplicable))

                texto += formatear_linea("Peso", f"{peso} KGS")

                texto += formatear_linea("Bultos", str(bultos)+' '+str(tipo))

                texto += formatear_linea("CBM", f"{volumen} M³")

                texto += "<br>"

                texto += formatear_linea("Mercadería", mercaderias[:-3])

                texto += formatear_linea("Depósito", row.deposito or "")


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
                                    if g.precio is not None and g.precio !=0:
                                        total_iva += float(g.precio) * 0.22
                                    elif g.costo is not None and g.costo !=0:
                                        total_iva += float(g.costo) * 0.22
                                    else:
                                        total_iva += 0

                                if g.precio is not None and g.precio !=0:
                                    texto += formatear_linea(servicio.nombre, f"{g.precio:.2f}", 1)
                                elif g.costo is not None and g.costo!=0:
                                    texto += formatear_linea(servicio.nombre, f"{g.costo:.2f}", 1)
                                else:
                                    texto += formatear_linea("Problema con los gastos cargados", 0)

                        texto += "<br>"

                        texto += formatear_linea("TOTAL DE GASTOS", f"{total_gastos:.2f}", 1)

                        texto += formatear_linea("I.V.A", f"{total_iva:.2f}", 1)

                        texto += formatear_linea("TOTAL A PAGAR", f"{total_gastos + total_iva:.2f}", 1)

                        texto += "<br>"


                if conex:
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
                    for c in conex:
                        salida = c.salida.strftime('%d/%m/%Y') if c.salida else 'S/i'
                        llegada = c.llegada.strftime('%d/%m/%Y') if c.llegada else 'S/i'
                        texto += "<tr>"
                        texto += f"<td style='padding: 2px 10px;'>{c.origen or ''}</td>"
                        texto += f"<td style='padding: 2px 10px;'>{c.destino or ''}</td>"
                        texto += f"<td style='padding: 2px 10px;'>{c.cia if row.modo in ['EXPORT AEREO','IMPORT AEREO'] else vapor }</td>"
                        texto += f"<td style='padding: 2px 10px;'>{c.viaje or ''}</td>"
                        texto += f"<td style='padding: 2px 10px;'>{salida}</td>"
                        texto += f"<td style='padding: 2px 10px;'>{llegada}</td>"
                        texto += "</tr>"

                    texto += "</table><br>"

                texto += "<pre style='font-family: Courier New, monospace; font-size: 12px;'>"

                texto += "Los buques, vuelos y las llegadas al puerto de Montevideo son siempre a CONFIRMAR, ya que puede haber trasbordos y/o alteraciones en las fechas estimadas de llegada\n"
                texto+="sin previo aviso, por lo cual le sugerimos consultarnos por la fecha de arribo que aparece en este aviso.\n"
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

                refcliente = row.refcliente if row.refcliente else "S/I"

                resultado[
                    'asunto'] = f'NOTIFICACION DE LLEGADA DE CARGA - Ref.: {row.numero} - HB/l: {row.hawb} - Ship: {row.embarcador} - Consig: {row.consignatario}; Vapor/vuelo: {vapor}; Ord. Cliente: {refcliente}'

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

                texto += formatear_linea("Origen", row.origen_text )

                texto += formatear_linea("Destino", row.destino_text )
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
                            if ruta.salida:
                                fecha = ruta.salida.strftime("%d-%m")
                            else:
                                fecha = '??/??'
                            tramo = f"({ruta.origen}/{ruta.destino})  {ruta.cia}{ruta.viaje}/{fecha}"
                            texto += formatear_linea("Vuelo", tramo)

                texto += formatear_linea("Embarcador", row.embarcador)

                texto += formatear_linea("Ref. Proveedor", row.refproveedor)

                cantidad_cntr = contenedores = precintos = movimiento = ''

                if row.modo not in ['IMPORT AEREO','EXPORT AEREO']:
                    cant_cntr = Envases.objects.filter(numero=row.numero).values(

                        'tipo', 'nrocontenedor', 'precinto', 'bultos', 'peso', 'unidad', 'volumen','movimiento'

                    ).annotate(total=Count('id'))

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
                    toneladas = calculado2= vol =0
                    for c in carga:
                        bruto=float(c.bruto or 0)
                        vol = c.cbm if c.cbm is not None else 0

                        texto += formatear_linea("Mercadería", c.producto.nombre)

                        texto += formatear_linea("Bultos", str(c.bultos) if c.bultos else 0)

                        texto += formatear_linea("Peso", bruto)
                        cbm=round(float(c.cbm or 0),2)
                        texto += formatear_linea("CBM", str(cbm or 'S/I')+' M³')


                        toneladas = round(float(bruto) / 1000, 2) if bruto else 0

                        calculado2 = str(vol) + ' AS VOL' if toneladas < vol else bruto

                        aplicable = str(row.aplicable)

                    if row.modo in ['IMPORT AEREO','EXPORT AEREO']:
                        texto += formatear_linea("Aplicable", str(aplicable))

                    if row.modo in ['IMPORT MARITIMO'] and movimiento != 'FCL/FCL':
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


                texto += "</pre>"
            elif title == 'Aviso de desconsolidacion':

                fecha_actual = datetime.datetime.now()

                fecha_formateada = fecha_actual.strftime(
                    f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y')

                resultado['asunto'] = (

                    f'Ref.: {row.numero} - HB/l: {row.hawb} - Ship: {row.embarcador}'

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
                texto += formatear_linea("Origen", row.origen_text)
                texto += formatear_linea("Destino", row.destino_text)

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

                    f'Seg.: {row.numero} - HB/l: {row.hawb} - Shipper: {row.embarcador} - CNEE: {row.consignatario}'

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

                    f'FCR.: {row.hawb or ""} - SEGUIMIENTO {row.numero or ""}'

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

                resultado['asunto'] = f'{row.awb} - seguimiento: {row.numero}'

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

                resultado['asunto'] = ' / NVOCC / CÍA AEREA'

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
                resultado['asunto'] = f'seguimiento: {row.numero}'

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

                resultado['asunto'] = 'Ref.: ' + str(row.numero) + '- Shipper: ' + str(row.embarcador) + '; Consignee: ' + str(row.consignatario)

                fecha_formateada = fecha_actual.strftime(

                    f'{dias_semana[fecha_actual.weekday()]}, %d de {meses[fecha_actual.month - 1]} del %Y'

                )

                texto += fecha_formateada.capitalize().upper() + '<br><br>'




                # Datos generales

                texto += formatear_linea("Embarque", str(row.numero) if row.numero is not None else "S/I")

                texto += formatear_linea("Posición", str(row.posicion) if row.posicion is not None else "S/I")

                texto += formatear_linea("Salida", row.etd.strftime('%d-%m-%Y') if row.etd else '')

                texto += formatear_linea("Llegada", row.eta.strftime('%d-%m-%Y') if row.eta else '')

                texto += formatear_linea("Origen", str(row.origen_text) if row.origen_text is not None else "S/I")

                texto += formatear_linea("Destino", str(row.destino_text) if row.destino_text is not None else "S/I")

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
                # Mercaderías

                mercaderia = Cargaaerea.objects.filter(numero=row.numero).values('producto__nombre','bultos','bruto','cbm')
                # Mercaderías
                # Bultos, peso y CBM
                if mercaderia:
                    bultos = [str(b['bultos']) if b['bultos'] else "S/I" for b in mercaderia]
                    pesos = [str(b['bruto']) if b['bruto'] else "S/I" for b in mercaderia]
                    cbms = [str(b['cbm']) if b['cbm'] else "S/I" for b in mercaderia]
                    nombres_merc = [b['producto__nombre'] if b['producto__nombre'] else "S/I" for b in mercaderia]
                    texto += formatear_linea("Mercadería", ", ".join(nombres_merc))
                    texto += formatear_linea("Bultos", ", ".join(bultos))
                    texto += formatear_linea("Peso", ", ".join(pesos))
                    texto += formatear_linea("CBM", ", ".join(cbms))
                # Contenedores y precintos


                if row.modo not in ['IMPORT AEREO','EXPORT AEREO']:
                    envases=Envases.objects.filter(numero=row.numero).values('nrocontenedor','precinto')
                    if envases:
                        contenedores = [str(e['nrocontenedor']) if e['nrocontenedor'] else "S/I" for e in envases]
                        precintos = [str(e['precinto']) if e['precinto'] else "S/I" for e in envases]

                        texto += formatear_linea("Nro. Contenedores", ", ".join(contenedores))
                        texto += formatear_linea("Precintos", ", ".join(precintos))

                texto += ('Los buques y las llegadas al puerto de Montevideo son siempre a CONFIRMAR, ya </br>'
                          ' que puede haber trasbordos y/o alteraciones en las fechas estimadas de llegada </br>'
                          'sin previo aviso, por lo cual sugerimos consultarnos por la fecha de arribo que aparece en este aviso.')

                texto += "<br>"
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
                ocean = Clientes.objects.get(codigo=835)

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

                if 'MARITIMO' in row.modo:
                    modo = 'SEAFREIGHT'
                    master='MBL'
                    house = 'HBL'
                elif 'AEREO' in row.modo:
                    modo = 'AIRFREIGHT'
                    master = 'AWB'
                    house = 'HAWB'
                elif 'TERRESTRE' in row.modo:
                    modo = 'ROADFREIGHT'
                    master = 'MCRT'
                    house = 'HCRT'
                else:
                    modo = 'UNKNOWN'
                    master = 'UNKNOWN'
                    house = 'UNKNOWN'

                texto = ''
                texto += formatear_linea("Date", fecha_formateada)
                texto += formatear_linea("To", agente.empresa if agente else "")
                texto += formatear_linea("Department", modo)
                texto += formatear_linea("Sent by", nombre)

                texto += "<br><p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>Dear colleagues:</p>"
                texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>Please contact the following company to coordinate the following shipment as per our instructions below:</p>"
                texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>Please ack this message and let us know status of cargo asap.</p><br>"
                if directo_boolean == 'true':
                    texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>Please add HS code on {master} an {house}</p><br>"
                if directo_boolean=='true':
                    texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>{master}</p>"
                    texto_ocean=str(ocean.empresa)+' '+str(ocean.direccion)+' '+'CP 11000 '+str(ocean.ruc)+' '+str(ocean.telefono)
                    texto += formatear_linea("Shipper", agente.empresa)
                    texto += formatear_linea("Consignee", texto_ocean)

                texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>{house if directo_boolean=='true' else master}</p>"

                texto +='</br>'
                texto += formatear_linea("Shipper name", empresa)
                texto += formatear_linea("Address", direccion)
                texto += formatear_linea("City", ciudad)
                texto += formatear_linea("Country", pais)
                texto += formatear_linea("E-mail", email)
                texto += formatear_linea("Contact", contactos)

                texto += "<br>"
                if consignatario:
                    texto += formatear_linea("Consignee name", consignatario.empresa)
                    texto += formatear_linea("Address", consignatario.direccion)
                    texto += formatear_linea("Country", consignatario.pais)
                    texto += formatear_linea("Tax ID", consignatario.ruc)
                    texto += formatear_linea("Phone", consignatario.telefono)

                texto += "<br>"
                texto += formatear_linea("Internal Reference", f"{row.numero}/{row.embarque}")
                texto += formatear_linea("Estimated delivery date", llegada)
                loading = 'S/I'
                discharge = 'S/I'

                if row.loading is not None:
                    ciudad_l = Ciudades.objects.filter(codigo=row.loading).first()
                    loading = ciudad_l.nombre
                if row.discharge is not None:
                    ciudad_d = Ciudades.objects.filter(codigo=row.discharge).first()
                    discharge = ciudad_d.nombre

                texto += formatear_linea("Port of loading", loading)
                texto += formatear_linea("Port of discharge", discharge)

                texto += "<br>"
                for m in mercaderia:
                    vol = m.cbm if m.cbm is not None else 0
                    pes = m.bruto if m.bruto is not None else 0
                    calculado = vol * 166.67
                    toneladas = round(float(m.bruto) / 1000, 2) if m.bruto else 0
                    calculado2 = str(vol) + ' AS VOL' if toneladas < vol else pes
                    calculado = pes if calculado < pes else str(calculado) + ' AS VOL'
                    aplicable =str(row.aplicable)

                    texto += formatear_linea("Commodity", m.producto)
                    texto += formatear_linea("Pieces", m.bultos)
                    texto += formatear_linea("Weight", str(m.bruto) + ' KGS')
                    texto += formatear_linea("Chargable weight", aplicable)
                    texto += formatear_linea("Volume", str(m.cbm) + ' CBM')

                texto += formatear_linea("Payment Condition", row.pago)
                texto += formatear_linea("Buying terms", row.terminos)
                if transportista == 'true':
                    texto += formatear_linea("Carrier", row.transportista)
                texto += formatear_linea("Transport contract", row.contratotra)
                texto += formatear_linea("Shipment mode", modo)
                texto += formatear_linea("Currency", moneda_nombre)
                texto += "<br>"
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
                ocean = Clientes.objects.get(codigo=835)

                mercaderia = Cargaaerea.objects.filter(numero=row.numero)
                moneda = Monedas.objects.get(codigo=row.moneda)
                if moneda is not None:
                    moneda_nombre=moneda.nombre
                else:
                    moneda_nombre = 'S/I'

                resultado['asunto'] = f"INSTRUCCIÓN DE EMBARQUE - Ref.: {row.numero} - Shipper: {empresa} - Consignee: {consignatario.empresa if consignatario else ''}"

                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                fecha_actual = datetime.datetime.now()
                fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()
                llegada = row.eta.strftime("%d/%m/%Y") if isinstance(row.eta, datetime.datetime) else ''
                nombre = str(request.user.first_name)+' '+str( request.user.last_name)
                texto = ''
                if 'MARITIMO' in row.modo:
                    modo = 'MARITIMO'
                    master = 'MBL'
                    house = 'HBL'
                elif 'AEREO' in row.modo:
                    modo = 'AEREO'
                    master = 'AWB'
                    house = 'HAWB'
                elif 'TERRESTRE' in row.modo:
                    modo = 'TERRESTRE'
                    master = 'MCRT'
                    house = 'HCRT'
                else:
                    modo = 'UNKNOWN'
                    master = 'UNKNOWN'
                    house = 'UNKNOWN'
                texto += formatear_linea("Fecha", fecha_formateada)
                texto += formatear_linea("A", agente.empresa if agente else "")
                texto += formatear_linea("Departamento", modo)
                texto += formatear_linea("Envíado", nombre)

                texto += "<br><p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>Estimados Sres.:</p><br>"
                texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>Por favor, contactar a la siguiente compañía para coordinar el siguiente embarque según nuestras instrucciones a continuación:</p>"
                texto += "<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>Por favor confirmar este mensaje e informarnos el estado de la carga a la brevedad.</p><br>"
                if directo_boolean == 'true':
                    texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>Favor incluir el código HS en {master} y {house}</p>"
                if directo_boolean == 'true':
                    texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>{master}</p>"
                    ocean = Clientes.objects.get(codigo=835)
                    texto_ocean = str(ocean.empresa) + ' ' + str(ocean.direccion) + ' CP 11000 ' + str(
                        ocean.ruc) + ' ' + str(ocean.telefono)
                    texto += formatear_linea("Shipper", agente.empresa)
                    texto += formatear_linea("Consignatario", texto_ocean)
                texto += "<br>"
                texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>{house if directo_boolean=='true' else master}</p>"
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

                #aca
                loading = 'S/I'
                discharge = 'S/I'

                if row.loading is not None:
                    ciudad_l = Ciudades.objects.filter(codigo=row.loading).first()
                    loading=ciudad_l.nombre
                if row.discharge is not None:
                    ciudad_d = Ciudades.objects.filter(codigo=row.discharge).first()
                    discharge=ciudad_d.nombre

                texto += formatear_linea("Puerto de carga", loading)
                texto += formatear_linea("Puerto de descarga", discharge)


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

                    aplicable = str(row.aplicable)
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
                texto += formatear_linea("Modo de Embarque", modo)
                texto += formatear_linea("Moneda", moneda_nombre)
                texto += "<br>"

            estilo = "font-family: Courier New, Courier, monospace; font-size: 12px;"
            texto += f"<div style='{estilo}'>Agradeciendo vuestra preferencia, le saludamos muy atentamente.</div></br>"
            texto += f"<div style='{estilo}'>{request.user.first_name} {request.user.last_name}</div>"
            texto += f"<div style='{estilo}'>{request.user.email}</div>"
            texto += f"<div style='{estilo}; font-weight: bold;'>DEPARTAMENTO DE {tipos_operativa[row.modo]}</div>"
            texto += f"<div style='{estilo}'>{settings.EMPRESA_firma}</div>"
            texto += f"<div style='{estilo}'>PH: +598 26052332</div>"

            resultado['email_cliente'] = email_cliente
            resultado['email_agente'] = email_agente
            emails_disponibles = list(AccountEmail.objects.filter(user=request.user).values_list('email', flat=True))
            resultado['emails_disponibles'] = emails_disponibles
            resultado['resultado'] = 'exito'
            resultado['mensaje'] = texto
            resultado['asunto']=str(title.upper())+' - '+str(resultado['asunto'])
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


