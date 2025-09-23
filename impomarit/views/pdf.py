import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from impomarit.models import VEmbarqueaereo, Embarqueaereo, Cargaaerea, Conexaerea, Envases
from impomarit.views.mails import formatear_caratula
from mantenimientos.models import Clientes, Vapores, Ciudades
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

            texto += formatear_caratula("Master", Vembarque.awb)
            texto += formatear_caratula("House", Vembarque.hawb)
            texto += formatear_caratula("ETA",
                                        Vembarque.eta.strftime('%d/%m/%Y') if isinstance(Vembarque.eta, datetime.datetime) else '?')
            texto += formatear_caratula("ETD",
                                        Vembarque.etd.strftime('%d/%m/%Y') if isinstance(Vembarque.etd, datetime.datetime) else '?')

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

            if embarque_items:
                total_bultos = 0
                total_peso = 0.0
                total_volumen = 0.0
                mercaderias = []
                tipo = None  # guardo el último tipo de bulto (si querés acumular todos, se puede)

                for e in embarque_items:
                    total_bultos += e.bultos or 0
                    total_peso += float(e.bruto or 0)
                    total_volumen += float(e.cbm or 0)
                    tipo = e.tipo  # me quedo con el último tipo (o podés concatenar todos)
                    if e.producto:
                        mercaderias.append(e.producto.nombre)

                mercaderias_str = "; ".join(mercaderias)

                # Totales
                if movimiento is not None and movimiento == 'LCL/LCL':
                    texto += formatear_caratula("Nro Bultos", f"{total_bultos} {tipo or ''}")
                else:
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
