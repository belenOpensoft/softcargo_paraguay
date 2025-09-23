import datetime
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from mantenimientos.models import Clientes as MantenimientosClientes, Ciudades as MantenimientosCiudades
from impomarit.views.mails import formatear_caratula
from mantenimientos.models import Vapores
from mantenimientos.views.bancos import is_ajax
from seguimientos.models import VGrillaSeguimientos, Envases, VCargaaerea, Cargaaerea, Conexaerea


@login_required(login_url='/')
def get_datos_caratula(request):
    resultado = {}
    if is_ajax(request):
        try:
            id = request.POST['numero']
            row = VGrillaSeguimientos.objects.get(numero=id)
            aereo = row.modo in ['IMPORT AEREO', 'EXPORT AEREO']

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
                seguimiento=row.numero,
                posicion=row.posicion or '',
                incoterms=row.terminos or ''
            )

            texto += '<p style="text-align:right;font-size: 14px; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:20px;">'
            origen = MantenimientosCiudades.objects.filter(codigo=row.origen).first()
            destino = MantenimientosCiudades.objects.filter(codigo=row.destino).first()
            texto += f'Origen: {origen.nombre or "" if origen else ""}<br>'
            texto += f'Destino:  {destino.nombre or "" if destino else ""}</p><br>'

            texto += formatear_caratula("Master", row.awb or "")
            texto += formatear_caratula("House", row.hawb or "")
            texto += formatear_caratula("ETA", row.eta.strftime('%d-%m-%Y') if isinstance(row.eta, datetime.datetime) else "?")
            texto += formatear_caratula("ETD", row.etd.strftime('%d-%m-%Y') if isinstance(row.etd, datetime.datetime) else "?")

            if aereo:
                vuelos = (
                    Conexaerea.objects
                    .filter(numero=row.numero)
                    .values_list('cia', 'vapor')
                )
                if vuelos:
                    nombre_vapor = "; ".join([f"{cia}{vapor}" for cia, vapor in vuelos])
                else:
                    nombre_vapor = "S/I"

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
                emb_ciudad = MantenimientosCiudades.objects.filter(codigo=emb.ciudad).first()
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
                con_ciudad = MantenimientosCiudades.objects.filter(codigo=con.ciudad).first()
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

            if agente_ciudad:
                ciudad = MantenimientosCiudades.objects.filter(codigo=agente_ciudad.ciudad).first()
                agente_ciudad_nombre = ciudad.nombre if ciudad else "S/I"
            else:
                agente_ciudad_nombre = "S/I"

            texto += f"<b>Agente:</b> {row.agente or ''} - {agente_ciudad_nombre}<br>"
            texto += f"<b>Deposito:</b> {row.deposito or ''}<br><br>"
            texto += '<span style="display: block; border-top: 0.2pt solid #CCC; margin: 2px 0;"></span><br>'

            # Detalle del embarque
            texto += "<b>Detalle del embarque:</b><br>"
            movimiento = None
            if not aereo:
                envases = Envases.objects.filter(numero=id)
                if envases:
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
            if embarque:
                total_bultos = 0
                total_peso = 0.0
                total_volumen = 0.0
                mercaderias = []
                for e in embarque:
                    total_bultos += e.bultos or 0
                    total_peso += float(e.bruto or 0)
                    total_volumen += float(e.cbm or 0)
                    if e.producto:
                        mercaderias.append(e.producto.nombre)

                mercaderias_str = "; ".join(mercaderias)

                if movimiento is not None and movimiento == 'LCL/LCL':
                    texto += formatear_caratula("Nro Bultos", f"{total_bultos} {e.tipo}")
                else:
                    texto += formatear_caratula("Nro Bultos", f"{total_bultos}")

                texto += formatear_caratula("Mercadería", mercaderias_str)
                texto += formatear_caratula("Peso", round(total_peso, 2))
                texto += formatear_caratula("Volumen", round(total_volumen, 2))

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




