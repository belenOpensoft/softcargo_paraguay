from datetime import datetime
from urllib.parse import urlencode

from django.shortcuts import redirect
from administracion_contabilidad.models import Dolar

class VerificarArbitrajeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # modulo = request.session.get('rol')
        modulo = getattr(request, "rol_pestana", None) or request.session.get("rol_activo") or request.session.get("rol")
        path = request.path

        excepciones = [
            '/admin_cont/verificar_arbitraje/',
            '/admin_cont/guardar_arbitraje/',
        ]

        if (
            modulo == 'administracion' and
            path.startswith('/admin_cont/') and
            path not in excepciones
        ):
            hoy = datetime.today().date()
            if not Dolar.objects.filter(ufecha__date=hoy).exists():
                query = urlencode({"rol": modulo}) if modulo else ""
                url = '/admin_cont/verificar_arbitraje/'
                if query:
                    url = f"{url}?{query}"
                return redirect(url)
                # return redirect('/admin_cont/verificar_arbitraje/')

        return self.get_response(request)

