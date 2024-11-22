from django.shortcuts import render
from administracion_contabilidad.forms import EditarConsultarPagos

def editar_consultar_pagos(request):
    form = EditarConsultarPagos(request.POST or None)
    return render(request, 'editar_consultar_pagos.html', {'form': form})
