from django.urls import path

from consultas_administrativas.views.balance_evolutivo import balance_evolutivo
from consultas_administrativas.views.consulta_arbitrajes import consulta_arbitrajes
from consultas_administrativas.views.antiguedad_saldos import antiguedad_saldos
from consultas_administrativas.views.antiguedad_saldos_compras import antiguedad_saldos_compras
from consultas_administrativas.views.antiguedad_saldos_mixtas import antiguedad_saldos_mixtas
from consultas_administrativas.views.balance_mixtas import balance_mixtas
from consultas_administrativas.views.balance_pagar import balance_pagos
from consultas_administrativas.views.estados_cuenta import estados_cuenta
from consultas_administrativas.views.estados_cuenta_compras import estados_cuenta_compras
from consultas_administrativas.views.estados_cuenta_mixtas import estados_cuenta_mixtas
from consultas_administrativas.views.ficha_embarque import ficha_embarque
from consultas_administrativas.views.libro_diario import libro_diario
from consultas_administrativas.views.mayores_analiticos import mayores_analiticos
from consultas_administrativas.views.plan_cuentas import plan_cuentas
from consultas_administrativas.views.reporte_cobranzas import reporte_cobranzas
from consultas_administrativas.views.reporte_pagos import reporte_pagos
from consultas_administrativas.views.subdiario_compras import subdiario_compras
from consultas_administrativas.views.subdiario_ventas import subdiario_ventas
from consultas_administrativas.views.balance_cobrar import balance_cobrar
from consultas_administrativas.views.utilidad_mensual_posicion import utilidad_mensual_posicion

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

    #mixtas
    path('balance_mixtas/', balance_mixtas, name='balance_mixtas'),
    path('estados_cuenta_mixtas/', estados_cuenta_mixtas, name='estados_cuenta_mixtas'),
    path('antiguedad_saldos_mixtas/', antiguedad_saldos_mixtas, name='antiguedad_saldos_mixtas'),

    #mixtas

    #contabilidad
    path('plan_cuentas/', plan_cuentas, name='plan_cuentas'),
    path('consulta_arbitrajes/', consulta_arbitrajes, name='consulta_arbitrajes'),
    path('libro_diario/', libro_diario, name='libro_diario'),
    path('mayores_analiticos/', mayores_analiticos, name='mayores_analiticos'),
    path('balance_evolutivo/', balance_evolutivo, name='balance_evolutivo'),

    #contabilidad

    #cargas
    path('ficha_embarque/', ficha_embarque, name='ficha_embarque'),
    path('utilidad_mensual_posicion/', utilidad_mensual_posicion, name='utilidad_mensual_posicion'),

    #cargas


]
