from django.shortcuts import render
from mantenimientos.models import Clientes, Servicios
from administracion_contabilidad.forms import ProveedoresGastos
from django.http import JsonResponse


def proveedores_gastos_view(request):
    form = ProveedoresGastos(request.POST or None)

    return render(request, 'proveedores_gastos.html', {'form': form})


def buscar_proveedor(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()  # Obtener y limpiar el término de búsqueda
        proveedores = Clientes.objects.filter(empresa__icontains=query)[:10]  # Limitar resultados a 10
        results = [{'id': proveedor.id, 'text': proveedor.empresa} for proveedor in proveedores]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def buscar_proveedores(request):
    if request.method == "GET":
        proveedor_id = request.GET.get("id")
        proveedor = Clientes.objects.filter(id=proveedor_id).first()

        if proveedor:
            data = {
                'codigo': proveedor.codigo,
                'empresa': proveedor.empresa,
                'ruc': proveedor.ruc,
                'direccion': proveedor.direccion,
                'localidad': proveedor.localidad,
                'telefono': proveedor.telefono,
            }
            return JsonResponse(data)

    return JsonResponse({'error': 'Cliente no encontrado'}, status=404)


def buscar_item_c(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()
        servicios = Servicios.objects.filter(nombre__icontains=query, tipogasto='C')[:10]
        results = [{'id': servicio.id, 'text': servicio.nombre} for servicio in servicios]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def buscar_items_c(request):
    if request.method == "GET":
        servicio_id = request.GET.get("id")
        servicio = Servicios.objects.filter(id=servicio_id, tipogasto='C').first()

        if servicio:
            iva_texto = "Exento" if servicio.tasa == "X" else "Básico" if servicio.tasa == "B" else "Desconocido"
            embarque_texto = "Pendiente" if servicio.imputar == "S" else "No imputar" if servicio.imputar == "N" else "Desconocido"

            data = {
                'item': servicio.codigo,
                'nombre': servicio.nombre,
                'iva': iva_texto,
                'cuenta': servicio.contable,
                'embarque': embarque_texto,
                'comp': servicio.activa,
                'gasto': servicio.modo,
            }
            return JsonResponse(data)

    return JsonResponse({'error': 'Servicio no encontrado'}, status=404)
