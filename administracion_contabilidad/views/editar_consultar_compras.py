import re

from django.shortcuts import render
from administracion_contabilidad.forms import EditarConsultarCompras, ComprasDetalle
from administracion_contabilidad.models import VistaProveedoresygastos, VItemsCompra, Ordenes, Movims
from django.http import JsonResponse

def editar_consultar_compras(request):
    form = EditarConsultarCompras(request.GET or None)
    form_compras_detalle = ComprasDetalle(request.GET or None)
    resultados = VistaProveedoresygastos.objects.none()  # Valor por defecto

    if form.is_valid():
        cd = form.cleaned_data
        filtros = {}

        if not cd['omitir_fechas']:
            if cd['fecha_desde']:
                filtros['fecha__gte'] = cd['fecha_desde']
            if cd['fecha_hasta']:
                filtros['fecha__lte'] = cd['fecha_hasta']

        if cd['monedas']:
            filtros['moneda'] = cd['monedas']

        if cd['monto']:
            filtros['monto__gte'] = cd['monto']

        if cd['proveedor_codigo']:
            filtros['nrocliente__icontains'] = cd['proveedor_codigo']

        if cd['documento']:
            filtros['num_completo__icontains'] = cd['documento']

        if cd['posicion']:
            filtros['posicion__icontains'] = cd['posicion']

        if cd['tipo']:
            filtros['tipo'] = cd['tipo']

        resultados = VistaProveedoresygastos.objects.filter(**filtros)

        if cd['estado'] == 'pendientes':
            resultados = resultados.exclude(saldo=0)  # saldo != 0
        elif cd['estado'] == 'cerradas':
            resultados = resultados.filter(saldo=0)



    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        datos = [
            {
                'documento': r.num_completo,
                'fecha': r.fecha.strftime('%d/%m/%Y') if r.fecha else '',
                'proveedor': r.cliente,
                'importe': float(r.total),
                'autogenerado': r.autogenerado,
                'numero': r.numero,
                'nrocliente': r.nrocliente,
            } for r in resultados
        ]
        return JsonResponse({'resultados': datos})

    return render(request, 'editar_consultar_compras/editar_consultar_compras.html', {
        'form': form,
        'compras_detalle':form_compras_detalle
    })

def obtener_detalle_compra(request):
    autogenerado = request.GET.get('autogenerado')

    if not autogenerado:
        return JsonResponse({'error': 'No se recibió el autogenerado'}, status=400)

    try:
        qs = VistaProveedoresygastos.objects.filter(autogenerado=autogenerado)

        # Intentar primero con registros que tienen 'posicion'
        detalle = qs.exclude(posicion__isnull=True).exclude(posicion='').first()

        # Si no hay ninguno con 'posicion', tomar cualquiera
        if not detalle:
            detalle = qs.first()

        items = VItemsCompra.objects.filter(autogenerado=autogenerado)
        imputable_total = sum(
            (item.precio or 0) + (item.iva or 0)
            for item in items
            if item.imputar == 'S'
        )

        data = {
            'numero': detalle.numero,
            'prefijo': detalle.prefijo,
            'serie': detalle.serie,
            'tipo': detalle.tipo,
            'moneda': detalle.moneda,  # Ajustar si es ForeignKey: detalle.moneda.nombre
            'fecha': detalle.fecha.strftime('%Y-%m-%d') if detalle.fecha else '',
            'fecha_ingreso': detalle.fecha_ingreso.strftime('%Y-%m-%d') if detalle.fecha_ingreso else '',
            'fecha_vencimiento': detalle.fecha_vencimiento.strftime('%Y-%m-%d') if detalle.fecha_vencimiento else '',
            'paridad': detalle.paridad,
            'arbitraje': detalle.tipo_cambio,
            'proveedor': detalle.cliente,  # Ajustar si es FK
            'detalle': detalle.detalle,
            'total': detalle.total,
            'imputable':imputable_total,
            'items': [
                {
                    'concepto': item.concepto,
                    'nombre': item.nombre,
                    'precio': item.precio,
                    'iva': item.iva,
                    'embarque': (
                        item.posicion if item.imputar == 'S' and item.posicion
                        else 'PENDIENTE' if item.imputar == 'S'
                        else 'NO IMPUTABLE'
                    ),
                    'posicion': (
                        item.posicion if item.imputar == 'S' and item.posicion
                        else 'PENDIENTE' if item.imputar == 'S'
                        else 'NO IMPUTABLE'
                    )
                } for item in items

            ]

        }

        return JsonResponse({'success': True, 'data': data})

    except VistaProveedoresygastos.DoesNotExist:
        return JsonResponse({'error': 'No se encontró el registro'}, status=404)


def buscar_ordenes_por_boleta(request):
    numero = request.GET.get('numero')
    cliente = request.GET.get('cliente')

    if not numero or not cliente:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    try:
        # Expresión regular: busca número exacto entre delimitadores
        regex = r'(^|;)\s*{}(\s*;|$)'.format(re.escape(numero))

        # Buscar en Ordenes
        ordenes = Movims.objects.filter(
            mdetalle__regex=regex,
            mcliente=cliente,
            mtipo=45
        )

        # Buscar en Movims (mtipo=25)
        movims = Movims.objects.filter(
            mdetalle__regex=regex,
            mcliente=cliente,
            mtipo=25
        )

        # Armar la lista combinada
        data = []

        for o in ordenes:
            data.append({
                'nro_documento': o.mboleta,
                'fecha': o.mfechamov.strftime('%Y-%m-%d') if o.mfechamov else '',
                'monto': o.mtotal,
                'tipo': 'ORDEN PAGO',
            })

        for m in movims:
            data.append({
                'nro_documento': m.mboleta if hasattr(m, 'mboleta') else '',
                'fecha': m.mfechamov.strftime('%Y-%m-%d') if m.mfechamov else '',
                'monto': m.mtotal,
                'tipo': 'COBRO',
            })

        return JsonResponse({'resultados': data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)