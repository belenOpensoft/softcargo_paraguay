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
from django.contrib import admin
from django.urls import path

from login.views.home import home_view
from login.views.login import login_view, select_rol, logout_view
from mantenimientos.views.ciudades import grilla_ciudades, source_ciudades, agregar_ciudad, modificar_ciudad, \
    eliminar_ciudad
from mantenimientos.views.clientes import grilla_clientes, source_socios_comerciales
from mantenimientos.views.vendedores import grilla_vendedores, source_vendedores, agregar_vendedor, modificar_vendedor, \
    eliminar_vendedor
from mantenimientos.views.buques import source_buques, grilla_buques, agregar_buque, modificar_buque, eliminar_buque
from mantenimientos.views.bancos import source_bancos, agregar_banco, modificar_banco, eliminar_banco, grilla_bancos
from mantenimientos.views.paises import grilla_paises, source_paises, agregar_pais, modificar_pais, eliminar_pais
from mantenimientos.views.monedas import source_monedas, grilla_monedas, modificar_moneda, eliminar_moneda, \
    agregar_moneda
from mantenimientos.views.productos import source_productos, agregar_producto, modificar_producto, eliminar_producto, \
    grilla_productos
from notificaciones.views.correos import envio_notificacion_seguimiento

urlpatterns = [
    ### CIUDADES ###
    path('envio_notificacion', envio_notificacion_seguimiento, name="envio_notificacion"),
    path('envio_notificacion/<str:modulo>/', envio_notificacion_seguimiento,name="envio_notificacion"),

]