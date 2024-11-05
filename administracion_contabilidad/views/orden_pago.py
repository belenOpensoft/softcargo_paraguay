from django.http import JsonResponse
from django.shortcuts import render
from administracion_contabilidad.forms import OrdenPago
from mantenimientos.models import Clientes
from administracion_contabilidad.models import Asientos


def orden_pago_view(request):
    form = OrdenPago(request.POST or None)
    return render(request, 'orden_pago.html', {'form': form})


def buscar_proveedor(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()  # Obtener y limpiar el término de búsqueda
        proveedores = Clientes.objects.filter(empresa__icontains=query)[:10]  # Limitar resultados a 10
        results = [{'id': proveedor.id, 'text': proveedor.empresa} for proveedor in proveedores]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def buscar_proveedores(request):
    if request.method == "GET":
        proveedor_id = request.GET.get("codigo")
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


def obtener_imputables(request):
    proveedor_id = request.GET.get('codigo')
    asientos = Asientos.objects.filter(cliente=proveedor_id)

    resultados = []
    for registro in asientos:
        resultados.append({
            'id': registro.id,
            'vto': registro.vto.strftime('%Y-%m-%d') if registro.vto else '',
            'fecha_emision': registro.fechaemision.strftime('%Y-%m-%d') if registro.fechaemision else '',
            'documento': registro.documento,
            'monto_total': str(registro.monto),
            'saldo': str(registro.mov),
            'detalle': registro.detalle,
            'embarque': registro.centro,
            'co': registro.cuenta,
            'posicion': registro.posicion,
            'tc': str(registro.cambio),
            'moneda': registro.moneda,
            'paridad': str(registro.paridad),
            'monto_original': str(registro.monto)
        })

    # Estructura de respuesta para DataTable
    response_data = {
        'draw': request.GET.get('draw', 0),  # Para mantener la coherencia con DataTable
        'recordsTotal': asientos.count(),  # Total de registros sin filtros
        'recordsFiltered': asientos.count(),  # Total de registros después del filtrado
        'data': resultados  # Datos que se mostrarán en la tabla
    }

    return JsonResponse(response_data, safe=False)
