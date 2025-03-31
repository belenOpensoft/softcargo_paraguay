import locale
from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
import base64
from django.views.decorators.csrf import csrf_exempt
from expmarit.models import VEmbarqueaereo, ExpmaritCargaaerea as Cargaaerea, ExpmaritEnvases as Envases, \
    ExpmaritServiceaereo as Serviceaereo, ExpmaritEmbarqueaereo as Embarqueaereo, ExpmaritConexaerea as Conexaerea
from impomarit.views.mails import formatear_linea
from mantenimientos.views.bancos import is_ajax
from mantenimientos.models import Productos, Clientes, Monedas, Servicios, Vapores
from seguimientos .models import VGrillaSeguimientos

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
            master = request.POST['master']
            gastos_boolean = request.POST['gastos']
            #9155
            row = VEmbarqueaereo.objects.get(numero=row_number)
            row2 = Cargaaerea.objects.filter(numero=row_number)
            row3 = Envases.objects.filter(numero=row_number)
            embarque=Embarqueaereo.objects.get(numero=row_number)
            gastos = Serviceaereo.objects.filter(numero=row_number)
            email_cliente = Clientes.objects.get(codigo=embarque.consignatario).emailem if embarque.consignatario is not None else 'S/I'
            email_agente = Clientes.objects.get(codigo=embarque.agente).emailem if embarque.agente is not None else 'S/I'

            if embarque.vapor is not None and embarque.vapor.isdigit():
                vapor = Vapores.objects.get(codigo=embarque.vapor).nombre
            elif embarque.vapor is not None:
                vapor = embarque.vapor
            else:
                vapor = 'S/I'


            try:
                seguimiento = VGrillaSeguimientos.objects.get(numero=row.seguimiento)

            except VGrillaSeguimientos.DoesNotExist:

                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='', deposito='', pago='',vendedor='')

            texto = ''
            texto += f'<br>'
            texto, resultado = get_data_html(row_number, row, row2, row3, title, texto, resultado,seguimiento,gastos,embarque,master,gastos_boolean,vapor)
            texto += "<b><p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>OCEANLINK,</p></b>"
            texto += f"<p style='font-family: Courier New, Courier, monospace; font-size: 12px;'>DEPARTAMENTO DE EXPORTACIÓN MARITIMA,</p>"
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



def get_data_html(row_number, row, row2, row3, title, texto, resultado, seguimiento,gastos,embarque,master,gastos_boolean,vapor):
    # merca = Productos.objects.get(codigo=row2.producto.codigo)
    if row2 is not None:
        merca = []
        for m in row2:
            merca.append(m.producto)

    fecha_actual = datetime.now()

    if title == 'Notificación de transbordo de carga':
        fecha_actual = datetime.now()

        resultado['asunto'] = 'NOTIFICACIÓN DE TRABSBORDO DE CARGA - Ref.: ' + str(row.referencia) + \
                              '/ CS: ' + str(row.seguimiento) + '- H B/L: ' + str(row.hawb) + '- Shipper: '

        fecha_formateada = fecha_actual.strftime(
            f'{DIAS_SEMANA[fecha_actual.weekday()]}, %d de {MESES[fecha_actual.month - 1]} del %Y'
        )

        texto += fecha_formateada.capitalize().upper() + '<br><br>'

        # Bultos y pesos
        cont = 1
        for b in row2:
            texto += formatear_linea(f"Bultos {cont}", b.bultos if b.bultos is not None else "S/I")
            texto += formatear_linea(f"Peso {cont}", b.bruto if b.bruto is not None else "S/I")
            cont += 1

        # Contenedores
        cont = 1
        for e in row3:
            texto += formatear_linea(f"Nro. Contenedor {cont}", str(e.nrocontenedor) if e.nrocontenedor else "S/I")
            cont += 1

        # Datos generales
        texto += formatear_linea("Vapor", str(vapor) if vapor is not None else "S/I")
        texto += formatear_linea("Viaje", str(row.viaje) if row.viaje is not None else "S/I")
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

        texto += "<br>"

        # Mini resumen
        texto += formatear_linea("Origen", str(row.origen) if row.origen is not None else "S/I")
        texto += formatear_linea("Destino", str(row.destino) if row.destino is not None else "S/I")
        texto += formatear_linea("Vapor/Vuelo", str(vapor) if vapor is not None else "S/I")
        texto += formatear_linea("Viaje", str(row.viaje) if row.viaje is not None else "S/I")
        texto += formatear_linea("Salida", format_fecha(row.fecha_embarque))
        texto += formatear_linea("Llegada", format_fecha(row.fecha_retiro))

        texto += "<br>"

        return texto, resultado
    elif title == 'Novedades sobre la carga':

        fecha_actual = datetime.now()

        resultado['asunto'] = (

                'NOVEDADES SOBRE LA CARGA - Ref.: ' + str(row.referencia) +

                ' / CS: ' + str(row.seguimiento) + ' - Shipper: ' + str(row.embarcador) +

                '; Consignee: ' + str(row.consignatario)

        )

        fecha_formateada = fecha_actual.strftime(

            f'{DIAS_SEMANA[fecha_actual.weekday()]}, %d de {MESES[fecha_actual.month - 1]} del %Y'

        )

        texto += fecha_formateada.capitalize().upper() + '<br><br>'

        # Mercadería

        cont = 1

        for m in merca:
            texto += formatear_linea(f"Mercadería {cont}", m.nombre if m.nombre else "S/I")

            cont += 1

        # Bultos / Peso / CBM

        cont = 1

        for b in row2:
            texto += formatear_linea(f"Bultos {cont}", b.bultos if b.bultos is not None else "S/I")

            texto += formatear_linea(f"Peso {cont}", b.bruto if b.bruto is not None else "S/I")

            texto += formatear_linea(f"CBM {cont}", b.cbm if b.cbm is not None else "S/I")

            cont += 1

        # Contenedores y precintos

        cont = 1

        for e in row3:
            texto += formatear_linea(f"Nro. Contenedor {cont}", e.nrocontenedor if e.nrocontenedor else "S/I")

            texto += formatear_linea(f"Precintos {cont}", e.precinto if e.precinto else "S/I")

            cont += 1

        # Datos generales

        texto += formatear_linea("Embarque", row_number if row_number else "S/I")

        texto += formatear_linea("Posición", row.posicion if row.posicion else "S/I")

        texto += formatear_linea("Salida", format_fecha(row.fecha_embarque))

        texto += formatear_linea("Llegada", format_fecha(row.fecha_retiro))

        texto += formatear_linea("Origen", row.origen if row.origen else "S/I")

        texto += formatear_linea("Destino", row.destino if row.destino else "S/I")

        texto += formatear_linea("Vapor", vapor if vapor else "S/I")

        texto += formatear_linea("H B/L", row.hawb if row.hawb else "S/I")

        texto += formatear_linea("Embarcador", row.embarcador if row.embarcador else "S/I")

        texto += formatear_linea("Consignatario", row.consignatario if row.consignatario else "S/I")

        # Despedida

        texto += "<br>Saludos cordiales,<br><b>OCEANLINK</b><br>"

        return texto, resultado
    elif title == 'Routing Order':

        hora_actual = datetime.now().strftime("%H:%M")

        fecha_actual = datetime.now()

        resultado['asunto'] = 'ROUTING ORDER - Ref.: ' + str(row.referencia) + \
 \
                              '/ CS: ' + str(row.seguimiento) + '- Shipper: ' + str(row.embarcador) + \
 \
                              '; Consignee: ' + str(row.consignatario)

        texto += f'{hora_actual} <br><br>'

        # Encabezado

        texto += formatear_linea("Fecha", format_fecha(fecha_actual))

        texto += formatear_linea("A", str(row.agente) if row.agente is not None else "S/I")

        texto += formatear_linea("Departamento", "MARITIMO")

        texto += '<br><br>Estimados Sres.: <br>'

        texto += 'Por favor, contactar la siguiente compañía para coordinar la operación referenciada: <br><br>'

        # Embarcador

        texto += formatear_linea("Proveedor", str(row.embarcador) if row.embarcador is not None else "S/I")

        texto += formatear_linea("Dirección",
                                 str(row.direccion_embarcador) if row.direccion_embarcador is not None else "S/I")

        texto += formatear_linea("Ciudad", str(row.ciudad_embarcador) if row.ciudad_embarcador is not None else "S/I")

        texto += formatear_linea("País", str(row.pais_embarcador) if row.pais_embarcador is not None else "S/I")

        texto += '<br>'

        # Consignatario

        texto += formatear_linea("Consignatario", str(row.consignatario) if row.consignatario is not None else "S/I")

        texto += formatear_linea("Dirección",
                                 str(row.direccion_consignatario) if row.direccion_consignatario is not None else "S/I")

        texto += formatear_linea("Ciudad",
                                 str(row.ciudad_consignatario) if row.ciudad_consignatario is not None else "S/I")

        texto += formatear_linea("País", str(row.pais_consignatario) if row.pais_consignatario is not None else "S/I")

        texto += '<br>'

        # Datos generales

        texto += formatear_linea("Referencia interna", str(row_number) if row_number is not None else "S/I")

        texto += formatear_linea("Orden cliente", str(row.orden_cliente) if row.orden_cliente is not None else "S/I")

        texto += formatear_linea("Origen", str(row.origen) if row.origen is not None else "S/I")

        texto += formatear_linea("Destino", str(row.destino) if row.destino is not None else "S/I")

        texto += '<br>'

        # Mercadería y bultos/peso

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

        texto += formatear_linea("Modo de embarque", "MARITIMO")

        texto += "<br>"

        return texto, resultado
    elif title == 'Notificación de llegada de carga':

        resultado[
            'asunto'] = f'NOTIFICACION DE LLEGADA DE CARGA - Ref.: {embarque.numero} - CS: {row.seguimiento} - HB/l: {row.hawb} - Ship: {row.embarcador} - Consig: {row.consignatario}; Vapor: {vapor}'

        # Fecha actual en español

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        fecha_actual = datetime.now()

        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

        consigna = Clientes.objects.get(codigo=embarque.consignatario)

        conex = Conexaerea.objects.filter(numero=embarque.numero).order_by('-id').last()

        carga = Cargaaerea.objects.filter(numero=embarque.numero)

        gastos = Serviceaereo.objects.filter(numero=embarque.numero)

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

        if master == 'true':
            texto += formatear_linea("AWB", row.awb)

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

                iva = servicio.tasa == 'B'

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
#hacer de nuevo
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
            if isinstance(embarque.llegada, datetime):
                llegada = str(embarque.llegada.strftime("%d/%m/%Y"))
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

            envase_text = ''
            if row3:
                for e in row3:
                    cantidad = e.cantidad if e.cantidad is not None else 0
                    tipo = e.tipo if e.tipo is not None else 'S/I'
                    unidad = e.unidad if e.unidad is not None else 'S/I'
                    nrocontenedor = e.nrocontenedor if e.nrocontenedor is not None else 'S/I'
                    envase_text += str(cantidad) + 'x' + str(unidad) + ' ' + str(tipo) + ': ' + str(nrocontenedor)
                    if len(row3) > 1:
                        envase_text += '<br>'

            condicion_pago = "Collect" if row.pago_flete == "C" else "Prepaid" if row.pago_flete == "P" else ""
            tabla_html += f"<tr><th align='left'>Condiciones de pago: </th><td>{condicion_pago}</td></tr>"
            tabla_html += f"<tr><th align='left'>Términos de compra: </th><td>{row.terminos}</td></tr>"
            tabla_html += f"<tr><th align='left'>Envase: </th><td>{envase_text}</td></tr>"
            tabla_html += f"<tr><th align='left'>Modo de embarque: </th><td>MARITIMO</td></tr>"
            tabla_html += f"<tr><th align='left'>Moneda: </th><td>{moneda.nombre}</td></tr>"
            tabla_html += "</table><br>"

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



def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data).decode("utf-8")
        return base64_data
