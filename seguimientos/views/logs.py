import json
from itertools import chain
from operator import attrgetter

import simplejson
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from seguimientos.models import Faxes, Seguimiento, Envases, Cargaaerea, Conexaerea, Serviceaereo, Attachhijo
from django.contrib.contenttypes.models import ContentType
from auditlog.models import LogEntry
import json

""" TABLA PUERTO """
columns_table_old = {
    1: 'fecha',
    2: 'notas',
    3: 'asunto',
    4: 'tipo',
}
columns_table = {
    0: 'icono',
    1: 'timestamp',
    2: 'actor',
    3: 'action',
    4: 'changes',
}



"""
def source_logs(request):
    if is_ajax(request):
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        draw = int(request.GET.get('draw', 1))
        numero = request.GET.get('numero')
        id = request.GET.get('id')
        end = start + length

        #content_type = ContentType.objects.get_for_model(Seguimiento)
        logs = LogEntry.objects.filter(
            content_type_id=131,
            object_pk=str(id)
        ).order_by('-timestamp')

        ct_envases = ContentType.objects.get_for_model(Envases)
        logs_envases = LogEntry.objects.filter(
            content_type=ct_envases,
            object_pk__in=[str(e.pk) for e in Envases.objects.filter(numero=numero)]
        ).order_by('-timestamp')

        data = []
        for log in logs[start:end]:
            data.append([
                log.id,
                log.timestamp.strftime("%Y-%m-%d %H:%M"),
                log.actor.username if log.actor else 'Sistema',
                log.get_action_display().capitalize(),
                format_changes(log.changes) if log.changes else ''
            ])

        return HttpResponse(json.dumps({
            'data': data,
            'draw': draw,
            'recordsTotal': logs.count(),
            'recordsFiltered': logs.count()
        }), content_type="application/json")

    return HttpResponse("fail")
def get_data(registros_filtrados):
    data = []
    for registro in registros_filtrados:
        fila = []
        fila.append(str(registro.timestamp.strftime('%Y-%m-%d %H:%M')))
        fila.append(str(registro.actor) if registro.actor else 'Sistema')
        fila.append(registro.get_action_display())  # 'Creado', 'Actualizado', etc.
        fila.append(registro.changes[:50] + '...' if registro.changes and len(registro.changes) > 100 else registro.changes)
        data.append(fila)
    return data
def format_changes(changes):
    try:
        cambios = json.loads(changes)
        resultado = []
        for campo, valores in cambios.items():
            antes, despues = valores
            if antes == "":
                antes = "(vacío)"
            if despues == "":
                despues = "(vacío)"
            resultado.append(f"{campo}: {antes} → {despues}")
        return "<br>".join(resultado)
    except:
        return changes  # fallback si no es JSON válido
"""

"""
def source_logs_old(request):
    if is_ajax(request):

        start = int(request.GET['start'])
        numero = request.GET['numero']
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)

        registros = Faxes.objects.filter(numero=numero).order_by(*order)

        resultado = {}
        data = get_data(registros[start:end])

        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Faxes.objects.filter(numero=numero).count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def get_data_old(registros_filtrados):
    try:

        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.fecha is None else str(registro.fecha)[:10])
            registro_json.append('' if registro.notas is None else str(registro.notas)[:50])
            registro_json.append('' if registro.asunto is None else str(registro.asunto)[:50])
            registro_json.append('' if registro.tipo is None else str(registro.tipo))
            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)
"""

def format_changes(changes):
    try:
        cambios = json.loads(changes)
        resultado = []
        for campo, valores in cambios.items():
            antes, despues = valores
            if antes == "" or antes is None:
                antes = "(vacío)"
            if despues == "" or despues is None:
                despues = "(vacío)"
            resultado.append(f"{campo}: {antes} → {despues}")
        return "<br>".join(resultado)
    except:
        return changes

def get_data(registros_filtrados):
    data = []

    # Íconos por modelo
    iconos = {
        'seguimiento': '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-globe2" viewBox="0 0 16 16"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m7.5-6.923c-.67.204-1.335.82-1.887 1.855q-.215.403-.395.872c.705.157 1.472.257 2.282.287zM4.249 3.539q.214-.577.481-1.078a7 7 0 0 1 .597-.933A7 7 0 0 0 3.051 3.05q.544.277 1.198.49zM3.509 7.5c.036-1.07.188-2.087.436-3.008a9 9 0 0 1-1.565-.667A6.96 6.96 0 0 0 1.018 7.5zm1.4-2.741a12.3 12.3 0 0 0-.4 2.741H7.5V5.091c-.91-.03-1.783-.145-2.591-.332M8.5 5.09V7.5h2.99a12.3 12.3 0 0 0-.399-2.741c-.808.187-1.681.301-2.591.332zM4.51 8.5c.035.987.176 1.914.399 2.741A13.6 13.6 0 0 1 7.5 10.91V8.5zm3.99 0v2.409c.91.03 1.783.145 2.591.332.223-.827.364-1.754.4-2.741zm-3.282 3.696q.18.469.395.872c.552 1.035 1.218 1.65 1.887 1.855V11.91c-.81.03-1.577.13-2.282.287zm.11 2.276a7 7 0 0 1-.598-.933 9 9 0 0 1-.481-1.079 8.4 8.4 0 0 0-1.198.49 7 7 0 0 0 2.276 1.522zm-1.383-2.964A13.4 13.4 0 0 1 3.508 8.5h-2.49a6.96 6.96 0 0 0 1.362 3.675c.47-.258.995-.482 1.565-.667m6.728 2.964a7 7 0 0 0 2.275-1.521 8.4 8.4 0 0 0-1.197-.49 9 9 0 0 1-.481 1.078 7 7 0 0 1-.597.933M8.5 11.909v3.014c.67-.204 1.335-.82 1.887-1.855q.216-.403.395-.872A12.6 12.6 0 0 0 8.5 11.91zm3.555-.401c.57.185 1.095.409 1.565.667A6.96 6.96 0 0 0 14.982 8.5h-2.49a13.4 13.4 0 0 1-.437 3.008M14.982 7.5a6.96 6.96 0 0 0-1.362-3.675c-.47.258-.995.482-1.565.667.248.92.4 1.938.437 3.008zM11.27 2.461q.266.502.482 1.078a8.4 8.4 0 0 0 1.196-.49 7 7 0 0 0-2.275-1.52c.218.283.418.597.597.932m-.488 1.343a8 8 0 0 0-.395-.872C9.835 1.897 9.17 1.282 8.5 1.077V4.09c.81-.03 1.577-.13 2.282-.287z"/></svg>',
        'envases': '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-box-seam" viewBox="0 0 16 16"' +
                            '><path d="M8.186 1.113a.5.5 0 0 0-.372 0L1.846 3.5l2.404.961L10.404 2l-2.218-.887zm3.564 1.426L5.596 5 8 5.961 14.154 3.5l-2.404-.' +
                            '961zm3.25 1.7-6.5 2.6v7.922l6.5-2.6V4.24zM7.5 14.762V6.838L1 4.239v7.923l6.5 2.6zM7.443.184a1.5 1.5 0 0 1 1.114 0l7.129 2.852A.5.5 0 0 1 16' +
                            ' 3.5v8.662a1 1 0 0 1-.629.928l-7.185 2.874a.5.5 0 0 1-.372 0L.63 13.09a1 1 0 0 1-.63-.928V3.5a.5.5 0 0 1 .314-.464L7.443.184z"/> </svg>',
        'cargaaerea': '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-truck" viewBox="0 0 16 16">\n' +
                         '<path d="M0 3.5A1.5 1.5 0 0 1 1.5 2h9A1.5 1.5 0 0 1 12 3.5V5h1.02a1.5 1.5 0 0 1 1.17.563l1.481 1.85a1.5 1.5 0 0 1 .329.938V10.5a1.5 1.5 0 0 1-1.5 1.5H14a2 2 0 1 1-4 0H5a2 2 0 1 1-3.998-.085A1.5 1.5 0 0 1 0 10.5zm1.294 7.456A2 2 0 0 1 4.732 11h5.536a2 2 0 0 1 .732-.732V3.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5v7a.5.5 0 0 0 .294.456M12 10a2 2 0 0 1 1.732 1h.768a.5.5 0 0 0 .5-.5V8.35a.5.5 0 0 0-.11-.312l-1.48-1.85A.5.5 0 0 0 13.02 6H12zm-9 1a1 1 0 1 0 0 2 1 1 0 0 0 0-2m9 0a1 1 0 1 0 0 2 1 1 0 0 0 0-2"/>\n' +
                         '</svg>',
        'conexaerea': '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">\n' +
                    '<path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>\n' +
                    '<path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>\n' +
                    '</svg>',
        'serviceaereo': '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-currency-dollar" viewBox="0 0 16 16"' +
                    '><path d="M4 10.781c.148 1.667 1.513 2.85 3.591 3.003V15h1.043v-1.216c2.27-.179 3.678-1.438 3.678-3.3 0-1.59-.947-2.51-2.956-3.028l-.722-.18' +
                    '7V3.467c1.122.11 1.879.714 2.07 1.616h1.47c-.166-1.6-1.54-2.748-3.54-2.875V1H7.591v1.233c-1.939.23-3.27 1.472-3.27 3.156 0 1.454.966 2.483 2.' +
                    '661 2.917l.61.162v4.031c-1.149-.17-1.94-.8-2.131-1.718H4zm3.391-3.836c-1.043-.263-1.6-.825-1.6-1.616 0-.944.704-1.641 1.8-1.828v3.495l-.2-.05z' +
                    'm1.591 1.872c1.287.323 1.852.859 1.852 1.769 0 1.097-.826 1.828-2.2 1.939V8.73l.348.086z"/>sss</svg>',
        'attachhijo': '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-filetype-docx" viewBox="0 0 16 16"' +
                            '><path fill-rule="evenodd" d="M14 4.5V11h-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5Zm-6.839 9.688v-.522a1.54 1.54 0 0 0-.117-.641.861.861 0 0 0-.322-.387.862.862 0 0 0-.469-.129.868.868 0 0 0-.471.13.868.868 0 0 0-.32.386 1.54 1.54 0 0 0-.117.641v.522c0 .256.04.47.117.641a.868.868 0 0 0 .32.387.883.883 0 0 0 .471.126.877.877 0 0 0 .469-.126.861.861 0 0 0 .322-.386 1.55 1.55 0 0 0 .117-.642Zm.803-.516v.513c0 .375-.068.7-.205.973a1.47 1.47 0 0 1-.589.627c-.254.144-.56.216-.917.216a1.86 1.86 0 0 1-.92-.216 1.463 1.463 0 0 1-.589-.627 2.151 2.151 0 0 1-.205-.973v-.513c0-.379.069-.704.205-.975.137-.274.333-.483.59-.627.257-.147.564-.22.92-.22.357 0 .662.073.916.22.256.146.452.356.59.63.136.271.204.595.204.972ZM1 15.925v-3.999h1.459c.406 0 .741.078 1.005.235.264.156.46.382.589.68.13.296.196.655.196 1.074 0 .422-.065.784-.196 1.084-.131.301-.33.53-.595.689-.264.158-.597.237-.999.237H1Zm1.354-3.354H1.79v2.707h.563c.185 0 .346-.028.483-.082a.8.8 0 0 0 .334-.252c.088-.114.153-.254.196-.422a2.3 2.3 0 0 0 .068-.592c0-.3-.04-.552-.118-.753a.89.89 0 0 0-.354-.454c-.158-.102-.361-.152-.61-.152Zm6.756 1.116c0-.248.034-.46.103-.633a.868.868 0 0 1 .301-.398.814.814 0 0 1 .475-.138c.15 0 .283.032.398.097a.7.7 0 0 1 .273.26.85.85 0 0 1 .12.381h.765v-.073a1.33 1.33 0 0 0-.466-.964 1.44 1.44 0 0 0-.49-.272 1.836 1.836 0 0 0-.606-.097c-.355 0-.66.074-.911.223-.25.148-.44.359-.571.633-.131.273-.197.6-.197.978v.498c0 .379.065.704.194.976.13.271.321.48.571.627.25.144.555.216.914.216.293 0 .555-.054.785-.164.23-.11.414-.26.551-.454a1.27 1.27 0 0 0 .226-.674v-.076h-.765a.8.8 0 0 1-.117.364.699.699 0 0 1-.273.248.874.874 0 0 1-.401.088.845.845 0 0 1-.478-.131.834.834 0 0 1-.298-.393 1.7 1.7 0 0 1-.103-.627v-.495Zm5.092-1.76h.894l-1.275 2.006 1.254 1.992h-.908l-.85-1.415h-.035l-.852 1.415h-.862l1.24-2.015-1.228-1.984h.932l.832 1.439h.035l.823-1.439Z"' +
                            '/></svg>',
    }

    for registro in registros_filtrados:
        modelo = registro.content_type.model.lower()
        icono = iconos.get(modelo, '')  # fallback sin icono
        usuario = registro.actor.username if registro.actor else 'Sistema'
        fila = [
            icono,
            registro.timestamp.strftime('%Y-%m-%d %H:%M'),
            f"<strong>{usuario}</strong>",
            registro.get_action_display().capitalize(),
            f"<strong>{modelo.upper()}</strong><br>{format_changes(registro.changes) if registro.changes else ''}"
        ]
        data.append(fila)
    return data

def source_logs(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        draw = int(request.GET.get('draw', 1))
        numero = request.GET.get('numero')
        id = request.GET.get('id')
        end = start + length

        # Logs del modelo Seguimiento
        logs_seguimiento = LogEntry.objects.filter(
            content_type=ContentType.objects.get_for_model(Seguimiento),
            object_pk=str(id)
        )

        # Logs del modelo Envases (relacionados por numero)
        ct_envases = ContentType.objects.get_for_model(Envases)
        envases_relacionados = Envases.objects.filter(numero=numero).values_list('pk', flat=True)
        logs_envases = LogEntry.objects.filter(
            content_type=ct_envases,
            object_pk__in=[str(pk) for pk in envases_relacionados]
        )
        # logs del modelo Cargaaerea
        ct_carga = ContentType.objects.get_for_model(Cargaaerea)
        carga_relacionados = Cargaaerea.objects.filter(numero=numero).values_list('pk', flat=True)
        logs_carga = LogEntry.objects.filter(
            content_type=ct_carga,
            object_pk__in=[str(pk) for pk in carga_relacionados]
        )
        # logs del modelo Conexaerea
        ct_conex = ContentType.objects.get_for_model(Conexaerea)
        conex_relacionados = Conexaerea.objects.filter(numero=numero).values_list('pk', flat=True)
        logs_conex = LogEntry.objects.filter(
            content_type=ct_conex,
            object_pk__in=[str(pk) for pk in conex_relacionados]
        )
        # logs del modelo Serviceaereo
        ct_ser = ContentType.objects.get_for_model(Serviceaereo)
        ser_relacionados = Serviceaereo.objects.filter(numero=numero).values_list('pk', flat=True)
        logs_ser = LogEntry.objects.filter(
            content_type=ct_ser,
            object_pk__in=[str(pk) for pk in ser_relacionados]
        )
        # logs del modelo Attach
        ct_att = ContentType.objects.get_for_model(Attachhijo)
        att_relacionados = Attachhijo.objects.filter(numero=numero).values_list('pk', flat=True)
        logs_att = LogEntry.objects.filter(
            content_type=ct_att,
            object_pk__in=[str(pk) for pk in att_relacionados]
        )
        # Combinar y ordenar por fecha
        logs_combinados = list(chain(logs_seguimiento, logs_envases,logs_carga,logs_conex,logs_ser,logs_att))
        logs_combinados.sort(key=attrgetter('timestamp'), reverse=True)

        # Aplicar paginación
        logs_paginados = logs_combinados[start:end]
        data = get_data(logs_paginados)

        return HttpResponse(json.dumps({
            'data': data,
            'draw': draw,
            'recordsTotal': len(logs_combinados),
            'recordsFiltered': len(logs_combinados)
        }), content_type="application/json")

    return HttpResponse("fail")

def get_order(request, columns):
    try:
        result = []
        order_column = request.GET['order[0][column]']
        order_dir = request.GET['order[0][dir]']
        order = columns[int(order_column)]
        if order_dir == 'desc':
            order = '-' + columns[int(order_column)]
        result.append(order)
        i = 1
        while i > 0:
            try:
                order_column = request.GET['order[' + str(i) + '][column]']
                order_dir = request.GET['order[' + str(i) + '][dir]']
                order = columns[int(order_column)]
                if order_dir == 'desc':
                    order = '-' + columns[int(order_column)]
                result.append(order)
                i += 1
            except Exception as e:
                i = 0
        result.append('id')
        return result
    except Exception as e:
        raise TypeError(e)

def is_ajax(request):
    try:
        req = request.META.get('HTTP_X_REQUESTED_WITH')
        # return req == 'XMLHttpRequest'
        return True
    except Exception as e:
        messages.error(request,e)


