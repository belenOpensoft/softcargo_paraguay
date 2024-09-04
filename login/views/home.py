from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from notificaciones.views.correos import envio_correo_electronico


@login_required(login_url='/login/')
def home_view(request):
    try:
        # envio_correo_electronico('mensaje de prueba',['tecnicosnm@gmail.com',],'ASUNTO DE PRUEBA')
        return render(request, 'base.html')
        # return render(request, 'menu/prueba.html')
    except Exception as e:
        messages.error(request,str(e))
        return render(request, 'base.html')