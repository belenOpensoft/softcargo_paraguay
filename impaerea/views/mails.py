import locale
from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
import base64
from django.views.decorators.csrf import csrf_exempt

from impaerea.models import VGastosHouse, ImportEmbarqueaereo, ImportReservas, ImportConexaerea
from impaerea.models import VEmbarqueaereo, ImportCargaaerea, ImportServiceaereo, ImportEmbarqueaereo as Embarqueaereo
from impomarit.views.mails import formatear_linea
from mantenimientos.views.bancos import is_ajax
from mantenimientos.models import Productos, Monedas, Clientes, Servicios
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
            directo_boolean = request.POST['directo']
            armador = request.POST['armador']

            #9155
            embarque=ImportEmbarqueaereo.objects.get(numero=row_number)
            row = VEmbarqueaereo.objects.get(numero=row_number)
            row2 = ImportCargaaerea.objects.filter(numero=row_number)
            gastos = VGastosHouse.objects.filter(numero=row_number)
            #master=ImportReservas.objects.filter(awb=embarque.awb)
            email_cliente = Clientes.objects.get(codigo=embarque.consignatario).emailia if embarque.consignatario is not None else 'S/I'
            email_agente = Clientes.objects.get(codigo=embarque.agente).emailia if embarque.agente is not None else 'S/I'
            conex = ImportConexaerea.objects.filter(numero=embarque.numero)
            if conex:
                vapor = conex[0].vuelo if conex[0].vuelo else 'S/I'
            else:
                vapor = 'S/I'
            try:
                seg = VGrillaSeguimientos.objects.get(numero=row.seguimiento)
                seguimiento = VGrillaSeguimientos.objects.get(numero=row.seguimiento)

            except VGrillaSeguimientos.DoesNotExist:
                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='', deposito='', pago='',vendedor='')
                seg = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='', deposito='', pago='',vendedor='')

            texto = ''
            texto += f'<br>'
            texto, resultado = get_data_html(row_number, row, row2,seg, title, texto, resultado,seguimiento,gastos,embarque,conex,vapor,transportista,master_boolean,gastos_boolean,directo_boolean,request,armador)
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


def get_data_html(row_number, row, row2,seg, title, texto, resultado,seguimiento,gastos,embarque,conex,vapor,transportista_boolean,master_boolean,gastos_boolean,directo_boolean,request,armador):
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

        # Datos generales
        texto += formatear_linea("Vuelo", str(vapor))
        texto += formatear_linea("Viaje", str(seg.viaje) if seg.viaje is not None else "S/I")
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

        # Mini tabla final como líneas formateadas
        texto += formatear_linea("Origen", str(row.origen) if row.origen is not None else "S/I")
        texto += formatear_linea("Destino", str(row.destino) if row.destino is not None else "S/I")
        texto += formatear_linea("Vuelo/Vuelo", str(vapor))
        texto += formatear_linea("Viaje", str(seg.viaje) if seg.viaje is not None else "S/I")
        texto += formatear_linea("Salida", format_fecha(row.fecha_embarque))
        texto += formatear_linea("Llegada", format_fecha(row.fecha_retiro))

        texto += "<br>"

        return texto, resultado
    elif title == 'Novedades sobre la carga':

        fecha_actual = datetime.now()

        resultado['asunto'] = 'NOVEDADES SOBRE LA CARGA - Ref.: ' + str(row.referencia) + \
     \
                                  ' / CS: ' + str(row.seguimiento) + ' - Shipper: ' + str(row.embarcador) + \
     \
                                  '; Consignee: ' + str(row.consignatario)

        fecha_formateada = fecha_actual.strftime(

            f'{DIAS_SEMANA[fecha_actual.weekday()]}, %d de {MESES[fecha_actual.month - 1]} del %Y'

        )

        texto += fecha_formateada.capitalize().upper() + '<br><br>'

        # Mercaderías

        cont = 1

        for m in merca:
            texto += formatear_linea(f"Mercadería {cont}", str(m.nombre) if m.nombre is not None else "S/I")

            cont += 1

        # Bultos y pesos

        cont = 1

        for b in row2:
            texto += formatear_linea(f"Bultos {cont}", b.bultos if b.bultos is not None else "S/I")

            texto += formatear_linea(f"Peso {cont}", b.bruto if b.bruto is not None else "S/I")

            cont += 1

        # Datos generales

        texto += formatear_linea("Embarque", str(row_number) if row_number is not None else "S/I")

        texto += formatear_linea("Posición", str(row.posicion) if row.posicion is not None else "S/I")

        texto += formatear_linea("Salida", format_fecha(row.fecha_embarque))

        texto += formatear_linea("Llegada", format_fecha(row.fecha_retiro))

        texto += formatear_linea("Origen", str(row.origen) if row.origen is not None else "S/I")

        texto += formatear_linea("Destino", str(row.destino) if row.destino is not None else "S/I")

        texto += formatear_linea("Vuelo", str(vapor) if vapor is not None else "S/I")

        texto += formatear_linea("H B/L", str(row.hawb) if row.hawb is not None else "S/I")

        texto += formatear_linea("Embarcador", str(row.embarcador) if row.embarcador is not None else "S/I")

        texto += formatear_linea("Consignatario", str(row.consignatario) if row.consignatario is not None else "S/I")

        texto += "<br>"

        return texto, resultado
    elif title == 'Routing Order':

        hora_actual = datetime.now().strftime("%H:%M")

        fecha_actual = datetime.now()

        resultado['asunto'] = 'ROUTING ORDER - Ref.: ' + str(row.referencia) + \
 \
                              ' / CS: ' + str(row.seguimiento) + ' - Shipper: ' + str(row.embarcador) + \
 \
                              '; Consignee: ' + str(row.consignatario)

        texto += f'{hora_actual} <br><br>'

        texto += formatear_linea("Fecha", format_fecha(fecha_actual))

        texto += formatear_linea("A", str(row.agente) if row.agente else "S/I")

        texto += formatear_linea("Departamento", "MARITIMO")

        texto += "<br>"

        texto += "Estimados Sres.: <br>"

        texto += "Por favor, contactar la siguiente compañía para coordinar la operación referenciada: <br><br>"

        # Datos del proveedor

        texto += formatear_linea("Proveedor", str(row.embarcador) if row.embarcador else "S/I")

        texto += formatear_linea("Dirección", str(row.direccion_embarcador) if row.direccion_embarcador else "S/I")

        texto += formatear_linea("Ciudad", str(row.ciudad_embarcador) if row.ciudad_embarcador else "S/I")

        texto += formatear_linea("País", str(row.pais_embarcador) if row.pais_embarcador else "S/I")

        texto += "<br>"

        # Datos del consignatario

        texto += formatear_linea("Consignatario", str(row.consignatario) if row.consignatario else "S/I")

        texto += formatear_linea("Dirección", str(row.direccion_consignatario) if row.direccion_consignatario else "S/I")

        texto += formatear_linea("Ciudad", str(row.ciudad_consignatario) if row.ciudad_consignatario else "S/I")

        texto += formatear_linea("País", str(row.pais_consignatario) if row.pais_consignatario else "S/I")

        texto += "<br>"

        # Datos de la operación

        texto += formatear_linea("Referencia interna", str(row_number) if row_number else "S/I")

        texto += formatear_linea("Orden cliente", str(row.orden_cliente) if row.orden_cliente else "S/I")

        texto += formatear_linea("Origen", str(row.origen) if row.origen else "S/I")

        texto += formatear_linea("Destino", str(row.destino) if row.destino else "S/I")

        texto += "<br>"

        # Mercadería y carga

        cont = 1

        for m in merca:
            texto += formatear_linea(f"Mercadería {cont}", str(m.nombre) if m.nombre else "S/I")

            cont += 1

        cont = 1

        for b in row2:
            texto += formatear_linea(f"Bultos {cont}", b.bultos if b.bultos is not None else "S/I")

            texto += formatear_linea(f"Peso {cont}", b.bruto if b.bruto is not None else "S/I")

            cont += 1

        texto += formatear_linea("Condiciones de pago", str(row.pago_flete) if row.pago_flete else "S/I")

        texto += formatear_linea("Términos de compra", str(row.terminos) if row.terminos else "S/I")

        texto += formatear_linea("Modo de embarque", "MARITIMO")

        texto += "<br>"

        return texto, resultado
    elif title == 'Notificación de llegada de carga':

        resultado['asunto'] = (

            f'NOTIFICACION DE LLEGADA DE CARGA - Ref.: {embarque.numero} - CS: {row.seguimiento} - '

            f'HB/l: {row.hawb} - Ship: {row.embarcador} - Consig: {row.consignatario}; Vuelo: {vapor}'

        )

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        fecha_actual = datetime.now()

        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

        consigna = Clientes.objects.get(codigo=embarque.consignatario)

        carga = ImportCargaaerea.objects.filter(numero=embarque.numero)

        gastos = ImportServiceaereo.objects.filter(numero=embarque.numero)

        texto = formatear_linea("Fecha", fecha_formateada)

        texto += "<br>"

        texto += formatear_linea("Att.", "")

        texto += formatear_linea("Notificar a", row.consignatario)

        texto += formatear_linea("Dirección", consigna.direccion if consigna else "")

        texto += formatear_linea("Teléfono", consigna.telefono if consigna else "")

        texto += "<br>"
        salida = seg.etd.strftime("%d/%m/%Y") if isinstance(row.etd, datetime) else ''

        llegada = seg.eta.strftime("%d/%m/%Y") if isinstance(row.eta, datetime) else ''

        texto += formatear_linea("Salida", salida )

        texto += formatear_linea("Llegada", llegada )

        texto += formatear_linea("Origen", row.origen)
        texto += formatear_linea("Destino", row.destino )

        texto += formatear_linea("HAWB", embarque.hawb)

        if master_boolean == 'true':
            texto += formatear_linea("AWB", embarque.awb)

        texto += formatear_linea("Referencia", embarque.numero)

        texto += formatear_linea("Posición", embarque.posicion)

        texto += formatear_linea("Seguimiento", row.seguimiento)

        if conex:
            for i, ruta in enumerate(conex):
                if ruta.llegada:
                    fecha = ruta.llegada.strftime("%d/%m")
                else:
                    fecha = '??/??'
                tramo = f"({ruta.origen}/{ruta.destino})   {ruta.cia}{ruta.viaje}/{fecha}"
                texto += formatear_linea("Vuelo", tramo)

        texto += formatear_linea("Embarcador", row.embarcador)

        texto += formatear_linea("Ref. Proveedor", row.embarcador)

        if carga:

            for c in carga:

                if c.medidas is not None:

                    medidas = c.medidas.split('*')

                else:

                    medidas = None

                if medidas and len(medidas) == 3 and all(m.isdigit() for m in medidas):

                    volumen = float(medidas[0]) * float(medidas[1]) * float(medidas[2])

                    ap1 = volumen * 166.67

                else:

                    ap1 = 0

                aplicable = round(ap1, 2) if ap1 > float(c.bruto) else float(c.bruto)

                texto += formatear_linea("Mercadería", c.producto.nombre)

                texto += formatear_linea("Bultos", str(c.bultos))

                texto += formatear_linea("Peso", str(c.bruto))

                texto += formatear_linea("Aplicable", str(aplicable))

            texto += "<br>"

        if gastos_boolean == 'true' and gastos:

            texto += '<p style="font-family: Courier New, monospace; font-size: 12px; line-height: 1;"> Detalle de gastos en Dólares U.S.A </p>'

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
    elif title == 'Liberacion':

        resultado['asunto'] = f'LIBERACIÓN: {row.awb} - seguimiento: {row.numero}'

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        fecha_actual = datetime.now()

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
        texto += formatear_linea("HAWB", row.hawb or "")

        if master_boolean == 'true':
            texto += formatear_linea("AWB", row.awb or "")

        if transportista_boolean == 'true':
            texto += formatear_linea("Transportista", row.transportista or "")

        if conex:
            for i, ruta in enumerate(conex):
                if ruta.llegada:
                    fecha = ruta.llegada.strftime("%d/%m")
                else:
                    fecha = '??/??'
                tramo = f"({ruta.origen}/{ruta.destino})   {ruta.cia}{ruta.viaje}/{fecha}"
                texto += formatear_linea("Vuelo", tramo)

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

        cant_cntr = ImportCargaaerea.objects.filter(numero=row.numero).values(

            'medidas', 'bruto', 'bultos', 'producto'

        ).annotate(total=Count('id'))

        if cant_cntr.exists():

            for cn in cant_cntr:

                if cn['medidas']:

                    medidas = cn['medidas'].split('*')

                    if len(medidas) == 3 and all(m.isdigit() for m in medidas):
                        volumen = float(medidas[0]) * float(medidas[1]) * float(medidas[2])

                bultos += cn['bultos']

                peso += cn['bruto'] if cn['bruto'] else 0

                producto = Productos.objects.get(codigo=int(cn['producto'])).nombre

                mercaderias += producto + ' - '

        texto += formatear_linea("House", row.hawb or "")

        texto += formatear_linea("Peso", f"{peso} KGS",1)

        texto += formatear_linea("Bultos", str(bultos),1)

        texto += formatear_linea("CBM", f"{volumen:.3f} M³",1)

        texto += "<br>"

        texto += formatear_linea("Mercadería", mercaderias.rstrip(' -'))

        texto += formatear_linea("Depósito", seguimiento.deposito or "")

        texto += formatear_linea("Doc. Originales", "SI" if seguimiento.originales else "NO")

        if gastos_boolean == 'true':

            if gastos:

                texto += '<p style="font-family: Courier New, monospace; font-size: 12px; line-height: 1;"> Detalle de gastos en Dólares U.S.A </p>'

                total_gastos = 0

                total_iva = 0

                for g in gastos:

                    servicio = Servicios.objects.get(codigo=g.servicio)

                    total_gastos += float(g.precio) if g.precio != 0 else float(g.costo)

                    iva = True if servicio.tasa == 'B' else False

                    if iva:
                        total_iva += float(g.precio) * 0.22 if g.precio != 0 else float(g.costo) * 0.22

                    if g.precio != 0:
                        texto += formatear_linea(servicio.nombre, f"{g.precio:.2f}", 1)
                    elif g.costo != 0:
                        texto += formatear_linea(servicio.nombre, f"{g.costo:.2f}", 1)
                    else:
                        texto += formatear_linea("Problema con los gastos cargados", 0)

                texto += "<br>"

                texto += formatear_linea("TOTAL DE GASTOS", f"{total_gastos:.2f}", 1)

                texto += formatear_linea("I.V.A", f"{total_iva:.2f}", 1)

                texto += formatear_linea("TOTAL A PAGAR", f"{total_gastos + total_iva:.2f}", 1)

                texto += "<br>"

        texto += "<br>"
        texto += "<table style='border: none; font-family: Courier New, monospace; font-size: 12px; border-collapse: collapse; width: 100%;'>"
        # Fila de títulos (encabezados)
        texto += "<tr>"
        texto += "<th style='padding: 2px 10px; text-align: left;'>Origen</th>"
        texto += "<th style='padding: 2px 10px; text-align: left;'>Destino</th>"
        texto += "<th style='padding: 2px 10px; text-align: left;'>Vuelo</th>"
        texto += "<th style='padding: 2px 10px; text-align: left;'>Viaje</th>"
        texto += "<th style='padding: 2px 10px; text-align: left;'>Salida</th>"
        texto += "<th style='padding: 2px 10px; text-align: left;'>Llegada</th>"
        texto += "</tr>"

        # Fila de valores
        #valor_vuelo = str(row.transportista) if armador !='true' else str(row.armador)
        texto += "<tr>"
        texto += f"<td style='padding: 2px 10px;'>{row.origen or ''}</td>"
        texto += f"<td style='padding: 2px 10px;'>{row.destino or ''}</td>"
        texto += f"<td style='padding: 2px 10px;'>{row.transportista}</td>"
        texto += f"<td style='padding: 2px 10px;'>{str(conex[0].ciavuelo)+str(conex[0].vuelo)}</td>"
        texto += f'<td style="padding: 2px 10px;">{salida}</td>'
        texto += f'<td style="padding: 2px 10px;">{llegada}</td>'
        texto += "</tr>"
        texto += "</table><br>"

        texto += "<pre style='font-family: Courier New, monospace; font-size: 12px;'>"

        texto += "Los vuelos y las llegadas al aeropuerto de Montevideo son siempre a CONFIRMAR, ya que puede haber trasbordos y/o alteraciones en las fechas estimadas de llegada\n"
        texto += "sin previo aviso, por lo cual le sugerimos consultarnos por la fecha de arribo que aparece en este aviso.\n"
        texto += "Agradeciendo vuestra preferencia, le saludamos muy atentamente."
        texto += "</pre>"
        return texto, resultado
    elif title == 'Aviso de desconsolidacion':

        fecha_actual = datetime.now()

        fecha_formateada = fecha_actual.strftime(
            f'{DIAS_SEMANA[fecha_actual.weekday()]}, %d de {MESES[fecha_actual.month - 1]} del %Y')

        resultado['asunto'] = (

            f'AVISO DE DESCONSOLIDACION - Ref.: {row.seguimiento} - CS: {row.numero} - HB/l: {row.hawb} - Ship: {row.embarcador}'


        )
        try:
            consigna=Clientes.objects.get(codigo=row.consignatario_id)
            telefono=consigna.telefono
        except Clientes.DoesNotExist:
            direccion=telefono='S/I'


        texto += formatear_linea("Fecha", fecha_formateada.upper())

        texto += "<br>"

        texto += formatear_linea("Att.", "DEPARTAMENTO DE OPERACIONES")

        texto += formatear_linea("Consignatario", str(row.consignatario))

        texto += formatear_linea("Dirección", row.direccion_consignatario or "")

        texto += formatear_linea("Teléfono", telefono or "")


       # texto += formatear_linea("Vapor", row.vapor or "")  # cambiar esto
        salida = seguimiento.etd.strftime("%d/%m/%Y") if isinstance(seguimiento.etd, datetime) else ""

        llegada = seguimiento.eta.strftime("%d/%m/%Y") if isinstance(seguimiento.eta, datetime) else ""

        texto += formatear_linea("Viaje", conex[0].viaje or "")

        texto += formatear_linea("Llegada", llegada)

        texto += formatear_linea("Posición", row.posicion or "")

        texto += formatear_linea("Seguimiento", row.seguimiento)

        texto += formatear_linea("Embarcador", row.embarcador)

        #texto += formatear_linea("Consignatario", row.consignatario)

        texto += formatear_linea("Orden cliente", seguimiento.refcliente)

        texto += formatear_linea("Referencia proveedor", seguimiento.refproveedor)

        texto += formatear_linea("Origen", row.origen)

        texto += formatear_linea("Destino", row.destino)

        # Datos de contenedores

        cantidad_cntr = ""

        contenedores = ""

        precintos = ""

        movimiento = ""

        mercaderias = ""

        bultos = 0

        peso = 0

        volumen = 0

        cant_cntr = ImportCargaaerea.objects.filter(numero=row.numero).values(

            'bruto', 'medidas', 'bultos','producto__nombre').annotate(total=Count('id'))

        if cant_cntr.count() > 0:

            for cn in cant_cntr:
                bultos += cn['bultos']
                if cn['bruto']:
                    peso += cn['bruto']

                if cn['medidas'] is not None:

                    medidas = cn['medidas'].split('*')

                else:

                    medidas = None

                if medidas and len(medidas) == 3 and all(m.isdigit() for m in medidas):

                    volumen += float(medidas[0]) * float(medidas[1]) * float(medidas[2])

                else:
                    volumen+=0

                mercaderias += f'{cn["producto__nombre"]} - '


        texto += formatear_linea("Bultos", str(bultos))

        texto += formatear_linea("Peso", f"{peso:.2f} KGS")

        texto += formatear_linea("CBM", f"{volumen:.2f} M³")

        texto += formatear_linea("Mercadería", mercaderias.strip(' -'))

        texto += formatear_linea("Depósito", str(seguimiento.deposito))
        texto += formatear_linea("WR", str(embarque.wreceipt))

        texto += "<br>"

        texto += "<b>ATENCION!</b><br><br>"

        texto += "DETALLE DE DESCONSOLIDACION<br><br>"
        return texto,resultado
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
    elif title == 'Notificacion cambio de linea':

        resultado['asunto'] = 'NOTIFICACIÓN CAMBIO DE LÍNEA / NVOCC / CÍA AEREA'

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        fecha_actual = datetime.now()

        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

        texto = ""

        texto += formatear_linea("Fecha", fecha_formateada)

        texto += "<br>"

        texto += "<pre style='font-family: Courier New, monospace; font-size: 12px;'>"

        texto += f"SEG: {row.seguimiento}\n\n"

        texto += "CONFIRMO CAMBIO DE LÍNEA / NVOCC / CÍA AÉREA DE ESTE SEGUIMIENTO\n\n"

        texto += "ANTERIOR:\n"

        texto += f"ACTUAL: {row.transportista}\n\n"

        texto += "OCEANLINK\n"

        texto += "</pre>"

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
#agregar completo
    elif title == 'Shipping instruction':
        #embarcador = Clientes.objects.get(codigo=embarque.embarcador)
        consignatario = Clientes.objects.get(codigo=embarque.consignatario)
        cliente = Clientes.objects.get(codigo=embarque.cliente)
        mercaderia = ImportCargaaerea.objects.filter(numero=row.numero)
        moneda = Monedas.objects.get(codigo=embarque.moneda)

        try:
            if embarque.embarcador:
                proveedor = Clientes.objects.get(codigo=embarque.embarcador)
                direccion = proveedor.direccion
                empresa = proveedor.empresa
                ciudad = proveedor.ciudad
                pais = proveedor.pais
                email = proveedor.emailim
                contactos = proveedor.contactos
            else:
                direccion = empresa = ciudad = pais = email = contactos = ''
        except Clientes.DoesNotExist:
            direccion = empresa = ciudad = pais = email = contactos = ''

        resultado['asunto'] = f'SHIPPING INSTRUCTION - Ref.: {seguimiento.numero} - Shipper: {empresa} - Consignee: {consignatario.empresa}'

        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%A, %B %d, %Y').upper()
        llegada = seguimiento.eta.strftime("%d/%m/%Y") if isinstance(seguimiento.eta, datetime) else ''
        nombre = f"{request.user.first_name} {request.user.last_name}"

        texto = ''
        texto += formatear_linea("Date", fecha_formateada)
        texto += formatear_linea("To", cliente.empresa)
        texto += formatear_linea("Department", "IMPORT AEREO")
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
        texto += formatear_linea("Consignee", consignatario.empresa)
        texto += formatear_linea("Address", consignatario.direccion)
        texto += formatear_linea("Country", consignatario.pais)
        texto += formatear_linea("Tax ID", consignatario.ruc)
        texto += formatear_linea("Phone", consignatario.telefono)

        texto += "<br>"
        texto += formatear_linea("Internal Reference", f"{seguimiento.numero}/{row.numero}")
        texto += formatear_linea("Position", row.posicion)
        texto += formatear_linea("Estimated delivery date", llegada)
        texto += formatear_linea("Airport of origin", embarque.origen)
        texto += formatear_linea("Airport of destination", embarque.destino)

        texto += "<br>"
        for m in mercaderia:
            peso = m.bruto if m.bruto else 0
            if m.medidas is not None:
                medidas = m.medidas.split('*')
            else:
                medidas = None

            if medidas and len(medidas) == 3 and all(m.isdigit() for m in medidas):
                volumen = float(medidas[0]) * float(medidas[1]) * float(medidas[2])
            else:
                volumen = 0
            calculado = volumen * 166.67
            aplicable = peso if peso > calculado else f"{calculado:.2f} AS VOL"

            texto += formatear_linea("Commodity", m.producto)
            texto += formatear_linea("Packages", m.bultos)
            texto += formatear_linea("Weight", f"{peso:.2f} KGS")
            texto += formatear_linea("Volume", f"{volumen:.2f} CBM")
            #texto += formatear_linea("Chargeable weight", aplicable)

        condicion_pago = "Collect" if row.pago_flete == "C" else "Prepaid" if row.pago_flete == "P" else "N/A"
        texto += formatear_linea("Payment terms", condicion_pago)
        texto += formatear_linea("Terms of purchase", row.terminos)
        if transportista_boolean == 'true':
            texto += formatear_linea("Carrier", row.transportista)

        texto += formatear_linea("Transport contract", seguimiento.contratotra)
        texto += formatear_linea("Mode of shipment", "AEREO")
        texto += formatear_linea("Currency", moneda.nombre if moneda is not None else 'S/I')
        texto += "<br>"
        return texto,resultado
    elif title == 'Instruccion de embarque':
        #embarcador = Clientes.objects.get(codigo=embarque.embarcador)
        consignatario = Clientes.objects.get(codigo=embarque.consignatario)
        cliente = Clientes.objects.get(codigo=embarque.cliente)
        mercaderia = ImportCargaaerea.objects.filter(numero=row.numero)
        moneda = Monedas.objects.get(codigo=embarque.moneda)

        try:
            if embarque.embarcador:
                proveedor = Clientes.objects.get(codigo=embarque.embarcador)
                direccion = proveedor.direccion
                empresa = proveedor.empresa
                ciudad = proveedor.ciudad
                pais = proveedor.pais
                email = proveedor.emailim
                contactos = proveedor.contactos
            else:
                direccion = empresa = ciudad = pais = email = contactos = ''
        except Clientes.DoesNotExist:
            direccion = empresa = ciudad = pais = email = contactos = ''

        resultado[
            'asunto'] = f"INSTRUCCIÓN DE EMBARQUE - Ref.: {seguimiento.numero} - Shipper: {empresa} - Consignee: {consignatario.empresa}"

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()
        llegada = seguimiento.eta.strftime("%d/%m/%Y") if isinstance(seguimiento.eta, datetime) else ''
        nombre = f"{request.user.first_name} {request.user.last_name}"

        texto = ''
        texto += formatear_linea("Fecha", fecha_formateada)
        texto += formatear_linea("A", cliente.empresa)
        texto += formatear_linea("Departamento", "IMPORT AÉREO")
        texto += formatear_linea("Envíado", nombre)

        texto += "<br><p style='font-family: Courier New, monospace; font-size: 12px;'>Estimados Sres.:</p><br>"
        texto += "<p style='font-family: Courier New, monospace; font-size: 12px;'>Por favor, contactar a la siguiente compañía para coordinar la operación referenciada:</p><br>"

        texto += formatear_linea("Proveedor", empresa)
        texto += formatear_linea("Dirección", direccion)
        texto += formatear_linea("Ciudad", ciudad)
        texto += formatear_linea("País", pais)
        texto += formatear_linea("E-mail", email)
        texto += formatear_linea("Contactos", contactos)

        texto += "<br>"
        texto += formatear_linea("Consignatario", consignatario.empresa)
        texto += formatear_linea("Dirección", consignatario.direccion)
        texto += formatear_linea("País", consignatario.pais)
        texto += formatear_linea("RUC", consignatario.ruc)
        texto += formatear_linea("Teléfono", consignatario.telefono)

        texto += "<br>"
        texto += formatear_linea("Referencia interna", f"{seguimiento.numero}/{row.numero}")
        texto += formatear_linea("Posición", row.posicion)
        texto += formatear_linea("Recepción estimada de mercadería", llegada)
        texto += formatear_linea("Aeropuerto de origen", embarque.origen)
        texto += formatear_linea("Aeropuerto de destino", embarque.destino)

        texto += "<br>"
        for m in mercaderia:
            peso = m.bruto if m.bruto else 0
            if m.medidas is not None:
                medidas = m.medidas.split('*')
            else:
                medidas = None

            if medidas and len(medidas) == 3 and all(m.isdigit() for m in medidas):
                volumen = float(medidas[0]) * float(medidas[1]) * float(medidas[2])
            else:
                volumen =0
            calculado = volumen * 166.67
            aplicable = peso if peso > calculado else f"{calculado:.2f} AS VOL"

            texto += formatear_linea("Mercadería", m.producto)
            texto += formatear_linea("Bultos", m.bultos)
            texto += formatear_linea("Peso", f"{peso:.2f} KGS")
            texto += formatear_linea("Volumen", f"{volumen:.2f} CBM")
            #texto += formatear_linea("Aplicable", aplicable)

        texto += formatear_linea("Condiciones de pago",
                                 "Collect" if row.pago_flete == "C" else "Prepaid" if row.pago_flete == "P" else "S/I")
        texto += formatear_linea("Términos de compra", row.terminos)
        if transportista_boolean == 'true':
            texto += formatear_linea("Transportista", row.transportista)
        texto += formatear_linea("Contrato transport.", seguimiento.contratotra)
        texto += formatear_linea("Modo de embarque", "AÉREO")
        texto += formatear_linea("Moneda", moneda.nombre if moneda is not None else 'S/I')
        texto += "<br>"
        return texto,resultado



def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data).decode("utf-8")
        return base64_data
