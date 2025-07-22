from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from django.http import HttpResponseRedirect


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
            rol_header = request.headers.get('X-Rol-Activo')
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