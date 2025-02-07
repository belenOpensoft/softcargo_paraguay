import math
import os
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
        self.awb = ''
        self.awb_sf = ''
        self.hawb = ''
        # VARIABLES BL
        self.seguimiento = ''
        # VARIABLES BL
        self.shipper = ''
        self.shipper_nom = ''
        self.consignatario = ''
        self.empresa = settings.EMPRESA_HAWB
        self.notify = ''
        self.agente = settings.EMPRESA_AWB
        self.trasbordos = ''
        self.routing = ''
        self.destino = ''
        self.final = ''
        self.airport_final = ''
        self.compania = ''
        self.arraydestinos = ''
        self.fechas = ''
        self.fechas2 = ''
        self.pago = ''
        self.othppd=0
        self.othcol=0
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
        self.total_precio_p = 0
        self.total_precio_c = 0
        self.otros_gastos = ''
        self.posicion = ''
        self.medidas_text = []

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
            """ EMPRESA """
            data = [[Paragraph(self.empresa, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[8.5 * cm, ], rowHeights=[1.5 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 18 * mm, 251 * mm)
            """ SHIPPER """
            data = [[Paragraph(self.shipper, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[7 * cm, ], rowHeights=[1.1 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 130 * mm, 257.5 * mm)
            """ CONSIGNATARIO """
            data = [[Paragraph(self.consignatario, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[9 * cm, ], rowHeights=[1.7 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 18 * mm, 228 * mm)
            """ NOTIFY """
            data = [[Paragraph(self.notify, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[9 * cm, ], rowHeights=[2.1 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 110 * mm, 195 * mm)
            """ AGENTE """
            data = [[Paragraph(self.agente, encoding='utf-8', style=style_texto_7)]]
            table = Table(data=data, colWidths=[9 * cm, ], rowHeights=[1.6 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 18 * mm, 208.3 * mm)
            """ DATOS """
            c.drawString(49,785,self.awb)
            c.drawString(500,785,self.awb_sf)
            c.drawString(500,70,self.awb_sf)
            c.setFont("Helvetica", 8)
            c.drawString(55,550,self.routing)
            c.drawString(55,527,self.destino)
            c.drawString(80,527,self.compania)
            c.drawString(217,527,self.arraydestinos)
            c.drawString(55,505,self.airport_final)
            """ FECHA1 """
            data = [[Paragraph(self.fechas, encoding='utf-8', style=style_texto_6)]]
            table = Table(data=data, colWidths=[2.5 * cm, ], rowHeights=[1 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'TOP'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 61 * mm, 172 * mm)
            """ FECHA2 """
            data = [[Paragraph(self.fechas2, encoding='utf-8', style=style_texto_6)]]
            table = Table(data=data, colWidths=[2.5 * cm, ], rowHeights=[1 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'TOP'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 83 * mm, 172 * mm)

            """ handling info """
            data = [[Paragraph('MARKS: AS PER ATTACHED MANIFEST<br/><br/>ATTACHED: ENVELOPE WITH DOCS',
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

            c.drawString(305, 527, 'USD')
            c.drawString(332, 527, self.pago)
            c.drawString(440, 527, 'NVD')
            c.drawString(520, 527, 'NCV')
            c.drawString(335, 505, 'NIL')
            """ MERCADERIAS """
            y = 420
            bultos = 0
            pesos = 0
            fletes = 0
            if self.mercaderias:
                m = self.mercaderias[0]

                c.drawString(52, y, str(m[0]))  # Total de bultos
                c.drawString(82, y, str(m[1]))  # Total de peso bruto
                c.drawString(127, y, str(m[2]))  # Unidad de medida (K)
                c.drawString(205, y, str(m[6]))  # aplicable
                c.drawString(280, y, str(m[5]))  # Tarifa de venta
                c.drawString(340, y, str(m[7]))  # Total

                # Asignar las sumas a las variables
                bultos = m[0]
                pesos = m[1]
                fletes = m[7]

                """ DESCRIPCION MERCADERIA """
                texto='CONSOLIDATION AS PER ATTACHED CARGO MANIFEST '+str(self.hawb)
                for txt in self.medidas_text:
                    texto+='<br/>'+txt

                data = [[Paragraph(str(texto), encoding='utf-8', style=style_texto_7)]]
                table = Table(data=data, colWidths=[5 * cm, ], rowHeights=[1 * cm, ],
                              style=[
                                  ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                                  ('VALIGN', (0, 0), (0, 0), 'TOP'),
                              ]
                              )
                table.wrapOn(c, 0, 0)
                table.drawOn(c, 145 * mm, 142 * mm)
                y -= 50
            c.drawString(52,280,str(bultos))
            c.drawString(82,280,str(pesos))
            c.drawString(340,280,str(fletes))
            if self.modopago == 'Prepaid':
                c.drawString(80,250,str(fletes))
                c.drawString(200,250,str(''))
                montoppd = fletes
                montocol = 0
            else:
                c.drawString(80,250,str(''))
                c.drawString(200,250,str(fletes))
                montoppd = 0
                montocol = fletes
            c.drawString(253,200,str(self.posicion))
            #c.drawString(350,200,str(self.shipper_nom))
            c.drawString(370,145,'OCEANLINK')

            """ otros datos """
            data = [[Paragraph('OCEANLINK AS AGENT<br/>OF DE CARRIER '+str(self.shipper_nom)+
                               '<br/>'+str(datetime.now().strftime('%Y-%m-%d'))+' MONTEVIDEO'+ '     OCEAN LINK LTDA / LLB',
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
            total_oth_ppd=0
            total_oth_col=0
            if self.othppd !=0:
                total_oth_ppd=float(self.othppd)
            if self.othcol !=0:
                total_oth_col=float(self.othcol)
            """ MONTOS """
            c.drawString(80, 230, validar_valor(round(self.valppd,2)))
            c.drawString(200, 230, validar_valor(round(self.valcol,2)))
            c.drawString(80, 200, validar_valor(round(self.taxppd,2)))
            c.drawString(200, 200, validar_valor(round(self.taxcol,2)))
            c.drawString(80, 155, validar_valor(round(self.total_precio_p,2)))
            c.drawString(200, 155, validar_valor(round(self.total_precio_c,2)))
            """ OTHER """

            data = [[Paragraph(self.otros_gastos,encoding='utf-8',style=style_texto_7)]]
            table = Table(data=data, colWidths=[10 * cm, ], rowHeights=[1 * cm, ],
                          style=[
                              ('BOX', (0, 0), (-1, -1), 0.5, colors.transparent),
                              ('VALIGN', (0, 0), (0, 0), 'TOP'),
                          ]
                          )
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 90 * mm, 82 * mm)
            """ TOTALES """

            fletes = Decimal(fletes)
            if self.total_precio_p ==0 and self.total_precio_c==0:
                self.total_precio_p= fletes if self.modopago=='Collect' else 0
                self.total_precio_c= fletes if self.modopago=='Prepaid' else 0

            if self.total_precio_p < fletes:
                self.total_precio_p+= fletes
            elif self.total_precio_c < fletes:
                self.total_precio_c+= fletes

            c.drawString(80, 107, validar_valor(round(self.total_precio_p,2)))
            c.drawString(200, 107, validar_valor(round(self.total_precio_c,2)))

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

def validar_valor(valor):
    return str(valor) if valor != 0 else ' '


