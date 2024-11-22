from django.urls import path
from administracion_contabilidad.views.cobranza import cobranza_view
from administracion_contabilidad.views.facturacion import facturacion_view, buscar_clientes, buscar_cliente, \
    buscar_item_v, buscar_items_v, procesar_factura, source_facturacion, source_infofactura, \
    cargar_preventa_infofactura, guardar_arbitraje
from administracion_contabilidad.views.proveedores_gastos import proveedores_gastos_view, buscar_proveedor, buscar_proveedores, buscar_item_c, buscar_items_c
from administracion_contabilidad.views.orden_pago import orden_pago_view, obtener_imputables
from administracion_contabilidad.views.editar_consultar_pagos import editar_consultar_pagos

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
    path('cargar_preventa_infofactura/', cargar_preventa_infofactura, name='cargar_preventa_infofactura'),
    path('editar_consultar_pagos/', editar_consultar_pagos, name='editar_consultar_pagos'),
    path('guardar_arbitraje/', guardar_arbitraje, name='guardar_arbitraje'),
]
