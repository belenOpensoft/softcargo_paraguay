import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from impomarit.models import VEmbarqueaereo, Embarqueaereo, Cargaaerea
from expmarit.models import VEmbarqueaereo, ExpmaritCargaaerea, ExpmaritEnvases, ExpmaritEmbarqueaereo, \
    ExpmaritConexaerea
from impomarit.views.mails import formatear_caratula
from mantenimientos.models import Clientes, Vapores
from mantenimientos.views.bancos import is_ajax
from seguimientos.models import VGrillaSeguimientos


@login_required(login_url='/')
def get_datos_caratula_old(request):
    resultado = {}
    if is_ajax(request):
        try:
            id = request.POST['numero']
            Vembarque = VEmbarqueaereo.objects.get(numero=id)
            embarque = ExpmaritEmbarqueaereo.objects.get(numero=id)
            embarcador = Clientes.objects.get(codigo=embarque.embarcador)
            consignatario = Clientes.objects.get(codigo=embarque.consignatario)
            ruta = ExpmaritConexaerea.objects.filter(numero=id).order_by('-id').values_list('salida', 'llegada').first()

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
            texto = '<div style="margin: 0 auto; font-family: Courier New, Courier, monospace; font-size: 12px;">'
            texto = texto + '<h2 style="text-align: left;">OCEANLINK LTDA.</h2>'
            # Ajustar el texto que se cortaba
            texto = texto + '<b><p style="font-size:20px;text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto = texto + 'Seguimiento: ' + str(seguimiento.numero if seguimiento.numero is not None else '') + '<br>'
            texto = texto + 'Posicion:  ' + str(Vembarque.posicion if Vembarque.posicion is not None else '') + '<br>'
            texto = texto + 'Incoterms: ' + str(seguimiento.terminos if seguimiento.terminos is not None else '') + '</p></b>'
            texto = texto + '<p style="text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto = texto + 'Origen: ' + str(Vembarque.origen if Vembarque.origen is not None else '') + '<br>'
            texto = texto + 'Destino:  ' + str(Vembarque.destino if Vembarque.destino is not None else '') + '</p><br>'
            texto = texto + '<b>Master: </b>' + str(Vembarque.awb if Vembarque.awb is not None else '') + '<br>'
            texto = texto + '<b>House: </b>' + str(Vembarque.hawb if Vembarque.hawb is not None else '') + '<br>'
            if isinstance(llegada, datetime.datetime):
                res = llegada.strftime('%d-%m-%Y')
            else:
                res = '?'
            texto = texto + '<b>ETA: </b>'+str(res)+'<br>'
            if isinstance(salida, datetime.datetime):
                res = salida.strftime('%d-%m-%Y')
            else:
                res = '?'

            if isinstance(embarque.vapor, int) or (isinstance(embarque.vapor, str) and embarque.vapor.isdigit()):
                vapor_obj = Vapores.objects.filter(codigo=int(embarque.vapor)).first()
                nombre_vapor = vapor_obj.nombre if vapor_obj else 'S/I'
            else:
                nombre_vapor = embarque.vapor if embarque.vapor is not None else 'S/I'

            texto = texto + '<b>ETD: </b>'+str(res)+'<br>'
            texto = texto + '<b>Vapor: </b>'+str(nombre_vapor)+'<br>'
            texto = texto + '<b>Transportista: </b>'+str(Vembarque.transportista if Vembarque.transportista is not None else '')+'<br>'
            texto = texto + '<b>Orden cliente: </b>'+str(seguimiento.refcliente if seguimiento.refcliente is not None else '')+''
            texto = texto + '<b>Embarcador: </b>'+str(Vembarque.embarcador if Vembarque.embarcador is not None else '')+'<br>'
            texto = texto + '<b>Datos del embarcador: </b><br>'
            texto = texto + '<b>Dirección: </b>' +str(embarcador.direccion if embarcador.direccion is not None else '')+' -'+str(embarcador.ciudad if embarcador.ciudad is not None else '')+'-'+str(embarcador.pais if embarcador.pais is not None else '')+'<br>'
            texto = texto + '<b>RUT: </b>' + str(embarcador.ruc if embarcador.ruc is not None else '') + '<br>'
            texto = texto + '<b>Teléfono: </b>' + str(embarcador.telefono if embarcador.telefono is not None else '') + '<br>'
            texto = texto + '<b>Contactos: </b>' + str(embarcador.contactos if embarcador.contactos is not None else '') + '<br>'
            texto = texto + '<br>'
            texto = texto + '<b>Consignatario: </b>'+str(Vembarque.consignatario if Vembarque.consignatario is not None else '')+'<br>'
            texto = texto + '<b>Datos del consignatario: </b><br>'
            texto = texto + '<b>Dirección: </b>' +str(consignatario.direccion if consignatario.direccion is not None else '')+' -'+str(consignatario.ciudad if consignatario.ciudad is not None else '')+'-'+str(consignatario.pais if consignatario.pais is not None else '')+'<br>'
            texto = texto + '<b>RUT: </b>' + str(consignatario.ruc if consignatario.ruc is not None else '') + '<br>'
            texto = texto + '<b>Teléfono: </b>' + str(consignatario.telefono if consignatario.telefono is not None else '') + '<br>'
            texto = texto + '<b>Contactos: </b>' + str(consignatario.contactos if consignatario.contactos is not None else '') + '<br>'
            texto = texto + '<br>'
            texto = texto + '<b>Agente: </b>'+str(Vembarque.agente if Vembarque.agente is not None else '')+'<br>'
            texto = texto + '<b>Deposito: </b>'+str(seguimiento.deposito if seguimiento.deposito is not None else '')
            # Detalle del embarque
            texto = texto + '<b>Detalle del embarque</b>'
            envase = ExpmaritEnvases.objects.filter(numero=id)
            embarque_h = ExpmaritCargaaerea.objects.filter(numero=id)
            if envase.count() > 0 :
                for registro in envase:
                    texto += '<br><b>' + (
                        str(registro.cantidad) if registro.cantidad is not None else '') + 'x' + (
                                 str(registro.unidad).upper() if registro.unidad is not None else '') + '</b>: ' + (
                                 str(registro.tipo).upper() if hasattr(registro,
                                                                       'tipo') and registro.tipo is not None else '')
                    texto += ' <b>CNTR:</b> '+ str(registro.nrocontenedor if registro.nrocontenedor is not None else '')
                    texto += ' <b>SEAL:</b> '+ str(registro.precinto if registro.precinto is not None else '')
                    texto += ' <b>WT:</b> '+ str('{:.3f}'.format(registro.peso) if registro.peso is not None else '')
                    texto += ' <b>VOL:</b> '+ str('{:.3f}'.format(registro.volumen) if registro.volumen is not None else '')

            if embarque_h.count()>0:
                for e in embarque_h:
                    texto += '<br><b>Bultos:</b> ' + str(e.bultos if e.bultos is not None else '')+'<br>'
                    texto += ' <b>Producto:</b> ' + str(e.producto.nombre if e.producto.nombre is not None else '')+'<br>'
                    texto += ' <b>Peso:</b> ' + str(e.bruto if e.bruto is not None else '')+'<br>'
                    texto += ' <b>Volumen:</b> ' + str(e.cbm if e.cbm is not None else '')+'<br>'
                    texto = texto + '<br>'

            texto = texto + '<b>Forma de pago: </b>'+str(seguimiento.pago if seguimiento.pago is not None else '')+'<br>'
            texto = texto + '<b>Vendedor: </b>'+str(seguimiento.vendedor if seguimiento.vendedor is not None else '')+'<br>'
            # Cerrar el contenedor
            texto = texto + '</div>'

            resultado['resultado'] = 'exito'
            resultado['texto'] = texto
        except Exception as e:
            resultado['resultado'] = str(e)
    else:
        resultado['resultado'] = 'Ha ocurrido un error.'
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def get_datos_caratula(request):
    resultado = {}
    if is_ajax(request):
        try:
            id = request.POST['numero']
            Vembarque = VEmbarqueaereo.objects.get(numero=id)
            embarque = ExpmaritEmbarqueaereo.objects.get(numero=id)
            embarcador = Clientes.objects.get(codigo=embarque.embarcador)
            consignatario = Clientes.objects.get(codigo=embarque.consignatario)
            ruta = ExpmaritConexaerea.objects.filter(numero=id).order_by('-id').values_list('salida', 'llegada').first()

            salida, llegada = ruta if ruta else (None, None)

            try:
                seguimiento = VGrillaSeguimientos.objects.get(numero=Vembarque.seguimiento)
            except VGrillaSeguimientos.DoesNotExist:
                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='', deposito='', pago='', vendedor='')

            texto = '<div style="margin: 0 auto; font-family: Courier New, monospace; font-size: 12px;">'
            texto += '<h2 style="text-align: left;">OCEANLINK LTDA.</h2>'
            texto += '<b><p style="font-size:20px;text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
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
            texto += '<br><hr style="border: none; border-top: 0.5px solid #000; margin: 2px 0;"><br>'

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
            texto += '<hr style="border: none; border-top: 0.5px solid #000; margin: 2px 0;"><br>'

            # Detalle del embarque - envases
            envase = ExpmaritEnvases.objects.filter(numero=id)
            if envase.exists():
                for registro in envase:
                    texto += (
                        f"{registro.cantidad}x{registro.unidad.upper() if registro.unidad else ''} "
                        f"{registro.tipo.upper() if registro.tipo else ''} "
                        f"CTER: {registro.nrocontenedor or ''} SEAL: {registro.precinto or ''} "
                        f"WT: {registro.peso:.3f} VOL: {registro.volumen:.3f}<br>"
                    )

            # Detalle de la mercadería
            embarque_h = ExpmaritCargaaerea.objects.filter(numero=id)
            for e in embarque_h:
                texto += formatear_caratula("Nro Bultos", f"{e.bultos} {e.tipo}" if e.tipo else e.bultos)
                texto += formatear_caratula("Mercadería", e.producto.nombre if e.producto else '')
                texto += '<br>'
                texto += formatear_caratula("Peso", e.bruto)
                texto += formatear_caratula("Volumen", e.cbm)
                texto += '<br><hr style="border: none; border-top: 0.5px solid #000; margin: 2px 0;"><br>'

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
