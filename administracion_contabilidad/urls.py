from django.urls import path

from administracion_contabilidad.views.bajar_cheques import bajar_cheques, buscar_cheques_bajar
from administracion_contabilidad.views.editar_consultar_cobranzas import editar_consultar_cobranzas, \
    obtener_detalle_cobranza, cargar_pendientes_imputacion_cobranza, procesar_imputaciones_cobranza, \
    actualizar_campos_movims_cobranza, anular_cobranza
from administracion_contabilidad.views.editar_consultar_ventas import editar_consultar_ventas, obtener_detalle_venta, \
    buscar_ordenes_por_boleta_ventas, obtener_detalle_pago_ventas, obtener_imputados_orden_venta, \
    modificar_embarque_imputado, actualizar_campos_movims_v
from administracion_contabilidad.views.editar_consultar_compras import editar_consultar_compras, obtener_detalle_compra, \
    buscar_ordenes_por_boleta, obtener_detalle_pago, obtener_imputados_orden_compra, obtener_imputados_compra, \
    procesar_imputaciones_compra, actualizar_campos_movims, anular_compra, obtener_datos_embarque_por_posicion
from administracion_contabilidad.views.editar_consultar_pagos import editar_consultar_pagos, obtener_detalle_pago_orden, \
    cargar_pendientes_imputacion_pago, procesar_imputaciones_pagos, actualizar_campos_movims_pago, anular_pago
from administracion_contabilidad.views.cobranza import cobranza_view, source_cobranza, source_cobranza_imputacion, \
    source_facturas_pendientes, guardar_impuventa, guardar_anticipo, cargar_arbitraje, obtener_proximo_mboleta, \
    get_email_recibo_cobranza
from administracion_contabilidad.views.facturacion import facturacion_view, buscar_clientes, buscar_cliente, \
    buscar_item_v, buscar_items_v, procesar_factura, source_facturacion, source_infofactura, \
    cargar_preventa_infofactura, source_infofactura_cliente, cargar_preventa_infofactura_multiple, guardar_arbitraje, \
    get_datos_embarque, hacer_nota_credito, cargar_pendientes_imputacion_venta, buscar_items_v_codigo, \
    refacturar_uruware, descargar_pdf_uruware
from administracion_contabilidad.views.filtrado_compras import buscar_embarques
from administracion_contabilidad.views.imprimir_preventa import get_datos_caratula
from administracion_contabilidad.views.ingresar_asientos import ingresar_asiento, guardar_asientos, reimprimir_asiento
from administracion_contabilidad.views.logs_administracion import audit_logs_page, audit_logs_data, \
    export_logs_administracion
from administracion_contabilidad.views.mantenimiento_chequeras import mantenimiento_chequeras, guardar_stock_cheques, \
    buscar_cheques, eliminar_cheque, habilitar_deshabilitar
from administracion_contabilidad.views.modificar_asientos import filtro_asientos, guardar_asiento_editado, \
    eliminar_asiento
from administracion_contabilidad.views.movimientos_bancarios import movimientos_bancarios, cheques_disponibles_clientes, \
    guardar_movimiento_bancario, cheques_disponibles_listado, cheques_disponibles_listado_diferidos, \
    generar_orden_pago_pdf, generar_comprobante_deposito_pdf
from administracion_contabilidad.views.movimientos_caja import movimientos_caja, guardar_movimiento_caja
from administracion_contabilidad.views.proveedores_gastos import proveedores_gastos_view, buscar_proveedor, \
    buscar_proveedores, buscar_item_c, buscar_items_c, procesar_factura_proveedor, source_proveedoresygastos, \
    cargar_pendientes_imputacion, obtener_proximo_mboleta_compra
from administracion_contabilidad.views.orden_pago import orden_pago_view, obtener_imputables, \
    obtener_cheques_disponibles, source_ordenes, guardar_impuorden, guardar_anticipo_orden, reimprimir_op, \
    obtener_proximo_mboleta_op
from administracion_contabilidad.views.preventa import guardar_infofactura, source_embarques_factura, \
    house_detail_factura, source_master_factura, get_name_by_id_productos, update_gasto_house, \
    check_if_reference_exists, eliminar_preventa, guardar_gasto_unificado, get_datos_ordenfactura, datos_xls
from login.views.login import verificar_arbitraje

urlpatterns = [
    path('facturacion/', facturacion_view, name='facturacion'),
    path('hacer_nota_credito/', hacer_nota_credito, name='hacer_nota_credito'),
    path('cargar_pendientes_imputacion_venta/', cargar_pendientes_imputacion_venta, name='cargar_pendientes_imputacion_venta'),
    path('source_facturacion/', source_facturacion, name="source_facturacion"),
    path('buscar_cliente/', buscar_cliente, name='buscar_cliente'),
    path('buscar_clientes/', buscar_clientes, name='buscar_clientes'),
    path('buscar_item_v/', buscar_item_v, name='buscar_item_v'),
    path('buscar_items_v/', buscar_items_v, name='buscar_items_v'),
    path('buscar_items_v_codigo/', buscar_items_v_codigo, name='buscar_items_v_codigo'),
    path('proveedores_gastos/', proveedores_gastos_view, name='proveedores_gastos'),
    path('buscar_proveedor/', buscar_proveedor, name='buscar_proveedor'),
    path('buscar_proveedores/', buscar_proveedores, name='buscar_proveedores'),
    path('buscar_item_c/', buscar_item_c, name='buscar_item_c'),
    path('buscar_items_c/', buscar_items_c, name='buscar_items_c'),
    path('procesar_factura/', procesar_factura, name='procesar_factura'),
    path('obtener_imputables/', obtener_imputables, name='obtener_imputables'),
    path('guardar_arbitraje/', guardar_arbitraje, name='guardar_arbitraje'),
    path('get_datos_embarque/', get_datos_embarque, name='get_datos_embarque'),

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
    path('proximo_mboleta/', obtener_proximo_mboleta, name='proximo_mboleta'),
    path('get_email_recibo_cobranza/', get_email_recibo_cobranza, name='get_email_recibo_cobranza'),
    #cobranza

    #orden de pago
    path('orden_pago/', orden_pago_view, name='orden_pago'),
    path('source_ordenes/', source_ordenes, name='source_ordenes'),
    path('obtener_imputables/', obtener_imputables, name='obtener_imputables'),
    path('obtener_cheques_disponibles/', obtener_cheques_disponibles, name='obtener_cheques_disponibles'),
    path('guardar_impuorden/', guardar_impuorden, name='guardar_impuorden'),
    path('guardar_anticipo_orden/', guardar_anticipo_orden, name='guardar_anticipo'),
    path('proximo_mboleta_op/', obtener_proximo_mboleta_op, name='proximo_mboleta_op'),

    #orden de pago

    #proveedores
    path('procesar_factura_proveedor/', procesar_factura_proveedor, name='procesar_factura_proveedor'),
    path('source_proveedoresygastos/', source_proveedoresygastos, name="source_proveedoresygastos"),
    path('buscar_embarques/', buscar_embarques, name='buscar_embarques'),
    path('cargar_pendientes_imputacion/', cargar_pendientes_imputacion, name='cargar_pendientes_imputacion'),
    path('obtener_proximo_mboleta_compra/', obtener_proximo_mboleta_compra, name='obtener_proximo_mboleta_compra'),
    #proveedores

    #editar y consultar compras#
    path('editar_consultar_compras/', editar_consultar_compras, name='editar_consultar_compras'),
    path('detalle_compra/', obtener_detalle_compra, name='detalle_compra'),
    path('buscar_ordenes_por_boleta/', buscar_ordenes_por_boleta, name='buscar_ordenes_por_boleta'),
    path('obtener_detalle_pago/', obtener_detalle_pago, name='obtener_detalle_pago'),
    path('obtener_imputados_orden_compra/', obtener_imputados_orden_compra, name='obtener_imputados_orden_compra'),
    path('obtener_imputados_compra/', obtener_imputados_compra, name='obtener_imputados_compra'),
    path('procesar_imputaciones_compra/', procesar_imputaciones_compra, name='procesar_imputaciones_compra'),
    path('modificar_compra/', actualizar_campos_movims, name='modificar_compra'),
    path('anular_compra/', anular_compra, name='anular_compra'),
    path('detalle_conocimiento/', obtener_datos_embarque_por_posicion, name='detalle_conocimiento'),

    #editar y consultar compras#

    #editar y consultar ventas#
    path('editar_consultar_ventas/', editar_consultar_ventas, name='editar_consultar_ventas'),
    path('detalle_venta/', obtener_detalle_venta, name='detalle_venta'),
    path('buscar_ordenes_por_boleta_ventas/', buscar_ordenes_por_boleta_ventas, name='buscar_ordenes_por_boleta_ventas'),
    path('obtener_detalle_pago_ventas/', obtener_detalle_pago_ventas, name='obtener_detalle_pago_ventas'),
    path('obtener_imputados_orden_venta/', obtener_imputados_orden_venta, name='obtener_imputados_orden_venta'),
    path('modificar_embarque_imputado/', modificar_embarque_imputado, name='modificar_embarque_imputado'),

    #editar y consultar ventas#

    #editar y conusltar cobranzas#
    path('editar_consultar_cobranzas/', editar_consultar_cobranzas, name='editar_consultar_cobranzas'),
    path('detalle_cobranza/', obtener_detalle_cobranza, name='detalle_cobranza'),
    path('cargar_pendientes_imputacion_cobranza/', cargar_pendientes_imputacion_cobranza, name='cargar_pendientes_imputacion_cobranza'),
    path('procesar_imputaciones_cobranza/', procesar_imputaciones_cobranza, name='procesar_imputaciones_cobranza'),
    path('actualizar_cobranza/', actualizar_campos_movims_cobranza, name='actualizar_cobranza'),
    path('anular_cobranza/', anular_cobranza, name='anular_cobranza'),
    path('modificar_venta/', actualizar_campos_movims_v, name='modificar_venta'),

    #editar y conusltar cobranzas#

    #editar y consultar pagos
    path('editar_consultar_pagos/', editar_consultar_pagos, name='editar_consultar_pagos'),
    path('detalle_pago/', obtener_detalle_pago_orden, name='detalle_pago'),
    path('cargar_pendientes_imputacion_pago/', cargar_pendientes_imputacion_pago,name='cargar_pendientes_imputacion_pago'),
    path('procesar_imputaciones_pago/', procesar_imputaciones_pagos, name='procesar_imputaciones_pago'),
    path('actualizar_pago/', actualizar_campos_movims_pago, name='actualizar_pago'),
    path('anular_pago/', anular_pago, name='anular_pago'),
    path('reimprimir_op/', reimprimir_op, name='reimprimir_op'),
    #editar y consultar pagos

    #contabilidad

    #ingresar asientos
    path('ingresar_asientos/', ingresar_asiento, name='ingresar_asientos'),
    path('guardar_asientos/', guardar_asientos, name='guardar_asientos'),
    #ingresar asientos

    #modificra asientos
    path('modificar_asientos/', filtro_asientos, name='modificar_asientos'),
    path('guardar_asiento_editado/', guardar_asiento_editado, name='guardar_asiento_editado'),
    path('eliminar_asiento/', eliminar_asiento, name='eliminar_asiento'),
    path('reimprimir_asiento/', reimprimir_asiento, name='reimprimir_asiento'),
    #modificra asientos

    #movimientos bancarios
    path('movimientos_bancarios/', movimientos_bancarios, name='movimientos_bancarios'),
    path('cheques_disponibles_clientes/', cheques_disponibles_clientes, name='cheques_disponibles'),
    path('guardar_movimiento_bancario/', guardar_movimiento_bancario, name='guardar_movimiento_bancario'),
    path('cheques_disponibles_listado/', cheques_disponibles_listado, name='cheques_disponibles_listado'),
    path('cheques_disponibles_listado_diferidos/', cheques_disponibles_listado_diferidos, name='cheques_disponibles_listado_diferidos'),
    path('generar_orden_pago_pdf/', generar_orden_pago_pdf, name='generar_orden_pago_pdf'),
    path('generar_comprobante_deposito_pdf/', generar_comprobante_deposito_pdf, name='generar_comprobante_deposito_pdf'),

    #movimientos bancarios

    #movimientod de caja
    path('movimientos_caja/', movimientos_caja, name='movimientos_caja'),
    path('verificar_arbitraje/', verificar_arbitraje, name='verificar_arbitraje'),
    path('guardar_movimiento_caja/', guardar_movimiento_caja, name='guardar_movimiento_caja'),

    #movimientod de caja

    #mantenimiento y consulta de chequeras
    path('ingresar_buscar_cheques/', mantenimiento_chequeras, name='mantenimiento_chequeras'),
    path('guardar_stock_cheques/', guardar_stock_cheques, name='guardar_stock_cheques'),
    path('buscar_cheques/', buscar_cheques, name='buscar_cheques'),
    path('eliminar_cheque/', eliminar_cheque, name='eliminar_cheque'),
    path('habilitar_deshabilitar/', habilitar_deshabilitar, name='habilitar_deshabilitar'),

    #mantenimiento y consulta de chequeras

    #bajar cheques
    path('bajar_a_banco/', bajar_cheques, name='bajar_cheques'),
    path('buscar_cheques_bajar/', buscar_cheques_bajar, name='buscar_cheques_bajar'),

    #bajar cheques


    #contabilidad

    #logs
    path("audit-logs/", audit_logs_page, name="audit_logs_page"),
    path("source_logs_administracion/", audit_logs_data, name="audit_logs_data"),
    path("export_logs_administracion/", export_logs_administracion, name="export_logs_administracion"),

    #logs

    #fcaturar uruware #

    path("refacturar_uruware/", refacturar_uruware, name="refacturar_uruware"),
    path("descargar_pdf_uruware/", descargar_pdf_uruware, name="descargar_pdf_uruware"),

    #fcaturar uruware #
]
