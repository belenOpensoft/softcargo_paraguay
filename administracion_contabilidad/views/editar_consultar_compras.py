import json
import re

from django.shortcuts import render
from administracion_contabilidad.forms import EditarConsultarCompras, ComprasDetalle, ComprasDetallePago, \
    DetalleEmbarqueForm
from administracion_contabilidad.models import VistaProveedoresygastos, VItemsCompra, Ordenes, Movims, Boleta, Asientos, \
    Cheques, Chequeorden, Impucompras
from django.http import JsonResponse

from expaerea.models import VEmbarqueaereo as ExportConexaerea, ExportCargaaerea, ExportEmbarqueaereo, ExportServiceaereo
from expterrestre.models import VEmbarqueaereo as ExpterraEmbarqueaereo, ExpterraCargaaerea, ExpterraServiceaereo, ExpterraEnvases
from impaerea.models import VEmbarqueaereo as ImportEmbarqueaereo, ImportConexaerea, ImportCargaaerea,ImportServiceaereo
from impomarit.models import VEmbarqueaereo as Embarqueaereo, Cargaaerea, Serviceaereo, Envases
from expmarit.models import VEmbarqueaereo as ExpmaritEmbarqueaereo, ExpmaritCargaaerea, ExpmaritServiceaereo, ExpmaritEnvases
from impterrestre.models import VEmbarqueaereo as ImpterraEmbarqueaereo, ImpterraCargaaerea, ImpterraServiceaereo, ImpterraEnvases
from mantenimientos.models import Monedas,Servicios
from seguimientos.models import VGrillaSeguimientos


def editar_consultar_compras(request):
    form = EditarConsultarCompras(request.GET or None)
    form_compras_detalle = ComprasDetalle(request.GET or None)
    form_compras_detalle_pago = ComprasDetallePago(request.GET or None)
    form_compras_detalle_conocimiento = DetalleEmbarqueForm(request.GET or None)
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
        'compras_detalle_pago':form_compras_detalle_pago,
        'compras_detalle_conocimiento':form_compras_detalle_conocimiento
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

        items = VItemsCompra.objects.filter(autogenerado=autogenerado).exclude(imputacion=2)
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


def buscar_ordenes_por_boleta_old(request):
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
def buscar_ordenes_por_boleta(request):
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
        notas = Impucompras.objects.filter(
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
            'por_imputar': pago.msaldo,
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
                nro=int(nro)
                boleta = Movims.objects.filter(mboleta=nro,mtipo__in=(40,41)).first()
                if boleta is None:
                    return JsonResponse({'boletas': boletas_data})

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
        body_unicode = request.body.decode('utf-8')  # decodifica bytes
        data = json.loads(body_unicode)  # convierte a dict
        autogen = data.get('autogen')
        resultados = []
        autofacs=None
        movims=None
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

def actualizar_campos_movims_old(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            autogen = data.get("autogen")
            tipo = data.get("tipo")

            if not autogen or not tipo:
                return JsonResponse({"success": False, "error": "Faltan parámetros clave."})

            factura = Movims.objects.filter(mautogen=autogen, mnombremov=tipo).first()

            if not factura:
                return JsonResponse({"success": False, "error": "Factura no encontrada."})

            # Asignación individual de campos
            if 'detalle' in data:
                factura.mdetalle = data['detalle']

            if 'fecha' in data:
                factura.mfechamov = (data['fecha'])

            if 'paridad' in data:
                factura.mparidad = float(data['paridad'])

            if 'arbitraje' in data:
                factura.marbitraje = float(data['arbitraje'])

            factura.save()
            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)


def actualizar_campos_movims(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            autogen = data.get("autogen")
            tipo = data.get("tipo")

            if not autogen or not tipo:
                return JsonResponse({"success": False, "error": "Faltan parámetros clave."})

            factura = Movims.objects.filter(mautogen=autogen, mnombremov=tipo).first()

            if not factura:
                return JsonResponse({"success": False, "error": "Factura no encontrada."})

            # Asignación individual de campos
            if 'detalle' in data:
                factura.mdetalle = data['detalle']

            if 'fecha' in data:
                factura.mfechamov = data['fecha']

            if 'paridad' in data:
                factura.mparidad = float(data['paridad'])

            if 'arbitraje' in data:
                factura.marbitraje = float(data['arbitraje'])

            factura.save()

            if 'posiciones' in data:
                for item in data['posiciones']:
                    nroserv = item.get('nroserv')
                    nueva_posicion = item.get('nueva_posicion')

                    if nroserv and nueva_posicion is not None:
                        asientos = Asientos.objects.filter(autogenerado=autogen, nroserv=nroserv)
                        for asiento in asientos:
                            if asiento.posicion != nueva_posicion:
                                asiento.posicion = nueva_posicion
                                asiento.save()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def anular_compra(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            autogen = data.get('autogen')

            if not autogen:
                return JsonResponse({'success': False, 'error': 'Autogenerado no proporcionado'})

            # Eliminar en orden lógico
            impus = Impucompras.objects.filter(autogen=autogen)
            movims = Movims.objects.filter(mautogen=autogen)
            asientos = Asientos.objects.filter(autogenerado=autogen)

            impus_deleted = impus.count()
            # movims_deleted = movims.count()
            asientos_deleted = asientos.count()

            impus.delete()
            for m in movims:
                m.mactivo='N'
                m.save()

            asientos.delete()

            return JsonResponse({
                'success': True,
                'message': 'Factura anulada correctamente',
                'eliminados': {
                    'Impucompras': impus_deleted,
                    'Asientos': asientos_deleted
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

def obtener_datos_embarque_por_posicion(request):
    if request.method == 'GET':
        posicion = request.GET.get('posicion')

        if not  posicion:
            return JsonResponse({'success': False, 'error': 'Posiciones no proporcionadas.'})

        resultados = []


        tipo_operativa = posicion[:2].upper()
        embarque = None
        envases = None
        gastos_raw = None
        gastos=[]
        cargas =None

        try:
            if tipo_operativa == 'IM':
                embarque = Embarqueaereo.objects.filter(posicion=posicion).first()
                cargas = list(Cargaaerea.objects.filter(numero=embarque.numero).values(
                'producto__nombre', 'bultos', 'bruto'
            ))
                gastos_raw = list(Serviceaereo.objects.filter(numero=embarque.numero).values(
                'servicio', 'moneda', 'precio','costo'
            ))
                envases = list(Envases.objects.filter(numero=embarque.numero).values(
                    'unidad', 'tipo', 'movimiento', 'terminos', 'cantidad', 'precio', 'costo', 'nrocontenedor'
                ))
            elif tipo_operativa == 'EM':
                embarque = ExpmaritEmbarqueaereo.objects.filter(posicion=posicion).first()
                cargas = list(ExpmaritCargaaerea.objects.filter(numero=embarque.numero).values(
                'producto__nombre', 'bultos', 'bruto'
            ))
                gastos_raw=list(ExpmaritServiceaereo.objects.filter(numero=embarque.numero).values(
                'servicio', 'moneda', 'precio','costo'
            ))
                envases = list(ExpmaritEnvases.objects.filter(numero=embarque.numero).values(
                    'unidad', 'tipo', 'movimiento', 'terminos', 'cantidad', 'precio', 'costo', 'nrocontenedor'
                ))
            elif tipo_operativa == 'IA':
                embarque = ImportEmbarqueaereo.objects.filter(posicion=posicion).first()
                cargas = list(ImportCargaaerea.objects.filter(numero=embarque.numero).values(
                'producto__nombre', 'bultos', 'bruto'
            ))
                gastos_raw = list(ImportServiceaereo.objects.filter(numero=embarque.numero).values(
                'servicio', 'moneda', 'precio','costo'
            ))
            elif tipo_operativa == 'EA':
                embarque = ExportEmbarqueaereo.objects.filter(posicion=posicion).first()
                cargas = list(ExportCargaaerea.objects.filter(numero=embarque.numero).values(
                'producto__nombre', 'bultos', 'bruto'
            ))
                gastos_raw = list(ExportServiceaereo.objects.filter(numero=embarque.numero).values(
                'servicio', 'moneda', 'precio','costo'
            ))
            elif tipo_operativa == 'IT':
                embarque = ImpterraEmbarqueaereo.objects.filter(posicion=posicion).first()
                cargas = list(ImpterraCargaaerea.objects.filter(numero=embarque.numero).values(
                'producto__nombre', 'bultos', 'bruto'
            ))
                gastos_raw = list(ImpterraServiceaereo.objects.filter(numero=embarque.numero).values(
                'servicio', 'moneda', 'precio','costo'
            ))
                envases = list(ImpterraEnvases.objects.filter(numero=embarque.numero).values(
                    'unidad', 'tipo', 'movimiento', 'terminos', 'cantidad', 'precio', 'costo', 'nrocontenedor'
                ))
            elif tipo_operativa == 'ET':
                embarque = ExpterraEmbarqueaereo.objects.filter(posicion=posicion).first()
                cargas =list(ExpterraCargaaerea.objects.filter(numero=embarque.numero).values(
                'producto__nombre', 'bultos', 'bruto'
            ))
                gastos_raw = list(ExpterraServiceaereo.objects.filter(numero=embarque.numero).values(
                'servicio', 'moneda', 'precio','costo'
            ))
                envases = list(ExpterraEnvases.objects.filter(numero=embarque.numero).values(
                    'unidad', 'tipo', 'movimiento', 'terminos', 'cantidad', 'precio', 'costo', 'nrocontenedor'
                ))
            else:
                resultados.append({
                    'posicion': posicion,
                    'success': False,
                    'error': 'Posición errónea o tipo no reconocido.'
                })

            if not embarque:
                resultados.append({
                    'posicion': posicion,
                    'success': False,
                    'error': 'No se encontró un embarque para esta posición.'
                })

            if embarque.seguimiento:
                seguimiento = VGrillaSeguimientos.objects.get(numero=embarque.seguimiento)
            else:
                seguimiento=None

            conex=None
            if tipo_operativa == 'IA':
                conex = ImportConexaerea.objects.filter(numero=embarque.numero).first()
            elif tipo_operativa == 'EA':
                conex = ExportConexaerea.objects.filter(numero=embarque.numero).first()

            vuelo = conex.vuelo if conex else 'S/I'

            datos = {
                'cliente': seguimiento.cliente if seguimiento else 'S/I',
                'embarcador': embarque.embarcador if embarque.embarcador else '',
                'consignatario': embarque.consignatario if embarque.consignatario else '',
                'agente': embarque.agente if embarque.agente else '',
                'transportista': embarque.transportista if embarque.transportista else '',
                'vapor_vuelo': embarque.vapor if tipo_operativa in ['IM','EM'] else vuelo,
                'etd_eta':seguimiento.eta.strftime("%Y-%m-%d"),
                'embarque': embarque.fecha_embarque.strftime("%Y-%m-%d"),
                'posicion': embarque.posicion,
                'mbl': embarque.awb,
                'hbl': embarque.hawb,
                'origen': embarque.origen,
                'destino': embarque.destino,
            }

            # Procesar gastos con nombres de servicio y moneda
            for g in gastos_raw:
                try:
                    servicio_nombre = Servicios.objects.get(codigo=g['servicio']).nombre if g['servicio'] else 'S/I'
                except Servicios.DoesNotExist:
                    servicio_nombre = 'S/I'
                try:
                    moneda_nombre = Monedas.objects.get(codigo=g['moneda']).nombre if g['moneda'] else 'S/I'
                except Monedas.DoesNotExist:
                    moneda_nombre = 'S/I'

                gastos.append({
                    'servicio': servicio_nombre,
                    'moneda': moneda_nombre,
                    'precio': g['precio'],
                    'costo': g['costo']
                })

            resultados.append({
                'success': True,
                'posicion': posicion,
                'formulario': datos,
                'servicios': gastos,
                'productos': cargas,
                'envases': envases
            })

        except Exception as e:
            resultados.append({
                'posicion': posicion,
                'success': False,
                'error': str(e)
            })

        return JsonResponse({'resultados': resultados})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

