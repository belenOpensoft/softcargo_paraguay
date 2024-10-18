from django.views.generic import ListView
from mantenimientos.models import Clientes, Vapores


class autocomplete_clientes(ListView):
    model = Clientes
    template_name = 'seleccion_autocompletar.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Clientes.objects.filter(empresa__icontains=query)[:15]
        return Clientes.objects.none()

class autocomplete_buques(ListView):
    model = Vapores
    template_name = 'seleccion_autocompletar.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Vapores.objects.filter(nombre__icontains=query)[:15]
        return Vapores.objects.none()
