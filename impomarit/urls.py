from django.urls import path

from impomarit.views.autocomplete import autocomplete_clientes, autocomplete_buques
from impomarit.views.impo_maritima import master_importacion_maritima, source_importacion_master, consultar_seguimientos

urlpatterns = [
    ### SEGUIMIENTOS ###
    path(r'masters/', master_importacion_maritima, name="master_importacion_maritima"),
    path(r'consultar_seguimientos/', consultar_seguimientos, name="consultar_seguimientos"),
    path(r'source_master/', source_importacion_master, name="source_importacion_marit_master"),
    # path(r'autocomplete_clientes/', autocomplete_clientes.as_view(), name="autocomplete_clientes"),
    # path(r'vapores_autocomplete/', autocomplete_buques.as_view(), name="vapores_autocomplete"),

]


