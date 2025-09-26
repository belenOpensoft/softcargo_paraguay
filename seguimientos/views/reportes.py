import io
import json
import sys
from audioop import reverse
from decimal import Decimal
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from django.forms import model_to_dict
from django.http import FileResponse, Http404, HttpResponseBadRequest, JsonResponse
import os
import xlsxwriter as xlsxwriter
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from cargosystem.settings import BASE_DIR
from expaerea.models import ExportEmbarqueaereo, ExportConexaerea, ExportCargaaerea, ExportServiceaereo, ExportReservas, \
    VEmbarqueaereo, ExportServireserva, ExportConexreserva, GuiasHijas, GuiasMadres
from impomarit.models import VistaOperativas, VistaOperativasGastos
from mantenimientos.models import Clientes as SociosComerciales, Ciudades, Servicios
from cargosystem import settings
from mantenimientos.forms import add_buque_form, reporte_seguimiento_form, reporte_operativas_form
from seguimientos.models import Seguimiento, VGrillaSeguimientos, Envases, Conexaerea, Cargaaerea, Serviceaereo, \
    PreferenciasReporteOp
from seguimientos.views.embarques import redondear_a_05_o_0
from seguimientos.views.guias import GuiasReport
from seguimientos.views.guias_hijas import GuiasReport as GuiasReportHijas, validar_valor
from base64 import b64encode
import  datetime
from io import BytesIO


def reportes_seguimiento(request):
    try:
        if request.user.has_perms(["seguimientos.download_report", ]):
            rol = request.POST.get('rol') or request.GET.get('rol') or getattr(request, 'rol_pestana', None)

            ctx = {
                'form': reporte_seguimiento_form(),
                'title_page': 'Reporte de seguimientos',
                'rol': rol
            }

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

                    filtro = {}
                    if desde:
                        filtro['fecha__gte'] = desde
                    if hasta:
                        filtro['fecha__lte'] = hasta
                    if modo:
                        filtro['modo__icontains'] = modo.upper()
                    if operacion:
                        filtro['operacion__icontains'] = operacion.upper()
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

                    resultados = VGrillaSeguimientos.objects.filter(**filtro).order_by(*orden)
                    if resultados.count() > 0:
                        return genero_xls_seguimientos(resultados, desde, hasta)
                    else:
                        messages.info(request, 'No se encontraron resultados para la busqueda')
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
        con = str(consignatario.empresa) + '<br />\n' + \
              str(consignatario.direccion) + '<br />\n' + \
              str(consignatario.ciudad) + '<br />\n' + \
              str(consignatario.pais) + ' RUT: ' + str(consignatario.ruc)
        rep.consignatario = con
        """ SHIPPER """
        shipper = SociosComerciales.objects.get(codigo=seg.embarcador)
        con = str(shipper.empresa) + '<br />\n' + \
              str(shipper.direccion) + '<br />\n' + \
              str(shipper.ciudad) + '<br />\n' + \
              str(shipper.pais) + ' RUT: ' + str(shipper.ruc)
        rep.shipper = con
        rep.shipper_nom = str(shipper.empresa)
        """ NOTIFY """
        notify = 'FREIGHT ' + str(seg.pago).upper() + '<br />\n'
        notificador = SociosComerciales.objects.get(codigo=seg.notificar)
        notify += 'NOTIFY: ' + str(notificador.empresa) + '<br />\n' + \
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




def reportes_operativas(request):
    try:
        if not request.user.has_perms(["operativas.download_report"]):
            raise TypeError('No tiene permisos para realizar esta accion.')

        rol = request.POST.get('rol') or request.GET.get('rol') or getattr(request, 'rol_pestana', None)

        ctx = {
            'form': reporte_operativas_form(),
            'title_page': 'Reporte de operativas',
            'rol': rol,  # --> para el hidden
        }

        if request.method == 'POST':
            form = reporte_operativas_form(request.POST)
            if form.is_valid():
                # rol otra vez por si vino en POST
                rol = request.POST.get('rol') or request.GET.get('rol') or getattr(request, 'rol_pestana', None)

                selected_columns = request.POST.get('selected_columns')
                if selected_columns:
                    selected_columns = json.loads(selected_columns)

                orden = []
                desde = form.cleaned_data['desde'].strftime('%Y-%m-%d')
                hasta = form.cleaned_data['hasta'].strftime('%Y-%m-%d')
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
                if not orden:
                    orden.append('-fecha')

                filtro, filtro2 = {}, {}
                if desde:
                    filtro['eta__gte'] = desde
                    filtro2['eta__gte'] = desde
                if hasta:
                    filtro['eta__lte'] = hasta
                    filtro2['eta__lte'] = hasta
                if modo:
                    filtro['modo'] = modo
                    filtro2['tipo'] = modo
                if operacion:
                    filtro['tipo_operacion__iexact'] = operacion
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

                resultados_raw = VistaOperativas.objects.filter(**filtro).order_by(*orden)

                vistos = set()
                resultados = []
                for r in resultados_raw:
                    clave = (r.numero, r.modo, r.tipo_operacion)
                    if clave not in vistos:
                        vistos.add(clave)
                        resultados.append(r)

                gastos = VistaOperativasGastos.objects.filter(**filtro2).order_by('-fecha')

                if len(resultados) >0:
                    # Esto devuelve un HttpResponse (xlsx). No redirijas.
                    return genero_xls_operativas(resultados, desde, hasta, selected_columns, gastos)

                messages.info(request, 'No se encontraron resultados para la búsqueda')

            # si POST inválido, re-render con el form y rol
            ctx['form'] = form

        return render(request, "seguimientos/reportes_op.html", ctx)

    except Exception as e:
        messages.error(request, str(e))
        # si vas a redirigir, preservá el rol vos (no esperes al middleware)
        base = reverse('reportes_operativas')  # ajusta al nombre de tu url
        if rol := (request.POST.get('rol') or request.GET.get('rol') or getattr(request, 'rol_pestana', None)):
            return HttpResponseRedirect(f"{base}?rol={rol}")
        return HttpResponseRedirect(base)


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
                elif columna == 'Fecha':
                    datos_finales.append(p.fecha if p.fecha else None)
                elif columna == 'ETA':
                    datos_finales.append(p.eta if p.eta else None)
                elif columna == 'ETD':
                    datos_finales.append(p.etd if p.etd else None)
                elif columna == 'Llegada':
                    datos_finales.append(p.fecha_retiro if p.fecha_retiro else None)
                elif columna == 'Embarque':
                    datos_finales.append(p.fecha_embarque if p.fecha_embarque else None)
                elif columna == 'Origen':
                    datos_finales.append(p.origen)
                elif columna == 'Destino':
                    datos_finales.append(p.destino)
                elif columna == 'Cliente':
                    datos_finales.append(p.cliente)
                elif columna == 'Transportista':
                    datos_finales.append(p.transportista)
                elif columna == 'Conocimiento':
                    datos_finales.append(str(p.master))
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


def guardar_preferencia(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        selected_columns = request.POST.get("selected_columns", "")

        if not nombre:
            return HttpResponseBadRequest("El nombre es requerido.")
        if not selected_columns:
            return HttpResponseBadRequest("No se enviaron columnas seleccionadas.")

        try:
            columns_list = json.loads(selected_columns)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Formato de columnas seleccionado inválido.")

        preferencias_data = {
            "nombre": nombre,
            "selected_columns": columns_list
        }

        preferencias_json = json.dumps(preferencias_data)

        preferencia = PreferenciasReporteOp.objects.create(
            opciones=preferencias_json,
            usuario=request.user
        )

        return JsonResponse({
            "success": True,
            "preferencia_id": preferencia.id
        })
    else:
        return HttpResponseBadRequest("Método no permitido.")



def cargar_preferencias(request):
    if request.method == "GET":
        # Consulta las preferencias del usuario logueado
        preferencias = PreferenciasReporteOp.objects.filter(usuario=request.user)
        datos = []
        for pref in preferencias:
            try:
                # Parseamos el JSON que se guardó en el campo 'opciones'
                opciones_data = json.loads(pref.opciones)
                nombre = opciones_data.get("nombre", "Sin nombre")
                selected_columns = opciones_data.get("selected_columns", [])
            except Exception as e:
                nombre = "Sin nombre"
                selected_columns = []
            datos.append({
                "id": pref.id,
                "nombre": nombre,
                "selected_columns": selected_columns,
            })
        return JsonResponse({"preferencias": datos})
    else:
        return HttpResponseBadRequest("Método no permitido.")

def eliminar_preferencia(request):
    if request.method == "POST":
        pref_id = request.POST.get("id")
        if not pref_id:
            return HttpResponseBadRequest("Falta el parámetro 'id'.")
        try:
            # Asegúrate de que solo el usuario propietario pueda eliminar su preferencia
            preferencia = PreferenciasReporteOp.objects.get(id=pref_id, usuario=request.user)
            preferencia.delete()
            return JsonResponse({"success": True})
        except PreferenciasReporteOp.DoesNotExist:
            return JsonResponse({"error": "Preferencia no encontrada."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido."}, status=400)


#editar guias

def editar_hawb(request, row_id):
    try:
        imagen_path = os.path.join(settings.BASE_DIR,'cargosystem', 'static', 'images', 'guias', 'normal.jpg')


        if not os.path.exists(imagen_path):
            raise FileNotFoundError(f"No se encontró la imagen: {imagen_path}")

        with open(imagen_path, 'rb') as img_file:
            img_b64 = b64encode(img_file.read()).decode('utf-8')
        guias = GuiasHijas.objects.filter(numero=row_id).order_by('-fecha_ingreso')

        if guias.exists():
            guia_existente = guias.first()
            datos = model_to_dict(guia_existente)
        else:
            datos = obtener_datos_guia(row_id)
        return render(request, 'expaerea/editar_hawb.html', {
            'imagen': img_b64,
            'datos': datos,
            'row_id': row_id,
        })
    except Exception as e:
        messages.error(request,str(e))
        return HttpResponseRedirect('/')

def obtener_datos_guia(row_id):
    try:
        data = {
            'numero':row_id,
            'total_bultos': 0,
            'total_pesos': 0,
            'total_total': 0,
            'posicion': '',
            'consignatario':'',
            'shipper':'',
            'awb_sf':'',
            'awb1':'',
            'awb2':'',
            'awb3':'',
            'hawb':'',
            'empresa':'',
            'info':'',
            'vuelos1':'',
            'vuelos2':'',
            'airport_departure':'',
            'airport_final':'',
            'final':'',
            'by_cia_1':'',
            'by_cia_3':'',
            'by_cia_2':'',
            'to_1':'',
            'to_2':'',
            'by_first_carrier':'',
            'array_destinos':'',
            'modopago':'',
            'cc1': '',
            'cc2': '',
            'pp1': '',
            'pp2': '',
            'pago_code': '',
            'mercaderias': [],
            'medidas_text': [],
            'volumen_total_embarque': 0,
            'valppd': 0,
            'valcol': 0,
            'prepaid': 0,
            'collect': 0,
            'taxppd': 0,
            'taxcol': 0,
            'agentppd': 0,
            'agentcol': 0,
            'carrierppd': 0,
            'carriercol': 0,
            'total_prepaid': 0,
            'total_collect': 0,
            'otros_gastos': '',
            'shipper_signature': '',
            'carrier_signature': '',
            'amount_insurance': 'NIL',
            'handling': '',
            'declared_value_for_carriage': 'NVD',
            'declared_value_for_customs': 'NCV',
            'iata_code_agente': '',
            'account_nro': '',
            'notify': '',
            'currency': '',
        }

        house = ExportEmbarqueaereo.objects.get(numero=row_id)
        master = ExportReservas.objects.get(posicion=house.posicion)

        # CONSIGNATARIO
        consignatario = SociosComerciales.objects.get(codigo=house.consignatario)
        carrier = SociosComerciales.objects.get(codigo=house.transportista)
        shipper = SociosComerciales.objects.get(codigo=house.cliente)

        data['consignatario'] = f"{consignatario.empresa}\n{consignatario.direccion}\n{consignatario.ciudad}\n{consignatario.pais} RUT: {consignatario.ruc} PH: {consignatario.telefono}"
        data['empresa']=f"{shipper.empresa}\n{shipper.direccion}\n{shipper.ciudad}\n{shipper.pais} RUT: {shipper.ruc} PH: {shipper.telefono}"
        data['by_first_carrier']=carrier.empresa
        # SHIPPER
        data['shipper'] = settings.EMPRESA_HAWB_editar
        data['shipper_signature'] = str(shipper.empresa)
        data['carrier_signature'] = (
                "AS AGENT\nOF DE CARRIER " + str(carrier.empresa) + "\n" +
                datetime.datetime.now().strftime("%Y-%m-%d") + " MONTEVIDEO\n" +
                "OCEAN LINK LTDA / LLB"
        )

        data['currency']='USD' if master.moneda == 2 else 'UYU' if master.moneda == 1 else 'S/I'

        # NOTIFY
        pago = 'COLLECT' if house.pagoflete == 'C' else 'PREPAID'
        notificador = SociosComerciales.objects.get(codigo=house.consignatario)
        data['info'] = f"FREIGHT {pago}\nNOTIFY: {notificador.empresa}\n{notificador.direccion}\n{notificador.ciudad}\n{notificador.pais} RUT: {notificador.ruc} PH: {notificador.telefono}"

        # AWB y HAWB
        if house.awb and house.awb != 'S/I':
            awb = house.awb.split('-')
            data['awb1'] = awb[0]
            data['awb2'] = "MVD"
            data['awb3'] = awb[1]
            data['awb_sf'] = house.awb
        if house.hawb and house.hawb != 'S/I':
            data['hawb'] = house.hawb

        # TRANSBORDOS
        trasbordos = list(ExportConexaerea.objects.filter(numero=house.numero).order_by( 'id'))
        data['airport_departure'] = "MONTEVIDEO"
        data['vuelos1'] = ''
        data['vuelos2'] = ''
        data['array_destinos'] = ''
        data['to_1'] = ''
        data['to_2'] = ''
        data['to_3'] = ''
        data['by_cia'] = ''
        data['by_cia_2'] = ''
        data['by_cia_3'] = ''

        destinos = []

        if trasbordos:
            count = len(trasbordos)

            if count == 1:
                data['to_1'] = str(trasbordos[0].destino)
                data['by_cia_1'] = trasbordos[0].ciavuelo

            elif count == 2:
                data['to_1'] = str(trasbordos[0].destino)
                data['by_cia_1'] = trasbordos[0].ciavuelo

                data['to_2'] = str(trasbordos[1].destino)
                data['by_cia_2'] = trasbordos[1].ciavuelo

            elif count == 3:
                data['to_1'] = str(trasbordos[0].destino)
                data['by_cia_1'] = trasbordos[0].ciavuelo

                data['to_2'] = str(trasbordos[1].destino)
                data['by_cia_2'] = trasbordos[1].ciavuelo

                data['to_3'] = str(trasbordos[2].destino)
                data['by_cia_3'] = trasbordos[2].ciavuelo

            else:  # más de 3
                data['to_1'] = str(trasbordos[0].destino)
                data['by_cia_1'] = trasbordos[0].ciavuelo

                data['to_2'] = str(trasbordos[1].destino)
                data['by_cia_2'] = trasbordos[1].ciavuelo

                data['to_3'] = str(trasbordos[-1].destino)
                data['by_cia_3'] = trasbordos[-1].ciavuelo

            data['vuelos1'] = ''
            data['vuelos2'] = ''

            # if trasbordos:
            #     count = len(trasbordos)
            #
            #     if count == 1:
            #         x = trasbordos[0]
            #         data['vuelos1'] = f"{x.ciavuelo}{x.vuelo}/{x.salida.strftime('%d-%B')[:6].upper()} "
            #         data['final']=x.destino
            #
            #     elif count == 2:
            #         x1, x2 = trasbordos[0], trasbordos[1]
            #         data['vuelos1'] = f"{x1.ciavuelo}{x1.vuelo}/{x1.salida.strftime('%d-%B')[:6].upper()} "
            #         data['vuelos2'] = f"{x2.ciavuelo}{x2.vuelo}/{x2.salida.strftime('%d-%B')[:6].upper()} "
            #         data['final']=x2.destino
            #
            #     else:  # más de 2 vuelos
            #         x1, xN = trasbordos[0], trasbordos[-1]
            #         data['vuelos1'] = f"{x1.ciavuelo}{x1.vuelo}/{x1.salida.strftime('%d-%B')[:6].upper()} "
            #         data['vuelos2'] = f"{xN.ciavuelo}{xN.vuelo}/{xN.salida.strftime('%d-%B')[:6].upper()} "
            #         data['final']=xN.destino

            if trasbordos:
                def fmt(vuelo):
                    return f"{vuelo.ciavuelo}{vuelo.vuelo}/{vuelo.salida.strftime('%d-%B')[:6].upper()} "

                vuelos1 = []
                vuelos2 = []

                for idx, x in enumerate(trasbordos, start=1):
                    if idx % 2 == 1:  # impar → vuelos1
                        vuelos1.append(fmt(x))
                    else:  # par → vuelos2
                        vuelos2.append(fmt(x))

                data['vuelos1'] = "".join(vuelos1)
                data['vuelos2'] = "".join(vuelos2)
                data['final'] = trasbordos[-1].destino


        # data['airport_departure'] += ' (MVD/'+str(data['to_1'])+')'
        # Construir lista de destinos to_1, to_2, to_3... que no estén vacíos
        to_keys = sorted([k for k in data.keys() if k.startswith('to_')],
                         key=lambda x: int(x.split('_')[1]))
        tos = [str(data[k]).strip() for k in to_keys if data.get(k)]

        # Base del texto (por si airport_departure ya trae el nombre de la ciudad)
        base = data.get('airport_departure', '').strip()
        iata_origen = "MVD"

        if tos:
            data['airport_departure'] = f"{base} ({iata_origen}/" + "/".join(tos) + ")"
        else:
            # Si no hay to_*, solo muestra el IATA origen
            data['airport_departure'] = f"{base} ({iata_origen})"

        data['array_destinos'] = '   '.join(reversed(destinos[:2]))

        ciudad = Ciudades.objects.filter(codigo=data['final'])
        if ciudad.exists():
            data['airport_final'] = ciudad[0].nombre

        # PAGO
        data['modopago'] = 'Collect' if house.pagoflete == 'C' else 'Prepaid'
        if house.pagoflete=='C':
            data['pago_code']='CC'
            data['cc1']='C'
            data['cc2']='C'
        else:
            data['pago_code']='PP'
            data['pp1']='P'
            data['pp2']='P'

        #cargas y mercaderia
        cargas = ExportCargaaerea.objects.filter(numero=house.numero)
        data['mercaderias'] = []
        data['volumen_total_embarque'] = 0
        top_base = 1030
        incremento = 30


        from decimal import Decimal, ROUND_HALF_UP
        import re

        if cargas.exists():
            total_bultos = 0
            total_bruto = Decimal('0')
            total_aplicable = Decimal('0')  # suma de aplicables > 0
            volumen_total = Decimal('0')
            medidas_descripciones = []
            productos = set()

            # Acumular
            for carga in cargas:
                # bultos y bruto
                total_bultos += (carga.bultos or 0)
                total_bruto += Decimal(str(carga.bruto or 0))

                # productos (únicos)
                if getattr(carga, "producto", None) and getattr(carga.producto, "nombre", None):
                    productos.add(carga.producto.nombre)

                # medidas → volumen y descripción
                if carga.medidas:
                    medidas_descripciones.append(f"({carga.bultos}) * {carga.medidas} MTS")
                    # calcular volumen L*W*H (si viene bien formado)
                    partes = [p.strip() for p in str(carga.medidas).split('*')]
                    if len(partes) == 3:
                        try:
                            largo = Decimal(partes[0])
                            ancho = Decimal(partes[1])
                            alto = Decimal(partes[2])
                            # nota: si querés considerar bultos en el volumen, usar: * Decimal(carga.bultos or 0)
                            volumen_total += (largo * ancho * alto)
                        except Exception:
                            pass

                # aplicable
                total_aplicable=volumen_total*Decimal(166.67)

            # Asignar CBM total consolidado (y guardarlo también en data si lo usás en otros lados)
            data['volumen_total_embarque'] = float(volumen_total.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP))

            # Descripción consolidada (productos + CBM + medidas)
            productos_txt = "; ".join(sorted(productos)) if productos else "SIN NOMBRE"
            descripcion_unica = (
                    "CONTAIN:\n"
                    f"{productos_txt}\n"
                    f"{data['volumen_total_embarque']} CBM\n"
                    + ("\n".join(medidas_descripciones) if medidas_descripciones else "")
            )
            data['descripcion_mercaderias'] = descripcion_unica

            # Tarifa (guía hija)
            tarifa = Decimal(str(getattr(house, "tarifaventa", 0) or 0))

            # Regla MIN:
            # - si total_aplicable == 0  => aplicable = "MIN" y total = tarifa (una sola vez)
            # - si total_aplicable  > 0  => aplicable = suma aplicables, total = suma * tarifa
            if total_aplicable == 0:
                aplicable_display = "MIN"
                total_total = tarifa
            else:
                aplicable_display = total_aplicable.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                total_total = (total_aplicable * tarifa)

            # Normalizaciones
            total_total = total_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            total_bruto = total_bruto.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            # UNA sola línea en mercaderías
            data['mercaderias'] = [{
                'bultos': total_bultos,
                'peso': float(total_bruto),
                'unidad': 'K',
                'aplicable': aplicable_display,
                'tarifa': float(tarifa),
                'total': float(total_total),
                'descripcion': data['descripcion_mercaderias'],
                'top': top_base,  # una fila
            }]

            # Totales consolidados
            data['total_bultos'] = total_bultos
            data['total_pesos'] = float(total_bruto)
            data['total_total'] = float(total_total)

        data['posicion'] = house.posicion

        if house.pagoflete=='C':
            data['collect']=data['total_total']
        else:
            data['prepaid']=data['total_total']

        # GASTOS
        gastos = ExportServiceaereo.objects.filter(numero=house.numero)
        for g in gastos:
            if g.precio == 0:
                continue

            if g.modo == 'C':  # COLLECT
                if g.tipogasto == 'OTHER':
                    data['valcol'] += g.precio
                elif g.tipogasto == 'DUE CARRIER':
                    data['carriercol'] += g.precio
                elif g.tipogasto == 'DUE AGENT':
                    data['agentcol'] += g.precio
                data['total_collect'] += g.precio
            else:  # PREPAID
                if g.tipogasto == 'OTHER':
                    data['valppd'] += g.precio
                elif g.tipogasto == 'DUE CARRIER':
                    data['carrierppd'] += g.precio
                elif g.tipogasto == 'DUE AGENT':
                    data['agentppd'] += g.precio
                data['total_prepaid'] += g.precio

            data['otros_gastos'] += f"{round(g.precio, 2)}   "

            data['valcol']=round(Decimal(data['valcol']),2)
            data['valppd']=round(Decimal(data['valppd']),2)
            data['carriercol']=round(Decimal(data['carriercol']),2)
            data['carrierppd']=round(Decimal(data['carrierppd']),2)
            data['agentcol']=round(Decimal(data['agentcol']),2)
            data['agentppd']=round(Decimal(data['agentppd']),2)
            data['agentppd']=round(Decimal(data['agentppd']),2)
            data['total_prepaid']=round(Decimal(data['total_prepaid']),2)
            data['total_collect']=round(Decimal(data['total_collect']),2)

        if house.pagoflete=='C':
            data['total_collect'] += round(Decimal(data['collect'] or 0),2)
        else:
            data['total_prepaid'] += round(Decimal(data['prepaid'] or 0),2)


        return data

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise Http404(f"Error: {str(e)}")

def _is_as_agreed(val: str) -> bool:
    s = str(val or "").strip().upper().replace("_", " ").replace("-", " ")
    return s == "AS AGREED"

def _dec_or_none(val: str, default_zero=True):
    """
    - Si viene 'AS AGREED' -> devuelve None
    - Si viene vacío y default_zero=True -> 0
    - Si es número -> Decimal(valor)
    """
    if _is_as_agreed(val):
        return None
    s = (val or "").strip()
    if s == "":
        return Decimal("0") if default_zero else None
    return Decimal(s)

def guardar_hawb(request, row_id):
    if request.method == 'POST':
        try:
            guia = GuiasHijas()
            # Campos numéricos
            guia.total_bultos = int(request.POST.get("total_bultos", 0) or 0)
            guia.total_pesos = Decimal(request.POST.get("total_pesos", 0) or 0)
            guia.total_total = Decimal(request.POST.get("total_total", 0) or 0)
            guia.volumen_total_embarque = Decimal(request.POST.get("volumen_total_embarque", 0) or 0)
            guia.valppd = Decimal(request.POST.get("valppd", 0) or 0)
            guia.valcol = Decimal(request.POST.get("valcol", 0) or 0)
            guia.prepaid = Decimal(request.POST.get("prepaid", 0) or 0)
            guia.collect = Decimal(request.POST.get("collect", 0) or 0)
            guia.taxppd = Decimal(request.POST.get("taxppd", 0) or 0)
            guia.taxcol = Decimal(request.POST.get("taxcol", 0) or 0)
            guia.agentppd = Decimal(request.POST.get("agentppd", 0) or 0)
            guia.agentcol = Decimal(request.POST.get("agentcol", 0) or 0)
            guia.carrierppd = Decimal(request.POST.get("carrierppd", 0) or 0)
            guia.carriercol = Decimal(request.POST.get("carriercol", 0) or 0)
            guia.total_prepaid = Decimal(request.POST.get("total_prepaid", 0) or 0)
            guia.total_collect = Decimal(request.POST.get("total_collect", 0) or 0)

            # Campos de texto
            guia.posicion = request.POST.get("posicion", "")
            guia.consignatario = request.POST.get("consignatario", "")
            guia.shipper = request.POST.get("shipper", "")
            guia.awb_sf = request.POST.get("awb", "")
            guia.awb1 = request.POST.get("awb1", "")
            guia.awb2 = request.POST.get("awb2", "")
            guia.awb3 = request.POST.get("awb3", "")
            guia.hawb = request.POST.get("hawb", "")
            guia.empresa = request.POST.get("empresa", "")
            guia.info = request.POST.get("info", "")
            guia.vuelos1 = request.POST.get("vuelos1", "")
            guia.vuelos2 = request.POST.get("vuelos2", "")
            guia.airport_departure = request.POST.get("airport_departure", "")
            guia.airport_final = request.POST.get("airport_final", "")
            guia.final = request.POST.get("final", "")
            guia.by_cia_1 = request.POST.get("by_cia_1", "")
            guia.by_cia_2 = request.POST.get("by_cia_2", "")
            guia.by_cia_3 = request.POST.get("by_cia_3", "")
            guia.to_1 = request.POST.get("to_1", "")
            guia.to_2 = request.POST.get("to_2", "")
            guia.to_3 = request.POST.get("to_3", "")
            guia.by_first_carrier = request.POST.get("by_first_carrier", "")
            guia.array_destinos = request.POST.get("array_destinos", "")
            guia.modopago = request.POST.get("modopago", "")
            guia.cc1 = request.POST.get("cc1", "")
            guia.cc2 = request.POST.get("cc2", "")
            guia.pp1 = request.POST.get("pp1", "")
            guia.pp2 = request.POST.get("pp2", "")
            guia.pago_code = request.POST.get("pago_code", "")
            guia.otros_gastos = request.POST.get("otros_gastos", "")
            guia.shipper_signature = request.POST.get("shipper_signature", "")
            guia.carrier_signature = request.POST.get("carrier_signature", "")
            guia.amount_insurance = request.POST.get("amount_insurance", "")
            guia.handling = request.POST.get("handling", "")
            guia.declared_value_for_carriage = request.POST.get("declared_value_for_carriage", "")
            guia.declared_value_for_customs = request.POST.get("declared_value_for_customs", "")
            guia.iata_code_agente = request.POST.get("iata_code_agente", "")
            guia.account_nro = request.POST.get("account_nro", "")
            guia.notify = request.POST.get("notify", "")
            guia.currency = request.POST.get("currency", "")
            guia.fecha_ingreso=datetime.datetime.now()
            guia.numero=row_id
            # Mercaderías
            mercaderias = []
            i = 1
            while f"bultos_{i}" in request.POST:
                mercaderias.append({
                    "bultos": request.POST.get(f"bultos_{i}", ""),
                    "peso": request.POST.get(f"pesos_{i}", ""),
                    "unidad": request.POST.get(f"unidad_{i}", ""),
                    "aplicable": request.POST.get(f"aplicable_{i}", ""),
                    "tarifa": request.POST.get(f"tarifa_{i}", ""),
                    "total": request.POST.get(f"total_{i}", ""),
                    "descripcion": request.POST.get(f"descripcion_{i}", ""),
                    "top": request.POST.get(f"top_{i}", ""),
                })
                i += 1
            guia.mercaderias = mercaderias

            guia.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'mensaje': str(e)})
    return JsonResponse({'success': False, 'mensaje': 'Método inválido'})

def descargar_hawb_operativas(request,row_id,draft=None,asagreed=None):
    try:
        reporte = GuiasReportHijas()
        ultima_guia = GuiasHijas.objects.filter(numero=row_id).order_by('-fecha_ingreso').first()
        house = ExportEmbarqueaereo.objects.get(numero=row_id)
        if ultima_guia:
            datos_previos = model_to_dict(ultima_guia)
            for key, value in datos_previos.items():
                if hasattr(reporte, key):
                    setattr(reporte, key, value)
        else:
            # tarifa = ExportReservas.objects.get(posicion=house.posicion).tarifaawb

            data = obtener_datos_guia(row_id)

            # Atributos principales
            reporte.numero = data.get("numero", "")
            reporte.total_bultos = data.get("total_bultos", 0)
            reporte.total_pesos = data.get("total_pesos", 0)
            reporte.total_total = data.get("total_total", 0)
            reporte.posicion = data.get("posicion", "")

            # Datos principales del documento
            reporte.consignatario = data.get("consignatario", "")
            reporte.shipper = data.get("empresa", "")
            reporte.empresa = data.get("shipper", "")
            reporte.issuing_carrier = data.get("issuing_carrier", "")
            reporte.info = data.get("info", "")

            # AWB y HAWB
            reporte.awb_sf = data.get("awb_sf", "")
            reporte.awb1 = data.get("awb1", "")
            reporte.awb2 = data.get("awb2", "")
            reporte.awb3 = data.get("awb3", "")
            reporte.hawb = data.get("hawb", "")

            # Vuelos y aeropuertos
            reporte.vuelos1 = data.get("vuelos1", "")
            reporte.vuelos2 = data.get("vuelos2", "")
            reporte.airport_departure = data.get("airport_departure", "")
            reporte.airport_final = data.get("airport_final", "")
            reporte.final = data.get("final", "")

            # Escalas y compañías
            reporte.by_cia_1 = data.get("by_cia_1", "")
            reporte.by_cia_2 = data.get("by_cia_2", "")
            reporte.by_cia_3 = data.get("by_cia_3", "")
            reporte.to_1 = data.get("to_1", "")
            reporte.to_2 = data.get("to_2", "")
            reporte.to_3 = data.get("to_3", "")
            reporte.by_first_carrier = data.get("by_first_carrier", "")
            reporte.arraydestinos = data.get("array_destinos", "")

            # Pago y condiciones
            reporte.modopago = data.get("modopago", "")
            reporte.cc1 = data.get("cc1", "")
            reporte.cc2 = data.get("cc2", "")
            reporte.pp1 = data.get("pp1", "")
            reporte.pp2 = data.get("pp2", "")
            reporte.pago_code = data.get("pago_code", "")

            # Mercaderías
            reporte.mercaderias = data.get("mercaderias", [])
            reporte.medidas_text = data.get("medidas_text", [])
            reporte.volumen_total_embarque = data.get("volumen_total_embarque", 0)
            reporte.descripcion_mercaderias = data.get("descripcion_mercaderias", "")

            # Valores monetarios
            reporte.valppd = data.get("valppd", 0)
            reporte.valcol = data.get("valcol", 0)
            reporte.prepaid = data.get("prepaid", 0)
            reporte.collect = data.get("collect", 0)
            reporte.taxppd = data.get("taxppd", 0)
            reporte.taxcol = data.get("taxcol", 0)
            reporte.agentppd = data.get("agentppd", 0)
            reporte.agentcol = data.get("agentcol", 0)
            reporte.carrierppd = data.get("carrierppd", 0)
            reporte.carriercol = data.get("carriercol", 0)
            reporte.total_prepaid = data.get("total_prepaid", 0)
            reporte.total_collect = data.get("total_collect", 0)
            reporte.total_precio_p = data.get("total_precio_p", 0)
            reporte.total_precio_c = data.get("total_precio_c", 0)

            # Otros datos
            reporte.otros_gastos = data.get("otros_gastos", "")
            reporte.shipper_signature = data.get("shipper_signature", "")
            reporte.carrier_signature = data.get("carrier_signature", "")
            reporte.amount_insurance = data.get("amount_insurance", "NIL")
            reporte.handling = data.get("handling", "")
            reporte.declared_value_for_carriage = data.get("declared_value_for_carriage", "NVD")
            reporte.declared_value_for_customs = data.get("declared_value_for_customs", "NCV")
            reporte.iata_code_agente = data.get("iata_code_agente", "")
            reporte.account_nro = data.get("account_nro", "")
            reporte.currency = data.get("currency", "")

        # OUTPUT
        def valor_presente(v):
            """Devuelve True si v no está vacío ni es 0."""
            if v is None:
                return False
            if isinstance(v, (int, float, Decimal)):
                return v != 0
            if isinstance(v, str):
                s = v.strip()
                return s != '' and s != '0'
            return bool(v)

        if asagreed == 1:
            # actualizás los atributos simples como antes...
            campos = [
                'total_prepaid', 'total_collect',
                'collect', 'prepaid',
                'valppd', 'valcol',
                'taxppd', 'taxcol',
                'agentppd', 'agentcol',
                'carrierppd', 'carriercol'
            ]
            for attr in campos:
                valor_actual = getattr(reporte, attr, None)
                if valor_presente(valor_actual):
                    setattr(reporte, attr, 'AS AGREED')

            reporte.total_total='AS AGREED'

            # ahora actualizás los totales dentro de mercaderias
            merc = getattr(reporte, 'mercaderias', None)
            if isinstance(merc, list):
                for item in merc:
                    item['total'] = 'AS AGREED'

            elif isinstance(merc, dict):
                # en caso de que mercaderias sea un único dict
                merc['total'] = 'AS AGREED'

        name = 'HWBL_' + str(house.seguimiento)
        output = str(BASE_DIR) + '/archivos/' + name + '.pdf'

        if draft is not None:
            reporte.generar_awb(output, fondo='carrier_hawb.jpg')
            reporte.generar_awb(output, fondo='dorso01.jpg', dorso=1)
            reporte.generar_awb(output, fondo='consignee.jpg')
            reporte.generar_awb(output, fondo='dorso02.jpg', dorso=1)
            reporte.generar_awb(output, fondo='shipper.jpg')
            reporte.generar_awb(output, fondo='dorso03.jpg', dorso=1)
            reporte.generar_awb(output, fondo='delivery_receipt.jpg')
            reporte.generar_awb(output, fondo='dorso04.jpg', dorso=1)
            reporte.generar_awb(output, fondo='copia1.jpg')
            reporte.generar_awb(output, fondo='copia2.jpg')
            reporte.generar_awb(output, fondo='copia3.jpg')
            reporte.generar_awb(output, fondo='copia4.jpg')
            reporte.generar_awb(output, fondo='copia5.jpg')
            reporte.generar_awb(output, fondo='copia6.jpg')
        else:
            reporte.generar_awb(output)

        return reporte.descargo_archivo(output)


    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise Http404(f"Error: {str(e)}")

#editar guias madre


def editar_awb(request, row_id):
    try:
        imagen_path = os.path.join(settings.BASE_DIR,'cargosystem', 'static', 'images', 'guias', 'normal.jpg')


        if not os.path.exists(imagen_path):
            raise FileNotFoundError(f"No se encontró la imagen: {imagen_path}")

        with open(imagen_path, 'rb') as img_file:
            img_b64 = b64encode(img_file.read()).decode('utf-8')
        guias = GuiasMadres.objects.filter(numero=row_id).order_by('-fecha_ingreso')

        if guias.exists():
            guia_existente = guias.first()
            datos = model_to_dict(guia_existente)
        else:
            datos = obtener_datos_guia_madre(row_id)
        return render(request, 'expaerea/editar_awb.html', {
            'imagen': img_b64,
            'datos': datos,
            'row_id': row_id,
        })
    except Exception as e:
        messages.error(request,str(e))
        return HttpResponseRedirect('/')

def obtener_datos_guia_madre(row_id):
    try:
        data = {
            'numero':row_id,
            'total_bultos': 0,
            'total_pesos': 0,
            'total_total': 0,
            'posicion': '',
            'consignatario':'',
            'shipper':'',
            'awb_sf':'',
            'awb1':'',
            'awb2':'',
            'awb3':'',
            'hawb':'',
            'empresa':'',
            'issuing_carrier':'',
            'info':'',
            'vuelos1':'',
            'vuelos2':'',
            'airport_departure':'',
            'airport_final':'',
            'final':'',
            'by_cia_1':'',
            'by_cia_3':'',
            'by_cia_2':'',
            'to_1':'',
            'to_2':'',
            'by_first_carrier':'',
            'array_destinos':'',
            'modopago':'',
            'cc1': '',
            'cc2': '',
            'pp1': '',
            'pp2': '',
            'pago_code': '',
            'mercaderias': [],
            'medidas_text': [],
            'volumen_total_embarque': 0,
            'valppd': 0,
            'valcol': 0,
            'prepaid': 0,
            'collect': 0,
            'taxppd': 0,
            'taxcol': 0,
            'agentppd': 0,
            'agentcol': 0,
            'carrierppd': 0,
            'carriercol': 0,
            'total_prepaid': 0,
            'total_collect': 0,
            'otros_gastos': '',
            'shipper_signature': '',
            'carrier_signature': '',
            'amount_insurance': 'NIL',
            'handling': '',
            'declared_value_for_carriage': 'NVD',
            'declared_value_for_customs': 'NCV',
            'iata_code_agente': '94-1-0046',
            'account_nro': '',
            'notify': '',
            'currency': '',
            'descripcion_mercaderias': '',
        }

        master = ExportReservas.objects.get(numero=row_id)

        # CONSIGNATARIO
        consignatario = SociosComerciales.objects.get(codigo=master.consignatario)
        carrier = SociosComerciales.objects.get(codigo=master.transportista)
        empresa = SociosComerciales.objects.get(codigo=master.transportista)

        data['consignatario'] = f"{consignatario.empresa}\n{consignatario.direccion}\n{consignatario.ciudad}\n{consignatario.pais} RUT: {consignatario.ruc} PH: {consignatario.telefono}"
        data['shipper']=f"{empresa.empresa}\n{empresa.direccion}\n{empresa.ciudad}\n{empresa.pais} RUT: {empresa.ruc} PH: {empresa.telefono}"
        data['issuing_carrier']=settings.EMPRESA_AWB_editar
        data['by_first_carrier']=carrier.empresa
        data['currency']='USD' if master.moneda == 2 else 'UYU' if master.moneda == 1 else 'S/I'
        # SHIPPER
        data['empresa'] = settings.EMPRESA_HAWB_editar
        data['shipper_signature'] = 'OCEANLINK'
        data['carrier_signature'] = (
                'OCEANLINK AS AGENT\n'
                'OF DE CARRIER ' + str(empresa.empresa) + '\n' +
                datetime.datetime.now().strftime('%Y-%m-%d') + ' MONTEVIDEO\n' +
                'OCEAN LINK LTDA / LLB'
        )

        # NOTIFY
        pago = 'COLLECT' if master.pagoflete == 'C' else 'PREPAID'
        notificador = SociosComerciales.objects.get(codigo=master.consignatario)
        data['info'] = f"FREIGHT {pago}\nNOTIFY: {notificador.empresa}\n{notificador.direccion}\n{notificador.ciudad}\n{notificador.pais} RUT: {notificador.ruc} PH: {notificador.telefono}"
        data['awb_sf'] = master.awb

        # AWB y HAWB
        if master.awb and master.awb != 'S/I':
            awb = master.awb.split('-')
            data['awb1'] = awb[0]
            data['awb2'] = "MVD"
            data['awb3'] = awb[1]
            data['hawb'] = master.awb

        # TRANSBORDOS
        trasbordos = list(ExportConexreserva.objects.filter(numero=master.numero).order_by( 'id'))
        data['airport_departure'] = "MONTEVIDEO"
        data['vuelos1'] = ''
        data['vuelos2'] = ''
        data['array_destinos'] = ''
        data['to_1'] = ''
        data['to_2'] = ''
        data['to_3'] = ''
        data['by_cia'] = ''
        data['by_cia_2'] = ''
        data['by_cia_3'] = ''

        destinos = []

        if trasbordos:
            count = len(trasbordos)

            if count == 1:
                data['to_1'] = str(trasbordos[0].destino)
                data['by_cia_1'] = trasbordos[0].ciavuelo

            elif count == 2:
                data['to_1'] = str(trasbordos[0].destino)
                data['by_cia_1'] = trasbordos[0].ciavuelo

                data['to_2'] = str(trasbordos[1].destino)
                data['by_cia_2'] = trasbordos[1].ciavuelo

            elif count == 3:
                data['to_1'] = str(trasbordos[0].destino)
                data['by_cia_1'] = trasbordos[0].ciavuelo

                data['to_2'] = str(trasbordos[1].destino)
                data['by_cia_2'] = trasbordos[1].ciavuelo

                data['to_3'] = str(trasbordos[2].destino)
                data['by_cia_3'] = trasbordos[2].ciavuelo

            else:  # más de 3
                data['to_1'] = str(trasbordos[0].destino)
                data['by_cia_1'] = trasbordos[0].ciavuelo

                data['to_2'] = str(trasbordos[1].destino)
                data['by_cia_2'] = trasbordos[1].ciavuelo

                data['to_3'] = str(trasbordos[-1].destino)
                data['by_cia_3'] = trasbordos[-1].ciavuelo

            data['vuelos1'] = ''
            data['vuelos2'] = ''

            # if trasbordos:
            #     count = len(trasbordos)
            #
            #     if count == 1:
            #         x = trasbordos[0]
            #         data['vuelos1'] = f"{x.ciavuelo}{x.vuelo}/{x.salida.strftime('%d-%B')[:6].upper()} "
            #         data['final']=x.destino
            #
            #     elif count == 2:
            #         x1, x2 = trasbordos[0], trasbordos[1]
            #         data['vuelos1'] = f"{x1.ciavuelo}{x1.vuelo}/{x1.salida.strftime('%d-%B')[:6].upper()} "
            #         data['vuelos2'] = f"{x2.ciavuelo}{x2.vuelo}/{x2.salida.strftime('%d-%B')[:6].upper()} "
            #         data['final']=x2.destino
            #
            #     else:  # más de 2 vuelos
            #         x1, xN = trasbordos[0], trasbordos[-1]
            #         data['vuelos1'] = f"{x1.ciavuelo}{x1.vuelo}/{x1.salida.strftime('%d-%B')[:6].upper()} "
            #         data['vuelos2'] = f"{xN.ciavuelo}{xN.vuelo}/{xN.salida.strftime('%d-%B')[:6].upper()} "
            #         data['final']=xN.destino
            if trasbordos:
                def fmt(vuelo):
                    return f"{vuelo.ciavuelo}{vuelo.vuelo}/{vuelo.salida.strftime('%d-%B')[:6].upper()} "

                vuelos1 = []
                vuelos2 = []

                for idx, x in enumerate(trasbordos, start=1):
                    if idx % 2 == 1:  # impar → vuelos1
                        vuelos1.append(fmt(x))
                    else:  # par → vuelos2
                        vuelos2.append(fmt(x))

                data['vuelos1'] = "".join(vuelos1)
                data['vuelos2'] = "".join(vuelos2)
                data['final'] = trasbordos[-1].destino

        # Construir lista de destinos to_1, to_2, to_3... que no estén vacíos
        to_keys = sorted([k for k in data.keys() if k.startswith('to_')],
                         key=lambda x: int(x.split('_')[1]))
        tos = [str(data[k]).strip() for k in to_keys if data.get(k)]

        # Base del texto (por si airport_departure ya trae el nombre de la ciudad)
        base = data.get('airport_departure', '').strip()
        iata_origen = "MVD"

        if tos:
            data['airport_departure'] = f"{base} ({iata_origen}/" + "/".join(tos) + ")"
        else:
            # Si no hay to_*, solo muestra el IATA origen
            data['airport_departure'] = f"{base} ({iata_origen})"

        data['array_destinos'] = '   '.join(reversed(destinos[:2]))

        ciudad = Ciudades.objects.filter(codigo=data['final'])
        if ciudad.exists():
            data['airport_final'] = ciudad[0].nombre

        # PAGO
        data['modopago'] = 'Collect' if master.pagoflete == 'C' else 'Prepaid'
        if master.pagoflete=='C':
            data['pago_code']='CC'
            data['cc1']='C'
            data['cc2']='C'
        else:
            data['pago_code']='PP'
            data['pp1']='P'
            data['pp2']='P'

        # Cargas y mercadería
        houses = ExportEmbarqueaereo.objects.only('numero', 'hawb').filter(awb=master.awb)
        house_numeros = houses.values_list('numero', flat=True)
        cargas = ExportCargaaerea.objects.filter(numero__in=house_numeros)

        data['mercaderias'] = []
        data['descripcion_mercaderias'] = ""  # una sola descripción común
        data['volumen_total_embarque'] = 0
        top_base = 1030
        incremento = 30

        # if cargas.exists():
        #     total_bultos = total_bruto = total_total = 0
        #     medidas_descripciones = []
        #
        #     # Generar descripción consolidada
        #     hawbs = [h.hawb for h in houses if h.hawb]
        #
        #     for carga in cargas:
        #         if carga.medidas:
        #             medidas_descripciones.append(f"({carga.bultos}) * {carga.medidas} MTS")
        #
        #     descripcion_unica = (
        #             "CONSOLIDATION AS PER ATTACHED CARGO MANIFEST\n" +
        #             "; ".join(hawbs) + "\n" +
        #             "\n".join(medidas_descripciones)
        #     )
        #     data['descripcion_mercaderias'] = descripcion_unica
        #
        #     # Generar filas sin descripción
        #     for idx, carga in enumerate(cargas):
        #         bruto = carga.bruto or 0
        #         valor_aplicable = carga.aplicable or 0
        #
        #         if valor_aplicable == 0:
        #             aplicable_display = 'MIN'
        #             total = float(master.tarifaawb)
        #         else:
        #             aplicable_display = round(valor_aplicable, 2)
        #             total = round(valor_aplicable * float(master.tarifaawb), 2)
        #
        #         data['mercaderias'].append({
        #             'bultos': carga.bultos,
        #             'peso': bruto,
        #             'unidad': 'K',
        #             'aplicable': aplicable_display,
        #             'tarifa': master.tarifaawb,
        #             'total': total,
        #             'top': top_base + (idx * incremento),
        #         })
        #
        #         total_bultos += carga.bultos
        #         total_bruto += bruto
        #         total_total += total
        #
        #     data['total_bultos'] = total_bultos
        #     data['total_pesos'] = total_bruto
        #     data['total_total'] = total_total
        from decimal import Decimal, ROUND_HALF_UP

        if cargas.exists():
            total_bultos = 0
            total_bruto = Decimal('0')
            total_aplicable = Decimal('0')  # solo suma valores > 0
            medidas_descripciones = []

            # Generar descripción consolidada
            hawbs = [h.hawb for h in houses if h.hawb]
            for carga in cargas:
                if carga.medidas:
                    medidas_descripciones.append(f"({carga.bultos}) * {carga.medidas} MTS")

            descripcion_unica = (
                    "CONSOLIDATION AS PER ATTACHED CARGO MANIFEST\n" +
                    "; ".join(hawbs) + "\n" +
                    "\n".join(medidas_descripciones)
            )
            data['descripcion_mercaderias'] = descripcion_unica

            # Acumuladores
            for carga in cargas:
                total_bultos += (carga.bultos or 0)
                total_bruto += Decimal(str(carga.bruto or 0))



            tarifa = Decimal(str(master.tarifaawb or 0))
            total_aplicable = Decimal(master.aplicable)

            if total_aplicable == 1:
                # Caso sin aplicables -> MIN (1 * tarifa), una sola vez
                aplicable_display = "MIN"
                total_total = tarifa
            else:
                # Caso con aplicables -> suma * tarifa
                aplicable_display = (total_aplicable.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
                total_total = (total_aplicable * tarifa)

            # Normalizar a 2 decimales
            total_total = total_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            total_bruto = total_bruto.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            # Guardar UNA sola fila en mercaderías
            data['mercaderias'] = [{
                'bultos': total_bultos,
                'peso': float(total_bruto),  # o dejar Decimal si preferís
                'unidad': 'K',
                'aplicable': aplicable_display,
                'tarifa': float(tarifa),
                'total': float(total_total),
                'top': top_base,  # una fila
            }]

            # Totales consolidados
            data['total_bultos'] = total_bultos
            data['total_pesos'] = float(total_bruto)
            data['total_total'] = float(total_total)

        data['posicion'] = master.posicion

        if master.pagoflete=='C':
            data['collect']=data['total_total']
        else:
            data['prepaid']=data['total_total']

        # GASTOS
        gastos = ExportServireserva.objects.filter(numero=master.numero)
        for g in gastos:
            if g.costo == 0:
                continue

            if g.modo == 'C':  # COLLECT
                if g.tipogasto == 'OTHER':
                    data['valcol'] += g.costo
                elif g.tipogasto == 'DUE CARRIER':
                    data['carriercol'] += g.costo
                elif g.tipogasto == 'DUE AGENT':
                    data['agentcol'] += g.costo
                data['total_collect'] += g.costo
            else:  # PREPAID
                if g.tipogasto == 'OTHER':
                    data['valppd'] += g.costo
                elif g.tipogasto == 'DUE CARRIER':
                    data['carrierppd'] += g.costo
                elif g.tipogasto == 'DUE AGENT':
                    data['agentppd'] += g.costo
                data['total_prepaid'] += g.costo

            data['otros_gastos'] += f"{round(g.costo, 2)}   "

            data['valcol']=round(Decimal(data['valcol']),2)
            data['valppd']=round(Decimal(data['valppd']),2)
            data['carriercol']=round(Decimal(data['carriercol']),2)
            data['carrierppd']=round(Decimal(data['carrierppd']),2)
            data['agentcol']=round(Decimal(data['agentcol']),2)
            data['agentppd']=round(Decimal(data['agentppd']),2)
            data['agentppd']=round(Decimal(data['agentppd']),2)
            data['total_prepaid']=round(Decimal(data['total_prepaid']),2)
            data['total_collect']=round(Decimal(data['total_collect']),2)

        if master.pagoflete=='C':
            data['total_collect'] += round(Decimal(data['collect'] or 0),2)
        else:
            data['total_prepaid'] += round(Decimal(data['prepaid'] or 0),2)


        return data

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise Http404(f"Error: {str(e)}")

def descargar_awb_operativas(request,row_id,draft=None):
    try:
        reporte = GuiasReport()
        ultima_guia = GuiasMadres.objects.filter(numero=row_id).order_by('-fecha_ingreso').first()
        # master = ExportReservas.objects.get(numero=row_id)

        if ultima_guia:
            datos_previos = model_to_dict(ultima_guia)
            for key, value in datos_previos.items():
                if hasattr(reporte, key):
                    setattr(reporte, key, value)
        else:
            data = obtener_datos_guia_madre(row_id)
            reporte = GuiasReport()

            # Atributos principales
            reporte.numero = data.get("numero", "")
            reporte.total_bultos = data.get("total_bultos", 0)
            reporte.total_pesos = data.get("total_pesos", 0)
            reporte.total_total = data.get("total_total", 0)
            reporte.posicion = data.get("posicion", "")

            # Datos principales del documento
            reporte.consignatario = data.get("consignatario", "")
            reporte.shipper = data.get("shipper", "")
            reporte.empresa = data.get("empresa", "")
            reporte.issuing_carrier = data.get("issuing_carrier", "")
            reporte.info = data.get("info", "")

            # AWB y HAWB
            reporte.awb_sf = data.get("awb_sf", "")
            reporte.awb1 = data.get("awb1", "")
            reporte.awb2 = data.get("awb2", "")
            reporte.awb3 = data.get("awb3", "")
            reporte.hawb = data.get("hawb", "")

            # Vuelos y aeropuertos
            reporte.vuelos1 = data.get("vuelos1", "")
            reporte.vuelos2 = data.get("vuelos2", "")
            reporte.airport_departure = data.get("airport_departure", "")
            reporte.airport_final = data.get("airport_final", "")
            reporte.final = data.get("final", "")

            # Escalas y compañías
            reporte.by_cia_1 = data.get("by_cia_1", "")
            reporte.by_cia_2 = data.get("by_cia_2", "")
            reporte.by_cia_3 = data.get("by_cia_3", "")
            reporte.to_1 = data.get("to_1", "")
            reporte.to_2 = data.get("to_2", "")
            reporte.to_3 = data.get("to_3", "")
            reporte.by_first_carrier = data.get("by_first_carrier", "")
            reporte.arraydestinos = data.get("array_destinos", "")

            # Pago y condiciones
            reporte.modopago = data.get("modopago", "")
            reporte.cc1 = data.get("cc1", "")
            reporte.cc2 = data.get("cc2", "")
            reporte.pp1 = data.get("pp1", "")
            reporte.pp2 = data.get("pp2", "")
            reporte.pago_code = data.get("pago_code", "")

            # Mercaderías
            reporte.mercaderias = data.get("mercaderias", [])
            reporte.medidas_text = data.get("medidas_text", [])
            reporte.volumen_total_embarque = data.get("volumen_total_embarque", 0)
            reporte.descripcion_mercaderias = data.get("descripcion_mercaderias", "")

            # Valores monetarios
            reporte.valppd = data.get("valppd", 0)
            reporte.valcol = data.get("valcol", 0)
            reporte.prepaid = data.get("prepaid", 0)
            reporte.collect = data.get("collect", 0)
            reporte.taxppd = data.get("taxppd", 0)
            reporte.taxcol = data.get("taxcol", 0)
            reporte.agentppd = data.get("agentppd", 0)
            reporte.agentcol = data.get("agentcol", 0)
            reporte.carrierppd = data.get("carrierppd", 0)
            reporte.carriercol = data.get("carriercol", 0)
            reporte.total_prepaid = data.get("total_prepaid", 0)
            reporte.total_collect = data.get("total_collect", 0)
            reporte.total_precio_p = data.get("total_precio_p", 0)
            reporte.total_precio_c = data.get("total_precio_c", 0)

            # Otros datos
            reporte.otros_gastos = data.get("otros_gastos", "")
            reporte.shipper_signature = data.get("shipper_signature", "")
            reporte.carrier_signature = data.get("carrier_signature", "")
            reporte.amount_insurance = data.get("amount_insurance", "NIL")
            reporte.handling = data.get("handling", "")
            reporte.declared_value_for_carriage = data.get("declared_value_for_carriage", "NVD")
            reporte.declared_value_for_customs = data.get("declared_value_for_customs", "NCV")
            reporte.iata_code_agente = data.get("iata_code_agente", "")
            reporte.account_nro = data.get("account_nro", "")
            reporte.currency = data.get("currency", "")

        name = 'AWB_' + str(reporte.numero)
        output = str(BASE_DIR) + f'/archivos/{name}.pdf'

        if draft is not None:
            reporte.generar_awb(output, fondo='carrier_hawb.jpg')
            reporte.generar_awb(output, fondo='dorso01.jpg', dorso=1)
            reporte.generar_awb(output, fondo='consignee.jpg')
            reporte.generar_awb(output, fondo='dorso02.jpg', dorso=1)
            reporte.generar_awb(output, fondo='shipper.jpg')
            reporte.generar_awb(output, fondo='dorso03.jpg', dorso=1)
            reporte.generar_awb(output, fondo='delivery_receipt.jpg')
            reporte.generar_awb(output, fondo='dorso04.jpg', dorso=1)
            reporte.generar_awb(output, fondo='copia1.jpg')
            reporte.generar_awb(output, fondo='copia2.jpg')
            reporte.generar_awb(output, fondo='copia3.jpg')
            reporte.generar_awb(output, fondo='copia4.jpg')
            reporte.generar_awb(output, fondo='copia5.jpg')
            reporte.generar_awb(output, fondo='copia6.jpg')
        else:
            reporte.generar_awb(output)

        return reporte.descargo_archivo(output)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise Http404(f"Error: {str(e)}")


def guardar_awb(request, row_id):
    if request.method == 'POST':
        try:
            guia = GuiasMadres()
            # Campos numéricos
            guia.total_bultos = int(request.POST.get("total_bultos", 0) or 0)
            guia.total_pesos = Decimal(request.POST.get("total_pesos", 0) or 0)
            guia.total_total = Decimal(request.POST.get("total_total", 0) or 0)
            guia.volumen_total_embarque = Decimal(request.POST.get("volumen_total_embarque", 0) or 0)
            guia.valppd = Decimal(request.POST.get("valppd", 0) or 0)
            guia.valcol = Decimal(request.POST.get("valcol", 0) or 0)
            guia.prepaid = Decimal(request.POST.get("prepaid", 0) or 0)
            guia.collect = Decimal(request.POST.get("collect", 0) or 0)
            guia.taxppd = Decimal(request.POST.get("taxppd", 0) or 0)
            guia.taxcol = Decimal(request.POST.get("taxcol", 0) or 0)
            guia.agentppd = Decimal(request.POST.get("agentppd", 0) or 0)
            guia.agentcol = Decimal(request.POST.get("agentcol", 0) or 0)
            guia.carrierppd = Decimal(request.POST.get("carrierppd", 0) or 0)
            guia.carriercol = Decimal(request.POST.get("carriercol", 0) or 0)
            guia.total_prepaid = Decimal(request.POST.get("total_prepaid", 0) or 0)
            guia.total_collect = Decimal(request.POST.get("total_collect", 0) or 0)

            # Campos de texto
            guia.posicion = request.POST.get("posicion", "")
            guia.consignatario = request.POST.get("consignatario", "")
            guia.shipper = request.POST.get("shipper", "")
            guia.awb_sf = request.POST.get("awb", "")
            guia.awb1 = request.POST.get("awb1", "")
            guia.awb2 = request.POST.get("awb2", "")
            guia.awb3 = request.POST.get("awb3", "")
            guia.hawb = request.POST.get("hawb", "")
            guia.empresa = request.POST.get("empresa", "")
            guia.info = request.POST.get("info", "")
            guia.vuelos1 = request.POST.get("vuelos1", "")
            guia.vuelos2 = request.POST.get("vuelos2", "")
            guia.airport_departure = request.POST.get("airport_departure", "")
            guia.airport_final = request.POST.get("airport_final", "")
            guia.issuing_carrier = request.POST.get("issuing_carrier", "")
            guia.final = request.POST.get("final", "")
            guia.by_cia_1 = request.POST.get("by_cia_1", "")
            guia.by_cia_2 = request.POST.get("by_cia_2", "")
            guia.by_cia_3 = request.POST.get("by_cia_3", "")
            guia.to_1 = request.POST.get("to_1", "")
            guia.to_2 = request.POST.get("to_2", "")
            guia.to_3 = request.POST.get("to_3", "")
            guia.by_first_carrier = request.POST.get("by_first_carrier", "")
            guia.array_destinos = request.POST.get("array_destinos", "")
            guia.modopago = request.POST.get("modopago", "")
            guia.cc1 = request.POST.get("cc1", "")
            guia.cc2 = request.POST.get("cc2", "")
            guia.pp1 = request.POST.get("pp1", "")
            guia.pp2 = request.POST.get("pp2", "")
            guia.pago_code = request.POST.get("pago_code", "")
            guia.otros_gastos = request.POST.get("otros_gastos", "")
            guia.shipper_signature = request.POST.get("shipper_signature", "")
            guia.carrier_signature = request.POST.get("carrier_signature", "")
            guia.amount_insurance = request.POST.get("amount_insurance", "")
            guia.handling = request.POST.get("handling", "")
            guia.declared_value_for_carriage = request.POST.get("declared_value_for_carriage", "")
            guia.declared_value_for_customs = request.POST.get("declared_value_for_customs", "")
            guia.iata_code_agente = request.POST.get("iata_code_agente", "")
            guia.account_nro = request.POST.get("account_nro", "")
            guia.notify = request.POST.get("notify", "")
            guia.currency = request.POST.get("currency", "")
            guia.descripcion_mercaderias = request.POST.get("descripcion_unica", "")
            guia.fecha_ingreso=datetime.datetime.now()
            guia.numero=row_id
            # Mercaderías
            mercaderias = []
            i = 1
            while f"bultos_{i}" in request.POST:
                mercaderias.append({
                    "bultos": request.POST.get(f"bultos_{i}", ""),
                    "peso": request.POST.get(f"pesos_{i}", ""),
                    "unidad": request.POST.get(f"unidad_{i}", ""),
                    "aplicable": request.POST.get(f"aplicable_{i}", ""),
                    "tarifa": request.POST.get(f"tarifa_{i}", ""),
                    "total": request.POST.get(f"total_{i}", ""),
                    "descripcion": request.POST.get(f"descripcion_{i}", ""),
                    "top": request.POST.get(f"top_{i}", ""),
                })
                i += 1
            guia.mercaderias = mercaderias

            guia.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'mensaje': str(e)})
    return JsonResponse({'success': False, 'mensaje': 'Método inválido'})

def descargar_awb_operativas_old(request,row_id,draft=None):
    try:
        rep = GuiasReport()
        ultima_guia = GuiasMadres.objects.filter(numero=row_id).order_by('-fecha_ingreso').first()
        master = ExportReservas.objects.get(numero=row_id)

        if ultima_guia:
            datos_previos = model_to_dict(ultima_guia)
            for key, value in datos_previos.items():
                if hasattr(rep, key):
                    setattr(rep, key, value)
        else:
            # CONSIGNATARIO
            consignatario = SociosComerciales.objects.get(codigo=master.consignatario)
            carrier = SociosComerciales.objects.get(codigo=master.transportista)

            rep.numero = row_id
            rep.posicion = master.posicion
            rep.consignatario = f"{consignatario.empresa}\n{consignatario.direccion}\n{consignatario.ciudad}\n{consignatario.pais} RUT: {consignatario.ruc} PH: {consignatario.telefono}"
            rep.shipper = settings.EMPRESA_HAWB_editar
            rep.issuing_carrier = settings.EMPRESA_AWB_editar
            rep.by_first_carrier = carrier.empresa

            rep.empresa = f"{carrier.empresa}\n{carrier.direccion}\n{carrier.ciudad}\n{carrier.pais} RUT: {carrier.ruc} PH: {carrier.telefono}"
            rep.shipper_signature = 'OCEANLINK'
            rep.carrier_signature = (
                'OCEANLINK AS AGENT\n'
                f'OF DE CARRIER {carrier.empresa}\n' +
                datetime.datetime.now().strftime('%Y-%m-%d') + ' MONTEVIDEO\n' +
                'OCEAN LINK LTDA / LLB'
            )

            pago = 'COLLECT' if master.pagoflete == 'C' else 'PREPAID'
            rep.modopago = pago.capitalize()
            rep.pago_code = 'CC' if master.pagoflete == 'C' else 'PP'
            rep.cc1 = 'C' if master.pagoflete == 'C' else ''
            rep.cc2 = 'C' if master.pagoflete == 'C' else ''
            rep.pp1 = 'P' if master.pagoflete == 'P' else ''
            rep.pp2 = 'P' if master.pagoflete == 'P' else ''

            rep.info = f"FREIGHT {pago}\nNOTIFY: {consignatario.empresa}\n{consignatario.direccion}\n{consignatario.ciudad}\n{consignatario.pais} RUT: {consignatario.ruc} PH: {consignatario.telefono}"

            if master.awb and master.awb != 'S/I':
                awb = master.awb.split('-')
                rep.awb1 = awb[0]
                rep.awb2 = "MVD"
                rep.awb3 = awb[1]
                rep.awb_sf = master.awb
                rep.hawb = master.awb

            # Conexiones
            trasbordos = list(ExportConexreserva.objects.filter(numero=master.numero).order_by('llegada', 'id'))
            rep.airport_departure = 'MONTEVIDEO (MVD/'+str(trasbordos[0].origen)+')'

            rep.to_1 = rep.to_2 = rep.to_3 = ''
            rep.by_cia_1 = rep.by_cia_2 = rep.by_cia_3 = ''
            rep.vuelos1 = rep.vuelos2 = ''
            rep.final = ''

            if trasbordos:
                destinos = []
                if len(trasbordos) >= 1:
                    rep.to_1 = str(trasbordos[0].destino)
                    rep.by_cia_1 = trasbordos[0].ciavuelo
                if len(trasbordos) >= 2:
                    rep.to_2 = str(trasbordos[1].destino)
                    rep.by_cia_2 = trasbordos[1].ciavuelo
                if len(trasbordos) >= 3:
                    rep.to_3 = str(trasbordos[2].destino)
                    rep.by_cia_3 = trasbordos[2].ciavuelo

                x1, xN = trasbordos[0], trasbordos[-1]
                rep.vuelos1 = f"{x1.ciavuelo}{x1.vuelo}/{x1.salida.strftime('%d-%B')[:6].upper()}"
                if len(trasbordos) > 1:
                    rep.vuelos2 = f"{xN.ciavuelo}{xN.vuelo}/{xN.salida.strftime('%d-%B')[:6].upper()}"
                rep.final = xN.destino

                ciudad = Ciudades.objects.filter(codigo=rep.final).first()
                if ciudad:
                    rep.airport_final = ciudad.nombre

            # Mercaderías
            houses = ExportEmbarqueaereo.objects.only('numero', 'hawb').filter(awb=master.awb)
            house_numeros = houses.values_list('numero', flat=True)
            cargas = ExportCargaaerea.objects.filter(numero__in=house_numeros)

            rep.mercaderias = []
            rep.descripcion_mercaderias = ""
            rep.volumen_total_embarque = Decimal('0.00')
            top_base = 1030
            incremento = 30
            rep.total_bultos = rep.total_pesos = rep.total_total = 0

            hawbs = [h.hawb for h in houses if h.hawb]
            medidas_descripciones = []

            for idx, carga in enumerate(cargas):
                bruto = carga.bruto or 0
                valor_aplicable = carga.aplicable or 0
                total = float(master.tarifaawb) if valor_aplicable == 0 else round(valor_aplicable * float(master.tarifaawb), 2)
                aplicable_display = 'MIN' if valor_aplicable == 0 else round(valor_aplicable, 2)

                if carga.medidas:
                    medidas_descripciones.append(f"({carga.bultos}) * {carga.medidas} MTS")

                rep.mercaderias.append({
                    'bultos': carga.bultos,
                    'peso': bruto,
                    'unidad': 'K',
                    'aplicable': aplicable_display,
                    'tarifa': master.tarifaawb,
                    'total': total,
                    'top': top_base + (idx * incremento),
                })

                rep.total_bultos += carga.bultos
                rep.total_pesos += bruto
                rep.total_total += total

            rep.descripcion_mercaderias = (
                "CONSOLIDATION AS PER ATTACHED CARGO MANIFEST\n" +
                "; ".join(hawbs) + "\n" +
                "\n".join(medidas_descripciones)
            )

            if rep.modopago == 'Collect':
                rep.collect = rep.total_total
            else:
                rep.prepaid = rep.total_total

            # Gastos
            gastos = ExportServireserva.objects.filter(numero=master.numero)
            rep.otros_gastos = ''
            for g in gastos:
                if g.costo == 0:
                    continue
                if g.modo == 'C':
                    if g.tipogasto == 'OTHER':
                        rep.valcol += g.costo
                    elif g.tipogasto == 'DUE CARRIER':
                        rep.carriercol += g.costo
                    elif g.tipogasto == 'DUE AGENT':
                        rep.agentcol += g.costo
                    rep.total_collect += g.costo
                else:
                    if g.tipogasto == 'OTHER':
                        rep.valppd += g.costo
                    elif g.tipogasto == 'DUE CARRIER':
                        rep.carrierppd += g.costo
                    elif g.tipogasto == 'DUE AGENT':
                        rep.agentppd += g.costo
                    rep.total_prepaid += g.costo

                rep.otros_gastos += f"{round(g.costo, 2)}   "

            if rep.modopago == 'Collect':
                rep.total_collect += round(Decimal(rep.collect or 0), 2)
            else:
                rep.total_prepaid += round(Decimal(rep.prepaid or 0), 2)

        name = 'AWB_' + str(rep.numero)
        output = str(BASE_DIR) + f'/archivos/{name}.pdf'

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
            rep.generar_awb(output, fondo='copia2.jpg')
            rep.generar_awb(output, fondo='copia3.jpg')
            rep.generar_awb(output, fondo='copia4.jpg')
            rep.generar_awb(output, fondo='copia5.jpg')
            rep.generar_awb(output, fondo='copia6.jpg')
        else:
            rep.generar_awb(output)

        return rep.descargo_archivo(output)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise Http404(f"Error: {str(e)}")
def descargar_hawb_operativas_old(request,row_id,draft=None,asagreed=None):
    try:
        rep = GuiasReportHijas()
        ultima_guia = GuiasHijas.objects.filter(numero=row_id).order_by('-fecha_ingreso').first()
        house = ExportEmbarqueaereo.objects.get(numero=row_id)
        if ultima_guia:
            datos_previos = model_to_dict(ultima_guia)
            for key, value in datos_previos.items():
                if hasattr(rep, key):
                    setattr(rep, key, value)
        else:
            tarifa = ExportReservas.objects.get(posicion=house.posicion).tarifaawb

            rep.numero = row_id
            rep.posicion = house.posicion
            rep.empresa = settings.EMPRESA_HAWB_editar
            rep.modopago = 'Collect' if house.pagoflete == 'C' else 'Prepaid'
            rep.pago_code = 'CC' if house.pagoflete == 'C' else 'PP'
            rep.cc1 = 'C' if house.pagoflete == 'C' else ''
            rep.cc2 = 'C' if house.pagoflete == 'C' else ''
            rep.pp1 = 'P' if house.pagoflete == 'P' else ''
            rep.pp2 = 'P' if house.pagoflete == 'P' else ''

            consignatario = SociosComerciales.objects.get(codigo=house.consignatario)
            rep.consignatario = f"{consignatario.empresa}\n{consignatario.direccion}\n{consignatario.ciudad}\n{consignatario.pais} RUT: {consignatario.ruc} PH: {consignatario.telefono}"

            shipper = SociosComerciales.objects.get(codigo=house.cliente)
            rep.shipper = f"{shipper.empresa}\n{shipper.direccion}\n{shipper.ciudad}\n{shipper.pais} RUT: {shipper.ruc} PH: {shipper.telefono}"
            rep.shipper_signature = shipper.empresa
            rep.carrier_signature = (
                'OCEANLINK AS AGENT\n'
                f'OF DE CARRIER {shipper.empresa}\n'
                f"{datetime.datetime.now().strftime('%Y-%m-%d')} MONTEVIDEO\n"
                'OCEAN LINK LTDA / LLB'
            )

            rep.info = f"FREIGHT {rep.modopago.upper()}\nNOTIFY: {consignatario.empresa}\n{consignatario.direccion}\n{consignatario.ciudad}\n{consignatario.pais} RUT: {consignatario.ruc} PH: {consignatario.telefono}"

            if house.awb and house.awb != 'S/I':
                awb = house.awb.split('-')
                rep.awb1 = awb[0]
                rep.awb2 = "MVD"
                rep.awb3 = awb[1]
                rep.awb_sf = house.awb

            if house.hawb and house.hawb != 'S/I':
                rep.hawb = house.hawb

            carrier = SociosComerciales.objects.get(codigo=house.transportista)
            rep.by_first_carrier = carrier.empresa

            trasbordos = list(ExportConexaerea.objects.filter(numero=house.numero).order_by('llegada', 'id'))
            rep.airport_departure = 'MONTEVIDEO (MVD/'+str(trasbordos[0].origen)+')'
            rep.to_1 = rep.to_2 = rep.to_3 = ''
            rep.by_cia_1 = rep.by_cia_2 = rep.by_cia_3 = ''
            rep.vuelos1 = rep.vuelos2 = ''
            rep.final = ''

            if trasbordos:
                if len(trasbordos) >= 1:
                    rep.to_1 = str(trasbordos[0].destino)
                    rep.by_cia_1 = trasbordos[0].ciavuelo
                if len(trasbordos) >= 2:
                    rep.to_2 = str(trasbordos[1].destino)
                    rep.by_cia_2 = trasbordos[1].ciavuelo
                if len(trasbordos) >= 3:
                    rep.to_3 = str(trasbordos[2].destino)
                    rep.by_cia_3 = trasbordos[2].ciavuelo

                if len(trasbordos) == 1:
                    x = trasbordos[0]
                    rep.vuelos1 = f"{x.ciavuelo}{x.vuelo}/{x.salida.strftime('%d-%B')[:6].upper()}"
                    rep.final = x.destino
                elif len(trasbordos) == 2:
                    x1, x2 = trasbordos[0], trasbordos[1]
                    rep.vuelos1 = f"{x1.ciavuelo}{x1.vuelo}/{x1.salida.strftime('%d-%B')[:6].upper()}"
                    rep.vuelos2 = f"{x2.ciavuelo}{x2.vuelo}/{x2.salida.strftime('%d-%B')[:6].upper()}"
                    rep.final = x2.destino
                else:
                    x1, xN = trasbordos[0], trasbordos[-1]
                    rep.vuelos1 = f"{x1.ciavuelo}{x1.vuelo}/{x1.salida.strftime('%d-%B')[:6].upper()}"
                    rep.vuelos2 = f"{xN.ciavuelo}{xN.vuelo}/{xN.salida.strftime('%d-%B')[:6].upper()}"
                    rep.final = xN.destino

            ciudad = Ciudades.objects.filter(codigo=rep.final).first()
            if ciudad:
                rep.airport_final = ciudad.nombre

            cargas = ExportCargaaerea.objects.filter(numero=house.numero)
            rep.mercaderias = []
            rep.volumen_total_embarque = 0
            top_base = 1030
            incremento = 10

            rep.total_bultos = rep.total_pesos = rep.total_total = 0
            tarifa_venta=house.tarifaventa

            for idx, carga in enumerate(cargas):
                bruto = carga.bruto or 0
                descripcion_medida = ''
                valor_aplicable = carga.aplicable or 0
                if carga.medidas:
                    medidas = carga.medidas.split('*')
                    if len(medidas) == 3:
                        try:
                            largo = float(medidas[0])
                            ancho = float(medidas[1])
                            alto = float(medidas[2])
                            vol = largo * ancho * alto
                            rep.volumen_total_embarque += vol
                            descripcion_medida = f"({carga.bultos}) * {carga.medidas} MTS"
                        except ValueError:
                            descripcion_medida = f"({carga.bultos}) * {carga.medidas} MTS"
                    else:
                        descripcion_medida = f"({carga.bultos}) * {carga.medidas} MTS"

                # Aplicable y total
                if valor_aplicable == 0:
                    aplicable_display = 'MIN'
                    total = float(house.tarifaventa)
                else:
                    aplicable_display = round(valor_aplicable, 2)
                    total = round(valor_aplicable * float(house.tarifaventa), 2)

                producto = carga.producto.nombre if carga.producto else 'SIN NOMBRE'

                descripcion = (
                    f'CONTAIN: \n{producto}\n'
                    f'{validar_valor(round(rep.volumen_total_embarque, 4))} CBM\n'
                    f'{descripcion_medida}'
                )

                rep.mercaderias.append({
                    'bultos': carga.bultos,
                    'peso': bruto,
                    'unidad': 'K',
                    'aplicable': aplicable_display,
                    'tarifa': tarifa_venta,
                    'total': total,
                    'descripcion': descripcion,
                    'top': top_base + (idx * incremento),
                })

                rep.total_bultos += carga.bultos
                rep.total_pesos += bruto
                rep.total_total += total

            if rep.modopago == 'Collect':
                rep.collect = rep.total_total
            else:
                rep.prepaid = rep.total_total

            gastos = ExportServiceaereo.objects.filter(numero=house.numero)
            rep.otros_gastos = ''
            for g in gastos:
                if g.precio == 0:
                    continue

                if g.modo == 'C':
                    if g.tipogasto == 'OTHER':
                        rep.valcol += g.precio
                    elif g.tipogasto == 'DUE CARRIER':
                        rep.carriercol += g.precio
                    elif g.tipogasto == 'DUE AGENT':
                        rep.agentcol += g.precio
                    rep.total_collect += g.precio
                else:
                    if g.tipogasto == 'OTHER':
                        rep.valppd += g.precio
                    elif g.tipogasto == 'DUE CARRIER':
                        rep.carrierppd += g.precio
                    elif g.tipogasto == 'DUE AGENT':
                        rep.agentppd += g.precio
                    rep.total_prepaid += g.precio

                rep.otros_gastos += f"{round(g.precio, 2)}   "

            if rep.modopago == 'Collect':
                rep.total_collect += Decimal(rep.collect or 0)
            else:
                rep.total_prepaid += Decimal(rep.prepaid or 0)

        # OUTPUT
        name = 'HWBL_' + str(house.seguimiento)
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
            rep.generar_awb(output, fondo='copia2.jpg')
            rep.generar_awb(output, fondo='copia3.jpg')
            rep.generar_awb(output, fondo='copia4.jpg')
            rep.generar_awb(output, fondo='copia5.jpg')
            rep.generar_awb(output, fondo='copia6.jpg')
        else:
            rep.generar_awb(output)

        return rep.descargo_archivo(output)


    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise Http404(f"Error: {str(e)}")
