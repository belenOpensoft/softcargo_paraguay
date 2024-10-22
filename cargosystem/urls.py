from django.contrib import admin
from django.urls import path, include
from cargosystem import settings
from login.views.correos import source_correo, correos
from login.views.home import home_view
from login.views.login import login_view, select_rol, logout_view, cambiar_modulo
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('', include('mantenimientos.urls')),
    path('', include('seguimientos.urls')),
    path('', include('notificaciones.urls')),
    path('', include('administracion_contabilidad.urls')),
    path('importacion_maritima/', include('impomarit.urls')),
    path('exportacion_maritima/', include('expmarit.urls')),
    path('importacion_aerea/', include('impaerea.urls')),
    path('exportacion_aerea/', include('expaerea.urls')),
    path('importacion_terrestre/', include('impterrestre.urls')),
    path('exportacion_terrestre/', include('expterrestre.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='vista_logout'),
    path('login/selecccionarol/', select_rol, name="vista_roles"),
    path('login/selecccionarol/<str:rol>', select_rol, name="vista_roles"),
    path('cambiar_modulo/<str:modulo>', cambiar_modulo, name="vista_cambiar_modulo"),
    path('correos/', correos, name='vista_correos'),
    path('source_correos/', source_correo, name='source_correos')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

