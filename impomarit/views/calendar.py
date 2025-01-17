from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import xlsxwriter
from django.http import HttpResponse

from impomarit.models import VistaEventosCalendario


@login_required(login_url='/')
def calendario(request):
    try:
        if request.user.has_perms(["impomarit.view_vistaeventoscalendario",]):
            opciones_busqueda = {
                'cliente__icontains': 'CLIENTE',
                'embarcador__icontains': 'EMBARCADOR',
                'consignatario__icontains': 'CONSIGNATARIO',
                'origen_text__icontains': 'ORIGEN',
                'destino_text__icontains': 'DESTINO',
                'awb__icontains': 'BL',
                'hawb__icontains': 'HBL',
                'vapor__icontains': 'Vapor',
                'posicion__icontains': 'Posicion',
                # 'contenedores__icontains': 'Contenedor',
            }
            return render(request, 'impormarit/calendar_general.html',{

            })
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')


def eventos_calendario(request):
    # Obtener los filtros desde la solicitud
    modo_filtro = request.GET.get('modo_filtro', '')
    filtro_cliente = request.GET.get('filtro_cliente', '')

    # Iniciar la consulta base
    eventos = VistaEventosCalendario.objects.all()

    # Aplicar filtro por 'source' (modo)
    if modo_filtro:
        eventos = eventos.filter(source=modo_filtro)

    # Aplicar filtro por consignatario
    if filtro_cliente:
        eventos = eventos.filter(consignatario__icontains=filtro_cliente)

    # Formatear eventos
    eventos_formateados = []
    for evento in eventos:
        titulo = f"{evento.posicion}"

        if evento.source == 'impmarit':
            color = '#ADD8E6'  # Azul claro para marítimo
            source_formatted = "IMPO MARÍTIMO"
        elif evento.source == 'import':
            color = '#90EE90'  # Verde claro para aéreo
            source_formatted = "IMPO AÉREO"
        elif evento.source == 'impterra':
            color = '#FF7F7F'
            source_formatted = "IMPO TERRESTRE"

        if evento.fecharetiro is not None:
            fecha_evento = evento.fecharetiro.strftime('%Y-%m-%d')
        else:
            fecha_evento = None

        if fecha_evento:
            # Agregar todos los campos relevantes al evento formateado
            eventos_formateados.append({
                'title': titulo,
                'start': fecha_evento,
                'color': color,
                'awb': evento.awb,
                'hawb': evento.hawb,
                'status': evento.status,
                'origen': evento.origen,
                'destino': evento.destino,
                'transportista': evento.transportista,
                'consignatario': evento.consignatario,
                'source_formatted': source_formatted,
                'posicion': evento.posicion,
            })

    return JsonResponse(eventos_formateados, safe=False)

@login_required(login_url='/')
def generar_reporte_excel(request):
    # Obtener los filtros desde la solicitud GET
    modo_filtro = request.GET.get('modo_filtro', '')
    filtro_cliente = request.GET.get('filtro_cliente', '')
    desde_filtro = request.GET.get('desde', '')
    hasta_filtro = request.GET.get('hasta', '')

    # Comprobar que se recibieron los valores esperados
    print(f"Modo Filtro: {modo_filtro}, Cliente: {filtro_cliente}, Desde: {desde_filtro}, Hasta: {hasta_filtro}")

    # Iniciar la consulta base
    eventos = VistaEventosCalendario.objects.all()

    # Aplicar filtro por 'source' (modo)
    if modo_filtro:
        eventos = eventos.filter(source=modo_filtro)

    # Aplicar filtro por consignatario
    if filtro_cliente:
        eventos = eventos.filter(consignatario__icontains=filtro_cliente)

    # Aplicar filtro por rango de fechas
    if desde_filtro and hasta_filtro:
        eventos = eventos.filter(fecharetiro__range=[desde_filtro, hasta_filtro])

    # Formatear los eventos para pasarlos a la función que genera el reporte Excel
    eventos_formateados = []
    for evento in eventos:
        eventos_formateados.append({
            'posicion': evento.posicion,
            'awb': evento.awb,
            'hawb': evento.hawb,
            'status': evento.status,
            'origen': evento.origen,
            'destino': evento.destino,
            'transportista': evento.transportista,
            'consignatario': evento.consignatario,
            'fecharetiro': evento.fecharetiro.strftime('%Y-%m-%d') if evento.fecharetiro else '',
            'source_formatted': (
                'IMPO AÉREO' if evento.source == 'import'
                else 'IMPO MARÍTIMO' if evento.source == 'impmarit'
                else 'IMPO TERRESTRE'
            )

        })

    # Llamar a la función que genera el reporte Excel y devolverlo
    return generar_reporte_excel_file(eventos_formateados, modo_filtro, filtro_cliente, desde_filtro, hasta_filtro)


def generar_reporte_excel_file(datos, modo_filtro='', filtro_cliente='', desde='', hasta=''):
    # Crear un objeto HttpResponse con el tipo de contenido Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_eventos.xlsx"'

    # Crear un archivo Excel en memoria usando xlsxwriter
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Ajustar el ancho de las columnas
    worksheet.set_column('A:A', 25)  # Ajustar la columna de 'Posición' a 15 caracteres de ancho
    worksheet.set_column('B:B', 20)  # Ajustar la columna de 'AWB' a 20 caracteres de ancho
    worksheet.set_column('C:C', 20)  # Ajustar la columna de 'HAWB' a 20 caracteres de ancho
    worksheet.set_column('D:D', 15)  # Ajustar la columna de 'Status' a 15 caracteres de ancho
    worksheet.set_column('E:E', 15)  # Ajustar la columna de 'Origen' a 15 caracteres de ancho
    worksheet.set_column('F:F', 15)  # Ajustar la columna de 'Destino' a 15 caracteres de ancho
    worksheet.set_column('G:G', 30)  # Ajustar la columna de 'Transportista' a 30 caracteres de ancho
    worksheet.set_column('H:H', 30)  # Ajustar la columna de 'Consignatario' a 30 caracteres de ancho
    worksheet.set_column('I:I', 15)  # Ajustar la columna de 'Fecha Retiro' a 15 caracteres de ancho
    worksheet.set_column('J:J', 20)  # Ajustar la columna de 'Tipo' a 20 caracteres de ancho

    # Escribir encabezados de columnas en la primera fila
    headers = ['Posición', 'AWB', 'HAWB', 'Status', 'Origen', 'Destino', 'Transportista', 'Consignatario', 'Fecha Retiro', 'Tipo']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Escribir los datos en las filas siguientes
    for row_num, evento in enumerate(datos, start=1):
        worksheet.write(row_num, 0, evento['posicion'])
        worksheet.write(row_num, 1, evento['awb'])
        worksheet.write(row_num, 2, evento['hawb'])
        worksheet.write(row_num, 3, evento['status'])
        worksheet.write(row_num, 4, evento['origen'])
        worksheet.write(row_num, 5, evento['destino'])
        worksheet.write(row_num, 6, evento['transportista'])
        worksheet.write(row_num, 7, evento['consignatario'])
        worksheet.write(row_num, 8, evento['fecharetiro'])
        worksheet.write(row_num, 9, evento['source_formatted'])

    # Si hay filtros aplicados, agregarlos en una sección del reporte
    filtro_texto = []
    if modo_filtro:
        filtro_texto.append(f"Modo: {modo_filtro}")
    if filtro_cliente:
        filtro_texto.append(f"Consignatario: {filtro_cliente}")
    if desde and hasta:
        filtro_texto.append(f"Rango de Fechas: {desde} - {hasta}")

    if filtro_texto:
        # Agregar una fila vacía antes de mostrar los filtros
        worksheet.write(row_num + 1, 0, "Filtros aplicados:")
        for i, filtro in enumerate(filtro_texto, start=row_num + 2):
            worksheet.write(i, 0, filtro)

    # Cerrar el archivo y devolver el response
    workbook.close()
    return response


