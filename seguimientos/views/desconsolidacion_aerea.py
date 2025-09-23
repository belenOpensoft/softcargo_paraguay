import json
from xml.dom import minidom
import re
import simplejson
from datetime import datetime
import base64

import urllib3
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from urllib.request import urlopen
from cargosystem import settings
from impaerea.models import ImportConexaerea, VEmbarqueaereo, ImportEmbarqueaereo, ImportCargaaerea, ImportReservas
from mantenimientos.forms import desconsolidacion_form
from mantenimientos.models import Clientes, Productos
from seguimientos.models import VGrillaSeguimientos, Conexaerea, Envases
from urllib.request import Request, urlopen

from seguimientos.views import seguimientos


def desconsolidacion_aerea(request):
    try:
        if not getattr(settings, "DESCONSOLIDACION_AEREA"):
            messages.error(request, "La funcionalidad de Desconsolidación Aérea está deshabilitada.")
            return HttpResponseRedirect("/")

        if request.user.has_perms(["seguimientos.add_", ]):
            ctx = {'form': desconsolidacion_form(), 'title_page': 'Desconsolidacion de importacion aerea'}
            if request.method == 'POST':
                form = desconsolidacion_form(request.POST)
                if form.is_valid():
                    resultado = {}
                    cia = form.cleaned_data['cia']
                    vuelo = form.cleaned_data['numero_vuelo']
                    llegada = form.cleaned_data['llegada']
                    registros = ImportConexaerea.objects.filter(vuelo=vuelo, llegada=str(llegada), ciavuelo=cia)
                    print(registros.query)
                    if registros.count() > 0:
                        for reg in registros:
                            embarque=ImportEmbarqueaereo.objects.get(numero=reg.numero)
                            reg_with_details = {
                                'id':reg.id,
                                'numero': embarque.numero,
                                'reg': reg,
                                'hawb': embarque.hawb,  # Hawb de ImportEmbarqueaereo
                                'awb': embarque.awb,  # Awb de ImportEmbarqueaereo
                                'origen': reg.origen,
                                'alta_baja':"B" if embarque.envioaduana == 'S' else "A"
                            }

                            # Usamos reg.numero como clave para agregar el diccionario completo
                            resultado[reg.numero] = reg_with_details
                        ctx['datos'] = resultado
                        ctx['form'] = desconsolidacion_form(request.POST)
                    else:
                        ctx['form'] = desconsolidacion_form(request.POST)
                        messages.info(request, 'No se encontraron resultados para la busqueda')
            return render(request, "seguimientos/desconsolidacion.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/desconsolidacion_aerea")

@csrf_exempt
def desconsolidar_aereo(request):
    resultado = {}
    try:
        data = simplejson.loads(request.GET['data'])
        url = settings.URL_DESCONSOLIDACION
        username = 'Oceanlink'
        password = 'ocean99'
        codigo_exito = 00 #probar
        respuestas = {}
        if get_status(url, username, password):
            for d in data:
                seg = ImportEmbarqueaereo.objects.get(numero=d[1])
                res = ImportReservas.objects.get(awb=seg.awb)
                con = ImportConexaerea.objects.get(id=d[0])
                select_html = d[5]
                match = re.search(r'<option value="([A-B])" selected.*?>', select_html)
                if match:
                    alta_baja = match.group(1)
                else:
                    alta_baja = None

                data = genero_xml_desconsolidacion(seg, con, alta_baja,res)
                # if data['Codigo'] == codigo_exito:
                #         embarque=ImportEmbarqueaereo()
                #         embarque.envioaduana='S'
                #         embarque.save()

                respuestas[d[1]] = envio_msj(url, data, username, password)

        else:
            resultado['resultado'] = 'Servicio no disponible'


        resultado['resultado'] = True
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

@csrf_exempt
def genero_xml_desconsolidacion(seg, con, alta_baja,res):
    try:
        tipo_documento = "4"
        id_documento = "216803670019" #verificar si este es el rut de oceanlink
        fecha_hora_documento = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        nro_transaccion = "CARX0000004521"
        manifiesto_numero = res.manifiesto
        recinto = "2089" #ver cual poner
        fecha_arribo = con.llegada.strftime("%Y%m%d")
        master = seg.awb
        transportista = Clientes.objects.filter(codigo=seg.transportista)
        consignatario = Clientes.objects.filter(codigo=seg.consignatario)
        rut_transportista = transportista[0].ruc
        rut_consignatario = consignatario[0].ruc
        agente = Clientes.objects.filter(codigo=seg.agente)
        """ DATOS A CONSULTAR """
        if agente[0].emailia is not None and agente[0].emailia != 'S/I':
            email_agente = agente[0].emailia
        else:
            email_agente = ''
        direccion_consignatario = consignatario[0].direccion
        nombre_consignatario = consignatario[0].empresa
        origen = con.origen
        destino = con.destino
        envases = ImportCargaaerea.objects.filter(numero=seg.numero).values('tipo', 'bultos', 'bruto', 'medidas','producto').annotate(total=Count('id'))
        volumen = 0
        lineas = '<Lineas>'
        if envases.count() > 0:
            linea = 1
            envase = ''
            peso = ''
            volumen=''
            for cn in envases:
                cant_bulto = cn['bultos']
                if cn['bruto'] is not None:
                    peso = cn['bruto']
                if cn['medidas'] is not None and cn['medidas'] !='S/I' and cn['medidas'] !='' :
                    params = cn['medidas'].split('*')
                    value = float(params[0]) * float(params[1]) * float(params[2])
                    volumen += value
                if cn['tipo'] is not None:
                    envase = cn['tipo']
                    try:
                        prod_nombre = Productos.objects.filter(codigo=cn['producto']).values_list('nombre',flat=True).first()
                    except Productos.DoesNotExist:
                        prod_nombre = None

                lineas += f'''
                            <Linea>
                                <LineaNumero>{linea}</LineaNumero>
                                <RegistroTipo>{alta_baja}</RegistroTipo>
                                <PesoBruto>{peso}</PesoBruto>
                                <BultoTipo>{envase}</BultoTipo>
                                <BultoCantidad>{cant_bulto}</BultoCantidad>
                                <Marcas/>
                                <MercaderiaDescripcion>{prod_nombre}</MercaderiaDescripcion>
                                <DepositoFinalCodigo/>
                                <MercaderiaPeligrosaCodigo/>
                                <OperacionTipo/>
                                <ContenedoresLinea/>
                                <PartidasLinea/>
                                <Asociaciones/>
                            </Linea>
                        </Lineas>'''
                linea += 1
        lineas += '</Lineas>'

        num_conocimiento = seg.awb #mirar si el conocimiento de embarque es el master o es un compuesto
        #BL
        num_sec_conocimiento = res.numero #traer de reserva
        vuelo = con.vuelo
        xml_str = f'''<?xml version = "1.0" encoding = "ISO-8859-1"?>
        <DAE xmlns="http://www.aduanas.gub.uy/LUCIA/DAE">
            <TipoDocumento>{tipo_documento}</TipoDocumento>
            <IdDocumento>{id_documento}</IdDocumento>
            <FechaHoraDocumentoElectronico>{fecha_hora_documento}</FechaHoraDocumentoElectronico>
            <CodigoIntercambio>WS_MANIFIESTO</CodigoIntercambio>
            <NroTransaccion>{nro_transaccion}</NroTransaccion>
            <Objeto>
                <Manifiestos>
                    <Manifiesto>
                        <TransporteTipo>4</TransporteTipo>
                        <ManifiestoTipo>0</ManifiestoTipo>
                        <ManifiestoNumero>{manifiesto_numero}</ManifiestoNumero>
                        <Recinto>{recinto}</Recinto>
                        <FechaArribo>{fecha_arribo}</FechaArribo>
                        <AgenteTransportistaTipoDocumento>4</AgenteTransportistaTipoDocumento>
                        <AgenteTransportistaDocumento>{rut_transportista}</AgenteTransportistaDocumento>
                        <LugarPartidaCodigo>{origen}</LugarPartidaCodigo>
                        <LugarDestinoCodigo>{destino}</LugarDestinoCodigo>
                        <UltimoPuerto>{destino}</UltimoPuerto>
                        <MedioTransporteMatricula>CXCR54</MedioTransporteMatricula>
                        <MedioTransporteNacionalidad>805</MedioTransporteNacionalidad>
                        <Observacion/>
                        <MedioTransporteNombre>AVION</MedioTransporteNombre>
                        <Conocimientos>
                            <Conocimiento>
                                <ConocimientoNumeroSecuencial>{num_sec_conocimiento}</ConocimientoNumeroSecuencial>
                                <ConocimientoOriginalNumero>{num_conocimiento}</ConocimientoOriginalNumero>
                                <PuertoEmbarque>{origen}</PuertoEmbarque>
                                <RegistroTipo>A</RegistroTipo>
                                <OperacionTipo/>
                                <ConocimientoTipo>HWB</ConocimientoTipo>
                                <ConocimientoMasterNumero>{master}</ConocimientoMasterNumero>
                                <PuertoDescarga>{destino}</PuertoDescarga>
                                <ConsignatarioTipoDocumento>4</ConsignatarioTipoDocumento>
                                <ConsignatarioDocumento>{rut_consignatario}</ConsignatarioDocumento>
                                <MercaderiaDestino>{destino}</MercaderiaDestino>
                                <RemitenteTipoDocumento>4</RemitenteTipoDocumento>
                                <RemitenteDocumento>{rut_consignatario}</RemitenteDocumento>
                                <RemitenteNombre>{nombre_consignatario}</RemitenteNombre>
                                <RemitenteDireccion>{direccion_consignatario}</RemitenteDireccion>
                                <CargaCubica>{volumen}</CargaCubica>
                                <NotificarTipoDocumento>4</NotificarTipoDocumento>
                                <NotificarDocumento>{rut_consignatario}</NotificarDocumento>
                                <NotificarNombre>{nombre_consignatario}</NotificarNombre>
                                <NotificarDireccion>{direccion_consignatario}</NotificarDireccion>
                                <NotificarTelefono/>
                                <ALaOrden>N</ALaOrden>
                                <FormaPago>C</FormaPago>
                                <AgenteConocimientoMail>{email_agente}</AgenteConocimientoMail>
                                <Trasbordo>N</Trasbordo>
                                <Liberado/>
                                <PuertoOrigen>{origen}</PuertoOrigen>
                                <ConsignatarioPais>858</ConsignatarioPais>
                                <GuiaDirecta/>
                                {lineas}
                            </Conocimiento>
                        </Conocimientos>
                        <Contenedores/>
                        <Imagenes/>
                    </Manifiesto>
                </Manifiestos>
            </Objeto>
        </DAE>'''
        print(xml_str)
        return xml_str
    except Exception as e:
        raise TypeError(e)

def envio_msj(url, datos, usuario, contrasena):
    try:
        # Asegurarse de que los datos estén en formato bytes
        if isinstance(datos, str):
            datos = datos.encode('ISO-8859-1')

        # Crear el encabezado de autorización Basic
        auth_value = f'{usuario}:{contrasena}'
        auth_value = base64.b64encode(auth_value.encode()).decode('utf-8')
        headers = {
            'Authorization': f'Basic {auth_value}',
            'Content-Type': 'application/xml'
        }

        # Crear la solicitud con los encabezados
        req = Request(url, data=datos, headers=headers)
        s = urlopen(req)
        sl = s.read()
        # resp = str(sl)[2:].replace('\\r\\n', '')
        xml_str = sl.decode('ISO-8859-1')
        xml_doc = minidom.parseString(xml_str)
        print(xml_str)

        # Ejemplo de cómo acceder a los elementos del XML
        # Obtén el primer nodo (ejemplo: <response>)
        root = xml_doc.documentElement

        # Accede a un nodo específico (ejemplo: <status>)
        status_nodes = root.getElementsByTagName('status')
        if status_nodes:
            status = status_nodes[0].firstChild.nodeValue
            print(f'Status: {status}')

        # Si quieres obtener todos los nodos, puedes hacer algo como:
        all_nodes = root.getElementsByTagName('*')
        respuesta = {}
        for node in all_nodes:
            respuesta[node.tagName] = node.firstChild.nodeValue
        return respuesta
    except Exception as e:
        raise TypeError(e)

def get_status_old(url, usuario, contrasena):
    try:
        datos = """<?xml version = "1.0" encoding = "ISO-8859-1"?>
            <DAE xmlns="http://www.aduanas.gub.uy/LUCIA/DAE">
                <TipoDocumento>4</TipoDocumento>
                <IdDocumento>213971080016</IdDocumento> 
                <FechaHoraDocumentoElectronico></FechaHoraDocumentoElectronico>
                <CodigoIntercambio>WS_MANIFIESTO</CodigoIntercambio>
                <NroTransaccion></NroTransaccion>
                <Objeto>
                </Objeto>
            </DAE>
        """
        print(datos)
        # Crear el encabezado de autorización Basic
        auth_value = f'{usuario}:{contrasena}'
        auth_value = base64.b64encode(auth_value.encode()).decode('utf-8')
        headers = {
            'Authorization': f'Basic {auth_value}'
        }
        if isinstance(datos, str):
            datos = datos.encode('utf-8')
        # Crear la solicitud con los encabezados
        req = Request(url, data=datos, headers=headers)
        s = urlopen(req)
        sl = s.read()
        # resp = str(sl)[2:].replace('\\r\\n', '')
        xml_str = sl.decode('ISO-8859-1')
        xml_doc = minidom.parseString(xml_str)

        # Ejemplo de cómo acceder a los elementos del XML
        # Obtén el primer nodo (ejemplo: <response>)
        root = xml_doc.documentElement

        # Accede a un nodo específico (ejemplo: <status>)
        status_nodes = root.getElementsByTagName('status')
        if status_nodes:
            status = status_nodes[0].firstChild.nodeValue
            print(f'Status: {status}')

        # Si quieres obtener todos los nodos, puedes hacer algo como:
        all_nodes = root.getElementsByTagName('*')
        respuesta = {}
        for node in all_nodes:
            respuesta[node.tagName] = node.firstChild.nodeValue
        if 'Codigo' in respuesta:
            return True
        else:
            return False
    except Exception as e:
        return False

def get_status(url, usuario, contrasena):
    try:
        xml_test = """<?xml version="1.0" encoding="ISO-8859-1"?>
        <DAE xmlns="http://www.aduanas.gub.uy/LUCIA/DAE">
            <TipoDocumento>4</TipoDocumento>
            <IdDocumento>213971080016</IdDocumento> 
            <CodigoIntercambio>WS_MANIFIESTO</CodigoIntercambio>
        </DAE>"""

        auth_value = f'{usuario}:{contrasena}'
        auth_value = base64.b64encode(auth_value.encode()).decode('utf-8')
        headers = {
            'Authorization': f'Basic {auth_value}',
            'Content-Type': 'application/xml'
        }

        req = Request(url, data=xml_test.encode('ISO-8859-1'), headers=headers, method='POST')
        response = urlopen(req)
        print(f"Respuesta del servidor: {response.read().decode('ISO-8859-1')}")
        return True
    except Exception as e:
        print(f"Error al enviar el XML: {e}")
        raise TypeError(e)
