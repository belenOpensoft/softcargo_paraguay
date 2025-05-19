from datetime import datetime
from django.shortcuts import redirect
from administracion_contabilidad.models import Dolar

class VerificarArbitrajeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        modulo = request.session.get('rol')
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
                return redirect('/admin_cont/verificar_arbitraje/')

        return self.get_response(request)

