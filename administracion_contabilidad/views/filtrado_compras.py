from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from datetime import datetime
from impomarit.models import VEmbarqueaereo as Vim
from impomarit.models import Reservas as Mim
from impomarit.models import Cargaaerea as Cim
from impaerea.models import VEmbarqueaereo as Via
from impaerea.models import ImportReservas as Mia
from impaerea.models import ImportCargaaerea as Cia
from impterrestre.models import VEmbarqueaereo as Vit
from impterrestre.models import ImpterraReservas as Mit
from impterrestre.models import ImpterraCargaaerea as Cit
from expmarit.models import VEmbarqueaereo as Vem
from expmarit.models import ExpmaritReservas as Mem
from expmarit.models import ExpmaritCargaaerea as Cem
from expaerea.models import VEmbarqueaereo as Vea
from expaerea.models import ExportReservas as Mea
from expaerea.models import ExportCargaaerea as Cea
from expterrestre.models import VEmbarqueaereo as Vet
from expterrestre.models import ExpterraReservas as Met
from expterrestre.models import ExpterraCargaaerea as Cet
from mantenimientos.models import Clientes


def buscar_reservas(departamento, fecha_desde, fecha_hasta, posicion, tipo_embarque, conocimiento, transportista,
                    agente, status, contenedor, vapor,embarque,seguimiento):
    try:
        modelos = {
            '1': Mim, '2': Mit, '3': Mia,
            '4': Mem, '5': Mea, '6': Met
        }
        modelo = modelos.get(departamento)

        modelos_embarque = {
            '1': Vim, '2': Cit, '3': Via,
            '4': Vem, '5': Vea, '6': Vet
        }
        modelo_embarque = modelos_embarque.get(departamento)

        modelos_carga = {
            '1': Cim, '2': Vit, '3': Cia,
            '4': Cem, '5': Cea, '6': Cet
        }
        modelo_carga = modelos_carga.get(departamento)

        if not modelo:
            return JsonResponse({'error': 'Departamento inválido'}, status=400)

        # Construcción de filtros dinámicos
        filtros = {}

        if fecha_desde:
            filtros['fechaingreso__gte'] = datetime.strptime(fecha_desde, "%Y-%m-%d")
        if fecha_hasta:
            filtros['fechaingreso__lte'] = datetime.strptime(fecha_hasta, "%Y-%m-%d")
        if posicion:
            filtros['posicion__icontains'] = posicion
        if conocimiento:
            filtros['awb__icontains'] = conocimiento
        if transportista:
            filtros['transportista__icontains'] = transportista
        if agente:
            filtros['agente__icontains'] = agente
        if status:
            filtros['status__icontains'] = status
        if vapor:
            filtros['vapor__icontains'] = vapor

        if seguimiento:
            resultados = modelo_embarque.objects.filter(seguimiento__icontains=seguimiento)
            resultados = resultados.values_list("awb", flat=True)
            if resultados:
                regex = '|'.join(resultados)
                filtros['awb__regex'] = regex

        if embarque:
            resultados = modelo_embarque.objects.filter(numero__icontains=embarque)
            resultados = resultados.values_list("awb", flat=True)
            if resultados:
                regex = '|'.join(resultados)
                filtros['awb__regex'] = regex

        if contenedor:
            numeros = modelo_carga.objects.filter(nrocontenedor=contenedor).values_list('numero',flat=True)
            embarques = modelo_embarque.objects.filter(numero__in=numeros).values_list('awb',flat=True)
            if embarques:
                regex = '|'.join(embarques)
                filtros['awb__regex'] = regex

        # Obtener resultados filtrados
        reservas = modelo.objects.filter(**filtros)

        # Convertir a JSON
        data = [
            {
                'embarque': e.numero,
                'tipo': 'CONSOLIDADO',
                'fecha': e.fechaingreso.strftime("%Y-%m-%d"),
                'posicion': e.posicion,
                'conocimiento': e.awb,
                'transportista': Clientes.objects.get(codigo=e.transportista).empresa if e.transportista is not None else '',
                'agente': Clientes.objects.get(codigo=e.agente).empresa if e.agente is not None else '',
                'tarifa': 0,  # Ajustar si se necesita
                'status': e.status,
                'cliente': Clientes.objects.get(codigo=e.consignatario).empresa if e.consignatario is not None else '',

            }
            for e in reservas
        ]

        return data
    except Exception as e:
        return e


def buscar_embarques(request):
    cual = request.GET.get('cual', '').strip()
    departamento = request.GET.get('departamento', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    posicion = request.GET.get('posicion', '').strip()
    tipo_embarque = request.GET.get('tipo_embarque', '')
    conocimiento = request.GET.get('conocimiento', '').strip()
    transportista = request.GET.get('transportista', '').strip()
    agente = request.GET.get('agente', '').strip()
    status = request.GET.get('status', '').strip()
    contenedor = request.GET.get('contenedor', '').strip()
    vapor = request.GET.get('vapor', '').strip()
    seguimiento = request.GET.get('seguimiento', '').strip()
    master = request.GET.get('master', '').strip()
    embarque = request.GET.get('embarque', '').strip()

    if cual == 'master':
        masters = buscar_reservas(departamento,fecha_desde,fecha_hasta,posicion,tipo_embarque,conocimiento,transportista,agente,status,contenedor,vapor,embarque,seguimiento)
        return JsonResponse({'resultados': masters}, safe=False)
    # Seleccionar el modelo correspondiente al departamento
    modelos = {
        '1': Vim, '2': Vit, '3': Via,
        '4': Vem, '5': Vea, '6': Vet
    }
    modelo = modelos.get(departamento)

    if not modelo:
        return JsonResponse({'error': 'Departamento inválido'}, status=400)

    # Construcción de filtros dinámicos
    filtros = {}

    if fecha_desde:
        filtros['fechaingreso__gte'] = datetime.strptime(fecha_desde, "%Y-%m-%d")
    if fecha_hasta:
        filtros['fechaingreso__lte'] = datetime.strptime(fecha_hasta, "%Y-%m-%d")
    if posicion:
        filtros['posicion__icontains'] = posicion
    if conocimiento:
        filtros['hawb__icontains'] = conocimiento
    if transportista:
        filtros['transportista__icontains'] = transportista
    if agente:
        filtros['agente__icontains'] = agente
    if status:
        filtros['status__icontains'] = status
    if contenedor:
        filtros['contenedor__icontains'] = contenedor
    if vapor:
        filtros['vapor__icontains'] = vapor
    if seguimiento:
        filtros['seguimiento__icontains'] = seguimiento
    if master:
        filtros['awb__icontains'] = master
    if embarque:
        filtros['numero__icontains'] = embarque

    # Filtrar por tipo de embarque
    if tipo_embarque == "consolidado":
        filtros['consolidado'] = 1
    elif tipo_embarque == "directo":
        filtros['consolidado'] = 0

    # Obtener resultados filtrados
    embarques = modelo.objects.filter(**filtros)

    # Convertir a JSON
    data = [
        {
            'embarque': e.numero,
            'tipo': 'CONSOLIDADO' if e.consolidado == 1 else 'DIRECTO',
            'fecha': e.fechaingreso.strftime("%Y-%m-%d"),
            'posicion': e.posicion,
            'conocimiento': e.hawb,
            'transportista': e.transportista,
            'agente': e.agente,
            'tarifa': 0,  # Ajustar si se necesita
            'status': e.status,
            'cliente': e.consignatario,

        }
        for e in embarques
    ]

    return JsonResponse({'resultados': data}, safe=False)



