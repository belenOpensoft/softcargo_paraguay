from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime

from administracion_contabilidad.models import Asientos, Cuentas, Movims, Factudif, Dolar
from consultas_administrativas.forms import LibroDiarioForm, FichaEmbarqueForm
from expaerea.models import ExportEmbarqueaereo, ExportConexaerea
from expmarit.models import ExpmaritEmbarqueaereo
from expterrestre.models import ExpterraEmbarqueaereo
from impaerea.models import ImportEmbarqueaereo, ImportConexaerea
from impomarit.models import Embarqueaereo
from impterrestre.models import ImpterraEmbarqueaereo
from mantenimientos.models import Clientes, Monedas

import io
import datetime
from decimal import Decimal
from django.http import HttpResponse
import xlsxwriter

from seguimientos.models import Seguimiento


def ficha_embarque(request):
    resultados = []
    total_ingresos = 0
    total_egresos = 0
    rentabilidad = 0
    datos = {
        'conocimiento': '', 'origen': '', 'destino': '', 'vapor': '',
        'viaje': '', 'embarcador': '', 'agente': '', 'status': '',
        'transportista': '', 'interno': '', 'detalle': ''
    }


    if request.method == 'POST':
        form = FichaEmbarqueForm(request.POST)

        if form.is_valid():
            operativa = form.cleaned_data['operativa']
            master = form.cleaned_data['master']
            house = form.cleaned_data['house']
            posicion = form.cleaned_data['posicion']
            seguimiento = form.cleaned_data['seguimiento']
            detallar_preventas = form.cleaned_data['detallar_preventas']
            expresar_moneda_nac = form.cleaned_data['expresar_moneda_nac']

            if operativa:
                modelos = {
                    'importacion_maritima': Embarqueaereo,
                    'importacion_aerea': ImportEmbarqueaereo,
                    'importacion_terrestre': ImpterraEmbarqueaereo,
                    'exportacion_maritima': ExpmaritEmbarqueaereo,
                    'exportacion_aerea': ExportEmbarqueaereo,
                    'exportacion_terrestre': ExpterraEmbarqueaereo,
                }
                modelo = modelos.get(operativa)

                filtros = {}
                if modelo:
                    if master:
                        filtros['awb']=master
                    if house:
                        filtros['hawb']=house
                    if seguimiento:
                        filtros['seguimiento'] = seguimiento

                    embarque = modelo.objects.filter(**filtros).first()

                    #si tengo el embarque, traigo los movimientos asociados
                    if embarque:
                        asientos = Asientos.objects.filter(posicion=posicion).values_list('autogenerado', flat=True)
                    else:
                        asientos=None
                else:
                    embarque=None

                #si puedo buscar por posicion
                if posicion:
                    if not embarque: #si no hay embarque tampoco hay movimientos
                        #traigo los movimientos
                        #movimientos = Movims.objects.filter(mposicion=posicion)
                        asientos = Asientos.objects.filter(posicion=posicion).values_list('autogenerado', flat=True)
                        posicion_prefijo = posicion[:2]

                        if posicion_prefijo:
                            prefijos = {
                                'IM': Embarqueaereo,
                                'IA': ImportEmbarqueaereo,
                                'IT': ImpterraEmbarqueaereo,
                                'EM': ExpmaritEmbarqueaereo,
                                'EA': ExportEmbarqueaereo,
                                'ET': ExpterraEmbarqueaereo,
                            }
                            modelo = prefijos.get(posicion_prefijo)

                        if not modelo:
                            return HttpResponse('No se encontro el modelo')
                        #traigo el embarque
                        embarque = modelo.objects.filter(posicion=posicion).first()

                #si encontre un embarque
                if embarque:
                    if operativa == 'importacion_aerea':
                        conex = ImportConexaerea.objects.filter(numero=embarque.numero).first()
                    if operativa == 'exportacion_aerea':
                        conex = ExportConexaerea.objects.filter(numero=embarque.numero).first()


                    datos={
                        'posicion':embarque.posicion,
                        'conocimiento': str(embarque.awb or '')+str(embarque.hawb or ''),
                        'origen':embarque.origen,
                        'destino':embarque.destino,
                        'vapor':embarque.vapor if operativa != 'importacion_aerea' and operativa != 'exportacion_aerea' else conex.ciavuelo if conex else 'S/I',
                        'viaje':embarque.viaje if operativa != 'importacion_aerea' and operativa != 'exportacion_aerea' else conex.viaje if conex else 'S/I',
                        'embarcador':embarque.embarcador,
                        'agente':embarque.agente,
                        'status':embarque.status,
                        'transportista':embarque.transportista,
                        'interno':embarque.numero,
                        'detalle':None
                    }
                else:
                    return HttpResponse('No se encontro embarque')

                if asientos:
                    movimientos = Movims.objects.filter(mautogen__in=asientos)
                    movimientos.query

                if not movimientos:
                    return HttpResponse('No se encontraron movimientos')

                if detallar_preventas:

                    if posicion:
                        preventas = Factudif.objects.filter(zposicion=posicion)
                    elif master:
                        preventas = Factudif.objects.filter(zmaster=master)
                    elif seguimiento:
                        preventas = Factudif.objects.filter(zseguimiento=seguimiento)
                    elif house:
                        preventas = Factudif.objects.filter(zhouse=house)
                    else:
                        preventas = None

                for m in movimientos:
                    moneda = Monedas.objects.only('nombre').filter(codigo=m.mmoneda).first()
                    tipo = int(m.mtipo)
                    monto = float(m.mmonto)

                    if not expresar_moneda_nac:
                        monto=convertir_monto(monto, m.mmoneda,2,m.marbitraje,m.mparidad)
                    else:
                        monto = convertir_monto(monto,m.mmoneda,1,m.marbitraje,m.mparidad)

                    if tipo in [20, 41, 25]:  # Venta, Nota crédito proveedor, Cobro
                        ingresos = monto
                        egresos = 0.0
                    elif tipo in [40, 21, 45]:  # Compra, Nota crédito cliente, Pago
                        ingresos = 0.0
                        egresos = monto
                    else:
                        ingresos = 0.0
                        egresos = 0.0

                    resultados.append({
                        'tipo': m.mnombremov,
                        'tipo_numero':m.mtipo,
                        'numero': m.mboleta,
                        'fecha': m.mfechamov,
                        'socio': m.mnombre,
                        'ingresos': ingresos,
                        'egresos': egresos,
                        'detalle': m.mdetalle,
                        'moneda': moneda.nombre if moneda else 'S/I',
                    })

                total_ingresos = sum([r['ingresos'] for r in resultados])
                total_egresos=sum([r['egresos'] for r in resultados])
                rentabilidad = 0 #ver con ana

            # Acciones especiales
            if 'accion' in request.POST:
                if request.POST['accion'] == 'excel':
                    pass
                    #return generar_excel(resultados, conocimiento)
                elif request.POST['accion'] == 'imprimir':
                    pass
                    #return generar_pdf(resultados, conocimiento)

    else:
        form = FichaEmbarqueForm()

    return render(request, 'cargas_ca/ficha_embarque.html', {
        'form': form,
        'resultados': resultados,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'rentabilidad': rentabilidad,
        **datos,
    })

def generar_excel_libro_diario(asientos, moneda, fecha_desde, fecha_hasta, consolidar_dolares, consolidar_moneda_nac):
    try:
        nombre_archivo = f'Libro_Diario_{fecha_desde}_al_{fecha_hasta}.xlsx'
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Libro_diario")

        # Título
        titulo = f"Asientos entre el {fecha_desde.strftime('%d/%m/%Y')} y el {fecha_hasta.strftime('%d/%m/%Y')}"
        worksheet.merge_range('A1:O1', titulo, workbook.add_format({'bold': True, 'align': 'left'}))

        # Encabezados
        encabezados = [
            'Fecha', 'Asiento', 'Tipo', 'Número', 'Detalle', 'Cuenta', 'Nombre', 'Tipo C.',
            'Paridad', 'Debe', 'Haber', 'Mov', 'Socio Comercial', 'Moneda', 'Posición'
        ]

        for col_num, header in enumerate(encabezados):
            worksheet.write(1, col_num, header, workbook.add_format({
                'bold': True, 'bg_color': '#d9d9d9', 'border': 1
            }))

        columnas_fecha = [0]
        columnas_monto = [8, 9, 10]  # Paridad, Debe, Haber

        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        decimal_format = workbook.add_format({'num_format': '#,##0.00'})
        normal_format = workbook.add_format({'border': 1})

        row_num = 2
        for a in asientos:
            # Filtrar por moneda si no hay consolidación
            if not consolidar_dolares and not consolidar_moneda_nac and moneda:
                if a.moneda != moneda.codigo:
                    continue

            monto = Decimal(a.monto or 0)
            arbitraje = Decimal(a.cambio or 1)
            paridad = Decimal(a.paridad or 1)
            moneda_origen = a.moneda
            moneda_destino = None

            if consolidar_dolares:
                moneda_destino = 2
            elif consolidar_moneda_nac:
                moneda_destino = 1

            if moneda_destino:
                monto = convertir_monto(monto, moneda_origen, moneda_destino, arbitraje, paridad)

            # Definición de debe y haber según tipo
            if a.tipo == 'Z':  # Cobros
                debe = float(monto) if a.imputacion == 2 else 0.0
                haber = float(monto) if a.imputacion == 1 else 0.0
            elif a.tipo == 'G':  # Pagos
                debe = float(monto) if a.imputacion == 1 else 0.0
                haber = float(monto) if a.imputacion == 2 else 0.0
            elif a.tipo == 'V':  # Ventas
                debe = float(monto) if a.imputacion == 2 else 0.0
                haber = float(monto) if a.imputacion == 1 else 0.0
            elif a.tipo == 'P':  # Compras
                debe = float(monto) if a.imputacion == 1 else 0.0
                haber = float(monto) if a.imputacion == 2 else 0.0
            elif a.tipo in ['D', 'T', 'I']:  # Diversos, Traspasos, Iniciales
                debe = float(monto) if a.imputacion == 1 else 0.0
                haber = float(monto) if a.imputacion == 2 else 0.0
            elif a.tipo == 'C':  # Cierre
                debe = float(monto) if a.imputacion == 2 else 0.0
                haber = float(monto) if a.imputacion == 1 else 0.0
            elif a.tipo == 'B':  # Banco
                debe = float(monto) if a.imputacion == 1 else 0.0
                haber = float(monto) if a.imputacion == 2 else 0.0
            else:
                debe = 0.0
                haber = 0.0

            nombre_cta = Cuentas.objects.only('xnombre').filter(xcodigo=a.cuenta).first()
            nombre = nombre_cta.xnombre if nombre_cta else ''

            socio = Clientes.objects.only('empresa').filter(codigo=a.cliente).first()
            socio_comercial = socio.empresa if socio else ''

            if moneda_destino:
                nombre_moneda = "DOLARES USA" if moneda_destino == 2 else "MONEDA NACIONAL"
            else:
                nombre_moneda= Monedas.objects.only('nombre').filter(codigo=a.moneda).first()

            fila = [
                a.fecha,
                a.asiento,
                a.tipo,
                a.documento,
                a.detalle or '',
                a.cuenta,
                nombre,
                a.cambio,
                float(a.paridad or 0),
                debe,
                haber,
                a.mov,
                socio_comercial,
                nombre_moneda,
                a.posicion
            ]

            for col_num, valor in enumerate(fila):
                if col_num in columnas_fecha and isinstance(valor, (datetime.date, datetime.datetime)):
                    worksheet.write(row_num, col_num, valor, date_format)
                elif col_num in columnas_monto:
                    worksheet.write(row_num, col_num, valor, decimal_format)
                else:
                    worksheet.write(row_num, col_num, valor, normal_format)
            row_num += 1

        worksheet.set_column('A:A', 10)  # Fecha
        worksheet.set_column('B:B', 10)  # Asiento
        worksheet.set_column('C:D', 8)   # Tipo, Número
        worksheet.set_column('E:E', 30)  # Detalle
        worksheet.set_column('F:F', 10)  # Cuenta
        worksheet.set_column('G:G', 35)  # Nombre
        worksheet.set_column('H:H', 10)  # Tipo C.
        worksheet.set_column('I:I', 10)  # Paridad
        worksheet.set_column('J:K', 14)  # Debe, Haber
        worksheet.set_column('L:L', 10)  # Mov
        worksheet.set_column('M:M', 25)  # Socio
        worksheet.set_column('N:N', 20)  # Moneda
        worksheet.set_column('O:O', 15)  # Posición

        workbook.close()
        output.seek(0)

        return HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
        )

    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel del libro diario: {e}")


def convertir_monto(monto, origen, destino, arbitraje, paridad):
    """
    Convierte un monto desde 'origen' a 'destino' utilizando arbitraje y paridad.
    origen y destino son enteros representando códigos de moneda:
    1 = moneda nacional, 2 = dólar, otros = otras monedas (ej: euro)
    """


    try:
        if arbitraje is None:
            dolar = Dolar.objects.filter(ufecha__date=datetime.date.today()).first()
            if dolar:
                arbitraje = float(dolar.uvalor)

        if origen == destino or monto == 0:
            return round(monto, 2)

        if destino == 1:  # convertir a moneda nacional
            if origen == 2 and arbitraje:
                return round(monto * arbitraje, 2)
            elif origen not in [1, 2] and arbitraje and paridad:
                dolares = monto / paridad
                return round(dolares * arbitraje, 2)

        elif destino == 2:  # convertir a dólares
            if origen == 1 and arbitraje:
                return round(monto / arbitraje, 2)
            elif origen not in [1, 2] and paridad:
                return round(monto / paridad, 2)

        else:  # convertir a otra moneda
            if origen == 1 and arbitraje and paridad:
                dolares = monto / arbitraje
                return round(dolares * paridad, 2)
            elif origen == 2 and paridad:
                return round(monto * paridad, 2)
            elif origen == destino:
                return round(monto, 2)

        # Si no se puede convertir, devolver sin modificar
        return round(monto, 2)
    except Exception as e:
        return str(e)
