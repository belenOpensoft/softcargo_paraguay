import json
import simplejson
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from mantenimientos.models import Productos
from seguimientos.models import Cargaaerea, VCargaaerea, VGrillaSeguimientos, Seguimiento

""" TABLA PUERTO """
columns_table = {
    1: 'id',
    2: 'producto',
    3: 'bultos',
    4: 'tipo',
    5: 'bruto',
    6: 'medidas',
    7: 'cbm',
    8: 'mercaderia',
    9: 'materialreceipt',
}

def source_embarques(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        """PROCESO FILTRO Y ORDEN BY"""
        start = int(request.GET['start'])
        numero = request.GET['numero']
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        registros = Cargaaerea.objects.filter(numero=numero).order_by(*order)
        se = VGrillaSeguimientos.objects.get(numero=numero)
        data_extra = {
            'tarifaprofit': float(se.tarifaprofit) if se.tarifaprofit is not None else '',
            'muestroflete': float(se.muestroflete) if se.muestroflete is not None else '',
            'tarifaventa': float(se.tarifaventa) if se.tarifaventa is not None else '',
            'tarifacompra': float(se.tarifacompra) if se.tarifacompra is not None else '',
            'volumen': float(se.volumen) if se.volumen is not None else '',
            'tipobonifcli': str(se.tipobonifcli) if se.tipobonifcli is not None else '',
            'tarifafija': str(se.tarifafija) if se.tarifafija is not None else '',
            'tomopeso': float(se.tomopeso) if se.tomopeso is not None else '',
            'bonifcli': float(se.bonifcli) if se.bonifcli is not None else '',
        }
        if se.aplicable is not None:
            data_extra['aplicable'] = float(se.aplicable),
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['data_extra'] = data_extra
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Cargaaerea.objects.filter(numero=numero).count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def get_data(registros_filtrados):
    try:
        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.producto is None else str(registro.producto.nombre))
            registro_json.append('' if registro.bultos is None else str(registro.bultos))
            registro_json.append('' if registro.tipo is None else str(registro.tipo))
            registro_json.append('' if registro.bruto is None else str(registro.bruto))
            registro_json.append('' if registro.medidas is None else str(registro.medidas))
            registro_json.append('' if registro.cbm is None else str(registro.cbm))
            registro_json.append('' if registro.mercaderia is None else str(registro.mercaderia))
            registro_json.append('' if registro.materialreceipt is None else str(registro.materialreceipt))
            registro_json.append('' if registro.producto is None else str(registro.producto.codigo))
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
        result.append('id')
        return result
    except Exception as e:
        raise TypeError(e)

def is_ajax(request):
    try:
        req = request.META.get('HTTP_X_REQUESTED_WITH')
        # return req == 'XMLHttpRequest'
        return True
    except Exception as e:
        messages.error(request,e)

def get_sugerencias_envases(request, numero):
    try:
        carga = Cargaaerea.objects.filter(numero=numero).first()

        data = {
            'bultos': carga.bultos,
            'bruto': carga.bruto,
            'nrocontenedor': carga.nrocontenedor,
            'cbm': carga.cbm
        }

        return JsonResponse({'status': 'success', 'data': data})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url='/login/')
def guardar_embarques(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        data = simplejson.loads(request.POST['data'])
        seg = Seguimiento.objects.get(numero=numero)
        registro = Cargaaerea()
        campos = vars(registro)

        for x in data:
            k = x['name']
            v = x['value']

            # Tratamiento especial para cod_producto
            if k == 'cod_producto' and v:
                try:
                    producto = Productos.objects.get(codigo=v)
                    setattr(registro, 'producto', producto)
                except Productos.DoesNotExist:
                    resultado['resultado'] = 'El producto con ese código no existe.'
                    data_json = json.dumps(resultado)
                    return HttpResponse(data_json, content_type="application/json")
                continue  # Evita que se reescriba más abajo

            # Evita sobrescribir el campo producto si viene duplicado
            if k == 'producto':
                continue

            for name in campos:
                if name == k:
                    if v is not None and len(v) > 0:
                        setattr(registro, name, v)
                    else:
                        setattr(registro, name, None)
                    break

        registro.numero = numero
        registro.save()

        # ACTUALIZO DATOS EN SEGUIMIENTO
        volumen = 0
        montoflete = 0
        aplicable = 0
        data_extra = simplejson.loads(request.POST['data_extra'])
        registros = Cargaaerea.objects.filter(numero=numero)

        for x in registros:
            if x.cbm is not None:
                volumen += x.cbm

            if data_extra[1]['value'] == '1':
                montoflete += redondear_a_05_o_0(float(x.bruto)) * float(data_extra[3]['value'])
                aplicable += float(x.bruto)
            elif data_extra[1]['value'] == '2':
                try:
                    params = x.medidas.split('*')
                    value = float(params[0]) * float(params[1]) * float(params[2])
                    ap = redondear_a_05_o_0(value * 166.67)
                    aplicable += ap
                    montoflete += ap * float(data_extra[3]['value'])
                except:
                    aplicable += 0

        seg.volumen = volumen
        seg.muestroflete = montoflete
        seg.aplicable = redondear_a_05_o_0(aplicable)
        seg.tomopeso = data_extra[1]['value']
        seg.tarifaprofit = data_extra[8]['value']
        seg.tarifacompra = data_extra[5]['value']
        seg.tarifaventa = data_extra[3]['value']
        seg.save()

        resultado['resultado'] = 'exito'
        resultado['numero'] = str(registro.numero)

    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)

    return HttpResponse(json.dumps(resultado), content_type="application/json")

@login_required(login_url='/login/')
def guardar_embarques_old(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        data = simplejson.loads(request.POST['data'])
        seg = Seguimiento.objects.get(numero=numero)
        registro = VCargaaerea()
        campos = vars(registro)
        for x in data:
            k = x['name']
            v = x['value']
            for name in campos:
                if name == k:
                    if v is not None and len(v) > 0:
                        if v is not None:
                            setattr(registro, name, v)
                        else:
                            if len(v) > 0:
                                setattr(registro, name, v)
                    else:
                        setattr(registro, name, None)
                    continue
        registro.numero = numero
        registro.save()
        """ ACTUALIZO DATOS EN SEGUIMIENTO """
        volumen = 0
        montoflete = 0
        aplicable = 0
        data_extra = simplejson.loads(request.POST['data_extra'])
        registros = Cargaaerea.objects.filter(numero=numero)
        for x in registros:
            if x.cbm is not None:
                volumen += x.cbm
            if data_extra[1]['value'] == '1':
                montoflete += redondear_a_05_o_0(float(x.bruto)) * float(data_extra[3]['value'])
                aplicable += float(x.bruto)
            elif data_extra[1]['value'] == '2':
                try:
                    params = x.medidas.split('*')
                    value = float(params[0]) * float(params[1]) * float(params[2])
                    ap = redondear_a_05_o_0(value * 166.67)
                    aplicable += ap
                    montoflete += ap * float(data_extra[3]['value'])
                except:
                    aplicable += 0
        seg.volumen = volumen
        seg.muestroflete = montoflete
        seg.aplicable = redondear_a_05_o_0(aplicable)
        seg.tomopeso = data_extra[1]['value']
        seg.tarifaprofit = data_extra[8]['value']
        seg.tarifacompra = data_extra[5]['value']
        # seg.numero = data_extra[7]['value']
        seg.tarifaventa = data_extra[3]['value']
        seg.save()
        resultado['resultado'] = 'exito'
        resultado['numero'] = str(registro.numero)
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def redondear_a_05_o_0(numero):
    # Redondea el número a 1 decimal
    numero_redondeado = round(numero, 1)

    # Calcula la parte decimal
    parte_decimal = numero_redondeado - int(numero_redondeado)

    # Redondea al valor más cercano a 0.5 o 0
    if parte_decimal < 0.25:
        return int(numero_redondeado)
    elif parte_decimal < 0.75:
        return int(numero_redondeado) + 0.5
    else:
        return int(numero_redondeado) + 1

def actualizo_datos_embarque(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        data = simplejson.loads(request.POST['data'])
        seg = Seguimiento.objects.get(numero=numero)
        seg.volumen = data[0]['value']
        seg.muestroflete = data[2]['value']
        seg.aplicable = data[4]['value']
        seg.tomopeso = data[1]['value']
        seg.tarifaprofit = data[8]['value']
        seg.tarifacompra = data[5]['value']
        # seg.numero = data_extra[7]['value']
        seg.tarifaventa = data[3]['value']
        seg.save()
        resultado['resultado'] = 'exito'
        resultado['numero'] = str(numero)
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def eliminar_embarque(request):
    resultado = {}
    try:
        id = request.POST['id']
        micarga = Cargaaerea.objects.get(id=id)
        numero = micarga.numero
        micarga.delete()
        seg = Seguimiento.objects.get(numero=numero)
        data_extra = simplejson.loads(request.POST['data_extra'])
        registros = Cargaaerea.objects.filter(numero=numero)
        volumen = 0
        aplicable = 0
        montoflete = 0
        for x in registros:
            if x.cbm is not None:
                volumen += x.cbm
            if data_extra[1]['value'] == '1':
                montoflete += redondear_a_05_o_0(float(x.bruto)) * float(data_extra[3]['value'])
                aplicable += float(x.bruto)
            elif data_extra[1]['value'] == '2':
                try:
                    params = x.medidas.split('*')
                    value = float(params[0]) * float(params[1]) * float(params[2])
                    ap = redondear_a_05_o_0(value * 166.67)
                    aplicable += ap
                    montoflete += ap * float(data_extra[3]['value'])
                except:
                    aplicable += 0
        seg.volumen = volumen
        seg.muestroflete = montoflete
        seg.aplicable = redondear_a_05_o_0(aplicable)
        seg.tomopeso = data_extra[1]['value']
        seg.tarifaprofit = data_extra[8]['value']
        seg.tarifacompra = data_extra[5]['value']
        # seg.numero = data_extra[7]['value']
        seg.tarifaventa = data_extra[3]['value']
        seg.save()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)