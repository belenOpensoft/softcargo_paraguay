import io
from datetime import datetime

import xlsxwriter
from django.http import JsonResponse, HttpResponse, Http404
import json
from administracion_contabilidad.models import Infofactura
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
                if embarque.consolidado!=1:
                    master=ImportReservas.objects.get(awb=embarque.awb)
                else:
                    master=ImportReservas(numero=None)
                aux='IMPORTACION AEREA'
            elif clase == 'importacion_maritima':
                embarque = Embarqueaereo.objects.get(numero=idembarque)
                Vembarque=Vmarit.objects.get(numero=idembarque)
                con=Conexaerea.objects.filter(numero=idembarque).last()
                carga=Cargaaerea.objects.filter(numero=idembarque).last()
                if embarque.consolidado != 1:
                    master=Reservas.objects.get(awb=embarque.awb)
                else:
                    master=Reservas(numero=None)
                aux ='IMPORTACION MARITIMA'
            elif clase == 'importacion_terrestre':
                embarque = ImpterraEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque=Vterrestre.objects.get(numero=idembarque)
                con=ImpterraConexaerea.objects.filter(numero=idembarque).last()
                carga=ImpterraCargaaerea.objects.filter(numero=idembarque).last()
                if embarque.consolidado != 1:
                    try:
                        master = ImpterraReservas.objects.get(awb=embarque.awb)
                    except ImpterraReservas.DoesNotExist:
                        master=ImpterraReservas(numero=None)
                else:
                    master=ImpterraReservas(numero=None)
                aux='IMPORTACION TERRESTRE'
            elif clase == 'exportacion_aerea':
                embarque = ExportEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque=Vexpaerea.objects.get(numero=idembarque)
                con=ExportConexaerea.objects.filter(numero=idembarque).last()
                carga=ExportCargaaerea.objects.filter(numero=idembarque).last()
                if embarque.consolidado != 1:
                    master=ExportReservas.objects.get(awb=embarque.awb)
                else:
                    master=ExportReservas(numero=None)
                aux='EXPORTACION AEREA'
            elif clase == 'exportacion_maritima':
                embarque = ExpmaritEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque=Vexpmarit.objects.get(numero=idembarque)
                con=ExpmaritConexaerea.objects.filter(numero=idembarque).last()
                carga=ExpmaritCargaaerea.objects.filter(numero=idembarque).last()
                if embarque.consolidado != 1:
                    master=ExpmaritReservas.objects.get(awb=embarque.awb)
                else:
                    master=ExpmaritReservas(numero=None)
                aux='EXPORTACION MARITIMA'
            elif clase == 'exportacion_terrestre':
                embarque = ExpterraEmbarqueaereo.objects.get(numero=idembarque)
                Vembarque=Vexpterrestre.objects.get(numero=idembarque)
                con=ExpterraConexaerea.objects.filter(numero=idembarque).last()
                carga=ExpterraCargaaerea.objects.filter(numero=idembarque).last()
                if embarque.consolidado != 1:
                    try:
                        master = ImpterraReservas.objects.get(awb=embarque.awb)
                    except ImpterraReservas.DoesNotExist:
                        master = ImpterraReservas(numero=None)
                else:
                    master=ExpterraReservas(numero=None)
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
        worksheet.write(row, col + 1, "MISIONES 1574 OF 201\nMONTEVIDEO MONTEVIDEO", border_format)
        row += 1
        worksheet.write(row, col, "Phone:", header_format)
        worksheet.write(row, col + 1, "PH: 598 2917 0501", border_format)
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




