import datetime
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from mantenimientos.forms import add_vendedor_form, edit_vendedor_form
from mantenimientos.models import Vendedores, Ciudades, Paises


@login_required(login_url='/')
def grilla_vendedores(request):
    try:
        if request.user.has_perms(["mantenimientos.view_vendedores",]):
            return render(request, 'vendedores/grilla_datos.html',{'title_page':'Mantenimiento de vendedores',})
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')
""" VISTA """

""" TABLA PUERTO """
columns_table = {
    0: 'id',
    1: 'codigo',
    2: 'nombre',
    3: 'direccion',
    4: 'localidad',
    5: 'ciudad',
    6: 'pais',
    7: 'telefono',
    8: 'email',
}
param_busqueda = {

    1: 'codigo__icontains',
    2: 'nombre__icontains',
    3: 'direccion__icontains',
    4: 'localidad__icontains',
    5: 'ciudad__icontains',
    6: 'pais__icontains',
    7: 'telefonos__icontains',
    8: 'email__icontains',
}
def source_vendedores(request):
    if is_ajax(request):
        """ BUSCO ORDEN """
        args = {
            '1': request.GET['columns[1][search][value]'],
            '2': request.GET['columns[2][search][value]'],
            '3': request.GET['columns[3][search][value]'],
            '4': request.GET['columns[4][search][value]'],
            '5': request.GET['columns[5][search][value]'],
            '6': request.GET['columns[6][search][value]'],
            '7': request.GET['columns[7][search][value]'],
            '8': request.GET['columns[8][search][value]'],
        }
        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        if filtro:
            registros = Vendedores.objects.filter(**filtro).order_by(*order)
        else:
            registros = Vendedores.objects.all().order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Vendedores.objects.all().count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)
def get_data(puertos_filtrados):
    try:
        data = []
        for puerto in puertos_filtrados:
            puerto_json = []
            puerto_json.append(str(puerto.id))
            puerto_json.append('' if puerto.codigo is None else str(puerto.codigo))
            puerto_json.append('' if puerto.nombre is None else str(puerto.nombre))
            puerto_json.append('' if puerto.direccion is None else str(puerto.direccion))
            puerto_json.append('' if puerto.localidad is None else str(puerto.localidad))
            puerto_json.append('' if puerto.ciudad is None else str(puerto.ciudad))
            puerto_json.append('' if puerto.pais is None else str(puerto.pais))
            puerto_json.append('' if puerto.telefono is None else str(puerto.telefono))
            puerto_json.append('' if puerto.email is None else str(puerto.email))
            data.append(puerto_json)
        return data
    except Exception as e:
        raise TypeError(e)
def get_order(request, columns):
    try:
        result = []
        order_column = request.GET['order[0][column]']
        order_dir = request.GET['order[0][dir]']
        order = columns[int(order_column)]
        if order_dir == 'desc':
            order = '-' + columns[int(order_column)]
        result.append(order)
        i = 1
        while i > 0:
            try:
                order_column = request.GET['order[' + str(i) + '][column]']
                order_dir = request.GET['order[' + str(i) + '][dir]']
                order = columns[int(order_column)]
                if order_dir == 'desc':
                    order = '-' + columns[int(order_column)]
                result.append(order)
                i += 1
            except Exception as e:
                i = 0
        result.append('id')
        return result
    except Exception as e:
        raise TypeError(e)
def get_argumentos_busqueda(**kwargs):
    try:
        result = {}
        for row in kwargs:
            if len(kwargs[row]) > 0:
                result[param_busqueda[int(row)]] = kwargs[row]
        return result
    except Exception as e:
        raise TypeError(e)
def is_ajax(request):
    return True

@login_required(login_url="/")
def agregar_vendedor(request):
    try:
        if request.user.has_perms(["mantenimientos.add_vendedores",]):
           # ctx = {'form': add_vendedor_form(),'title_page':'Agregar vendedor'}
            if request.method == 'POST':
                form = add_vendedor_form(request.POST)
                if form.is_valid():
                    vendedor = Vendedores()
                    ultimo_codigo = Vendedores.objects.order_by('-codigo').values_list('codigo', flat=True).first()
                    vendedor.codigo = ultimo_codigo + 1
                    vendedor.nombre = form.cleaned_data['nombre']
                    vendedor.direccion = form.cleaned_data['direccion']
                    vendedor.telefono = form.cleaned_data['telefono']
                    vendedor.localidad = form.cleaned_data['localidad']
                    vendedor.ciudad = form.cleaned_data['ciudad']
                    vendedor.pais = form.cleaned_data['pais']
                    vendedor.email = form.cleaned_data['email']
                    #vendedor.activo = form.cleaned_data['activo']
                    """ DATOS EXTRA GRILLA """
                   # vendedor.fax = form.cleaned_data['fax']
                    #vendedor.email = form.cleaned_data['observaciones']
                   # vendedor.condiciones = form.cleaned_data['condiciones']
                    vendedor.save()
                    messages.success(request, 'Vendedor agregado con èxito')
                    return HttpResponseRedirect('/vendedores')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    return HttpResponseRedirect('/agregar_vendedor')
            else:
                form = add_vendedor_form()
            paises = Paises.objects.all()  # Obtén la lista de países
            ciudades = Ciudades.objects.all()  # Obtén la lista de países
            ctx = {'form': form, 'title_page': 'Agregar Vendedor', 'paises': paises, 'ciudades': ciudades}
            return render(request, "vendedores/agregar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/vendedores")

@login_required(login_url='/')
def modificar_vendedor(request, id_vendedor):
    try:
        if request.user.has_perms(["mantenimientos.change_vendedores", ]):
            vendedor = Vendedores.objects.get(id=id_vendedor)
            paises = Paises.objects.all()  # Obtén la lista de países
            ciudades = Ciudades.objects.all()  # Obtén la lista de países
            ctx = {'form': edit_vendedor_form({
                'codigo': vendedor.codigo,
                'nombre': vendedor.nombre,
                'direccion': vendedor.direccion,
                'localidad': vendedor.localidad,
                'ciudad': vendedor.ciudad,
                'pais': vendedor.pais,
                'telefono': vendedor.telefono,
                'email': vendedor.email,
            },

            ),'title_page':'Modificar vendedor'
            , 'paises': paises, 'ciudades': ciudades,}
            if request.method == 'POST':
                form = edit_vendedor_form(request.POST)
                if form.is_valid():
                    vendedor.codigo = form.cleaned_data['codigo']
                    vendedor.nombre = form.cleaned_data['nombre']
                    vendedor.direccion = form.cleaned_data['direccion']
                    vendedor.telefono = form.cleaned_data['telefono']
                    vendedor.localidad = form.cleaned_data['localidad']
                    vendedor.ciudad = form.cleaned_data['ciudad']
                    vendedor.pais = form.cleaned_data['pais']
                    vendedor.email = form.cleaned_data['email']
                    #vendedor.activo = form.cleaned_data['activo']
                    vendedor.save()
                    messages.success(request, 'Vendedor modificada con èxito')
                    return HttpResponseRedirect('/vendedores')
                else:
                    messages.error(request, 'Formulario invalido, intente nuevamente.')
                    #return HttpResponseRedirect('/modificar_vendedor')
            else:
                return render(request, "vendedores/modificar.html", ctx)
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/vendedores")


@login_required(login_url='/')
def eliminar_vendedor(request):

    resultado = {}
    if request.user.has_perms(["mantenimientos.delete_vendedores", ]):
        if is_ajax(request):
            try:
                id = request.GET['id']
                vendedor = Vendedores.objects.get(id=id)
                vendedor.delete()
                resultado['resultado'] = 'exito'
            except Exception as e:
                resultado['resultado'] = str(e)
        else:
            resultado['resultado'] = 'Ha ocurrido un error.'
    else:
        resultado['resultado'] = 'No tiene permisos para realizar esta accion.'
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


