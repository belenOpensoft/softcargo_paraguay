from datetime import datetime
from django.http import JsonResponse, HttpResponse, Http404
import json
from administracion_contabilidad.models import Infofactura
from expaerea.models import ExportServiceaereo, ExportEmbarqueaereo, ExportCargaaerea, ExportReservas
from expmarit.models import ExpmaritServiceaereo, ExpmaritEmbarqueaereo, ExpmaritCargaaerea, ExpmaritReservas
from expterrestre.models import ExpterraServiceaereo, ExpterraEmbarqueaereo, ExpterraCargaaerea, ExpterraReservas
from impaerea.models import ImportServiceaereo, ImportEmbarqueaereo, ImportCargaaerea, ImportReservas
from impomarit.models import Cargaaerea, Embarqueaereo, Reservas
from impterrestre.models import ImpterraServiceaereo, ImpterraEmbarqueaereo, ImpterraCargaaerea, ImpterraReservas
from mantenimientos.models import Productos, Monedas
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
            if fecha_str == None:
                fecha_str=str(datetime.now())
            autogenerado = generar_autogenerado(fecha_str)

            if fecha_str:
                try:
                    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S")
                    fecha_formateada = fecha_obj.strftime("%d/%m/%y")

                except ValueError:
                    fecha_formateada=datetime.now()
                    fecha_formateada = fecha_formateada.strftime("%d/%m/%y")

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
            infofactura.consigna = datos.get("consigna") if datos.get("consigna")  else datos.get("consignatario")
            infofactura.embarca = datos.get("embarca")
            infofactura.agente = datos.get("agente")
            infofactura.posicion = datos.get("posicion")
            infofactura.terminos = datos.get("terminos")
            infofactura.pagoflete = datos.get("pagoflete")
            infofactura.wr = datos.get("wr")

            infofactura.save()

            return JsonResponse({"resultado": "exito"})
        except Exception as e:
            return JsonResponse({"resultado": "error", "mensaje": str(e)}, status=500)
    else:
        return JsonResponse({"resultado": "error", "mensaje": "Método no permitido"}, status=405)


def source_embarques_factura(request):
    numero = request.GET.get('numero')
    clase = request.GET.get('clase')

    if numero and clase:

        if clase == "IM":
            registros = Cargaaerea.objects.filter(numero=numero).values('producto_id')
        elif clase == "EM":
            registros = ExpmaritCargaaerea.objects.filter(numero=numero).values('producto_id')
        elif clase == "IA":
            registros = ImportCargaaerea.objects.filter(numero=numero).values('producto_id')
        elif clase == "EA":
            registros = ExportCargaaerea.objects.filter(numero=numero).values('producto_id')
        elif clase == "IT":
            registros = ImpterraCargaaerea.objects.filter(numero=numero).values('producto_id')
        elif clase == "ET":
            registros = ExpterraCargaaerea.objects.filter(numero=numero).values('producto_id')
        else:
            return JsonResponse({'error': 'Clase no válida'}, status=400)

    data = list(registros)
    data_json = json.dumps(data)

    mimetype = "application/json"
    return HttpResponse(data_json, content_type=mimetype)


def house_detail_factura(request):
    if request.method == 'GET':
        numero = request.GET.get('numero', None)
        clase = request.GET.get('clase', None)

        if numero and clase:

            if clase == "IM":
                house = Embarqueaereo.objects.get(numero=numero)
            elif clase == "EM":
                house = ExpmaritEmbarqueaereo.objects.get(numero=numero)
            elif clase == "IA":
                house = ImportEmbarqueaereo.objects.get(numero=numero)
            elif clase == "EA":
                house = ExportEmbarqueaereo.objects.get(numero=numero)
            elif clase == "IT":
                house = ImpterraEmbarqueaereo.objects.get(numero=numero)
            elif clase == "ET":
                house = ExpterraEmbarqueaereo.objects.get(numero=numero)
            else:
                return JsonResponse({'error': 'Clase no válida'}, status=400)

        if numero:
            try:
                data = {
                    'id': house.id if clase == 'IM' else house.numero,
                    'cliente_e': house.cliente,
                    'vendedor_e': house.vendedor,
                    'transportista_e': house.transportista,
                    'agente_e': house.agente,
                    'consignatario_e': house.consignatario,
                    'origen_e': house.origen,
                    'loading_e': house.loading if clase == 'IM' or clase =='EM' else None,
                    'destino_e': house.destino ,
                    'discharge_e': house.discharge if clase == 'IM' or clase =='EM' else None,
                    'posicion_e': house.posicion,
                    'operacion_e': house.operacion,
                    'hawb_e': house.hawb,
                    'vapor_e': house.vapor if clase == 'IM' or clase =='EM' else None,
                    'viaje_e': house.viaje if clase == 'IM' or clase =='EM' else None,
                    'pago': house.pagoflete,
                    'moneda_e': house.moneda,
                    'arbitraje_e': house.arbitraje,
                    'demora_e': house.demora if clase == 'IM' or clase =='EM' else None,
                    'embarcador_e': house.embarcador,
                    'armador_e': house.armador if clase == 'IM' or clase =='EM' else None,
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
        clase = request.GET.get('clase')

        if master_id !=0 and clase:
            if clase == "IM":
                master = Reservas.objects.get(awb=master_id)
            elif clase == "EM":
                master = ExpmaritReservas.objects.get(awb=master_id)
            elif clase == "IA":
                master = ImportReservas.objects.get(awb=master_id)
            elif clase == "EA":
                master = ExportReservas.objects.get(awb=master_id)
            elif clase == "IT":
                master = ImpterraReservas.objects.get(awb=master_id)
            elif clase == "ET":
                master = ExpterraReservas.objects.get(awb=master_id)
            else:
                return JsonResponse({'error': 'Clase no válida'}, status=400)

        if master_id != 0:
            try:

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

def eliminar_preventa(request):
    if request.method == "POST":
        try:
            datos = json.loads(request.body.decode('utf-8'))
            preventa_id = datos.get("id")

            if not preventa_id:
                return JsonResponse({"resultado": "error", "mensaje": "ID no proporcionado"}, status=400)

            try:
                infofactura = Infofactura.objects.get(id=preventa_id)
                infofactura.delete()
                return JsonResponse({"resultado": "éxito", "mensaje": "Preventa eliminada correctamente"})
            except Infofactura.DoesNotExist:
                return JsonResponse({"resultado": "error", "mensaje": "La preventa no existe"}, status=404)

        except Exception as e:
            return JsonResponse({"resultado": "error", "mensaje": str(e)}, status=500)
    else:
        return JsonResponse({"resultado": "error", "mensaje": "Método no permitido"}, status=405)


def guardar_gasto_unificado(request):
    if request.method == "POST":
        try:
            datos = json.loads(request.body.decode('utf-8'))

            gastos = datos.get('gastos', [])
            clase = datos.get('clase', None)

            if not clase:
                return JsonResponse({'error': 'Clase no proporcionada'}, status=400)

            # Seleccionar el modelo adecuado según la clase
            if clase == "IM":
                registro_model = Serviceaereo
            elif clase == "EM":
                registro_model = ExpmaritServiceaereo
            elif clase == "IA":
                registro_model = ImportServiceaereo
            elif clase == "EA":
                registro_model = ExportServiceaereo
            elif clase == "IT":
                registro_model = ImpterraServiceaereo
            elif clase == "ET":
                registro_model = ExpterraServiceaereo
            else:
                return JsonResponse({'error': 'Clase no válida'}, status=400)

            ref = datos.get('referencia', None)

            # Procesar cada gasto
            for gasto in gastos:
                registro = registro_model()

                descripcion = gasto.get('descripcion')
                numero = descripcion.split('-')[0]
                registro.numero = ref
                registro.servicio= numero
                registro.descripcion = gasto.get('descripcion')

                # Obtener la moneda
                try:
                    moneda = Monedas.objects.get(nombre=gasto.get('moneda'))
                    registro.moneda = moneda.codigo  # Asignar el código de la moneda
                except Monedas.DoesNotExist:
                    return JsonResponse({'error': f"Moneda no encontrada: {gasto.get('moneda')}"}, status=400)

                registro.precio = gasto.get('total')

                # Guardar el registro en la base de datos
                registro.save()

            return JsonResponse({'exito': True}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al procesar el JSON'}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

