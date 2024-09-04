import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from mantenimientos.views.bancos import is_ajax
from seguimientos.models import VGrillaSeguimientos, Envases


@login_required(login_url='/')
def get_datos_caratula(request):
    resultado = {}
    if is_ajax(request):
        try:
            id = request.POST['numero']
            row = VGrillaSeguimientos.objects.get(numero=id)
            texto = '<h1>OCEANLINK</h1><HR><h2>'
            texto = texto + '<p style="text-align:right;">Seguimiento: '+str(row.numero if row.numero is not None else '')+'<br>'
            texto = texto + 'Posicion:  '+str(row.posicion if row.posicion is not None else '')+'<br>'
            texto = texto + 'Incoterms: ' +str(row.terminos if row.terminos is not None else '')+'</p></h2><hr>'
            texto = texto + '<b>Master: </b>'+str(row.awb if row.awb is not None else '')+'<br>'
            texto = texto + '<b>House: </b>'+str(row.hawb if row.hawb is not None else '') +'<br>'
            if isinstance(row.eta, datetime.datetime):
                res = row.eta.strftime('%d-%m-%Y')
            else:
                res = '?'
            texto = texto + '<b>ETA: </b>'+str(res)+'<br>'
            if isinstance(row.etd, datetime.datetime):
                res = row.etd.strftime('%d-%m-%Y')
            else:
                res = '?'
            texto = texto + '<b>ETD: </b>'+str(res)+'<br>'
            texto = texto + '<b>Vapor: </b>'+str(row.vapor if row.vapor is not None else '')+'<br>'
            texto = texto + '<b>Transportista: </b>'+str(row.transportista if row.transportista is not None else '')+'<br>'
            texto = texto + '<b>Orden cliente: </b>'+str(row.refcliente if row.refcliente is not None else '')+'<hr>'
            texto = texto + '<b>Embarcador: </b>'+str(row.embarcador if row.embarcador is not None else '')+'<br>'
            texto = texto + '<b>Datos del embarcador: </b><br>'
            texto = texto + '<br>'
            texto = texto + '<b>Consignatario: </b>'+str(row.consignatario if row.consignatario is not None else '')+'<br>'
            texto = texto + '<b>Datos del consignatario: </b><hr>'
            texto = texto + '<b>Agente: </b>'+str(row.agente if row.agente is not None else '')+'<br>'
            texto = texto + '<b>Deposito: </b>'+str(row.deposito if row.deposito is not None else '')
            # Detalle del embarque
            texto = texto + '<hr><b>Detalle del embarque</b>'
            envase = Envases.objects.filter(numero=id)
            if envase.count() > 0 :
                for registro in envase:
                    texto += '<br><b>'+ str(registro.unidad if registro.unidad is not None else '').upper() +'</b>: '+ str('{:.3f}'.format(registro.cantidad) if registro.cantidad is not None else '')
                    texto += ' <b>CNTR:</b> '+ str(registro.nrocontenedor if registro.nrocontenedor is not None else '')
                    texto += ' <b>SEAL:</b> '+ str(registro.precinto if registro.precinto is not None else '')
                    texto += ' <b>WT:</b> '+ str('{:.3f}'.format(registro.peso) if registro.peso is not None else '')
                    texto += ' <b>VOL:</b> '+ str('{:.3f}'.format(registro.volumen) if registro.volumen is not None else '')
            texto = texto + '<hr>'
            texto = texto + '<b>Forma de pago: </b>'+str(row.pago if row.pago is not None else '')+'<br>'
            texto = texto + '<b>Vendedor: </b>'+str(row.vendedor if row.vendedor is not None else '')+'<br>'

            resultado['resultado'] = 'exito'
            resultado['texto'] = texto
        except Exception as e:
            resultado['resultado'] = str(e)
    else:
        resultado['resultado'] = 'Ha ocurrido un error.'
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)