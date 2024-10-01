from datetime import datetime
import json
from django.http import HttpResponse
import base64
from django.views.decorators.csrf import csrf_exempt
from impomarit.models import VEmbarqueaereo, Cargaaerea, Envases
from mantenimientos.views.bancos import is_ajax
from mantenimientos.models import Productos

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
# @login_required(login_url='/')
def get_data_email_op(request):
    resultado = {}
    if is_ajax(request):
        try:
            title = request.POST['title']
            row_number = 9155 #request.POST['row_number']
            row = VEmbarqueaereo.objects.get(numero=row_number)
            row2 = Cargaaerea.objects.get(numero=row_number)
            row3 = Envases.objects.get(numero=row_number)
            texto = ''
            # image_path = str(settings.BASE_DIR) +  "/cargosystem/static/images/oceanlink.png"  # Cambia esto a la ruta de tu imagen
            # base64_string = image_to_base64(image_path)
            # texto += f'<img src="data:image/jpeg;base64,{base64_string}" alt="Imagen Base64">' + '<br><br><br><br>'
            texto += f'<br>'
            texto, resultado = get_data_html(row_number, row, row2, row3, title, texto, resultado)
            texto += '<b>OCEANLINK,</b><br>'
            # texto += str(request.user.first_name) + ' ' + str(request.user.last_name) + ' <br>'
            texto += 'DEPARTAMENTO DE IMPORTACION MARITIMA, <br>'
            texto += 'MISIONES 1574 OF 201 <br>'
            texto += 'OPERACIONES <br>'
            texto += 'EMAIL: <br>'
            texto += 'TEL: 598 2917 0501 <br>'
            texto += 'FAX: 598 2916 8215 <br><br><br><br>'
            texto += '</table>'
            resultado['resultado'] = 'exito'
            resultado['mensaje'] = texto
        except Exception as e:
            resultado['resultado'] = str(e)
    else:
        resultado['resultado'] = 'Ha ocurrido un error.'
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def get_data_html(row_number, row, row2, row3, title, texto, resultado):
    merca = Productos.objects.get(codigo=row2.producto)
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

        campos = [
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
            ("Nro. Contenedor: ", str(row3.nrocontenedor) if row3.nrocontenedor is not None else "S/I"),
            ("Bultos: ", str(row2.bultos) if row2.bultos is not None else "S/I"),
            ("Peso: ", str(row2.bruto) if row2.bruto is not None else "S/I"),
            ("Mercadería: ", str(merca) if merca is not None else "S/I"),
        ]

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

        campos = [
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
            #("Depósito: ", str() if  is not None else "S/I"),
            ("Mercadería: ", str(merca) if merca is not None else "S/I"),
            ("Bultos: ", str(row2.bultos) if row2.bultos is not None else "S/I"),
            ("Peso: ", str(row2.bruto) if row2.bruto is not None else "S/I"),
            ("CBM: ", f"{row2.cbm:.4f}" if row2.cbm is not None else "S/I"),
            ("Nro. Contenedor: ", str(row3.nrocontenedor) if row3.nrocontenedor is not None else "S/I"),
            ("Precintos: ", str(row3.precinto) if row3.precinto is not None else "S/I"),
        ]

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
        campos5 = [
            ("Mercadería: ", str(merca) if merca is not None else "S/I"),
            ("Bultos: ", str(row2.bultos) if row2.bultos is not None else "S/I"),
            ("Peso: ", str(row2.bruto) if row2.bruto is not None else "S/I"),
            ("Condiciones de pago: ", str(row.pago_flete) if row.pago_flete is not None else "S/I"),
            ("Términos de compra: ", str(row.terminos) if row.terminos is not None else "S/I"),
            ("Modo de embarque: ", "MARITIMO"),
        ]

        for campo, valor in campos5:
            tabla_html5 += f"<tr><th align='left'>{campo}</th><td>{valor}</td></tr>"

        tabla_html5 += "</table> <br><br>"
        texto += tabla_html5

        return texto, resultado


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data).decode("utf-8")
        return base64_data
