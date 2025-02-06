import base64
import json
import os
import socket
import sys
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import simplejson
from django.core import mail
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.http import  HttpResponse

from cargosystem.settings import BASE_DIR
from login.models import CorreoEnviado, Account
from cargosystem import settings
from login.views.correos import is_ajax
from seguimientos.models import Attachhijo, Faxes, Seguimiento


def envio_notificacion_seguimiento(request):
    resultado = {}
    if is_ajax(request):
        try:
            to = request.POST['to'].split(';')
            cc = request.POST['cc'].split(';') if request.POST['cc'] is not None else []
            cco = request.POST['cco'].split(';') if (request.POST['cco'] is not None and request.POST['cco']) else []
            tipo = request.POST['tipo']
            seguimiento = request.POST['seguimiento']
            aux = Seguimiento.objects.get(numero=seguimiento)
            num_seg = str(aux.numero) + ' ' + str(aux.modo)
            adjuntos = simplejson.loads(request.POST['archivos_adjuntos'])
            subject = request.POST['subject']
            message = request.POST['message']
            user = Account.objects.filter(user__id=request.user.id)
            if user.count() > 0 and user[0].email is not None and len(user[0].email) > 0 and len(user[0].clave) > 0:
                usuario = user[0].email
                clave = user[0].clave
                firma = user[0].firma
                name_firma = user[0].firma.name

                if envio_correo_electronico(message,to,subject,adjuntos,cc,cco,tipo=tipo,seguimiento=num_seg,usuario=request.user,emisor=usuario,clave=clave,name_firma=name_firma):
                    fx = Faxes()
                    fx.fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
                    fx.numero = seguimiento
                    fx.asunto = subject
                    fx.tipo = ''
                    fx.save()
                    resultado['resultado'] = 'exito'
                else:
                    resultado['resultado'] = 'Ocurrio un error al enviar el email'
            else:
                resultado['resultado'] = 'El usuario no tiene definido correctamente su email y contraseña, favor avisar a un supervisor.'
        except Exception as e:
            resultado['resultado'] = str(e)
    else:
        resultado['resultado'] = 'Ha ocurrido un error.'
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)



def envio_correo_electronico(mensaje, remitentes, titulo, adjuntos, cc,cco,clave=None,seguimiento=None,usuario=None,empresa='', tipo='PRUEBA', archivos=None, emisor=None,name_firma=None):
    correo = CorreoEnviado()
    try:
        # Crear el mensaje HTML con la imagen incrustada
        html_message = f'<html><body><img src="https://opensoft.uy/static/images/oceanlink.png"><br><br>' + str(mensaje)
        # firma
        cc.append(emisor)
        file = str(BASE_DIR) + '/cargosystem/media/' + name_firma
        if name_firma is not None and os.path.isfile(file):
            html_message += '<br><img src="https://opensoft.uy/media/' + name_firma + '">'
        html_message += '</body></html>'
        # Crear el objeto EmailMessage
        if clave is not None and emisor is not None:
            conexion_smtp = mail.get_connection(
                username=emisor,
                password=clave,
                fail_silently=False,
            )
        else:
            conexion_smtp = mail.get_connection(
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                fail_silently=False,
            )
        email = EmailMessage(
            subject=titulo,
            body=html_message,
            from_email=settings.EMAIL_HOST_USER if emisor is None else emisor,
            connection=conexion_smtp,
            # to=remitentes,
        )
        # CORREO SISTEMA
        if emisor is not None:
            correo.emisor = emisor
        else:
            correo.emisor = settings.EMAIL_HOST_USER
        correo.correo = empresa
        correo.fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for r in remitentes:
            correo.enviado_a += ';' + r
        for c in cc:
            if len(c) > 0:
                correo.enviado_a += ';' + c
        for co in cco:
            if len(co) > 0:
                correo.enviado_a += ';' + co
        correo.enviado_a = correo.enviado_a[1:]
        correo.tipo = tipo
        correo.usuario = usuario
        correo.seguimiento = seguimiento
        correo.mensaje = mensaje
        # FIN CORREO
        # email.to = ['tecnicosnm@gmail.com',]
        email.to = remitentes

        email.cc = cc
        email.bcc = cco
        email.content_subtype = 'html'
        # Adjuntar archivos
        for adjunto_id in adjuntos:
            documento = Attachhijo.objects.get(id=adjunto_id)
            path_to_file = default_storage.path(documento.archivo.url[7:])
            file_path = os.path.join(settings.MEDIA_ROOT, path_to_file)
            email.attach_file(file_path)


        # Enviar el correo electrónico
        email.send()
        correo.estado = 'ENVIADO'
        correo.save()
        return True
    except Exception as e:
        correo.estado = 'FALLIDO'
        correo.error = str(e)
        correo.save()
        return False



#
# def envio_correo_electronico2(mensaje,remitentes,titulo,adjuntos,usuario=None,empresa='',tipo='PRUEBA',archivos=None,emisor=None):
#     try:
#         """ GUARDO CORREO A ENVIAR """
#         with open(str(settings.BASE_DIR) + '/cargosystem/static/images/oceanlink.png', 'rb') as image_file:
#             image_data = base64.b64encode(image_file.read()).decode('utf-8')
#         mensaje += ' <img src="data:image/png;base64,' + image_data + '">'
#         correo = CorreoEnviado()
#         correo.correo = empresa
#         correo.fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         correo.enviado_a = remitentes
#         correo.tipo = tipo
#         correo.usuario = usuario
#         correo.mensaje = mensaje
#         """ ENVIO MAIL """
#         from django.core.mail import EmailMessage
#         """VALIDAR EMAIL """
#         try:
#             html_content = f'<html><body>' + mensaje + '</body></html>'
#             email = EmailMessage(titulo, html_content, to=remitentes)
#             if emisor is None:
#                 email.from_email = settings.EMAIL_HOST_USER
#             else:
#                 email.from_email = emisor
#             email.content_subtype = 'HTML'
#             for a in adjuntos:
#                 documento = Attachhijo.objects.get(id=a)
#                 path_to_file = default_storage.path(documento.archivo.url[7:])
#                 file_path = os.path.join(settings.MEDIA_ROOT, path_to_file)
#                 email.attach_file(file_path)
#             email.send()
#             correo.estado = 'ENVIADO'
#             correo.save()
#             return True
#         except Exception as e:
#             correo.estado = 'FALLIDO'
#             correo.error = str(e)
#             correo.save()
#             return False
#     except Exception as e:
#        raise TypeError(e)
#

