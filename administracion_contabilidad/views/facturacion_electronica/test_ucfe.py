import base64
import os
import uuid
from datetime import datetime

import urllib3
from zeep.helpers import serialize_object

from administracion_contabilidad.views.facturacion_electronica.ucfe_client import UCFEClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_obtener_pdf(ucfe):
    try:
        # Datos de prueba
        rut_emisor = "213971080016"
        tipo_cfe = 111
        serie = "A"
        numero = 37

        resp = ucfe.soap_query.service.ObtenerPdf(
            rut=rut_emisor,
            tipoCfe=tipo_cfe,
            serieCfe=serie,
            numeroCfe=numero
        )

        if not resp:
            return

        # Caso 1: el servicio devuelve PDF binario directo
        if isinstance(resp, (bytes, bytearray)) and resp.startswith(b"%PDF"):
            pdf_bytes = resp

        # Caso 2: el servicio devuelve base64 en string
        else:
            import base64
            pdf_bytes = base64.b64decode(resp)

        # Guardar PDF en archivo
        ruta = f"TEST_CFE_{tipo_cfe}_{serie}{numero}.pdf"
        with open(ruta, "wb") as f:
            f.write(pdf_bytes)


    except Exception as e:
        print("❌ Error durante la prueba:", e)


def main():
    # === Inicializar cliente ===
    ucfe = UCFEClient(
        base_url="https://test.ucfe.com.uy/Inbox115/CfeService.svc",
        usuario="213971080016",
        rut="213971080016",
        clave="9rtcl5NzMXlRHKU2PGtPUw==",
        cod_comercio="OCEANL-394",
        cod_terminal="FC-394",
        wsdl_inbox="https://test.ucfe.com.uy/Inbox115/CfeService.svc?singleWsdl",
        wsdl_query="https://test.ucfe.com.uy/Query116/WebServicesFE.svc?singleWsdl"
    )
    uuid_val = str(uuid.uuid4())
    next_num = 38

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    rut_emisor = "213971080016"
    tipo_cfe = 111
    serie = "A"

    print("==== Paso 1: Verificar si el folio está libre ====")
    if ucfe.is_folio_free(tipo_cfe, serie, next_num, rut_emisor):
        print("✅ El número está LIBRE para usarse.")
    else:
        print("❌ El número ya fue emitido.")

    print("\n==== SOAP ENDPOINTS (Inbox) ====")

    print("\n==== Paso 1: Generar XML ====")
    xml = ucfe.xml_efactura(next_num).strip()
    # xml = ucfe.xml_efactura(next_num).strip()
    print("==== XML generado ====")
    print(xml)

    print("\n==== Paso 2: Solicitar Firma ====")
    try:
        resp_firma = ucfe.soap_solicitar_firma(
            xml,
            uuid_str=uuid_val,
            rut_emisor=rut_emisor,
            tipo_cfe=tipo_cfe,
            serie=serie,
            numero=next_num
        )
        print("Respuesta Firma:", resp_firma)

        data_firma = serialize_object(resp_firma)

        if not data_firma or not data_firma.get("Resp") or not data_firma["Resp"].get("XmlCfeFirmado"):
            print("⚠️ No se pudo firmar el CFE, revisar respuesta.")
            return

        xml_firmado = data_firma["Resp"]["XmlCfeFirmado"]
        certificado = data_firma["Resp"].get("Certificado")
        datos_qr = data_firma["Resp"].get("DatosQr")
        id_req = data_firma["Resp"].get("IdReq")

    except Exception as e:
        print("❌ Error en solicitar firma:", e)
        return
    try:
        # Guardar firmado en archivo
        ruta = os.path.abspath("cfe_firmado.xml")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(xml_firmado)
        print("XML firmado guardado en:", ruta)
    except Exception as e:
        print("❌ Error guardando XML firmado:", e)
        return


    print("\n==== Paso 2: Verificar estado luego de enviar ====")
    try:
        resp_post = ucfe.soap_obtener_cfe_emitido(
            rut=rut_emisor,
            tipo_cfe=tipo_cfe,
            serie=serie,
            numero=next_num
        )
        data_post = serialize_object(resp_post)
        print("Respuesta post-envío:", data_post)

        if data_post:
            print(f"✅ El CFE {tipo_cfe}-{serie}-{next_num} quedó registrado en UCFE.")
        else:
            print(f"⚠️ No se encontró el CFE {tipo_cfe}-{serie}-{next_num}.")
    except Exception as e:
        print(f"❌ Error consultando estado post-envío: {e}")

    test_obtener_pdf(ucfe)






