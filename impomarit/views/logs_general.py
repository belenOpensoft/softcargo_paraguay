import json
from itertools import chain
from operator import attrgetter
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from auditlog.models import LogEntry


ICONOS_MODELOS = {
    'embarqueaereo': '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-globe2" viewBox="0 0 16 16"><path d="..."/></svg>',
    'envases': '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-box-seam" viewBox="0 0 16 16"><path d="..."/></svg>',
    'cargaaerea': '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-truck" viewBox="0 0 16 16"><path d="..."/></svg>',
    'conexaerea': '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16"><path d="..."/></svg>',
    'serviceaereo': '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-currency-dollar" viewBox="0 0 16 16"><path d="..."/></svg>',
    'attachhijo': '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-filetype-docx" viewBox="0 0 16 16"><path d="..."/></svg>',
}


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
    for registro in registros_filtrados:
        modelo = registro.content_type.model.lower()

        icono = ''
        for clave, svg in ICONOS_MODELOS.items():
            if clave in modelo:
                icono = svg
                break

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



def obtener_logs_generico(request, modelo_principal, field_id, modelos_relacionados):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        draw = int(request.GET.get('draw', 1))
        numero = request.GET.get('numero')
        object_id = request.GET.get('id')
        end = start + length

        logs = LogEntry.objects.filter(
            content_type=ContentType.objects.get_for_model(modelo_principal),
            object_pk=str(object_id)
        )

        for model in modelos_relacionados:
            ct = ContentType.objects.get_for_model(model)
            relacionados = model.objects.filter(**{field_id: numero}).values_list('pk', flat=True)
            logs = chain(logs, LogEntry.objects.filter(content_type=ct, object_pk__in=[str(pk) for pk in relacionados]))

        logs_combinados = list(logs)
        logs_combinados.sort(key=attrgetter('timestamp'), reverse=True)
        logs_paginados = logs_combinados[start:end]
        data = get_data(logs_paginados)

        return HttpResponse(json.dumps({
            'data': data,
            'draw': draw,
            'recordsTotal': len(logs_combinados),
            'recordsFiltered': len(logs_combinados)
        }), content_type="application/json")

    return HttpResponse("fail")
