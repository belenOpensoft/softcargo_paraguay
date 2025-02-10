import io
import json
import datetime
import sys

from django.http import FileResponse, Http404
import os
import xlsxwriter as xlsxwriter
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from cargosystem.settings import BASE_DIR
from expaerea.models import ExportEmbarqueaereo, ExportConexaerea, ExportCargaaerea, ExportServiceaereo, ExportReservas, \
    VEmbarqueaereo, ExportServireserva, ExportConexreserva
from impomarit.models import VistaOperativas, VistaOperativasGastos
from mantenimientos.models import Clientes as SociosComerciales, Ciudades, Servicios
from cargosystem import settings
from mantenimientos.forms import add_buque_form, reporte_seguimiento_form, reporte_operativas_form
from seguimientos.models import Seguimiento, VGrillaSeguimientos, Envases, Conexaerea, Cargaaerea, Serviceaereo
from seguimientos.views.embarques import redondear_a_05_o_0
from seguimientos.views.guias import GuiasReport
from seguimientos.views.guias_hijas import GuiasReport as GuiasReportHijas


def reportes_seguimiento(request):
    try:
        if request.user.has_perms(["seguimientos.download_report", ]):
            ctx = {'form': reporte_seguimiento_form(),
                   'title_page': 'Reporte de seguimientos'}
            if request.method == 'POST':
                form = reporte_seguimiento_form(request.POST)
                if form.is_valid():
                    orden = []
                    desde = form.cleaned_data['desde']
                    hasta = form.cleaned_data['hasta']
                    modo = form.cleaned_data['modo']
                    operacion = form.cleaned_data['operacion']
                    vendedor = form.cleaned_data['vendedor']
                    tipo_de_operacion = form.cleaned_data['tipo_de_operacion']
                    origen = form.cleaned_data['origen']
                    destino = form.cleaned_data['destino']
                    status = form.cleaned_data['status']
                    buque = form.cleaned_data['buque']
                    cliente = form.cleaned_data['cliente']
                    embarcador = form.cleaned_data['embarcador']
                    consignatario = form.cleaned_data['consignatario']
                    if form.cleaned_data['filtro1']:
                        orden.append(form.cleaned_data['filtro1'])
                    if form.cleaned_data['filtro2']:
                        orden.append(form.cleaned_data['filtro2'])
                    if form.cleaned_data['filtro3']:
                        orden.append(form.cleaned_data['filtro3'])
                    if len(orden) == 0:
                        orden.append('fecha')
                    # Construye el filtro de consulta
                    filtro = {}
                    if desde:
                        filtro['fecha__gte'] = desde
                    if hasta:
                        filtro['fecha__lte'] = hasta
                    if modo:
                        filtro['modo__icontains'] = modo.upper()
                    if operacion:
                        filtro['modo__icontains'] = operacion.upper()
                    if vendedor:
                        filtro['vendedor_codigo'] = vendedor.codigo
                    if tipo_de_operacion:
                        filtro['operacion'] = tipo_de_operacion
                    if origen:
                        filtro['origen'] = origen.codigo
                    if destino:
                        filtro['destino'] = destino.codigo
                    if status:
                        filtro['status'] = status
                    if buque:
                        filtro['vapor_codigo'] = buque.codigo
                    if cliente:
                        filtro['cliente_codigo'] = cliente.codigo
                    if embarcador:
                        filtro['embarcador_codigo'] = embarcador.codigo
                    if consignatario:
                        filtro['consignatario_codigo'] = consignatario.codigo
                    # Realiza la consulta a la tabla Seguimientos con el filtro
                    resultados = VGrillaSeguimientos.objects.filter(**filtro).order_by(*orden)
                    if resultados.count() > 0:
                        return genero_xls_seguimientos(resultados,desde,hasta)
                    else:
                        messages.info(request,'No se encontraron resultados para la busqueda')
            return render(request, "seguimientos/reportes.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/")

def genero_xls_seguimientos(resultados,desde,hasta):
    try:
        name = 'Reporte_op_' + str(desde) + '_' + str(hasta)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Reporte')
        header_format = workbook.add_format({'bold': True, 'bg_color': '#0D6EFD', 'font_color': 'white'})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        row = 0
        col = 0
        for header in ['Seguimiento','Llegada','Modo', 'Cliente', 'Transportista', 'Conocimiento', 'House', 'Posicion', 'Vapor/Vuelo',
                       'Volumen', "20'", "40'", 'Contenedor','Origen','Destino']:
            worksheet.write(row, col, header, header_format)
            col += 1
        row += 1
        col = 0

        for p in resultados:
            cantidad_cntr = ""
            contenedores = ""
            mercaderias = ""
            precintos = ""
            bultos = 0
            peso = 0
            volumen = 0
            c20 = 0
            c40 = 0
            cant_cntr = Envases.objects.filter(numero=p.numero).values('tipo', 'nrocontenedor', 'precinto', 'bultos',
                                                                       'peso', 'envase', 'volumen', 'unidad').annotate(
                total=Count('id'))
            if cant_cntr.count() > 0:
                for cn in cant_cntr:
                    cantidad_cntr += f' {cn["total"]} x {cn["tipo"]} -'
                    contenedores += f' {cn["nrocontenedor"]} -'
                    if cn['precinto'] is not None and len(cn['precinto']) > 0:
                        precintos += f'{cn["precinto"]} - '
                    if cn['bultos'] is not None:
                        bultos += cn['bultos']
                    if cn['peso'] is not None:
                        peso += cn['peso']
                    if cn['volumen'] is not None:
                        volumen += cn['volumen']
                    if cn['envase'] is not None:
                        mercaderias += cn['envase'] + ' - '
                    if cn['unidad'] == '20':
                        c20 += 1
                    if cn['unidad'] == '40':
                        c40 += 1
            if p.modo in ['IMPORT AEREO', 'EXPORT AEREO']:
                vap = p.viaje
            else:
                vap = p.vapor
            ## DATOS
            worksheet.write(row, col, str(p.numero).zfill(8))
            col += 1
            worksheet.write(row, col, p.eta,date_format)
            col += 1
            worksheet.write(row, col, p.modo)
            col += 1
            worksheet.write(row, col, p.cliente)
            col += 1
            worksheet.write(row, col, p.transportista)
            col += 1
            worksheet.write(row, col, p.awb)
            col += 1
            worksheet.write(row, col, p.hawb)
            col += 1
            worksheet.write(row, col, p.posicion)
            col += 1
            worksheet.write(row, col, vap)
            col += 1
            worksheet.write(row, col, volumen)
            col += 1
            worksheet.write(row, col, c20)
            col += 1
            worksheet.write(row, col, c40)
            col += 1
            worksheet.write(row, col, contenedores[:-3])
            col += 1
            worksheet.write(row, col, p.origen_text)
            col += 1
            worksheet.write(row, col, p.destino_text)
            col = 0
            row += 1
        # Ajustar el ancho de las columnas automáticamente al contenido de texto
        for i, header in enumerate(['Seguimiento','Llegada', 'Cliente', 'Transportista', 'Conocimiento', 'House', 'Posicion', 'Vapor/Vuelo','Volumen', "20'", "40'", 'Contenedor', 'Entrega de vacío en patio']):
            max_len = max([len(str(header)) for p in resultados]) + 2  # Agregar un pequeño margen
            worksheet.set_column(i, i, max_len)
        file_name = 'filename=' + str(name) + '.xlsx'
        # Fijar la primera columna
        worksheet.freeze_panes(1, 1)
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; " + file_name + ""
        return response
    except Exception as e:
        raise TypeError(e)

def descargar_pdf(request, pdf_file_name):
    pdf_path = str(settings.BASE_DIR) + '/cargosystem/' +  str(os.path.join('media/pdf/', pdf_file_name))
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()
            return HttpResponse(pdf_data, content_type="application/pdf")
    except FileNotFoundError:
        raise Http404("El archivo PDF no se encontró")

def descargar_awb_seguimientos(request,row_id,draft=None):
    try:
        rep = GuiasReport()
        seg = Seguimiento.objects.get(id=row_id)
        """ CONSIGNATARIO """
        consignatario = SociosComerciales.objects.get(codigo=seg.consignatario)
        con = str(consignatario.razonsocial) + '<br />\n' + \
              str(consignatario.direccion) + '<br />\n' + \
              str(consignatario.ciudad) + '<br />\n' + \
              str(consignatario.pais) + ' RUT: ' + str(consignatario.ruc)
        rep.consignatario = con
        """ SHIPPER """
        shipper = SociosComerciales.objects.get(codigo=seg.embarcador)
        con = str(shipper.razonsocial) + '<br />\n' + \
              str(shipper.direccion) + '<br />\n' + \
              str(shipper.ciudad) + '<br />\n' + \
              str(shipper.pais) + ' RUT: ' + str(shipper.ruc)
        rep.shipper = con
        rep.shipper_nom = str(shipper.razonsocial)
        """ NOTIFY """
        notify = 'FREIGHT ' + str(seg.pago).upper() + '<br />\n'
        notificador = SociosComerciales.objects.get(codigo=seg.notificar)
        notify += 'NOTIFY: ' + str(notificador.razonsocial) + '<br />\n' + \
                  str(notificador.direccion) + '<br />\n' + \
                  str(notificador.ciudad) + '<br />\n' + \
                  str(notificador.pais) + ' RUT: ' + str(shipper.ruc)
        rep.notify = notify
        if seg.awb is not None and len(seg.awb) > 0:
            awb = seg.awb.split('-')
            rep.awb = awb[0] + '   MVD   ' + awb[1]
        if seg.hawb is not None and len(seg.hawb) > 0:
            rep.hawb = seg.hawb
        trasbordos = Conexaerea.objects.filter(numero=seg.numero).order_by('llegada','id')
        arraydestinos = []
        if trasbordos.exists():
            rep.routing += 'MONTEVIDEO (' + str(trasbordos[0].origen)
            rep.compania = trasbordos[0].cia
            rep.destino = str(trasbordos[0].destino)

            for index, x in enumerate(trasbordos):
                arraydestinos.append(str(x.destino) + '    ' + str(x.cia)[:2])

                fecha_str = f"{x.cia}{x.viaje}/{x.salida.strftime('%d-%B')[:6].upper()} "

                if index % 2 == 0:
                    rep.fechas += fecha_str
                else:
                    rep.fechas2 += fecha_str

                rep.routing += '/' + str(x.destino)
                rep.final = str(x.destino)

        arraydestinos.reverse()
        flag = 0
        if len(arraydestinos) > 0:
            for x in arraydestinos:
                if flag < 2:
                    rep.arraydestinos = x + '   ' + rep.arraydestinos
                    flag += 1
        if len(rep.routing) > 0:
            rep.routing += ')'
        ciudad = Ciudades.objects.filter(codigo=rep.final)
        if ciudad.count() > 0:
            rep.airport_final = ciudad[0].nombre
        rep.modopago = seg.pago
        if seg.pago == 'Collect':
            rep.pago = 'CC          C            C'
        else:
            rep.pago = 'PP    P           P'
        cargas = Cargaaerea.objects.filter(numero=seg.numero)
        if cargas.exists():
            # Inicializar acumuladores
            total_bultos = 0
            total_bruto = 0
            total_volumen = 0
            total_tarifa = seg.tarifaventa
            aplicable = 0
            total = 0
            productos = set()

            for x in cargas:
                total_bultos += x.bultos
                total_bruto += x.bruto

                volumen = x.bruto  # Por defecto, se usa el peso bruto si no se calcula el volumen

                if seg.tomopeso == 2 and x.medidas:
                    texto_medidas = '(' + str(x.bultos) + ') * ' + str(x.medidas) + ' MTS'
                    rep.medidas_text.append(texto_medidas)
                    medidas = x.medidas.split('*')
                    if len(medidas) == 3 and all(m.isdigit() for m in medidas):
                        volumen = float(medidas[0]) * float(medidas[1]) * float(medidas[2]) * 166.67
                        total_volumen += redondear_a_05_o_0(volumen)
                    else:
                        volumen = 'Error en medidas'

                productos.add(x.producto.descripcion)
            total = 0
            if seg.aplicable is not None:
                aplicable = seg.aplicable
                total += round(aplicable * float(total_tarifa), 2)
            # Guardar solo un registro con los totales
            rep.mercaderias.append([
                total_bultos, total_bruto, 'K', '',
                total_volumen if seg.tomopeso == 2 else total_bruto,
                total_tarifa, aplicable, total,
                ', '.join(productos)  # Unir los productos en una sola cadena
            ])

        rep.posicion = seg.posicion
        """ GASTOS """
        gastos = Serviceaereo.objects.filter(numero=seg.numero)

        if gastos.count() > 0:
            for g in gastos:
                if g.modo == 'Collect':
                    if g.tipogasto == 'OTHER':
                        rep.othcol += g.precio
                        rep.total_precio_c += g.precio
                    elif g.tipogasto == 'DUE CARRIER':
                        rep.carriercol += g.precio
                        rep.total_precio_c += g.precio
                    elif g.tipogasto == 'TAX':
                        rep.taxcol += g.precio
                        rep.total_precio_c += g.precio
                    elif g.tipogasto == 'VALUATION CHARGES':
                        rep.valcol += g.precio
                        rep.total_precio_c += g.precio

                    servicio = Servicios.objects.get(codigo=g.servicio).nombre
                    rep.otros_gastos += str(servicio if servicio else None) + ' ' + str(
                        round(g.precio, 2)) + '&nbsp;&nbsp;&nbsp;'
                else:
                    if g.tipogasto == 'OTHER':
                        rep.othppd += g.precio
                        rep.total_precio_p += g.precio
                    elif g.tipogasto == 'DUE CARRIER':
                        rep.carrierppd += g.precio
                        rep.total_precio_p += g.precio
                    elif g.tipogasto == 'TAX':
                        rep.taxppd += g.precio
                        rep.total_precio_p += g.precio
                    elif g.tipogasto == 'VALUATION CHARGES':
                        rep.valppd += g.precio
                        rep.total_precio_p += g.precio

                    servicio = Servicios.objects.get(codigo=g.servicio).nombre
                    rep.otros_gastos += str(servicio if servicio else None) + ' ' + str(
                        round(g.precio, 2)) + '&nbsp;&nbsp;&nbsp;'

        """ OUTPUT """
        name = 'HWBL_' + str(seg.numero)
        output = str(BASE_DIR) + '/archivos/' + name + '.pdf'
        if draft is not None:
            rep.generar_awb(output, fondo='carrier_hawb.jpg')
            rep.generar_awb(output, fondo='dorso01.jpg', dorso=1)
            rep.generar_awb(output, fondo='consignee.jpg')
            rep.generar_awb(output, fondo='dorso02.jpg', dorso=1)
            rep.generar_awb(output, fondo='shipper.jpg')
            rep.generar_awb(output, fondo='dorso03.jpg', dorso=1)
            rep.generar_awb(output, fondo='delivery_receipt.jpg')
            rep.generar_awb(output, fondo='dorso04.jpg', dorso=1)
            rep.generar_awb(output, fondo='copia1.jpg')
            rep.generar_awb(output, fondo='dorso11.jpg', dorso=1)
            rep.generar_awb(output, fondo='copia2.jpg')
            rep.generar_awb(output, fondo='dorso12.jpg', dorso=1)
            rep.generar_awb(output, fondo='copia3.jpg')
            rep.generar_awb(output, fondo='dorso13.jpg', dorso=1)
            rep.generar_awb(output, fondo='copia4.jpg')
            rep.generar_awb(output, fondo='dorso14.jpg', dorso=1)
            rep.generar_awb(output, fondo='copia5.jpg')
            rep.generar_awb(output, fondo='dorso15.jpg', dorso=1)
            rep.generar_awb(output, fondo='copia6.jpg')
            rep.generar_awb(output, fondo='dorso16.jpg', dorso=1)
        else:
            rep.generar_awb(output)

        return rep.descargo_archivo(output)


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        import traceback
        print(traceback.format_exc())
        raise Http404(f"Error: {str(e)}")

def descargar_awb_operativas(request,row_id,draft=None):
    try:
        rep = GuiasReport()
        master = ExportReservas.objects.get(numero=row_id)
        houses = ExportEmbarqueaereo.objects.filter(awb=master.awb)


        """ CONSIGNATARIO """
        consignatario = SociosComerciales.objects.get(codigo=master.consignatario)
        con = str(consignatario.razonsocial) + '<br />\n' + \
              str(consignatario.direccion) + '<br />\n' + \
              str(consignatario.ciudad) + '<br />\n' + \
              str(consignatario.pais) + ' RUT: ' + str(consignatario.ruc)
        rep.consignatario = con
        """ SHIPPER """
        shipper = SociosComerciales.objects.get(codigo=master.transportista)
        con = str(shipper.razonsocial) + '<br />\n' + \
              str(shipper.direccion) + '<br />\n' + \
              str(shipper.ciudad) + '<br />\n' + \
              str(shipper.pais) + ' RUT: ' + str(shipper.ruc)
        rep.shipper = con
        rep.shipper_nom = str(shipper.razonsocial)
        """ NOTIFY """
        pago = 'COLLECT' if master.pagoflete == 'C' else 'PREPAID'
        notify = 'FREIGHT ' + pago + '<br />\n'
        notificador = SociosComerciales.objects.get(codigo=master.consignatario)
        notify += 'NOTIFY: ' + str(notificador.razonsocial) + '<br />\n' + \
                  str(notificador.direccion) + '<br />\n' + \
                  str(notificador.ciudad) + '<br />\n' + \
                  str(notificador.pais) + ' RUT: ' + str(notificador.ruc)
        rep.notify = notify
        if master.awb is not None and len(master.awb) > 0 and master.awb != 'S/I':
            awb = master.awb.split('-')
            rep.awb = awb[0] + '   MVD   ' + awb[1]
            rep.awb_sf=master.awb

        #if houses[0].hawb is not None and len(houses[0].hawb) > 0 and houses[0].hawb != 'S/I':
            #rep.hawb = houses[0].hawb
        trasbordos = ExportConexreserva.objects.filter(numero=master.numero).order_by('llegada', 'id')
        arraydestinos = []

        if trasbordos.exists():
            rep.routing += 'MONTEVIDEO (' + str(trasbordos[0].origen)
            rep.compania = trasbordos[0].ciavuelo
            rep.destino = str(trasbordos[0].destino)

            for index, x in enumerate(trasbordos):
                arraydestinos.append(str(x.destino) + '    ' + str(x.ciavuelo)[:2])

                fecha_str = f"{x.ciavuelo}{x.vuelo}/{x.salida.strftime('%d-%B')[:6].upper()} "

                if index % 2 == 0:
                    rep.fechas += fecha_str
                else:
                    rep.fechas2 += fecha_str

                rep.routing += '/' + str(x.destino)
                rep.final = str(x.destino)

        arraydestinos.reverse()
        flag = 0
        if len(arraydestinos) > 0:
            for x in arraydestinos:
                if flag < 2:
                    rep.arraydestinos = x + '   ' + rep.arraydestinos
                    flag += 1
        if len(rep.routing) > 0:
            rep.routing += ')'
        ciudad = Ciudades.objects.filter(codigo=rep.final)
        if ciudad.count() > 0:
            rep.airport_final = ciudad[0].nombre
        rep.modopago = 'Collect' if master.pagoflete == 'C' else 'Prepaid'
        if master.pagoflete == 'C':
            rep.pago = 'CC          C            C'
        else:
            rep.pago = 'PP    P           P'
        cargas = ExportCargaaerea.objects.filter(numero=houses[0].numero)

        if cargas.exists():
            # Inicializar acumuladores
            total_bultos = 0
            total_bruto = 0
            total_volumen = 0
            total_tarifa = master.tarifaawb
            aplicable = 0
            total = 0
            productos = set()

            for x in cargas:
                total_bultos += x.bultos
                total_bruto += x.bruto

                volumen = x.bruto  # Por defecto, se usa el peso bruto si no se calcula el volumen

                if houses[0].tomopeso == 2 and x.medidas:
                    texto_medidas = '(' + str(x.bultos) + ') * ' + str(x.medidas)+' MTS'
                    rep.medidas_text.append(texto_medidas)
                    medidas = x.medidas.split('*')
                    if len(medidas) == 3 and all(m.isdigit() for m in medidas):
                        volumen = float(medidas[0]) * float(medidas[1]) * float(medidas[2]) * 166.67
                        total_volumen += redondear_a_05_o_0(volumen)
                    else:
                        volumen = 'Error en medidas'

                productos.add(x.producto.descripcion)
            total=0
            if master.aplicable is not None:
                aplicable = master.aplicable
                total += round(aplicable * float(total_tarifa), 2)
            # Guardar solo un registro con los totales
            rep.mercaderias.append([
                total_bultos, total_bruto, 'K', '',
                total_volumen if houses[0].tomopeso == 2 else total_bruto,
                total_tarifa,aplicable, total,
                ', '.join(productos)  # Unir los productos en una sola cadena
            ])

        rep.posicion = master.posicion
        """ GASTOS """
        gastos = ExportServireserva.objects.filter(numero=master.numero)

        if gastos.count() > 0:
            for g in gastos:
                if g.modo == 'Collect':
                    if g.tipogasto == 'OTHER':
                        rep.othcol+=g.costo
                        rep.total_precio_c+=g.costo
                    elif g.tipogasto == 'DUE CARRIER':
                        rep.carriercol += g.costo
                        rep.total_precio_c+=g.costo
                    elif g.tipogasto == 'TAX':
                        rep.taxcol += g.costo
                        rep.total_precio_c+=g.costo
                    elif g.tipogasto == 'VALUATION CHARGES':
                        rep.valcol += g.costo
                        rep.total_precio_c+=g.costo

                    servicio = Servicios.objects.get(codigo=g.servicio).nombre
                    rep.otros_gastos += str(servicio if servicio else None)+' '+str(round(g.costo,2)) +'&nbsp;&nbsp;&nbsp;'
                else:
                    if g.tipogasto == 'OTHER':
                        rep.othppd+=g.costo
                        rep.total_precio_p+=g.costo
                    elif g.tipogasto == 'DUE CARRIER':
                        rep.carrierppd += g.costo
                        rep.total_precio_p+=g.costo
                    elif g.tipogasto == 'TAX':
                        rep.taxppd += g.costo
                        rep.total_precio_p+=g.costo
                    elif g.tipogasto == 'VALUATION CHARGES':
                        rep.valppd += g.costo
                        rep.total_precio_p+=g.costo

                    servicio = Servicios.objects.get(codigo=g.servicio).nombre
                    rep.otros_gastos += str(servicio if servicio else None) +' '+ str(round(g.costo, 2)) + '&nbsp;&nbsp;&nbsp;'


        """ OUTPUT """
        name = 'HWBL_' + str(master.numero)
        output = str(BASE_DIR) + '/archivos/' + name + '.pdf'
        if draft is not None:
            rep.generar_awb(output,fondo='carrier_hawb.jpg')
            rep.generar_awb(output,fondo='dorso01.jpg',dorso=1)
            rep.generar_awb(output,fondo='consignee.jpg')
            rep.generar_awb(output,fondo='dorso02.jpg',dorso=1)
            rep.generar_awb(output,fondo='shipper.jpg')
            rep.generar_awb(output,fondo='dorso03.jpg',dorso=1)
            rep.generar_awb(output,fondo='delivery_receipt.jpg')
            rep.generar_awb(output,fondo='dorso04.jpg',dorso=1)
            rep.generar_awb(output,fondo='copia1.jpg')
            rep.generar_awb(output,fondo='dorso11.jpg',dorso=1)
            rep.generar_awb(output,fondo='copia2.jpg')
            rep.generar_awb(output,fondo='dorso12.jpg',dorso=1)
            rep.generar_awb(output,fondo='copia3.jpg')
            rep.generar_awb(output,fondo='dorso13.jpg',dorso=1)
            rep.generar_awb(output,fondo='copia4.jpg')
            rep.generar_awb(output,fondo='dorso14.jpg',dorso=1)
            rep.generar_awb(output,fondo='copia5.jpg')
            rep.generar_awb(output,fondo='dorso15.jpg',dorso=1)
            rep.generar_awb(output,fondo='copia6.jpg')
            rep.generar_awb(output,fondo='dorso16.jpg',dorso=1)
        else:
            rep.generar_awb(output)


        return rep.descargo_archivo(output)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        import traceback
        print(traceback.format_exc())
        raise Http404(f"Error: {str(e)}")

def descargar_hawb_operativas(request,row_id,draft=None,asagreed=None):
    try:
        rep = GuiasReportHijas()
        house = ExportEmbarqueaereo.objects.get(numero=row_id)
        tarifa = ExportReservas.objects.get(posicion=house.posicion).tarifaawb


        """ CONSIGNATARIO """
        consignatario = SociosComerciales.objects.get(codigo=house.consignatario)
        con = str(consignatario.razonsocial) + '<br />\n' + \
              str(consignatario.direccion) + '<br />\n' + \
              str(consignatario.ciudad) + '<br />\n' + \
              str(consignatario.pais) + ' RUT: ' + str(consignatario.ruc)
        rep.consignatario = con
        """ SHIPPER """
        shipper = SociosComerciales.objects.get(codigo=house.cliente)
        con = str(shipper.razonsocial) + '<br />\n' + \
              str(shipper.direccion) + '<br />\n' + \
              str(shipper.ciudad) + '<br />\n' + \
              str(shipper.pais) + ' RUT: ' + str(shipper.ruc)
        rep.shipper = con
        rep.shipper_nom = str(shipper.razonsocial)
        """ NOTIFY """
        pago = 'COLLECT' if house.pagoflete == 'C' else 'PREPAID'
        notify = 'FREIGHT ' + pago + '<br />\n'
        notificador = SociosComerciales.objects.get(codigo=house.consignatario)
        notify += 'NOTIFY: ' + str(notificador.razonsocial) + '<br />\n' + \
                  str(notificador.direccion) + '<br />\n' + \
                  str(notificador.ciudad) + '<br />\n' + \
                  str(notificador.pais) + ' RUT: ' + str(notificador.ruc)
        rep.notify = notify
        if house.awb is not None and len(house.awb) > 0 and house.awb != 'S/I':
            awb = house.awb.split('-')
            rep.awb = awb[0] + '   MVD   ' + awb[1]
            rep.awb_sf=house.awb

        if house.hawb is not None and len(house.hawb) > 0 and house.hawb != 'S/I':
            rep.hawb = house.hawb

        trasbordos = ExportConexaerea.objects.filter(numero=house.numero).order_by('llegada', 'id')
        arraydestinos = []

        if trasbordos.exists():
            rep.routing += 'MONTEVIDEO (' + str(trasbordos[0].origen)
            rep.compania = trasbordos[0].ciavuelo
            rep.destino = str(trasbordos[0].destino)

            for index, x in enumerate(trasbordos):
                arraydestinos.append(str(x.destino) + '    ' + str(x.ciavuelo)[:2])

                fecha_str = f"{x.ciavuelo}{x.vuelo}/{x.salida.strftime('%d-%B')[:6].upper()} "

                if index % 2 == 0:
                    rep.fechas += fecha_str
                else:
                    rep.fechas2 += fecha_str

                rep.routing += '/' + str(x.destino)
                rep.final = str(x.destino)

        arraydestinos.reverse()
        flag = 0
        if len(arraydestinos) > 0:
            for x in arraydestinos:
                if flag < 2:
                    rep.arraydestinos = x + '   ' + rep.arraydestinos
                    flag += 1
        if len(rep.routing) > 0:
            rep.routing += ')'
        ciudad = Ciudades.objects.filter(codigo=rep.final)
        if ciudad.count() > 0:
            rep.airport_final = ciudad[0].nombre
        rep.modopago = 'Collect' if house.pagoflete == 'C' else 'Prepaid'
        if house.pagoflete == 'C':
            rep.pago = 'CC          C            C'
        else:
            rep.pago = 'PP    P           P'
        cargas = ExportCargaaerea.objects.filter(numero=house.numero)

        if cargas.exists():
            # Inicializar acumuladores
            total_bultos = 0
            total_bruto = 0
            total_volumen = 0
            total_tarifa = house.tarifaventa
            aplicable = 0
            total = 0
            productos = set()
            vol=0

            for x in cargas:
                total_bultos += x.bultos
                total_bruto += x.bruto

                volumen = x.bruto  # Por defecto, se usa el peso bruto si no se calcula el volumen

                if house.tomopeso == 2 and x.medidas:
                    texto_medidas = '(' + str(x.bultos) + ') * ' + str(x.medidas)+' MTS'
                    rep.medidas_text.append(texto_medidas)
                    medidas = x.medidas.split('*')
                    if len(medidas) == 3:
                        vol+= float(medidas[0]) * float(medidas[1]) * float(medidas[2])
                        volumen = float(medidas[0]) * float(medidas[1]) * float(medidas[2]) * 166.67
                        total_volumen += redondear_a_05_o_0(volumen)
                    else:
                        volumen = 'Error en medidas'

                productos.add(x.producto.nombre)

            aplicable = total_volumen
            rep.volumen_total_embarque=vol
            total += round(aplicable * float(total_tarifa), 2)
            # Guardar solo un registro con los totales
            rep.mercaderias.append([
                total_bultos, total_bruto, 'K', '',
                total_volumen if house.tomopeso == 2 else total_bruto,
                total_tarifa,aplicable, total,
                productos  # Unir los productos en una sola cadena
            ])


        rep.posicion = house.posicion
        """ GASTOS """
        gastos = ExportServiceaereo.objects.filter(numero=house.numero)


        if gastos.count() > 0:
            for g in gastos:
                if g.modo == 'C':
                    if g.tipogasto == 'OTHER' and g.precio!=0:
                        rep.othcol+=g.precio
                        rep.total_precio_c+=g.precio
                    elif g.tipogasto == 'DUE CARRIER' and g.precio!=0:
                        rep.carriercol += g.precio
                        rep.total_precio_c+=g.precio
                    elif g.tipogasto == 'DUE AGENT' and g.precio!=0:
                        rep.agentcol += g.precio
                        rep.total_precio_c+=g.precio

                    rep.otros_gastos += str(round(g.precio,2)) +'&nbsp;&nbsp;&nbsp;'
                else:
                    if g.tipogasto == 'OTHER' and g.precio!=0:
                        rep.othppd+=g.precio
                        rep.total_precio_p+=g.precio
                    elif g.tipogasto == 'DUE CARRIER' and g.precio!=0:
                        rep.carrierppd += g.precio
                        rep.total_precio_p+=g.precio
                    elif g.tipogasto == 'DUE AGENT' and g.precio!=0:
                        rep.agentppd += g.precio
                        rep.total_precio_p+=g.precio

                    if g.precio !=0:
                        rep.otros_gastos += str(round(g.precio, 2)) + '&nbsp;&nbsp;&nbsp;'


        """ OUTPUT """
        name = 'HWBL_' + str(house.numero)
        output = str(BASE_DIR) + '/archivos/' + name + '.pdf'
        if draft is not None:
            rep.generar_awb(output,fondo='carrier_hawb.jpg')
            rep.generar_awb(output,fondo='dorso01.jpg',dorso=1)
            rep.generar_awb(output,fondo='consignee.jpg')
            rep.generar_awb(output,fondo='dorso02.jpg',dorso=1)
            rep.generar_awb(output,fondo='shipper.jpg')
            rep.generar_awb(output,fondo='dorso03.jpg',dorso=1)
            rep.generar_awb(output,fondo='delivery_receipt.jpg')
            rep.generar_awb(output,fondo='dorso04.jpg',dorso=1)
            rep.generar_awb(output,fondo='copia1.jpg')
            rep.generar_awb(output,fondo='dorso11.jpg',dorso=1)
            rep.generar_awb(output,fondo='copia2.jpg')
            rep.generar_awb(output,fondo='dorso12.jpg',dorso=1)
            rep.generar_awb(output,fondo='copia3.jpg')
            rep.generar_awb(output,fondo='dorso13.jpg',dorso=1)
            rep.generar_awb(output,fondo='copia4.jpg')
            rep.generar_awb(output,fondo='dorso14.jpg',dorso=1)
            rep.generar_awb(output,fondo='copia5.jpg')
            rep.generar_awb(output,fondo='dorso15.jpg',dorso=1)
            rep.generar_awb(output,fondo='copia6.jpg')
            rep.generar_awb(output,fondo='dorso16.jpg',dorso=1)
        else:
            rep.generar_awb(output)


        return rep.descargo_archivo(output)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        import traceback
        print(traceback.format_exc())
        raise Http404(f"Error: {str(e)}")


def reportes_operativas(request):
    try:
        if request.user.has_perms(["operativas.download_report", ]):
            ctx = {'form': reporte_operativas_form(),
                   'title_page': 'Reporte de operativas'}
            if request.method == 'POST':
                form = reporte_operativas_form(request.POST)

                if form.is_valid():

                    selected_columns = request.POST.get('selected_columns')
                    if selected_columns:
                        selected_columns = json.loads(selected_columns)

                    orden = []
                    desde = form.cleaned_data['desde']
                    hasta = form.cleaned_data['hasta']
                    modo = form.cleaned_data['modo']
                    operacion = form.cleaned_data['operacion']
                    vendedor = form.cleaned_data['vendedor']
                    tipo_de_operacion = form.cleaned_data['tipo_de_operacion']
                    origen = form.cleaned_data['origen']
                    destino = form.cleaned_data['destino']
                    status = form.cleaned_data['status']
                    cliente = form.cleaned_data['cliente']
                    embarcador = form.cleaned_data['embarcador']
                    consignatario = form.cleaned_data['consignatario']
                    transportista = form.cleaned_data['transportista']
                    if form.cleaned_data['filtro1']:
                        orden.append(form.cleaned_data['filtro1'])
                    if form.cleaned_data['filtro2']:
                        orden.append(form.cleaned_data['filtro2'])
                    if form.cleaned_data['filtro3']:
                        orden.append(form.cleaned_data['filtro3'])
                    if len(orden) == 0:
                        orden.append('fecha_embarque')
                    # Construye el filtro de consulta
                    filtro = {}
                    filtro2 = {}
                    if desde:
                        filtro['fecha_embarque__gte'] = desde
                        filtro2['fecha_embarque__gte'] = desde
                    if hasta:
                        filtro['fecha_retiro__lte'] = hasta
                        filtro2['fecha_retiro__lte'] = hasta
                    if modo:
                        filtro['modo'] = modo
                        filtro2['tipo'] = modo
                    if operacion:
                        filtro['tipo_operacion'] = operacion
                        filtro2['operacion'] = operacion
                    if vendedor:
                        filtro['nrovendedor'] = vendedor.codigo
                    if tipo_de_operacion:
                        filtro['operacion'] = tipo_de_operacion
                    if origen:
                        filtro['origen'] = origen.codigo
                    if destino:
                        filtro['destino'] = destino.codigo
                    if status:
                        filtro['status'] = status
                    if cliente:
                        filtro['nrocliente'] = cliente.codigo
                    if embarcador:
                        filtro['nroembarcador'] = embarcador.codigo
                    if consignatario:
                        filtro['nroconsignatario'] = consignatario.codigo
                    if transportista:
                        filtro['nrotransportista'] = transportista.codigo
                    # Realiza la consulta a la tabla Seguimientos con el filtro
                    resultados = VistaOperativas.objects.filter(**filtro).order_by(*orden)
                    gastos = VistaOperativasGastos.objects.filter(**filtro2).order_by('fecha_embarque')
                    if resultados.count() > 0 and gastos.count()> 0:
                        return genero_xls_operativas(resultados,desde,hasta,selected_columns,gastos)
                    else:
                        messages.info(request,'No se encontraron resultados para la busqueda')
            return render(request, "seguimientos/reportes_op.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/")


def genero_xls_operativas(resultados, desde, hasta, columnas,gastos):
    try:
        name = 'Reporte_op_' + str(desde) + '_' + str(hasta)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Reporte')
        header_format = workbook.add_format({'bold': True, 'bg_color': '#0D6EFD', 'font_color': 'white'})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        gastos_dict = {
            (gasto.tipo, gasto.operacion, gasto.numero): gasto
            for gasto in gastos
        }
        # Escribir encabezados
        row = 0
        col = 0
        for header in columnas:
            worksheet.write(row, col, header, header_format)
            col += 1

        row += 1

        # Recorrer los resultados y generar los datos en función de las columnas seleccionadas
        for p in resultados:
            datos_finales = []  # Vector temporal para almacenar los datos de una fila
            clave_gasto = (p.modo.lower(), p.tipo_operacion.lower(), str(p.numero))
            gasto_correspondiente = gastos_dict.get(clave_gasto)

            for columna in columnas:
                if columna == 'Numero':
                    datos_finales.append(str(p.numero).zfill(8))
                elif columna == 'Embarque':
                    datos_finales.append(p.fecha_embarque if p.fecha_embarque else None)
                elif columna == 'Llegada':
                    datos_finales.append(p.fecha_retiro if p.fecha_retiro else None)
                elif columna == 'Origen':
                    datos_finales.append(p.origen)
                elif columna == 'Destino':
                    datos_finales.append(p.destino)
                elif columna == 'Cliente':
                    datos_finales.append(p.cliente)
                elif columna == 'Transportista':
                    datos_finales.append(p.transportista)
                elif columna == 'Conocimiento':
                    datos_finales.append(str(p.master.awb)+str(p.house))
                elif columna == 'Tipo':
                    if p.tipo==0:
                        valor = 'Consolidado'
                    else:
                        valor='Directo'
                    datos_finales.append(valor)
                elif columna == 'House':
                    datos_finales.append(p.house)
                elif columna == 'Pago':
                    if p.pago=='C':
                        valor = 'Collect'
                    else:
                        valor = 'Prepaid'
                    datos_finales.append(valor)
                elif columna == 'Flete':
                    datos_finales.append(p.flete)
                elif columna == 'Otros Ingresos':
                    # datos_finales.append(p.otros_ingresos)
                    datos_finales.append('S/I')
                elif columna == 'Costo':
                    datos_finales.append('S/I')
                    # datos_finales.append('costo')
                elif columna == 'Otros Egresos':
                    # datos_finales.append(p.otros_egresos)
                    datos_finales.append('S/I')
                elif columna == 'Profit Final':
                    # datos_finales.append(p.profit_final)
                    datos_finales.append('S/I')
                elif columna == 'Precio Vendido':
                    datos_finales.append('S/I')
                    # datos_finales.append(gasto_correspondiente.precio)
                elif columna == 'Bultos':
                    datos_finales.append(p.bultos)
                elif columna == 'Peso Bruto':
                    datos_finales.append(p.peso_bruto)
                elif columna == 'Volumen':
                    datos_finales.append(p.volumen)
                elif columna == 'Aplicable':
                    datos_finales.append(p.aplicable)
                elif columna == 'Agente':
                    datos_finales.append(p.agente)
                elif columna == 'Consignatario':
                    datos_finales.append(p.consignatario)
                elif columna == 'Embarcador':
                    datos_finales.append(p.embarcador)
                elif columna == 'Vendedor':
                    datos_finales.append(p.vendedor)
                elif columna == 'User':
                    datos_finales.append('S/I')
                    # datos_finales.append(p.user)
                elif columna == 'Vapor/Vuelo':
                    datos_finales.append(p.vapor)
                elif columna == 'Viaje':
                    datos_finales.append(p.viaje)
                elif columna == 'Tipo Contenedor':
                    datos_finales.append(p.tipo_contenedor)
                elif columna == 'Movimiento':
                    datos_finales.append(p.movimiento)
                elif columna == 'Contenedor':
                    datos_finales.append(p.contenedor)
                elif columna == 'Propio':
                    datos_finales.append(p.propio)
                elif columna == 'Cotizacion':
                    datos_finales.append(p.cotizacion)
                elif columna == 'Seguimiento':
                    datos_finales.append(p.seguimiento)
                elif columna == 'DUE Agent':
                    datos_finales.append(gasto_correspondiente.due_agent if gasto_correspondiente else None)
                    # datos_finales.append(p.due_agent)
                elif columna == 'DUE Carrier':
                    # datos_finales.append(p.due_carrier)
                    datos_finales.append(gasto_correspondiente.due_carrier if gasto_correspondiente else None)
                elif columna == 'Local Charges':
                    datos_finales.append(gasto_correspondiente.local_charges if gasto_correspondiente else None)
                elif columna == 'Otros':
                    datos_finales.append(gasto_correspondiente.others if gasto_correspondiente else None)
                elif columna == 'Producto':
                    datos_finales.append(p.producto)
                elif columna == 'Pais':
                    datos_finales.append(p.pais)
                elif columna == 'Fecha Facturacion':
                    datos_finales.append(p.fecha_facturacion if p.fecha_facturacion else '')
                elif columna == 'Customer':
                    datos_finales.append(p.customer)
                elif columna == 'Status':
                    datos_finales.append(p.status)
                elif columna == 'Despachante':
                    datos_finales.append(p.despachante)
                elif columna == 'Operacion':
                    datos_finales.append(p.tipo_operacion)
                elif columna == 'Volumen Total':
                    datos_finales.append(p.volumen_total)
                elif columna == 'Armador/Arribado Con':
                    datos_finales.append(p.armador)
                elif columna == 'Usuario':
                    datos_finales.append(p.usuario)
                elif columna == 'Loading':
                    datos_finales.append(p.loading)
                elif columna == 'Discharge':
                    datos_finales.append(p.discharge)

            col = 0
            for dato in datos_finales:
                if isinstance(dato, (datetime.date, datetime.datetime)):  # Verifica si es una fecha
                    worksheet.write_datetime(row, col, dato, date_format)
                else:
                    worksheet.write(row, col, dato)  # Escribe normalmente si no es fecha
                col += 1

            row += 1  # Incrementa la fila después de escribir los datos

        # Ajustar el ancho de las columnas automáticamente al contenido de texto
        for i, header in enumerate(columnas):
            max_len = max(len(str(header)), 10)  # Longitud mínima de 10
            worksheet.set_column(i, i, max_len)

        # Fijar la primera fila
        worksheet.freeze_panes(1, 0)

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f"attachment; filename={name}.xlsx"
        return response

    except Exception as e:
        raise TypeError(e)





# def genero_xls_operativas(resultados,desde,hasta,columnas):
#     try:
#         name = 'Reporte_op_' + str(desde) + '_' + str(hasta)
#         output = io.BytesIO()
#         workbook = xlsxwriter.Workbook(output, {'in_memory': True})
#         worksheet = workbook.add_worksheet('Reporte')
#         header_format = workbook.add_format({'bold': True, 'bg_color': '#0D6EFD', 'font_color': 'white'})
#         date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
#         row = 0
#         col = 0
#
#         for header in columnas:
#             worksheet.write(row, col, header, header_format)
#             col += 1
#
#         row += 1
#         col = 0
#
#         for p in resultados:
#             cantidad_cntr = ""
#             contenedores = ""
#             mercaderias = ""
#             precintos = ""
#             bultos = 0
#             peso = 0
#             volumen = 0
#             c20 = 0
#             c40 = 0
#             cant_cntr = Envases.objects.filter(numero=p.numero).values('tipo', 'nrocontenedor', 'precinto', 'bultos',
#                                                                        'peso', 'envase', 'volumen', 'unidad').annotate(
#                 total=Count('id'))
#             if cant_cntr.count() > 0:
#                 for cn in cant_cntr:
#                     cantidad_cntr += f' {cn["total"]} x {cn["tipo"]} -'
#                     contenedores += f' {cn["nrocontenedor"]} -'
#                     if cn['precinto'] is not None and len(cn['precinto']) > 0:
#                         precintos += f'{cn["precinto"]} - '
#                     if cn['bultos'] is not None:
#                         bultos += cn['bultos']
#                     if cn['peso'] is not None:
#                         peso += cn['peso']
#                     if cn['volumen'] is not None:
#                         volumen += cn['volumen']
#                     if cn['envase'] is not None:
#                         mercaderias += cn['envase'] + ' - '
#                     if cn['unidad'] == '20':
#                         c20 += 1
#                     if cn['unidad'] == '40':
#                         c40 += 1
#             if p.modo in ['IMPORT AEREO', 'EXPORT AEREO']:
#                 vap = p.viaje
#             else:
#                 vap = p.vapor
#             ## DATOS
#             worksheet.write(row, col, str(p.numero).zfill(8))
#             col += 1
#             worksheet.write(row, col, p.eta,date_format)
#             col += 1
#             worksheet.write(row, col, p.modo)
#             col += 1
#             worksheet.write(row, col, p.cliente)
#             col += 1
#             worksheet.write(row, col, p.transportista)
#             col += 1
#             worksheet.write(row, col, p.awb)
#             col += 1
#             worksheet.write(row, col, p.hawb)
#             col += 1
#             worksheet.write(row, col, p.posicion)
#             col += 1
#             worksheet.write(row, col, vap)
#             col += 1
#             worksheet.write(row, col, volumen)
#             col += 1
#             worksheet.write(row, col, c20)
#             col += 1
#             worksheet.write(row, col, c40)
#             col += 1
#             worksheet.write(row, col, contenedores[:-3])
#             col += 1
#             worksheet.write(row, col, p.origen_text)
#             col += 1
#             worksheet.write(row, col, p.destino_text)
#             col = 0
#             row += 1
#         # Ajustar el ancho de las columnas automáticamente al contenido de texto
#         for i, header in enumerate(['Seguimiento','Llegada', 'Cliente', 'Transportista', 'Conocimiento', 'House', 'Posicion', 'Vapor/Vuelo','Volumen', "20'", "40'", 'Contenedor', 'Entrega de vacío en patio']):
#             max_len = max([len(str(header)) for p in resultados]) + 2  # Agregar un pequeño margen
#             worksheet.set_column(i, i, max_len)
#         file_name = 'filename=' + str(name) + '.xlsx'
#         # Fijar la primera columna
#         worksheet.freeze_panes(1, 1)
#         workbook.close()
#         output.seek(0)
#         response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#         response['Content-Disposition'] = "attachment; " + file_name + ""
#         return response
#
#     except Exception as e:
#         raise TypeError(e)