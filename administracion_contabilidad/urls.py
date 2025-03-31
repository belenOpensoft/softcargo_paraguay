from django.urls import path

from administracion_contabilidad.views.editar_consultar_compras import editar_consultar_compras, obtener_detalle_compra, \
    buscar_ordenes_por_boleta
from administracion_contabilidad.views.editar_consultar_pagos import editar_consultar_pagos
from administracion_contabilidad.views.cobranza import cobranza_view, source_cobranza, source_cobranza_imputacion, \
    source_facturas_pendientes, guardar_impuventa, guardar_anticipo, cargar_arbitraje
from administracion_contabilidad.views.facturacion import facturacion_view, buscar_clientes, buscar_cliente, \
    buscar_item_v, buscar_items_v, procesar_factura, source_facturacion, source_infofactura, \
    cargar_preventa_infofactura, source_infofactura_cliente, cargar_preventa_infofactura_multiple, guardar_arbitraje
from administracion_contabilidad.views.filtrado_compras import buscar_embarques
from administracion_contabilidad.views.imprimir_preventa import get_datos_caratula
from administracion_contabilidad.views.proveedores_gastos import proveedores_gastos_view, buscar_proveedor, \
    buscar_proveedores, buscar_item_c, buscar_items_c, procesar_factura_proveedor, source_proveedoresygastos, \
    cargar_pendientes_imputacion
from administracion_contabilidad.views.orden_pago import orden_pago_view, obtener_imputables, \
    obtener_cheques_disponibles, source_ordenes, guardar_impuorden, guardar_anticipo_orden
from administracion_contabilidad.views.preventa import guardar_infofactura, source_embarques_factura, \
    house_detail_factura, source_master_factura, get_name_by_id_productos, update_gasto_house, \
    check_if_reference_exists, eliminar_preventa, guardar_gasto_unificado, get_datos_ordenfactura, datos_xls

urlpatterns = [
    path('facturacion/', facturacion_view, name='facturacion'),
    path('source_facturacion/', source_facturacion, name="source_facturacion"),
    path('buscar_cliente/', buscar_cliente, name='buscar_cliente'),
    path('buscar_clientes/', buscar_clientes, name='buscar_clientes'),
    path('buscar_item_v/', buscar_item_v, name='buscar_item_v'),
    path('buscar_items_v/', buscar_items_v, name='buscar_items_v'),
    path('proveedores_gastos/', proveedores_gastos_view, name='proveedores_gastos'),
    path('buscar_proveedor/', buscar_proveedor, name='buscar_proveedor'),
    path('buscar_proveedores/', buscar_proveedores, name='buscar_proveedores'),
    path('buscar_item_c/', buscar_item_c, name='buscar_item_c'),
    path('buscar_items_c/', buscar_items_c, name='buscar_items_c'),
    path('procesar_factura/', procesar_factura, name='procesar_factura'),
    path('obtener_imputables/', obtener_imputables, name='obtener_imputables'),
    path('guardar_arbitraje/', guardar_arbitraje, name='guardar_arbitraje'),
    path('editar_consultar_pagos/', editar_consultar_pagos, name='editar_consultar_pagos'),

    # preventa
    path('get_datos_pdf_preventa/', get_datos_caratula, name='get_datos_pdf_preventa'),
    path('cargar_preventa_infofactura/', cargar_preventa_infofactura, name='cargar_preventa_infofactura'),
    path('source_infofactura_cliente/', source_infofactura_cliente, name='source_infofactura_cliente'),
    path('source_infofactura/', source_infofactura, name='source_infofactura'),
    path('source_embarque_factura/', source_embarques_factura, name='source_embarque_factura'),
    path('house_detail_factura/', house_detail_factura, name='house_detail_factura'),
    path('source_master_factura/', source_master_factura, name='source_master_factura'),
    path('get_datos_ordenfactura/', get_datos_ordenfactura, name='get_datos_caratula'),
    path('get_name_by_id_productos/', get_name_by_id_productos, name='get_name_by_id_productos'),
    path('preventa/', guardar_infofactura, name='preventa'),
    path('cargar_preventa_infofactura_multiple/', cargar_preventa_infofactura_multiple, name='cargar_preventa_infofactura_multiple'),
    path('guardar_gasto_unificado/', guardar_gasto_unificado, name='guardar_gasto_unificado'),
    path('update_gasto_house/', update_gasto_house, name='update_gasto_house'),
    path('check_if_reference_exists/', check_if_reference_exists, name='check_if_reference_exists'),
    path('eliminar_preventa/', eliminar_preventa, name='eliminar_preventa'),
    path('datos_xls/', datos_xls, name='datos_xls'),
    # preventa

    #cobranza
    path('cobranza/', cobranza_view, name='cobranza'),
    path('source_cobranza/', source_cobranza, name='source_cobranza'),
    path('source_cobranza_imputacion/', source_cobranza_imputacion, name='source_cobranza_imputacion'),
    path('source_facturas_pendientes/', source_facturas_pendientes, name='source_facturas_pendientes'),
    path('guardar_impuventa/', guardar_impuventa, name='guardar_impuventa'),
    path('guardar_anticipo/', guardar_anticipo, name='guardar_anticipo'),
    path('cargar_arbitraje/', cargar_arbitraje, name='cargar_arbitraje'),

    #cobranza

    #orden de pago
    path('orden_pago/', orden_pago_view, name='orden_pago'),
    path('source_ordenes/', source_ordenes, name='source_ordenes'),
    path('obtener_imputables/', obtener_imputables, name='obtener_imputables'),
    path('obtener_cheques_disponibles/', obtener_cheques_disponibles, name='obtener_cheques_disponibles'),
    path('guardar_impuorden/', guardar_impuorden, name='guardar_impuorden'),
    path('guardar_anticipo_orden/', guardar_anticipo_orden, name='guardar_anticipo'),

    #orden de pago

    #proveedores
    path('procesar_factura_proveedor/', procesar_factura_proveedor, name='procesar_factura_proveedor'),
    path('source_proveedoresygastos/', source_proveedoresygastos, name="source_proveedoresygastos"),
    path('buscar_embarques/', buscar_embarques, name='buscar_embarques'),
    path('cargar_pendientes_imputacion/', cargar_pendientes_imputacion, name='cargar_pendientes_imputacion'),
    #proveedores

    #editar y consultar compras#
    path('editar_consultar_compras/', editar_consultar_compras, name='editar_consultar_compras'),
    path('detalle_compra/', obtener_detalle_compra, name='detalle_compra'),
    path('buscar_ordenes_por_boleta/', buscar_ordenes_por_boleta, name='buscar_ordenes_por_boleta'),

    #editar y consultar compras#

]
