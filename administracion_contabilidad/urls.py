from django.urls import path
from administracion_contabilidad.views.facturacion import facturacion_view, buscar_clientes, buscar_cliente, buscar_item, buscar_items

urlpatterns = [
    path('facturacion/', facturacion_view, name='facturacion'),
    path('buscar_cliente/', buscar_cliente, name='buscar_cliente'),
    path('buscar_clientes/', buscar_clientes, name='buscar_clientes'),
    path('buscar_item/', buscar_item, name='buscar_item'),
    path('buscar_items/', buscar_items, name='buscar_items'),
]
