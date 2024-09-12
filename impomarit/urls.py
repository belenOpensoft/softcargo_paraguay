from django.urls import path

from impomarit.views.autocomplete import autocomplete_clientes, autocomplete_buques
from impomarit.views.house import add_house
from impomarit.views.impo_maritima import master_importacion_maritima, source_importacion_master, source_embarque_aereo
from impomarit.views.master import consultar_seguimientos, add_importacion_maritima

urlpatterns = [

    path(r'masters/', master_importacion_maritima, name="master_importacion_maritima"),
    path(r'consultar_seguimientos/', consultar_seguimientos, name="consultar_seguimientos"),
    path(r'source_master/', source_importacion_master, name="source_importacion_marit_master"),
    path(r'source_embarque_aereo/<str:master>/', source_embarque_aereo, name="source_embarque_aereo"), #hauses
    path(r'add_master/', add_importacion_maritima, name="add_master"),
    path(r'add_house/', add_house, name="add_house"),
    # path(r'autocomplete_clientes/', autocomplete_clientes.as_view(), name="autocomplete_clientes"),
    # path(r'vapores_autocomplete/', autocomplete_buques.as_view(), name="vapores_autocomplete"),

]


