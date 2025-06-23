from django.urls import path

from consultas_administrativas.views.antiguedad_saldos import antiguedad_saldos
from consultas_administrativas.views.antiguedad_saldos_compras import antiguedad_saldos_compras
from consultas_administrativas.views.balance_pagar import balance_pagos
from consultas_administrativas.views.estados_cuenta import estados_cuenta
from consultas_administrativas.views.estados_cuenta_compras import estados_cuenta_compras
from consultas_administrativas.views.reporte_cobranzas import reporte_cobranzas
from consultas_administrativas.views.reporte_pagos import reporte_pagos
from consultas_administrativas.views.subdiario_compras import subdiario_compras
from consultas_administrativas.views.subdiario_ventas import subdiario_ventas
from consultas_administrativas.views.balance_cobrar import balance_cobrar

urlpatterns = [
    #ventas
    path('subdiario_ventas/', subdiario_ventas, name='subdiario_ventas'),
    path('balance_cobrar/', balance_cobrar, name='balance_cobrar'),
    path('reporte_cobranzas/', reporte_cobranzas, name='reporte_cobranzas'),
    path('antiguedad_saldos/', antiguedad_saldos, name='antiguedad_saldos'),
    path('estados_cuenta/', estados_cuenta, name='estados_cuenta'),
    # ventas

    #compras
    path('subdiario_compras/', subdiario_compras, name='subdiario_compras'),
    path('balance_pagos/', balance_pagos, name='balance_pagos'),
    path('reporte_pagos/', reporte_pagos, name='reporte_pagos'),
    path('antiguedad_saldos_compras/', antiguedad_saldos_compras, name='antiguedad_saldos_compras'),
    path('estados_cuenta_compras/', estados_cuenta_compras, name='estados_cuenta_compras'),

    #compras


]
