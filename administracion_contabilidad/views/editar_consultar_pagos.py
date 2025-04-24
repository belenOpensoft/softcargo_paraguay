from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from administracion_contabilidad.forms import EditarConsultarPagos, PagosDetalle
from administracion_contabilidad.models import VistaOrdenesPago


def editar_consultar_pagos(request):
    form = EditarConsultarPagos(request.GET or None)
    form_pagos_detalle = PagosDetalle(request.GET or None)
    resultados = VistaOrdenesPago.objects.none()

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

        resultados = VistaOrdenesPago.objects.filter(**filtros)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        datos = [
            {
                'documento': r.numero,
                'fecha': r.fecha.strftime('%d/%m/%Y') if r.fecha else '',
                'proveedor': r.cliente,
                'importe': float(r.total),
                'autogenerado': r.autogenerado,
                'numero': r.numero,
                'nroproveedor': r.nrocliente,
            } for r in resultados
        ]
        return JsonResponse({'resultados': datos})

    return render(request, 'editar_consultar_pagos/editar_consultar_pagos.html', {
        'form': form,
        'pagos_detalle': form_pagos_detalle,
    })