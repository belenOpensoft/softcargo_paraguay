import json
from datetime import datetime

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from administracion_contabilidad.forms import OrdenPago
from administracion_contabilidad.views.facturacion import generar_numero, modificar_numero, generar_autogenerado
from mantenimientos.models import Clientes
from administracion_contabilidad.models import Asientos


def orden_pago_view(request):
    form = OrdenPago(request.POST or None)
    return render(request, 'orden_pago.html', {'form': form})


def buscar_proveedor(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()  # Obtener y limpiar el término de búsqueda
        proveedores = Clientes.objects.filter(empresa__icontains=query)[:10]  # Limitar resultados a 10
        results = [{'id': proveedor.id, 'text': proveedor.empresa} for proveedor in proveedores]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def buscar_proveedores(request):
    if request.method == "GET":
        proveedor_id = request.GET.get("codigo")
        proveedor = Clientes.objects.filter(id=proveedor_id).first()

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


def obtener_imputables(request):
    proveedor_id = request.GET.get('codigo')
    asientos = Asientos.objects.filter(cliente=proveedor_id)

    resultados = []
    for registro in asientos:
        resultados.append({
            'id': registro.id,
            'vto': registro.vto.strftime('%Y-%m-%d') if registro.vto else '',
            'fecha_emision': registro.fechaemision.strftime('%Y-%m-%d') if registro.fechaemision else '',
            'documento': registro.documento,
            'monto_total': str(registro.monto),
            'saldo': str(registro.mov),
            'detalle': registro.detalle,
            'embarque': registro.centro,
            'co': registro.cuenta,
            'posicion': registro.posicion,
            'tc': str(registro.cambio),
            'moneda': registro.moneda,
            'paridad': str(registro.paridad),
            'monto_original': str(registro.monto)
        })

    # Estructura de respuesta para DataTable
    response_data = {
        'draw': request.GET.get('draw', 0),  # Para mantener la coherencia con DataTable
        'recordsTotal': asientos.count(),  # Total de registros sin filtros
        'recordsFiltered': asientos.count(),  # Total de registros después del filtrado
        'data': resultados  # Datos que se mostrarán en la tabla
    }

    return JsonResponse(response_data, safe=False)

# @transaction.atomic
# def guardar_impuventa(request):
#     try:
#         if request.method == 'POST':
#             body_unicode = request.body.decode('utf-8')
#             body_data = json.loads(body_unicode)
#             vector = body_data.get('vector', {})
#             imputaciones = vector.get('imputaciones', [])
#             asientos = vector.get('asiento', [])
#             movimiento = vector.get('movimiento', [])
#             cobranza = vector.get('cobranza', [])
#
#             autogenerado_impuventa = generar_autogenerado(datetime.now().strftime("%Y-%m-%d"))
#             fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#             if vector and imputaciones:
#                 for item in imputaciones:
#
#                     try:
#                         boleta = Boleta.objects.filter(numero=item['nroboleta']).order_by('-id').first()
#                     except Exception as _:
#                         boleta = None
#
#                     if boleta:
#                         autofac = boleta.autogenerado
#                         parteiva=boleta.totiva
#                         #diferenciar si son acreedor o proveedor 40 va negativo
#                         monto = float(item['imputado']) if boleta.tipo == 20 else -float(item['imputado']) if boleta.tipo == 21  else 0
#                         cliente=boleta.nrocliente
#                         impuventa = Impuvtas()
#                         impuventa.autogen = autogenerado_impuventa
#                         impuventa.tipo = 1
#                         impuventa.cliente = cliente
#                         impuventa.monto = monto
#                         impuventa.autofac = autofac
#                         impuventa.parteiva = parteiva
#                         impuventa.fechaimpu = fecha
#                         impuventa.save()
#
#             try:
#                 cliente_data = Clientes.objects.get(codigo=cobranza[0]['nrocliente'])
#             except Exception as _:
#                 cliente_data = None
#
#             if cliente_data:
#                 for asiento in asientos:
#                     fechaj = datetime.now().strftime("%Y-%m-%d")
#                     fecha_obj = datetime.strptime(fechaj, '%Y-%m-%d')
#                     nroasiento = generar_numero()
#                     movimiento_num = modificar_numero(nroasiento)
#
#                     detalle_asiento = 'COBRO' + cobranza[0]['serie'] +'-'+ str(cobranza[0]['prefijo']) +'-'+ str(cobranza[0]['numero']) +'-'+ cliente_data.empresa
#                     asiento_vector_1 = {
#                         'detalle': detalle_asiento,
#                         'monto': asiento['total_pago'],
#                         'moneda': cobranza[0]['nromoneda'],
#                         'cambio': cobranza[0]['arbitraje'],
#                         'asiento': nroasiento,
#                         'conciliado': 'N',
#                         'clearing': fecha_obj,
#                         'fecha': fecha_obj,
#                         'imputacion': 1,
#                         'modo': asiento['modo'],
#                         'tipo': 'Z',
#                         'cuenta': asiento['cuenta'],
#                         'documento': cobranza[0]['numero'],
#                         'vencimiento': fecha_obj,
#                         'pasado': 0,
#                         'autogenerado': autogenerado_impuventa,
#                         'cliente': cliente_data.codigo,
#                         'banco': asiento['banco'] if asiento['modo'] != 'CHEQUE' else " - ".join(map(str, Cuentas.objects.filter(xcodigo=asiento['cuenta']).values_list('xcodigo', 'xnombre').first() or ('', ''))),
#                         'centro': 'ADM',
#                         'mov': int(movimiento_num) + 1,
#                         'anio': fecha_obj.year,
#                         'mes': fecha_obj.month,
#                         'fechacheque': fecha_obj,
#                         'paridad': cobranza[0]['paridad'],
#                         'posicion': boleta.posicion if boleta.posicion else None
#
#                     }  # haber
#                     crear_asiento(asiento_vector_1)
#                     if asiento.get('modo') == 'CHEQUE':
#                         numero=asiento['nro_mediopago']
#                         banco=asiento['banco']
#                         fecha_vencimiento=asiento['vencimiento']
#                         monto=asiento['total_pago']
#                         autogenerado=autogenerado_impuventa
#                         detalle=detalle_asiento
#                         moneda=cobranza[0]['nromoneda']
#                         nrocliente=cobranza[0]['nrocliente']
#                         tipo_cheque='CH'
#                         cheque = Cheques()
#                         cheque.cnumero=numero
#                         cheque.cbanco=banco
#                         cheque.cfecha=fecha_obj
#                         cheque.cvto=fecha_vencimiento
#                         cheque.cmonto=monto
#                         cheque.cautogenerado=autogenerado
#                         cheque.cdetalle=detalle
#                         cheque.ccliente=nrocliente
#                         cheque.cmoneda=moneda
#                         cheque.ctipo=tipo_cheque
#                         cheque.save()
#
#                 #asiento general
#                 asiento_vector_2 = {  # deber
#                     'detalle': detalle_asiento,
#                     'monto': cobranza[0]['total'],
#                     'moneda': cobranza[0]['nromoneda'],
#                     'cambio': cobranza[0]['arbitraje'],
#                     'asiento': nroasiento,
#                     'conciliado': 'N',
#                     'clearing': fecha_obj,
#                     'fecha': fecha_obj,
#                     'imputacion': 2,
#                     'modo': None,
#                     'tipo': 'Z',
#                     'cuenta': cliente_data.ctavta,
#                     'documento': cobranza[0]['numero'],
#                     'vencimiento': fecha_obj,
#                     'pasado': 0,
#                     'autogenerado': autogenerado_impuventa,
#                     'cliente': cliente_data.codigo,
#                     'banco': 'S/I',
#                     'centro': 'S/I',
#                     'mov': movimiento_num,
#                     'anio': fecha_obj.year,
#                     'mes': fecha_obj.month,
#                     'fechacheque': fecha_obj,
#                     'paridad': cobranza[0]['paridad'],
#                     'posicion': boleta.posicion if boleta.posicion else None
#                 }  # deber general
#                 crear_asiento(asiento_vector_2)
#                 #crear el movimiento
#                 movimiento_vec = {
#                     'tipo': 25,
#                     'fecha': fecha_obj,
#                     'boleta': cobranza[0]['numero'],
#                     'monto': 0,
#                     'paridad': cobranza[0]['paridad'],
#                     'iva': boleta.totiva,
#                     'total': cobranza[0]['total'],
#                     'saldo': movimiento[0]['saldo'],
#                     'moneda': cobranza[0]['nromoneda'],
#                     'detalle': movimiento[0]['boletas'],
#                     'cliente': cliente_data.codigo,
#                     'nombre': cliente_data.empresa,
#                     'nombremov': 'COBRO',
#                     'cambio': cobranza[0]['arbitraje'],
#                     'autogenerado': autogenerado_impuventa,
#                     'serie': cobranza[0]['serie'],
#                     'prefijo': cobranza[0]['prefijo'],
#                     'posicion': boleta.posicion if boleta else None,
#                     'anio': fecha_obj.year,
#                     'mes': fecha_obj.month,
#                     'monedaoriginal': cobranza[0]['nromoneda'],
#                     'montooriginal': cobranza[0]['total'],
#                     'arbitraje': cobranza[0]['arbitraje'],
#
#                 }
#                 crear_movimiento(movimiento_vec)
#
#             return JsonResponse({'status': 'exito'})
#     except Exception as e:
#         return JsonResponse({'status': 'Error: ' + str(e)})
#
# def crear_asiento(asiento):
#     try:
#         lista = Asientos()
#         id = lista.get_id()
#         lista.id = lista.get_id()
#         lista.fecha = asiento['fecha']
#         lista.asiento = asiento['asiento']
#         lista.cuenta = asiento['cuenta']
#         lista.imputacion = asiento['imputacion']
#         lista.tipo = asiento['tipo']
#         lista.documento = asiento['documento']
#         lista.vto = asiento['vencimiento']
#         lista.pasado = asiento['pasado']
#         lista.autogenerado = asiento['autogenerado']
#         lista.cliente = asiento['cliente']
#         lista.banco = asiento['banco']
#         lista.centro = asiento['centro']
#         lista.mov = asiento['mov']
#         lista.anoimpu = asiento['anio']
#         lista.mesimpu = asiento['mes']
#         lista.fechacheque = asiento['fechacheque']
#         lista.paridad = asiento['paridad']
#         lista.monto = asiento['monto']
#         lista.detalle = asiento['detalle']
#         lista.cambio = asiento['cambio']
#         lista.moneda = asiento['moneda']
#         lista.save()
#
#     except Exception as e:
#         return JsonResponse({'status': 'Error: ' + str(e)})
#
# def crear_movimiento(movimiento):
#     try:
#         lista = Movims()
#         lista.id = lista.get_id()
#         lista.mtipo = movimiento['tipo']
#         lista.mfechamov = movimiento['fecha']
#         lista.mboleta = movimiento['boleta']
#         lista.mmonto = movimiento['monto']
#         lista.miva = movimiento['iva']
#         lista.mtotal = movimiento['total']
#         lista.msobretasa = 0
#         lista.msaldo = movimiento['saldo']
#         lista.mvtomov = movimiento['fecha']
#         lista.mmoneda = movimiento['moneda']
#         lista.mdetalle = movimiento['detalle']
#         lista.mcliente = movimiento['cliente']
#         lista.mnombre = movimiento['nombre']
#         lista.mnombremov = movimiento['nombremov']
#         lista.mcambio = movimiento['cambio']
#         lista.mautogen = movimiento['autogenerado']
#         lista.mserie = movimiento['serie']
#         lista.mprefijo = movimiento['prefijo']
#         lista.mposicion = movimiento['posicion']
#         lista.mmesimpu = movimiento['mes']
#         lista.manoimpu = movimiento['anio']
#         lista.mmonedaoriginal = movimiento['monedaoriginal']
#         lista.marbitraje = movimiento['arbitraje']
#         lista.mmontooriginal = movimiento['montooriginal']
#         lista.save()
#
#     except Exception as e:
#         return JsonResponse({'status': 'Error:' + str(e)})