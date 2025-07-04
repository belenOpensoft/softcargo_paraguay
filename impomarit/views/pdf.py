import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from impomarit.models import VEmbarqueaereo, Embarqueaereo, Cargaaerea, Conexaerea, Envases
from impomarit.views.mails import formatear_caratula
from mantenimientos.models import Clientes, Vapores
from mantenimientos.views.bancos import is_ajax
from seguimientos.models import VGrillaSeguimientos


@login_required(login_url='/')
def get_datos_caratula(request):
    resultado = {}
    if is_ajax(request):
        try:
            id = request.POST['numero']
            Vembarque = VEmbarqueaereo.objects.get(numero=id)
            embarque = Embarqueaereo.objects.get(numero=id)
            embarcador = Clientes.objects.get(codigo=embarque.embarcador)
            consignatario = Clientes.objects.get(codigo=embarque.consignatario)
            ruta = Conexaerea.objects.filter(numero=id).order_by('-id').values_list('salida', 'llegada').first()

            salida, llegada = ruta if ruta else (None, None)

            try:
                seguimiento = VGrillaSeguimientos.objects.get(numero=Vembarque.seguimiento)
            except VGrillaSeguimientos.DoesNotExist:
                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='', deposito='', pago='', vendedor='')

            texto = '<div style="margin: 0 auto; font-family: Courier New, monospace; font-size: 11.5px;">'
            texto += '<h2 style="text-align: left;">OCEANLINK LTDA.</h2>'
            texto += '<b><p style="font-size:17px;text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto += f'Seguimiento: {seguimiento.numero}<br>'
            texto += f'Posicion:  {Vembarque.posicion}<br>'
            texto += f'Incoterms: {seguimiento.terminos}</p></b>'
            texto += '<p style="text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto += f'Origen: {Vembarque.origen}<br>'
            texto += f'Destino:  {Vembarque.destino}</p><br>'

            texto += formatear_caratula("Master", Vembarque.awb)
            texto += formatear_caratula("House", Vembarque.hawb)
            texto += formatear_caratula("ETA", llegada.strftime('%d-%m-%Y') if isinstance(llegada, datetime.datetime) else '?')
            texto += formatear_caratula("ETD", salida.strftime('%d-%m-%Y') if isinstance(salida, datetime.datetime) else '?')

            if isinstance(embarque.vapor, int) or (isinstance(embarque.vapor, str) and embarque.vapor.isdigit()):
                vapor_obj = Vapores.objects.filter(codigo=int(embarque.vapor)).first()
                nombre_vapor = vapor_obj.nombre if vapor_obj else 'S/I'
            else:
                nombre_vapor = embarque.vapor if embarque.vapor is not None else 'S/I'

            texto += formatear_caratula("Vapor", nombre_vapor)
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
                    movimiento=registro.movimiento

            # Detalle de la mercadería
            embarque_items = Cargaaerea.objects.filter(numero=id)
            for e in embarque_items:
                texto += formatear_caratula("Nro Bultos", f"{e.bultos} {e.tipo}") if movimiento is not None and movimiento == 'LCL/LCL' else formatear_caratula("Nro Bultos", f"{e.bultos}")
                texto += formatear_caratula("Mercadería", e.producto.nombre if e.producto else '')
                texto += '<br>'
                texto += formatear_caratula("Peso", e.bruto)
                texto += formatear_caratula("Volumen", e.cbm)
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
