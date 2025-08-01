from django.contrib import admin
from django.urls import path, include
from cargosystem import settings
from cargosystem.views.desbloquear import desbloquear, desbloquear_modulo_usuario
from login.views.correos import source_correo, correos
from login.views.home import home_view
from login.views.login import login_view, select_rol, logout_view, cambiar_modulo
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('', include('mantenimientos.urls')),
    path('', include('seguimientos.urls')),
    path('', include('notificaciones.urls')),
    path('admin_cont/', include('administracion_contabilidad.urls')),
    path('consultas_administrativas/', include('consultas_administrativas.urls')),
    path('importacion_maritima/', include('impomarit.urls')),
    path('exportacion_maritima/', include('expmarit.urls')),
    path('importacion_aerea/', include('impaerea.urls')),
    path('exportacion_aerea/', include('expaerea.urls')),
    path('importacion_terrestre/', include('impterrestre.urls')),
    path('exportacion_terrestre/', include('expterrestre.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='vista_logout'),
    path('login/seleccionarol/', select_rol, name="vista_roles"),
    path('login/seleccionarol/<str:rol>', select_rol, name="vista_roles"),
    path('cambiar_modulo/<str:modulo>/', cambiar_modulo, name="vista_cambiar_modulo"),
    path('correos/', correos, name='vista_correos'),
    path('source_correos/', source_correo, name='source_correos'),
    path('desbloquear/', desbloquear, name='desbloquear'),
    path('desbloquear_usuario_modulo/', desbloquear_modulo_usuario, name='desbloquear_usuario_modulo'),
    path('cambiar_clave/', PasswordChangeView.as_view(template_name='cambiar_clave.html',success_url='/clave_cambiada/'),name='cambiar_clave'),
    path('clave_cambiada/', PasswordChangeDoneView.as_view(template_name='clave_cambiada.html'), name='clave_cambiada'),



] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

