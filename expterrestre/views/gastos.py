from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse

from administracion_contabilidad.models import Boleta, Impuvtas
from consultas_administrativas.views.utilidad_mensual_posicion import normalizar_numero
from expterrestre.models import ExpterraServireserva, VGastosMaster, VGastosHouse, ExpterraServiceaereo
import json


columns_table = {
    1: 'servicio',
    2: 'moneda',
    3: 'precio',
    4: 'costo',
    5: 'detalle',
    6: 'modo',
    7: 'tipogasto',
    8: 'arbitraje',
    9: 'notomaprofit',
    10: 'secomparte',
    11: 'pinformar',
    12: 'socio',
    13: 'notas',
}
def source_gastos(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        """PROCESO FILTRO Y ORDEN BY"""
        start = int(request.GET['start'])
        numero = request.GET['numero']
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        registros = VGastosMaster.objects.filter(numero=numero).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data_master(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = VGastosMaster.objects.filter(numero=numero).count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)
def source_gastos_house_preventa(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        """PROCESO FILTRO Y ORDEN BY"""
        start = int(request.GET['start'])
        numero = request.GET['numero']
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        registros = VGastosHouse.objects.filter(numero=numero).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data_preventa(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = VGastosHouse.objects.filter(numero=numero).count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)
def source_gastos_house(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        """PROCESO FILTRO Y ORDEN BY"""
        start = int(request.GET['start'])
        numero = request.GET['numero']
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        registros = VGastosHouse.objects.filter(numero=numero).order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = VGastosHouse.objects.filter(numero=numero).count()
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
            registro_json.append('' if registro.servicio is None else str(registro.servicio))
            registro_json.append('' if registro.moneda is None else str(registro.moneda))
            registro_json.append('' if registro.precio is None else str(registro.precio))
            registro_json.append('' if registro.costo is None else str(registro.costo))
            registro_json.append('' if registro.detalle is None else str(registro.detalle))
            registro_json.append('' if registro.modo is None else str(registro.modo))
            registro_json.append('' if registro.tipogasto is None else str(registro.tipogasto))
            registro_json.append('' if registro.arbitraje is None else str(registro.arbitraje))
            registro_json.append('' if registro.notomaprofit is None else str(registro.notomaprofit))
            registro_json.append('' if registro.secomparte is None else str(registro.secomparte))
            registro_json.append('' if registro.pinformar is None else str(registro.pinformar))
            registro_json.append('' if registro.socio is None else str(registro.socio))
            registro_json.append('' if registro.notas is None else str(registro.notas))
            registro_json.append('' if registro.id_servicio is None else str(registro.id_servicio))
            registro_json.append('' if registro.id_moneda is None else str(registro.id_moneda))
            registro_json.append('' if registro.id_socio is None else str(registro.id_socio))
            color = 'NINGUNO'
            numero = 'S/I'
            if registro.detalle is not None and registro.detalle != 'S/I' and registro.detalle != '':
                color = 'AMARILLO'
                se_facturo = Boleta.objects.filter(autogenerado=registro.detalle).exists()
                if se_facturo:
                    color = 'ROJO'
                    boleta = Boleta.objects.only('numero', 'serie', 'prefijo', 'cliente', 'fecha').filter(
                        autogenerado=registro.detalle).first()
                    fecha = boleta.fecha.strftime('%d/%m/%Y') if boleta.fecha is not None else None
                    fecha = fecha if fecha is not None else 'S/I'
                    numero = f"{boleta.serie}{boleta.prefijo}-{str(normalizar_numero(boleta.numero))}  ({fecha}) - {boleta.cliente}"

                    se_cobro = Impuvtas.objects.filter(autofac=registro.detalle).exists()
                    if se_cobro:
                        color = 'VERDE'

            registro_json.append(color)
            registro_json.append(numero)
            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)

def get_data_preventa(registros_filtrados):
    try:

        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.servicio is None else str(registro.servicio))
            registro_json.append('' if registro.moneda is None else str(registro.moneda))
            registro_json.append('' if registro.precio is None else str(registro.precio))
            registro_json.append('' if registro.costo is None else str(registro.costo))
            registro_json.append('' if registro.detalle is None else str(registro.detalle))
            registro_json.append('' if registro.modo is None else str(registro.modo))
            registro_json.append('' if registro.tipogasto is None else str(registro.tipogasto))
            registro_json.append('' if registro.arbitraje is None else str(registro.arbitraje))
            registro_json.append('' if registro.notomaprofit is None else str(registro.notomaprofit))
            registro_json.append('' if registro.secomparte is None else str(registro.secomparte))
            registro_json.append('' if registro.pinformar is None else str(registro.pinformar))
            registro_json.append('' if registro.socio is None else str(registro.socio))
            registro_json.append('' if registro.notas is None else str(registro.notas))
            registro_json.append('' if registro.id_servicio is None else str(registro.id_servicio))
            registro_json.append('' if registro.id_moneda is None else str(registro.id_moneda))
            registro_json.append('' if registro.id_socio is None else str(registro.id_socio))
            color = 'NINGUNO'
            numero = 'S/I'
            if registro.detalle is not None and registro.detalle != 'S/I' and registro.detalle != '':
                color = 'AMARILLO'
                se_facturo = Boleta.objects.filter(autogenerado=registro.detalle).exists()
                if se_facturo:
                    color = 'ROJO'
                    boleta = Boleta.objects.only('numero', 'serie', 'prefijo', 'cliente', 'fecha').filter(
                        autogenerado=registro.detalle).first()
                    fecha = boleta.fecha.strftime('%d/%m/%Y') if boleta.fecha is not None else None
                    fecha = fecha if fecha is not None else 'S/I'
                    numero = f"{boleta.serie}{boleta.prefijo}-{str(normalizar_numero(boleta.numero))}  ({fecha}) - {boleta.cliente}"
                    se_cobro = Impuvtas.objects.filter(autofac=registro.detalle).exists()
                    if se_cobro:
                        color = 'VERDE'


            registro_json.append(color)
            registro_json.append(numero)
            data.append(registro_json)
        return data
    except Exception as e:
        raise TypeError(e)

def get_data_master(registros_filtrados):
    try:

        data = []
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.servicio is None else str(registro.servicio))
            registro_json.append('' if registro.moneda is None else str(registro.moneda))
            registro_json.append('' if registro.precio is None else str(registro.precio))
            registro_json.append('' if registro.costo is None else str(registro.costo))
            registro_json.append('' if registro.detalle is None else str(registro.detalle))
            registro_json.append('' if registro.modo is None else str(registro.modo))
            registro_json.append('' if registro.tipogasto is None else str(registro.tipogasto))
            registro_json.append('' if registro.arbitraje is None else str(registro.arbitraje))
            registro_json.append('' if registro.notomaprofit is None else str(registro.notomaprofit))
            registro_json.append('' if registro.pinformar is None else str(registro.pinformar))
            registro_json.append('' if registro.socio is None else str(registro.socio))
            registro_json.append('' if registro.notas is None else str(registro.notas))
            registro_json.append('' if registro.id_servicio is None else str(registro.id_servicio))
            registro_json.append('' if registro.id_moneda is None else str(registro.id_moneda))
            registro_json.append('' if registro.id_socio is None else str(registro.id_socio))
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


def add_gasto_master(request):
    resultado = {}
    try:
        # Recibir los datos JSON enviados por AJAX
        data = json.loads(request.POST.get('data'))

        # Crear un diccionario para acceder fácilmente a los valores
        form_data = {item['name']: item['value'] for item in data}

        # Acceder a los valores del formulario usando el diccionario
        numero = form_data.get('numero')
        servicio = form_data.get('servicio')
        moneda = form_data.get('moneda')
        costo = form_data.get('costo')
        arbitraje = form_data.get('arbitraje', 0)  # valor opcional
        tipogasto = form_data.get('tipogasto')
        pinformar = form_data.get('pinformar', 0)  # valor opcional
        notomaprofit = form_data.get('notomaprofit') == 'on'
        modo = form_data.get('modo')
        socio = form_data.get('socio')
        detalle = form_data.get('detalle')
        prorrateo = form_data.get('prorrateo')
        empresa = form_data.get('empresa')
        reembolsable = form_data.get('reembolsable')

        # Verificar si el registro ya existe
        if 'id_gasto_id' in form_data and form_data['id_gasto_id']:
            # Modificar el registro existente
            registro = ExpterraServireserva.objects.get(id=form_data['id_gasto_id'])
        else:
            # Crear un nuevo registro si no existe
            registro = ExpterraServireserva()

        # Actualizar o crear el registro con los datos del formulario
        registro.numero = numero
        registro.servicio = servicio
        registro.moneda = moneda
        registro.costo = costo if costo else 0
        registro.arbitraje = arbitraje
        registro.tipogasto = tipogasto
        registro.pinformar = pinformar
        registro.notomaprofit = notomaprofit
        registro.modo = modo
        registro.socio = socio
        registro.detalle = detalle
        registro.prorrateo = prorrateo
        registro.empresa = empresa
        registro.reembolsable = reembolsable

        # Guardar el registro en la base de datos
        registro.save()

        # Devolver el resultado de éxito
        resultado['resultado'] = 'exito'
        resultado['numero'] = registro.numero

    except ExpterraServireserva.DoesNotExist:
        resultado['resultado'] = 'Registro no encontrado.'
    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)

    # Retornar el resultado en formato JSON
    return JsonResponse(resultado)

def eliminar_gasto_master(request):
    resultado = {}
    try:
        id = request.POST['id']
        ExpterraServireserva.objects.get(id=id).delete()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def add_gasto_house(request):
    resultado = {}
    try:
        # Recibir los datos JSON enviados por AJAX
        data = json.loads(request.POST.get('data'))

        # Crear un diccionario para acceder fácilmente a los valores
        form_data = {item['name']: item['value'] for item in data}

        # Acceder a los valores del formulario usando el diccionario
        numero = form_data.get('numero')
        servicio = form_data.get('servicio')
        secomparte = form_data.get('secomparte')
        moneda = form_data.get('moneda')
        costo = form_data.get('costo')
        precio = form_data.get('precio')
        arbitraje = form_data.get('arbitraje', 0)  # valor opcional
        tipogasto = form_data.get('tipogasto')
        pinformar = form_data.get('pinformar', 0)  # valor opcional
        notomaprofit = form_data.get('notomaprofit') == 'on'
        modo = form_data.get('modo')
        socio = form_data.get('socio')
        detalle = form_data.get('detalle')
        empresa = form_data.get('empresa',0)
        reembolsable = form_data.get('reembolsable')

        # Verificar si el registro ya existe
        if 'id_gasto_id_house' in form_data and form_data['id_gasto_id_house']:
            # Modificar el registro existente
            registro = ExpterraServiceaereo.objects.get(id=form_data['id_gasto_id_house'])

        else:
            # Crear un nuevo registro si no existe
            registro = ExpterraServiceaereo()

        registro.numero = numero
        registro.servicio = servicio
        registro.secomparte = secomparte
        registro.moneda = moneda
        registro.costo = costo if costo else 0
        registro.precio = precio if precio else 0
        registro.arbitraje = arbitraje
        registro.tipogasto = tipogasto
        registro.pinformar = pinformar
        registro.notomaprofit = notomaprofit
        registro.modo = modo
        registro.socio = socio
        registro.detalle = detalle
        registro.empresa = empresa
        registro.reembolsable = reembolsable

        registro.save()
        # Devolver el resultado de éxito
        resultado['resultado'] = 'exito'
        resultado['numero'] = registro.numero

    except ExpterraServireserva.DoesNotExist:
        resultado['resultado'] = 'Registro no encontrado.'
    except IntegrityError:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)

    # Retornar el resultado en formato JSON
    return JsonResponse(resultado)

def add_gasto_importado(request):
    try:
        if request.method == 'POST':
            # Asumimos que el array de datos llega en formato JSON
            data = json.loads(request.body)

            if isinstance(data, list):
                # Iteramos sobre cada elemento en la lista
                for gasto_data in data:
                    # Crear la instancia de ImpterraServiceaereo para cada registro
                    registro = ExpterraServiceaereo()

                    # Asignar los valores desde el JSON al modelo
                    registro.numero = gasto_data.get('numero')
                    registro.servicio = gasto_data.get('servicio')
                    registro.secomparte = gasto_data.get('secomparte')
                    registro.moneda = gasto_data.get('moneda')
                    registro.costo = gasto_data.get('costo')
                    registro.precio = gasto_data.get('precio')
                    registro.arbitraje = gasto_data.get('arbitraje')
                    registro.tipogasto = gasto_data.get('tipogasto')
                    registro.pinformar = gasto_data.get('pinformar')
                    registro.notomaprofit = gasto_data.get('notomaprofit')
                    registro.modo = gasto_data.get('modo')
                    registro.socio = gasto_data.get('socio')
                    registro.detalle = gasto_data.get('detalle')

                    # Guardar el registro en la base de datos
                    registro.save()


                return JsonResponse({'success': True, 'message': 'Todos los gastos agregados con éxito'})
            else:
                return JsonResponse({'success': False, 'message': 'Los datos enviados no son una lista válida.'})

        else:
            return JsonResponse({
                'success': False,
                'message': 'Método no permitido.'
            })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Ocurrió un error: {str(e)}',
            'errors': {}
        })


def eliminar_gasto_house(request):
    resultado = {}
    try:
        id = request.POST['id']
        ExpterraServiceaereo.objects.get(id=id).delete()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)
