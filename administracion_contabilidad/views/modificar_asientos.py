import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from administracion_contabilidad.forms import FiltroAsientosForm, EditarAsientoForm
from administracion_contabilidad.models import Asientos, Cuentas


def filtro_asientos(request):
    form = FiltroAsientosForm(request.GET or None)
    detalle = EditarAsientoForm(request.GET or None)
    resultados = Asientos.objects.none()

    if form.is_valid():
        cd = form.cleaned_data
        filtros = {}

        if not cd['omitir_fechas']:
            if cd['fecha_desde']:
                filtros['fecha__gte'] = cd['fecha_desde']
            if cd['fecha_hasta']:
                filtros['fecha__lte'] = cd['fecha_hasta']

        if cd['cuenta']:
            filtros['cuenta'] = cd['cuenta'].xcodigo

        if cd['detalle']:
            filtros['detalle__icontains'] = cd['detalle']

        if cd['asiento']:
            filtros['asiento'] = cd['asiento']


        resultados = Asientos.objects.filter(**filtros)


    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        datos = [
            {
                'asiento': r.asiento,
                'autogenerado': r.autogenerado,
                'fecha': r.fecha.strftime('%Y-%d-%m') if r.fecha else None,
                'detalle': r.detalle,
                'monto': round(r.monto,2) if r.monto else 0,
                'imputacion': r.imputacion,
                'tipo_cambio': r.cambio if r.cambio else 0,
                'paridad': r.paridad if r.paridad else 0,
                'posicion': r.posicion if r.posicion else 'S/I',
                'moneda': r.moneda,
                'id': r.id,
                'nrocuenta': r.cuenta,
                'cuenta': Cuentas.objects.filter(xcodigo=r.cuenta).first().xnombre if r.cuenta else None,
            } for r in resultados
        ]
        return JsonResponse({'resultados': datos})

    return render(request, 'contabilidad/modificar_asientos.html', {
        'form': form,
        'detalle': detalle,
    })

def guardar_asiento_editado(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data['editar']==True:
                asiento=Asientos.objects.filter(asiento=data['asiento'])
                for a in asiento:
                    if a.tipo!='D':
                        return JsonResponse({"success": False,'error':'No puede editar asientos que no fueron agregados de manera directa.'})
                    if data['cuenta']:
                        a.cuenta = data['cuenta']
                    if data['moneda']:
                        a.moneda=data['moneda']
                    if data['arbitraje']:
                        a.cambio=data['arbitraje']
                    if data['paridad']:
                        a.paridad=data['paridad']
                    if data['detalle']:
                        a.detalle=data['detalle']
                    if data['posicion']:
                        a.posicion=data['posicion']
                    if data['monto']:
                        a.monto=data['monto']

                    a.save()
            else:
                a = Asientos.objects.get(id=data['id'])
                if a.tipo != 'D':
                    return JsonResponse({"success": False,
                                         'error': 'No puede editar asientos que no fueron agregados de manera directa.'})
                if data['cuenta']:
                    a.cuenta = data['cuenta']
                if data['moneda']:
                    a.moneda = data['moneda']
                if data['arbitraje']:
                    a.cambio = data['arbitraje']
                if data['paridad']:
                    a.paridad = data['paridad']
                if data['detalle']:
                    a.detalle = data['detalle']
                if data['posicion']:
                    a.posicion = data['posicion']
                if data['monto']:
                    a.monto = data['monto']

                a.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def eliminar_asiento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data['editar']==True:
                asiento=Asientos.objects.filter(asiento=data['asiento'])
                for a in asiento:
                    if a.tipo!='D':
                        return JsonResponse({"success": False,'error':'No puede eliminar asientos que no fueron agregados de manera directa.'})
                    a.delete()
            else:
                a = Asientos.objects.get(id=data['id'])
                if a.tipo != 'D':
                    return JsonResponse({"success": False,
                                         'error': 'No puede eliminar asientos que no fueron agregados de manera directa.'})
                a.delete()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

@require_GET
def asientos_relacionados(request):
    autogenerado = (request.GET.get('autogenerado') or '').strip()
    exclude_id   = (request.GET.get('exclude_id') or '').strip()

    if not autogenerado:
        return JsonResponse({'data': []})

    qs = Asientos.objects.filter(autogenerado=autogenerado)
    if exclude_id.isdigit():
        qs = qs.exclude(id=int(exclude_id))

    # Si querés limitar a mismo número de asiento, quitá el exclude y filtrá como te convenga.
    # Orden sugerido: por fecha y por id
    qs = qs.order_by('fecha', 'id')

    data = []
    for a in qs:
        # Nombre de cuenta opcional
        cuenta_nombre = None
        if a.cuenta:
            c = Cuentas.objects.filter(xcodigo=a.cuenta).first()
            cuenta_nombre = c.xnombre if c else None

        # Mapeo: asumiendo que 'imputacion' == 1 => Debe, otro => Haber
        debe  = float(a.monto) if getattr(a, 'imputacion', None) == 1 else 0.0
        haber = float(a.monto) if getattr(a, 'imputacion', None) != 1 else 0.0

        data.append({
            'id': a.id,
            'autogenerado': a.autogenerado or '',
            'fecha': a.fecha.strftime('%Y-%m-%d') if a.fecha else '',
            'asiento': a.asiento,
            'cuenta': a.cuenta,
            'cuenta_nombre': cuenta_nombre,
            'detalle': a.detalle or '',
            'debe': debe,
            'haber': haber,
            'moneda': a.moneda or '',
            'posicion': a.posicion or '',
            'paridad': a.paridad or '',
            'arbitraje': a.cambio or '',
            'tipo': 'D' if getattr(a, 'imputacion', None) == 1 else 'H',
        })

    return JsonResponse({'data': data})