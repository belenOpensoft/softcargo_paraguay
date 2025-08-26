import io
import random
from datetime import datetime
from django.db.models import Q

import xlsxwriter
from django.core.checks import messages
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
import json
from administracion_contabilidad.models import Infofactura, Factudif, VistaGastosPreventa
from expaerea.models import ExportServiceaereo, ExportEmbarqueaereo, ExportCargaaerea, ExportReservas, ExportConexaerea
from expmarit.models import ExpmaritServiceaereo, ExpmaritEmbarqueaereo, ExpmaritCargaaerea, ExpmaritReservas, \
    ExpmaritConexaerea
from expterrestre.models import ExpterraServiceaereo, ExpterraEmbarqueaereo, ExpterraCargaaerea, ExpterraReservas, \
    ExpterraConexaerea
from impaerea.models import ImportServiceaereo, ImportEmbarqueaereo, ImportCargaaerea, ImportReservas, VEmbarqueaereo, \
    ImportConexaerea
from impomarit.models import Cargaaerea, Embarqueaereo, Reservas, Conexaerea
from impterrestre.models import ImpterraServiceaereo, ImpterraEmbarqueaereo, ImpterraCargaaerea, ImpterraReservas, \
    ImpterraConexaerea
from mantenimientos.models import Productos, Monedas, Clientes
from impomarit.models import Serviceaereo
from seguimientos.models import VGrillaSeguimientos
from seguimientos.views.seguimientos import is_ajax

from impomarit.models import VEmbarqueaereo as Vmarit
from impaerea.models import VEmbarqueaereo as Vaereo
from impterrestre.models import VEmbarqueaereo as Vterrestre
from expmarit.models import VEmbarqueaereo as Vexpmarit
from expaerea.models import VEmbarqueaereo as Vexpaerea
from expterrestre.models import VEmbarqueaereo as Vexpterrestre
from django.db.models import Q, Case, When, IntegerField

def generar_autogenerado(fecha_noseusa=None):
    fecha = datetime.now()

    # Formato con microsegundos: yyyyMMddHHmmssffffff
    fecha_str = fecha.strftime('%Y%m%d%H%M%S%f')

    qsy = str(random.randint(100, 999))  # Aleatorio de 3 dígitos

    autogenerado = f"{fecha_str}{qsy}"

    return autogenerado

def guardar_infofactura(request):
    if request.method == "POST":
        try:
            datos_json = json.loads(request.body.decode('utf-8'))
            preventa_datos = datos_json.get("preventa")
            tipo = datos_json.get("tipo")
            fecha_str = preventa_datos.get("fecha")

            if fecha_str is None:
                fecha_str = datetime.now().strftime("%d-%m-%y")

            try:
                fecha_obj = datetime.strptime(fecha_str, "%d-%m-%y")
                fecha_formateada = fecha_obj.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                fecha_formateada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if not isinstance(preventa_datos, dict):
                return JsonResponse({"resultado": "error", "mensaje": "Los datos no son un objeto válido."}, status=400)

            hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            posicion = preventa_datos.get("posicion", "")

            infofactura = Factudif()
            numero = infofactura.get_num()

            embarque = preventa_datos.get("referencia")
            # ids = preventa_datos.get("items_ids")
            # clase = posicion[:2]
            #
            # gastos = VistaGastosPreventa.objects.filter(
            #     numero=embarque,
            #     source=clase,
            #     modo=tipo.capitalize()
            # ).filter(
            #     Q(detalle__isnull=True) | Q(detalle='S/I') | Q(detalle='')
            # )
            ids_raw = preventa_datos.get("items_ids", []) or []

            # 1) Normalizar -> ints únicos
            try:
                ids_seleccionados = list({int(x) for x in ids_raw})
            except (TypeError, ValueError):
                return JsonResponse({'error': 'items_ids inválidos'}, status=400)

            clase = posicion[:2]

            # Base (tu mismo filtro de siempre)
            gastos_base = (VistaGastosPreventa.objects
                           .filter(
                numero=embarque,
                source=clase,
                modo=tipo.capitalize()
            )
                           .filter(Q(detalle__isnull=True) | Q(detalle='S/I') | Q(detalle=''))
                           )

            # 2) Si mandaron IDs, verificá pertenencia y filtrá por ellas
            if ids_seleccionados:
                # Verificación de pertenencia (opcional pero recomendable)
                valid_count = VistaGastosPreventa.objects.filter(
                    pk__in=ids_seleccionados,
                    numero=embarque,
                    source=clase,
                    modo=tipo.capitalize()
                ).count()

                if valid_count != len(ids_seleccionados):
                    return JsonResponse({'error': 'Algún ítem seleccionado no pertenece al embarque/clase/modo'},
                                        status=400)

                # 3) Aplicar filtro por pk__in
                gastos = gastos_base.filter(pk__in=ids_seleccionados)

                # 4) (Opcional) preservar el orden en que vinieron las IDs
                orden_map = {pk: idx for idx, pk in enumerate(ids_seleccionados)}
                case_expr = Case(
                    *[When(pk=pk, then=idx) for pk, idx in orden_map.items()],
                    output_field=IntegerField()
                )
                gastos = gastos.order_by(case_expr)
            else:
                # Sin selección explícita: mantenés tu comportamiento actual (todos los elegibles)
                gastos = gastos_base

            for gasto in gastos:
                nueva_infofactura = Factudif()
                nueva_infofactura.znumero = numero
                nueva_infofactura.zrefer = preventa_datos.get("referencia")
                nueva_infofactura.zseguimiento = preventa_datos.get("seguimiento")
                nueva_infofactura.zcarrier = preventa_datos.get("transportista")
                nueva_infofactura.zmaster = preventa_datos.get("master")
                nueva_infofactura.zhouse = preventa_datos.get("house")
                nueva_infofactura.zfechagen = hoy
                nueva_infofactura.zllegasale = fecha_formateada
                nueva_infofactura.zcommodity = preventa_datos.get("commodity")
                nueva_infofactura.zkilos = preventa_datos.get("kilos")
                nueva_infofactura.zvolumen = preventa_datos.get("volumen")
                nueva_infofactura.zbultos = preventa_datos.get("bultos")
                nueva_infofactura.zorigen = preventa_datos.get("origen")
                nueva_infofactura.zdestino = preventa_datos.get("destino")
                nueva_infofactura.zconsignatario = preventa_datos.get("consigna") or preventa_datos.get("consignatario")
                nueva_infofactura.zcliente = preventa_datos.get("cliente")
                nueva_infofactura.zembarcador = preventa_datos.get("embarca")
                nueva_infofactura.zagente = preventa_datos.get("agente")
                nueva_infofactura.zposicion = preventa_datos.get("posicion")
                nueva_infofactura.zterminos = preventa_datos.get("terminos")
                nueva_infofactura.zpagoflete = preventa_datos.get("pagoflete")
                nueva_infofactura.zwr = preventa_datos.get("wr")
                nueva_infofactura.ztransporte = posicion[1] if len(posicion) > 1 else None
                nueva_infofactura.zclase = posicion[:2] if len(posicion) >= 2 else None

                monto = gasto.precio if gasto.precio not in [None, 0] else gasto.costo if gasto.costo not in [None, 0] else 0
                nueva_infofactura.zitem = gasto.id_servicio
                nueva_infofactura.zmonto = monto
                nueva_infofactura.ziva = 1 if gasto.iva == 'Basico' else 0
                nueva_infofactura.zmoneda = gasto.id_moneda

                nueva_infofactura.save()

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
                    'kilos': master.kilosmadre if clase == 'IA' or clase == 'IM' or clase == 'IT' else master.kilos,
                    'bultos': master.bultosmadre if clase == 'IA' or clase == 'IM' or clase == 'IT' else None,
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


def house_detail_factura_old(request):
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
                    'notifcliente_e': house.notifcliente if clase == 'IM' or clase == 'IA' or clase == 'IT' else None,
                    'notifagente_e': house.notifagente if clase == 'IM' or clase == 'IA' or clase == 'IT' else None,
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
            except Exception as e:
                raise Http404("Ocurrió un error")
        else:
            return JsonResponse({'error': 'No ID provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def house_detail_factura(request):
    if request.method == 'GET':
        numero = request.GET.get('numero', None)
        clase = request.GET.get('clase', None)


        if numero and clase:

            if clase == "IM":
                house = Embarqueaereo.objects.get(numero=numero)
                registros = Cargaaerea.objects.filter(numero=numero).values('producto','bruto','bultos','cbm').first()
            elif clase == "EM":
                house = ExpmaritEmbarqueaereo.objects.get(numero=numero)
                registros = ExpmaritCargaaerea.objects.filter(numero=numero).values('producto','bruto','bultos','cbm').first()
            elif clase == "IA":
                house = ImportEmbarqueaereo.objects.get(numero=numero)
                registros = ImportCargaaerea.objects.filter(numero=numero).values('producto','bruto','bultos','medidas').first()
            elif clase == "EA":
                house = ExportEmbarqueaereo.objects.get(numero=numero)
                registros = ExportCargaaerea.objects.filter(numero=numero).values('producto','bruto','bultos','medidas').first()
            elif clase == "IT":
                house = ImpterraEmbarqueaereo.objects.get(numero=numero)
                registros = ImpterraCargaaerea.objects.filter(numero=numero).values('producto','bruto','bultos','cbm').first()
            elif clase == "ET":
                house = ExpterraEmbarqueaereo.objects.get(numero=numero)
                registros = ExpterraCargaaerea.objects.filter(numero=numero).values('producto','bruto','bultos','cbm').first()
            else:
                return JsonResponse({'error': 'Clase no válida'}, status=400)

            try:

                bruto = registros.get('bruto') if registros else None
                bultos = registros.get('bultos') if registros else None
                cbm = registros.get('cbm') if registros else None

                if not cbm and registros:
                    medidas = registros.get('medidas')
                    if medidas:
                        cbm = calcular_cbm_desde_medidas(medidas)


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
                    'notifcliente_e': house.notifcliente if clase == 'IM' or clase == 'IA' or clase == 'IT' else None,
                    'notifagente_e': house.notifagente if clase == 'IM' or clase == 'IA' or clase == 'IT' else None,
                    'fecharetiro_e': house.fecharetiro,
                    'fechaembarque_e': house.fechaembarque,
                    'status_e': house.status,
                    'wreceipt_e': house.wreceipt,
                    'trackid_e': house.trackid,
                    'seguimiento': house.seguimiento,
                    'terminos':house.terminos,
                    'wr':house.wreceipt,
                    'producto_id':registros['producto'] if registros else None,
                    'bultos': bultos,
                    'bruto': bruto,
                    'cbm': cbm if cbm else 0
                }

                data['awb_e'] = house.awb if house.awb is not None else 0

                return JsonResponse(data)
            except Exception as e:
                raise Http404("Ocurrió un error")
        else:
            return JsonResponse({'error': 'No ID provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def calcular_cbm_desde_medidas(medidas_str):
    try:
        partes = medidas_str.strip().lower().replace(' ', '').split('*')
        if len(partes) == 3:
            largo = float(partes[0])
            ancho = float(partes[1])
            alto = float(partes[2])
            volumen = largo * ancho * alto
            return round(volumen, 2)
    except:
        pass
    return None

def update_gasto_house(request):
    resultado = {'exitosos': [], 'errores': []}
    try:
        data = json.loads(request.body.decode('utf-8'))

        for gasto in data:
            id_gasto = int(gasto.get('id_gasto'))
            notas = gasto.get('notas')
            descripcion = gasto.get('descripcion')

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
    if request.user.has_perms(["administracion_contabilidad.view_vistagastospreventa", ]):
        if request.method == 'GET':
            numero = request.GET.get('numero')  # Obtén el número de la referencia desde la URL

            if numero:
                try:
                    # Consulta si existe un registro en Infofactura con la referencia proporcionada
                    existe = Factudif.objects.filter(zrefer=numero).exists()

                    # Retorna True si existe, False si no
                    return JsonResponse({'exists': existe})
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        messages.error(request, 'No tiene permisos para realizar esta accion.')
        return HttpResponseRedirect('/')


def eliminar_preventa(request):
    if request.method == "POST":
        try:
            datos = json.loads(request.body.decode('utf-8'))
            preventa_id = datos.get("id")

            if not preventa_id:
                return JsonResponse({"resultado": "error", "mensaje": "ID no proporcionado"}, status=400)

            try:
                Factudif.objects.filter(znumero=preventa_id).delete()
                return JsonResponse({"resultado": "éxito", "mensaje": "Preventa eliminada correctamente"})
            except Factudif.DoesNotExist:
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

def get_datos_ordenfactura(request):
    resultado = {}
    if is_ajax(request):
        try:
            idembarque = request.POST['numero']
            clase = request.POST['clase']
            if clase == 'importacion_aerea':
                embarque = ImportEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque=Vaereo.objects.get(numero=idembarque)
                con=ImportConexaerea.objects.filter(numero=idembarque).last()
                carga=ImportCargaaerea.objects.filter(numero=idembarque).last()
                if embarque.awb:
                    try:
                        master = ImportReservas.objects.get(awb=embarque.awb)
                    except ImportReservas.DoesNotExist:
                        master = ImportReservas(numero=None)
                else:
                    master = ImportReservas(numero=None)

                aux='IMPORTACION AEREA'
            elif clase == 'importacion_maritima':
                embarque = Embarqueaereo.objects.get(numero=idembarque)
                Vembarque=Vmarit.objects.get(numero=idembarque)
                con=Conexaerea.objects.filter(numero=idembarque).last()
                carga=Cargaaerea.objects.filter(numero=idembarque).last()
                if embarque.awb:
                    try:
                        master = Reservas.objects.get(awb=embarque.awb)
                    except Reservas.DoesNotExist:
                        master = Reservas(numero=None)
                else:
                    master = Reservas(numero=None)

                aux ='IMPORTACION MARITIMA'
            elif clase == 'importacion_terrestre':
                embarque = ImpterraEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque=Vterrestre.objects.get(numero=idembarque)
                con=ImpterraConexaerea.objects.filter(numero=idembarque).last()
                carga=ImpterraCargaaerea.objects.filter(numero=idembarque).last()
                if embarque.awb:
                    try:
                        master = ImpterraReservas.objects.get(awb=embarque.awb)
                    except ImpterraReservas.DoesNotExist:
                        master = ImpterraReservas(numero=None)
                else:
                    master = ImpterraReservas(numero=None)
                aux='IMPORTACION TERRESTRE'
            elif clase == 'exportacion_aerea':
                embarque = ExportEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque=Vexpaerea.objects.get(numero=idembarque)
                con=ExportConexaerea.objects.filter(numero=idembarque).last()
                carga=ExportCargaaerea.objects.filter(numero=idembarque).last()
                if embarque.awb:
                    try:
                        master = ExportReservas.objects.get(awb=embarque.awb)
                    except ExportReservas.DoesNotExist:
                        master = ExportReservas(numero=None)
                else:
                    master = ExportReservas(numero=None)
                aux='EXPORTACION AEREA'
            elif clase == 'exportacion_maritima':
                embarque = ExpmaritEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque=Vexpmarit.objects.get(numero=idembarque)
                con=ExpmaritConexaerea.objects.filter(numero=idembarque).last()
                carga=ExpmaritCargaaerea.objects.filter(numero=idembarque).last()
                if embarque.awb:
                    try:
                        master = ExpmaritReservas.objects.get(awb=embarque.awb)
                    except ExpmaritReservas.DoesNotExist:
                        master = ExpmaritReservas(numero=None)
                else:
                    master = ExpmaritReservas(numero=None)
                aux='EXPORTACION MARITIMA'
            elif clase == 'exportacion_terrestre':
                embarque = ExpterraEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque=Vexpterrestre.objects.get(numero=idembarque)
                con=ExpterraConexaerea.objects.filter(numero=idembarque).last()
                carga=ExpterraCargaaerea.objects.filter(numero=idembarque).last()
                if embarque.awb:
                    try:
                        master = ExpterraReservas.objects.get(awb=embarque.awb)
                    except ExpterraReservas.DoesNotExist:
                        master = ExpterraReservas(numero=None)
                else:
                    master = ExpterraReservas(numero=None)
                aux='EXPORTACION TERRESTRE'
            else:
                return JsonResponse({'error':'la clase es incorrecta'})


            try:
                seguimiento = VGrillaSeguimientos.objects.get(numero=embarque.seguimiento)
            except VGrillaSeguimientos.DoesNotExist:
                seguimiento = VGrillaSeguimientos(numero='', eta=None, etd=None, refcliente='',deposito='', pago='', vendedor='')


            if embarque.posicion[0] == 'I':
                if embarque.posicion[1]=='A':
                    aux = carga.medidas if carga.medidas is not None else 0
                    if aux!=0:
                        medidas = aux.split('*')
                        if len(medidas) == 3 and all(m is not None and m.isdigit() for m in medidas):
                            valor = float(medidas[0]) * float(medidas[1]) * float(medidas[2])
                        else:
                            valor=0
                    else:
                        valor=0

                else:
                    cbm=carga.cbm if carga.cbm is not None else 0
                    if cbm !=0:
                        valor=cbm
                    else:
                        aux = carga.medidas if carga.medidas is not None else 0
                        if aux!=0:
                            medidas = aux.split('*')
                            if len(medidas) == 3 and all(m is not None and m.isdigit() for m in medidas):
                                valor = float(medidas[0]) * float(medidas[1]) * float(medidas[2])
                            else:
                                valor = 0
                        else:
                            valor = 0

                peso = float(carga.bruto)
                bultos = float(carga.bultos)
                volumen = float(valor)

            elif embarque.posicion[0]=='E':
                if embarque.posicion[1] == 'A':
                    aux = carga.medidas if carga.medidas is not None else 0
                    if aux != 0:
                        medidas = aux.split('*')
                        if len(medidas) == 3 and all(m is not None and m.isdigit() for m in medidas):
                            valor = float(medidas[0]) * float(medidas[1]) * float(medidas[2])
                        else:
                            valor = 0
                    else:
                        valor = 0

                else:
                    cbm = carga.cbm if carga.cbm is not None else 0
                    if cbm != 0:
                        valor = cbm
                    else:
                        aux = carga.medidas if carga.medidas is not None else 0
                        if aux != 0:
                            medidas = aux.split('*')
                            if len(medidas) == 3 and all(m is not None and m.isdigit() for m in medidas):
                                valor = float(medidas[0]) * float(medidas[1]) * float(medidas[2])
                            else:
                                valor = 0
                        else:
                            valor = 0

                peso = float(carga.bruto)
                bultos = float(carga.bultos)
                volumen=float(valor)

            peso=round(peso,2)
            bultos=round(bultos,2)
            volumen=round(volumen,2)


            hoy = datetime.now().strftime("%d/%m/%Y")
            # Añadir un contenedor con ancho máximo
            texto = '<div style=" margin: 0 auto;">'

            # Encabezado centrado
            texto = texto + '<h2 style="text-align: left;">OCEANLINK LTDA.</h2>'
            texto = texto + '<h2 style="text-align: center;">ORDEN DE FACTURACION-' + aux + '</h2>'
            texto = texto + '<h3 style="text-align: center;">Posicion: ' + str(Vembarque.posicion if Vembarque.posicion is not None else '') + '</h3>'
            texto = texto + '<h3 style="text-align: center;">Referencia: ' + str(idembarque) + '</h3>'

            texto = texto + '<h4 style="text-align: left;">' + hoy + '</h4>'
            # Información de embarque alineada a la derecha
            texto = texto + '<b><p style="font-size:12px;text-align:left; word-wrap: break-word; white-space: normal; max-width: 100%; margin-right:60px;">'
            texto = texto + 'Embarcador: ' + str(
                Vembarque.embarcador if Vembarque.embarcador is not None else '') + '<br>'
            texto = texto + 'Consignatario:  ' + str(
                Vembarque.consignatario if Vembarque.consignatario is not None else '') + '<br>'
            texto = texto + 'Transportista: ' + str(
                Vembarque.consignatario if Vembarque.consignatario is not None else '') + '<br>'

            # Información adicional alineada a la derecha
            texto = texto + 'LLegada: ' + str(con.llegada if con.llegada is not None else '') + '<br>'
            texto = texto + 'Origen: ' + str(Vembarque.origen if Vembarque.origen is not None else '') + '<br>'
            texto = texto + 'Destino: ' + str(Vembarque.destino if Vembarque.destino is not None else '') + '<br>'
            texto = texto + 'MAWB: ' + str(Vembarque.awb if Vembarque.awb is not None else '') + '<br>'
            texto = texto + 'HAWB: ' + str(Vembarque.awb if Vembarque.awb is not None else '') + '<br>'
            texto = texto + 'Referencia: ' + str(idembarque) + '<br>'
            texto = texto + 'Seguimiento: ' + str(seguimiento.numero if seguimiento.numero is not None else '') + '<br>'
            texto = texto + 'Referencia master: ' + str(master.numero if master.numero is not None else '') + '<br>'
            texto = texto + 'Posicion: ' + str(Vembarque.posicion if Vembarque.posicion is not None else '') + '<br>'
            texto = texto + 'Peso: ' + str(peso) + '<br>'
            texto = texto + 'Bultos: ' + str(bultos) + '<br>'
            texto = texto + 'Volumen: ' + str(volumen) + '</p></b><hr>'

            # Detalle del embarque
            texto = texto + '<hr><b>A FACTURAR</b><br>'

            # Cerrar el contenedor
            texto = texto + '</div>'

            resultado['resultado'] = 'exito'
            resultado['texto'] = texto
        except Exception as e:
            resultado['resultado'] = str(e)
    else:
        resultado['resultado'] = 'Ha ocurrido un error.'
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)

def datos_xls(request):
    if request.method == 'GET':
        try:
            idembarque = request.GET['numero']
            clase = request.GET['clase']
            total = request.GET['total']

            if clase == 'importacion_aerea':
                embarque = ImportEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque = Vaereo.objects.get(numero=idembarque)
                con = ImportConexaerea.objects.filter(numero=idembarque).last()
                carga = ImportCargaaerea.objects.filter(numero=idembarque).last()

            elif clase == 'importacion_maritima':
                embarque = Embarqueaereo.objects.get(numero=idembarque)
                Vembarque = Vmarit.objects.get(numero=idembarque)
                con = Conexaerea.objects.filter(numero=idembarque).last()
                carga = Cargaaerea.objects.filter(numero=idembarque).last()

            elif clase == 'importacion_terrestre':
                embarque = ImpterraEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque = Vterrestre.objects.get(numero=idembarque)
                con = ImpterraConexaerea.objects.filter(numero=idembarque).last()
                carga = ImpterraCargaaerea.objects.filter(numero=idembarque).last()

            elif clase == 'exportacion_aerea':
                embarque = ExportEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque = Vexpaerea.objects.get(numero=idembarque)
                con = ExportConexaerea.objects.filter(numero=idembarque).last()
                carga = ExportCargaaerea.objects.filter(numero=idembarque).last()

            elif clase == 'exportacion_maritima':
                embarque = ExpmaritEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque = Vexpmarit.objects.get(numero=idembarque)
                con = ExpmaritConexaerea.objects.filter(numero=idembarque).last()
                carga = ExpmaritCargaaerea.objects.filter(numero=idembarque).last()

            elif clase == 'exportacion_terrestre':
                embarque = ExpterraEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque = Vexpterrestre.objects.get(numero=idembarque)
                con = ExpterraConexaerea.objects.filter(numero=idembarque).last()
                carga = ExpterraCargaaerea.objects.filter(numero=idembarque).last()

            else:
                return JsonResponse({'error': 'la clase es incorrecta'})

            try:
                cliente = Clientes.objects.get(codigo=embarque.cliente)
            except Clientes.DoesNotExist:
                cliente = VGrillaSeguimientos(codigo='', empresa=None, direccion=None, telefono='', contcatos='')

            hoy = datetime.now().strftime("%d/%m/%Y")


            if clase=='importacion_maritima' or clase == 'exportacion_maritima':
                viaje=con.viaje
                vapor=con.vapor
            elif clase == 'importacion_aerea' or clase == 'exportacion_aerea':
                viaje=con.vuelo
                vapor=con.ciavuelo
            else:
                viaje =con.vuelo
                vapor=con.cia

            if clase == 'importacion_aerea':
                if embarque.consolidado!=1:
                    master=ImportReservas.objects.get(awb=embarque.awb)
                    valor=master.aplicable
                else:
                    valor=0

                aplicable=valor
            else:
                aplicable=carga.bruto

            file_url = genero_xls_seguimientos(Vembarque, hoy, cliente, con, total, carga, carga.producto.nombre,viaje,vapor,aplicable)


            # Retornar la respuesta del archivo directamente, no un JsonResponse
            return file_url

        except Exception as e:
            return  JsonResponse({f'error {e}'})

def genero_xls_seguimientos(embarque, fecha, cliente, conexion, total, carga, producto,viaje,vapor,aplicable):
    try:
        name = 'Factura_Preventa' + str(embarque.posicion) + '.xlsx'
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Preventa')

        # Formatos
        header_format = workbook.add_format({'bold': True, 'bg_color': '#0D6EFD', 'font_color': 'white', 'align': 'center'})
        title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center'})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        currency_format = workbook.add_format({'num_format': '$#,##0.00'})
        border_format = workbook.add_format({'border': 1})

        # Configurar el ancho de las columnas
        worksheet.set_column('A:A', 20)  # Ajustar el ancho de la columna A
        worksheet.set_column('B:B', 20)  # Ajustar el ancho de la columna B
        worksheet.set_column('C:C', 20)  # Ajustar el ancho de la columna C
        worksheet.set_column('D:D', 30)  # Ajustar el ancho de la columna D

        row = 0
        col = 0

        # Título principal
        worksheet.merge_range(row, col, row, col + 3, "Liquidacion Nro.: "+str(embarque.posicion), title_format)
        row += 1
        worksheet.merge_range(row, col, row, col + 3, fecha, title_format)
        row += 2

        # Remit to y Bill to
        worksheet.write(row, col, "Remit to:", header_format)
        worksheet.write(row, col + 1, "OCEANLINK", border_format)
        row += 1
        worksheet.write(row, col, "Address:", header_format)
        worksheet.write(row, col + 1, "Bolonia 2280 LATU, Edificio Los Álamos, Of.103 ", border_format)
        row += 1
        worksheet.write(row, col, "Phone:", header_format)
        worksheet.write(row, col + 1, "PH: +5982 2605 2332", border_format)
        row += 1
        worksheet.write(row, col, "Balance Due:", header_format)
        worksheet.write(row, col + 1, "USD 0.00", currency_format)
        row += 2

        # Bill to (Cliente)
        worksheet.write(row, col, "Bill to:", header_format)
        worksheet.write(row, col + 1, cliente.empresa, border_format)
        row += 1
        worksheet.write(row, col, "Address:", header_format)
        worksheet.write(row, col + 1, cliente.direccion, border_format)
        row += 1
        worksheet.write(row, col, "Phone:", header_format)
        worksheet.write(row, col + 1, "TEL. "+cliente.telefono, border_format)
        row += 1
        worksheet.write(row, col, "Contact:", header_format)
        worksheet.write(row, col + 1, cliente.contactos, border_format)
        row += 2

        # Flight Details
        worksheet.write(row, col, "CHR Load Number:", header_format)
        worksheet.write(row, col + 1, "S/R", border_format)
        worksheet.write(row, col + 2, "Our Reference:", header_format)
        worksheet.write(row, col + 3, str(embarque.posicion), border_format)
        row += 1
        worksheet.write(row, col, "Shipper:", header_format)
        worksheet.write(row, col + 1, embarque.embarcador, border_format)
        row += 1
        worksheet.write(row, col, "Airline:", header_format)
        worksheet.write(row, col + 1, vapor, border_format)
        row += 1
        worksheet.write(row, col, "Flight #:", header_format)
        worksheet.write(row, col + 1, viaje, border_format)
        row += 1
        worksheet.write(row, col, "MAWB #:", header_format)
        worksheet.write(row, col + 1, embarque.awb, border_format)
        row += 1
        worksheet.write(row, col, "HAWB #:", header_format)
        worksheet.write(row, col + 1, embarque.hawb, border_format)
        row += 1
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})  # o 'dd/mm/yyyy'

        # Escribir los datos con el formato de fecha
        worksheet.write(row, col, "Origin Airport:", header_format)
        worksheet.write(row, col + 1, conexion.origen, border_format)
        worksheet.write(row, col + 2, "Departure Date:", header_format)
        worksheet.write(row, col + 3, conexion.salida, date_format)  # Aplicar el formato de fecha
        row += 1
        worksheet.write(row, col, "Dest. Airport:", header_format)
        worksheet.write(row, col + 1, conexion.destino, border_format)
        worksheet.write(row, col + 2, "Arrival Date:", header_format)
        worksheet.write(row, col + 3, conexion.llegada, date_format)  # Aplicar el formato de fecha
        row += 3

        # Column headers for items
        worksheet.write(row, col, "QTY", header_format)
        worksheet.write(row, col + 1, "UOM", header_format)
        worksheet.write(row, col + 2, "Weight", header_format)
        worksheet.write(row, col + 3, "UOM", header_format)
        worksheet.write(row, col + 4, "Chrg Wt", header_format)
        worksheet.write(row, col + 5, "UOM", header_format)
        worksheet.write(row, col + 6, "Destination", header_format)
        worksheet.write(row, col + 7, "Commodity", header_format)
        row += 1

        # Datos de los contenedores
        worksheet.write(row, col, carga.bultos, border_format)  # QTY
        worksheet.write(row, col + 1, carga.tipo, border_format)  # UOM
        worksheet.write(row, col + 2, carga.bruto, border_format)  # Weight
        worksheet.write(row, col + 3, "KGS", border_format)  # UOM
        worksheet.write(row, col + 4, aplicable, border_format)  # Chrg Wt
        worksheet.write(row, col + 5, "KGS", border_format)  # UOM
        worksheet.write(row, col + 6, conexion.destino, border_format)  # Destination
        worksheet.write(row, col + 7, producto, border_format)  # Commodity
        row+=1
        # Total (Balance Due)
        worksheet.merge_range(row, col, row, col + 6, "Balance Due: "+total, currency_format)

        # Cerrar y generar archivo en memoria
        workbook.close()
        output.seek(0)

        # Crear la respuesta de descarga de archivo
        response = HttpResponse(output.read(),content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f"attachment; filename={name}"  # Nombre del archivo a descargar
        return response

    except Exception as e:
        raise TypeError(e)




