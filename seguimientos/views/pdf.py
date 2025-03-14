import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from administracion_contabilidad.models import MantenimientosClientes, MantenimientosCiudades
from mantenimientos.models import Vapores
from mantenimientos.views.bancos import is_ajax
from seguimientos.models import VGrillaSeguimientos, Envases, VCargaaerea


@login_required(login_url='/')
def get_datos_caratula(request):
    resultado = {}
    if is_ajax(request):
        try:
            id = request.POST['numero']
            row = VGrillaSeguimientos.objects.get(numero=id)

            # Añadir un contenedor con ancho máximo
            texto = '<div style=" margin: 0 auto;">'
            texto = texto + '<h2 style="text-align: left;">OCEANLINK LTDA.</h2><HR>'
            # Ajustar el texto que se cortaba
            texto = texto + '<b><p style="text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto = texto + '<span style="font-size: 20px;">Seguimiento: ' + str(row.numero if row.numero is not None else '') + '</span><br>'
            texto = texto + '<span style="font-size: 20px;">Posicion:  ' + str(row.posicion if row.posicion is not None else '') + '</span><br><br>'
            texto = texto + '<span style="font-size: 20px;">Incoterms: ' + str(row.terminos if row.terminos is not None else '') + '</span></b><br><br>'
            texto = texto + 'Origen: ' + str(row.origen if row.origen is not None else '') + '<br>'
            texto = texto + 'Destino: ' + str(row.destino if row.destino is not None else '') + '</p>'
            texto = texto + '<strong><b>Master: </b>' + str(row.awb if row.awb is not None else '') + '<br>'
            texto = texto + '<b>House: </b>' + str(row.hawb if row.hawb is not None else '') + '<br>'
            if isinstance(row.eta, datetime.datetime):
                res = row.eta.strftime('%d-%m-%Y')
            else:
                res = '?'
            texto = texto + '<b>ETA: </b>'+str(res)+'<br>'
            if isinstance(row.etd, datetime.datetime):
                res = row.etd.strftime('%d-%m-%Y')
            else:
                res = '?'

            if MantenimientosClientes.objects.filter(codigo=row.embarcador_codigo).exists():
                emb = MantenimientosClientes.objects.get(codigo=row.embarcador_codigo)
                emb_dir = emb.direccion
                emb_c = emb.ciudad

                if MantenimientosCiudades.objects.filter(codedi=emb_c).exists():
                    emb_cc = MantenimientosCiudades.objects.get(codedi=emb_c).nombre
                else:
                    emb_cc = "S/I"

                emb_p = emb.pais
            else:
                emb = emb_dir = emb_c = emb_cc = emb_p = "S/I"

            if MantenimientosClientes.objects.filter(codigo=row.consignatario_codigo).exists():
                con = MantenimientosClientes.objects.get(codigo=row.consignatario_codigo)
                con_dir = con.direccion
                con_c = con.ciudad

                if MantenimientosCiudades.objects.filter(codedi=con_c).exists():
                    con_cc = MantenimientosCiudades.objects.get(codedi=con_c).nombre
                else:
                    con_cc = "S/I"

                con_p = con.pais
                con_r = con.ruc
            else:
                con = con_dir = con_c = con_cc = con_p = con_r = "S/I"

            if MantenimientosClientes.objects.filter(codigo=row.agente_codigo).exists():
                agen_c = MantenimientosClientes.objects.get(codigo=row.agente_codigo).ciudad
            else:
                agen_c = "S/I"

            texto = texto + '<b>ETD: </b>'+str(res)+'<br>'
            if isinstance(row.vapor, int) or (isinstance(row.vapor, str) and row.vapor.isdigit()):
                vapor_obj = Vapores.objects.filter(codigo=int(row.vapor)).first()
                nombre_vapor = vapor_obj.nombre if vapor_obj else 'S/I'
            else:
                nombre_vapor = row.vapor if row.vapor is not None else 'S/I'

            texto = texto + f'<b>Vapor: </b>{nombre_vapor}<br>'

            texto = texto + '<b>Transportista: </b>'+str(row.transportista if row.transportista is not None else '')+'<br>'
            texto = texto + '<b>Orden cliente: </b>'+str(row.refcliente if row.refcliente is not None else 'S/O')+'</strong><hr>'
            texto = texto + '<b><strong>Embarcador: </b>' + str(row.embarcador if row.embarcador is not None else '') + '</strong><br>'
            texto = texto + 'Datos Embarcador:' + str(row.embarcador if row.embarcador is not None else '') + '<br>'
            texto = texto + str(emb_dir if emb_dir is not None else '') + ', ' + str(emb_cc if emb_cc is not None else '') + ', ' + str(emb_p if emb_p is not None else '') + '<br><br>'
            texto = texto + '<b><strong>Consignatario: </b>' + str(row.consignatario if row.consignatario is not None else '')+'</strong><br>'
            texto = texto + 'Datos Consignatario: ' + str(row.consignatario if row.consignatario is not None else '')+'<br>'
            texto = texto + str(con_dir if con_dir is not None else '') + ', ' + str(con_cc if con_cc is not None else '') + ', ' + str(con_c if con_c is not None else '') + ', ' + str(con_p if con_p is not None else '') + '<br>'
            texto = texto + 'RUT: ' + str(con_r if con_r is not None else '') + '<br><br>'
            texto = texto + '<strong>Agente: ' + str(f'{row.agente} - ' if row.agente is not None else '') + str(agen_c if agen_c is not None else '') + '<br><br>'
            texto = texto + 'Deposito: '+str(row.deposito if row.deposito is not None else '') + '</strong><br><br>'
            # Detalle del embarque
            # texto = texto + '<hr><b>Detalle del embarque</b>'
            envase = Envases.objects.filter(numero=id)
            mercaderia = VCargaaerea.objects.filter(numero=row.numero)
            reg = ''
            if mercaderia.exists():
                reg = ', '.join([mer.mercaderia for mer in mercaderia if mer.mercaderia])
            if row.modo == 'IMPORT AEREO':
                if envase.count() > 0 :
                    for registro in envase:
                        texto += 'Nro Contenedor: ' + str(registro.nrocontenedor if registro.nrocontenedor is not None else '') + '<br>'
                        texto += 'Nro Bultos: ' + str(f'{registro.bultos} {registro.envase}' if registro.bultos is not None else '') + '<br>'
                        texto += 'Mercaderia: ' + str(reg if reg is not None else '') + '<br><br>'

                        texto += 'Peso: ' + str(registro.peso if registro.peso is not None else '') + '<br>'
                        texto += 'Volumen: ' + str(registro.volumen if registro.volumen is not None else '') + '<br>'
            if row.modo == 'IMPORT MARITIMO':
                if envase.count() > 0:
                    for registro in envase:
                        texto += str('{:.0f}'.format(registro.cantidad) if registro.cantidad is not None else '') + ' x ' + str(registro.unidad if registro.unidad is not None else '').upper() + ' ' + str(registro.tipo if registro.tipo is not None else '').upper()
                        texto += '  CTER: ' + str(registro.nrocontenedor if registro.nrocontenedor is not None else '')
                        texto += '  WT: ' + str('{:.3f}'.format(registro.peso) if registro.peso is not None else '')
                        texto += '  VOL: ' + str('{:.3f}'.format(registro.volumen) if registro.volumen is not None else '') + '<br><br>'

                        texto += 'Nro Contenedor: ' + str(registro.nrocontenedor if registro.nrocontenedor is not None else '') + '<br>'
                        texto += 'Nro Bultos: ' + str(f'{registro.bultos} {registro.envase}' if registro.bultos is not None else '') + '<br>'
                        texto += 'Mercaderia: ' + str(reg if reg is not None else '') + '<br><br>' '<br><br>'

                        texto += 'Peso: ' + str(registro.peso if registro.peso is not None else '') + '<br>'
                        texto += 'Volumen: ' + str(registro.volumen if registro.volumen is not None else '') + '<br>'
            texto = texto + '<hr>'
            texto = texto + 'Forma de pago: '+str(row.pago if row.pago is not None else '')+'<br>'
            texto = texto + 'Vendedor: '+str(row.vendedor if row.vendedor is not None else '')+'<br>'
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

