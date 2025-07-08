import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from expterrestre.models import (VEmbarqueaereo, ExpterraEmbarqueaereo, ExpterraCargaaerea, ExpterraConexaerea)
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
            embarque = ExpterraEmbarqueaereo.objects.get(numero=id)
            embarcador = Clientes.objects.get(codigo=embarque.embarcador)
            consignatario = Clientes.objects.get(codigo=embarque.consignatario)
            ruta = ExpterraConexaerea.objects.filter(numero=id).order_by('-id').values_list('salida', 'llegada').first()

            if ruta:
                salida, llegada = ruta
            else:
                salida = None
                llegada = None
            try:
                seguimiento = VGrillaSeguimientos.objects.get(numero=Vembarque.seguimiento)
            except VGrillaSeguimientos.DoesNotExist:
                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='',deposito='', pago='', vendedor='')
            # Añadir un contenedor con ancho máximo
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
            texto += f'Origen: {origen.nombre or ""}<br>'
            texto += f'Destino:  {destino.nombre or ""}</p><br>'

            texto += formatear_caratula("Master", Vembarque.awb)
            texto += formatear_caratula("House", Vembarque.hawb)
            texto += formatear_caratula("ETA",
                                        Vembarque.eta.strftime('%d/%m/%Y') if isinstance(Vembarque.eta, datetime.datetime) else '?')
            texto += formatear_caratula("ETD",
                                        Vembarque.etd.strftime('%d/%m/%Y') if isinstance(Vembarque.etd, datetime.datetime) else '?')


            texto += formatear_caratula("Transportista", Vembarque.transportista)
            texto += formatear_caratula("Orden cliente", seguimiento.refcliente)
            texto += '<br><span style="display: block; border-top: 0.2pt solid #CCC; margin: 2px 0;"></span><br>'

            texto += f"<b>Embarcador: {Vembarque.embarcador}</b><br>"
            texto += "<b>Datos del embarcador:</b><br>"
            direccion_embarcador = f"{embarcador.direccion} - {embarcador.ciudad} - {embarcador.pais}"
            texto += formatear_caratula("Empresa", embarcador.empresa)
            texto += formatear_caratula("Dirección", direccion_embarcador)
            texto += formatear_caratula("Ph", embarcador.telefono)
            texto += formatear_caratula("RUT", embarcador.ruc)
            texto += '<br>'

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
            movimiento = None

            # Detalle del embarque - envases
            envase = Envases.objects.filter(numero=id)
            if envase.exists():
                for registro in envase:
                    texto += (
                        f"{int(registro.cantidad or 0)}x{registro.unidad.upper() if registro.unidad else ''} {registro.movimiento if registro.movimiento else 'S/I'} "
                        f"{registro.tipo.upper() if registro.tipo else ''} "
                        f"CTER: {registro.nrocontenedor or ''} SEAL: {registro.precinto or ''} "
                        f"WT: {registro.peso:.3f}" if registro.peso is not None else "WT: S/I"
                    )
                    texto += " "
                    texto += (
                        f"VOL: {registro.volumen:.3f}<br>" if registro.volumen is not None else "VOL: S/I<br>"
                    )
                    movimiento = registro.movimiento

            # Detalle de la mercadería
            embarque_items = ExpterraCargaaerea.objects.filter(numero=id)
            for e in embarque_items:
                texto += formatear_caratula("Nro Bultos",
                                            f"{e.bultos} {e.tipo}") if movimiento is not None and movimiento == 'LCL/LCL' else formatear_caratula(
                    "Nro Bultos", f"{e.bultos}")
                texto += formatear_caratula("Mercadería", e.producto.nombre if e.producto else '')
                texto += '<br>'
                texto += formatear_caratula("Peso", round(float(e.bruto or 0),2))
                texto += formatear_caratula("Volumen", round(float(e.cbm or 0),2))
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

