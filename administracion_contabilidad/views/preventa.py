from datetime import datetime
from django.http import JsonResponse, HttpResponse, Http404
import json
from administracion_contabilidad.models import Infofactura
from impomarit.models import Cargaaerea, Embarqueaereo, Reservas
from mantenimientos.models import Productos
from impomarit.models import Serviceaereo


def generar_autogenerado(fecha):
    fecha = fecha.replace('-', '').replace(':', '').replace('T', '')
    qsy = 999
    aux = Infofactura.objects.last()

    try:
        numero = str(int(str(aux.autogenerado).zfill(9)[-9:]) + 1).zfill(9)
        # numero = int(aux.autogenerado[-9:]) + 1
    except AttributeError:
        numero = 1
    except TypeError:
        numero = 1

    autogenerado = f"{fecha}{qsy}{numero}"
    print(autogenerado)

    return autogenerado


def guardar_infofactura(request):
    if request.method == "POST":
        try:
            datos = json.loads(request.body.decode('utf-8'))
            fecha_str = datos.get("fecha")
            autogenerado = generar_autogenerado(fecha_str)

            if fecha_str:
                try:
                    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S")
                    fecha_formateada = fecha_obj.strftime("%d/%m/%y")

                except ValueError:
                    print("Formato de fecha no válido")

            # Asegúrate de que 'datos' sea un diccionario
            if not isinstance(datos, dict):
                return JsonResponse({"resultado": "error", "mensaje": "Los datos no son un objeto válido."}, status=400)

            # Crea una nueva instancia de Infofactura
            infofactura = Infofactura()
            infofactura.id = infofactura.get_id()
            infofactura.autogenerado = autogenerado
            infofactura.referencia = datos.get("referencia")
            infofactura.seguimiento = datos.get("seguimiento")
            infofactura.transportista = datos.get("transportista")
            infofactura.vuelo = datos.get("vuelo")
            infofactura.master = datos.get("master")
            infofactura.house = datos.get("house")
            infofactura.fecha = fecha_formateada
            infofactura.commodity = datos.get("commodity")
            infofactura.kilos = datos.get("kilos")
            infofactura.volumen = datos.get("volumen")
            infofactura.bultos = datos.get("bultos")
            infofactura.origen = datos.get("origen")
            infofactura.destino = datos.get("destino")
            infofactura.consigna = datos.get("consigna")
            infofactura.embarca = datos.get("embarca")
            infofactura.agente = datos.get("agente")
            infofactura.posicion = datos.get("posicion")
            infofactura.terminos = datos.get("terminos")
            infofactura.pagoflete = datos.get("pagoflete")
            infofactura.wr = datos.get("wr")

            # Guarda la instancia en la base de datos
            infofactura.save()

            return JsonResponse({"resultado": "exito"})
        except Exception as e:
            return JsonResponse({"resultado": "error", "mensaje": str(e)}, status=500)
    else:
        return JsonResponse({"resultado": "error", "mensaje": "Método no permitido"}, status=405)


def source_embarques_factura(request):
    numero = request.GET.get('numero')
    registros = Cargaaerea.objects.filter(numero=numero).values('producto_id')

    data = list(registros)
    data_json = json.dumps(data)

    mimetype = "application/json"
    return HttpResponse(data_json, content_type=mimetype)


def house_detail_factura(request):
    if request.method == 'GET':
        numero = request.GET.get('numero', None)
        if numero:
            try:
                house = Embarqueaereo.objects.get(numero=numero)
                data = {
                    'id': house.id,
                    'cliente_e': house.cliente,
                    'vendedor_e': house.vendedor,
                    'transportista_e': house.transportista,
                    'agente_e': house.agente,
                    'consignatario_e': house.consignatario,
                    'origen_e': house.origen,
                    'loading_e': house.loading,
                    'destino_e': house.destino,
                    'discharge_e': house.discharge,
                    'posicion_e': house.posicion,
                    'operacion_e': house.operacion,
                    'hawb_e': house.hawb,
                    'vapor_e': house.vapor,
                    'viaje_e': house.viaje,
                    'pago': house.pagoflete,
                    'moneda_e': house.moneda,
                    'arbitraje_e': house.arbitraje,
                    'demora_e': house.demora,
                    'embarcador_e': house.embarcador,
                    'armador_e': house.armador,
                    'agventas_e': house.ageventas,
                    'agcompras_e': house.agecompras,
                    'notifcliente_e': house.notifcliente,
                    'notifagente_e': house.notifagente,
                    'fecharetiro_e': house.fecharetiro,
                    'fechaembarque_e': house.fechaembarque,
                    'status_e': house.status,
                    'wreceipt_e': house.wreceipt,
                    'trackid_e': house.trackid,
                    'seguimiento': house.seguimiento,
                    'terminos':house.terminos,
                    'wr':house.wreceipt,
                }

                data['awb_e'] = house.awb if house.awb is not None else 0

                return JsonResponse(data)
            except Embarqueaereo.DoesNotExist:
                raise Http404("House does not exist")
        else:
            return JsonResponse({'error': 'No ID provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def source_master_factura(request):
    if request.method == 'GET':
        master_id = request.GET.get('master', 0)
        if master_id != 0:
            try:
                master = Reservas.objects.get(awb=master_id)
                # Convierte el objeto en un diccionario
                data = {
                    'kilos': master.kilosmadre,
                    'bultos': master.bultosmadre,
                    'volumen': master.volumen,
                }
                return JsonResponse(data)
            except Reservas.DoesNotExist:
                raise Http404("Master does not exist")
        else:
            return JsonResponse({'error': 'No ID provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_name_by_id_productos(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        if id:
            producto = Productos.objects.get(codigo=id)
            name = producto.nombre

            return JsonResponse({'name': name})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def update_gasto_house(request):
    resultado = {'exitosos': [], 'errores': []}  # Resultado de éxitos y errores
    try:
        # Recibir y decodificar los datos JSON enviados por AJAX
        data = json.loads(request.body.decode('utf-8'))

        # Iterar sobre el vector de gastos que llega
        for gasto in data:
            id_gasto = int(gasto.get('id_gasto'))  # ID del gasto a actualizar
            notas = gasto.get('notas')
            descripcion = gasto.get('descripcion')

            # Verificar si se ha proporcionado el ID del gasto
            if id_gasto:
                try:
                    # Buscar el registro y actualizar los campos
                    registro = Serviceaereo.objects.get(id=id_gasto)
                    registro.notas = notas
                    registro.descripcion = descripcion
                    registro.save()

                    # Agregar el id del gasto actualizado al resultado
                    resultado['exitosos'].append(registro.id)

                except Serviceaereo.DoesNotExist:
                    # Si no se encuentra el registro, agregarlo a los errores
                    resultado['errores'].append({'id_gasto': id_gasto, 'error': 'Registro no encontrado.'})

            else:
                # Si no se proporciona el ID del gasto, agregarlo a los errores
                resultado['errores'].append({'id_gasto': id_gasto, 'error': 'ID del gasto no proporcionado.'})

    except Exception as e:
        # Si ocurre un error en el procesamiento general
        resultado['errores'].append({'error': str(e)})

    # Retornar el resultado en formato JSON
    return JsonResponse(resultado)


def check_if_reference_exists(request):
    if request.method == 'GET':
        numero = request.GET.get('numero')  # Obtén el número de la referencia desde la URL

        if numero:
            try:
                # Consulta si existe un registro en Infofactura con la referencia proporcionada
                existe = Infofactura.objects.filter(referencia=numero).exists()

                # Retorna True si existe, False si no
                return JsonResponse({'exists': existe})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
