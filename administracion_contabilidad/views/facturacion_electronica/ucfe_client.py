import base64
import logging
import re
from datetime import date, datetime
from typing import Dict, Any, Optional

import requests
import json

from django.conf import settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.helpers import serialize_object
from zeep.transports import Transport
from zeep.wsse import UsernameToken
from datetime import datetime
import uuid
from jinja2 import Environment, FileSystemLoader
from datetime import date

from cargosystem.settings import RUTA_PROYECTO, BASE_DIR

logging.basicConfig(
    level=logging.INFO,                      # Nivel de log: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato de salida
    handlers=[
        logging.StreamHandler(),             # Muestra en consola
        logging.FileHandler(str(BASE_DIR) + "/logs/facturacion.log", mode="a", encoding="utf-8")  # Guarda en archivo
    ]
)


class UCFEClient:
    """
    Cliente unificado para UCFE (REST + SOAP).
    - REST: envío de CFE, firma, eco test.
    - SOAP: consultas adicionales (estado, PDF, conciliaciones).
    """

    def __init__(self, base_url: str, usuario: str,rut:str, clave: str,
                 cod_comercio: str, cod_terminal: str,
                 wsdl_inbox: str = None, wsdl_query: str = None):
        self.base_url = base_url.rstrip("/")
        self.auth = (usuario, clave)
        self.cod_comercio = cod_comercio
        self.cod_terminal = cod_terminal
        self.rut = rut

        # Configuración SOAP
        self.soap_inbox = None
        self.soap_query = None
        if wsdl_inbox:
            session = Session()
            # session.auth = HTTPBasicAuth(usuario, clave)
            session.verify = False  # certificado UCFE es autofirmado
            transport = Transport(session=session, timeout=30)
            self.soap_inbox = Client(
                wsdl_inbox,
                transport=transport,
                wsse=UsernameToken(usuario, clave)
            )


        if wsdl_query:
            session = Session()
            # session.auth = HTTPBasicAuth(usuario, clave)
            session.verify = False
            transport = Transport(session=session, timeout=30)
            # self.soap_query = Client(wsdl_query, transport=transport)
            self.soap_query = Client(
                wsdl_query,
                transport=transport,
                wsse=UsernameToken(usuario, clave)
            )


    def soap_eco_test(self):
        try:
            if not self.soap_inbox:
                raise RuntimeError("WSDL de Inbox no configurado")

            now = datetime.now()
            fecha_req = now.strftime("%Y%m%d")  # ej. 20250908
            hora_req = now.strftime("%H%M%S")  # ej. 125959
            request_date = now.strftime("%Y-%m-%dT%H:%M:%S")

            req = {
                "Req": {
                    "CodComercio": self.cod_comercio,
                    "CodTerminal": self.cod_terminal,
                    "TipoMensaje": 820,
                    "FechaReq": fecha_req,
                    "HoraReq": hora_req,
                },
                "RequestDate": request_date,
                "Tout": 30000,
                "CodComercio": self.cod_comercio,
                "CodTerminal": self.cod_terminal,
            }

            return self.soap_inbox.service.Invoke(req)

        except Exception as e:
            print("SOAP ECO ERROR:", e)
            return None

    def _extract_tipo_cfe(self, cfe_xml: str) -> str:
        """Extrae TipoCFE desde el XML con regex simple."""
        m = re.search(r"<TipoCFE>(\d+)</TipoCFE>", cfe_xml)
        return m.group(1) if m else None

    def _extract_serie(self, cfe_xml: str) -> str:
        """Extrae Serie desde el XML (opcional)."""
        m = re.search(r"<Serie>([A-Z])</Serie>", cfe_xml)
        return m.group(1) if m else "A"

    def _extract_numero(self, cfe_xml: str) -> str:
        """Extrae Nro desde el XML (opcional)."""
        m = re.search(r"<Nro>(\d+)</Nro>", cfe_xml)
        return m.group(1) if m else "1"

        # -------------------------------
        #  Solicitar Firma
        # -------------------------------

    def soap_solicitar_firma(self, cfe_xml: str, uuid_str: str = "TEST-UUID-001",
                             rut_emisor: str = "213971080016",
                             serie: str = None, numero: str = None,
                             tipo_cfe: str = None):

        if not self.soap_inbox:
            raise RuntimeError("WSDL de Inbox no configurado")

        now = datetime.now()
        id_req = f"REQ{now.strftime('%Y%m%d%H%M%S')}"

        # Si no se pasa explícito, lo saco del XML
        tipo_cfe = tipo_cfe or self._extract_tipo_cfe(cfe_xml)
        serie = serie or self._extract_serie(cfe_xml)
        numero = numero or self._extract_numero(cfe_xml)

        # Tipos desde el WSDL
        RequerimientoParaUcfe = self.soap_inbox.get_type("ns0:RequerimientoParaUcfe")
        ReqBody = self.soap_inbox.get_type("ns0:ReqBody")

        req_ucfe = RequerimientoParaUcfe(
            CodComercio=self.cod_comercio,
            CodTerminal=self.cod_terminal,
            TipoMensaje=310,  # Solicitar firma
            Uuid=uuid_str,
            RutEmisor=rut_emisor,
            Serie=serie,
            TipoCfe=tipo_cfe,
            NumeroCfe=numero,
            IdReq=id_req,
            FechaReq=now.strftime("%Y%m%d"),
            HoraReq=now.strftime("%H%M%S"),
            CfeXmlOTexto=cfe_xml,
        )

        req_body = ReqBody(
            Req=req_ucfe,
            RequestDate=now.isoformat(),
            Tout=30000,
            CodComercio=self.cod_comercio,
            CodTerminal=self.cod_terminal
        )

        try:
            return self.soap_inbox.service.Invoke(req=req_body)
        except Exception as e:
            print("SOAP Solicitar Firma ERROR:", e)
            logging.info("SOAP Solicitar Firma ERROR:", e)
            return None

        # -------------------------------
        #  Enviar CFE Firmado
        # -------------------------------


    def soap_consultar_estado_emitido(self, tipo_cfe: int, serie: str, numero: int,
                                      rut_emisor: str, rut_consultante: str = None):
        """
        Consulta el estado de un CFE emitido usando ObtenerEstadoCfeRecibido.

        :param tipo_cfe: Código del CFE (ej. 111 = eFactura)
        :param serie: Serie del CFE (ej. "A")
        :param numero: Número del CFE
        :param rut_emisor: RUT del emisor del CFE
        :param rut_consultante: RUT que hace la consulta (si None, se usa el mismo emisor)
        :return: dict con la respuesta de UCFE
        """
        if not self.soap_query:
            raise RuntimeError("WSDL de Query no configurado")

        rut_consultante = rut_consultante or rut_emisor

        try:
            resp = self.soap_query.service.ObtenerEstadoCfeRecibido(
                rut=rut_consultante,
                rutRecibido=rut_emisor,
                tipoCfe=tipo_cfe,
                serieCfe=serie,
                numeroCfe=numero
            )
            return serialize_object(resp)
        except Exception as e:
            print("SOAP Consulta ESTADO ERROR:", e)
            return None

    # def soap_obtener_pdf(self, tipo_cfe: int, serie: str, numero: int,
    #                      rut_emisor: str = "213971080016"):
    #     if not self.soap_query:
    #         raise RuntimeError("WSDL de Query no configurado")
    #     return self.soap_query.service.ObtenerPdf(
    #         rut=rut_emisor,
    #         tipoCfe=tipo_cfe,
    #         serieCfe=serie,
    #         numeroCfe=numero,
    #     )


    def soap_obtener_cfe_emitido(self, rut: str, tipo_cfe: int, serie: str, numero: int):
        """
        Consulta un CFE emitido por el emisor (si existe y en qué estado está).

        :param rut: RUT emisor
        :param tipo_cfe: Tipo de CFE (ej: 111 factura, 101 ticket, etc.)
        :param serie: Serie del comprobante (ej: "A")
        :param numero: Número de comprobante
        :return: Respuesta UCFE serializada o None en caso de error
        """
        if not self.soap_query:
            raise RuntimeError("WSDL de Query no configurado")

        try:
            resp = self.soap_query.service.ObtenerCfeEmitido(
                rut=rut,
                tipoCfe=tipo_cfe,
                serieCfe=serie,
                numeroCfe=numero
            )
            return resp
        except Exception as e:
            print(f"❌ SOAP ObtenerCfeEmitido ERROR: {e}")
            return None

    def is_folio_free(self, tipo_cfe: int, serie: str, numero: int, rut_emisor: str = "213971080016") -> bool:
        """Consulta si un folio está libre en UCFE antes de usarlo."""
        try:
            resp = self.soap_query.service.ObtenerCfeEmitido(
                rut=rut_emisor,
                tipoCfe=tipo_cfe,
                serieCfe=serie,
                numeroCfe=numero
            )
            print("Respuesta UCFE:", resp)

            # Caso 1: UCFE devuelve None → libre
            if not resp:
                return True

            # Caso 2: UCFE devuelve objeto pero vacío
            if isinstance(resp, dict) and not resp:
                return True

            # Caso 3: UCFE devuelve algo con Id o Numero → ya está usado
            if isinstance(resp, dict) and resp.get("Numero"):
                return False

            # Si llega acá, mejor lo tratamos como ocupado
            return False

        except Exception as e:
            print("❌ SOAP ObtenerCfeEmitido ERROR:", e)
            # En caso de error interno de UCFE, asumimos que está libre
            # pero conviene loguearlo y revisarlo.
            return True

    # def obtener_pdf_emitido(ucfe, rut_emisor, tipo_cfe, serie, numero):
    #     try:
    #         resp = ucfe.soap_query.service.ObtenerPdf(
    #             rut=rut_emisor,
    #             tipoCfe=tipo_cfe,
    #             serieCfe=serie,
    #             numeroCfe=numero
    #         )
    #         print("Respuesta PDF:", resp)
    #
    #         if not resp or not getattr(resp, "PdfCfe", None):
    #             print("⚠️ No se obtuvo PDF")
    #             return None
    #
    #         pdf_b64 = resp.PdfCfe
    #         pdf_bytes = base64.b64decode(pdf_b64)
    #
    #         ruta = f"CFE_{tipo_cfe}_{serie}{numero}.pdf"
    #         with open(ruta, "wb") as f:
    #             f.write(pdf_bytes)
    #
    #         print(f"✅ PDF guardado en {ruta}")
    #         logging.info(f"PDF guardado en {ruta}")
    #         return ruta
    #
    #     except Exception as e:
    #         print("❌ Error obteniendo PDF:", e)
    #         return None

    def render_xml(self,data: dict, items: list[dict], referencias: list[dict] = None) -> str:
        """
        Renderiza un XML CFE genérico usando plantillas Jinja2.

        Parámetros:
            data (dict): datos generales (incluye al menos 'tipo_cfe', 'serie', 'numero', 'fecha_emision', etc.)
            items (list): lista de ítems (detalle del comprobante)
            referencias (list, opcional): referencias a otros comprobantes (para notas)

        Retorna:
            str: XML generado
        """
        env = Environment(loader=FileSystemLoader(RUTA_PROYECTO + "/media/plantillas_xml"))
        # Mapear tipo CFE a la plantilla correspondiente
        plantilla_map = {
            "101": "eticket.xml",
            "102": "nc_eticket.xml",
            "103": "xml_nd_eticket.xml",
            "111": "efactura.xml",
            "112": "nc_efactura.xml",
            "113": "xml_nd_efactura.xml",
            "121": "efactura_exportacion.xml",
            "122": "nc_efactura_exportacion.xml",
            "123": "xml_nd_efactura_exportacion.xml",
            "124": "remito_exportacion.xml",
            "151": "eboleta.xml",
            "181": "remito.xml",
            "182": "resguardo.xml",
        }

        tipo_cfe = str(data.get("tipo_cfe"))
        plantilla = plantilla_map.get(tipo_cfe)

        if not plantilla:
            raise ValueError(f"No existe plantilla definida para TipoCFE {tipo_cfe}")

        template = env.get_template(plantilla)

        # Renderizar
        return template.render(
            **data,
            items=items,
            referencias=referencias or []
        ).strip()

    # def test_obtener_pdf(self, rut_emisor, tipo_cfe, serie, numero):
    #     try:
    #         # Datos de prueba
    #         rut_emisor = "213971080016"
    #         tipo_cfe = 111
    #         serie = "A"
    #         numero = 37
    #
    #         resp = self.soap_query.service.ObtenerPdf(
    #             rut=rut_emisor,
    #             tipoCfe=tipo_cfe,
    #             serieCfe=serie,
    #             numeroCfe=numero
    #         )
    #
    #         if not resp:
    #             return
    #
    #         # Caso 1: el servicio devuelve PDF binario directo
    #         if isinstance(resp, (bytes, bytearray)) and resp.startswith(b"%PDF"):
    #             pdf_bytes = resp
    #
    #         # Caso 2: el servicio devuelve base64 en string
    #         else:
    #             import base64
    #             pdf_bytes = base64.b64decode(resp)
    #
    #         # Guardar PDF en archivo
    #         ruta = f"TEST_CFE_{tipo_cfe}_{serie}{numero}.pdf"
    #         with open(ruta, "wb") as f:
    #             f.write(pdf_bytes)
    #
    #
    #     except Exception as e:
    #         print("❌ Error durante la prueba:", e)

    # def obtener_pdf(self, rut_emisor, tipo_cfe, serie, numero):
    #     """
    #     Obtiene el PDF desde UCFE y devuelve los bytes listos para descarga.
    #     """
    #     try:
    #         resp = self.soap_query.service.ObtenerPdf(
    #             rut=rut_emisor,
    #             tipoCfe=tipo_cfe,
    #             serieCfe=serie,
    #             numeroCfe=numero
    #         )
    #
    #         if not resp:
    #             return None
    #
    #         # Caso 1: UCFE devuelve binario directo
    #         if isinstance(resp, (bytes, bytearray)) and resp.startswith(b"%PDF"):
    #             pdf_bytes = resp
    #         # Caso 2: UCFE devuelve base64 (string)
    #         else:
    #             pdf_bytes = base64.b64decode(resp)
    #         logging.info(f"PDF obtenido correctamente: {rut_emisor}-{tipo_cfe}-{serie}-{numero}")
    #         return pdf_bytes
    #
    #     except Exception as e:
    #         print("❌ Error en obtener_pdf:", e)
    #         return None

    #PARA PRUEBAS#

    def xml_eticket(self,numero: int) -> str:
        """Genera XML de e-Ticket según ejemplo del manual UCFE."""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
      <eTck>
        <Encabezado>
          <IdDoc>
            <TipoCFE>101</TipoCFE>
            <Serie>A</Serie>
            <Nro>{numero}</Nro>
            <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
            <FmaPago>1</FmaPago>
          </IdDoc>
          <Emisor>
            <RUCEmisor>213971080016</RUCEmisor>
            <RznSoc>Tu Empresa SA</RznSoc>
            <CdgDGISucur>1</CdgDGISucur>
            <DomFiscal>Av. Siempre Viva 123</DomFiscal>
            <Ciudad>Montevideo</Ciudad>
            <Departamento>Montevideo</Departamento>
          </Emisor>
          <Totales>
            <TpoMoneda>UYU</TpoMoneda>
            <MntNetoIvaTasaMin>50</MntNetoIvaTasaMin>
            <MntNetoIVATasaBasica>100</MntNetoIVATasaBasica>
            <IVATasaMin>10.000</IVATasaMin>
            <IVATasaBasica>22.000</IVATasaBasica>
            <MntIVATasaMin>5</MntIVATasaMin>
            <MntIVATasaBasica>22</MntIVATasaBasica>
            <MntTotal>177</MntTotal>
            <CantLinDet>2</CantLinDet>
            <MntPagar>177</MntPagar>
          </Totales>
        </Encabezado>
        <Detalle>
          <Item>
            <NroLinDet>1</NroLinDet>
            <IndFact>3</IndFact>
            <NomItem>Prueba tasa básica</NomItem>
            <Cantidad>1</Cantidad>
            <UniMed>UND1</UniMed>
            <PrecioUnitario>100</PrecioUnitario>
            <MontoItem>100</MontoItem>
          </Item>
          <Item>
            <NroLinDet>2</NroLinDet>
            <IndFact>2</IndFact>
            <NomItem>Prueba tasa mínima</NomItem>
            <Cantidad>1</Cantidad>
            <UniMed>UND2</UniMed>
            <PrecioUnitario>50</PrecioUnitario>
            <MontoItem>50</MontoItem>
          </Item>
        </Detalle>
      </eTck>
    </CFE>"""
        return xml.strip()

    def xml_eticket_con_receptor(self, num: int) -> str:
        """Genera XML de e-Ticket (Tipo 101) con datos del receptor (monto > 10.000 UI)."""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
      <eTck>
        <Encabezado>
          <IdDoc>
            <TipoCFE>101</TipoCFE>
            <Serie>A</Serie>
            <Nro>{num}</Nro>
            <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
            <FmaPago>1</FmaPago>
          </IdDoc>
          <Emisor>
            <RUCEmisor>213971080016</RUCEmisor>
            <RznSoc>Tu Empresa SA</RznSoc>
            <CdgDGISucur>1</CdgDGISucur>
            <DomFiscal>Av. Siempre Viva 123</DomFiscal>
            <Ciudad>Montevideo</Ciudad>
            <Departamento>Montevideo</Departamento>
          </Emisor>
          <Receptor>
            <TipoDocRecep>2</TipoDocRecep> <!-- 2 = RUC -->
            <CodPaisRecep>UY</CodPaisRecep>
            <DocRecep>217994080015</DocRecep>
            <RznSocRecep>Cliente Ejemplo SA</RznSocRecep>
            <DirRecep>Av. Principal 456</DirRecep>
            <CiudadRecep>Montevideo</CiudadRecep>
            <PaisRecep>Uruguay</PaisRecep>
          </Receptor>
          <Totales>
            <TpoMoneda>UYU</TpoMoneda>
            <MntNetoIVATasaBasica>50000</MntNetoIVATasaBasica>
            <IVATasaBasica>22.000</IVATasaBasica>
            <MntIVATasaBasica>11000</MntIVATasaBasica>
            <MntTotal>61000</MntTotal>
            <CantLinDet>1</CantLinDet>
            <MntPagar>61000</MntPagar>
          </Totales>
        </Encabezado>
        <Detalle>
          <Item>
            <NroLinDet>1</NroLinDet>
            <IndFact>3</IndFact> <!-- Gravado básico -->
            <NomItem>Servicio profesional</NomItem>
            <Cantidad>1</Cantidad>
            <UniMed>UNI</UniMed>
            <PrecioUnitario>50000</PrecioUnitario>
            <MontoItem>50000</MontoItem>
          </Item>
        </Detalle>
      </eTck>
    </CFE>"""
        return xml.strip()

    def xml_nc_eticket(self, num: int) -> str:
        """Genera XML de Nota de Crédito e-Ticket (Tipo 102) sin datos de receptor."""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
      <eTck>
        <Encabezado>
          <IdDoc>
            <TipoCFE>102</TipoCFE>
            <Serie>A</Serie>
            <Nro>{num}</Nro>
            <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
            <MntBruto>1</MntBruto>
            <FmaPago>1</FmaPago>
          </IdDoc>
          <Emisor>
            <RUCEmisor>213971080016</RUCEmisor>
            <RznSoc>Tu Empresa SA</RznSoc>
            <CdgDGISucur>1</CdgDGISucur>
            <DomFiscal>Av. Siempre Viva 123</DomFiscal>
            <Ciudad>Montevideo</Ciudad>
            <Departamento>Montevideo</Departamento>
          </Emisor>
          <Totales>
            <TpoMoneda>UYU</TpoMoneda>
            <MntNetoIVATasaBasica>100</MntNetoIVATasaBasica>
            <IVATasaMin>10.000</IVATasaMin>
            <IVATasaBasica>22.000</IVATasaBasica>
            <MntIVATasaBasica>22</MntIVATasaBasica>
            <MntTotal>122</MntTotal>
            <CantLinDet>1</CantLinDet>
            <MntPagar>122</MntPagar>
          </Totales>
        </Encabezado>
        <Detalle>
          <Item>
            <NroLinDet>1</NroLinDet>
            <IndFact>3</IndFact>
            <NomItem>Desarrollo de soporte lógico</NomItem>
            <Cantidad>1</Cantidad>
            <UniMed>N/A</UniMed>
            <PrecioUnitario>122</PrecioUnitario>
            <MontoItem>122</MontoItem>
          </Item>
        </Detalle>
        <Referencia>
          <Referencia>
            <NroLinRef>1</NroLinRef>
            <TpoDocRef>101</TpoDocRef>
            <Serie>A</Serie>
            <NroCFERef>20</NroCFERef>
            <FechaCFEref>{date.today().strftime("%Y-%m-%d")}</FechaCFEref>
          </Referencia>
        </Referencia>
      </eTck>
    </CFE>"""
        return xml.strip()

    def xml_nc_eticket_con_receptor(self, num: int) -> str:
        """Genera XML de Nota de Crédito e-Ticket (Tipo 102) con datos de receptor."""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
      <eTck>
        <Encabezado>
          <IdDoc>
            <TipoCFE>102</TipoCFE>
            <Serie>A</Serie>
            <Nro>{num}</Nro>
            <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
            <MntBruto>1</MntBruto>
            <FmaPago>1</FmaPago>
          </IdDoc>
          <Emisor>
            <RUCEmisor>213971080016</RUCEmisor>
            <RznSoc>Tu Empresa SA</RznSoc>
            <CdgDGISucur>1</CdgDGISucur>
            <DomFiscal>Av. Siempre Viva 123</DomFiscal>
            <Ciudad>Montevideo</Ciudad>
            <Departamento>Montevideo</Departamento>
          </Emisor>
          <Receptor>
            <TipoDocRecep>2</TipoDocRecep>
            <CodPaisRecep>UY</CodPaisRecep>
            <DocRecep>217994080015</DocRecep>
            <RznSocRecep>Cliente Ejemplo SA</RznSocRecep>
            <DirRecep>Av. Principal 456</DirRecep>
            <CiudadRecep>Montevideo</CiudadRecep>
            <PaisRecep>Uruguay</PaisRecep>
          </Receptor>
          <Totales>
            <TpoMoneda>UYU</TpoMoneda>
            <MntNetoIVATasaBasica>20000</MntNetoIVATasaBasica>
            <IVATasaBasica>22.000</IVATasaBasica>
            <MntIVATasaBasica>4400</MntIVATasaBasica>
            <MntTotal>24400</MntTotal>
            <CantLinDet>1</CantLinDet>
            <MntPagar>24400</MntPagar>
          </Totales>
        </Encabezado>
        <Detalle>
          <Item>
            <NroLinDet>1</NroLinDet>
            <IndFact>3</IndFact>
            <NomItem>Devolución por servicios</NomItem>
            <Cantidad>1</Cantidad>
            <UniMed>UNI</UniMed>
            <PrecioUnitario>20000</PrecioUnitario>
            <MontoItem>20000</MontoItem>
          </Item>
        </Detalle>
        <Referencia>
          <Referencia>
            <NroLinRef>1</NroLinRef>
            <TpoDocRef>101</TpoDocRef>
            <Serie>A</Serie>
            <NroCFERef>21</NroCFERef>
            <FechaCFEref>{date.today().strftime("%Y-%m-%d")}</FechaCFEref>
          </Referencia>
        </Referencia>
      </eTck>
    </CFE>"""
        return xml.strip()

    def xml_efactura(self,num) -> str:
        """Genera XML de e-Factura siguiendo el ejemplo 6.2.2.1 del manual,
        adaptado a los RUTs y agregando Serie y Nro obligatorios.
        """
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
      <eFact>
        <Encabezado>
          <IdDoc>
            <TipoCFE>111</TipoCFE>
            <Serie>A</Serie>
            <Nro>{num}</Nro>
            <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
            <FmaPago>1</FmaPago>
          </IdDoc>
          <Emisor>
            <RUCEmisor>213971080016</RUCEmisor>
            <RznSoc>Tu Empresa SA</RznSoc>
            <CdgDGISucur>1</CdgDGISucur>
            <DomFiscal>Av. Siempre Viva 123</DomFiscal>
            <Ciudad>Montevideo</Ciudad>
            <Departamento>Montevideo</Departamento>
          </Emisor>
          <Receptor>
            <TipoDocRecep>2</TipoDocRecep>
            <CodPaisRecep>UY</CodPaisRecep>
            <DocRecep>217994080015</DocRecep>
            <RznSocRecep>Cliente Demo</RznSocRecep>
            <DirRecep>Av. Principal 456</DirRecep>
            <CiudadRecep>Montevideo</CiudadRecep>
            <PaisRecep>Uruguay</PaisRecep>
          </Receptor>
          <Totales>
            <TpoMoneda>UYU</TpoMoneda>
            <MntNetoIVATasaBasica>99</MntNetoIVATasaBasica>
            <IVATasaMin>10.000</IVATasaMin>
            <IVATasaBasica>22.000</IVATasaBasica>
            <MntIVATasaBasica>21.78</MntIVATasaBasica>
            <MntTotal>120.78</MntTotal>
            <CantLinDet>2</CantLinDet>
            <MontoNF>0.22</MontoNF>
            <MntPagar>121</MntPagar>
          </Totales>
        </Encabezado>
        <Detalle>
          <Item>
            <NroLinDet>1</NroLinDet>
            <IndFact>3</IndFact>
            <NomItem>Servicios de desarrollo</NomItem>
            <Cantidad>1</Cantidad>
            <UniMed>N/A</UniMed>
            <PrecioUnitario>99</PrecioUnitario>
            <MontoItem>99</MontoItem>
          </Item>
          <Item>
            <NroLinDet>2</NroLinDet>
            <IndFact>6</IndFact>
            <NomItem>Redondeo</NomItem>
            <DscItem>Redondeo Sistema</DscItem>
            <Cantidad>1</Cantidad>
            <UniMed>N/A</UniMed>
            <PrecioUnitario>0.22</PrecioUnitario>
            <MontoItem>0.22</MontoItem>
          </Item>
        </Detalle>
      </eFact>
    </CFE>"""
        return xml.strip()

    def xml_nc_efactura(self, num: int) -> str:
        """Genera XML de Nota de Crédito de e-Factura (TipoCFE 112) siguiendo misma estructura que e-Factura."""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
          <eFact>
            <Encabezado>
              <IdDoc>
                <TipoCFE>112</TipoCFE>
                <Serie>A</Serie>
                <Nro>{num}</Nro>
                <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
                <FmaPago>1</FmaPago>
              </IdDoc>
              <Emisor>
                <RUCEmisor>213971080016</RUCEmisor>
                <RznSoc>Tu Empresa SA</RznSoc>
                <CdgDGISucur>1</CdgDGISucur>
                <DomFiscal>Av. Siempre Viva 123</DomFiscal>
                <Ciudad>Montevideo</Ciudad>
                <Departamento>Montevideo</Departamento>
              </Emisor>
              <Receptor>
                <TipoDocRecep>2</TipoDocRecep>
                <CodPaisRecep>UY</CodPaisRecep>
                <DocRecep>215404940014</DocRecep>
                <RznSocRecep>Cliente S.A.</RznSocRecep>
                <DirRecep>Bv. España 2579</DirRecep>
                <CiudadRecep>Montevideo</CiudadRecep>
                <PaisRecep>Uruguay</PaisRecep>
              </Receptor>
              <Totales>
                <TpoMoneda>UYU</TpoMoneda>
                <MntNetoIVATasaBasica>99</MntNetoIVATasaBasica>
                <IVATasaMin>10.000</IVATasaMin>
                <IVATasaBasica>22.000</IVATasaBasica>
                <MntIVATasaBasica>21.78</MntIVATasaBasica>
                <MntTotal>120.78</MntTotal>
                <CantLinDet>2</CantLinDet>
                <MontoNF>0.22</MontoNF>
                <MntPagar>121</MntPagar>
              </Totales>
            </Encabezado>
            <Detalle>
              <Item>
                <NroLinDet>1</NroLinDet>
                <IndFact>3</IndFact>
                <NomItem>Corrección de servicio facturado</NomItem>
                <Cantidad>1</Cantidad>
                <UniMed>N/A</UniMed>
                <PrecioUnitario>99</PrecioUnitario>
                <MontoItem>99</MontoItem>
              </Item>
              <Item>
                <NroLinDet>2</NroLinDet>
                <IndFact>6</IndFact>
                <NomItem>Redondeo</NomItem>
                <DscItem>Redondeo Sistema</DscItem>
                <Cantidad>1</Cantidad>
                <UniMed>N/A</UniMed>
                <PrecioUnitario>0.22</PrecioUnitario>
                <MontoItem>0.22</MontoItem>
              </Item>
            </Detalle>
            <Referencia>
              <Referencia>
                <NroLinRef>1</NroLinRef>
                <TpoDocRef>111</TpoDocRef>
                <Serie>A</Serie>
                <NroCFERef>27</NroCFERef>
                <FechaCFEref>{date.today().strftime("%Y-%m-%d")}</FechaCFEref>
              </Referencia>
            </Referencia>
          </eFact>
        </CFE>"""
        return xml.strip()

    def xml_efactura_exportacion(self, num: int) -> str:
        """Genera XML de e-Factura de Exportación (Tipo 121)."""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
      <eFact_Exp>
        <Encabezado>
          <IdDoc>
            <TipoCFE>121</TipoCFE>
            <Serie>A</Serie>
            <Nro>{num}</Nro>
            <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
            <FmaPago>1</FmaPago>
            <ClauVenta>N/A</ClauVenta>
            <ModVenta>1</ModVenta>
            <ViaTransp>1</ViaTransp>
          </IdDoc>
          <Emisor>
            <RUCEmisor>213971080016</RUCEmisor>
            <RznSoc>Tu Empresa SA</RznSoc>
            <CdgDGISucur>1</CdgDGISucur>
            <DomFiscal>Av. Siempre Viva 123</DomFiscal>
            <Ciudad>Montevideo</Ciudad>
            <Departamento>Montevideo</Departamento>
          </Emisor>
          <Receptor>
            <TipoDocRecep>4</TipoDocRecep>
            <CodPaisRecep>CN</CodPaisRecep>
            <DocRecepExt>1234567890123456</DocRecepExt>
            <RznSocRecep>Cliente Exportación</RznSocRecep>
            <DirRecep>Tayuan Office Building 1-1-2 (100600)</DirRecep>
            <CiudadRecep>Beijing</CiudadRecep>
            <DeptoRecep>Beijing</DeptoRecep>
            <PaisRecep>China</PaisRecep>
          </Receptor>
          <Totales>
            <TpoMoneda>UYU</TpoMoneda>
            <MntExpoyAsim>60000</MntExpoyAsim>
            <MntTotal>60000</MntTotal>
            <CantLinDet>1</CantLinDet>
            <MntPagar>60000</MntPagar>
          </Totales>
        </Encabezado>
        <Detalle>
          <Item>
            <NroLinDet>1</NroLinDet>
            <IndFact>10</IndFact>
            <NomItem>Artículos de consumo</NomItem>
            <Cantidad>150</Cantidad>
            <UniMed>UNID</UniMed>
            <PrecioUnitario>400</PrecioUnitario>
            <MontoItem>60000</MontoItem>
          </Item>
        </Detalle>
      </eFact_Exp>
    </CFE>"""
        return xml.strip()

    def xml_remito(self, num: int) -> str:
        """Genera XML de Remito electrónico (Tipo 181)."""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
      <eRem>
        <Encabezado>
          <IdDoc>
            <TipoCFE>181</TipoCFE>
            <Serie>A</Serie>
            <Nro>{num}</Nro>
            <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
            <TipoTraslado>1</TipoTraslado>
          </IdDoc>
          <Emisor>
            <RUCEmisor>213971080016</RUCEmisor>
            <RznSoc>Tu Empresa SA</RznSoc>
            <CdgDGISucur>1</CdgDGISucur>
            <DomFiscal>Av. Siempre Viva 123</DomFiscal>
            <Ciudad>Montevideo</Ciudad>
            <Departamento>Montevideo</Departamento>
          </Emisor>
          <Receptor>
            <TipoDocRecep>2</TipoDocRecep>
            <CodPaisRecep>UY</CodPaisRecep>
            <DocRecep>215404940014</DocRecep>
            <RznSocRecep>Cliente Demo</RznSocRecep>
            <DirRecep>Bv. España 2579</DirRecep>
            <CiudadRecep>Montevideo</CiudadRecep>
            <PaisRecep>Uruguay</PaisRecep>
          </Receptor>
          <Totales>
            <CantLinDet>1</CantLinDet>
          </Totales>
        </Encabezado>
        <Detalle>
          <Item>
            <!-- En remitos no se incluyen importes ni IndFact -->
            <NroLinDet>1</NroLinDet>
            <NomItem>Servidor cuántico</NomItem>
            <Cantidad>2</Cantidad>
            <UniMed>UNID</UniMed>
          </Item>
        </Detalle>
      </eRem>
    </CFE>"""
        return xml.strip()

    def xml_remito_correccion(self, num: int) -> str:
        """Genera XML de Remito electrónico de corrección (Tipo 181)."""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
      <eRem>
        <Encabezado>
          <IdDoc>
            <TipoCFE>181</TipoCFE>
            <Serie>A</Serie>
            <Nro>{num}</Nro>
            <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
            <TipoTraslado>1</TipoTraslado>
          </IdDoc>
          <Emisor>
            <RUCEmisor>213971080016</RUCEmisor>
            <RznSoc>Tu Empresa SA</RznSoc>
            <CdgDGISucur>1</CdgDGISucur>
            <DomFiscal>Av. Siempre Viva 123</DomFiscal>
            <Ciudad>Montevideo</Ciudad>
            <Departamento>Montevideo</Departamento>
          </Emisor>
          <Receptor>
            <TipoDocRecep>2</TipoDocRecep>
            <CodPaisRecep>UY</CodPaisRecep>
            <DocRecep>215404940014</DocRecep>
            <RznSocRecep>Cliente Demo</RznSocRecep>
            <DirRecep>Bv. España 2579</DirRecep>
            <CiudadRecep>Montevideo</CiudadRecep>
            <PaisRecep>Uruguay</PaisRecep>
          </Receptor>
          <Totales>
            <CantLinDet>1</CantLinDet>
          </Totales>
        </Encabezado>
        <Detalle>
          <Item>
            <NroLinDet>1</NroLinDet>
            <IndFact>8</IndFact> <!-- Indicador de corrección -->
            <NomItem>Servidor cuántico</NomItem>
            <Cantidad>1</Cantidad>
            <UniMed>UNID</UniMed>
          </Item>
        </Detalle>
        <Referencia>
          <Referencia>
            <NroLinRef>1</NroLinRef>
            <TpoDocRef>181</TpoDocRef>
            <Serie>A</Serie>
            <NroCFERef>29</NroCFERef>
            <RazonRef>Se corrige total trasladado</RazonRef>
            <FechaCFEref>{date.today().strftime("%Y-%m-%d")}</FechaCFEref>
          </Referencia>
        </Referencia>
      </eRem>
    </CFE>"""
        return xml.strip()

    def xml_remito_exportacion(self, num: int) -> str:
        """Genera XML de e-Remito Exportación (TipoCFE 124)."""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
          <eRem_Exp>
            <Encabezado>
              <IdDoc>
                <TipoCFE>124</TipoCFE>
                <Serie>A</Serie>
                <Nro>{num}</Nro>
                <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
                <TipoTraslado>1</TipoTraslado>
                <ModVenta>1</ModVenta>
                <ViaTransp>1</ViaTransp>
              </IdDoc>
              <Emisor>
                <RUCEmisor>213971080016</RUCEmisor>
                <RznSoc>Tu Empresa SA</RznSoc>
                <CdgDGISucur>1</CdgDGISucur>
                <DomFiscal>Av. Siempre Viva 123</DomFiscal>
                <Ciudad>Montevideo</Ciudad>
                <Departamento>Montevideo</Departamento>
              </Emisor>
              <Receptor>
                <RznSocRecep>Cliente Exportación</RznSocRecep>
                <DirRecep>Tayuan Office Building 1-1-2 (100600)</DirRecep>
                <CiudadRecep>Beijing</CiudadRecep>
                <DeptoRecep>Beijing</DeptoRecep>
                <PaisRecep>China</PaisRecep>
              </Receptor>
              <Totales>
                <TpoMoneda>UYU</TpoMoneda>
                <MntExpoyAsim>150000</MntExpoyAsim>
                <MntTotal>150000</MntTotal>
                <CantLinDet>1</CantLinDet>
              </Totales>
            </Encabezado>
            <Detalle>
              <Item>
                <NroLinDet>1</NroLinDet>
                <NomItem>Lana cruda</NomItem>
                <Cantidad>1000</Cantidad>
                <UniMed>TON</UniMed>
                <PrecioUnitario>150</PrecioUnitario>
                <MontoItem>150000</MontoItem>
              </Item>
            </Detalle>
          </eRem_Exp>
        </CFE>"""
        return xml.strip()

    def xml_resguardo(self, num: int) -> str:
        """Genera XML de e-Resguardo (Tipo 182)."""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
      <eResg>
        <Encabezado>
          <IdDoc>
            <TipoCFE>182</TipoCFE>
            <Serie>A</Serie>
            <Nro>{num}</Nro>
            <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
          </IdDoc>
          <Emisor>
            <RUCEmisor>213971080016</RUCEmisor>
            <RznSoc>Tu Empresa SA</RznSoc>
            <CdgDGISucur>1</CdgDGISucur>
            <DomFiscal>Av. Siempre Viva 123</DomFiscal>
            <Ciudad>Montevideo</Ciudad>
            <Departamento>Montevideo</Departamento>
          </Emisor>
          <Receptor>
            <TipoDocRecep>3</TipoDocRecep>
            <CodPaisRecep>UY</CodPaisRecep>
            <DocRecep>13353214</DocRecep>
            <RznSocRecep>Juan Perez</RznSocRecep>
            <PaisRecep>Uruguay</PaisRecep>
          </Receptor>
          <Totales>
            <TpoMoneda>UYU</TpoMoneda>
            <MntTotRetenido>32000</MntTotRetenido>
            <CantLinDet>1</CantLinDet>
            <RetencPercep>
              <CodRet>2183114</CodRet>
              <ValRetPerc>22000</ValRetPerc>
            </RetencPercep>
            <RetencPercep>
              <CodRet>2183121</CodRet>
              <ValRetPerc>10000</ValRetPerc>
            </RetencPercep>
          </Totales>
        </Encabezado>
        <Detalle>
          <Item>
            <NroLinDet>1</NroLinDet>
            <RetencPercep>
              <CodRet>2183114</CodRet>
              <Tasa>22</Tasa>
              <MntSujetoaRet>90000</MntSujetoaRet>
              <ValRetPerc>19800</ValRetPerc>
            </RetencPercep>
            <RetencPercep>
              <CodRet>2183114</CodRet>
              <Tasa>22</Tasa>
              <MntSujetoaRet>10000</MntSujetoaRet>
              <ValRetPerc>2200</ValRetPerc>
            </RetencPercep>
            <RetencPercep>
              <CodRet>2183121</CodRet>
              <Tasa>10</Tasa>
              <MntSujetoaRet>100000</MntSujetoaRet>
              <ValRetPerc>10000</ValRetPerc>
            </RetencPercep>
          </Item>
        </Detalle>
      </eResg>
    </CFE>"""
        return xml.strip()

    def xml_resguardo_correccion(self, num: int) -> str:
        """Genera XML de corrección de e-Resguardo (TipoCFE 182)
        siguiendo el ejemplo del manual UCFE.
        """
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
      <eResg>
        <Encabezado>
          <IdDoc>
            <TipoCFE>182</TipoCFE>
            <Serie>A</Serie>
            <Nro>{num}</Nro>
            <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
          </IdDoc>
          <Emisor>
            <RUCEmisor>213971080016</RUCEmisor>
            <RznSoc>Tu Empresa SA</RznSoc>
            <CdgDGISucur>1</CdgDGISucur>
            <DomFiscal>Av. Siempre Viva 123</DomFiscal>
            <Ciudad>Montevideo</Ciudad>
            <Departamento>Montevideo</Departamento>
          </Emisor>
          <Receptor>
            <TipoDocRecep>3</TipoDocRecep>
            <CodPaisRecep>UY</CodPaisRecep>
            <DocRecep>13353214</DocRecep>
            <RznSocRecep>Juan Perez</RznSocRecep>
            <PaisRecep>Uruguay</PaisRecep>
          </Receptor>
          <Totales>
            <TpoMoneda>UYU</TpoMoneda>
            <MntTotRetenido>-2200</MntTotRetenido>
            <CantLinDet>1</CantLinDet>
            <RetencPercep>
              <CodRet>2183114</CodRet>
              <ValRetPerc>-2200</ValRetPerc>
            </RetencPercep>
          </Totales>
        </Encabezado>
        <Detalle>
          <Item>
            <NroLinDet>1</NroLinDet>
            <IndFact>9</IndFact>
            <RetencPercep>
              <CodRet>2183114</CodRet>
              <Tasa>22</Tasa>
              <MntSujetoaRet>10000</MntSujetoaRet>
              <ValRetPerc>2200</ValRetPerc>
            </RetencPercep>
          </Item>
        </Detalle>
        <Referencia>
          <Referencia>
            <NroLinRef>1</NroLinRef>
            <TpoDocRef>182</TpoDocRef>
            <Serie>A</Serie>
            <NroCFERef>32</NroCFERef>
            <FechaCFEref>{date.today().strftime("%Y-%m-%d")}</FechaCFEref>
          </Referencia>
        </Referencia>
      </eResg>
    </CFE>"""
        return xml.strip()

    def xml_eboleta(self) -> str:
        """Genera XML de e-Boleta (TipoCFE 151) según ejemplo UCFE."""
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <CFE version="1.0" xmlns="http://cfe.dgi.gub.uy">
      <eBoleta>
        <Encabezado>
          <IdDoc>
            <TipoCFE>151</TipoCFE>
            <FchEmis>{date.today().strftime("%Y-%m-%d")}</FchEmis>
            <FmaPago>1</FmaPago>
          </IdDoc>
          <Emisor>
            <RUCEmisor>213971080016</RUCEmisor>
            <RznSoc>Tu Empresa SA</RznSoc>
            <CdgDGISucur>1</CdgDGISucur>
            <DomFiscal>Av. Siempre Viva 123</DomFiscal>
            <Ciudad>Montevideo</Ciudad>
            <Departamento>Montevideo</Departamento>
          </Emisor>
          <Receptor>
            <TipoDocRecep>2</TipoDocRecep>
            <CodPaisRecep>UY</CodPaisRecep>
            <DocRecep>215404940014</DocRecep>
            <RznSocRecep>Uruware S.A.</RznSocRecep>
            <DirRecep>Bv. España 2579</DirRecep>
            <CiudadRecep>Montevideo</CiudadRecep>
            <PaisRecep>Uruguay</PaisRecep>
          </Receptor>
          <Totales>
            <TpoMoneda>UYU</TpoMoneda>
            <MntNoGrv>122</MntNoGrv>
            <MntTotal>122</MntTotal>
            <CantLinDet>1</CantLinDet>
            <MntPagar>122</MntPagar>
          </Totales>
        </Encabezado>
        <Detalle>
          <Item>
            <NroLinDet>1</NroLinDet>
            <IndFact>15</IndFact>
            <NomItem>Servicios de desarrollo</NomItem>
            <Cantidad>1</Cantidad>
            <UniMed>N/A</UniMed>
            <PrecioUnitario>122</PrecioUnitario>
            <MontoItem>122</MontoItem>
          </Item>
        </Detalle>
      </eBoleta>
    </CFE>"""
        return xml.strip()