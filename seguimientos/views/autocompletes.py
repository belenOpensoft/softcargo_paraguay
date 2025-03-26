from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect

from mantenimientos.forms import add_buque_form
from mantenimientos.models import Clientes, Ciudades, Vendedores, Vapores, Proyectos, Traficos, Actividades, Depositos, \
    Productos


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

def agregar_buque(request):
    try:
            if request.method == 'POST':
                form = add_buque_form(request.POST)
                if form.is_valid():
                    buque = Vapores()
                    buque.codigo = buque.get_codigo()
                    buque.nombre = form.cleaned_data['nombre']
                    buque.save()
                    return JsonResponse({"success": True, "id": buque.codigo})
                else:
                    return JsonResponse({"success": False, "error": 'formulario incorrecto'}, status=500)


    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

def autocomplete_productos(request):
    if 'term' in request.GET:
        qs = Productos.objects.filter(nombre__istartswith=request.GET.get('term')).order_by('nombre')
        lista = []
        for x in qs:
            lista.append({'id':x.codigo,
                          'codigo':x.codigo,
                          'label':x.nombre,
                          'value':x.nombre,}
                         )
        return JsonResponse(lista,safe=False)


def agregar_producto_ajax(request):
    if request.method == 'POST':
        if not request.user.has_perms(["mantenimientos.add_productos"]):
            return JsonResponse({'success': False, 'error': 'Sin permisos'}, status=403)

        nombre = request.POST.get('nombre', '').strip()
        if not nombre:
            return JsonResponse({'success': False, 'error': 'Nombre vacío'})

        # Verificamos si ya existe por nombre o código
        producto_existente = Productos.objects.filter(nombre__iexact=nombre).first()
        if producto_existente:
            return JsonResponse({'success': True, 'id': producto_existente.codigo, 'nombre': producto_existente.nombre})

        # Creamos un producto nuevo
        nuevo_producto = Productos(nombre=nombre.upper(), descripcion=nombre.upper())
        nuevo_producto.save()

        return JsonResponse({'success': True, 'id': nuevo_producto.codigo, 'nombre': nuevo_producto.nombre})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)