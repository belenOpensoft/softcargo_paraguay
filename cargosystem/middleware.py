import json
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.timezone import now, timedelta
from django.http import HttpResponse
from django.urls import resolve
from impomarit.models import BloqueoEdicion


class RolPorPestanaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.rol_pestana = (
            request.headers.get('X-Rol-Activo')
            or request.GET.get('rol')
            or request.session.get('rol')
        )
        return self.get_response(request)

class RolRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Solo aplica si es un redirect
        if isinstance(response, HttpResponseRedirect):
            rol_header = request.headers.get('X-Rol-Activo') or request.session.get('rol_activo')
            if not rol_header:
                return response

            # Parsear la URL
            url_parts = urlparse(response['Location'])
            query_params = parse_qs(url_parts.query)

            if 'rol' not in query_params:
                query_params['rol'] = [rol_header]
                new_query = urlencode(query_params, doseq=True)
                new_url = urlunparse(url_parts._replace(query=new_query))
                return HttpResponseRedirect(new_url)

        return response

class RolActivoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Buscar rol en header, POST o GET
        rol_header = (
            request.headers.get('X-Rol-Activo') or
            request.POST.get('rol_oculto_header') or
            request.GET.get('rol')
        )

        # Guardarlo en sesión si existe
        if rol_header:
            request.session['rol_activo'] = rol_header

        return self.get_response(request)


DEPENDIENTES_MODAL = {
    '/get_data_seguimiento/': [
        {
            'ruta': '/get_data_cronologia/',
            'formulario': 'conologiaForm',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/eliminar_seguimiento/',
            'formulario': 'eliminar_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/get_datos_caratula/',
            'formulario': 'caratula_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/get_data_email/',
            'formulario': 'email_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/source_archivos',
            'formulario': 'archivos_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/source_envases',
            'formulario': 'envases_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/clonar_seguimiento/',
            'formulario': 'clonar_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/source_rutas',
            'formulario': 'rutas_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/source_logs_seguimiento',
            'formulario': 'logs_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/source_gastos',
            'formulario': 'gastos_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/descargar_awb_seguimientos/',
            'formulario': 'guia_madre_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/descargar_awb_seguimientos_draft/',
            'formulario': 'guia_madre_draft_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/get_datos_aplicables/',
            'formulario': 'aplicable_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/source_embarques',
            'formulario': 'carga_no_form',
            'modulo': 'seguimientos',
        },
        {
            'ruta': '/source/',
            'formulario': 'notas_no_form',
            'modulo': 'seguimientos',
        }

    ],
    '/master-detail/': [

    ],
}

RUTAS_BLOQUEO_MODAL = {
    '/get_data_seguimiento/': {
        'formulario': 'seguimientoForm',
        'modulo': 'seguimientos'
    },
    '/master-detail/': {
        'formulario': 'form_modal_embarque',
        'modulo': 'dinamico'
    },
    '/house-detail/': {
        'formulario': 'editHouseForm',
        'modulo': 'dinamico'
    },
}

class BloqueoModalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._bloqueo_info = None

        if request.user.is_authenticated and request.method == 'GET':
            ruta_actual = request.path

            # Verificar si es una master-detail genérica con prefijo
            if ruta_actual.endswith('/master-detail/') and 'id' in request.GET:
                referencia = request.GET.get("id")
                try:
                    int(referencia)
                except ValueError:
                    referencia = None

                if referencia:
                    partes = ruta_actual.strip('/').split('/')
                    modulo = partes[0] if len(partes) >= 2 else 'operaciones'

                    formulario = 'editForm'
                    expiracion = now() + timedelta(minutes=5)

                    # Buscar bloqueo existente
                    bloqueo = BloqueoEdicion.objects.filter(
                        referencia=referencia,
                        formulario=formulario,
                        fecha_expiracion__gt=now(),
                        activo=True,
                        modulo=modulo
                    ).exclude(usuario=request.user).first()

                    if bloqueo:
                        tiempo_restante = bloqueo.fecha_expiracion - now()
                        minutos = int(tiempo_restante.total_seconds() // 60)
                        segundos = int(tiempo_restante.total_seconds() % 60)
                        request._bloqueo_info = {
                            'bloqueado': True,
                            'usuario': bloqueo.usuario.username,
                            'mensaje': f'Este registro está siendo editado por {bloqueo.usuario.username}. '
                                       f'Podrás editarlo en aproximadamente {minutos} min {segundos} seg.'
                        }
                    else:
                        BloqueoEdicion.objects.create(
                            referencia=referencia,
                            formulario=formulario,
                            fecha_expiracion=expiracion,
                            activo=True,
                            usuario=request.user,
                            modulo=modulo
                        )

            #para los directos
            if ruta_actual.endswith('/house-detail/') and 'id' in request.GET:
                referencia = request.GET.get("id")
                try:
                    int(referencia)
                except ValueError:
                    referencia = None

                if referencia:
                    partes = ruta_actual.strip('/').split('/')
                    modulo = partes[0] if len(partes) >= 2 else 'operaciones'

                    formulario = 'editHouseForm'
                    expiracion = now() + timedelta(minutes=5)

                    # Buscar bloqueo existente
                    bloqueo = BloqueoEdicion.objects.filter(
                        referencia=referencia,
                        formulario=formulario,
                        fecha_expiracion__gt=now(),
                        activo=True,
                        modulo=modulo
                    ).exclude(usuario=request.user).first()

                    if bloqueo:
                        tiempo_restante = bloqueo.fecha_expiracion - now()
                        minutos = int(tiempo_restante.total_seconds() // 60)
                        segundos = int(tiempo_restante.total_seconds() % 60)
                        request._bloqueo_info = {
                            'bloqueado': True,
                            'usuario': bloqueo.usuario.username,
                            'mensaje': f'Este registro está siendo editado por {bloqueo.usuario.username}. '
                                       f'Podrás editarlo en aproximadamente {minutos} min {segundos} seg.'
                        }
                    else:
                        BloqueoEdicion.objects.create(
                            referencia=referencia,
                            formulario=formulario,
                            fecha_expiracion=expiracion,
                            activo=True,
                            usuario=request.user,
                            modulo=modulo
                        )

            # 1. Verificar si es una ruta principal
            for ruta_base, config in RUTAS_BLOQUEO_MODAL.items():
                if ruta_actual.startswith(ruta_base):
                    try:
                        id_obj = ruta_actual.rstrip('/').split('/')[-1]
                        int(id_obj)
                    except ValueError:
                        continue

                    referencia = str(id_obj)
                    formulario = config['formulario']
                    modulo = config['modulo']

                    bloqueo = BloqueoEdicion.objects.filter(
                        referencia=referencia,
                        formulario=formulario,
                        fecha_expiracion__gt=now(),
                        activo=True
                    ).exclude(usuario=request.user).first()

                    if bloqueo:
                        tiempo_restante = bloqueo.fecha_expiracion - now()
                        minutos = int(tiempo_restante.total_seconds() // 60)
                        segundos = int(tiempo_restante.total_seconds() % 60)
                        request._bloqueo_info = {
                            'bloqueado': True,
                            'usuario': bloqueo.usuario.username,
                            'mensaje': f'Este registro está siendo editado por {bloqueo.usuario.username}. '
                                       f'Podrás editarlo en aproximadamente {minutos} min {segundos} seg.'
                        }
                    else:
                        expiracion = now() + timedelta(minutes=5)

                        bloqueo = BloqueoEdicion(
                            referencia=referencia,
                            formulario=formulario,
                            fecha_expiracion=expiracion,
                            activo=True,
                            usuario=request.user,
                            modulo=modulo
                        )
                        bloqueo.save()

                        # Crear bloqueos para formularios dependientes de esta ruta
                        dependientes = DEPENDIENTES_MODAL.get(ruta_base, [])
                        for dep in dependientes:
                            bloqueo_dep = BloqueoEdicion(
                                referencia=referencia,
                                formulario=dep['formulario'],
                                fecha_expiracion=expiracion,
                                activo=True,
                                usuario=request.user,
                                modulo=dep['modulo']
                            )
                            bloqueo_dep.save()
                    break

            # 2. Si es una ruta dependiente accedida directamente, bloquear también el resto
            for ruta_base, dependientes in DEPENDIENTES_MODAL.items():
                for dep in dependientes:
                    if ruta_actual.startswith(dep['ruta']):
                        try:
                            id_obj = ruta_actual.rstrip('/').split('/')[-1]
                            int(id_obj)
                        except ValueError:
                            continue

                        referencia = str(id_obj)
                        expiracion = now() + timedelta(minutes=5)

                        # Bloqueo para la ruta dependiente actual
                        bloqueo_actual = BloqueoEdicion.objects.filter(
                            referencia=referencia,
                            formulario=dep['formulario'],
                            fecha_expiracion__gt=now(),
                            activo=True
                        ).exclude(usuario=request.user).first()

                        if bloqueo_actual:
                            tiempo_restante = bloqueo_actual.fecha_expiracion - now()
                            minutos = int(tiempo_restante.total_seconds() // 60)
                            segundos = int(tiempo_restante.total_seconds() % 60)
                            request._bloqueo_info = {
                                'bloqueado': True,
                                'usuario': bloqueo_actual.usuario.username,
                                'mensaje': f'Este registro está siendo editado por {bloqueo_actual.usuario.username}. '
                                           f'Podrás editarlo en aproximadamente {minutos} min {segundos} seg.'
                            }
                            break  # No seguimos si ya está bloqueado

                        # Si no estaba bloqueado, crear bloqueos en:
                        # - el actual
                        # - el principal
                        # - las otras dependencias
                        BloqueoEdicion.objects.create(
                            referencia=referencia,
                            formulario=dep['formulario'],
                            fecha_expiracion=expiracion,
                            activo=True,
                            usuario=request.user,
                            modulo=dep['modulo']
                        )

                        # Bloquear la ruta principal asociada
                        principal_config = RUTAS_BLOQUEO_MODAL.get(ruta_base)
                        if principal_config:
                            BloqueoEdicion.objects.create(
                                referencia=referencia,
                                formulario=principal_config['formulario'],
                                fecha_expiracion=expiracion,
                                activo=True,
                                usuario=request.user,
                                modulo=principal_config['modulo']
                            )

                        # Bloquear las otras rutas dependientes
                        for otra_dep in dependientes:
                            if otra_dep['formulario'] != dep['formulario']:
                                BloqueoEdicion.objects.create(
                                    referencia=referencia,
                                    formulario=otra_dep['formulario'],
                                    fecha_expiracion=expiracion,
                                    activo=True,
                                    usuario=request.user,
                                    modulo=otra_dep['modulo']
                                )

                        break  # ya encontramos una coincidencia, no seguimos buscando

        # Ejecutar la vista y capturar la respuesta
        response = self.get_response(request)

        # # Inyectar el estado de bloqueo si aplica
        # if isinstance(response, JsonResponse) and hasattr(request, '_bloqueo_info') and request._bloqueo_info:
        #     data = json.loads(response.content.decode('utf-8'))
        #     data.update(request._bloqueo_info)
        #     return JsonResponse(data)

        # Inyectar el estado de bloqueo si aplica (no tocar listas)
        if isinstance(response, JsonResponse) and getattr(request, '_bloqueo_info', None):
            try:
                data = json.loads(response.content.decode('utf-8'))
            except Exception:
                return response  # si no puedo parsear, no toco nada

            if isinstance(data, list):  # ⬅️ clave 1: si es lista (autocomplete), no tocar
                return response

            data.update(request._bloqueo_info)  # ⬅️ clave 2: comportamiento actual para dicts
            new = JsonResponse(data, status=response.status_code)
            for k, v in response.items():  # ⬅️ clave 3: preserva headers originales
                new[k] = v
            return new

        return response


