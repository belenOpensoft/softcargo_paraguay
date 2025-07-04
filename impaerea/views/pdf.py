import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from impaerea.models import (VEmbarqueaereo, ImportEmbarqueaereo, ImportCargaaerea, ImportConexaerea)
from impomarit.views.mails import formatear_caratula
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
            embarque = ImportEmbarqueaereo.objects.get(numero=id)
            embarcador = Clientes.objects.get(codigo=embarque.embarcador)
            consignatario = Clientes.objects.get(codigo=embarque.consignatario)
            ruta = ImportConexaerea.objects.filter(numero=id).order_by('-id').values_list('salida', 'llegada','vuelo','ciavuelo').first()

            salida, llegada, vuelo, cia = ruta if ruta else (None, None, None, None)

            try:
                seguimiento = VGrillaSeguimientos.objects.get(numero=Vembarque.seguimiento)
            except VGrillaSeguimientos.DoesNotExist:
                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='', deposito='', pago='', vendedor='')

            texto = '<div style="margin: 0 auto; font-family: Courier New, monospace; font-size: 11.5px !important;">'
            texto += '<h2 style="text-align: left;">OCEANLINK LTDA.</h2>'
            texto += '<b><p style="font-size:17px;text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto += f'Seguimiento: {seguimiento.numero}<br>'
            texto += f'Posicion:  {Vembarque.posicion}<br>'
            texto += f'Incoterms: {seguimiento.terminos}</p></b>'
            texto += '<p style="text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto += f'Origen: {Vembarque.origen}<br>'
            texto += f'Destino:  {Vembarque.destino}</p><br>'

            # Primer bloque
            texto += formatear_caratula("Master", Vembarque.awb)
            texto += formatear_caratula("House", Vembarque.hawb)
            texto += formatear_caratula("ETA", llegada.strftime('%d-%m-%Y') if isinstance(llegada, datetime.datetime) else '?')
            texto += formatear_caratula("ETD", salida.strftime('%d-%m-%Y') if isinstance(salida, datetime.datetime) else '?')
            texto += formatear_caratula("Vuelo", vuelo if vuelo else 'S/I')
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
            cargas = ImportCargaaerea.objects.filter(numero=id)
            for e in cargas:
                volumen = ''
                if e.medidas:
                    medidas = e.medidas.split('*')
                else:
                    medidas = None

                if medidas and len(medidas) == 3 and all(m.replace('.', '', 1).isdigit() for m in medidas):
                    try:
                        volumen = round(float(medidas[0]) * float(medidas[1]) * float(medidas[2]) * float(e.bultos) / 1000000, 2)
                    except:
                        volumen = 0
                else:
                    volumen = 0


                texto += formatear_caratula("Nro Bultos", e.bultos)
                texto += formatear_caratula("Mercaderia", e.producto.nombre if e.producto else '')
                texto += '<br>'
                texto += formatear_caratula("Peso", e.bruto)
                texto += formatear_caratula("Volumen", volumen)
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
