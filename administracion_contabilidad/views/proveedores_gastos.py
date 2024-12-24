import json
from datetime import datetime

from django.db import transaction
from django.shortcuts import render

from administracion_contabilidad.models import Movims, Asientos, VistaProveedoresygastos
from administracion_contabilidad.views.facturacion import generar_autogenerado, generar_numero, modificar_numero
from mantenimientos.models import Clientes, Servicios
from administracion_contabilidad.forms import ProveedoresGastos
from django.http import JsonResponse
param_busqueda = {
    0: 'autogenerado__icontains',
    1: 'numero__icontains',
    2: 'detalle__icontains',
    3: 'tipo__icontains',
    4: 'monto__icontains',
    5: 'iva__icontains',
    6: 'total__icontains',
}

columns_table = {
    0: 'autogenerado',
    1: 'numero',
    2: 'detalle',
    3: 'tipo',
    4: 'monto',
    5: 'iva',
    6: 'total',
}


def proveedores_gastos_view(request):
    form = ProveedoresGastos(request.POST or None)

    return render(request, 'proveedores_gastos.html', {'form': form})


def buscar_proveedor(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('term', '').strip()  # Obtener y limpiar el término de búsqueda
        proveedores = Clientes.objects.filter(empresa__icontains=query)[:10]  # Limitar resultados a 10
        results = [{'id': proveedor.id, 'text': proveedor.empresa} for proveedor in proveedores]
        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def buscar_proveedores(request):
    if request.method == "GET":
        proveedor_id = request.GET.get("id")
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
            }
            return JsonResponse(data)

    return JsonResponse({'error': 'Servicio no encontrado'}, status=404)


@transaction.atomic
def procesar_factura_proveedor(request):
    try:
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
            prefijo = request.POST.get('prefijo', 0)
            moneda = request.POST.get('moneda', "")
            arbitraje = request.POST.get('arbitraje', 0)
            paridad = request.POST.get('paridad', 0)
            cliente_data = json.loads(request.POST.get('clienteData'))
            codigo_cliente = cliente_data['codigo']
            cliente = Clientes.objects.get(codigo=codigo_cliente)
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')

            precio_total = request.POST.get('total', 0) #con iva
            neto = request.POST.get('neto', 0) #sin iva
            iva = request.POST.get('iva', 0)

            items_data = json.loads(request.POST.get('items'))

            tipo_mov = tipo
            tipo_asiento = 'V'
            detalle1 = 'S/I'
            detalle_mov = "detallemov"  #va a tener un house asociado
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
                'cuenta': 0,
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
                'paridad': paridad
            }
            crear_asiento(asiento_general)

            for item_data in items_data:
                aux = int(movimiento_num) + 1

                precio = float(item_data.get('precio'))
                coniva = 0
                totaliva = 0
                key = False
                if item_data.get('iva') == 'Basico':
                    coniva = precio * 1.22
                    totaliva = precio * 0.22
                    key = True
                else:
                    coniva = precio
                    totaliva = 0
                    key = False

                movimiento = {
                    'tipo': tipo_mov,
                    'fecha': fecha_obj,
                    'boleta': numero,
                    'monto': precio,
                    'iva': totaliva,
                    'total': coniva,
                    'saldo': coniva,
                    'moneda': moneda,
                    'detalle': detalle_mov,
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
                        'mov': aux,
                        'anio': fecha_obj.year,
                        'mes': fecha_obj.month,
                        'fechacheque': fecha_obj,
                        'paridad': paridad
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
                        'mov': aux,
                        'anio': fecha_obj.year,
                        'mes': fecha_obj.month,
                        'fechacheque': fecha_obj,
                        'paridad': paridad
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
                        'mov': aux,
                        'anio': fecha_obj.year,
                        'mes': fecha_obj.month,
                        'fechacheque': fecha_obj,
                        'paridad': paridad
                    }
                    crear_asiento(asiento_vector)

                movimiento_num = aux

            return JsonResponse({'status': 'Factura procesada correctamente N° ' + str(numero)})
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
        lista.save()

    except Exception as e:
        return JsonResponse({'status': 'Error: ' + str(e)})

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
        lista.mmontooriginal = movimiento['montooriginal']
        lista.save()

    except Exception as e:
        return JsonResponse({'status': 'Error:' + str(e)})

def source_proveedoresygastos(request):
    try:
        # Usar un bucle para recoger dinámicamente las columnas que existen
        args = {}
        for i in range(10):  # Cambia el rango según el número de columnas reales
            key = f'columns[{i}][search][value]'
            args[str(i)] = request.GET.get(key, '')  # Usa un valor predeterminado si la clave no existe

        # Filtros y lógica de búsqueda
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        buscar = request.GET.get('buscar', '')
        que_buscar = request.GET.get('que_buscar', '')

        if buscar:
            filtro[que_buscar] = buscar

        end = start + length

        # Consulta a la base de datos
        if filtro:
            registros = VistaProveedoresygastos.objects.filter(**filtro).order_by()
        else:
            registros = VistaProveedoresygastos.objects.all().order_by()

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


def get_data(registros_filtrados):
    try:
        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append('' if registro.autogenerado is None else str(registro.autogenerado))
            registro_json.append('' if registro.numero is None else str(registro.numero))
            registro_json.append('' if registro.detalle is None else str(registro.detalle))
            registro_json.append('' if registro.tipo is None else str(registro.tipo))
            registro_json.append('' if registro.monto is None else str(registro.monto))
            registro_json.append('' if registro.iva is None else str(registro.iva))
            registro_json.append('' if registro.total is None else str(registro.total))
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