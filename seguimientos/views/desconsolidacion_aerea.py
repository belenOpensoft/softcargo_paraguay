import json
import simplejson
from datetime import datetime
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from urllib.request import urlopen
from mantenimientos.forms import desconsolidacion_form
from mantenimientos.models import Clientes
from seguimientos.models import VGrillaSeguimientos, Conexaerea, Envases
from cargosystem.webservice import enviar_xml


def desconsolidacion_aerea(request):
    try:
        if request.user.has_perms(["seguimientos.add_", ]):
            ctx = {'form': desconsolidacion_form(),'title_page': 'Desconsolidacion de importación aérea'}
            if request.method == 'POST':
                form = desconsolidacion_form(request.POST)
                if form.is_valid():
                    resultado = {}
                    cia = form.cleaned_data['cia']
                    vuelo = form.cleaned_data['numero_vuelo']
                    llegada = form.cleaned_data['llegada']
                    registros = Conexaerea.objects.filter(viaje=vuelo,llegada=str(llegada),cia=cia)
                    print(registros.query)
                    if registros.count() > 0:
                        for reg in registros:
                            resultado[reg.numero] = reg
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
        for d in data:
            print(d[0])
            seg = VGrillaSeguimientos.objects.get(numero=d[1])
            con = Conexaerea.objects.get(id=d[0])
            aux = genero_xml_desconsolidacion(seg, con)
        resultado['resultado'] = aux
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


@csrf_exempt
def genero_xml_desconsolidacion(seg, con):
    tipo_documento = "4"
    id_documento = "216803670019"
    fecha_hora_documento = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    nro_transaccion = "CARX0000004521"
    manifiesto_numero = "VZ0104"
    recinto = "2089"
    fecha_arribo = con.llegada.strftime("%Y%m%d")
    master = seg.awb
    # Agregar más variables según sea necesario
    transportista = Clientes.objects.filter(codigo=seg.transportista_codigo)
    consignatario = Clientes.objects.filter(codigo=seg.consignatario_codigo)
    rut_transportista = transportista[0].ruc
    rut_consignatario = consignatario[0].ruc
    agente = Clientes.objects.filter(codigo=seg.agente_codigo)
    """ DATOS A CONSULTAR """
    if agente[0].emailia is not None and agente[0].emailia != 'S/I':
        email_agente = agente[0].emailia
    else:
        email_agente = ''
    direccion_consignatario = consignatario[0].direccion
    nombre_consignatario = consignatario[0].razonsocial
    origen = con.origen
    destino = con.destino

    # Obtener datos de los contenedores y calcular los valores
    envases = Envases.objects.filter(numero=seg.numero).values('tipo','bultos', 'peso', 'envase', 'volumen').annotate(total=Count('id'))
    volumen = 0
    lineas = '<Lineas>'
    if envases.count() > 0:
        linea = 1
        envase = ''
        peso = ''
        for cn in envases:
            cant_bulto = cn['bultos']
            if cn['peso'] is not None:
                peso = cn['peso']
            if cn['volumen'] is not None:
                volumen += cn['volumen']
            if cn['envase'] is not None:
                envase = cn['envase']
            mercaderia = cn['envase']
            lineas += f'''
                        <Linea>
                            <LineaNumero>{linea}</LineaNumero>
                            <RegistroTipo>A</RegistroTipo>
                            <PesoBruto>{peso}</PesoBruto>
                            <BultoTipo>{envase}</BultoTipo>
                            <BultoCantidad>{cant_bulto}</BultoCantidad>
                            <Marcas/>
                            <MercaderiaDescripcion>{mercaderia}</MercaderiaDescripcion>
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

    num_conocimiento = '08713'
    #BL
    num_sec_conocimiento = 136
    vuelo = 'VZ0104'
    # Construir el XML como una cadena de texto
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
                    <MedioTransporteMatricula>CXCAR</MedioTransporteMatricula>
                    <MedioTransporteNacionalidad>032</MedioTransporteNacionalidad>
                    <Observacion/>
                    <MedioTransporteNombre>{vuelo}</MedioTransporteNombre>
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
                            <AgenteConocimientoMail>{ email_agente }</AgenteConocimientoMail>
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

    result = enviar_xml(xml_str)

    return HttpResponse(result)


def envioMsj(url, datos):
    try:
        s = urlopen(url, datos)
        sl = s.read()
        return str(sl)[2:].replace('\\r\\n', '')
    except Exception as e:
        raise TypeError(e)
