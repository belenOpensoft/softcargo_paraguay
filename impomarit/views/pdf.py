import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from impomarit.models import VEmbarqueaereo, Embarqueaereo, Cargaaerea
from mantenimientos.models import Clientes
from mantenimientos.views.bancos import is_ajax
from seguimientos.models import VGrillaSeguimientos, Envases


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
            try:
                seguimiento = VGrillaSeguimientos.objects.get(numero=Vembarque.seguimiento)
            except VGrillaSeguimientos.DoesNotExist:
                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='',deposito='', pago='', vendedor='')
            # Añadir un contenedor con ancho máximo
            texto = '<div style=" margin: 0 auto;">'
            texto = texto + '<h2 style="text-align: left;">OCEANLINK LTDA.</h2>'
            # Ajustar el texto que se cortaba
            texto = texto + '<b><p style="font-size:20px;text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto = texto + 'Seguimiento: ' + str(seguimiento.numero if seguimiento.numero is not None else '') + '<br>'
            texto = texto + 'Posicion:  ' + str(Vembarque.posicion if Vembarque.posicion is not None else '') + '<br>'
            texto = texto + 'Incoterms: ' + str(seguimiento.terminos if seguimiento.terminos is not None else '') + '</p></b><hr>'
            texto = texto + '<p style="text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto = texto + 'Origen: ' + str(Vembarque.origen if Vembarque.origen is not None else '') + '<br>'
            texto = texto + 'Destino:  ' + str(Vembarque.destino if Vembarque.destino is not None else '') + '</p><br>'
            texto = texto + '<b>Master: </b>' + str(Vembarque.awb if Vembarque.awb is not None else '') + '<br>'
            texto = texto + '<b>House: </b>' + str(Vembarque.hawb if Vembarque.hawb is not None else '') + '<br>'
            if isinstance(seguimiento.eta, datetime.datetime):
                res = seguimiento.eta.strftime('%d-%m-%Y')
            else:
                res = '?'
            texto = texto + '<b>ETA: </b>'+str(res)+'<br>'
            if isinstance(seguimiento.etd, datetime.datetime):
                res = seguimiento.etd.strftime('%d-%m-%Y')
            else:
                res = '?'
            texto = texto + '<b>ETD: </b>'+str(res)+'<br>'
            texto = texto + '<b>Vapor: </b>'+str(embarque.vapor if embarque.vapor is not None else '')+'<br>'
            texto = texto + '<b>Transportista: </b>'+str(Vembarque.transportista if Vembarque.transportista is not None else '')+'<br>'
            texto = texto + '<b>Orden cliente: </b>'+str(seguimiento.refcliente if seguimiento.refcliente is not None else '')+'<hr>'
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
            texto = texto + '<hr><b>Detalle del embarque</b>'
            envase = Envases.objects.filter(numero=id)
            embarque = Cargaaerea.objects.filter(numero=id)
            if envase.count() > 0 :
                for registro in envase:
                    texto += '<br><b>'+ str(registro.unidad if registro.unidad is not None else '').upper() +'</b>: '+ str('{:.3f}'.format(registro.cantidad) if registro.cantidad is not None else '')
                    texto += ' <b>CNTR:</b> '+ str(registro.nrocontenedor if registro.nrocontenedor is not None else '')
                    texto += ' <b>SEAL:</b> '+ str(registro.precinto if registro.precinto is not None else '')
                    texto += ' <b>WT:</b> '+ str('{:.3f}'.format(registro.peso) if registro.peso is not None else '')
                    texto += ' <b>VOL:</b> '+ str('{:.3f}'.format(registro.volumen) if registro.volumen is not None else '')

            texto = texto + '<hr>'
            if embarque.count()>0:
                for e in embarque:
                    texto += '<br><b>Bultos:</b> ' + str(e.bultos if e.bultos is not None else '')+'<br>'
                    texto += ' <b>Producto:</b> ' + str(e.producto.nombre if e.producto.nombre is not None else '')+'<br>'
                    texto += ' <b>Peso:</b> ' + str(e.bruto if e.bruto is not None else '')+'<br>'
                    texto += ' <b>Volumen:</b> ' + str(e.cbm if e.cbm is not None else '')+'<br>'
                    texto = texto + '<br>'

            texto = texto + '<hr>'
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