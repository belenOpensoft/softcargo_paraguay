from administracion_contabilidad.models import PendienteFacturar
from administracion_contabilidad.views.facturacion import facturar_pendiente


def comprobar_facturas_pendientes():
    try:
        """
            1 Recorrer la tabla de Facturas pendiente filtrando estado en "PENDIENTE"
            for x in registros:
                facturar_pendiente(x.autogenerado)
        """
        mis_pendientes = PendienteFacturar.objects.filter(estado='PENDIENTE')
        for x in mis_pendientes:
            facturar_pendiente(x.autogenerado)
    except Exception as e:
        print(e)
