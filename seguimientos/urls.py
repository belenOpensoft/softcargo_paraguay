"""cargosystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from cargosystem import settings
from mantenimientos.models import Clientes
from mantenimientos.views.guias import grilla_guias, source_guias, agregar_guias, anular_guia, asignar_guia_aerea, \
    obtener_guias_transportista
from seguimientos.views.desconsolidacion_aerea import desconsolidacion_aerea, desconsolidar_aereo
from seguimientos.views.archivos import source_archivos, guardar_archivo, eliminar_archivo, descargar_archivo
from seguimientos.views.autocompletes import autocomplete_clientes, autocomplete_ciudades, autocomplete_vendedores, \
    autocomplete_vapores, autocomplete_proyectos, autocomplete_traficos, autocomplete_actividades, \
    autocomplete_depositos, autocomplete_ciudades_codigo, agregar_buque, autocomplete_productos, agregar_producto_ajax
from seguimientos.views.email import get_data_email
from seguimientos.views.embarques import source_embarques, guardar_embarques, actualizo_datos_embarque, \
    eliminar_embarque, get_sugerencias_envases
from seguimientos.views.envases import source_envases
from seguimientos.views.gastos import source_gastos, guardar_gasto, eliminar_gasto
from seguimientos.views.getdata import get_data_cronologia, get_data_seguimiento
from seguimientos.views.logs import source_logs
from seguimientos.views.pdf import get_datos_caratula
from seguimientos.views.reportes import reportes_seguimiento, descargar_pdf, descargar_awb_seguimientos, \
    reportes_operativas, guardar_preferencia, cargar_preferencias, eliminar_preferencia
from seguimientos.views.rutas import source_rutas, guardar_ruta, eliminar_ruta, datos_seguimiento
from seguimientos.views.seguimientos import grilla_seguimientos, source_seguimientos, guardar_notas, guardar_cronologia, \
    guardar_seguimiento, guardar_envases, eliminar_envase, clonar_seguimiento, eliminar_nota, source, \
    eliminar_seguimiento, get_datos_aplicables, guardar_aplicable
from seguimientos.views.vapores import comprobar_vapores

urlpatterns = [
    ### SEGUIMIENTOS ###
    path('seguimientos', grilla_seguimientos, name="vista_seguimientos"),
    path('source_seguimientos', source_seguimientos, name="source_seguimientos"),
    path('datos_seguimiento', datos_seguimiento, name="datos_seguimiento"),
    path('source_envases', source_envases, name="source_envases"),
    path('get_sugerencias_envases/<int:numero>/', get_sugerencias_envases, name="get_sugerencias_envases"),
    path('source_rutas', source_rutas, name="source_rutas"),
    path('source_logs_seguimiento', source_logs, name="source_logs_seguimiento"),
    path('source_embarques', source_embarques, name="source_embarques"),
    path('source_gastos', source_gastos, name="source_gastos"),
    path('source_archivos', source_archivos, name="source_archivos"),
    # path('source_envases', source_envases, name="source_envases"),
    path('guardar_notas/', guardar_notas, name="guardar_notas"),
    path('eliminar_nota/', eliminar_nota, name="eliminar_nota"),
    path('source/', source, name="source"), #de notas
    path('eliminar_seguimiento/', eliminar_seguimiento, name="eliminar_seguimiento"),
    path('guardar_envases/', guardar_envases, name="guardar_envases"),
    path('guardar_ruta/', guardar_ruta, name="guardar_ruta"),
    path('guardar_gasto/', guardar_gasto, name="guardar_gasto"),
    path('guardar_archivo/', guardar_archivo, name="guardar_archivo"),
    path('guardar_embarques/', guardar_embarques, name="guardar_embarques"),
    path('actualizo_datos_embarque/', actualizo_datos_embarque, name="actualizo_datos_embarque"),
    path('eliminar_envase/', eliminar_envase, name="eliminar_envase"),
    path('clonar_seguimiento/', clonar_seguimiento, name="clonar_seguimiento"),
    path('eliminar_ruta/', eliminar_ruta, name="eliminar_ruta"),
    path('eliminar_gasto/', eliminar_gasto, name="eliminar_gasto"),
    path('eliminar_archivo/', eliminar_archivo, name="eliminar_archivo"),
    path('descargar_archivo/<int:id>', descargar_archivo, name="descargar_archivo"),
    path('eliminar_embarque/', eliminar_embarque, name="eliminar_embarque"),
    path('guardar_cronologia/', guardar_cronologia, name="guardar_cronologia"),
    path('guardar_seguimiento/', guardar_seguimiento, name="guardar_seguimiento"),
    path('autocomplete_clientes/', autocomplete_clientes, name='autocomplete_clientes'),
    path('autocomplete_ciudades/', autocomplete_ciudades, name='autocomplete_ciudades'),
    path('autocomplete_ciudades_codigo/', autocomplete_ciudades_codigo, name='autocomplete_ciudades_codigo'),
    path('autocomplete_depositos/', autocomplete_depositos, name='autocomplete_depositos'),
    path('autocomplete_vendedores/', autocomplete_vendedores, name='autocomplete_vendedores'),
    path('autocomplete_vapores/', autocomplete_vapores, name='autocomplete_vapores'),
    path('agregar_buque/', agregar_buque, name='guardar_buque'),
    path('agregar_producto/', agregar_producto_ajax, name='agregar_producto'),
    path('autocomplete_proyectos/', autocomplete_proyectos, name='autocomplete_proyectos'),
    path('autocomplete_traficos/', autocomplete_traficos, name='autocomplete_traficos'),
    path('autocomplete_actividades/', autocomplete_actividades, name='autocomplete_actividades'),
    path('autocomplete_depositos/', autocomplete_depositos, name='autocomplete_depositos'),
    path('autocomplete_productos/', autocomplete_productos, name='autocomplete_productos'),
    path('get_datos_caratula/', get_datos_caratula, name='get_datos_caratula'),
    path('get_data_cronologia/<int:id>/', get_data_cronologia, name='get_data_cronologia'),
    path('get_data_seguimiento/<int:id>/', get_data_seguimiento, name='get_data_seguimiento'),
    path('get_data_email/', get_data_email, name='get_data_email'),
    path('guias/', grilla_guias, name='vista_guias'),
    path('obtener-guias/<int:transportista_id>/', obtener_guias_transportista, name='obtener_guias_transportista'),
    path('source_guias/', source_guias, name='source_guias'),
    path('agregar_guias', agregar_guias, name='agregar_guias'),
    path('anular_guia', anular_guia, name='anular_guia'),
    path('asignar_guia_aerea/', asignar_guia_aerea, name='asignar_guia_aerea'),
    path('reportes_seguimiento/', reportes_seguimiento, name='vista_reportes'),
    path('reportes_operativas/', reportes_operativas, name='vista_reportes_op'),
    path('guardar_preferencia/', guardar_preferencia, name='guardar_preferencia'),
    path('cargar_preferencias/', cargar_preferencias, name='cargar_preferencias'),
    path('eliminar_preferencia/', eliminar_preferencia, name='eliminar_preferencia'),
    path('comprobar_vapores/', comprobar_vapores, name='comprobar_vapores'),
    path('desconsolidacion_aerea/', desconsolidacion_aerea, name='vista_desconsolidacion_aerea'),
    path('desconsolidar_aereo/', desconsolidar_aereo, name='vista_desconsolidar_aereo'),
    path('descargar_pdf/<str:pdf_file_name>/', descargar_pdf, name='descargar_pdf'),
    path('descargar_awb_seguimientos/<int:row_id>/', descargar_awb_seguimientos, name='descargar_hawb'),
    path('descargar_awb_seguimientos_draft/<int:row_id>/<str:draft>', descargar_awb_seguimientos, name='descargar_hawb'),
    path('get_datos_aplicables/', get_datos_aplicables, name='get_datos_aplicables'),
    path('guardar_aplicable/', guardar_aplicable, name='guardar_aplicable'),

]


