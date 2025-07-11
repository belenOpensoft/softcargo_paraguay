import math
import os
from curses.ascii import isdigit
from datetime import datetime
from decimal import Decimal
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch, cm
from reportlab.platypus import Table, Paragraph
from cargosystem import settings
from cargosystem.settings import BASE_DIR
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import utils

class GuiasReport:

    def __init__(self):
        self.archivo = None
        self.numero = ''
        self.total_bultos = 0
        self.total_pesos = 0
        self.total_total = 0
        self.posicion = ''
        self.consignatario = ''
        self.shipper = ''
        self.awb_sf = ''
        self.awb1 = ''
        self.awb2 = ''
        self.awb3 = ''
        self.hawb = ''
        self.empresa = ''
        self.info = ''
        self.fechas = ''
        self.fechas2 = ''
        self.airport_departure = ''
        self.airport_final = ''
        self.final = ''
        self.by_cia_1 = ''
        self.by_cia_2 = ''
        self.by_cia_3 = ''
        self.to_1 = ''
        self.to_2 = ''
        self.to_3 = ''
        self.by_first_carrier = ''
        self.arraydestinos = ''
        self.modopago = ''
        self.cc1 = ''
        self.cc2 = ''
        self.pp1 = ''
        self.pp2 = ''
        self.pago_code = ''
        self.mercaderias = []
        self.medidas_text = []
        self.volumen_total_embarque = 0
        self.valppd = 0
        self.valcol = 0
        self.prepaid = 0
        self.collect = 0
        self.taxppd = 0
        self.taxcol = 0
        self.agentppd = 0
        self.agentcol = 0
        self.carrierppd = 0
        self.carriercol = 0
        self.total_precio_p = 0
        self.total_precio_c = 0
        self.total_prepaid = 0
        self.total_collect = 0
        self.otros_gastos = ''
        self.shipper_signature = ''
        self.carrier_signature = ''
        self.amount_insurance = 'NIL'
        self.handling = ''
        self.declared_value_for_carriage = 'NVD'
        self.declared_value_for_customs = 'NCV'
        self.iata_code_agente = ''
        self.account_nro = ''
        self.currency = ''
        self.vuelos1 = ''
        self.vuelos2 = ''
        self.issuing_carrier = ''
        self.descripcion_mercaderias = ''

    def generar_awb(self,output,fondo=None,dorso=0):
        try:
            i = 0
            if self.archivo is not None:
                self.archivo.showPage()
            else:
                self.archivo = canvas.Canvas(output, pagesize=A4)
            c = self.archivo
            if fondo is not None:
                fondo = utils.ImageReader(str(settings.BASE_DIR) + '/archivos/' + str(fondo))
                ancho_pagina, alto_pagina = A4
                ancho_imagen, alto_imagen = fondo.getSize()
                escala = min(ancho_pagina / ancho_imagen, alto_pagina / alto_imagen)
                c.drawImage(fondo, 0, 0, width=ancho_imagen * escala, height=alto_imagen * escala)
                if dorso == 1:
                    self.archivo = c
                    return

            # Agrega la imagen de fondo en cada página
            auxCab = []
            y = 820
            c.setFont("Helvetica-Bold", 10)
            styles = getSampleStyleSheet()
            style_texto = ParagraphStyle(
                name='BodyText',
                fontName='Helvetica',
                fontSize=8,
                leading=8
            )
            style_texto_7 = ParagraphStyle(
                name='BodyText',
                fontName='Helvetica',
                fontSize=7,
                leading=7
            )
            style_texto_6 = ParagraphStyle(
                name='BodyText',
                fontName='Helvetica',
                fontSize=6,
                leading=5
            )
            """ SHIPPER """
            data = [[Paragraph(self.empresa, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[8.5 * cm, ], rowHeights=[1.5 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'TOP'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 18 * mm, 251 * mm)

            """ EMPRESA """
            data = [[Paragraph(self.shipper, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[7 * cm, ], rowHeights=[1.1 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'TOP'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 130 * mm, 260.5 * mm)
            """ CONSIGNATARIO """
            data = [[Paragraph(self.consignatario, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[9 * cm, ], rowHeights=[1.6 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'TOP'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 18 * mm, 226 * mm)
            """ NOTIFY """
            data = [[Paragraph(self.info, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[9 * cm, ], rowHeights=[2.8 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'TOP'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 110 * mm, 195 * mm)
            """ AGENTE """
            data = [[Paragraph(self.issuing_carrier, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[9 * cm, ], rowHeights=[1.5 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'TOP'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 18 * mm, 208.3 * mm)
            """ DATOS """
            c.drawString(49,785,self.awb1)
            c.drawString(76,785,self.awb2)
            c.drawString(100,785,self.awb3)
            c.drawString(500,785,self.awb_sf)
            c.drawString(500,70,self.awb_sf)
            c.setFont("Helvetica", 8)
            c.drawString(55,550,self.airport_departure)
            c.drawString(55,575,self.iata_code_agente)

            c.drawString(55,527,self.to_1)
            c.drawString(80,527,self.by_cia_1)
            c.drawString(205,527,self.to_2)
            c.drawString(232,527,self.by_cia_2)
            c.drawString(255,527,self.to_3)
            c.drawString(280,527,self.by_cia_3)

            c.drawString(55,505,self.airport_final)

            """ FECHA1 """
            data = [[Paragraph(self.vuelos1, encoding='utf-8', style=style_texto_6)]]
            table = Table(data=data, colWidths=[2.5 * cm, ], rowHeights=[1 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'TOP'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 61 * mm, 172 * mm)
            """ FECHA2 """
            data = [[Paragraph(self.vuelos2, encoding='utf-8', style=style_texto_6)]]
            table = Table(data=data, colWidths=[2.5 * cm, ], rowHeights=[1 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'TOP'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 83 * mm, 172 * mm)

            """ handling info """
            data = [[Paragraph(self.handling,
                               encoding='utf-8',
                               style=style_texto_7)]]
            table = Table(data=data, colWidths=[5.5 * cm, ], rowHeights=[1.4 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'TOP'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 20 * mm, 158 * mm)
            c.drawString(305, 527, self.currency)
            c.drawString(333, 527, self.pago_code)
            c.drawString(350, 523, self.pp1)
            c.drawString(364, 523, self.cc1)
            c.drawString(375, 523, self.pp2)
            c.drawString(390, 523, self.cc2)
            c.drawString(440, 527, self.declared_value_for_carriage)
            c.drawString(520, 527, self.declared_value_for_customs)
            c.drawString(335, 505, self.amount_insurance )
            """ MERCADERIAS """
            y = 420

            if self.mercaderias:
                for m in self.mercaderias:
                    c.drawString(52, y, str(m['bultos']))  # Bultos
                    c.drawString(82, y, str(m['peso']))  # Peso bruto
                    c.drawString(127, y, str(m['unidad']))  # Unidad (K)
                    c.drawString(205, y, self.formatear_valor(m['aplicable']))  # Aplicable
                    c.drawString(280, y, self.formatear_valor(m['tarifa']))  # Tarifa
                    c.drawString(340, y, self.formatear_valor(m['total']))  # Total

                    y -= 50  # espacio entre filas

            # Mostrar descripción una sola vez
            if hasattr(self, 'descripcion_mercaderias') and self.descripcion_mercaderias:
                data = [[Paragraph(self.descripcion_mercaderias, encoding='utf-8', style=style_texto_7)]]
                table = Table(
                    data=data,
                    colWidths=[5 * cm],
                    style=[
                        ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                        ('VALIGN', (0, 0), (0, 0), 'TOP'),
                    ]
                )
                table.wrapOn(c, 0, 0)
                table.drawOn(c, 145 * mm, 142 * mm)  # ajustar posición si hace falta

            # Totales pie
            c.drawString(52, 280, str(self.total_bultos))
            c.drawString(82, 280, self.formatear_valor(self.total_pesos))
            c.drawString(340, 280, self.formatear_valor(self.total_total))

            # Prepaid o Collect
            if self.pago_code == 'PP':
                c.drawString(80, 250, self.formatear_valor(self.total_total))
                c.drawString(200, 250, '')
                montoppd = self.total_total
                montocol = 0
            else:
                c.drawString(80, 250, '')
                c.drawString(200, 250, self.formatear_valor(self.total_total))
                montoppd = 0
                montocol = self.total_total

            # Posición
            c.drawString(253, 200, str(self.posicion))

            # Shipper en posición final
            c.drawString(300, 145, self.shipper_signature)

            """ otros datos """
            data = [[Paragraph(self.carrier_signature,
                               encoding='utf-8',
                               style=style_texto_7)]]
            table = Table(data=data, colWidths=[10 * cm, ], rowHeights=[1.4 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'TOP'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 90 * mm, 30 * mm)
            # Montos columna izquierda (PREPAID)
            c.drawString(80, 230, self.formatear_valor(self.valppd))
            c.drawString(80, 200, self.formatear_valor(self.taxppd))
            c.drawString(80, 180, self.formatear_valor(self.agentppd))
            c.drawString(80, 155, self.formatear_valor(self.carrierppd))
            c.drawString(80, 107, self.formatear_valor(self.total_prepaid))

            # Montos columna derecha (COLLECT)
            c.drawString(200, 230, self.formatear_valor(self.valcol))
            c.drawString(200, 200, self.formatear_valor(self.taxcol))
            c.drawString(200, 180, self.formatear_valor(self.agentcol))
            c.drawString(200, 155, self.formatear_valor(self.carriercol))
            c.drawString(200, 107, self.formatear_valor(self.total_collect))

            # Otros gastos (cuadro texto libre)
            otros_data = [[Paragraph(self.otros_gastos, encoding='utf-8', style=style_texto_7)]]
            tabla_otros = Table(
                data=otros_data,
                colWidths=[10 * cm],
                rowHeights=[1 * cm],
                style=[
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                    ('VALIGN', (0, 0), (0, 0), 'TOP'),
                ]
            )
            tabla_otros.wrapOn(c, 0, 0)
            tabla_otros.drawOn(c, 90 * mm, 74 * mm)

            c.drawString(80, 107, self.formatear_valor(self.total_precio_p))  # Total Prepaid
            c.drawString(200, 107, self.formatear_valor(self.total_precio_c))  # Total Collect

            self.archivo = c
        except Exception as e:
            raise TypeError(e)

    def descargo_archivo(self,output):
        try:
            self.archivo.save()
            pdf_data = open(output, "rb").read()
            os.remove(output)
            return HttpResponse(pdf_data, content_type="application/pdf")
        except Exception as e:
            raise TypeError(e)

    def formatear_valor(self, valor):
        try:
            if valor is not None:
                valor_str = str(valor)
                # Intentamos convertir a Decimal para verificar si es numérico
                try:
                    val = Decimal(valor_str)
                    return str(round(val, 2)) if val != 0 else ''
                except:
                    return valor_str
            else:
                return ''
        except Exception:
            return 'ERROR'




