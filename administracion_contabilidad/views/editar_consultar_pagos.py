from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from administracion_contabilidad.forms import EditarConsultarPagos

def editar_consultar_pagos(request):
    if request.user.has_perms(["administracion_contabilidad.view_forzarerror", ]):
        form = EditarConsultarPagos(request.POST or None)
        return render(request, 'editar_consultar_pagos.html', {'form': form})
    else:
        messages.error(request,'Funcionalidad en construcción.')
        return HttpResponseRedirect('/')