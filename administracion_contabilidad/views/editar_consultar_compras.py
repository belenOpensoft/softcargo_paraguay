import json
import re

from django.shortcuts import render
from administracion_contabilidad.forms import EditarConsultarCompras, ComprasDetalle, ComprasDetallePago
from administracion_contabilidad.models import VistaProveedoresygastos, VItemsCompra, Ordenes, Movims, Boleta, Asientos, \
    Cheques, Chequeorden, Impucompras
from django.http import JsonResponse

from mantenimientos.models import Monedas


def editar_consultar_compras(request):
    form = EditarConsultarCompras(request.GET or None)
    form_compras_detalle = ComprasDetalle(request.GET or None)
    form_compras_detalle_pago = ComprasDetallePago(request.GET or None)
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
        'compras_detalle':form_compras_detalle,
        'compras_detalle_pago':form_compras_detalle_pago
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
            'nroproveedor': detalle.nrocliente,  # Ajustar si es FK
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

        return JsonResponse({'resultados': data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def obtener_detalle_pago_old(request):
    autogenerado = request.GET.get('autogenerado')
    try:
        pago = Movims.objects.get(mautogen=autogenerado)

        data = {
            'numero': pago.mboleta,
            'moneda': pago.mmoneda,
            'fecha': pago.mfechamov.strftime('%Y-%m-%d'),
            'arbitraje': pago.marbitraje,
            'importe': pago.mtotal,
            'por_imputar': 0,
            'paridad': pago.mparidad,
            'proveedor': pago.mnombre,
            'detalle': pago.mdetalle,
        }
        return JsonResponse(data)

    except Movims.DoesNotExist:
        return JsonResponse({'error': 'No se encontró el registro'}, status=404)

def obtener_detalle_pago(request):
    autogenerado = request.GET.get('autogenerado')
    try:
        pago = Movims.objects.get(mautogen=autogenerado)

        data = {
            'numero': pago.mboleta,
            'moneda': pago.mmoneda,
            'fecha': pago.mfechamov.strftime('%Y-%m-%d'),
            'arbitraje': pago.marbitraje,
            'importe': pago.mtotal,
            'por_imputar': 0,
            'paridad': pago.mparidad,
            'proveedor': pago.mnombre,
            'detalle': pago.mdetalle,
            'cheques': []  # Lista de cheques encontrados
        }

        cheques = Chequeorden.objects.filter(corden=pago.mboleta)
        if cheques.count()>0:
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


def obtener_imputados_orden_compra(request):
    try:
        body = json.loads(request.body)
        boletas_nros = body.get('boletas', [])

        boletas_data = []
        for nro in boletas_nros:
            try:
                boleta = Movims.objects.filter(mboleta=nro,mtipo__in=(40,41)).first()
                num_completo=str(boleta.mnombremov)+'-'+str(boleta.mserie)+str(boleta.mprefijo)+str(boleta.mboleta)
                boletas_data.append({
                    'documento':num_completo ,
                    'imputado': boleta.mtotal,
                    'moneda': Monedas.objects.get(codigo=boleta.mmoneda).nombre if boleta.mmoneda is not None else 'S/I',
                    'detalle': boleta.mdetalle,
                })
            except Boleta.DoesNotExist:
                continue

        return JsonResponse({'boletas': boletas_data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def obtener_imputados_compra(request):
    try:
        body = json.loads(request.body)
        autogen = body.get('autogen')
        resultados = []
        if not autogen:
            return JsonResponse({'error': 'Falta el campo autogen'}, status=400)

        # Buscar los registros en Impucompras con ese autogen
        imputaciones = Impucompras.objects.filter(autogen=autogen)

        if imputaciones.exists():
            # Obtener todos los valores de autofac relacionados
            autofacs = imputaciones.values_list('autofac', flat=True)

            # Buscar en Movims por esos mautogen (autofac)
        if autofacs:

            movims = Movims.objects.filter(mautogen__in=autofacs)

        if movims:
            for mov in movims:
                documento = f"{mov.mserie}{mov.mprefijo}{mov.mboleta}"
                resultados.append({
                    'autogenerado':mov.mautogen,
                    'documento': documento,
                    'imputado': mov.mtotal,
                })

        return JsonResponse({'documentos': resultados})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def procesar_imputaciones_compra(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            accion = data.get('accion')  # 'guardar' o 'eliminar'

            if accion == 'guardar':
                try:
                    facturas = data.get('facturas', [])
                    autogen = data.get('autogen')
                    cliente = data.get('cliente')  # si lo necesitás guardar

                    if not autogen or not isinstance(facturas, list):
                        return JsonResponse({'success': False, 'error': 'Datos incompletos'})

                    for fac in facturas:
                        impuc = Impucompras()
                        impuc.autogen = str(autogen)
                        impuc.cliente = cliente
                        impuc.monto = fac.get('monto_imputado')
                        impuc.autofac = fac.get('autofac')
                        impuc.save()

                        factura = Movims.objects.filter(mautogen=fac.get('autofac'),mtipo=40).first()
                        if factura:
                            saldo = float(factura.msaldo) - float(fac.get('monto_imputado'))
                            factura.msaldo= saldo
                            factura.save()

                        nota=Movims.objects.filter(mautogen=autogen,mtipo=41).first()
                        if nota:
                            nota.msaldo=float(nota.msaldo)-float(fac.get('monto_imputado'))
                            nota.save()

                    return JsonResponse({'success': True, 'message': 'Imputaciones guardadas correctamente'})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': e})

            elif accion == 'eliminar':
                autogen = data.get('autogen')
                autofac = data.get('autofac')

                if not autogen or not autofac:
                    return JsonResponse({'success': False, 'error': 'Faltan parámetros para eliminar'})

                eliminado = Impucompras.objects.get(autogen=autogen, autofac=autofac)
                monto = eliminado.monto
                eliminado.delete()
                factura = Movims.objects.filter(mautogen=autofac, mtipo=40).first()
                factura.msaldo=float(factura.msaldo)+float(monto)
                factura.save()
                nota = Movims.objects.filter(mautogen=autogen, mtpo=41).first()
                if nota:
                    nota.msaldo = float(nota.msaldo)+float(monto)
                    nota.save()

                if eliminado:
                    return JsonResponse({'success': True, 'message': 'Imputación eliminada'})
                else:
                    return JsonResponse({'success': False, 'error': 'No se encontró la imputación'})

            else:
                return JsonResponse({'success': False, 'error': 'Acción no válida'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)