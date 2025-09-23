import json
from datetime import datetime
import numpy as np
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from administracion_contabilidad.models import Dolar
from administracion_contabilidad.views.get_brou_rates import brou_rates
from cargosystem import settings
from login.forms import usuarioForm


def login_view(request):
    if request.user.is_authenticated:
        if 'rol' in request.session:
            return HttpResponseRedirect('/')
        else:
            logout(request)
            return HttpResponseRedirect('/login')
    else:
        contexto = {
            'form': usuarioForm(),
        }
        if request.method == 'POST':
            form = usuarioForm(request.POST)
            if form.is_valid():
                try:
                    usuario = form.cleaned_data['usuario']
                    clave = form.cleaned_data['clave']
                    usuario = authenticate(username=usuario, password=clave)
                    if usuario is not None and usuario.is_active:
                        login(request, usuario, None)
                        l_roles = list(usuario.groups.all().values_list('name', flat=True))
                        request.session['roles'] = l_roles
                        if len(l_roles) > 1:
                            request.session['roles'] = l_roles
                            return HttpResponseRedirect('seleccionarol/')
                        elif len(l_roles) == 1:
                            request.session['rol'] = str(l_roles[0])
                            request.session['empresa'] = settings.EMPRESA
                            return HttpResponseRedirect('/')
                        else:
                            messages.error(request, "El usuario no tiene roles asociados")
                    else:
                        contexto['form'] = form
                        messages.error(request, 'Nombre y/o clave incorrectos.')
                except Exception as e:
                    messages.error(request, str(e))
            else:
                messages.error(request, 'Formulario invalido, intente nuevamente')
    return render(request, 'login.html', contexto)


@login_required(login_url='/login/')
def select_rol(request, rol=None):
    if rol is not None:
        try:
            if rol in request.session['roles']:
                request.session['rol'] = rol
                request.session['empresa'] = settings.EMPRESA
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'No tiene permisos para ingresar a este modulo')
        except Exception as e:
            messages.error(request, str(e))
            return HttpResponseRedirect('/')
    if 'roles' not in request.session:
        return HttpResponseRedirect('/')
    roles = np.array_split(request.session['roles'], 5)
    ctx = {'roles': roles, }
    return render(request, 'roles.html', ctx)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def verificar_arbitraje_old(request):
    return render(request, 'forzar_arbitraje.html', {
        'hoy': datetime.today().strftime('%Y-%m-%d')
    })
def verificar_arbitraje(request):
    hoy = datetime.today().strftime('%Y-%m-%d')
    raw_rates = brou_rates()
    rates = json.loads(raw_rates.content.decode("utf-8"))

    arb_dolar = 0
    ui = 0
    tipo_moneda = "2"  # 2 = Dólares USA en tu <select>
    if getattr(settings, "DATOS_BROU"):
        if "dolar" in rates:
            try:
                arb_dolar = float(rates["dolar"]["bid"].replace(",", "."))
            except Exception as e:
                pass
        if "unidad_indexada" in rates:
            try:
                ui = float(rates["unidad_indexada"]["ask"].replace(",", "."))
            except Exception as e:
                pass

    return render(request, 'forzar_arbitraje.html', {
        'hoy': hoy,
        'arb_dolar': arb_dolar,
        'ui': ui,
        'tipo_moneda': tipo_moneda,
    })

def cambiar_modulo_old(request, modulo):
    request.session["rol"] = modulo
    if modulo == 'administracion':
        hoy = datetime.today().date()
        arbitraje_existente = Dolar.objects.filter(ufecha__date=hoy).exists()

        if not arbitraje_existente:
            return redirect('/admin_cont/verificar_arbitraje/')

    if modulo == 'seguimientos':
        return  HttpResponseRedirect('/seguimientos')
    else:
        return HttpResponseRedirect('/')


def cambiar_modulo(request, modulo):
    # solo actualizar la sesión si no vino por pestaña
    if not (
        request.headers.get('X-Rol-Activo') or request.GET.get('rol')
    ):
        request.session["rol"] = modulo

    if modulo == 'administracion':
        hoy = datetime.today().date()
        arbitraje_existente = Dolar.objects.filter(ufecha__date=hoy).exists()
        if not arbitraje_existente:
            return redirect('/admin_cont/verificar_arbitraje/')

    if modulo == 'seguimientos':
        return redirect('/seguimientos?rol=seguimientos')

    return redirect(f"/?rol={modulo}")
