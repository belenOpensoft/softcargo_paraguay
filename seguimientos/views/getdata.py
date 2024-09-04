from django.http import JsonResponse
from seguimientos.models import Seguimiento, VGrillaSeguimientos


def get_data_cronologia(request,id):
    try:
        data = Seguimiento.objects.filter(id=id).values(
                'fecha',
                'estimadorecepcion',
                'recepcion',
                'fecemision',
                'fecseguro',
                'fecdocage',
                'loadingdate',
                'arriboreal',
                'fecaduana',
                'pagoenfirme',
                'vencimiento',
                'etd',
                'eta',
                'fechaonhand',
                'fecrecdoc',
                'recepcionprealert',
                'lugar',
                'nroseguro',
                'bltipo',
                'manifiesto',
                'credito',
                'prima',
                'originales',)
        if data:
                # Convertir los valores en una lista de diccionarios clave-valor
                return JsonResponse(data[0], safe=False)
        else:
                return JsonResponse({'error': 'El objeto no existe'}, status=404)
        return JsonResponse(list(data), safe=False)
    except Exception as e:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)

def get_data_seguimiento(request,id):
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
                                                              )
        if data:
                # Convertir los valores en una lista de diccionarios clave-valor
                 return JsonResponse(data[0], safe=False)
        else:
                return JsonResponse({'error': 'El objeto no existe'}, status=404)
        return JsonResponse(list(data), safe=False)
    except Exception as e:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)
