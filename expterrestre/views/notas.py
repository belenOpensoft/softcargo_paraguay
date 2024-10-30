import json

import simplejson
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from expterrestre.models import ExpterraFaxes as Faxes
from impomarit.forms import NotasForm

def source(request):
    # Verificación de solicitud AJAX en Django 4.2
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax:
        numero = request.GET.get('numero')
        if numero:
            notas_list = Faxes.objects.filter(numero=numero).values('id', 'fecha', 'notas', 'asunto', 'tipo','notas')
        else:
            notas_list = Faxes.objects.all().values('id', 'fecha', 'asunto', 'tipo','notas')

        response_data = {"data": list(notas_list)}
        return JsonResponse(response_data)

    # Renderiza la plantilla cuando no es una solicitud AJAX
    return render(request, 'notas.html')  # Ajusta 'notas.html' con el nombre de tu plantilla real


def guardar_notas(request):
    resultado = {}
    try:
        # Verifica que request.body contenga datos
        if not request.body:
            return JsonResponse({"resultado": "error", "mensaje": "No data received"}, status=400)

        # Carga los datos JSON desde request.body
        data = json.loads(request.body)  # Convierte JSON a diccionario

        # Extrae los valores de los campos
        id_nota = data.get('id_nota')  # ID de la nota, si existe
        numero = data.get('numero')
        fecha = data.get('fecha')
        asunto = data.get('asunto')
        tipo = data.get('tipo')
        notas = data.get('notas')

        # Si id_nota está presente, trata la solicitud como una actualización
        if id_nota:
            registro = Faxes.objects.get(id=id_nota)
            registro.numero = numero
            registro.fecha = fecha
            registro.asunto = asunto
            registro.tipo = tipo
            registro.notas = notas
            registro.save()
            resultado['resultado'] = 'exito'
            resultado['mensaje'] = 'Nota actualizada correctamente'
        else:
            # Si no hay id_nota, crea un nuevo registro
            registro = Faxes(
                numero=numero,
                fecha=fecha,
                asunto=asunto,
                tipo=tipo,
                notas=notas
            )
            registro.save()
            resultado['resultado'] = 'exito'
            resultado['mensaje'] = 'Nota creada correctamente'
            resultado['id'] = registro.id

    except Faxes.DoesNotExist:
        resultado['resultado'] = 'error'
        resultado['mensaje'] = 'Nota no encontrada para actualización.'
    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = 'error'
        resultado['mensaje'] = str(e)

    return JsonResponse(resultado)

def eliminar_nota(request):
    resultado = {}
    try:
        id = request.POST.get('id')
        Faxes.objects.get(id=id).delete()
        resultado['resultado'] = 'exito'
    except Faxes.DoesNotExist:
        resultado['resultado'] = 'La nota no existe.'
    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)

    return JsonResponse(resultado)