from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from administracion_contabilidad.forms import EditarConsultarCompras
from administracion_contabilidad.models import VistaProveedoresygastos


from django.http import JsonResponse
from django.forms.models import model_to_dict

def editar_consultar_compras(request):
    form = EditarConsultarCompras(request.GET or None)
    resultados = VistaProveedoresygastos.objects.all()

    if form.is_valid():
        cd = form.cleaned_data

        if not cd['omitir_fechas']:
            if cd['fecha_desde']:
                resultados = resultados.filter(fecha__gte=cd['fecha_desde'])
            if cd['fecha_hasta']:
                resultados = resultados.filter(fecha__lte=cd['fecha_hasta'])

        if cd['monedas']:
            resultados = resultados.filter(moneda=cd['monedas'])

        if cd['monto']:
            resultados = resultados.filter(monto__gte=cd['monto'])

        if cd['proveedor']:
            resultados = resultados.filter(proveedor__icontains=cd['proveedor'])

        if cd['documento']:
            resultados = resultados.filter(documento__icontains=cd['documento'])

        if cd['posicion']:
            resultados = resultados.filter(posicion__icontains=cd['posicion'])

        if cd['tipo']:
            resultados = resultados.filter(tipo=cd['tipo'])

        if cd['estado'] == 'pendientes':
            resultados = resultados.filter(estado='pendiente')
        elif cd['estado'] == 'cerradas':
            resultados = resultados.filter(estado='cerrado')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        datos = [
            {
                'documento': r.documento,
                'fecha': r.fecha.strftime('%d/%m/%Y') if r.fecha else '',
                'proveedor': r.proveedor,
                'importe': float(r.importe),
                'autogenerado': r.autogenerado,
            } for r in resultados
        ]
        return JsonResponse({'resultados': datos})

    return render(request, 'editar_consultar_compras.html', {
        'form': form,
        'resultados': resultados,
    })

