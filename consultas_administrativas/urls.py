from django.urls import path

from consultas_administrativas.views.antiguedad_saldos import antiguedad_saldos
from consultas_administrativas.views.reporte_cobranzas import reporte_cobranzas
from consultas_administrativas.views.subdiario_ventas import subdiario_ventas
from consultas_administrativas.views.balance_cobrar import balance_cobrar

urlpatterns = [
    #ventas
    path('subdiario_ventas/', subdiario_ventas, name='subdiario_ventas'),
    path('balance_cobrar/', balance_cobrar, name='balance_cobrar'),
    path('reporte_cobranzas/', reporte_cobranzas, name='reporte_cobranzas'),
    path('antiguedad_saldos/', antiguedad_saldos, name='antiguedad_saldos'),
    # ventas

]
