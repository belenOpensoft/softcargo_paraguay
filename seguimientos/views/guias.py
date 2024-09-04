import math
import os
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
        self.awb = ''
        self.hawb = ''
        # VARIABLES BL
        self.seguimiento = ''
        # VARIABLES BL
        self.shipper = ''
        self.shipper_nom = ''
        self.consignatario = ''
        self.empresa = settings.EMPRESA_HAWB
        self.notify = ''
        self.agente = settings.EMPRESA_HAWB
        self.trasbordos = ''
        self.routing = ''
        self.destino = ''
        self.final = ''
        self.airport_final = ''
        self.compania = ''
        self.arraydestinos = ''
        self.fechas = ''
        self.pago = ''
        self.mercaderias = []
        self.modopago = ''
        self.valppd = 0
        self.valcol = 0
        self.taxppd = 0
        self.taxcol = 0
        self.agentppd = 0
        self.agentcol = 0
        self.carrierppd = 0
        self.carriercol = 0
        self.othppd = 0
        self.othcol = 0
        self.posicion = ''

    def generar_hawb(self,output,fondo=None):
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
            """ SHIPPER """
            data = [[Paragraph(self.shipper, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[9 * cm, ], rowHeights=[1.7 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 9 * mm, 265 * mm)
            """ EMPRESA """
            data = [[Paragraph(self.empresa, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[7 * cm, ], rowHeights=[1.1 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 127 * mm, 273.5 * mm)
            """ CONSIGNATARIO """
            data = [[Paragraph(self.consignatario, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[9 * cm, ], rowHeights=[1.7 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 9 * mm, 242.5 * mm)
            """ NOTIFY """
            data = [[Paragraph(self.notify, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[9 * cm, ], rowHeights=[2.1 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 110 * mm, 215 * mm)
            """ AGENTE """
            data = [[Paragraph(self.agente, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[9 * cm, ], rowHeights=[1.8 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 9 * mm, 221 * mm)
            """ DATOS """
            c.drawString(40,815,self.awb)
            c.drawString(500,815,self.hawb)
            c.setFont("Helvetica", 8)
            c.drawString(30,580,self.routing)
            c.drawString(30,550,self.destino)
            c.drawString(80,550,self.compania)
            c.drawString(210,550,self.arraydestinos)
            c.drawString(30,525,self.airport_final)
            """ AGENTE """
            data = [[Paragraph(self.fechas, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[4.5 * cm, ], rowHeights=[1 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 60 * mm, 178 * mm)
            c.drawString(305, 550, 'USD')
            c.drawString(332, 550, self.pago)
            c.drawString(440, 550, 'NVD')
            c.drawString(520, 550, 'NCV')
            c.drawString(335, 525, 'NIL')
            """ MERCADERIAS """
            y = 430
            bultos = 0
            pesos = 0
            fletes = 0
            for m in self.mercaderias:
                c.drawString(30,y,str(m[0]))
                c.drawString(60,y,str(m[1]))
                c.drawString(110,y,str(m[2]))
                c.drawString(210,y,str(m[4]))
                c.drawString(300,y,str(m[5]))
                c.drawString(385,y,str(m[6]))
                bultos += m[0]
                pesos += m[1]
                fletes += m[6]
                # c.drawString(470,y,str(m[7]))
                """ DESCRIPCION MERCADERIA """
                data = [[Paragraph(str(m[7]), encoding='utf-8', style=style_texto_7)]]
                table = Table(data=data, colWidths=[4 * cm, ], rowHeights=[1 * cm, ],
                              style=[
                                  ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                                  ('VALIGN', (0, 0), (0, 0), 'TOP'),
                              ]
                              )
                table.wrapOn(c, 0, 0)
                table.drawOn(c, 162 * mm, 145 * mm)
                y -= 50
            c.drawString(30,287,str(bultos))
            c.drawString(60,287,str(pesos))
            c.drawString(385,287,str(fletes))
            if self.modopago == 'Prepaid':
                c.drawString(40,255,str(fletes))
                c.drawString(200,255,str(0))
                montoppd = fletes
                montocol = 0
            else:
                c.drawString(40,255,str(0))
                c.drawString(200,255,str(fletes))
                montoppd = 0
                montocol = fletes
            c.drawString(300,130,str(self.posicion))
            c.drawString(420,130,str(self.shipper_nom))
            """ MONTOS """
            c.drawString(40, 230, str(round(self.valppd,2)))
            c.drawString(200, 230, str(round(self.valcol,2)))
            c.drawString(40, 200, str(round(self.taxppd,2)))
            c.drawString(200, 200, str(round(self.taxcol,2)))
            c.drawString(40, 170, str(round(self.agentppd,2)))
            c.drawString(200, 170, str(round(self.agentcol,2)))
            c.drawString(40, 140, str(round(self.carrierppd,2)))
            c.drawString(200, 140, str(round(self.carriercol,2)))
            """ OTHER """
            c.drawString(40, 115, str(round(self.othppd,2)))
            c.drawString(200, 115, str(round(self.othcol,2)))
            """ TOTALES """
            c.drawString(40, 85, str(round(Decimal(montoppd) + self.othppd + self.valppd + self.taxppd + self.agentppd + self.carrierppd,2)))
            c.drawString(200, 85, str(round(Decimal(montocol) + self.othcol + self.valcol + self.taxcol + self.agentcol + self.carriercol,2)))

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
