from django.http import JsonResponse

from mantenimientos.models import Clientes, Ciudades, Vendedores, Vapores, Proyectos, Traficos, Actividades, Depositos


# class ClienteAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         qs = Clientes.objects.all()
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#         return qs
#
def autocomplete_clientes(request):
    if 'term' in request.GET:
        qs = Clientes.objects.filter(empresa__istartswith=request.GET.get('term')).order_by('empresa')
        lista = []
        for x in qs:
            lista.append({'id':x.codigo,
                          'label':x.empresa,
                          'value':x.empresa,}
                         )
        return JsonResponse(lista,safe=False)

def autocomplete_clientes_codigo(request):
    if 'term' in request.GET:
        qs = Clientes.objects.filter(empresa__istartswith=request.GET.get('term')).order_by('empresa')
        lista = []
        for x in qs:
            lista.append({'id':x.codigo,
                          'label':x.empresa,
                          'value':x.codigo,}
                         )
        return JsonResponse(lista,safe=False)

def autocomplete_ciudades(request):
    if 'term' in request.GET:
        qs = Ciudades.objects.filter(nombre__istartswith=request.GET.get('term')).order_by('nombre')
        lista = []
        for x in qs:
            lista.append({'id':x.codigo,
                          'label':x.nombre,
                          'value':x.nombre,}
                         )
        return JsonResponse(lista,safe=False)

def autocomplete_ciudades_codigo(request):
    if 'term' in request.GET:
        qs = Ciudades.objects.filter(nombre__istartswith=request.GET.get('term')).order_by('codigo')
        lista = []
        for x in qs:
            lista.append({'id':x.codigo,
                          'label':x.nombre,
                          'value':x.codigo,}
                         )
        return JsonResponse(lista,safe=False)

def autocomplete_vendedores(request):
    if 'term' in request.GET:
        qs = Vendedores.objects.filter(nombre__istartswith=request.GET.get('term')).order_by('nombre')
        lista = []
        for x in qs:
            lista.append({'id':x.codigo,
                          'label':x.nombre,
                          'value':x.nombre,}
                         )
        return JsonResponse(lista,safe=False)

def autocomplete_vapores(request):
    if 'term' in request.GET:
        qs = Vapores.objects.filter(nombre__istartswith=request.GET.get('term')).order_by('nombre')
        lista = []
        for x in qs:
            lista.append({'id':x.id,
                          'codigo':x.codigo,
                          'label':x.nombre,
                          'value':x.nombre,}
                         )
        return JsonResponse(lista,safe=False)

def autocomplete_proyectos(request):
    if 'term' in request.GET:
        qs = Proyectos.objects.filter(nombre__istartswith=request.GET.get('term')).order_by('nombre')
        lista = []
        for x in qs:
            lista.append({'id':x.codigo,
                          'label':x.nombre,
                          'value':x.nombre,}
                         )
        return JsonResponse(lista,safe=False)

def autocomplete_traficos(request):
    if 'term' in request.GET:
        qs = Traficos.objects.filter(nombre__istartswith=request.GET.get('term')).order_by('nombre')
        lista = []
        for x in qs:
            lista.append({'id':x.codigo,
                          'label':x.nombre,
                          'value':x.nombre,}
                         )
        return JsonResponse(lista,safe=False)

def autocomplete_actividades(request):
    if 'term' in request.GET:
        qs = Actividades.objects.filter(nombre__istartswith=request.GET.get('term')).order_by('nombre')
        lista = []
        for x in qs:
            lista.append({'id':x.numero,
                          'label':x.nombre,
                          'value':x.nombre,}
                         )
        return JsonResponse(lista,safe=False)

def autocomplete_depositos(request):
    if 'term' in request.GET:
        qs = Depositos.objects.filter(empresa__istartswith=request.GET.get('term')).order_by('empresa')
        lista = []
        for x in qs:
            lista.append({'id':x.codigo,
                          'label':x.empresa,
                          'value':x.empresa,
                        })
        return JsonResponse(lista,safe=False)


