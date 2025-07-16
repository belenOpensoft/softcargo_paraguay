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
from expaerea.models import ExportEmbarqueaereo
from expmarit.models import ExpmaritEmbarqueaereo
from expterrestre.models import ExpterraEmbarqueaereo
from impaerea.models import ImportEmbarqueaereo
from impomarit.models import Embarqueaereo
from impterrestre.models import ImpterraEmbarqueaereo
from login.models import CorreoEnviado, Account, AccountEmail
from cargosystem import settings
from login.views.correos import is_ajax
from seguimientos.models import Attachhijo, Faxes, Seguimiento

def envio_notificacion_seguimiento(request,modulo=None):
    resultado = {}
    if is_ajax(request):
        try:
            to = request.POST['to'].split(';')
            from_email = request.POST['from']
            cc = request.POST['cc'].split(';') if request.POST['cc'] is not None else []
            cco = request.POST['cco'].split(';') if (request.POST['cco'] is not None and request.POST['cco']) else []
            tipo = request.POST['tipo']
            seguimiento = request.POST['seguimiento']
            num_seg = ''
            if modulo == 'SG':
                aux = Seguimiento.objects.get(numero=seguimiento)
                num_seg = str(aux.numero) + ' ' + str(aux.modo)
            elif modulo == 'IA':
                aux = ImportEmbarqueaereo.objects.get(numero=seguimiento).seguimiento
                num_seg = str(aux) + ' IMPORT AEREO'
            elif modulo == 'IM':
                aux = Embarqueaereo.objects.get(numero=seguimiento).seguimiento
                num_seg = str(aux) + ' IMPORT MARITIMO'
            elif modulo == 'IT':
                aux = ImpterraEmbarqueaereo.objects.get(numero=seguimiento).seguimiento
                num_seg = str(aux) + ' IMPORT TERRESTRE'
            elif modulo == 'EA':
                aux = ExportEmbarqueaereo.objects.get(numero=seguimiento).seguimiento
                num_seg = str(aux) + ' EXPORT AEREO'
            elif modulo == 'EM':
                aux = ExpmaritEmbarqueaereo.objects.get(numero=seguimiento).seguimiento
                num_seg = str(aux) + ' EXPORT MARITIMO'
            elif modulo == 'ET':
                aux = ExpterraEmbarqueaereo.objects.get(numero=seguimiento).seguimiento
                num_seg = str(aux) + ' EXPORT TERRESTRE'
            elif modulo == 'AD':
                num_seg = 'ADMINISTRACION'


            adjuntos = simplejson.loads(request.POST['archivos_adjuntos'])
            subject = request.POST['subject']
            message = request.POST['message']
            user = Account.objects.filter(user__id=request.user.id).first()
            account_email = AccountEmail.objects.filter(user=request.user, email=from_email).first()
            if not account_email or not account_email.clave:
                resultado['resultado'] = 'El usuario no tiene definido correctamente su email y contraseña, favor avisar a un supervisor.'
            else:
                clave = account_email.clave

            if clave is not None:
                if envio_correo_electronico(message,to,subject,adjuntos,cc,cco,tipo=tipo,seguimiento=num_seg,usuario=request.user,emisor=from_email,clave=clave,name_firma=user.firma.name,modulo=modulo):
                    fx = Faxes()
                    fx.fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
                    fx.numero = seguimiento
                    fx.asunto = subject
                    fx.tipo = ''
                    fx.save()
                    resultado['resultado'] = 'exito'
                else:
                    resultado['resultado'] = 'Ocurrio un error al enviar el email'

        except Exception as e:
            resultado['resultado'] = str(e)
    else:
        resultado['resultado'] = 'Ha ocurrido un error.'
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def envio_correo_electronico(mensaje, remitentes, titulo, adjuntos, cc,cco,clave=None,seguimiento=None,usuario=None,empresa='', tipo='PRUEBA', archivos=None, emisor=None,name_firma=None,modulo=None):
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
        if modulo:
            correo.modulo = modulo

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







