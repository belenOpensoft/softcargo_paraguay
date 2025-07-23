from datetime import datetime

from django.http import JsonResponse

from mantenimientos.models import Vapores
from seguimientos.models import Seguimiento, VGrillaSeguimientos


def get_data_cronologia_old(request,id):
    try:
        data = Seguimiento.objects.filter(id=id)

        # Lista de campos que son fechas
        campos_fecha = [
            'fecha', 'estimadorecepcion', 'recepcion', 'fecemision', 'fecseguro',
            'fecdocage', 'loadingdate', 'arriboreal', 'fecaduana', 'pagoenfirme',
            'vencimiento', 'etd', 'eta', 'fechaonhand', 'fecrecdoc', 'recepcionprealert'
        ]

        # Construcción del array con solo los campos de fecha formateados
        resultado = []
        for obj in data:
            item = {}
            for field_name in campos_fecha:
                value = getattr(obj, field_name, None)

                # Si el valor no es None, formatearlo
                if value is not None:
                    item[field_name] = value.strftime('%Y-%m-%d')
                else:
                    item[field_name] = None  # Mantener None si el campo es vacío

            resultado.append(item)
        return JsonResponse(list(resultado), safe=False)
    except Exception as e:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)

def get_data_cronologia(request, id):
    try:
        data = Seguimiento.objects.filter(id=id)

        # Lista de todos los campos requeridos
        fields = [
            'fecha', 'estimadorecepcion', 'recepcion', 'fecemision', 'fecseguro',
            'fecdocage', 'loadingdate', 'arriboreal', 'fecaduana', 'pagoenfirme',
            'vencimiento', 'etd', 'eta', 'fechaonhand', 'fecrecdoc', 'recepcionprealert',
            'lugar', 'nroseguro', 'bltipo', 'manifiesto', 'credito', 'prima',
            'originales', 'observaciones'
        ]

        # Lista de campos que son fechas para formatearlos
        campos_fecha = [
            'fecha', 'estimadorecepcion', 'recepcion', 'fecemision', 'fecseguro',
            'fecdocage', 'loadingdate', 'arriboreal', 'fecaduana', 'pagoenfirme',
            'vencimiento', 'etd', 'eta', 'fechaonhand', 'fecrecdoc', 'recepcionprealert'
        ]

        # Construcción del array con todos los campos formateados correctamente
        resultado = []
        for obj in data:
            item = {}
            for field_name in fields:
                value = getattr(obj, field_name, None)

                # Si el campo es de fecha y tiene valor, formatearlo
                if field_name in campos_fecha and value is not None:
                    item[field_name] = value.strftime('%Y-%m-%d')
                else:
                    item[field_name] = value  # Mantener el valor original para los otros campos

            resultado.append(item)

        return JsonResponse({
            'bloqueado': False,
            'datos': resultado
        })

    except Exception as e:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)

def get_data_seguimiento_old(request,id):
    try:
        data = VGrillaSeguimientos.objects.filter(id=id).values('numero',
                                                                'cliente',
                                                                'cliente_codigo',
                                                                'embarcador',
                                                                'embarcador_codigo',
                                                                'consignatario',
                                                                'consignatario_codigo',
                                                                'agente',
                                                                'agente_codigo',
                                                                'armador',
                                                                'armador_codigo',
                                                                'transportista',
                                                                'transportista_codigo',
                                                                'agecompras',
                                                                'agecompras_codigo',
                                                                'ageventas',
                                                                'ageventas_codigo',
                                                                'origen',
                                                                'destino',
                                                                'status',
                                                                'moneda',
                                                                'loading',
                                                                'discharge',
                                                                'posicion',
                                                                'pago',
                                                                'vendedor',
                                                                'vendedor_codigo',
                                                                'deposito',
                                                                'deposito_codigo',
                                                                'vapor',
                                                                'vapor_codigo',
                                                                'viaje',
                                                                'arbitraje',
                                                                'awb',
                                                                'hawb',
                                                                'operacion',
                                                                'wreceipt',
                                                                'pago',
                                                                'notificar',
                                                                'notificar_codigo',
                                                                'valor',
                                                                'notas',
                                                                'viaje',
                                                                'ubicacion',
                                                                'booking',
                                                                'trackid',
                                                                'proyecto',
                                                                'proyecto_codigo',
                                                                'trafico',
                                                                'trafico_codigo',
                                                                'actividad',
                                                                'actividad_codigo',
                                                                'diasalmacenaje',
                                                                'demora',
                                                                'modo',
                                                                'id',
                                                                'origen_text',
                                                                'destino_text',
                                                                'refproveedor',
                                                                'refcliente',
                                                                'loadingdate',
                                                                'fecha',
                                                                'vencimiento',
                                                              )
        if data:
                # Convertir los valores en una lista de diccionarios clave-valor
                 return JsonResponse(data[0], safe=False)
        else:
                return JsonResponse({'error': 'El objeto no existe'}, status=404)
        return JsonResponse(list(data), safe=False)
    except Exception as e:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)



def get_data_seguimiento(request, id):
    try:
        data = VGrillaSeguimientos.objects.filter(id=id).values(
            'numero', 'cliente', 'cliente_codigo', 'embarcador', 'embarcador_codigo',
            'consignatario', 'consignatario_codigo', 'agente', 'agente_codigo',
            'armador', 'armador_codigo', 'transportista', 'transportista_codigo',
            'agecompras', 'agecompras_codigo', 'ageventas', 'ageventas_codigo',
            'origen', 'destino', 'status', 'moneda', 'loading', 'discharge',
            'posicion', 'pago', 'vendedor', 'vendedor_codigo', 'deposito',
            'deposito_codigo', 'vapor', 'vapor_codigo', 'viaje', 'arbitraje',
            'awb', 'hawb', 'operacion', 'wreceipt', 'pago', 'notificar',
            'notificar_codigo', 'valor', 'notas', 'viaje', 'ubicacion',
            'booking', 'trackid', 'proyecto', 'proyecto_codigo', 'trafico',
            'trafico_codigo', 'actividad', 'actividad_codigo', 'diasalmacenaje',
            'demora', 'modo', 'id', 'origen_text', 'destino_text',
            'refproveedor', 'refcliente', 'loadingdate', 'fecha', 'vencimiento','terminos','volumen','trafico','contratotra'
        )

        if data:
            item = dict(data[0])

            # Campos de fecha que queremos formatear
            campos_fecha = ['loadingdate', 'fecha', 'vencimiento']

            for field_name in campos_fecha:
                value = item.get(field_name)
                if isinstance(value, datetime):
                    item[field_name] = value.strftime('%Y-%m-%d')

                vapor_codigo = item.get('vapor')  # Obtener el valor del campo vapor

                if isinstance(vapor_codigo, int) or (isinstance(vapor_codigo, str) and vapor_codigo.isdigit()):
                    vapor_obj = Vapores.objects.filter(codigo=int(vapor_codigo)).first()
                    if vapor_obj:
                        item['vapor'] = vapor_obj.nombre

            return JsonResponse(item, safe=False)
        else:
            return JsonResponse({'error': 'El objeto no existe'}, status=404)

    except Exception as e:
        return JsonResponse({'error': 'Error interno: ' + str(e)}, status=500)
