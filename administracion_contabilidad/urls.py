from django.urls import path
from administracion_contabilidad.views.cobranza import cobranza_view
from administracion_contabilidad.views.facturacion import facturacion_view, buscar_clientes, buscar_cliente, \
    buscar_item_v, buscar_items_v, procesar_factura, source_facturacion, source_infofactura, \
    cargar_preventa_infofactura, source_infofactura_cliente
from administracion_contabilidad.views.imprimir_preventa import get_datos_caratula
from administracion_contabilidad.views.proveedores_gastos import proveedores_gastos_view, buscar_proveedor, buscar_proveedores, buscar_item_c, buscar_items_c
from administracion_contabilidad.views.orden_pago import orden_pago_view, obtener_imputables
from administracion_contabilidad.views.preventa import guardar_infofactura, source_embarques_factura, \
    house_detail_factura, source_master_factura, get_name_by_id_productos, update_gasto_house, check_if_reference_exists, eliminar_preventa

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
    path('cobranza/', cobranza_view, name='cobranza'),
    path('orden_pago/', orden_pago_view, name='orden_pago'),
    path('obtener_imputables/', obtener_imputables, name='obtener_imputables'),
    path('source_infofactura/', source_infofactura, name='source_infofactura'),
    path('source_infofactura_cliente/', source_infofactura_cliente, name='source_infofactura_cliente'),
    path('cargar_preventa_infofactura/', cargar_preventa_infofactura, name='cargar_preventa_infofactura'),
    path('get_datos_pdf_preventa/', get_datos_caratula, name='get_datos_pdf_preventa'),

    # preventa
    path('source_embarque_factura/', source_embarques_factura, name='source_embarque_factura'),
    path('house_detail_factura/', house_detail_factura, name='house_detail_factura'),
    path('source_master_factura/', source_master_factura, name='source_master_factura'),
    path('get_name_by_id_productos/', get_name_by_id_productos, name='get_name_by_id_productos'),
    path('preventa/', guardar_infofactura, name='preventa'),
    path('update_gasto_house/', update_gasto_house, name='update_gasto_house'),
    path('check_if_reference_exists/', check_if_reference_exists, name='check_if_reference_exists'),
    path('eliminar_preventa/', eliminar_preventa, name='eliminar_preventa'),
    # preventa

]
