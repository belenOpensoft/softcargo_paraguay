import io
from django.http import FileResponse, Http404
import os
import xlsxwriter as xlsxwriter
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from cargosystem.settings import BASE_DIR
from mantenimientos.models import Clientes as SociosComerciales, Ciudades
from cargosystem import settings
from mantenimientos.forms import add_buque_form, reporte_seguimiento_form
from seguimientos.models import Seguimiento, VGrillaSeguimientos, Envases, Conexaerea, Cargaaerea, Serviceaereo
from seguimientos.views.embarques import redondear_a_05_o_0
from seguimientos.views.guias import GuiasReport


def reportes_seguimiento(request):
    try:
        if request.user.has_perms(["seguimientos.add_", ]):
            ctx = {'form': reporte_seguimiento_form(),
                   'title_page': 'Reporte de operativas'}
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
        return HttpResponseRedirect("/reportes_seguimiento")

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

def descargar_hawb(request,row_id,draft=None):
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
        if trasbordos.count() > 0:
            rep.routing += 'MONTEVIDEO  (' + str(trasbordos[0].origen)
            rep.compania = trasbordos[0].cia
            rep.destino = str(trasbordos[0].destino)
            for x in trasbordos:
                arraydestinos.append(str(x.destino) + '    ' + str(x.cia))
                rep.fechas += str(x.cia) + str(x.vapor) + '/' + x.salida.strftime("%m-%B")[:6].upper() + ' '
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
        if cargas.count() > 0:
            for x in cargas:
                aux = [x.bultos,x.bruto,'K','']
                if seg.tomopeso == 2:
                    if x.medidas is not None and len(x.medidas) > 0:
                        medidas = x.medidas.split('*')
                        if len(medidas) == 3 and all(m is not None and m.isdigit() for m in medidas):
                            valor = float(medidas[0]) * float(medidas[1]) * float(medidas[2]) * 166.67
                            aux.append(str(redondear_a_05_o_0(valor)) + ' AS VOL')
                        else:
                            # Manejar el caso de error o valores faltantes
                            aux.append('Error en medidas')
                else:
                    aux.append(x.bruto)
                aux.append(seg.tarifaventa)
                if seg.aplicable is not None:
                    aux.append(round(seg.aplicable * seg.tarifaventa,2))
                else:
                    aux.append(0)
                aux.append(x.producto.descripcion)
                rep.mercaderias.append(aux)

        rep.posicion = seg.posicion
        """ GASTOS """
        gastos = Serviceaereo.objects.filter(numero=seg.numero)

        if gastos.count() > 0:
            for g in gastos:
                if g.modo == 'Collect':
                    if g.tipogasto == 'DUE AGENT':
                        rep.agentcol += g.precio
                    elif g.tipogasto == 'DUE CARRIER':
                        rep.carriercol += g.precio
                    elif g.tipogasto == 'TAX':
                        rep.taxcol += g.precio
                    elif g.tipogasto == 'VALUATION CHARGES':
                        rep.valcol += g.precio
                    else:
                        rep.othcol += g.precio
                else:
                    if g.tipogasto == 'DUE AGENT':
                        rep.agentppd += g.precio
                    elif g.tipogasto == 'DUE CARRIER':
                        rep.carrierppd += g.precio
                    elif g.tipogasto == 'TAX':
                        rep.taxppd += g.precio
                    elif g.tipogasto == 'VALUATION CHARGES':
                        rep.valppd += g.precio
                    else:
                        rep.othppd += g.precio

        """ OUTPUT """
        name = 'HWBL_' + str(seg.numero)
        output = str(BASE_DIR) + '/archivos/' + name + '.pdf'
        if draft is not None:
            rep.generar_hawb(output,fondo='carrier_hawb.jpg')
            rep.generar_hawb(output,fondo='consignee.jpg')
            rep.generar_hawb(output,fondo='shipper.jpg')
            rep.generar_hawb(output,fondo='delivery_receipt.jpg')
            rep.generar_hawb(output,fondo='normal.jpg')
        else:
            rep.generar_hawb(output)


        return rep.descargo_archivo(output)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise Http404(f"Error: {str(e)}")