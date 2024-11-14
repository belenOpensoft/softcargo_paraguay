from datetime import datetime
import json
import locale
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from administracion_contabilidad.models import Infofactura, VistaGastosPreventa
from expaerea.models import ExportEmbarqueaereo
from expmarit.models import ExpmaritEmbarqueaereo
from expterrestre.models import ExpterraEmbarqueaereo
from impaerea.models import ImportEmbarqueaereo
from impomarit.models import Embarqueaereo
from impterrestre.models import ImpterraEmbarqueaereo
from mantenimientos.models import Clientes
from mantenimientos.views.bancos import is_ajax
from seguimientos.models import VGrillaSeguimientos


@login_required(login_url='/')
def get_datos_caratula(request):
    resultado = {}
    if is_ajax(request):
        try:
            id = request.POST['id']
            clase=request.POST['clase']
            modo = request.POST['modo']

            preventa = Infofactura.objects.get(id=id)
            gastos = VistaGastosPreventa.objects.filter(numero=preventa.referencia)

            if clase=='IM':
                embarque = Embarqueaereo.objects.get(numero=preventa.referencia)
            elif clase=='EM':
                embarque = ExpmaritEmbarqueaereo.objects.get(numero=preventa.referencia)
            elif clase=='IA':
                embarque = ImportEmbarqueaereo.objects.get(numero=preventa.referencia)
            elif clase=='EA':
                embarque = ExportEmbarqueaereo.objects.get(numero=preventa.referencia)
            elif clase == 'IT':
                embarque = ImpterraEmbarqueaereo.objects.get(numero=preventa.referencia)
            elif clase=='ET':
                embarque = ExpterraEmbarqueaereo.objects.get(numero=preventa.referencia)

            cliente = Clientes.objects.get(codigo=embarque.cliente)
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Revisa si este ajuste de idioma causa problemas
            fecha_actual = datetime.now()
            fecha_formateada = fecha_actual.strftime('%A, %d de %B del %Y').upper()

            try:
                seg = VGrillaSeguimientos.objects.get(numero=preventa.seguimiento)
            except VGrillaSeguimientos.DoesNotExist:
                seg = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='',deposito='', pago='', vendedor='')

            # Añadir un contenedor con ancho máximo
            texto = '<div style=" margin: 0 auto;">'
            texto = texto + '<h2 style="text-align: left;">OCEANLINK LTDA.</h2>'
            texto = texto + '<h3 style="text-align: right;margin-right:60px;">PRE-FACTURA</h3>'
            # Ajustar el texto que se cortaba
            texto = texto + '<p style="font-size:16px;text-align:left; word-wrap: break-word; white-space: normal; max-width: 100%;">'
            texto = texto + 'Fecha: ' + fecha_formateada + '<br>'
            texto = texto + 'Nro Preventa:  ' + id + '<br>'
            texto = texto + 'Status: PARA FACTURAR</p><hr>'
            texto = texto + '<p style="text-align:left; word-wrap: break-word; white-space: normal; max-width: 100%;">'
            texto = texto + 'Cliente: ' + str(cliente.empresa if cliente.empresa is not None else '') + '<br>'
            texto = texto + 'Ciudad: ' + str(cliente.ciudad if cliente.ciudad is not None else '') + '<br>'
            texto = texto + 'Id fiscal: ' + str(cliente.ruc if cliente.ruc is not None else '') + '<br>'
            texto = texto + 'Dirección:  ' + str(cliente.direccion if cliente.direccion is not None else '') + '</p><hr><br>'

            texto = texto + '<p style="text-align:left; word-wrap: break-word; white-space: normal; max-width: 100%;">'
            texto = texto + 'Posicion: ' + str(preventa.posicion if preventa.posicion is not None else '') + '<br>'
            texto = texto + 'Modo: ' + modo + '<br>'
            texto = texto + 'Peso/Bultos/Volumen: ' + str(preventa.kilos if preventa.kilos is not None else '') + '-'+ str(preventa.bultos if preventa.bultos is not None else '') + '-'+ str(preventa.volumen if preventa.volumen is not None else '') +'<br>'
            texto = texto + 'House: ' + str(preventa.house if preventa.house is not None else '') + '<br>'
            texto = texto + 'Pago: ' + str(preventa.pagoflete if preventa.pagoflete is not None else '') + '<br>'
            texto = texto + 'Incoterms: ' + str(preventa.terminos if preventa.terminos is not None else '') + '<br>'
            texto = texto + 'Consignatario: ' + str(preventa.consigna if preventa.consigna is not None else '') + '<br>'
            texto = texto + 'Embarcador: ' + str(preventa.embarca if preventa.embarca is not None else '') + '<br>'
            texto = texto + 'Vuelo/Vapor: ' + str(preventa.vuelo if preventa.vuelo is not None else '') + '<br>'
            texto = texto + 'Ref. Cliente: ' + str(seg.refcliente if seg.refcliente  is not None else '') + '<br>'

            if isinstance(seg.eta, datetime):
                res = seg.eta.strftime('%d-%m-%Y')
            else:
                res = '?'
            texto = texto + '<b>ETA: </b>'+str(res)+'<br>'
            if isinstance(seg.etd, datetime):
                res = seg.etd.strftime('%d-%m-%Y')
            else:
                res = '?'
            texto = texto + '<b>ETD: </b>'+str(res)+'<br>'
            texto = texto + 'Master:  ' + str(preventa.master if preventa.master is not None else '') + '</p><br>'



            texto = texto + '<hr><b>Detalle del embarque</b><br>'
            total_sin_iva=0
            total_con_iva=0
            if gastos.count() > 0 :
                for registro in gastos:
                    texto += ' <b>Concepto:</b> '+ str(registro.servicio if registro.servicio is not None else '')
                    texto += ' <b>Monto:</b> '+ str(registro.precio if registro.precio  is not None else '')
                    texto += ' <b>IVA:</b> '+ str( registro.iva  if registro.iva is not None else '')
                    texto+='<br>'
                    total_sin_iva += registro.precio
                    if registro.iva == 'Basico':
                        total_con_iva += registro.precio * Decimal('1.22')
                    else:
                        total_con_iva += registro.precio

            texto = texto + '<hr><br>'

            texto = texto + '<b>Total sin IVA: </b>'+str(total_sin_iva)+'<br>'
            texto = texto + '<b>Total con IVA: </b>'+str(total_con_iva)+'<br>'
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