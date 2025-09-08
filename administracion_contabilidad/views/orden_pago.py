import json
import os
from collections import defaultdict
from datetime import datetime
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import length
from num2words import num2words
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from administracion_contabilidad.forms import OrdenPago, PagosDetalleTabla
from administracion_contabilidad.views.facturacion import generar_numero, modificar_numero
from administracion_contabilidad.views.preventa import generar_autogenerado
from cargosystem import settings
from mantenimientos.models import Clientes, Monedas
from administracion_contabilidad.models import Asientos, VistaPagos, Dolar, Cheques, Impuordenes, Ordenes, Cuentas, \
    Movims, Chequeorden, VistaOrdenesPago, Chequeras


@login_required(login_url='/login')
def orden_pago_view(request):
    #if request.user.has_perms(["administracion_contabilidad.view_vistapagos", ]):
    #if request.user.has_perms(["administracion_contabilidad.view_forzarerror", ]):
    form = OrdenPago(initial={'fecha':datetime.now().strftime('%Y-%m-%d')})
    detalle = PagosDetalleTabla()
    return render(request, 'orden_pago.html', {'form': form,'detalle':detalle})
    #else:
     #   messages.error(request,'Funcionalidad en construcción.')
      #  return HttpResponseRedirect('/')

param_busqueda = {
    1: 'autogenerado__icontains',
    2: 'fecha__icontains',
    3: 'num_completo__icontains',
    4: 'cliente__icontains',
    5: 'posicion__icontains',
    6: 'monto__icontains',
    7: 'iva__icontains',
    8: 'total__icontains',
}

columns_table = {
    0:'vacia',
    1: 'autogenerado',
    2: 'fecha',
    3: 'num_completo',
    4: 'cliente',
    5: 'posicion',
    6: 'monto',
    7: 'iva',
    8: 'total',
}

def source_ordenes(request):
    try:
        args = {}
        for i in range(10):  # Ajustar si tenés más o menos columnas
            key = f'columns[{i}][search][value]'
            args[str(i)] = request.GET.get(key, '')

        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        buscar = request.GET.get('buscar', '')
        que_buscar = request.GET.get('que_buscar', '')
        order = get_order(request, columns_table)

        if buscar:
            filtro[que_buscar] = buscar

        end = start + length

        if filtro:
            registros = VistaOrdenesPago.objects.filter(**filtro).order_by(*order)
        else:
            registros = VistaOrdenesPago.objects.all().order_by(*order)

        resultado = {
            'data': get_data(registros[start:end]),
            'length': length,
            'draw': request.GET.get('draw', '1'),
            'recordsTotal': Movims.objects.filter(mtipo=45).count(),
            'recordsFiltered': registros.count(),
        }

        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_data(registros_filtrados):
    try:
        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str('O/PAGO'))
            registro_json.append('' if registro.autogenerado is None else str(registro.autogenerado))
            registro_json.append('' if registro.fecha is None else registro.fecha.strftime('%Y-%m-%d'))
            registro_json.append('' if registro.num_completo is None else str(registro.num_completo))
            registro_json.append('' if registro.cliente is None else str(registro.cliente))
            registro_json.append('' if registro.posicion is None else str(registro.posicion))
            registro_json.append('' if registro.monto is None else str(registro.monto))
            registro_json.append('' if registro.iva is None else str(registro.iva))
            registro_json.append('' if registro.total is None else str(registro.total))
            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)

def get_order(request, columns):
    try:
        result = []
        order_column = request.GET['order[0][column]']
        order_dir = request.GET['order[0][dir]']
        order = columns[int(order_column)]
        if order_dir == 'desc':
            order = '-' + columns[int(order_column)]
        result.append(order)
        i = 1
        while i > 0:
            try:
                order_column = request.GET['order[' + str(i) + '][column]']
                order_dir = request.GET['order[' + str(i) + '][dir]']
                order = columns[int(order_column)]
                if order_dir == 'desc':
                    order = '-' + columns[int(order_column)]
                result.append(order)
                i += 1
            except Exception as e:
                i = 0
        return result
    except Exception as e:
        raise TypeError(e)

def get_argumentos_busqueda(**kwargs):
    try:
        result = {}
        for row in kwargs:
            if len(kwargs[row]) > 0:
                result[param_busqueda[int(row)]] = kwargs[row]
        return result
    except Exception as e:
        raise TypeError(e)

def buscar_proveedor(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()  # Obtener y limpiar el término de búsqueda
        proveedores = Clientes.objects.filter(empresa__icontains=query)[:10]  # Limitar resultados a 10
        results = [{'id': proveedor.id, 'text': proveedor.empresa,'codigo': proveedor.codigo,} for proveedor in proveedores]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)

def buscar_proveedor_old(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()  # Obtener y limpiar el término de búsqueda
        proveedores = Clientes.objects.filter(empresa__icontains=query)[:10]  # Limitar resultados a 10
        results = [{'id': proveedor.id, 'text': proveedor.empresa} for proveedor in proveedores]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)

def buscar_proveedores(request):
    if request.method == "GET":
        proveedor_id = request.GET.get("codigo")
        proveedor = Clientes.objects.filter(codigo=proveedor_id).first()

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


def obtener_imputables_old_(request):
    proveedor_id = request.GET.get('codigo')

    # Obtener los parámetros de paginación
    start = int(request.GET.get('start', 0))  # Inicio de la página (offset)
    length = int(request.GET.get('length', 5))  # Número de registros por página
    # Filtrar los registros según el proveedor
    registros_totales = VistaPagos.objects.filter(nrocliente=proveedor_id)

    filtrados=[]
    for r in registros_totales:
        if r.tipo_factura!='anticipo':
            saldo = r.total - r.pago if r.pago is not None else r.total
            if saldo <0:
                saldo='error'
        else:
            saldo = -r.saldo

        pago = r.pago if r.pago is not None else 0
        if pago != r.total and saldo !='error':
            try:
                moneda_nombre = Monedas.objects.get(codigo=r.moneda).nombre if r.moneda in [1, 2, 3, 4, 5,6] else ''
            except Monedas.DoesNotExist:
                moneda_nombre = ''

            filtrados.append({
                'autogenerado': r.autogenerado,
                'fecha': r.fecha.strftime('%Y-%m-%d') if r.fecha else '',
                'documento': r.documento,
                'total': r.total,
                'monto': r.monto,
                'iva': r.iva,
                'tipo': r.tipo_factura,
                'moneda': moneda_nombre,
                'saldo': saldo,
                'imputado': 0
            })

    # Aplicar la paginación: [start:start+length] para obtener solo los registros de la página solicitada
    registros = filtrados[start:start + length]


    # Estructura de respuesta para DataTable
    response_data = {
        'draw': request.GET.get('draw', 0),  # Para mantener la coherencia con DataTable
        'recordsTotal': registros_totales.count(),  # Total de registros sin filtros
        'recordsFiltered': len(filtrados),
        # Total de registros después del filtrado (aplica el filtro de 'nrocliente')
        'data': registros  # Datos que se mostrarán en la tabla
    }

    return JsonResponse(response_data, safe=False)


def obtener_imputables(request):
    proveedor_id = request.GET.get('codigo')
    moneda_objetivo = request.GET.get('moneda')
    # Obtener los parámetros de paginación
    start = int(request.GET.get('start', 0))  # Inicio de la página (offset)
    length = int(request.GET.get('length', 5))  # Número de registros por página
    # Filtrar los registros según el proveedor
    registros_totales = Movims.objects.filter(mcliente=proveedor_id,mactivo='S').exclude(msaldo=0)

    filtrados=[]
    for r in registros_totales:

        # try:
        #     # moneda_nombre = Monedas.objects.get(codigo=r.mmoneda).nombre if r.mmoneda in [1, 2, 3, 4, 5,6] else ''
        #     moneda_nombre = Monedas.objects.get(codigo=moneda_objetivo).nombre
        # except Monedas.DoesNotExist:
        #     moneda_nombre = ''

        total = float(r.mtotal or 0)
        saldo = float(r.msaldo or 0)

        arbitraje = float(r.marbitraje or 0)
        paridad = float(r.mparidad or 0)

        try:

            if arbitraje != 0:
                total_convertido = convertir_monto(total, int(r.mmoneda or 0), int(moneda_objetivo or 0),
                                                   arbitraje, paridad)
                saldo_convertido = convertir_monto(saldo, int(r.mmoneda or 0), int(moneda_objetivo or 0),
                                                   arbitraje, paridad)
                moneda_nombre = Monedas.objects.get(codigo=moneda_objetivo).nombre
            else:
                total_convertido = total
                saldo_convertido = saldo
                moneda_nombre = Monedas.objects.get(codigo=r.mmoneda).nombre

        except ObjectDoesNotExist:
            moneda_nombre = "Desconocida"

        nro_completo = ""
        if r.mserie and r.mprefijo and r.mboleta:
            s = str(r.mserie)
            p = str(r.mprefijo)

            tz = len(s) - len(s.rstrip('0'))
            lz = len(p) - len(p.lstrip('0'))

            sep = '0' * max(0, 3 - (tz + lz))

            nro_completo = f"{s}{sep}{p}-{r.mboleta}"

        source = 'VERDE' if r.mtipo in [20,21,23,24,25] else 'AZUL'

        # total_convertido = convertir_monto(total, int(r.mmoneda or 0), int(moneda_objetivo or 0), arbitraje, paridad)
        # saldo_convertido = convertir_monto(saldo, int(r.mmoneda or 0), int(moneda_objetivo or 0), arbitraje, paridad)

        total_convertido = total_convertido if r.mtipo in [40, 45, 21, 23] else - total_convertido
        saldo_convertido = saldo_convertido if r.mtipo in [40, 45, 21, 23] else - saldo_convertido

        filtrados.append({
            'autogenerado': r.mautogen,
            'fecha': r.mfechamov.strftime('%Y-%d-%m') if r.mfechamov else None,
            'documento': nro_completo,
            'total': total_convertido,
            'monto': r.mmonto,
            'iva': r.miva,
            'tipo': r.mnombremov,
            'moneda': moneda_nombre,
            'saldo': saldo_convertido,
            'imputado': 0,
            'arbitraje': arbitraje,
            'paridad': paridad,
            'source': source,
        })

    registros = filtrados[start:start + length]


    # Estructura de respuesta para DataTable
    response_data = {
        'draw': request.GET.get('draw', 0),
        'recordsTotal': registros_totales.count(),
        'recordsFiltered': len(filtrados),
        'data': registros
    }

    return JsonResponse(response_data, safe=False)

def obtener_imputables_old(request):
    proveedor_id = request.GET.get('codigo')
    moneda_objetivo = request.GET.get('moneda')
    # Obtener los parámetros de paginación
    start = int(request.GET.get('start', 0))  # Inicio de la página (offset)
    length = int(request.GET.get('length', 5))  # Número de registros por página
    # Filtrar los registros según el proveedor
    registros_totales = VistaPagos.objects.filter(nrocliente=proveedor_id)

    filtrados=[]
    for r in registros_totales:

        try:
            moneda_nombre = Monedas.objects.get(codigo=r.moneda).nombre if r.moneda in [1, 2, 3, 4, 5,6] else ''
        except Monedas.DoesNotExist:
            moneda_nombre = ''

        try:
            arbitraje, paridad = Movims.objects.filter(mautogen=r.autogenerado).values_list('mcambio','mparidad').first() or (0,0)
        except Exception:
            arbitraje, paridad = 0, 0

        total = float(r.total or 0)
        saldo = float(r.saldo or 0)

        arbitraje = float(arbitraje) if arbitraje else 0
        paridad = float(paridad) if paridad else 0

        total_convertido = convertir_monto(total, int(r.moneda or 0), int(moneda_objetivo or 0), arbitraje, paridad)
        saldo_convertido = convertir_monto(saldo, int(r.moneda or 0), int(moneda_objetivo or 0), arbitraje, paridad)

        filtrados.append({
            'autogenerado': r.autogenerado,
            'fecha': r.fecha.strftime('%Y-%d-%m') if r.fecha else None,
            'documento': r.documento,
            'total': total_convertido,
            'monto': r.monto,
            'iva': r.iva,
            'tipo': r.tipo_factura,
            'moneda': moneda_nombre,
            'saldo': saldo_convertido,
            'imputado': 0,
            'arbitraje': arbitraje,
            'paridad': paridad
        })

    # Aplicar la paginación: [start:start+length] para obtener solo los registros de la página solicitada
    registros = filtrados[start:start + length]


    # Estructura de respuesta para DataTable
    response_data = {
        'draw': request.GET.get('draw', 0),  # Para mantener la coherencia con DataTable
        'recordsTotal': registros_totales.count(),  # Total de registros sin filtros
        'recordsFiltered': len(filtrados),
        # Total de registros después del filtrado (aplica el filtro de 'nrocliente')
        'data': registros  # Datos que se mostrarán en la tabla
    }

    return JsonResponse(response_data, safe=False)

def convertir_monto(monto, origen, destino, arbitraje, paridad):
    """
    Convierte un monto desde 'origen' a 'destino' utilizando arbitraje y paridad.
    origen y destino son enteros representando códigos de moneda:
    1 = moneda nacional, 2 = dólar, otros = otras monedas (ej: euro)
    """

    try:
        if origen == destino or monto == 0:
            return round(monto, 2)

        if destino == 1:  # convertir a moneda nacional
            if origen == 2 and arbitraje:
                return round(monto * arbitraje, 2)
            elif origen not in [1, 2] and arbitraje and paridad:
                dolares = monto / paridad
                return round(dolares * arbitraje, 2)

        elif destino == 2:  # convertir a dólares
            if origen == 1 and arbitraje:
                return round(monto / arbitraje, 2)
            elif origen not in [1, 2] and paridad:
                return round(monto / paridad, 2)

        else:  # convertir a otra moneda
            if origen == 1 and arbitraje and paridad:
                dolares = monto / arbitraje
                return round(dolares * paridad, 2)
            elif origen == 2 and paridad:
                return round(monto * paridad, 2)
            elif origen == destino:
                return round(monto, 2)

        # Si no se puede convertir, devolver sin modificar
        return round(monto, 2)
    except Exception as e:
        return str(e)

def guardar_impuorden_old(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                vector = body_data.get('vector', {})
                imputaciones = vector.get('imputaciones', [])
                asientos = vector.get('asiento', [])
                movimiento = vector.get('movimiento', [])
                cobranza = vector.get('cobranza', [])

                verificar_num = int(cobranza[0]['numero'])
                verif = Movims.objects.filter(mboleta=verificar_num, mnombremov='O/PAGO')
                if verif.exists():
                    return JsonResponse({'status': 'Error: ' + 'El número ingresado para la orden de pago, ya existe.'})

                autogenerado_impuventa = generar_autogenerado(datetime.now().strftime("%Y-%m-%d"))
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                if vector and imputaciones:
                    for item in imputaciones:

                        boleta = VistaPagos.objects.filter(documento=item['nroboleta'],tipo_factura=item['source'])
                        if boleta.count() == 1:
                            monto = float(item['imputado']) #if boleta.tipo == 20 else -float(item['imputado']) if boleta.tipo == 21  else 0
                            impuordenes = Impuordenes()
                            impuordenes.autofac = boleta[0].autogenerado
                            impuordenes.numero = item['nroboleta']
                            impuordenes.prefijo = boleta[0].prefijo
                            impuordenes.serie = boleta[0].serie
                            impuordenes.orden = cobranza[0]['numero']
                            impuordenes.cliente = cobranza[0]['nrocliente']
                            impuordenes.monto = monto
                            impuordenes.save()

                            movimiento_fac=Movims.objects.filter(mautogen=boleta[0].autogenerado).first()
                            if movimiento_fac:
                                movimiento_fac.msaldo=float(movimiento_fac.msaldo)-float(item['imputado'])
                                movimiento_fac.save()

                        elif boleta.count() > 1:
                            raise TypeError('Error: mas de una boleta encontrada.')
                        else:
                            raise TypeError('Error: boleta no encontrada.')

                try:
                    cliente_data = Clientes.objects.get(codigo=cobranza[0]['nrocliente'])
                except Exception as _:
                    cliente_data = None

                orden = Ordenes()
                orden.mmonto=cobranza[0]['total']
                orden.mboleta=cobranza[0]['numero']
                orden.mfechamov=fecha
                orden.mmoneda=cobranza[0]['nromoneda']
                orden.mdetalle=movimiento[0]['boletas']
                orden.mcliente=cobranza[0]['nrocliente']
                orden.mactiva='N' if cobranza[0]['definitivo'] == True else 'S'
                orden.mcaja=11112 if cobranza[0]['nromoneda'] !=1 else 11111
                orden.mautogenmovims=autogenerado_impuventa if cobranza[0]['definitivo'] == True else None
                if cliente_data:
                    orden.mnombre=cliente_data.empresa
                else:
                    orden.mnombre=''
                orden.save()

                if cobranza[0]['definitivo'] == True:
                    if cliente_data:
                        for asiento in asientos:
                            fechaj = datetime.now().strftime("%Y-%m-%d")
                            fecha_obj = datetime.strptime(fechaj, '%Y-%m-%d')
                            nroasiento = generar_numero()
                            movimiento_num = modificar_numero(nroasiento)

                            detalle_asiento = 'O/PAGO' +'-'+ str(cobranza[0]['numero']) +'-'+ cliente_data.empresa
                            asiento_vector_1 = {
                                'detalle': detalle_asiento,
                                'monto': asiento['total_pago'],
                                'moneda': cobranza[0]['nromoneda'],
                                'cambio': cobranza[0]['arbitraje'],
                                'asiento': nroasiento,
                                'conciliado': 'N',
                                'clearing': fecha_obj,
                                'fecha': fecha_obj,
                                'imputacion': 2,
                                'modo': asiento['modo'],
                                'tipo': 'G',
                                'cuenta': asiento['cuenta'],
                                'documento': cobranza[0]['numero'],
                                'vencimiento': fecha_obj,
                                'pasado': 1,
                                'autogenerado': autogenerado_impuventa,
                                'cliente': cliente_data.codigo,
                                'banco': asiento['banco'] if asiento['modo'] != 'CHEQUE' else " - ".join(map(str, Cuentas.objects.filter(xcodigo=asiento['cuenta']).values_list('xcodigo', 'xnombre').first() or ('', ''))),
                                'centro': 'ADM',
                                'mov': int(movimiento_num) + 1,
                                'anio': fecha_obj.year,
                                'mes': fecha_obj.month,
                                'fechacheque': fecha_obj,
                                'paridad': cobranza[0]['paridad'],
                                'posicion': None

                            }  # haber
                            crear_asiento(asiento_vector_1)
                            if asiento.get('modo') == 'CHEQUE':
                                numero=asiento['nro_mediopago']
                                banco=asiento['banco']
                                fecha_vencimiento=asiento['vencimiento']
                                monto=asiento['total_pago']
                                chequera=Chequeras.ojects.filter(cheque=numero).first()
                                if chequera:
                                    chequera.estado=1
                                    chequera.save()
                                    cheque = Chequeorden()
                                    cheque.cnumero=numero
                                    cheque.cbanco=banco
                                    cheque.cfecha=fecha_obj
                                    cheque.cvto=fecha_vencimiento
                                    cheque.corden=cobranza[0]['numero']
                                    cheque.cmonto=monto
                                    cheque.save()

                            elif asiento.get('modo') == 'CHEQUE TERCEROS':
                                cheque=Cheques.objects.get(id=asiento['cuenta'])
                                cheque.cestado=2
                                cheque.save()

                        #asiento general
                        asiento_vector_2 = {  # deber
                            'detalle': detalle_asiento,
                            'monto': cobranza[0]['total'],
                            'moneda': cobranza[0]['nromoneda'],
                            'cambio': cobranza[0]['arbitraje'],
                            'asiento': nroasiento,
                            'conciliado': 'N',
                            'clearing': fecha_obj,
                            'fecha': fecha_obj,
                            'imputacion': 1,
                            'modo': None,
                            'tipo': 'G',
                            'cuenta': cliente_data.ctavta,
                            'documento': cobranza[0]['numero'],
                            'vencimiento': fecha_obj,
                            'pasado': 1,
                            'autogenerado': autogenerado_impuventa,
                            'cliente': cliente_data.codigo,
                            'banco': 'S/I',
                            'centro': 'S/I',
                            'mov': movimiento_num,
                            'anio': fecha_obj.year,
                            'mes': fecha_obj.month,
                            'fechacheque': fecha_obj,
                            'paridad': cobranza[0]['paridad'],
                            'posicion': None
                        }  # deber general
                        crear_asiento(asiento_vector_2)
                        #crear el movimiento
                        movimiento_vec = {
                            'tipo': 45,
                            'fecha': fecha_obj,
                            'boleta': cobranza[0]['numero'],
                            'monto': 0,
                            'paridad': cobranza[0]['paridad'],
                            'iva': boleta[0].iva,
                            'total': cobranza[0]['total'],
                            'saldo': movimiento[0]['saldo'],
                            'moneda': cobranza[0]['nromoneda'],
                            'detalle': movimiento[0]['boletas'],
                            'cliente': cliente_data.codigo,
                            'nombre': cliente_data.empresa,
                            'nombremov': 'O/PAGO',
                            'cambio': cobranza[0]['arbitraje'],
                            'autogenerado': autogenerado_impuventa,
                            'serie': None,
                            'prefijo': None,
                            'posicion':None,
                            'anio': fecha_obj.year,
                            'mes': fecha_obj.month,
                            'monedaoriginal': cobranza[0]['nromoneda'],
                            'montooriginal': cobranza[0]['total'],
                            'arbitraje': cobranza[0]['arbitraje'],

                        }
                        crear_movimiento(movimiento_vec)

                return JsonResponse({'status': 'exito'})
    except Exception as e:
        return JsonResponse({'status': 'Error: ' + str(e)})


def crear_asiento(asiento):
    try:
        lista = Asientos()
        id = lista.get_id()
        lista.id = lista.get_id()
        lista.fecha = asiento['fecha']
        lista.asiento = asiento['asiento']
        lista.cuenta = asiento['cuenta']
        lista.imputacion = asiento['imputacion']
        lista.tipo = asiento['tipo']
        lista.documento = asiento['documento']
        lista.vto = asiento['vencimiento']
        lista.pasado = asiento['pasado']
        lista.autogenerado = asiento['autogenerado']
        lista.cliente = asiento['cliente']
        lista.banco = asiento['banco']
        lista.centro = asiento['centro']
        lista.mov = asiento['mov']
        lista.anoimpu = asiento['anio']
        lista.mesimpu = asiento['mes']
        lista.fechacheque = asiento['fechacheque']
        lista.paridad = asiento['paridad']
        lista.monto = asiento['monto']
        lista.detalle = asiento['detalle']
        lista.cambio = asiento['cambio']
        lista.moneda = asiento['moneda']
        lista.modo = asiento['modo']
        lista.save()

    except Exception as e:
        raise

def crear_movimiento(movimiento):
    try:
        lista = Movims()
        lista.id = lista.get_id()
        lista.mtipo = movimiento['tipo']
        lista.mfechamov = movimiento['fecha']
        lista.mboleta = movimiento['boleta']
        lista.mmonto = movimiento['monto']
        lista.miva = movimiento['iva']
        lista.mtotal = movimiento['total']
        lista.msobretasa = 0
        lista.msaldo = movimiento['saldo']
        lista.mvtomov = movimiento['fecha']
        lista.mmoneda = movimiento['moneda']
        lista.mdetalle = movimiento['detalle']
        lista.mcliente = movimiento['cliente']
        lista.mnombre = movimiento['nombre']
        lista.mnombremov = movimiento['nombremov']
        lista.mcambio = movimiento['cambio']
        lista.mautogen = movimiento['autogenerado']
        lista.mserie = movimiento['serie']
        lista.mprefijo = movimiento['prefijo']
        lista.mposicion = movimiento['posicion']
        lista.mmesimpu = movimiento['mes']
        lista.manoimpu = movimiento['anio']
        lista.mmonedaoriginal = movimiento['monedaoriginal']
        lista.marbitraje = movimiento['arbitraje']
        lista.mactivo = 'S'
        lista.mmontooriginal = movimiento['montooriginal']
        lista.save()

    except Exception as e:
        raise


def obtener_cheques_disponibles(request):

    # Obtener los parámetros de paginación
    start = int(request.GET.get('start', 0))  # Inicio de la página (offset)
    length = int(request.GET.get('length', 10))  # Número de registros por página
    cliente = int(request.GET.get('cliente', 0))  # Número de registros por página
    # Filtrar los registros según el proveedor
    if cliente and cliente!=0:
        cheques = Cheques.objects.filter(cestado=0,ccliente=cliente)
    else:
        cheques = Cheques.objects.filter(cestado=0)

    resultado=[]
    registros = cheques[start:start + length]
    for r in registros:
        try:
            cliente = Clientes.objects.get(codigo=r.ccliente).empresa if r.ccliente else ''
        except Clientes.DoesNotExist:
            cliente = ''

        resultado.append({
            'id': r.id,
            'vto': r.cvto.strftime('%Y-%m-%d') if r.cvto else '',
            'emision': r.cfecha.strftime('%Y-%m-%d') if r.cfecha else '',
            'banco': r.cbanco,
            'numero': r.cnumero,
            'cliente': cliente,
            'total': r.cmonto,
            'moneda':r.cmoneda
        })

    # Estructura de respuesta para DataTable
    response_data = {
        'draw': request.GET.get('draw', 0),  # Para mantener la coherencia con DataTable
        'recordsTotal': cheques.count(),  # Total de registros sin filtros
        'recordsFiltered': cheques.count(),
        # Total de registros después del filtrado (aplica el filtro de 'nrocliente')
        'data': resultado  # Datos que se mostrarán en la tabla
    }

    return JsonResponse(response_data, safe=False)

def guardar_anticipo_orden(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                vector = body_data.get('vector', {})
                # imputaciones = vector.get('imputaciones', []) #pasar el numero de cliente
                asientos = vector.get('asiento', [])
                # movimiento = vector.get('movimiento', [])
                cobranza = vector.get('cobranza', [])

                autogenerado_impuventa = generar_autogenerado(datetime.now().strftime("%Y-%m-%d"))+'111'

                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                arbitraje = float(cobranza[0]['arbitraje'])
                paridad = float(cobranza[0]['paridad'])
                nromoneda = int(cobranza[0]['nromoneda'])
                total = float(cobranza[0]['total'])
                saldo = float(cobranza[0].get('saldo', 0))


                if vector:
                    orden = Ordenes()
                    orden.mmonto = cobranza[0]['total']
                    orden.mboleta = cobranza[0]['numero']
                    orden.mfechamov = fecha
                    orden.mmoneda = cobranza[0]['nromoneda']
                    orden.mdetalle = None
                    orden.mcliente = cobranza[0]['nrocliente']
                    orden.mcaja = 11112 if cobranza[0]['nromoneda'] != 1 else 11111
                    es_definitivo = cobranza[0].get('definitivo', False)
                    orden.mactiva = 'N' if es_definitivo else 'S'
                    orden.mautogenmovims = autogenerado_impuventa if es_definitivo else None

                try:
                    cliente_data = Clientes.objects.get(codigo=cobranza[0]['nrocliente'])
                except Exception as _:
                    cliente_data = None

                if cliente_data:
                    for asiento in asientos:
                        fechaj = datetime.now().strftime("%Y-%m-%d")
                        fecha_obj = datetime.strptime(fechaj, '%Y-%m-%d')
                        nroasiento = generar_numero()
                        movimiento_num = modificar_numero(nroasiento)
                        detalle_asiento = 'O/PAGO' + '-' + str(cobranza[0]['numero']) + '-' + cliente_data.empresa
                        asiento_monto = asiento['total_pago']

                        if nromoneda == 2:  # dolar
                            monto_asiento = float(asiento_monto) * arbitraje
                        elif nromoneda not in [1, 2]:
                            aux = float(asiento_monto) * paridad
                            monto_asiento = aux * arbitraje
                        else:
                            monto_asiento = 0

                        asiento_vector_1 = {
                            'detalle': detalle_asiento,
                            'monto': monto_asiento,
                            'moneda': cobranza[0]['nromoneda'],
                            'cambio': cobranza[0]['arbitraje'],
                            'asiento': nroasiento,
                            'conciliado': 'N',
                            'clearing': fecha_obj,
                            'fecha': fecha_obj,
                            'imputacion': 1,
                            'modo': asiento['modo'],
                            'tipo': 'Z',
                            'cuenta': asiento['cuenta'],
                            'documento': cobranza[0]['numero'],
                            'vencimiento': fecha_obj,
                            'pasado': 1,
                            'autogenerado': autogenerado_impuventa,
                            'cliente': cliente_data.codigo,
                            'banco': asiento['banco'] if asiento['modo'] != 'CHEQUE' else " - ".join(map(str, Cuentas.objects.filter(xcodigo=asiento['cuenta']).values_list('xcodigo', 'xnombre').first() or ('', ''))),
                            'centro': 'ADM',
                            'mov': int(movimiento_num) + 1,
                            'anio': fecha_obj.year,
                            'mes': fecha_obj.month,
                            'fechacheque': fecha_obj,
                            'paridad': cobranza[0]['paridad'],
                            'posicion': None

                        }  # haber
                        crear_asiento(asiento_vector_1)

                        if asiento.get('modo') == 'CHEQUE':
                            numero=asiento['nro_mediopago']
                            banco=asiento['banco']
                            fecha_vencimiento=asiento['vencimiento']
                            monto=asiento['total_pago']
                            autogenerado=autogenerado_impuventa
                            detalle=detalle_asiento
                            moneda=cobranza[0]['nromoneda']
                            nrocliente=cobranza[0]['nrocliente']
                            tipo_cheque='CH'
                            cheque = Chequeorden()
                            cheque.cnumero=numero
                            cheque.cbanco=banco
                            cheque.cfecha=fecha_obj
                            cheque.cvto=fecha_vencimiento
                            cheque.cmonto=monto
                            cheque.corden=cobranza[0]['numero']
                            cheque.cmoneda=moneda
                            cheque.save()

                    #asiento general
                    asiento_vector_2 = {  # deber
                        'detalle': detalle_asiento,
                        'monto': total,
                        'moneda': cobranza[0]['nromoneda'],
                        'cambio': cobranza[0]['arbitraje'],
                        'asiento': nroasiento,
                        'conciliado': 'N',
                        'clearing': fecha_obj,
                        'fecha': fecha_obj,
                        'imputacion': 2,
                        'modo': None,
                        'tipo': 'G',
                        'cuenta': cliente_data.ctavta,
                        'documento': cobranza[0]['numero'],
                        'vencimiento': fecha_obj,
                        'pasado': 1,
                        'autogenerado': autogenerado_impuventa,
                        'cliente': cliente_data.codigo,
                        'banco': 'S/I',
                        'centro': 'S/I',
                        'mov': movimiento_num,
                        'anio': fecha_obj.year,
                        'mes': fecha_obj.month,
                        'fechacheque': fecha_obj,
                        'paridad': cobranza[0]['paridad'],
                        'posicion': None
                    }  # deber general
                    crear_asiento(asiento_vector_2)
                    #crear el movimiento
                    movimiento_vec = {
                        'tipo': 25,
                        'fecha': fecha_obj,
                        'boleta': cobranza[0]['numero'],
                        'monto': 0,
                        'paridad': cobranza[0]['paridad'],
                        'iva': 0,
                        'total': total,
                        'saldo': saldo,
                        'moneda': cobranza[0]['nromoneda'],
                        'detalle': 0,
                        'cliente': cliente_data.codigo,
                        'nombre': cliente_data.empresa,
                        'nombremov': 'COBRO',
                        'cambio': cobranza[0]['arbitraje'],
                        'autogenerado': autogenerado_impuventa,
                        'serie': cobranza[0].get('serie'),
                        'prefijo': cobranza[0].get('prefijo'),
                        'posicion': None,
                        'anio': fecha_obj.year,
                        'mes': fecha_obj.month,
                        'monedaoriginal': cobranza[0]['nromoneda'],
                        'montooriginal': total,
                        'arbitraje': cobranza[0]['arbitraje'],

                    }
                    crear_movimiento(movimiento_vec)

                return JsonResponse({'status': 'exito'})
            return None
    except Exception as e:
        return JsonResponse({'status': 'Error: ' + str(e)})

def guardar_impuorden(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                vector = body_data.get('vector', {})
                imputaciones = vector.get('imputaciones', [])
                asientos = vector.get('asiento', [])
                movimiento = vector.get('movimiento', [])
                cobranza = vector.get('cobranza', [])

                verificar_num = int(cobranza[0]['numero'])
                verif = Movims.objects.filter(mboleta=verificar_num, mnombremov='O/PAGO')
                if verif.exists():
                    return HttpResponse(
                        json.dumps({'status': 'Error: El número ingresado para la orden de pago, ya existe.'}),
                        content_type='application/json',
                        status=200
                    )
                autogenerado_impuventa = generar_autogenerado(datetime.now().strftime("%Y-%m-%d"))
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                facturas_list = []
                if vector and imputaciones:
                    for item in imputaciones:

                        boleta = VistaPagos.objects.filter(autogenerado=item['autogenerado'])
                        movim = Movims.objects.filter(mautogen=boleta[0].autogenerado).first()
                        asiento_boleta = Asientos.objects.filter(autogenerado=boleta[0].autogenerado).exclude(posicion__isnull=True).first()
                        posicion = asiento_boleta.posicion if asiento_boleta and asiento_boleta.posicion else 'S/I'

                        if boleta.count() == 1:


                            facturas_list.append({
                                "documento": item['nroboleta'],
                                "importe": abs(float(item['imputado'] or 0)),
                                "detalle_fac": movim.mdetalle if movim.mdetalle else "S/I",
                                "cambio": float(movim.marbitraje) if movim.marbitraje else 0,
                                "posicion": posicion
                            })

                            monto = abs(float(item['imputado'] or 0)) #if boleta.tipo == 20 else -float(item['imputado']) if boleta.tipo == 21  else 0
                            impuordenes = Impuordenes()
                            impuordenes.autofac = boleta[0].autogenerado
                            impuordenes.numero = item['nroboleta']
                            impuordenes.prefijo = boleta[0].prefijo
                            impuordenes.serie = boleta[0].serie
                            impuordenes.orden = cobranza[0]['numero']
                            impuordenes.cliente = cobranza[0]['nrocliente']
                            impuordenes.monto = monto
                            impuordenes.save()

                            movimiento_fac=Movims.objects.filter(mautogen=boleta[0].autogenerado).first()
                            if movimiento_fac:
                                # movimiento_fac.msaldo=float(movimiento_fac.msaldo)-float(item['imputado'])
                                movimiento_fac.msaldo = float(movimiento_fac.msaldo) - abs(float(item['imputado']))
                                movimiento_fac.save()

                        elif boleta.count() > 1:
                            raise TypeError('Error: mas de una boleta encontrada.')
                        else:
                            raise TypeError('Error: boleta no encontrada.')

                try:
                    cliente_data = Clientes.objects.get(codigo=cobranza[0]['nrocliente'])
                except Exception as _:
                    cliente_data = None

                orden = Ordenes()
                orden.mmonto=cobranza[0]['total']
                orden.mboleta=cobranza[0]['numero']
                orden.mfechamov=fecha
                orden.mmoneda=cobranza[0]['nromoneda']
                orden.mdetalle=movimiento[0]['boletas']
                orden.mcliente=cobranza[0]['nrocliente']
                orden.mactiva='N' if cobranza[0]['definitivo'] == True else 'S'
                orden.mcaja=11112 if cobranza[0]['nromoneda'] !=1 else 11111
                orden.mautogenmovims=autogenerado_impuventa if cobranza[0]['definitivo'] == True else None
                if cliente_data:
                    orden.mnombre=cliente_data.empresa
                else:
                    orden.mnombre=''
                orden.save()

                if cobranza[0]['definitivo'] == True:
                    if cliente_data:
                        for asiento in asientos:
                            fechaj = datetime.now().strftime("%Y-%m-%d")
                            fecha_obj = datetime.strptime(fechaj, '%Y-%m-%d')
                            nroasiento = generar_numero()
                            movimiento_num = modificar_numero(nroasiento)

                            detalle_asiento = 'O/PAGO' +'-'+ str(cobranza[0]['numero']) +'-'+ cliente_data.empresa
                            asiento_vector_1 = {
                                'detalle': detalle_asiento,
                                'monto': asiento['total_pago'],
                                'moneda': cobranza[0]['nromoneda'],
                                'cambio': cobranza[0]['arbitraje'],
                                'asiento': nroasiento,
                                'conciliado': 'N',
                                'clearing': fecha_obj,
                                'fecha': fecha_obj,
                                'imputacion': 2,
                                'modo': asiento['modo'],
                                'tipo': 'G',
                                'cuenta': asiento['cuenta'] if 'cuenta' in asiento and asiento['cuenta'] != '' else None,
                                'documento': cobranza[0]['numero'],
                                'vencimiento': fecha_obj,
                                'pasado': 1,
                                'autogenerado': autogenerado_impuventa,
                                'cliente': cliente_data.codigo,
                                'banco': asiento['banco'] if asiento['modo'] != 'CHEQUE' else " - ".join(map(str, Cuentas.objects.filter(xcodigo=asiento['cuenta']).values_list('xcodigo', 'xnombre').first() or ('', ''))),
                                'centro': 'ADM',
                                'mov': int(movimiento_num) + 1,
                                'anio': fecha_obj.year,
                                'mes': fecha_obj.month,
                                'fechacheque': fecha_obj,
                                'paridad': cobranza[0]['paridad'],
                                'posicion': None

                            }  # haber
                            crear_asiento(asiento_vector_1)
                            if asiento.get('modo') == 'CHEQUE':
                                numero=asiento['nro_mediopago']
                                banco=asiento['banco']
                                fecha_vencimiento=asiento['vencimiento']
                                monto=asiento['total_pago']
                                chequera=Chequeras.ojects.filter(cheque=numero).first()
                                if chequera:
                                    chequera.estado=1
                                    chequera.save()
                                    cheque = Chequeorden()
                                    cheque.cnumero=numero
                                    cheque.cbanco=banco
                                    cheque.cfecha=fecha_obj
                                    cheque.cvto=fecha_vencimiento
                                    cheque.corden=cobranza[0]['numero']
                                    cheque.cmonto=monto
                                    cheque.save()

                            elif asiento.get('modo') == 'CHEQUE TERCEROS':
                                cheque=Cheques.objects.get(id=asiento['cuenta'])
                                cheque.cestado=2
                                cheque.save()

                        #asiento general
                        asiento_vector_2 = {  # deber
                            'detalle': detalle_asiento,
                            'monto': cobranza[0]['total'],
                            'moneda': cobranza[0]['nromoneda'],
                            'cambio': cobranza[0]['arbitraje'],
                            'asiento': nroasiento,
                            'conciliado': 'N',
                            'clearing': fecha_obj,
                            'fecha': fecha_obj,
                            'imputacion': 1,
                            'modo': None,
                            'tipo': 'G',
                            'cuenta': cliente_data.ctavta,
                            'documento': cobranza[0]['numero'],
                            'vencimiento': fecha_obj,
                            'pasado': 1,
                            'autogenerado': autogenerado_impuventa,
                            'cliente': cliente_data.codigo,
                            'banco': 'S/I',
                            'centro': 'S/I',
                            'mov': movimiento_num,
                            'anio': fecha_obj.year,
                            'mes': fecha_obj.month,
                            'fechacheque': fecha_obj,
                            'paridad': cobranza[0]['paridad'],
                            'posicion': None
                        }  # deber general
                        crear_asiento(asiento_vector_2)
                        #crear el movimiento
                        movimiento_vec = {
                            'tipo': 45,
                            'fecha': fecha_obj,
                            'boleta': cobranza[0]['numero'],
                            'monto': 0,
                            'paridad': cobranza[0]['paridad'],
                            'iva': boleta[0].iva if boleta and boleta.exists() else 0,
                            'total': cobranza[0]['total'],
                            'saldo': movimiento[0]['saldo'],
                            'moneda': cobranza[0]['nromoneda'],
                            'detalle': movimiento[0]['boletas'],
                            'cliente': cliente_data.codigo,
                            'nombre': cliente_data.empresa,
                            'nombremov': 'O/PAGO',
                            'cambio': cobranza[0]['arbitraje'],
                            'autogenerado': autogenerado_impuventa,
                            'serie': None,
                            'prefijo': None,
                            'posicion':None,
                            'anio': fecha_obj.year,
                            'mes': fecha_obj.month,
                            'monedaoriginal': cobranza[0]['nromoneda'],
                            'montooriginal': cobranza[0]['total'],
                            'arbitraje': cobranza[0]['arbitraje'],

                        }
                        crear_movimiento(movimiento_vec)

                #return JsonResponse({'status': 'exito'})
                pdf_data = {
                    "nro": cobranza[0]['numero'],
                    "fecha_pago": fecha_obj.strftime("%Y-%m-%d"),
                    "vto": fecha_obj.strftime("%Y-%m-%d"),  # o el vencimiento real si lo tenés
                    "detalle": movimiento[0]['boletas'],
                    "cambio_general": cobranza[0]['arbitraje'],
                    "monto_total": str(cobranza[0]['total']),
                    "moneda": "MONEDA NACIONAL" if cobranza[0]['nromoneda'] == 1 else "DÓLARES",
                    "proveedor_nombre": cliente_data.empresa if cliente_data else "",
                    "proveedor_direccion": cliente_data.direccion if cliente_data else "",
                    "proveedor_telefono": cliente_data.telefono if cliente_data else "",

                    "facturas": json.dumps(facturas_list),

                    "forma_pago": json.dumps([
                        {
                            "modo": i.get("modo", "S/I"),
                            "numero": i.get("nro_mediopago", ""),
                            'banco': asiento['banco'] if asiento['modo'] != 'CHEQUE' else " - ".join(map(str,Cuentas.objects.filter(xcodigo= asiento['cuenta']).values_list('xcodigo','xnombre').first() or ( '', ''))),
                            "monto_total": i.get("total_pago", "0"),
                            "vencimiento_cheque": i.get("vencimiento", None)
                        }
                        for i in asientos
                    ])
                }

                try:
                    return generar_orden_pago_pdf(pdf_data, request)
                except Exception as e:
                    return JsonResponse({
                        'status': 'exito',
                        'mensaje': f'No se pudo generar el PDF ({str(e)})'
                    }, status=200)
            return None
    except Exception as e:
        return HttpResponse(
            json.dumps({'status': 'Error: ' + str(e)}),
            content_type='application/json',
            status=200
        )

def generar_orden_pago_pdf_sin_prov(pdf_data, request):
    try:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="orden_pago.pdf"; filename*=UTF-8\'\'orden_pago.pdf'

        c = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 30 * mm

        # Logo
        logo_path = os.path.join(settings.PACKAGE_ROOT, 'static', 'images', 'oceanlink.png')
        c.drawImage(logo_path, 20 * mm, y, width=40 * mm, preserveAspectRatio=True, mask='auto')
        y -= 5 * mm

        fecha_pago_str = pdf_data.get("fecha_pago")
        vto_str = pdf_data.get("vto")
        try:
            fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d").strftime('%d/%m/%Y')
            vto = datetime.strptime(vto_str, "%Y-%m-%d").strftime('%d/%m/%Y')
        except (ValueError, TypeError):
            fecha_pago = fecha_pago_str
            vto = fecha_pago_str

        # Datos principales
        c.setFont("Courier", 12)
        y -= 5 * mm
        c.drawString(20 * mm, y, f"Orden de pago .....: {pdf_data.get('nro')}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Fecha de pago .....: {fecha_pago}")
        y -= 6 * mm
        nombre = str(request.user.first_name) + ' ' + str(request.user.last_name)
        c.drawString(20 * mm, y, f"Solicitada por ....: {nombre}")

        # Moneda y monto
        c.setFont("Courier-Bold", 10)
        y -= 10 * mm
        c.drawString(20 * mm, y, f"Moneda ............: {pdf_data.get('moneda')}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Monto a pagar .....: {pdf_data.get('monto_total')}")

        # Cuentas imputadas
        y -= 12 * mm
        c.setFont("Courier-Bold", 10)
        titulo = "Cuentas imputadas en el pago:"
        c.drawString(20 * mm, y, titulo)
        c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(titulo, "Courier-Bold", 10), y - 1.5 * mm)

        y -= 8 * mm
        c.setFont("Courier", 10)
        encabezado = "Cuenta                           Monto        Detalle"
        c.drawString(20 * mm, y, encabezado)
        c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(encabezado, "Courier", 10), y - 1.5 * mm)

        y -= 6 * mm
        try:
            detalle_items = json.loads(pdf_data.get('facturas', '[]'))
            for item in detalle_items:
                cuenta_p = item.get('cuenta', '')[:30].ljust(30)
                monto_p = f"{float(item.get('importe', 0)):>10.2f}"
                detalle_p = item.get('detalle_fac', '')[:25]
                c.drawString(20 * mm, y, f"{cuenta_p} {monto_p}    {detalle_p}")
                y -= 6 * mm
        except Exception as e:
            c.drawString(20 * mm, y, f"[Error al procesar filas: {str(e)}]")
            y -= 6 * mm

        y -= 6 * mm
        c.setFont("Courier-Bold", 10)
        titulo_fp = "Detalle"
        c.drawString(20 * mm, y, titulo_fp)
        c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(titulo_fp, "Courier-Bold", 10), y - 1.5 * mm)
        y -= 6 * mm
        c.setFont("Courier", 10)
        c.drawString(20 * mm, y, pdf_data.get('detalle', '')[:80])

        # Forma de pago
        y -= 12 * mm
        c.setFont("Courier-Bold", 10)
        titulo_fp = "Forma de pago:"
        c.drawString(20 * mm, y, titulo_fp)
        c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(titulo_fp, "Courier-Bold", 10), y - 1.5 * mm)

        y -= 6 * mm
        c.setFont("Courier", 10)
        c.drawString(20 * mm, y, "Tipo")
        c.drawString(40 * mm, y, "Número")
        c.drawString(70 * mm, y, "Banco")
        c.drawString(140 * mm, y, "Importe")
        c.drawString(170 * mm, y, "Vto.")
        c.line(20 * mm, y - 1.5 * mm, 200 * mm, y - 1.5 * mm)

        forma_pago = json.loads(pdf_data.get('forma_pago', '[]'))
        for f in forma_pago:
            y -= 6 * mm
            tipo = f.get("modo", "S/I")
            numero = str(f.get("numero", ""))
            banco = f.get("banco", "")[:25]
            importe = str(f.get("monto_total", "0"))
            vto_fp = f.get("vencimiento_cheque", " ")

            c.drawString(20 * mm, y, str(tipo or ""))
            c.drawString(40 * mm, y, str(numero or ""))
            c.drawString(70 * mm, y, str(banco or ""))
            c.drawRightString(155 * mm, y, str(importe or "0.00"))
            c.drawString(170 * mm, y, str(vto_fp or ""))

        # Monto en letras
        y -= 10 * mm
        monto = pdf_data.get('monto_total', '0')
        leyenda_monto = monto_a_letras(monto,pdf_data.get('moneda'))
        c.drawString(20 * mm, y, leyenda_monto)

        # Firmas
        y -= 30 * mm
        c.drawString(40 * mm, y, "______________________")
        c.drawString(130 * mm, y, "______________________")
        y -= 6 * mm
        c.drawString(50 * mm, y, "Autorizado")
        c.drawString(140 * mm, y, "Recibido")

        c.showPage()
        c.save()
        return response

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generar_orden_pago_pdf(data,request):
    try:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="orden_pago.pdf"; filename*=UTF-8\'\'orden_pago.pdf'

        c = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 30 * mm

        # Logo
        logo_path = os.path.join(settings.PACKAGE_ROOT, 'static', 'images', 'oceanlink.png')
        c.drawImage(logo_path, 20 * mm, y, width=40 * mm, preserveAspectRatio=True, mask='auto')
        y -= 5 * mm

        detalle = data.get('detalle', '')[:35]
        fecha_pago_str = data.get("fecha_pago")
        vto_str = data.get("vto")
        try:
            fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d")  # o el formato en que venga tu fecha
            vto = datetime.strptime(vto_str, "%Y-%m-%d")  # o el formato en que venga tu fecha
            fecha_pago = fecha_pago.strftime('%d/%m/%Y')
            vto = vto.strftime('%d/%m/%Y')
        except (ValueError, TypeError):
            fecha_pago = fecha_pago_str
            vto = fecha_pago_str

            # Datos principales
        c.setFont("Courier", 12)
        y -= 5 * mm
        c.drawString(20 * mm, y, f"Orden de pago .....: {data.get('nro')}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Fecha de pago .....: {fecha_pago}")
        y -= 6 * mm
        nombre = str(request.user.first_name) + ' ' + str(request.user.last_name)
        c.drawString(20 * mm, y, f"Solicitada por ....: {nombre}")

        c.setFont("Courier", 10)
        y -= 10 * mm
        c.drawString(20 * mm, y, f"Proveedor .........: {data.get('proveedor_nombre', '')}")
        y -= 6 * mm  # bajar una línea
        c.drawString(20 * mm, y, f"                    {data.get('proveedor_direccion', '')}")
        y -= 6 * mm  # bajar una línea
        c.drawString(20 * mm, y, f"                    {data.get('proveedor_telefono', '')}")

        # Moneda y monto
        c.setFont("Courier-Bold", 10)
        y -= 10 * mm
        c.drawString(20 * mm, y, f"Moneda ............: {data.get('moneda')}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Tipo de cambio ....: {data.get('cambio_general')}")
        y -= 6 * mm
        c.drawString(20 * mm, y, f"Monto a pagar .....: {data.get('monto_total')}")

        # Cuentas imputadas
        y -= 12 * mm
        c.setFont("Courier", 11)
        titulo = "Facturas imputadas en el pago:"
        c.drawString(20 * mm, y, titulo)

        y -= 8 * mm
        c.setFont("Courier", 10)
        encabezado = "Numero    Vencimiento    Importe    Detalle                  T.C.    Posicion    "
        c.drawString(20 * mm, y, encabezado)
        c.line(20 * mm, y - 1.5 * mm, 20 * mm + c.stringWidth(encabezado, "Courier", 10), y - 1.5 * mm)

        y -= 6 * mm

        """
                banco = data.get('banco', '')[:30].ljust(30)
        monto_valor = float(data.get('monto_total') or 0)
        monto = f"{monto_valor:>10.2f}"
        """

        try:
            facturas_items = json.loads(data.get('facturas', '[]'))
            for item in facturas_items:
                documento_fac = item.get('documento', '')
                cambio_fac = item.get('cambio', '')
                posicion_fac = item.get('posicion', '')
                monto_p = f"{float(item.get('importe', 0)):>10.2f}"
                detalle_p = item.get('detalle_fac', '')[:25]
                c.drawString(20 * mm, y, f"{documento_fac}    {fecha_pago}    {monto_p}    {detalle_p}                    {cambio_fac}    {posicion_fac}")
                y -= 6 * mm
        except Exception as e:
            c.drawString(20 * mm, y, f"[Error al procesar filas: {str(e)}]")
            y -= 6 * mm

        # Forma de pago

        forma_pago = json.loads(data.get('forma_pago', '[]'))

        # Titulos
        y -= 12 * mm
        c.setFont("Courier", 11)
        titulo_fp = "Forma de pago:"
        c.drawString(20 * mm, y, titulo_fp)

        # Encabezado
        y -= 6 * mm
        c.setFont("Courier", 10)
        c.drawString(20 * mm, y, "Tipo")
        c.drawString(40 * mm, y, "Número")
        c.drawString(70 * mm, y, "Banco")
        c.drawString(140 * mm, y, "Importe")
        c.drawString(170 * mm, y, "Vto.")
        c.line(20 * mm, y - 1.5 * mm, 200 * mm, y - 1.5 * mm)

        for f in forma_pago:
            # Valores
            y -= 6 * mm
            tipo = f.get("modo")
            numero = f.get("numero", "")
            banco = f.get("banco", "")[:25]
            importe = f.get("monto_total", "0")
            vto = f.get("vencimiento_cheque", None)
            if vto:
                vto = datetime.strptime(vto_str, "%Y-%m-%d")  # o el formato en que venga tu fecha
                vto = vto.strftime('%Y/%m/%d')

            c.drawString(20 * mm, y, str(tipo))
            c.drawString(40 * mm, y, str(numero))
            c.drawString(70 * mm, y, str(banco))
            c.drawRightString(155 * mm, y, str(importe))
            c.drawString(170 * mm, y, str(vto or ""))

        y -= 12 * mm
        c.setFont("Courier", 10)
        titulo_fp = "Detalle"
        c.drawString(20 * mm, y, titulo_fp)
        y -= 6 * mm
        c.setFont("Courier", 10)
        c.drawString(20 * mm, y, detalle)

        # Texto en letras
        y -= 10 * mm
        monto = data.get('monto_total', '0')
        leyenda_monto = monto_a_letras(monto,data.get('moneda'))
        c.drawString(20 * mm, y, leyenda_monto)

        # Firmas
        y -= 30 * mm
        c.drawString(40 * mm, y, "______________________")
        c.drawString(130 * mm, y, "______________________")
        y -= 6 * mm
        c.drawString(50 * mm, y, "Autorizado")
        c.drawString(140 * mm, y, "Recibido")

        c.showPage()
        c.save()
        return response
    except Exception as e:
        raise RuntimeError(f"Error al generar PDF: {e}")

def monto_a_letras(monto,moneda):
    try:
        monto = float(str(monto).replace(",", ""))  # Asegura formato numérico
        enteros = int(monto)
        decimales = int(round((monto - enteros) * 100))
        letras = num2words(enteros, lang='es').upper()
        return f"SON {moneda} {letras} CON {decimales:02d}/100."
    except:
        return f"SON {moneda} S/I"

def reimprimir_op_old(request):
    autogenerado = request.GET.get('autogenerado')
    if not autogenerado:
        return JsonResponse({'status': 'Error: falta el autogenerado'}, status=400)

    try:
        orden = Ordenes.objects.get(mautogenmovims=autogenerado)
        cliente_data = Clientes.objects.filter(codigo=orden.mcliente).first()
        asientos = Asientos.objects.filter(autogenerado=orden.mautogenmovims,imputacion=2)
        imputaciones = Impuordenes.objects.filter(orden=orden.mboleta)
        movimiento = Movims.objects.filter(mautogen=autogenerado).first()

        if not movimiento:
            return JsonResponse({'status': 'Error: no se encontró el movimiento para la orden'}, status=404)

        facturas_list = []
        for imp in imputaciones:
            movimiento_fac = Movims.objects.filter(mautogen=imp.autofac).first()
            asiento_fac = Asientos.objects.filter(autogenerado=imp.autofac).exclude(posicion__isnull=True).values('posicion').first()
            facturas_list.append({
                "documento": movimiento_fac.mboleta if movimiento_fac else 'S/I',
                "importe": float(imp.monto),
                "detalle_fac": movimiento_fac.mdetalle if movimiento_fac and movimiento_fac.mdetalle else "S/I",
                "cambio": float(movimiento_fac.marbitraje) if movimiento_fac else 0,
                "posicion": asiento_fac['posicion'] if asiento_fac else "S/I"
            })

        pdf_data = {
            "nro": orden.mboleta,
            "fecha_pago": orden.mfechamov.strftime("%Y-%m-%d"),
            "vto": orden.mfechamov.strftime("%Y-%m-%d"),
            "detalle": orden.mdetalle,
            "cambio_general": float(movimiento.marbitraje) if hasattr(movimiento, 'marbitraje') else "",
            "monto_total": str(orden.mmonto),
            "moneda": "MONEDA NACIONAL" if orden.mmoneda == 1 else "DÓLARES",
            "proveedor_nombre": cliente_data.empresa if cliente_data else "",
            "proveedor_direccion": cliente_data.direccion if cliente_data else "",
            "proveedor_telefono": cliente_data.telefono if cliente_data else "",
            "facturas": json.dumps(facturas_list),
            "forma_pago": json.dumps([
                {
                    "modo": i.modo,
                    "numero": (
                        Chequeorden.objects.filter(corden=orden.mboleta).first().cnumero
                        if i.modo == 'CHEQUE' else 0
                    ),
                    "banco": i.banco,
                    "monto_total": float(i.monto),
                    "vencimiento_cheque": i.vto.strftime('%Y-%m-%d') if i.vto else None
                }
                for i in asientos
            ])
        }

        return generar_orden_pago_pdf(pdf_data, request)

    except Ordenes.DoesNotExist:
        return JsonResponse({'status': 'Error: orden no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'Error: ' + str(e)}, status=500)

def reimprimir_op(request):
    autogenerado = request.GET.get('autogenerado')
    if not autogenerado:
        return JsonResponse({'status': 'Error: falta el autogenerado'}, status=400)

    try:
        orden = Ordenes.objects.get(mautogenmovims=autogenerado)
        if orden.mcliente is None:
            cliente_data = False
        else:
            cliente_data = Clientes.objects.filter(codigo=orden.mcliente).first()
        movimiento = Movims.objects.filter(mautogen=autogenerado).first()
        asientos = Asientos.objects.filter(autogenerado=orden.mautogenmovims, imputacion=2)

        if not movimiento:
            return JsonResponse({'status': 'Error: no se encontró el movimiento para la orden'}, status=404)

        # Común para ambas funciones
        fecha_pago_str = orden.mfechamov.strftime("%Y-%m-%d")
        vto_str = fecha_pago_str
        moneda_str = "MONEDA NACIONAL" if orden.mmoneda == 1 else "DÓLARES"
        cambio = float(movimiento.marbitraje) if hasattr(movimiento, 'marbitraje') and movimiento.marbitraje else 0

        forma_pago = json.dumps([
            {
                "modo": i.modo,
                "numero": (
                    Chequeorden.objects.filter(corden=orden.mboleta).first().cnumero
                    if i.modo == 'CHEQUE' else 0
                ),
                "banco": i.banco,
                "monto_total": float(i.monto),
                "vencimiento_cheque": i.vto.strftime('%Y-%m-%d') if i.vto else None
            }
            for i in asientos
        ])

        if cliente_data:
            # Estructura para generar_orden_pago_pdf (con proveedor y facturas imputadas)
            imputaciones = Impuordenes.objects.filter(orden=orden.mboleta)
            facturas_list = []
            for imp in imputaciones:
                movimiento_fac = Movims.objects.filter(mautogen=imp.autofac).first()
                asiento_fac = Asientos.objects.filter(autogenerado=imp.autofac).exclude(posicion__isnull=True).values('posicion').first()
                facturas_list.append({
                    "documento": movimiento_fac.mboleta if movimiento_fac else 'S/I',
                    "importe": float(imp.monto),
                    "detalle_fac": movimiento_fac.mdetalle if movimiento_fac and movimiento_fac.mdetalle else "S/I",
                    "cambio": float(movimiento_fac.marbitraje) if movimiento_fac and movimiento.marbitraje else 0,
                    "posicion": asiento_fac['posicion'] if asiento_fac else "S/I"
                })

            pdf_data = {
                "nro": orden.mboleta,
                "fecha_pago": fecha_pago_str,
                "vto": vto_str,
                "detalle": orden.mdetalle,
                "cambio_general": cambio,
                "monto_total": str(orden.mmonto),
                "moneda": moneda_str,
                "proveedor_nombre": cliente_data.empresa,
                "proveedor_direccion": cliente_data.direccion,
                "proveedor_telefono": cliente_data.telefono,
                "facturas": json.dumps(facturas_list),
                "forma_pago": forma_pago
            }
            return generar_orden_pago_pdf(pdf_data, request)

        else:
            # Estructura para generar_orden_pago_pdf_sin_prov (con cuentas imputadas)
            cuentas_list = []
            for i in asientos:
                cuenta_obj = Cuentas.objects.filter(xcodigo=i.cuenta).values('xcodigo', 'xnombre').first()
                cuentas_list.append({
                    "posicion": i.posicion if i.posicion else "S/I",
                    "importe": float(i.monto),
                    "cuenta": f"{cuenta_obj['xcodigo']} - {cuenta_obj['xnombre']}" if cuenta_obj else "S/I",
                    "detalle_fac": i.detalle[:40] if i.detalle else "S/I"
                })

            pdf_data = {
                "nro": orden.mboleta,
                "fecha_pago": fecha_pago_str,
                "vto": vto_str,
                "detalle": orden.mdetalle,
                "monto_total": str(orden.mmonto),
                "moneda": moneda_str,
                "facturas": json.dumps(cuentas_list),  # ← en esta versión, se llama igual pero con otra estructura
                "forma_pago": forma_pago
            }
            return generar_orden_pago_pdf_sin_prov(pdf_data, request)

    except Ordenes.DoesNotExist:
        return JsonResponse({'status': 'Error: orden no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'Error: ' + str(e)}, status=500)

def obtener_proximo_mboleta_op(request):
    try:
        ultima = Movims.objects.filter(mtipo=45).order_by('-id').first()
        proximo = int(ultima.mboleta) + 1 if ultima and ultima.mboleta.isdigit() else 1
        return JsonResponse({'proximo_mboleta': str(proximo)})
    except Exception as e:
        return JsonResponse({'error': f'Error al obtener mboleta: {str(e)}'}, status=500)