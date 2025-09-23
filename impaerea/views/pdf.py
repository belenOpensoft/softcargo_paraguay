import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from impaerea.models import (VEmbarqueaereo, ImportEmbarqueaereo, ImportCargaaerea, ImportConexaerea)
from impomarit.views.mails import formatear_caratula
from mantenimientos.models import Clientes, Ciudades
from mantenimientos.views.bancos import is_ajax
from seguimientos.models import VGrillaSeguimientos, Envases


@login_required(login_url='/')
def get_datos_caratula(request):
    resultado = {}
    if is_ajax(request):
        try:
            id = request.POST['numero']
            Vembarque = VEmbarqueaereo.objects.get(numero=id)
            embarque = ImportEmbarqueaereo.objects.get(numero=id)
            embarcador = Clientes.objects.get(codigo=embarque.embarcador)
            consignatario = Clientes.objects.get(codigo=embarque.consignatario)
            # ruta = ImportConexaerea.objects.filter(numero=id).order_by('-id').values_list('salida', 'llegada','vuelo','ciavuelo').first()
            #
            # salida, llegada, vuelo, cia = ruta if ruta else (None, None, None, None)

            try:
                seguimiento = VGrillaSeguimientos.objects.get(numero=Vembarque.seguimiento)
            except VGrillaSeguimientos.DoesNotExist:
                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='', deposito='', pago='', vendedor='')

            texto = '<div style="margin: 0px auto 0 auto; font-family: Courier New, monospace; font-size: 11.5px;">'

            # Encabezado: Oceanlink y datos a la derecha
            texto += '''
                       <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                           <div style="text-align: left;">
                               <b><h1 style="margin: 0; font-size: 21px;font-family: Courier New, monospace;">OCEANLINK LTDA.</h1></b>
                           </div>
                           <div style="text-align: right; font-size: 20px; line-height: 1.4; margin-top: 8px; margin-right:20px; max-width: 60%;font-family: Courier New, monospace;">
                               <b>
                                   Seguimiento: {seguimiento}<br>
                                   Posición: {posicion}<br>
                                   Incoterms: {incoterms}
                               </b>
                           </div>
                       </div><br>
                       '''.format(
                seguimiento=seguimiento.numero,
                posicion=Vembarque.posicion or '',
                incoterms=seguimiento.terminos or ''
            )

            texto += '<p style="text-align:right;font-size: 14px; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:20px;">'
            origen = Ciudades.objects.filter(codigo=Vembarque.origen).first()
            destino = Ciudades.objects.filter(codigo=Vembarque.destino).first()
            texto += f'Origen: {origen.nombre or "" if origen else ""}<br>'
            texto += f'Destino:  {destino.nombre or "" if destino else ""}</p><br>'

            # Primer bloque
            texto += formatear_caratula("Master", Vembarque.awb)
            texto += formatear_caratula("House", Vembarque.hawb)
            texto += formatear_caratula("ETA",
                                        Vembarque.eta.strftime('%d/%m/%Y') if isinstance(Vembarque.eta, datetime.datetime) else '?')
            texto += formatear_caratula("ETD",
                                        Vembarque.etd.strftime('%d/%m/%Y') if isinstance(Vembarque.etd, datetime.datetime) else '?')
            vuelos = (
                ImportConexaerea.objects
                .filter(numero=Vembarque.numero)
                .values_list('ciavuelo', 'vuelo')
            )
            if vuelos:
                nombre_vapor = "; ".join([f"{ciavuelo}{vuelo}" for ciavuelo, vuelo in vuelos])
                cia = "; ".join([cia for cia, _ in vuelos])
            else:
                nombre_vapor = "S/I"
                cia = "S/I"

            texto += formatear_caratula("Vuelo", nombre_vapor)
            texto += formatear_caratula("Compañía", cia if cia else 'S/I')
            texto += formatear_caratula("Transportista", Vembarque.transportista)
            texto += formatear_caratula("Orden cliente", seguimiento.refcliente)
            texto += '<br><span style="display: block; border-top: 0.2pt solid #CCC; margin: 2px 0;"></span><br>'

            # Embarcador
            texto += f"<b>Embarcador: {Vembarque.embarcador}</b><br>"
            texto += "<b>Datos del embarcador:</b><br>"
            direccion_embarcador = f"{embarcador.direccion} - {embarcador.ciudad} - {embarcador.pais}"
            texto += formatear_caratula("Empresa", embarcador.empresa)
            texto += formatear_caratula("Dirección", direccion_embarcador)
            texto += formatear_caratula("Ph", embarcador.telefono)
            texto += formatear_caratula("RUT", embarcador.ruc)
            texto += '<br>'

            # Consignatario
            texto += f"<b>Consignatario: {Vembarque.consignatario}</b><br>"
            texto += "<b>Datos del consignatario:</b><br>"
            direccion_consignatario = f"{consignatario.direccion} - {consignatario.ciudad} - {consignatario.pais}"
            texto += formatear_caratula("Empresa", consignatario.empresa)
            texto += formatear_caratula("Dirección", direccion_consignatario)
            texto += formatear_caratula("Ph", consignatario.telefono)
            texto += '<br>'

            texto += f"<b>Agente:</b> {Vembarque.agente}<br>"
            texto += f"<b>Deposito:</b> {seguimiento.deposito}<br><br>"
            texto += '<span style="display: block; border-top: 0.2pt solid #CCC; margin: 2px 0;"></span><br>'

            # Detalle del embarque
            embarque = ImportCargaaerea.objects.filter(numero=id)
            if embarque:
                total_bultos = 0
                total_peso = 0.0
                total_volumen = 0.0
                mercaderias = []
                for e in embarque:
                    total_bultos += e.bultos or 0
                    total_peso += float(e.bruto or 0)
                    volumen = ''
                    if e.medidas is not None:
                        medidas = e.medidas.split('*')
                    else:
                        medidas = None

                    if medidas and len(medidas) == 3 and all(m.isdigit() for m in medidas):
                        volumen = float(medidas[0]) * float(medidas[1]) * float(medidas[2])
                    else:
                        volumen = 0

                    total_volumen += float(volumen or 0)
                    if e.producto:
                        mercaderias.append(e.producto.nombre)

                mercaderias_str = "; ".join(mercaderias)

                texto += formatear_caratula("Nro Bultos", f"{total_bultos}")

                texto += formatear_caratula("Mercadería", mercaderias_str)
                texto += formatear_caratula("Peso", round(total_peso, 2))
                texto += formatear_caratula("Volumen", round(total_volumen, 2))
                texto += '<br><span style="display: block; border-top: 0.2pt solid #CCC; margin: 2px 0;"></span><br>'

            texto += formatear_caratula("Forma de pago", seguimiento.pago)
            texto += formatear_caratula("Vendedor", seguimiento.vendedor)
            texto += '</div>'

            resultado['resultado'] = 'exito'
            resultado['texto'] = texto
        except Exception as e:
            resultado['resultado'] = str(e)
    else:
        resultado['resultado'] = 'Ha ocurrido un error.'
    return HttpResponse(json.dumps(resultado), "application/json")
