from django.urls import path
from impomarit.views.gastos import add_gasto_master, source_gastos, eliminar_gasto_master, source_gastos_house, \
    eliminar_gasto_house, add_gasto_house
from impomarit.views.house import add_house, add_house_impmarit, edit_house_function, house_detail, \
    get_name_by_id_vendedores, source_seguimientos_importado, add_house_importado
from impomarit.views.impo_maritima import master_importacion_maritima, source_importacion_master, source_embarque_aereo
from impomarit.views.mails import get_data_email_op
from impomarit.views.master import consultar_seguimientos, add_importacion_maritima, edit_master,master_detail, get_name_by_id
from impomarit.views.rutas import source_rutas_house, guardar_ruta, eliminar_ruta
from notificaciones.views.correos import envio_notificacion_seguimiento
from seguimientos.views.seguimientos import source_seguimientos_modo

urlpatterns = [

    path(r'masters/', master_importacion_maritima, name="master_importacion_maritima"),
    path(r'consultar_seguimientos/', consultar_seguimientos, name="consultar_seguimientos"),
    path(r'source_master/', source_importacion_master, name="source_importacion_marit_master"),
    path(r'source_gastos/', source_gastos, name="source_gastos"),
    path(r'source_gastos_house/', source_gastos_house, name="source_gastos_house"),
    path(r'source_rutas_house/', source_rutas_house, name="source_rutas_house"),
    path(r'source_seguimientos_importado/', source_seguimientos_importado, name="source_seguimientos_importado"),
    path(r'eliminar_gasto_master/', eliminar_gasto_master, name="source_gastos"),
    path(r'eliminar_gasto_house/', eliminar_gasto_house, name="eliminar_gasto_house"),
    path(r'eliminar_ruta_house/', eliminar_ruta, name="eliminar_ruta_house"),
    path(r'source_embarque_aereo/<str:master>/', source_embarque_aereo, name="source_embarque_aereo"), #hauses
    path(r'add_master/', add_importacion_maritima, name="add_master"),
    path('edit_master/<int:id_master>/', edit_master, name='edit_master'),
    path('edit_house/<int:numero>/', edit_house_function, name='edit_house'),
    path(r'add_house/', add_house_impmarit, name="add_house"),
    path(r'add_house_importado/', add_house_importado, name="add_house_importado"),
    path('master-detail/', master_detail, name='master_detail'),
    path('add_gasto_master/', add_gasto_master, name='add_gasto_master'),
    path('add_gasto_house/', add_gasto_house, name='add_gasto_house'),
    path('add_ruta_house/', guardar_ruta, name='add_ruta_house'),
    path('house-detail/', house_detail, name='house_detail'),
    path('get_data_email/', get_data_email_op, name='get_data_email'),
    path('get_name_by_id/', get_name_by_id, name='get_name_by_id'),
    path('get_name_by_id_vendedor/', get_name_by_id_vendedores, name='get_name_by_id_vendedor'),
    path('source_seguimientos_modo/<str:modo>/', source_seguimientos_modo, name="source_seguimientos_modo"),
    path('envio_notificacion_seguimiento/', envio_notificacion_seguimiento, name="envio_notificacion_seguimiento"),

]


