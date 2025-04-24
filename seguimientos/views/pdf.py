import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from administracion_contabilidad.models import MantenimientosClientes, MantenimientosCiudades
from impomarit.views.mails import formatear_caratula
from mantenimientos.models import Vapores
from mantenimientos.views.bancos import is_ajax
from seguimientos.models import VGrillaSeguimientos, Envases, VCargaaerea, Cargaaerea, Conexaerea


@login_required(login_url='/')
def get_datos_caratula_old(request):
    resultado = {}
    if is_ajax(request):
        try:
            id = request.POST['numero']
            row = VGrillaSeguimientos.objects.get(numero=id)
            aereo = False
            if row.modo == 'IMPORT AEREO' or row.modo == 'EXPORT AEREO':
                aereo = True

            # Añadir un contenedor con ancho máximo
            texto = '<div style="margin: 0 auto; font-family: Courier New, monospace; font-size: 11px;">'
            texto = texto + '<h2 style="text-align: left;">OCEANLINK LTDA.</h2><HR>'
            # Ajustar el texto que se cortaba
            texto = texto + '<b><p style="text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto = texto + '<span style="font-size: 17px;">Seguimiento: ' + str(row.numero if row.numero is not None else '') + '</span><br>'
            texto = texto + '<span style="font-size: 17px;">Posicion:  ' + str(row.posicion if row.posicion is not None else '') + '</span><br><br>'
            texto = texto + '<span style="font-size: 17px;">Incoterms: ' + str(row.terminos if row.terminos is not None else '') + '</span></b><br><br>'
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
                emb_tel = emb.telefono
                emb_empresa = emb.empresa
                emb_contactos = emb.contactos
                emb_r=emb.ruc

                if MantenimientosCiudades.objects.filter(codedi=emb_c).exists():
                    emb_cc = MantenimientosCiudades.objects.get(codedi=emb_c).nombre
                else:
                    emb_cc = "S/I"

                emb_p = emb.pais
            else:
                emb = emb_dir = emb_c = emb_cc = emb_p = emb_tel = emb_empresa = emb_contactos=emb_r= "S/I"

            if MantenimientosClientes.objects.filter(codigo=row.consignatario_codigo).exists():
                con = MantenimientosClientes.objects.get(codigo=row.consignatario_codigo)
                con_dir = con.direccion
                con_tel = con.telefono
                con_empresa = con.empresa
                con_contactos = con.contactos
                con_c = con.ciudad

                if MantenimientosCiudades.objects.filter(codedi=con_c).exists():
                    con_cc = MantenimientosCiudades.objects.get(codedi=con_c).nombre
                else:
                    con_cc = "S/I"

                con_p = con.pais
                con_r = con.ruc
            else:
                con = con_dir = con_c = con_cc = con_p = con_r = con_empresa=con_contactos=con_tel= "S/I"

            if MantenimientosClientes.objects.filter(codigo=row.agente_codigo).exists():
                agen_c = MantenimientosClientes.objects.get(codigo=row.agente_codigo).ciudad
            else:
                agen_c = "S/I"

            texto = texto + '<b>ETD: </b>'+str(res)+'<br>'

            if aereo:
                vapor = ''
                ruta_seg = Conexaerea.objects.filter(numero=row.numero).values('vapor')
                if len(ruta_seg) > 0:
                    vapor = ruta_seg[0]['vapor']
                nombre_vapor=vapor

            else:
                if isinstance(row.vapor, int) or (isinstance(row.vapor, str) and row.vapor.isdigit()):
                    vapor_obj = Vapores.objects.filter(codigo=int(row.vapor)).first()
                    nombre_vapor = vapor_obj.nombre if vapor_obj else 'S/I'
                else:
                    nombre_vapor = row.vapor if row.vapor is not None else 'S/I'

            texto = texto + f'<b>Vapor: </b>{nombre_vapor}<br>' if not aereo else texto + f'<b>Vuelo: </b>{nombre_vapor}<br>'

            texto = texto + '<b>Transportista: </b>'+str(row.transportista if row.transportista is not None else '')+'<br>'
            texto = texto + '<b>Orden cliente: </b>'+str(row.refcliente if row.refcliente is not None else 'S/O')+'</strong>'
            texto = texto + '<b>Embarcador: </b>' + str(emb_empresa) + '<br>'
            texto = texto + '<b>Datos del embarcador: </b><br>'
            texto = texto + '<b>Dirección: </b>' + str(emb_dir) + ' -' + str(emb_cc) + '-' + str(emb_p) + '<br>'
            texto = texto + '<b>RUT: </b>' + str(emb_r) + '<br>'
            texto = texto + '<b>Teléfono: </b>' + str(emb_tel) + '<br>'
            texto = texto + '<b>Contactos: </b>' + str(emb_contactos) + '<br>'
            texto = texto + '<br>'
            texto = texto + '<b>Consignatario: </b>' + str(con_empresa) + '<br>'
            texto = texto + '<b>Datos del consignatario: </b><br>'
            texto = texto + '<b>Dirección: </b>' + str(con_dir) + ' -' + str(con_cc) + '-' + str(con_p) + '<br>'
            texto = texto + '<b>RUT: </b>' + str(con_r) + '<br>'
            texto = texto + '<b>Teléfono: </b>' + str(con_tel) + '<br>'
            texto = texto + '<b>Contactos: </b>' + str(con_contactos) + '<br>'
            texto = texto + '<br>'
            texto = texto + '<strong>Agente: ' + str(f'{row.agente} - ' if row.agente is not None else '') + str(agen_c if agen_c is not None else '') + '<br><br>'
            texto = texto + 'Deposito: '+str(row.deposito if row.deposito is not None else '') + '</strong><br><br>'
            # Detalle del embarque
            texto = texto + '<b>Detalle del embarque</b>'

            if row.modo=='IMPORT AEREO' or row.modo == 'EXPORT AEREO':
                envase=None
            else:
                envase = Envases.objects.filter(numero=id)

            embarque = Cargaaerea.objects.filter(numero=id)

            if not aereo:
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


            if embarque.count()>0:
                for e in embarque:
                    texto += '<br><b>Bultos:</b> ' + str(e.bultos if e.bultos is not None else '')+'<br>'
                    texto += ' <b>Producto:</b> ' + str(e.producto.nombre if e.producto.nombre is not None else '')+'<br>'
                    texto += ' <b>Peso:</b> ' + str(e.bruto if e.bruto is not None else '')+'<br>'
                    texto += ' <b>Volumen:</b> ' + str(e.cbm if e.cbm is not None else '')+'<br>'
                    texto = texto + '<br>'
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
def get_datos_caratula(request):
    resultado = {}
    if is_ajax(request):
        try:
            id = request.POST['numero']
            row = VGrillaSeguimientos.objects.get(numero=id)
            aereo = row.modo in ['IMPORT AEREO', 'EXPORT AEREO']

            texto = '<div style="margin: 0 auto; font-family: Courier New, monospace; font-size: 11px;">'
            texto += '<h2 style="text-align: left;">OCEANLINK LTDA.</h2>'
            texto += '<b><p style="font-size:17px;text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto += f'Seguimiento: {row.numero}<br>'
            texto += f'Posicion:  {row.posicion or ""}<br>'
            texto += f'Incoterms: {row.terminos or ""}</p></b>'
            texto += '<p style="text-align:right; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto += f'Origen: {row.origen or ""}<br>'
            texto += f'Destino:  {row.destino or ""}</p><br>'

            texto += formatear_caratula("Master", row.awb or "")
            texto += formatear_caratula("House", row.hawb or "")
            texto += formatear_caratula("ETA", row.eta.strftime('%d-%m-%Y') if isinstance(row.eta, datetime.datetime) else "?")
            texto += formatear_caratula("ETD", row.etd.strftime('%d-%m-%Y') if isinstance(row.etd, datetime.datetime) else "?")

            if aereo:
                vapor = Conexaerea.objects.filter(numero=row.numero).values_list('vapor', flat=True).first()
                nombre_vapor = vapor or 'S/I'
                texto += formatear_caratula("Vuelo", nombre_vapor)
            else:
                if isinstance(row.vapor, int) or (isinstance(row.vapor, str) and row.vapor.isdigit()):
                    vapor_obj = Vapores.objects.filter(codigo=int(row.vapor)).first()
                    nombre_vapor = vapor_obj.nombre if vapor_obj else 'S/I'
                else:
                    nombre_vapor = row.vapor or 'S/I'
                texto += formatear_caratula("Vapor", nombre_vapor)

            texto += formatear_caratula("Transportista", row.transportista or "")
            texto += formatear_caratula("Orden cliente", row.refcliente or "S/O")
            texto += '<br><span style="display: block; border-top: 0.2pt solid #CCC; margin: 2px 0;"></span><br>'

            # Embarcador
            emb = MantenimientosClientes.objects.filter(codigo=row.embarcador_codigo).first()
            if emb:
                emb_ciudad = MantenimientosCiudades.objects.filter(codedi=emb.ciudad).first()
                direccion_emb = f"{emb.direccion} - {emb_ciudad.nombre if emb_ciudad else 'S/I'} - {emb.pais}"
                texto += f"<b>Embarcador: {emb.empresa}</b><br>"
                texto += "<b>Datos del embarcador:</b><br>"
                texto += formatear_caratula("Empresa", emb.empresa)
                texto += formatear_caratula("Dirección", direccion_emb)
                texto += formatear_caratula("Ph", emb.telefono)
                texto += formatear_caratula("RUT", emb.ruc)
                texto += formatear_caratula("Contactos", emb.contactos)
            else:
                texto += "<b>Embarcador:</b> S/I<br><b>Datos del embarcador:</b><br>"
                texto += formatear_caratula("Empresa", "S/I")
                texto += formatear_caratula("Dirección", "S/I")
                texto += formatear_caratula("Ph", "S/I")
                texto += formatear_caratula("RUT", "S/I")
                texto += formatear_caratula("Contactos", "S/I")
            texto += '<br>'

            # Consignatario
            con = MantenimientosClientes.objects.filter(codigo=row.consignatario_codigo).first()
            if con:
                con_ciudad = MantenimientosCiudades.objects.filter(codedi=con.ciudad).first()
                direccion_con = f"{con.direccion} - {con_ciudad.nombre if con_ciudad else 'S/I'} - {con.pais}"
                texto += f"<b>Consignatario: {con.empresa}</b><br>"
                texto += "<b>Datos del consignatario:</b><br>"
                texto += formatear_caratula("Empresa", con.empresa)
                texto += formatear_caratula("Dirección", direccion_con)
                texto += formatear_caratula("Ph", con.telefono)
                texto += formatear_caratula("RUT", con.ruc)
                texto += formatear_caratula("Contactos", con.contactos)
            else:
                texto += "<b>Consignatario:</b> S/I<br><b>Datos del consignatario:</b><br>"
                texto += formatear_caratula("Empresa", "S/I")
                texto += formatear_caratula("Dirección", "S/I")
                texto += formatear_caratula("Ph", "S/I")
                texto += formatear_caratula("RUT", "S/I")
                texto += formatear_caratula("Contactos", "S/I")
            texto += '<br>'

            # Agente
            agente_ciudad = MantenimientosClientes.objects.filter(codigo=row.agente_codigo).first()
            agente_ciudad_nombre = MantenimientosCiudades.objects.filter(codedi=agente_ciudad.ciudad).first().nombre if agente_ciudad else "S/I"
            texto += f"<b>Agente:</b> {row.agente or ''} - {agente_ciudad_nombre}<br>"
            texto += f"<b>Deposito:</b> {row.deposito or ''}<br><br>"
            texto += '<span style="display: block; border-top: 0.2pt solid #CCC; margin: 2px 0;"></span><br>'

            # Detalle del embarque
            texto += "<b>Detalle del embarque:</b><br>"
            movimiento = None
            if not aereo:
                envases = Envases.objects.filter(numero=id)
                for registro in envases:
                    peso = f"{registro.peso:.3f}" if registro.peso else "0.000"
                    volumen = f"{registro.volumen:.3f}" if registro.volumen else "0.000"

                    texto += (
                        f"{int(registro.cantidad or 0)}x{registro.unidad.upper() if registro.unidad else ''} {registro.movimiento if registro.movimiento else 'S/I'} "
                        f"{registro.tipo.upper() if registro.tipo else ''} "
                        f"CNTR: {registro.nrocontenedor or ''} SEAL: {registro.precinto or ''} "
                        f"WT: {peso} VOL: {volumen}<br>"
                    )
                    movimiento=registro.movimiento

            # Detalle de mercadería
            embarque = Cargaaerea.objects.filter(numero=id)
            for e in embarque:
                texto += formatear_caratula("Nro Bultos", f"{e.bultos} {e.tipo}") if movimiento is not None and movimiento == 'LCL/LCL' else formatear_caratula("Nro Bultos", f"{e.bultos}")
                texto += formatear_caratula("Mercadería", e.producto.nombre if e.producto else '')
                texto += '<br>'
                texto += formatear_caratula("Peso", e.bruto)
                texto += formatear_caratula("Volumen", e.cbm)
                texto += '<br><span style="display: block; border-top: 0.2pt solid #CCC; margin: 2px 0;"></span><br>'

            texto += formatear_caratula("Forma de pago", row.pago)
            texto += formatear_caratula("Vendedor", row.vendedor)
            texto += '</div>'

            resultado['resultado'] = 'exito'
            resultado['texto'] = texto
        except Exception as e:
            resultado['resultado'] = str(e)
    else:
        resultado['resultado'] = 'Ha ocurrido un error.'
    return HttpResponse(json.dumps(resultado), "application/json")




