import json
from datetime import datetime
from random import randint

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render

from administracion_contabilidad.models import Movims, Asientos, VistaProveedoresygastos, Impucompras
from administracion_contabilidad.views.facturacion import generar_autogenerado, generar_numero, modificar_numero
from mantenimientos.models import Clientes, Servicios
from administracion_contabilidad.forms import ProveedoresGastos, ComprasDetalleTabla
from django.http import JsonResponse
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

@login_required(login_url='/login')
def proveedores_gastos_view(request):

    hoy = datetime.now().strftime('%Y-%m-%d')
    form = ProveedoresGastos(initial={'fecha_registro':hoy,'fecha_documento':hoy,'vencimiento':hoy,'prefijo': '0001'})
    detalle= ComprasDetalleTabla()

    return render(request, 'proveedores_gastos.html', {'form': form,'detalle':detalle})

def buscar_proveedor(request):
    if request.method == 'GET':
        query = request.GET.get('term', '').strip()
        proveedores = Clientes.objects.filter(empresa__icontains=query)[:10]
        results = [
            {'id': p.id, 'text': p.empresa, 'codigo': p.codigo}
            for p in proveedores
        ]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Método inválido'}, status=405)


def buscar_proveedores(request):
    if request.method == "GET":
        proveedor_codigo = request.GET.get("codigo")
        proveedor = Clientes.objects.filter(codigo=proveedor_codigo).first()

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

def buscar_item_c(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()
        servicios = Servicios.objects.filter(nombre__icontains=query, tipogasto='C')[:10]
        results = [{'id': servicio.id, 'text': servicio.nombre} for servicio in servicios]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)

def buscar_items_c(request):
    if request.method == "GET":
        servicio_id = request.GET.get("id")
        servicio = Servicios.objects.filter(id=servicio_id, tipogasto='C').first()

        if servicio:
            iva_texto = "Exento" if servicio.tasa == "X" else "Básico" if servicio.tasa == "B" else "Desconocido"
            embarque_texto = "Pendiente" if servicio.imputar == "S" else "No imputar" if servicio.imputar == "N" else "Desconocido"

            data = {
                'item': servicio.codigo,
                'nombre': servicio.nombre,
                'iva': iva_texto,
                'cuenta': servicio.contable,
                'embarque': embarque_texto,
                'comp': servicio.activa,
                'gasto': servicio.modo,
                'imputar': servicio.imputar
            }
            return JsonResponse(data)

    return JsonResponse({'error': 'Servicio no encontrado'}, status=404)


def procesar_factura_proveedor(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':

                hora = datetime.now().strftime('%H%M%S%f')
                fecha = request.POST.get('fecha')
                tipo = request.POST.get('tipoFac', 0)
                numero = request.POST.get('numero', 0)

                autogenerado=generar_autogenerado(tipo, hora, fecha, numero)
                master=None
                house=None
                posicion=None
                kilos=None
                bultos=None
                terminos=None
                pagoflete=None
                origen=None
                destino=None
                seguimiento=None

                serie = request.POST.get('serie', "")
                detalle = request.POST.get('detalle', "")
                prefijo = request.POST.get('prefijo', 1)
                moneda = request.POST.get('moneda', "")
                arbitraje = request.POST.get('arbitraje', 0)
                paridad = request.POST.get('paridad', 0)
                cliente_data = json.loads(request.POST.get('clienteData'))
                facturas_json = request.POST.get('facturas_imputadas')
                if facturas_json:
                    facturas_imputadas = json.loads(facturas_json)
                else:
                    facturas_imputadas = []

                saldo_nota_cred = request.POST.get('saldo_nota_cred', 0)
                codigo_cliente = cliente_data['codigo']
                cliente = Clientes.objects.get(codigo=codigo_cliente)
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')

                precio_total = request.POST.get('total', 0)
                neto = request.POST.get('neto', 0)
                iva = request.POST.get('iva', 0)

                items_data = json.loads(request.POST.get('items'))

                tipo_mov = tipo
                tipo_asiento = 'V'
                detalle1 = 'S/I'
                detalle_mov = ""
                nombre_mov = ""
                asiento = generar_numero()
                movimiento_num = modificar_numero(asiento)


                if int(tipo) == 10:
                    detalle1 = 'VTA/CRED'
                    tipo_asiento = 'V'
                    nombre_mov = 'CONTADO'
                elif int(tipo) == 11:
                    detalle1 = 'DEV/CTDO'
                    tipo_asiento='V'
                    nombre_mov = 'DEVOLUCION'
                elif int(tipo) == 41:
                    detalle1 = 'NOT/CRED'
                    tipo_asiento = 'P'
                    nombre_mov = 'NOTA CRED.'
                elif int(tipo) == 40:
                    detalle1 = 'CPRA/CRED'
                    tipo_asiento = 'P'
                    nombre_mov = 'FACTURA'

                if int(tipo)==41 and facturas_imputadas:
                    for fac_i in facturas_imputadas:

                        impuc=Impucompras()
                        impuc.autogen=str(autogenerado)
                        impuc.cliente=codigo_cliente
                        impuc.monto=fac_i.get('monto_imputado')
                        impuc.autofac=fac_i.get('autogenerado')
                        impuc.save()

                        fac=Movims.objects.filter(mautogen=fac_i.get('autogenerado'),mtipo=40).first()
                        # fac.msaldo=fac.msaldo - float(fac_i.get('monto_imputado'))
                        fac.msaldo = (float(fac.msaldo) if fac.msaldo else 0) - float(fac_i.get('monto_imputado'))
                        fac.save()

                detalle_asiento = detalle1 + '-' + serie + '-' + str(prefijo) + '-' + str(numero) + '-' + cliente.empresa


                asiento_general = {
                    'detalle': detalle_asiento,
                    'asiento': asiento,
                    'monto': precio_total,
                    'moneda': moneda,
                    'cambio': arbitraje,
                    'conciliado': 'N',
                    'clearing': fecha_obj,
                    'fecha': fecha_obj,
                    'imputacion': 2,
                    'tipo': tipo_asiento,
                    'cuenta': cliente.ctacomp,
                    'documento': str(numero),
                    'vencimiento': fecha_obj,
                    'pasado': 0,
                    'autogenerado': autogenerado,
                    'cliente': cliente.codigo,
                    'banco': 'S/I',
                    'centro': 'S/I',
                    'mov': movimiento_num,
                    'anio': fecha_obj.year,
                    'mes': fecha_obj.month,
                    'fechacheque': fecha_obj,
                    'paridad': paridad,
                    'posicion':'S/I',
                    'nroserv': 0,

                }

                crear_asiento(asiento_general)

                coniva = 0
                totaliva = 0


                for item_data in items_data:
                    #aux = int(movimiento_num) + 1

                    precio = float(item_data.get('precio'))
                    key = False
                    if item_data.get('iva') == 'Basico':
                        coniva = precio * 1.22
                        totaliva = precio * 0.22
                        key = True
                    else:
                        coniva = precio
                        totaliva = 0
                        key = False

                    if key==True:
                        iva_total_asiento = {
                            'detalle': detalle_asiento,
                            'monto': totaliva,
                            'moneda': moneda,
                            'cambio': arbitraje,
                            'asiento': asiento,
                            'conciliado': 'N',
                            'clearing': fecha_obj,
                            'fecha': fecha_obj,
                            'imputacion': 1,
                            'tipo': tipo_asiento,
                            'cuenta': item_data.get('cuenta'),
                            'documento': str(numero),
                            'vencimiento': fecha_obj,
                            'pasado': 0,
                            'autogenerado': autogenerado,
                            'cliente': cliente.codigo,
                            'banco': 'S/I',
                            'centro': 'S/I',
                            'mov': movimiento_num,
                            'anio': fecha_obj.year,
                            'mes': fecha_obj.month,
                            'fechacheque': fecha_obj,
                            'paridad': paridad,
                            'posicion': item_data.get('posicion'),
                            'nroserv': item_data.get('id'),
                        }
                        monto_original_asiento = {
                            'detalle': detalle_asiento,
                            'monto': precio,
                            'moneda': moneda,
                            'cambio': arbitraje,
                            'asiento': asiento,
                            'conciliado': 'N',
                            'clearing': fecha_obj,
                            'fecha': fecha_obj,
                            'imputacion': 1,
                            'tipo': tipo_asiento,
                            'cuenta': item_data.get('cuenta'),
                            'documento': str(numero),
                            'vencimiento': fecha_obj,
                            'pasado': 0,
                            'autogenerado': autogenerado,
                            'cliente': cliente.codigo,
                            'banco': 'S/I',
                            'centro': 'S/I',
                            'mov': movimiento_num,
                            'anio': fecha_obj.year,
                            'mes': fecha_obj.month,
                            'fechacheque': fecha_obj,
                            'paridad': paridad,
                            'posicion': item_data.get('posicion'),
                            'nroserv': item_data.get('id'),
                        }

                        crear_asiento(iva_total_asiento)
                        crear_asiento(monto_original_asiento)
                    else:
                        asiento_vector = {
                            'detalle': detalle_asiento,
                            'monto': precio,
                            'moneda': moneda,
                            'cambio': arbitraje,
                            'asiento': asiento,
                            'conciliado': 'N',
                            'clearing': fecha_obj,
                            'fecha': fecha_obj,
                            'imputacion': 1,
                            'tipo': tipo_asiento,
                            'cuenta': item_data.get('cuenta'),
                            'documento': str(numero),
                            'vencimiento': fecha_obj,
                            'pasado': 0,
                            'autogenerado': autogenerado,
                            'cliente': cliente.codigo,
                            'banco': 'S/I',
                            'centro': 'S/I',
                            'mov': movimiento_num,
                            'anio': fecha_obj.year,
                            'mes': fecha_obj.month,
                            'fechacheque': fecha_obj,
                            'paridad': paridad,
                            'posicion': item_data.get('posicion'),
                            'nroserv': item_data.get('id'),

                        }
                        crear_asiento(asiento_vector)

                    #movimiento_num = aux

                movimiento = {
                    'tipo': tipo_mov,
                    'fecha': fecha_obj,
                    'boleta': numero,
                    'monto': precio_total,
                    'iva': totaliva,
                    'total': precio_total,
                    'saldo': precio_total if int(tipo) !=41 else saldo_nota_cred,
                    'moneda': moneda,
                    'detalle': detalle,
                    'cliente': cliente.codigo,
                    'nombre': cliente.empresa,
                    'nombremov': nombre_mov,
                    'cambio': arbitraje,
                    'autogenerado': autogenerado,
                    'serie': serie,
                    'prefijo': prefijo,
                    'posicion': posicion,
                    'anio': fecha_obj.year,
                    'mes': fecha_obj.month,
                    'monedaoriginal': moneda,
                    'montooriginal': precio_total,
                    'arbitraje': arbitraje
                }
                crear_movimiento(movimiento)

                return JsonResponse({'status': 'Factura procesada correctamente N° ' + str(numero)})
            return None
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
        lista.posicion = asiento['posicion']
        lista.nroserv = asiento['nroserv']
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

def source_proveedoresygastos(request):
    try:
        args = {
            '1': request.GET['columns[1][search][value]'],
            '2': request.GET['columns[2][search][value]'],
            '3': request.GET['columns[3][search][value]'],
            '4': request.GET['columns[4][search][value]'],
            '5': request.GET['columns[5][search][value]'],
            '6': request.GET['columns[6][search][value]'],
            '7': request.GET['columns[7][search][value]'],
            '8': request.GET['columns[8][search][value]'],
        }

        # Filtros y lógica de búsqueda
        filtro = get_argumentos_busqueda(**args)
        order = get_order(request, columns_table)
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        buscar = request.GET.get('buscar', '')
        que_buscar = request.GET.get('que_buscar', '')

        if buscar:
            filtro[que_buscar] = buscar

        end = start + length

        # Consulta a la base de datos
        if filtro:
            registros = VistaProveedoresygastos.objects.filter(**filtro).order_by(*order)
        else:
            registros = VistaProveedoresygastos.objects.all().order_by(*order)

        # Preparación de la respuesta
        resultado = {
            'data': get_data(registros[start:end]),
            'length': length,
            'draw': request.GET.get('draw', '1'),
            'recordsTotal': VistaProveedoresygastos.objects.count(),
            'recordsFiltered': registros.count(),
        }
        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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
        result.append('fecha')
        return result
    except Exception as e:
        raise TypeError(e)

def get_data(registros_filtrados):
    try:
        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(registro.tipo)
            registro_json.append('' if registro.autogenerado is None else str(registro.autogenerado))
            registro_json.append('' if registro.fecha is None else registro.fecha.strftime('%Y-%m-%d'))
            registro_json.append('' if registro.num_completo is None else str(registro.num_completo))
            registro_json.append('' if registro.cliente is None else str(registro.cliente))
            registro_json.append('' if registro.posicion is None else str(registro.posicion))
            registro_json.append('' if registro.monto is None else str(registro.monto))
            registro_json.append('' if registro.iva is None else str(registro.iva))
            registro_json.append('' if registro.total is None else str(registro.total))
            registro_json.append('' if registro.nrocliente is None else str(registro.nrocliente))
            registro_json.append('' if registro.numero is None else str(registro.numero))
            data.append(registro_json)
        return data
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


def cargar_pendientes_imputacion(request):
    try:
        nrocliente = request.GET.get('nrocliente', None)

        if not nrocliente:
            return JsonResponse({'error': 'Debe proporcionar un nrocliente'}, status=400)

        registros = VistaProveedoresygastos.objects.filter(
            nrocliente=nrocliente,
            tipo='FACTURA'
        ).exclude(saldo=0)

        data = []
        for registro in registros:
            data.append({
                'autogenerado': registro.autogenerado,
                'vto': registro.fecha.strftime('%Y-%m-%d') if registro.fecha else '',
                'emision': registro.fecha.strftime('%Y-%m-%d') if registro.fecha else '',
                'num_completo': registro.num_completo,
                'total': float(registro.total) if registro.total else 0,
                'saldo': float(registro.saldo) if registro.saldo else 0,
                'imputado': 0,
                'tipo_cambio': float(registro.tipo_cambio) if registro.tipo_cambio else 0,
                'detalle': registro.detalle if registro.detalle else '',
            })

        # Retornar los datos en formato JSON sin paginación
        return JsonResponse({'data': data}, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def obtener_proximo_mboleta_compra(request):
    try:
        ultima = Movims.objects.filter(mtipo__in=[40, 41, 10, 11]).order_by('-id').first()
        proximo = int(ultima.mboleta) + 1 if ultima and ultima.mboleta.isdigit() else 1
        return JsonResponse({'proximo_mboleta': str(proximo)})
    except Exception as e:
        return JsonResponse({'error': f'Error al obtener mboleta: {str(e)}'}, status=500)