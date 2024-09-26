from django.urls import path

from impomarit.views.autocomplete import autocomplete_clientes, autocomplete_buques
from impomarit.views.gastos import add_gasto_master, source_gastos, eliminar_gasto_master
from impomarit.views.house import add_house, add_house_impmarit, edit_house_function, house_detail, get_name_by_id_vendedores
from impomarit.views.impo_maritima import master_importacion_maritima, source_importacion_master, source_embarque_aereo
from impomarit.views.master import consultar_seguimientos, add_importacion_maritima, edit_master,master_detail, get_name_by_id
from seguimientos.views.seguimientos import source_seguimientos_modo

urlpatterns = [

    path(r'masters/', master_importacion_maritima, name="master_importacion_maritima"),
    path(r'consultar_seguimientos/', consultar_seguimientos, name="consultar_seguimientos"),
    path(r'source_master/', source_importacion_master, name="source_importacion_marit_master"),
    path(r'source_gastos/', source_gastos, name="source_gastos"),
    path(r'eliminar_gasto_master/', eliminar_gasto_master, name="source_gastos"),
    path(r'source_embarque_aereo/<str:master>/', source_embarque_aereo, name="source_embarque_aereo"), #hauses
    path(r'add_master/', add_importacion_maritima, name="add_master"),
    path('edit_master/<int:id_master>/', edit_master, name='edit_master'),
    path('edit_house/<int:numero>/', edit_house_function, name='edit_house'),
    path(r'add_house/', add_house_impmarit, name="add_house"),
    path('master-detail/', master_detail, name='master_detail'),
    path('add_gasto_master/', add_gasto_master, name='add_gasto_master'),
    path('house-detail/', house_detail, name='house_detail'),
    path('get_name_by_id/', get_name_by_id, name='get_name_by_id'),
    path('get_name_by_id_vendedor/', get_name_by_id_vendedores, name='get_name_by_id_vendedor'),
    path('source_seguimientos_modo/<str:modo>/', source_seguimientos_modo, name="source_seguimientos_modo"),

]


