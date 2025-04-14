import json
import re

from django.http import JsonResponse
from django.shortcuts import render

from administracion_contabilidad.forms import EditarConsultarVentas, VentasDetalle, VentasDetallePago, \
    DetalleEmbarqueForm
from administracion_contabilidad.models import VistaVentas, VItemsVenta, Movims, Impucompras, Impuvtas, Cheques, \
    Asientos
from mantenimientos.models import Monedas


def editar_consultar_ventas(request):
    form = EditarConsultarVentas(request.GET or None)
    form_ventas_detalle = VentasDetalle(request.GET or None)
    form_ventas_detalle_pago = VentasDetallePago(request.GET or None)
    form_ventas_detalle_conocimiento = DetalleEmbarqueForm(request.GET or None)
    resultados = VistaVentas.objects.none()

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

        if cd['cliente_codigo']:
            filtros['nrocliente__icontains'] = cd['cliente_codigo']

        if cd['documento']:
            filtros['num_completo__icontains'] = cd['documento']

        if cd['posicion']:
            filtros['posicion__icontains'] = cd['posicion']

        if cd['tipo']:
            filtros['tipo'] = cd['tipo']

        resultados = VistaVentas.objects.filter(**filtros)

        if cd['estado'] == 'pendientes':
            resultados = resultados.exclude(saldo=0)  # saldo != 0
        elif cd['estado'] == 'cerradas':
            resultados = resultados.filter(saldo=0)



    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        datos = [
            {
                'documento': r.num_completo,
                'fecha': r.fecha.strftime('%d/%m/%Y') if r.fecha else '',
                'cliente': r.cliente,
                'importe': float(r.total),
                'autogenerado': r.autogenerado,
                'numero': r.numero,
                'nrocliente': r.nrocliente,
            } for r in resultados
        ]
        return JsonResponse({'resultados': datos})

    return render(request, 'editar_consultar_ventas/editar_consultar_ventas.html', {
        'form': form,
        'ventas_detalle':form_ventas_detalle,
        'ventas_detalle_pago':form_ventas_detalle_pago,
        'ventas_detalle_conocimiento':form_ventas_detalle_conocimiento
    })

def obtener_detalle_venta(request):
    autogenerado = request.GET.get('autogenerado')

    if not autogenerado:
        return JsonResponse({'error': 'No se recibió el autogenerado'}, status=400)

    try:
        qs = VistaVentas.objects.filter(autogenerado=autogenerado)

        # Intentar primero con registros que tienen 'posicion'
        detalle = qs.exclude(posicion__isnull=True).exclude(posicion='').first()

        # Si no hay ninguno con 'posicion', tomar cualquiera
        if not detalle:
            detalle = qs.first()

        items = VItemsVenta.objects.filter(autogenerado=autogenerado)

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
            'cliente': detalle.cliente,  # Ajustar si es FK
            'nrocliente': detalle.nrocliente,  # Ajustar si es FK
            'detalle': detalle.detalle,
            'total': detalle.total,
            'posicion': detalle.posicion,
            'observaciones': 'sin dato',
            'cae': 'sin dato',
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

    except VistaVentas.DoesNotExist:
        return JsonResponse({'error': 'No se encontró el registro'}, status=404)

def buscar_ordenes_por_boleta_ventas(request):
    numero = request.GET.get('numero')
    cliente = request.GET.get('cliente')
    autogenerado = request.GET.get('autogenerado')

    if not numero or not cliente:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    try:
        regex = r'(^|;)\s*{}(\s*;|$)'.format(re.escape(numero))

        ordenes = Movims.objects.filter(
            mdetalle__regex=regex,
            mcliente=cliente,
            mtipo=45
        )
        movims = Movims.objects.filter(
            mdetalle__regex=regex,
            mcliente=cliente,
            mtipo=25
        )
        notas = Impuvtas.objects.filter(
            autofac=autogenerado
        )

        data = []

        for o in ordenes:
            data.append({
                'autogenerado': o.mautogen,
                'nro_documento': o.mboleta,
                'fecha': o.mfechamov.strftime('%Y-%m-%d') if o.mfechamov else '',
                'monto': o.mtotal,
                'tipo': 'ORDEN PAGO',
            })

        for m in movims:
            data.append({
                'autogenerado': m.mautogen,
                'nro_documento': m.mboleta if hasattr(m, 'mboleta') else '',
                'fecha': m.mfechamov.strftime('%Y-%m-%d') if m.mfechamov else '',
                'monto': m.mtotal,
                'tipo': 'COBRO',
            })

        # Si hay notas, buscar los movims relacionados por autogen
        if notas.exists():
            for nota in notas:
                movims_relacionados = Movims.objects.filter(mautogen=nota.autogen)
                for mv in movims_relacionados:
                    data.append({
                        'autogenerado': mv.mautogen,
                        'nro_documento': mv.mboleta if hasattr(mv, 'mboleta') else '',
                        'fecha': mv.mfechamov.strftime('%Y-%m-%d') if mv.mfechamov else '',
                        'monto': mv.mtotal,
                        'tipo': 'NOTA',
                    })

        return JsonResponse({'resultados': data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def obtener_detalle_pago_ventas(request):
    autogenerado = request.GET.get('autogenerado')
    try:
        pago = Movims.objects.get(mautogen=autogenerado)

        data = {
            'numero': pago.mboleta,
            'moneda': pago.mmoneda,
            'fecha': pago.mfechamov.strftime('%Y-%m-%d'),
            'arbitraje': pago.marbitraje,
            'importe': pago.mtotal,
            'por_imputar': pago.msaldo,
            'paridad': pago.mparidad,
            'proveedor': pago.mnombre,
            'detalle': pago.mdetalle,
            'efectivo_recibido': 'sin datos',
            'status': 'sin datos',
            'cheques': []  # Lista de cheques encontrados
        }

        asiento = Asientos.objects.filter(autogenerado=autogenerado,imputacion=2).values('detalle').first()
        if asiento:
            detalle = asiento['detalle']
            cheques = Cheques.objects.filter(cdetalle=detalle)
            if cheques.exists():
                for cheque in cheques:
                    data['cheques'].append({
                        'fecha': cheque.cfecha.strftime('%Y-%m-%d') if cheque.cfecha else '',
                        'banco': cheque.cbanco,
                        'numero': cheque.cnumero,
                        'monto': cheque.cmonto,
                        'moneda': Monedas.objects.get(codigo=cheque.cmoneda).nombre if cheque.cmoneda is not None else 'S/I',
                        'vencimiento': cheque.cvto.strftime('%Y-%m-%d') if cheque.cvto else '',
                    })

        return JsonResponse(data)

    except Movims.DoesNotExist:
        return JsonResponse({'error': 'No se encontró el registro'}, status=404)

def obtener_imputados_orden_venta(request):
    try:
        body = json.loads(request.body)
        boletas_nros = body.get('boletas', [])

        boletas_data = []
        for nro in boletas_nros:
            try:
                nro=int(nro)
                boleta = Movims.objects.filter(mboleta=nro,mtipo__in=(20,22,21,23,24)).first()
                num_completo=str(boleta.mnombremov)+'-'+str(boleta.mserie)+str(boleta.mprefijo)+str(boleta.mboleta)
                boletas_data.append({
                    'documento':num_completo ,
                    'imputado': boleta.mtotal,
                    'moneda': Monedas.objects.get(codigo=boleta.mmoneda).nombre if boleta.mmoneda is not None else 'S/I',
                    'detalle': boleta.mdetalle,
                })
            except Movims.DoesNotExist:
                continue

        return JsonResponse({'boletas': boletas_data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

"""


{% include 'impucompra_nota.html' %} """