from seguimientos.views import desconsolidacion_aerea
import requests
import base64


def enviar_xml(xml_str):
    url = 'http://www.importsys.com.uy/ws/wsOcean.exe'  # URL del servicio web

    usuario = 'Oceanlink'
    contrasena = 'ocean99'
    credenciales = f"{usuario}:{contrasena}"
    credenciales_b64 = base64.b64encode(credenciales.encode()).decode()

    headers = {
        'Content-Type': 'text/xml',  # Asegúrate de que el servicio espere este tipo de contenido
        'Authorization': f'Basic {credenciales_b64}'  # Agrega el encabezado de autorización
    }

    print("Enviando XML a la URL:", url)
    print("Headers:", headers)
    print("XML a enviar:")
    print(xml_str)

    try:
        # Realizamos una solicitud POST al webservice enviando el XML en el cuerpo
        response = requests.post(url, data=xml_str, headers=headers)

        # Imprimimos el código de estado y la respuesta completa para ver qué devuelve
        print("Código de estado de la respuesta:", response.status_code)
        print("Respuesta del servidor:")
        print(response.text)

        # Comprobamos el código de estado de la respuesta
        if response.status_code == 200:
            # Retornamos la respuesta si todo fue bien
            return response.text
        else:
            # Si hubo algún error en la solicitud, retornamos el código de estado
            return f"Error {response.status_code}: {response.text}"

    except requests.exceptions.RequestException as e:
        # Si ocurre una excepción durante la solicitud, la capturamos y la mostramos
        print("Error en la solicitud:", str(e))
        return f"Error en la solicitud: {str(e)}"
