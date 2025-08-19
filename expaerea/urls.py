from django.urls import path

from expaerea.views.embarques import source_embarques, eliminar_embarque, guardar_embarques, add_embarque_importado
from expaerea.views.gastos import add_gasto_master, source_gastos, eliminar_gasto_master, source_gastos_house, \
    eliminar_gasto_house, add_gasto_house, add_gasto_importado, source_gastos_house_preventa

from expaerea.views.house import add_house_impmarit, edit_house_function, house_detail, \
    get_name_by_id_vendedores, source_seguimientos_importado, add_house_importado, source_gastos_importado, \
    eliminar_house, source_envases_importado, source_rutas_importado, source_embarque_id, source_seguimiento_id, \
    generar_posicion, source_embarque_importado, source_archivos_importado
from expaerea.views.exp_aerea import master_expo_aerea, source_importacion_master, source_embarque_aereo, \
    source_embarque_consolidado, house_importacion_maritima, source_archivos, guardar_archivo_im, eliminar_archivo, \
    descargar_archivo, modificar_fecha_retiro, add_archivo_importado, source_embarque_aereo_full, buscar_registros, \
    source_logs, buscar_registros_directos, source_embarques_general, buscar_registros_general, \
    embarques_exportacion_aerea
from expaerea.views.master import master_detail, add_importacion_maritima, edit_master, get_name_by_id, \
    consultar_seguimientos

from expaerea.views.mails import get_data_email_op
from expaerea.views.notas import source, guardar_notas, eliminar_nota
from expaerea.views.pdf import get_datos_caratula
from expaerea.views.rutas import source_rutas_house, guardar_ruta, eliminar_ruta, add_ruta_importado, \
    datos_embarque_ruta, source_rutas_master, eliminar_ruta_master, guardar_ruta_master, datos_embarque_ruta_master
from impaerea.views.imp_aerea import embarques_importacion_aerea

from notificaciones.views.correos import envio_notificacion_seguimiento
from seguimientos.views.reportes import descargar_awb_operativas, descargar_hawb_operativas, editar_hawb, guardar_hawb, \
    editar_awb, guardar_awb
from seguimientos.views.seguimientos import source_seguimientos_modo

urlpatterns = [
    path('source/', source, name='source'),
    path('datos_embarque_ruta/', datos_embarque_ruta, name='datos_embarque_ruta'),
    path('datos_embarque_ruta_master/', datos_embarque_ruta_master, name='datos_embarque_ruta_master'),
    path('guardar_notas/', guardar_notas, name='guardar_notas'),
    path('eliminar_nota/', eliminar_nota, name='eliminar_nota'),
    path('get_datos_caratula/', get_datos_caratula, name='get_datos_caratula'),
    path(r'masters/', master_expo_aerea, name="master_importacion_maritima"),
    path('descargar_archivo/<int:id>', descargar_archivo, name="descargar_archivo"),
    path('eliminar_archivo/', eliminar_archivo, name="eliminar_archivo"),
    path('modificar_fecha_retiro/', modificar_fecha_retiro, name="modificar_fecha_retiro"),
    path('source_archivos/', source_archivos, name="source_archivos"),
    path('guardar_archivo/', guardar_archivo_im, name="guardar_archivo"),
    path(r'house_directo/', house_importacion_maritima, name="house_directo"),
    path(r'consultar_seguimientos/', consultar_seguimientos, name="consultar_seguimientos"),
    path(r'source_master/', source_importacion_master, name="source_importacion_marit_master"),
    path(r'source_gastos/', source_gastos, name="source_gastos"),
    path(r'source_embarque_id/', source_embarque_id, name="source_embarque_id"),
    path(r'generar_posicion/', generar_posicion, name="generar_posicion"),
    path(r'source_seguimiento_id/', source_seguimiento_id, name="source_seguimiento_id"),
    path(r'source_embarque_consolidado/', source_embarque_consolidado, name="source_embarque_consolidado"),
    path(r'source_gastos_house/', source_gastos_house, name="source_gastos_house"),
    path(r'source_gastos_house_preventa/', source_gastos_house_preventa, name="source_gastos_house_preventa"),

    path(r'source_rutas_house/', source_rutas_house, name="source_rutas_house"),
    path(r'source_rutas_master/', source_rutas_master, name="source_rutas_master"),
    path(r'source_embarques_house/', source_embarques, name="source_embarques_house"),
    path(r'source_seguimientos_importado/', source_seguimientos_importado, name="source_seguimientos_importado"),
    path(r'source_gastos_importado/', source_gastos_importado, name="source_gastos_importado"),
    path(r'source_archivos_importado/', source_archivos_importado, name="source_archivos_importado"),
    path(r'source_embarque_importado/', source_embarque_importado, name="source_embarque_importado"),
    path(r'source_envases_importado/', source_envases_importado, name="source_envases_importado"),
    path(r'source_rutas_importado/', source_rutas_importado, name="source_rutas_importado"),
    path('add_ruta_importado/', add_ruta_importado, name='add_ruta_importado'),
    path('add_archivo_importado/', add_archivo_importado, name='add_archivo_importado'),
    path(r'eliminar_gasto_master/', eliminar_gasto_master, name="source_gastos"),
    path(r'eliminar_gasto_house/', eliminar_gasto_house, name="eliminar_gasto_house"),
    path(r'eliminar_embarques_house/', eliminar_embarque, name="eliminar_embarques_house"),
    path('add_embarque_house/', guardar_embarques, name='add_embarque_house'),
    path(r'eliminar_ruta_house/', eliminar_ruta, name="eliminar_ruta_house"),
    path(r'eliminar_ruta_master/', eliminar_ruta_master, name="eliminar_ruta_master"),
    path(r'eliminar_house/', eliminar_house, name="eliminar_house"),
    path(r'source_embarque_aereo/', source_embarque_aereo, name="source_embarque_aereo"), #hauses
    path(r'source_embarque_aereo_full/<str:master>/', source_embarque_aereo_full, name="source_embarque_aereo_full"),  # hauses
    path(r'add_master/', add_importacion_maritima, name="add_master"),
    path('buscar_registros/', buscar_registros, name='buscar_registros'),
    path('buscar_registros_directos/', buscar_registros_directos, name='buscar_registros_directos'),
    path('edit_master/<int:id_master>/', edit_master, name='edit_master'),
    path('edit_house/<int:numero>/', edit_house_function, name='edit_house'),
    path(r'add_house/', add_house_impmarit, name="add_house"),
    path(r'add_house_importado/', add_house_importado, name="add_house_importado"),
    path('master-detail/', master_detail, name='master_detail'),
    path('add_gasto_master/', add_gasto_master, name='add_gasto_master'),
    path('add_gasto_house/', add_gasto_house, name='add_gasto_house'),
    path('add_gasto_importado/', add_gasto_importado, name='add_gasto_house'),
    path('add_embarque_importado/', add_embarque_importado, name='add_embarque_importado'),
    path('add_ruta_house/', guardar_ruta, name='add_ruta_house'),
    path('add_ruta_master/', guardar_ruta_master, name='add_ruta_master'),
    path('house-detail/', house_detail, name='house_detail'),
    path('get_data_email/', get_data_email_op, name='get_data_email'),
    path('get_name_by_id/', get_name_by_id, name='get_name_by_id'),
    path('get_name_by_id_vendedor/', get_name_by_id_vendedores, name='get_name_by_id_vendedor'),
    path('source_seguimientos_modo/<str:modo>/', source_seguimientos_modo, name="source_seguimientos_modo"),
    path('source_logs/', source_logs, name="source_logs"),

    path('descargar_awb/<int:row_id>/', descargar_awb_operativas, name='descargar_awb'),
    path('descargar_awb_draft/<int:row_id>/<str:draft>', descargar_awb_operativas, name='descargar_awb'),
    path('descargar_hawb/<int:row_id>/', descargar_hawb_operativas, name='descargar_hawb'),
    path('descargar_hawb_draft/<int:row_id>/<str:draft>', descargar_hawb_operativas, name='descargar_hawb'),


    #editar guia
    path('editar_hawb/<int:row_id>/', editar_hawb, name='editar_hawb'),
    path('editar_awb/<int:row_id>/', editar_awb, name='editar_awb'),
    path('guardar_hawb/<int:row_id>/', guardar_hawb, name='guardar_hawb'),
    path('guardar_awb/<int:row_id>/', guardar_awb, name='guardar_awb'),

    path('source_embarques_general/', source_embarques_general, name='source_embarques_general'),
    path('buscar_registros_general/', buscar_registros_general, name='buscar_registros_general'),
    path('embarques/', embarques_exportacion_aerea, name='embarques'),
]


