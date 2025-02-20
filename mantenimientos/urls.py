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
from mantenimientos.views.clientes import grilla_clientes, agregar_socio_comercial, \
    source_socios_comerciales,eliminar_socio_comercial
from mantenimientos.views.vendedores import grilla_vendedores, source_vendedores, agregar_vendedor, modificar_vendedor, \
    eliminar_vendedor
from mantenimientos.views.buques import source_buques, grilla_buques, agregar_buque, modificar_buque, eliminar_buque
from mantenimientos.views.bancos import source_bancos, agregar_banco, modificar_banco, eliminar_banco, grilla_bancos
from mantenimientos.views.paises import grilla_paises, source_paises, agregar_pais, modificar_pais, eliminar_pais
from mantenimientos.views.monedas import source_monedas, grilla_monedas, modificar_moneda, eliminar_moneda, \
    agregar_moneda
from mantenimientos.views.productos import source_productos, agregar_producto, modificar_producto, eliminar_producto, \
    grilla_productos

from mantenimientos.views.servicios import source_servicios, agregar_servicio, modificar_servicio, eliminar_servicio, \
    grilla_servicios, clonar_servicio

urlpatterns = [
    ### CIUDADES ###
    path('ciudades', grilla_ciudades, name="vista_ciudades"),
    path('source_ciudades', source_ciudades, name="source_ciudades"),
    path('agregar_ciudad', agregar_ciudad, name="agregar_ciudad"),
    path('modificar_ciudad/<int:id_ciudad>', modificar_ciudad, name="modificar_ciudad"),
    path('eliminar_ciudad', eliminar_ciudad, name="eliminar_ciudad"),
    ### CLIENTES ###
    path('socios_comerciales', grilla_clientes, name="vista_socios_comerciales"),
    path('source_socios_comerciales', source_socios_comerciales, name="source_socios_comerciales"),
    path('agregar_socio_comercial', agregar_socio_comercial, name="agregar_socio_comercial"),
    path('modificar_socio_comercial/<int:id_socio>', agregar_socio_comercial, name="modificar_socio_comercial"),
    path('eliminar_socio_comercial', eliminar_socio_comercial, name="eliminar_socio_comercial"),
    ### VENDEDORES ###
    path('vendedores', grilla_vendedores, name="vista_vendedores"),
    path('source_vendedores', source_vendedores, name="source_vendedores"),
    path('agregar_vendedor', agregar_vendedor, name="agregar_vendedor"),
    path('modificar_vendedor/<int:id_vendedor>', modificar_vendedor, name="modificar_vendedor"),
    path('eliminar_vendedor', eliminar_vendedor, name="eliminar_vendedor"),
    ### BANCOS ###
    path('bancos', grilla_bancos, name="vista_bancos"),
    path('source_bancos', source_bancos, name="source_bancos"),
    path('agregar_banco', agregar_banco, name="agregar_banco"),
    path('modificar_banco/<int:id_banco>', modificar_banco, name="modificar_banco"),
    path('eliminar_banco', eliminar_banco, name="eliminar_banco"),
    ### PAISES ###
    path('source_paises', source_paises, name="source_paises"),
    path('paises', grilla_paises, name="vista_paises"),
    path('agregar_pais', agregar_pais, name="agregar_pais"),
    path('modificar_pais/<int:id_pais>', modificar_pais, name="modificar_pais"),
    path('eliminar_pais', eliminar_pais, name="eliminar_pais"),
    ### MONEDAS ###
    path('source_monedas', source_monedas, name="source_monedas"),
    path('monedas', grilla_monedas, name="vista_monedas"),
    path('agregar_moneda', agregar_moneda, name="agregar_moneda"),
    path('modificar_moneda/<int:id_moneda>', modificar_moneda, name="modificar_moneda"),
    path('eliminar_moneda', eliminar_moneda, name="eliminar_moneda"),
    ### PRODUCTOS ###
    path('source_productos', source_productos, name="source_productos"),
    path('productos', grilla_productos, name="vista_productos"),
    path('agregar_producto', agregar_producto, name="agregar_producto"),
    path('modificar_producto/<int:id_producto>', modificar_producto, name="modificar_producto"),
    path('eliminar_producto', eliminar_producto, name="eliminar_producto"),
    ### BUQUES ###
    path('source_buques', source_buques, name="source_buques"),
    path('buques', grilla_buques, name="vista_buques"),
    path('agregar_buque', agregar_buque, name="agregar_buque"),
    path('modificar_buque/<int:id_buque>', modificar_buque, name="modificar_buque"),
    path('eliminar_buque', eliminar_buque, name="eliminar_buque"),
    ### SERVICIOS ###
    path('servicios', grilla_servicios, name="vista_servicios"),
    path('source_servicios', source_servicios, name="source_servicios"),
    path('agregar_servicio', agregar_servicio, name="agregar_servicio"),
    path('modificar_servicio/<int:id_servicio>', modificar_servicio, name="modificar_servicio"),
    path('clonar_servicio/<int:id_servicio>', clonar_servicio, name="clonar_servicio"),
    path('eliminar_servicio', eliminar_servicio, name="eliminar_servicio")
]
