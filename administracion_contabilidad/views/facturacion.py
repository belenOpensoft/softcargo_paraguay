from django.shortcuts import render
from mantenimientos.models import Clientes, Servicios
from administracion_contabilidad.forms import Factura
from administracion_contabilidad.models import Boleta
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Max


def facturacion_view(request):
    form = Factura(request.POST or None)

    return render(request, 'facturacion.html', {'form': form})


def buscar_cliente(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()  # Obtener y limpiar el término de búsqueda
        clientes = Clientes.objects.filter(empresa__icontains=query)[:10]  # Limitar resultados a 10
        results = [{'id': cliente.id, 'text': cliente.empresa} for cliente in clientes]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def buscar_clientes(request):
    if request.method == "GET":
        cliente_id = request.GET.get("id")
        cliente = Clientes.objects.filter(id=cliente_id).first()

        if cliente:
            data = {
                'codigo': cliente.codigo,
                'empresa': cliente.empresa,
                'ruc': cliente.ruc,
                'direccion': cliente.direccion,
                'localidad': cliente.localidad,
                'telefono': cliente.telefono,
            }
            return JsonResponse(data)

    return JsonResponse({'error': 'Cliente no encontrado'}, status=404)


def buscar_item(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()
        tipo_gasto = request.GET.get('tipo_gasto', '')

        servicios = Servicios.objects.filter(
            nombre__icontains=query,
            tipogasto=tipo_gasto
        )[:10]

        results = [{'id': servicio.id, 'text': servicio.nombre} for servicio in servicios]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def buscar_items(request):
    if request.method == "GET":
        servicio_id = request.GET.get("id")
        servicio = Servicios.objects.filter(id=servicio_id).first()

        if servicio:
            iva_texto = "Exento" if servicio.tasa == "X" else "Básico" if servicio.tasa == "B" else "Desconocido"

            data = {
                'item': servicio.codigo,
                'nombre': servicio.nombre,
                'iva': iva_texto,
                'cuenta': servicio.contable,
            }
            return JsonResponse(data)

    return JsonResponse({'error': 'Servicio no encontrado'}, status=404)


def generar_autogenerado():
    ahora = datetime.now()
    fecha_hora = ahora.strftime('%Y%m%d%H%M%S%f')[:-3]
    ultimo = Boleta.objects.aggregate(Max('autogenerado'))['autogenerado__max']
    secuencia_actual = int(ultimo[-10:])
    nuevo_numero = secuencia_actual + 1
    autogenerado = f"{fecha_hora}{nuevo_numero}"

    return autogenerado


def procesar_factura(request):
    if request.method == 'POST':
        serie = request.POST.get('serie')
        prefijo = request.POST.get('prefijo')
        numero = request.POST.get('numero')
        fecha = request.POST.get('fecha')
        moneda = request.POST.get('moneda')
        arbitraje = request.POST.get('arbitraje')
        paridad = request.POST.get('paridad')
        imputar = request.POST.get('imputar')
        cliente_id = request.POST.get('cliente')

        items_data = json.loads(request.POST.get('items'))  # Convertir JSON a diccionario Python

        for item_data in items_data:
            ItemFactura.objects.create(
                factura=factura,
                item=item_data['codigo'],
                descripcion=item_data['descripcion'],
                precio=item_data['precio'],
                iva=item_data['iva'],
                cuenta=item_data['cuenta']
            )

        return JsonResponse({'status': 'success', 'message': 'Factura procesada correctamente'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
