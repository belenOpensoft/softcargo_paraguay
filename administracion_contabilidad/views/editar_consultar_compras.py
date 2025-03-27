from django.shortcuts import render
from administracion_contabilidad.forms import EditarConsultarCompras
from administracion_contabilidad.models import VistaProveedoresygastos
from django.http import JsonResponse

def editar_consultar_compras(request):
    form = EditarConsultarCompras(request.GET or None)
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

        if cd['proveedor']:
            filtros['nrocliente__icontains'] = cd['proveedor']

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
                'importe': float(r.monto),
                'autogenerado': r.autogenerado,
            } for r in resultados
        ]
        return JsonResponse({'resultados': datos})

    return render(request, 'editar_consultar_compras.html', {
        'form': form,
    })

