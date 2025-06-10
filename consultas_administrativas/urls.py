from django.urls import path

from administracion_contabilidad.views.editar_consultar_pagos import editar_consultar_pagos
from administracion_contabilidad.views.cobranza import cobranza_view, source_cobranza, source_cobranza_imputacion, \
    source_facturas_pendientes, guardar_impuventa, guardar_anticipo, cargar_arbitraje
from administracion_contabilidad.views.facturacion import facturacion_view, buscar_clientes, buscar_cliente, \
    buscar_item_v, buscar_items_v, procesar_factura, source_facturacion, source_infofactura, \
    cargar_preventa_infofactura, source_infofactura_cliente, cargar_preventa_infofactura_multiple, guardar_arbitraje
from administracion_contabilidad.views.imprimir_preventa import get_datos_caratula
from administracion_contabilidad.views.proveedores_gastos import proveedores_gastos_view, buscar_proveedor, \
    buscar_proveedores, buscar_item_c, buscar_items_c, procesar_factura_proveedor, source_proveedoresygastos
from administracion_contabilidad.views.orden_pago import orden_pago_view, obtener_imputables, \
    obtener_cheques_disponibles, source_ordenes, guardar_impuorden, guardar_anticipo_orden
from administracion_contabilidad.views.preventa import guardar_infofactura, source_embarques_factura, \
    house_detail_factura, source_master_factura, get_name_by_id_productos, update_gasto_house, \
    check_if_reference_exists, eliminar_preventa, guardar_gasto_unificado, get_datos_ordenfactura, datos_xls
from consultas_administrativas.views.subdiario_ventas import subdiario_ventas

urlpatterns = [
    #ventas
    path('subdiario_ventas/', subdiario_ventas, name='subdiario_ventas'),
    # ventas

]
