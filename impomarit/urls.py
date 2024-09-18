from django.urls import path

from impomarit.views.autocomplete import autocomplete_clientes, autocomplete_buques
from impomarit.views.house import add_house, add_house_impmarit
from impomarit.views.impo_maritima import master_importacion_maritima, source_importacion_master, source_embarque_aereo
from impomarit.views.master import consultar_seguimientos, add_importacion_maritima, edit_master,master_detail, get_name_by_id

urlpatterns = [

    path(r'masters/', master_importacion_maritima, name="master_importacion_maritima"),
    path(r'consultar_seguimientos/', consultar_seguimientos, name="consultar_seguimientos"),
    path(r'source_master/', source_importacion_master, name="source_importacion_marit_master"),
    path(r'source_embarque_aereo/<str:master>/', source_embarque_aereo, name="source_embarque_aereo"), #hauses
    path(r'add_master/', add_importacion_maritima, name="add_master"),
    path('edit_master/<int:id_master>/', edit_master, name='edit_master'),
    path(r'add_house/', add_house_impmarit, name="add_house"),
    path('master-detail/', master_detail, name='master_detail'),
    path('get_name_by_id/', get_name_by_id, name='get_name_by_id'),

]


