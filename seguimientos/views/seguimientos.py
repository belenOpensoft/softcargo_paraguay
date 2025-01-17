import json
from copy import deepcopy
import simplejson as simplejson
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from seguimientos.forms import notasForm, seguimientoForm, cronologiaForm, envasesForm, embarquesForm, gastosForm, \
    pdfForm, archivosForm, rutasForm, emailsForm, clonarForm
from seguimientos.models import VGrillaSeguimientos as Seguimiento, Seguimiento as SeguimientoReal, Envases, Cargaaerea, \
    Attachhijo, Serviceaereo, Conexaerea


@login_required(login_url='/')
def grilla_seguimientos(request):
    try:
        if request.user.has_perms(["seguimientos.view_seguimiento", ]):
            opciones_busqueda = {
                'cliente__icontains': 'CLIENTE',
                'embarcador__icontains': 'EMBARCADOR',
                'consignatario__icontains': 'CONSIGNATARIO',
                'origen_text__icontains': 'ORIGEN',
                'destino_text__icontains': 'DESTINO',
                'awb__icontains': 'BL',
                'hawb__icontains': 'HBL',
                'vapor__icontains': 'Vapor',
                'posicion__icontains': 'Posicion',
                # 'contenedores__icontains': 'Contenedor',
            }
            return render(request, 'seguimientos/grilla_datos.html', {
                'form_notas': notasForm(),
                'form_emails': emailsForm(),
                'form': seguimientoForm(),
                'form_cronologia': cronologiaForm(),
                'form_envases': envasesForm(),
                'form_embarques': embarquesForm(),
                'form_gastos': gastosForm(),
                'form_pdf': pdfForm(),
                'form_archivos': archivosForm(),
                'form_rutas': rutasForm(),
                'form_clonar': clonarForm(),
                'title_page': 'Seguimientos',
                'opciones_busqueda': opciones_busqueda,
            })
        else:
            raise TypeError('No tiene permisos para realizar esta accion.')
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect('/')


""" VISTA """

param_busqueda = {
    1: 'numero__icontains',
    2: 'modo__icontains',
    3: 'cliente__icontains',
    4: 'origen__icontains',
    5: 'destino__icontains',
    6: 'fecha__icontains',
    7: 'status__icontains',
}
""" TABLA PUERTO """
columns_table = {
    0: 'id',
    1: 'numero',
    2: 'modo',
    3: 'cliente',
    4: 'origen',
    5: 'destino',
    6: 'fecha',
    7: 'status',
}


def source_seguimientos(request):
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
        }
        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        buscar = str(request.GET['buscar'])
        que_buscar = str(request.GET['que_buscar'])
        if len(buscar) > 0:
            filtro[que_buscar] = buscar
        end = start + length
        order = get_order(request, columns_table)
        """FILTRO REGISTROS"""
        if filtro:
            registros = Seguimiento.objects.filter(**filtro).order_by(*order)
        else:
            registros = Seguimiento.objects.all().order_by(*order)
        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])
        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Seguimiento.objects.all().count()
        resultado['recordsFiltered'] = str(registros.count())
        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def source_seguimientos_modo_old(request, modo):
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
        }
        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])

        # Agrega el filtro de modo
        filtro['modo'] = modo  # Aquí se asegura que solo traiga registros que coincidan con el modo

        end = start + length
        order = get_order(request, columns_table)

        """FILTRO REGISTROS"""
        if filtro:
            registros = Seguimiento.objects.filter(**filtro).order_by(*order)
        else:
            registros = Seguimiento.objects.all().order_by(*order)

        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])

        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Seguimiento.objects.all().count()
        resultado['recordsFiltered'] = str(registros.count())

        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'

    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def source_seguimientos_modo(request, modo):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        """ BUSCO ORDEN """
        args = {
            '1': request.GET['columns[1][search][value]'],
            '2': request.GET['columns[2][search][value]'],
            '3': request.GET['columns[3][search][value]'],
            '4': request.GET['columns[4][search][value]'],
            '5': request.GET['columns[5][search][value]'],
            '6': request.GET['columns[6][search][value]'],
            '7': request.GET['columns[7][search][value]'],
        }

        """PROCESO FILTRO Y ORDEN BY"""
        filtro = get_argumentos_busqueda(**args)
        start = int(request.GET['start'])
        length = int(request.GET['length'])

        # Agrega el filtro de modo
        filtro['modo'] = modo

        end = start + length
        order = get_order(request, columns_table)

        # Obtener el array de IDs agregados desde la solicitud
        ids_agregados = request.GET.getlist('ids_agregados[]')

        """FILTRO REGISTROS"""
        if filtro:
            registros = Seguimiento.objects.filter(**filtro).order_by(*order)
        else:
            registros = Seguimiento.objects.all().order_by(*order)

        # Excluir los registros que están en el array de 'agregados', solo si no está vacío
        if ids_agregados:
            registros = registros.exclude(id__in=ids_agregados)

        """PREPARO DATOS"""
        resultado = {}
        data = get_data(registros[start:end])

        """Devuelvo parametros"""
        resultado['data'] = data
        resultado['length'] = length
        resultado['draw'] = request.GET['draw']
        resultado['recordsTotal'] = Seguimiento.objects.all().count()
        resultado['recordsFiltered'] = registros.count()

        data_json = json.dumps(resultado)
    else:
        data_json = 'fail'

    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def get_data(registros_filtrados):
    try:
        data = []
        cronologia = [
            'fecha',
            'estimadorecepcion',
            'recepcion',
            'fecemision',
            'fecseguro',
            'fecdocage',
            'loadingdate',
            'arriboreal',
            'fecaduana',
            'pagoenfirme',
            'vencimiento',
            'etd',
            'eta',
            'fechaonhand',
            'fecrecdoc',
            'recepcionprealert',
            'lugar',
            'nroseguro',
            'bltipo',
            'manifiesto',
            'credito',
            'prima',
            'observaciones',

        ]
        for registro in registros_filtrados:
            registro_json = []
            registro_json.append(str(registro.id))
            registro_json.append('' if registro.numero is None else str(registro.numero))
            registro_json.append('' if registro.modo is None else str(registro.modo))
            registro_json.append('' if registro.cliente is None else str(registro.cliente))
            registro_json.append('' if registro.origen is None else str(registro.origen))
            registro_json.append('' if registro.destino is None else str(registro.destino))
            registro_json.append('' if registro.fecha is None else str(registro.fecha)[:10])
            registro_json.append('' if registro.status is None else str(registro.status))
            """ EXTRAS """
            registro_json.append('' if registro.notas is None else str(registro.notas))
            """ PRIMER COLUMNA """
            registro_json.append('' if registro.cliente is None else str(registro.cliente))
            registro_json.append('' if registro.embarcador is None else str(registro.embarcador))
            registro_json.append('' if registro.consignatario is None else str(registro.consignatario))
            registro_json.append('' if registro.notificar is None else str(registro.notificar))
            registro_json.append('' if registro.agente is None else str(registro.agente))
            registro_json.append('' if registro.transportista is None else str(registro.transportista))
            registro_json.append('' if registro.armador is None else str(registro.armador))
            registro_json.append('' if registro.agecompras is None else str(registro.agecompras))
            registro_json.append('' if registro.ageventas is None else str(registro.ageventas))
            registro_json.append('' if registro.despachante is None else str(registro.despachante))
            """ SEGUNDA COLUMNA """
            registro_json.append('' if registro.nroreferedi is None else str(registro.nroreferedi))
            registro_json.append('' if registro.moneda is None else str(registro.moneda))
            registro_json.append('' if registro.vendedor is None else str(registro.vendedor))
            registro_json.append('' if registro.deposito is None else str(registro.deposito))
            registro_json.append('' if registro.vapor is None else str(registro.vapor))
            registro_json.append('' if registro.viaje is None else str(registro.viaje))
            registro_json.append('' if registro.awb is None else str(registro.awb))
            registro_json.append('' if registro.hawb is None else str(registro.hawb))
            registro_json.append('' if registro.operacion is None else str(registro.operacion))
            registro_json.append('' if registro.refcliente is None else str(registro.refcliente))
            """ TERCER COLUMNA """
            registro_json.append('' if registro.loading is None else str(registro.loading))
            registro_json.append('' if registro.discharge is None else str(registro.discharge))
            registro_json.append('' if registro.posicion is None else str(registro.posicion))
            registro_json.append('' if registro.pago is None else str(registro.pago))
            registro_json.append('' if registro.arbitraje is None else str(registro.arbitraje))
            registro_json.append('' if registro.ubicacion is None else str(registro.ubicacion))
            registro_json.append('' if registro.booking is None else str(registro.booking))
            registro_json.append('' if registro.trackid is None else str(registro.trackid))
            registro_json.append('' if registro.proyecto is None else str(registro.proyecto))
            registro_json.append('' if registro.trafico is None else str(registro.trafico))
            registro_json.append('' if registro.actividad is None else str(registro.actividad))
            registro_json.append('' if registro.demora is None else str(registro.demora))
            registro_json.append('' if registro.diasalmacenaje is None else str(registro.diasalmacenaje))
            registro_json.append('' if registro.wreceipt is None else str(registro.wreceipt))
            registro_json.append('' if registro.valor is None else str(registro.valor))
            # archivos = Attachhijo.objects.filter(numero=registro.numero).annotate(num_archivos=Count('id')).values('num_archivos').first()
            # embarques = Cargaaerea.objects.filter(numero=registro.numero).annotate(num_archivos=Count('id')).values('num_archivos').first()
            # envases = Envases.objects.filter(numero=registro.numero).annotate(num_archivos=Count('id')).values('num_archivos').first()
            # gastos = Serviceaereo.objects.filter(numero=registro.numero).annotate(num_archivos=Count('id')).values('num_archivos').first()
            # rutas = Conexaerea.objects.filter(numero=registro.numero).annotate(num_archivos=Count('id')).values('num_archivos').first()
            archivos = Attachhijo.objects.filter(numero=registro.numero).count()
            embarques = Cargaaerea.objects.filter(numero=registro.numero).count()
            envases = Envases.objects.filter(numero=registro.numero).count()
            gastos = Serviceaereo.objects.filter(numero=registro.numero).count()
            rutas = Conexaerea.objects.filter(numero=registro.numero).count()
            #falta historial
            registro_json.append(archivos)
            registro_json.append(embarques)
            registro_json.append(envases)
            registro_json.append(gastos)
            crono = False
            registro2 = SeguimientoReal()
            campos = vars(registro2)
            for c in campos:
                if c in cronologia:
                    aux = getattr(registro2, c)
                    if aux is not None:
                        crono = True
            registro_json.append(crono)
            registro_json.append(rutas)
            """ cargo emails segun el tipo de seguimiento """
            if registro.modo == 'IMPORT MARITIMO':
                registro_json.append(registro.emailim)
            elif registro.modo == 'IMPORT AEREO':
                registro_json.append(registro.emailia)
            elif registro.modo == 'IMPORT TERRESTRE':
                registro_json.append(registro.emailit)
            elif registro.modo == 'EXPORT MARITIMO':
                registro_json.append(registro.emailem)
            elif registro.modo == 'EXPORT AEREO':
                registro_json.append(registro.emailea)
            elif registro.modo == 'EXPORT TERRESTRE':
                registro_json.append(registro.emailet)
            else:
                registro_json.append('')

            #registro_json.append(historial)
            data.append(registro_json)
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
    try:
        req = request.META.get('HTTP_X_REQUESTED_WITH')
        # return req == 'XMLHttpRequest'
        return True
    except Exception as e:
        messages.error(request, e)


def guardar_notas(request):
    resultado = {}
    try:
        id = request.POST['id']
        data = simplejson.loads(request.POST['data'])
        registro = SeguimientoReal.objects.get(id=id)
        registro.observaciones = data[0]['value']
        registro.save()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def guardar_envases(request):
    resultado = {}
    try:
        numero = request.POST['numero']
        data = simplejson.loads(request.POST['data'])
        registro = Envases()
        campos = vars(registro)
        for x in data:
            k = x['name']
            v = x['value']
            for name in campos:
                if name == k:
                    if v is not None and len(v) > 0:
                        if v is not None:
                            setattr(registro, name, v)
                        else:
                            if len(v) > 0:
                                setattr(registro, name, v)
                    else:
                        setattr(registro, name, None)
                    continue
        registro.numero = numero
        registro.save()
        resultado['resultado'] = 'exito'
        resultado['numero'] = str(registro.numero)
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def eliminar_envase(request):
    resultado = {}
    try:
        id = request.POST['id']
        Envases.objects.get(id=id).delete()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def guardar_cronologia(request):
    resultado = {}
    try:
        id = request.POST['id']
        data = simplejson.loads(request.POST['data'])
        registro = SeguimientoReal.objects.get(id=id)
        campos = vars(registro)
        for name in campos:
            for d in data:
                if name in d['name']:
                    if len(d['value']) > 0:
                        setattr(registro, name, d['value'])
                    else:
                        setattr(registro, name, None)
        registro.save()
        resultado['resultado'] = 'exito'
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente.'
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def guardar_seguimiento(request):
    resultado = {}
    try:
        data = simplejson.loads(request.POST['form'])
        tipo = request.POST['tipo']

        if 'id' in data and data['id'][0] != '':
            registro = SeguimientoReal.objects.get(id=data['id'][0])
            tiporeg = 'modifica'
        else:
            registro = SeguimientoReal()
            numero = SeguimientoReal.objects.all().values_list('numero').order_by('-numero')[:1][0][0]
            registro.numero = numero + 1
            tiporeg = 'nuevo'
        campos = vars(registro)
        for k, v in data.items():
            for name in campos:
                if name == k:
                    if v[0] is not None and len(v[0]) > 0:
                        if v[1] is not None:
                            setattr(registro, name, v[1])
                        else:
                            if len(v[0]) > 0:
                                setattr(registro, name, v[0])
                    else:
                        setattr(registro, name, None)
                    continue
        registro.modo = tipo
        if 'id' in data and data['id'][0] != '':
            registro.id = data['id'][0]
            registro.save()
        else:
            registro.save()
        resultado['resultado'] = 'exito'
        resultado['numero'] = str(registro.numero)
        resultado['tipo'] = tiporeg
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente:. ' + str(e)
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)


def clonar_seguimiento(request):
    resultado = {}
    try:
        data = simplejson.loads(request.POST['data'])
        original = SeguimientoReal.objects.get(id=request.POST['id'])
        numero = SeguimientoReal.objects.all().values_list('numero').order_by('-numero')[:1][0][0]
        clonado = deepcopy(original)
        clonado.id = None
        clonado.numero = numero + 1
        for row in data:
            registros = None
            if row['name'] == 'envases' and row['value'] == 'SI':
                registros = Envases.objects.filter(numero=original.numero)
            elif row['name'] == 'embarques' and row['value'] == 'SI':
                registros = Cargaaerea.objects.filter(numero=original.numero)
            elif row['name'] == 'gastos' and row['value'] == 'SI':
                registros = Serviceaereo.objects.filter(numero=original.numero)
            elif row['name'] == 'trasbordo' and row['value'] == 'SI':
                registros = Conexaerea.objects.filter(numero=original.numero)
            if registros is not None and registros.count() > 0:
                for r in registros:
                    aux = deepcopy(r)
                    aux.numero = clonado.numero
                    aux.id = None
                    aux.save()
        clonado.save()
        resultado['resultado'] = 'exito'
        resultado['numero'] = str(clonado.numero)
    except IntegrityError as e:
        resultado['resultado'] = 'Error de integridad, intente nuevamente:. ' + str(e)
    except Exception as e:
        resultado['resultado'] = str(e)
    data_json = json.dumps(resultado)
    mimetype = "application/json"
    return HttpResponse(data_json, mimetype)
