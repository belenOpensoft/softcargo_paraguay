import os
from django.urls import reverse
from urllib.parse import urlencode

from django.http import JsonResponse
from django.shortcuts import render, redirect

from cargosystem import settings
from impaerea.models import ImportEmbarqueaereo
from impomarit.forms import EntregaDocumentacionForm, GenerarDocumentoForm
from impomarit.models import Embarqueaereo
from impterrestre.models import ImpterraEmbarqueaereo
from mantenimientos.models import Clientes

# views.py
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import datetime
from django.contrib import messages

def generar_entrega_documentacion_pdf_old(request):
    if request.method == 'POST':
        data = request.POST

        # Configurar response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="entrega_documentacion.pdf"'

        # Crear PDF
        c = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 30 * mm
        logo_path = os.path.join(settings.PACKAGE_ROOT, 'static', 'images', 'oceanlink.png')
        # Asegurate de ubicar la imagen dentro de los márgenes de la hoja
        c.drawImage(logo_path, 20 * mm, y, width=30 * mm, preserveAspectRatio=True, mask='auto')

        """
                c.setFont("Courier-Bold", 12)
        c.drawString(20 * mm, y, "Oceanlink Group")
        c.setFont("Courier", 9)
        c.drawString(20 * mm, y - 5 * mm, "TOTAL LOGISTICS")
        """


        titulo = "ENTREGA DE DOCUMENTACIÓN"
        c.setFont("Courier-Bold", 11)
        text_width = c.stringWidth(titulo, "Courier-Bold", 11)
        x_centro = (width - text_width) / 2
        c.drawString(x_centro, y - 13 * mm, titulo)

        c.setFont("Courier", 10)
        c.drawString(20 * mm, y - 22 * mm, f"Estamos adjuntando documentación de {data.get('modo')}, embarcado por vuestra firma.")

        y -= 35 * mm
        c.setFont("Courier", 9)

        def linea(label, valor, bold=False):
            nonlocal y
            c.setFont("Courier-Bold" if bold else "Courier", 9)
            c.drawString(20 * mm, y, f"{label:<15}: {valor}")
            y -= 6 * mm

        linea("Referencia", data.get("orden", "S/I"), bold=True)
        linea("Posicion", data.get("posicion", "S/I"), bold=True)
        linea("Modo", data.get("modo", "S/I"), bold=True)
        linea("Fecha", datetime.now().strftime("%d/%m/%Y"), bold=True)
        y -= 5 * mm
        c.setFont("Courier-Bold", 9)
        titulo_datos = "Datos generales:"
        c.drawString(20 * mm, y, titulo_datos)
        c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(titulo_datos, "Courier-Bold", 9), y - 1.5 * mm)

        y -= 6 * mm

        linea("Embarcador", data.get("embarcador", ""))
        linea("Cliente", data.get("cliente", ""))
        linea("RUT", data.get("rut", ""))
        linea("Orden cliente", data.get("orden", ""))
        linea("MBL / AWB", data.get("mbl_awb", ""))
        linea("Origen", data.get("origen", ""))
        linea("Destino", data.get("destino", ""))
        linea("Fecha salida", datetime.now().strftime("%d/%m/%Y"))

        y -= 5 * mm
        c.setFont("Courier-Bold", 9)
        titulo_doc = "Documentos adjuntos"
        c.drawString(20 * mm, y, titulo_doc)

        # Calcular ancho del texto para la línea
        line_length = c.stringWidth(titulo_doc, "Courier-Bold", 9)
        c.line(20 * mm, y - 1.5 * mm, 20 * mm + line_length, y - 1.5 * mm)
        y -= 6 * mm
        c.setFont("Courier", 9)

        docs = request.POST.getlist('documentos_adjuntos')
        if docs:
            col_width = 55 * mm  # Ancho por columna
            max_cols = 3
            for i, doc in enumerate(docs):
                col = i % max_cols
                row = i // max_cols
                x = 25 * mm + col * col_width
                y_offset = y - (row * 5 * mm)
                c.drawString(x, y_offset, f"* {doc.replace('_', ' ').upper()}")
            y -= ((len(docs) + 2) // 3) * 5 * mm  # Ajustar el y final en base a filas utilizadas
        else:
            c.drawString(25 * mm, y, "S/I")
            y -= 5 * mm

        y -= 5 * mm
        c.setFont("Courier-Bold", 9)
        titulo_entrega = "Entréguese a:"
        c.drawString(20 * mm, y, titulo_entrega)
        c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(titulo_entrega, "Courier-Bold", 9), y - 1.5 * mm)
        y -= 6 * mm
        c.setFont("Courier", 9)
        linea("Nombre", data.get("nombre_entrega", ""))
        linea("Dirección", data.get("direccion_entrega", ""))
        linea("Ciudad", data.get("ciudad_entrega", ""))
        linea("Teléfono", data.get("telefono_entrega", ""))

        if data.get("imprimir_comentarios"):
            c.setFont("Courier-Bold", 9)
            y -= 5 * mm
            c.drawString(20 * mm, y, "Comentarios:")
            y -= 6 * mm
            c.setFont("Courier", 9)
            text = c.beginText(25 * mm, y)
            text.textLines(data.get("comentarios", ""))
            c.drawText(text)
            y = text.getY() - 6 * mm

        y -= 5 * mm
        c.drawString(20 * mm, y, "Recepcionado por:")
        y -= 10 * mm
        c.drawString(20 * mm, y, "Nombre ..........: ________________________")
        y -= 6 * mm
        c.drawString(20 * mm, y, "Referencia ......: ________________________")
        y -= 6 * mm
        c.drawString(20 * mm, y, "Firma ........... ________________________     Sello/CI ________________________")
        y -= 6 * mm
        c.drawString(20 * mm, y, "Fecha ...........: ____/____/______     Teléfono ______________________")
        y -= 6 * mm
        c.drawString(20 * mm, y, "Hora ............: __________________")

        # Footer
        y -= 12 * mm
        c.setFont("Courier-Bold", 8)
        c.drawString(20 * mm, y, "BOLONIA 2280, EDIFICIO LOS ALAMOS OF 103 (LATU), MONTEVIDEO, 11500")
        y -= 5 * mm
        c.drawString(20 * mm, y, "Tel.: S/I, Fax: S/I")

        c.showPage()
        c.save()
        return response


def entrega_documentacion_general(request):
    form_data = request.GET.copy()
    rol = request.GET.get('rol', request.rol_pestana)

    form_data.pop('rol', None)
    form_busqueda = GenerarDocumentoForm(form_data or None)

    form_modal = EntregaDocumentacionForm()
    resultados = []
    resultado_seleccionado = None
    busqueda_realizada = False

    cliente_data = {'nombre': '', 'direccion': '', 'ciudad': '', 'telefono': ''}
    despachante_data = {'nombre': '', 'direccion': '', 'ciudad': '', 'telefono': ''}

    if form_busqueda.is_valid():
        seguimiento = form_busqueda.cleaned_data.get('seguimiento')
        operativa = form_busqueda.cleaned_data.get('operativa')
        embarque = None
        busqueda_realizada = True

        if operativa == 'IT':
            embarque = ImpterraEmbarqueaereo
        elif operativa == 'IA':
            embarque = ImportEmbarqueaereo
        elif operativa == 'IM':
            embarque = Embarqueaereo
        else:
            return JsonResponse({'success': False, 'error': 'No coincide la operativa'})

        resultados = embarque.objects.filter(seguimiento=seguimiento)

        if resultados.exists():
            form_busqueda = GenerarDocumentoForm()
            resultado = resultados.first()
            resultado_seleccionado = resultado

            cliente = Clientes.objects.filter(codigo=resultado.consignatario).first() if resultado.consignatario else None
            embarcador = Clientes.objects.filter(codigo=resultado.embarcador).first() if resultado.embarcador else None
            despachante = Clientes.objects.filter(codigo=resultado.despachante).first() if resultado.despachante else None

            consignatario = cliente.empresa if cliente else 'S/I'
            rut = cliente.ruc if cliente else 'S/I'
            emb = embarcador.empresa if embarcador else 'S/I'

            initial_data = {
                'cliente': consignatario,
                'embarcador': emb,
                'orden': resultado.ordencliente,
                'rut': rut,
                'modo': operativa,
                'mbl_awb': resultado.awb,
                'origen': resultado.origen,
                'destino': resultado.destino,
                'posicion': resultado.posicion,
                'entregar_a': 'cliente',
            }

            cliente_data = {
                'nombre': consignatario,
                'direccion': cliente.direccion if cliente else '',
                'ciudad': cliente.ciudad if cliente else '',
                'telefono': cliente.telefono if cliente else '',
            }
            despachante_data = {
                'nombre': despachante.empresa if despachante else '',
                'direccion': despachante.direccion if despachante else '',
                'ciudad': despachante.ciudad if despachante else '',
                'telefono': despachante.telefono if despachante else '',
            }

            form_modal = EntregaDocumentacionForm(initial=initial_data)

        else:
            messages.info(request, "No se encontraron resultados.")
            return redirect('entrega_documentacion_general')

    return render(request, 'impormarit/entrega_documentacion_general.html', {
        'form': form_busqueda,
        'form_modal': form_modal,
        'resultados': resultados,
        'resultado': resultado_seleccionado,
        'cliente_data': cliente_data,
        'despachante_data': despachante_data,
        'busqueda_realizada': busqueda_realizada,
        'rol': rol,
    })


def generar_entrega_documentacion_pdf(request):

    if request.method == 'POST':
        data = request.POST
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="entrega_documentacion.pdf"'
        c = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 30 * mm
        logo_path = os.path.join(settings.PACKAGE_ROOT, 'static', 'images', 'oceanlink.png')
        c.drawImage(logo_path, 20 * mm, y, width=30 * mm, preserveAspectRatio=True, mask='auto')

        def check_page_space(c, y, needed_space, margin_bottom=20 * mm):
            if y - needed_space < margin_bottom:
                c.showPage()
                c.setFont("Courier", 9)
                return height - 30 * mm
            return y

        titulo = "ENTREGA DE DOCUMENTACIÓN"
        c.setFont("Courier-Bold", 11)
        text_width = c.stringWidth(titulo, "Courier-Bold", 11)
        x_centro = (width - text_width) / 2
        y = check_page_space(c, y, 13 * mm)
        c.drawString(x_centro, y - 13 * mm, titulo)

        modo = 'S/I'
        if data.get('modo')=='IM':
            modo = 'IMPORTACION MARITIMA'
        elif data.get('modo') == 'IA':
            modo = 'IMPORTACION AEREA'
        elif data.get('modo')=='IT':
            modo = 'IMPORTACION TERRESTRE'

        c.setFont("Courier", 10)
        y = check_page_space(c, y, 22 * mm)
        c.drawString(20 * mm, y - 22 * mm, f"Estamos adjuntando documentación de {modo}, embarcado por vuestra firma.")
        y -= 35 * mm
        c.setFont("Courier", 9)

        def linea(label, valor, bold=False):
            nonlocal y
            y = check_page_space(c, y, 6 * mm)
            c.setFont("Courier-Bold" if bold else "Courier", 9)
            c.drawString(20 * mm, y, f"{label:<15}: {valor}")
            y -= 6 * mm

        linea("Referencia", data.get("orden", "S/I"), bold=True)
        linea("Posicion", data.get("posicion", "S/I"), bold=True)
        linea("Modo", modo, bold=True)
        linea("Fecha", datetime.now().strftime("%d/%m/%Y"), bold=True)

        y = check_page_space(c, y, 5 * mm)
        y -= 5 * mm
        c.setFont("Courier-Bold", 9)
        titulo_datos = "Datos generales:"
        y = check_page_space(c, y, 6 * mm)
        c.drawString(20 * mm, y, titulo_datos)
        c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(titulo_datos, "Courier-Bold", 9), y - 1.5 * mm)
        y -= 6 * mm

        linea("Embarcador", data.get("embarcador", ""))
        linea("Cliente", data.get("cliente", ""))
        linea("RUT", data.get("rut", ""))
        linea("Orden cliente", data.get("orden", ""))
        linea("MBL / AWB", data.get("mbl_awb", ""))
        linea("Origen", data.get("origen", ""))
        linea("Destino", data.get("destino", ""))
        linea("Fecha salida", datetime.now().strftime("%d/%m/%Y"))

        y = check_page_space(c, y, 5 * mm)
        y -= 5 * mm
        c.setFont("Courier-Bold", 9)
        titulo_doc = "Documentos adjuntos"
        y = check_page_space(c, y, 6 * mm)
        c.drawString(20 * mm, y, titulo_doc)
        line_length = c.stringWidth(titulo_doc, "Courier-Bold", 9)
        c.line(20 * mm, y - 1.5 * mm, 20 * mm + line_length, y - 1.5 * mm)
        y -= 6 * mm
        c.setFont("Courier", 9)

        docs = request.POST.getlist('documentos_adjuntos')
        if docs:
            col_width = 55 * mm  # Ancho por columna
            max_cols = 3
            row_height = 5 * mm
            rows = (len(docs) + max_cols - 1) // max_cols
            for row in range(rows):
                for col in range(max_cols):
                    index = row + rows * col
                    if index < len(docs):
                        x = 25 * mm + col * col_width
                        c.drawString(x, y, f"* {docs[index].replace('_', ' ').upper()}")
                y -= row_height
        else:
            c.drawString(25 * mm, y, "S/I")
            y -= 5 * mm

        y = check_page_space(c, y, 5 * mm)
        y -= 5 * mm
        c.setFont("Courier-Bold", 9)
        titulo_entrega = "Entréguese a:"
        y = check_page_space(c, y, 6 * mm)
        c.drawString(20 * mm, y, titulo_entrega)
        c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(titulo_entrega, "Courier-Bold", 9), y - 1.5 * mm)
        y -= 6 * mm
        c.setFont("Courier", 9)
        linea("Nombre", data.get("nombre_entrega", ""))
        linea("Dirección", data.get("direccion_entrega", ""))
        linea("Ciudad", data.get("ciudad_entrega", ""))
        linea("Teléfono", data.get("telefono_entrega", ""))

        if data.get("imprimir_comentarios"):
            c.setFont("Courier-Bold", 9)
            y = check_page_space(c, y, 5 * mm)
            y -= 5 * mm
            c.drawString(20 * mm, y, "Comentarios:")
            y -= 6 * mm
            c.setFont("Courier", 9)
            text = c.beginText(25 * mm, y)
            text.textLines(data.get("comentarios", ""))
            c.drawText(text)
            y = text.getY() - 6 * mm

        y = check_page_space(c, y, 35 * mm)
        y -= 5 * mm
        c.drawString(20 * mm, y, "Recepcionado por:")
        y -= 10 * mm
        c.drawString(20 * mm, y, "Nombre ..........: ________________________")
        y -= 6 * mm
        c.drawString(20 * mm, y, "Referencia ......: ________________________")
        y -= 6 * mm
        c.drawString(20 * mm, y, "Firma ........... ________________________     Sello/CI ________________________")
        y -= 6 * mm
        c.drawString(20 * mm, y, "Fecha ...........: ____/____/______     Teléfono ______________________")
        y -= 6 * mm
        c.drawString(20 * mm, y, "Hora ............: __________________")

        y = check_page_space(c, y, 12 * mm)
        y -= 12 * mm
        c.setFont("Courier-Bold", 8)
        c.drawString(20 * mm, y, "BOLONIA 2280, EDIFICIO LOS ALAMOS OF 103 (LATU), MONTEVIDEO, 11500")
        y -= 5 * mm
        c.drawString(20 * mm, y, "Tel.: S/I, Fax: S/I")

        c.showPage()
        c.save()
        return response
