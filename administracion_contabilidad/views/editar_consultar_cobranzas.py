import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.datetime_safe import datetime

from administracion_contabilidad.forms import EditarConsultarCobranzas, CobranzasDetalle
from administracion_contabilidad.models import ListaCobranzas, VistaCobranza, Movims, Asientos, Cuentas, Cheques, \
    Impuvtas, Boleta
from mantenimientos.models import Monedas


def editar_consultar_cobranzas(request):
    form = EditarConsultarCobranzas(request.GET or None)
    form_cobranzas_detalle = CobranzasDetalle(request.GET or None)
    resultados = ListaCobranzas.objects.none()

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


        resultados = ListaCobranzas.objects.filter(**filtros)


    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        datos = [
            {
                'documento': r.numero,
                'fecha': r.fecha.strftime('%d/%m/%Y') if r.fecha else '',
                'cliente': r.cliente,
                'importe': float(r.total),
                'autogenerado': r.autogenerado,
                'numero': r.numero,
                'nrocliente': r.nrocliente,
            } for r in resultados
        ]
        return JsonResponse({'resultados': datos})

    return render(request, 'editar_consultar_cobranzas/editar_consultar_cobranzas.html', {
        'form': form,
        'cobranzas_detalle':form_cobranzas_detalle,
    })

def obtener_detalle_cobranza(request):
    autogenerado = request.GET.get('autogenerado')

    if not autogenerado:
        return JsonResponse({'error': 'No se recibió el autogenerado'}, status=400)

    try:
        detalle = Movims.objects.get(mautogen=autogenerado)

        transferencia = deposito = efectivo = diferencia = ''
        data = {
            'numero': detalle.mboleta,
            'moneda': detalle.mmoneda,
            'fecha': detalle.mfechamov.strftime('%Y-%m-%d') if detalle.mfechamov else '',
            'paridad': detalle.mparidad,
            'arbitraje': detalle.marbitraje,
            'cliente': detalle.mnombre,
            'nrocliente': detalle.mcliente,
            'detalle': detalle.mdetalle,
            'total': detalle.mtotal,
            'imputable': detalle.msaldo,
            'transferencia': transferencia,
            'deposito': deposito,
            'efectivo': efectivo,
            'diferencia': diferencia,
            'cheques': [],
            'imputados': []
        }

        # Buscar cheques y movimientos asociados
        asientos = Asientos.objects.filter(autogenerado=autogenerado)
        for asiento in asientos:
            banco = Cuentas.objects.filter(xcodigo=asiento.cuenta).first() if asiento.cuenta else None
            nombre = banco.xnombre if banco else ''
            if asiento.modo == 'TRANSFER':
                if asiento.monto:
                    transferencia += f"{nombre} {asiento.monto:.2f} "
            elif asiento.modo == 'EFECTIVO':
                if asiento.monto:
                    efectivo += f"{nombre} {asiento.monto:.2f} "
            elif asiento.modo == 'DEPOSITO':
                if asiento.monto:
                    deposito += f"{nombre} {asiento.monto:.2f} "
            elif asiento.modo == 'DIFER':
                if asiento.monto:
                    diferencia += f"{nombre} {asiento.monto:.2f} "
            elif asiento.modo == 'CHEQUE':
                cheques = Cheques.objects.filter(corden=detalle.mboleta)
                for cheque in cheques:
                    data['cheques'].append({
                        'fecha': cheque.cfecha.strftime('%Y-%m-%d') if cheque.cfecha else '',
                        'banco': cheque.cbanco,
                        'numero': cheque.cnumero,
                        'monto': cheque.cmonto,
                        'moneda': Monedas.objects.get(codigo=cheque.cmoneda).nombre if cheque.cmoneda else 'S/I',
                        'vencimiento': cheque.cvto.strftime('%Y-%m-%d') if cheque.cvto else '',
                    })

        # Procesar documentos imputados desde el campo detalle
        if detalle.mdetalle:
            boletas_raw = detalle.mdetalle.split(';')
            boletas_nros = [int(b.strip()) for b in boletas_raw if b.strip().isdigit()]
            if boletas_nros:
                for nro in boletas_nros:
                    imputado = Boleta.objects.filter(numero=nro,nrocliente=detalle.mcliente).first()
                    if imputado:
                        num_completo = f"{imputado.tipo}-{imputado.serie}{imputado.prefijo}{imputado.numero}"
                        data['imputados'].append({
                            'autogenerado':imputado.autogenerado,
                            'documento': num_completo,
                            'imputado': imputado.total,
                            'referencia': imputado.seguimiento,
                            'posicion': imputado.posicion,
                        })

        data['transferencia'] = transferencia.strip()
        data['efectivo'] = efectivo.strip()
        data['deposito'] = deposito.strip()
        data['diferencia'] = diferencia.strip()

        return JsonResponse({'success': True, 'data': data})

    except Movims.DoesNotExist:
        return JsonResponse({'error': 'No se encontró el registro'}, status=404)

def cargar_pendientes_imputacion_cobranza(request):
    try:
        nrocliente = request.GET.get('nrocliente', None)

        if not nrocliente:
            return JsonResponse({'error': 'Debe proporcionar un nrocliente'}, status=400)

        registros = Movims.objects.filter(
            mcliente=nrocliente,
            mtipo__in=(20, 21, 22, 24)
        ).exclude(msaldo=0)

        data = []
        for registro in registros:
            data.append({
                'autogenerado': registro.mautogen,
                'vto': registro.mfechamov.strftime('%Y-%m-%d') if registro.mfechamov else '',
                'emision': registro.mfechamov.strftime('%Y-%m-%d') if registro.mfechamov else '',
                'num_completo': str(registro.mserie or '')+str(registro.mprefijo or '')+str(registro.mboleta or ''),
                'total': float(registro.mtotal) if registro.mtotal else 0,
                'saldo': float(registro.msaldo) if registro.msaldo else 0,
                'imputado': 0,
                'tipo_cambio': float(registro.marbitraje) if registro.marbitraje else 0,
                'detalle': registro.mdetalle if registro.mdetalle else '',
            })

        # Retornar los datos en formato JSON sin paginación
        return JsonResponse({'data': data}, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#probar si agrega y elimina imputaciones correctamente
def procesar_imputaciones_cobranza(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            accion = data.get('accion')  # 'guardar' o 'eliminar'

            if accion == 'guardar':
                try:
                    facturas = data.get('facturas', [])
                    autogen = data.get('autogen')
                    cliente = data.get('cliente')  # si lo necesitás guardar
                    saldo_nuevo = data.get('saldo')  # si lo necesitás guardar

                    if not autogen or not isinstance(facturas, list):
                        return JsonResponse({'success': False, 'error': 'Datos incompletos'})

                    for fac in facturas:
                        impuventa = Impuvtas()
                        impuventa.autogen = str(autogen)
                        impuventa.tipo = 2
                        impuventa.cliente = cliente
                        impuventa.monto =  fac.get('monto_imputado')
                        impuventa.autofac = fac.get('autofac')
                        impuventa.fechaimpu = datetime.now().strftime('%Y-%m-%d')
                        impuventa.save()

                        factura = Movims.objects.filter(mautogen=fac.get('autofac')).first()
                        if factura:
                            saldo = float(factura.msaldo) - float(fac.get('monto_imputado'))
                            factura.msaldo= saldo
                            factura.save()

                        cobranza=Movims.objects.filter(mautogen=autogen).first()
                        if cobranza:
                            cobranza.msaldo=saldo_nuevo
                            cobranza.mdetalle=str(cobranza.mdetalle)+str(factura.mboleta)+';'
                            cobranza.save()

                    return JsonResponse({'success': True, 'message': 'Imputaciones guardadas correctamente'})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': e})

            elif accion == 'eliminar':
                autogen = data.get('autogen')
                autofac = data.get('autofac')

                if not autogen or not autofac:
                    return JsonResponse({'success': False, 'error': 'Faltan parámetros para eliminar'})

                eliminado = Impuvtas.objects.filter(autogen=autogen, autofac=autofac).first()
                monto = eliminado.monto
                eliminado.delete()
                factura = Movims.objects.filter(mautogen=autofac).first()
                factura.msaldo=float(factura.msaldo)+float(monto)
                factura.save()
                cobranza = Movims.objects.filter(mautogen=autogen).first()
                if cobranza:
                    cobranza.msaldo = float(cobranza.msaldo)+float(monto)
                    nro_bole = factura.mboleta if factura else None

                    if nro_bole:
                        # Separar el campo mdetalle en lista, filtrar y volver a unir
                        lista_boletas = cobranza.mdetalle.split(';')
                        lista_boletas = [b for b in lista_boletas if b.strip() and b.strip() != str(nro_bole)]
                        cobranza.mdetalle = ';'.join(lista_boletas) + (';' if lista_boletas else '')

                    cobranza.save()

                if eliminado:
                    return JsonResponse({'success': True, 'message': 'Imputación eliminada'})
                else:
                    return JsonResponse({'success': False, 'error': 'No se encontró la imputación'})

            else:
                return JsonResponse({'success': False, 'error': 'Acción no válida'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

def actualizar_campos_movims_cobranza(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            autogen = data.get("autogen")

            if not autogen:
                return JsonResponse({"success": False, "error": "Faltan parámetros clave."})

            factura = Movims.objects.filter(mautogen=autogen).first()

            if not factura:
                return JsonResponse({"success": False, "error": "Cobranza no encontrada."})

            # Asignación de campos editables
            for campo in ['paridad', 'arbitraje']:
                if campo in data:
                    valor = data[campo]
                    if campo in ['paridad', 'arbitraje']:
                        valor = float(valor) if valor else 0
                    setattr(factura, f"m{campo}", valor)

            factura.save()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)
