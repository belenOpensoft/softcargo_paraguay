import datetime
import io
from decimal import Decimal

import xlsxwriter
from django.http import HttpResponse
from django.shortcuts import render

from administracion_contabilidad.models import Impuvtas, Movims
from consultas_administrativas.forms import ReporteMovimientosForm
from consultas_administrativas.models import VReporteSubdiarioVentas
from impomarit.models import VistaOperativas


def subdiario_ventas_old(request):
    if request.method == 'POST':
        form = ReporteMovimientosForm(request.POST)
        if form.is_valid():
            # Obtenemos los datos limpios del formulario
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            moneda = form.cleaned_data['moneda']
            todas_monedas = form.cleaned_data['todas_monedas']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            socio_comercial = form.cleaned_data['socio_comercial']
            movimiento = form.cleaned_data['movimiento']
            estado = form.cleaned_data['estado']

            # Acá podés generar el archivo o realizar acciones
            print("Desde:", fecha_desde)
            print("Hasta:", fecha_hasta)
            print("Moneda:", moneda)
            print("Todas monedas:", todas_monedas)
            print("Consolidar:", consolidar_dolares)
            print("Socio Comercial:", socio_comercial)
            print("Movimiento:", movimiento)
            print("Estado:", estado)

            # Por ejemplo, podrías retornar un archivo o una respuesta
            return HttpResponse("Formulario recibido. (Acá generarías el reporte)")

    else:
        form = ReporteMovimientosForm(initial={'estado': 'todo'})

    return render(request, 'ventas_ca/subdiario_ventas.html', {'form': form})

def subdiario_ventas(request):
    if request.method == 'POST':
        form = ReporteMovimientosForm(request.POST)
        if form.is_valid():
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            moneda = form.cleaned_data['moneda']
            todas_monedas = form.cleaned_data['todas_monedas']
            consolidar_dolares = form.cleaned_data['consolidar_dolares']
            socio_comercial = form.cleaned_data['socio_comercial_i']
            movimiento = form.cleaned_data['movimiento']
            estado = form.cleaned_data['estado']

            filtros = {
                'fecha__range': (fecha_desde, fecha_hasta)
            }

            if not todas_monedas and moneda:
                filtros['moneda'] = moneda.nombre

            if socio_comercial:
                filtros['nro_cliente'] = socio_comercial

            if estado == 'canceladas':
                filtros['cancelada'] = 'SI'
            elif estado == 'pendientes':
                filtros['cancelada'] = 'NO'

            if movimiento and movimiento !='todos':
                filtros['tipo'] = movimiento

            queryset = VReporteSubdiarioVentas.objects.filter(**filtros)


            cobros_factura = {}
            seguimientos_facturas = {}
            embarque=None

            for q in queryset:
                impuvtas = Impuvtas.objects.filter(autofac=q.autogen_factura).only('autogen', 'monto')

                if impuvtas.exists():
                    lista_cobros = []
                    for i in impuvtas:
                        movim = Movims.objects.filter(mautogen=i.autogen).only('mfechamov', 'mcambio',
                                                                               'mparidad').first()

                        cobro = {
                            'autogen': i.autogen,
                            'monto': i.monto,
                            'fecha': movim.mfechamov if movim else None,
                            'cambio': movim.mcambio if movim else None,
                            'paridad': movim.mparidad if movim else None,
                        }
                        lista_cobros.append(cobro)

                    cobros_factura[q.autogen_factura] = lista_cobros

                if q.posicion is not None and q.house is not None:
                    embarque = VistaOperativas.objects.filter(posicion=q.posicion, house=q.house).only(
                        'seguimiento').first()

                if embarque:
                    seguimientos_facturas[q.autogen_factura] = embarque.seguimiento

            for q in queryset:
                cobros = cobros_factura.get(q.autogen_factura, [])

                if cobros:
                    # Obtener el último cobro por fecha
                    ultimo_cobro = max(cobros, key=lambda c: c['fecha'])

                    # Sumar montos
                    suma_cobros = sum(c['monto'] for c in cobros)

                    # Determinar estado de cancelación
                    if suma_cobros == q.total:
                        q.cancelada = "SI"
                    elif suma_cobros > 0:
                        q.cancelada = "PARCIAL"

                    # Asignar datos del último cobro
                    if ultimo_cobro:
                        q.cobro = ultimo_cobro['fecha']
                        q.tipo_cambio_cobro = ultimo_cobro['cambio']
                    else:
                        q.cobro = None
                        q.tipo_cambio_cobro = None

                else:
                    q.cancelada = "NO"
                    q.cobro = None
                    q.tipo_cambio_cobro = None

            datos = []
            for q in queryset:
                seguimiento = seguimientos_facturas.get(q.autogen_factura, None)
                datos.append((
                    q.fecha, q.tipo, q.numero, q.nro_cliente, q.cliente, q.detalle, q.exento, q.gravado,
                    q.iva, q.total, q.tipo_cambio, q.paridad, q.referencia, q.cancelada,
                    q.posicion, q.cuenta, q.vendedor, q.vencimiento, q.cobro, q.tipo_cambio_cobro,
                    q.moneda, q.rut, q.vapor, q.viaje,seguimiento, q.master, q.house, q.embarcador,
                    q.consignatario, q.flete, q.etd, q.eta, q.imputada, q.orden_cliente,
                    q.agente, q.origen, q.destino, q.operacion, q.movimiento, q.deposito, q.wr,
                    q.transportista, q.serie, q.prefijo
                ))

            # Generar Excel
            return generar_excel_subdiario_ventas(datos, fecha_desde, fecha_hasta,consolidar_dolares)

    else:
        form = ReporteMovimientosForm(initial={'estado': 'todo'})

    return render(request, 'ventas_ca/subdiario_ventas.html', {'form': form})

def generar_excel_subdiario_ventas(datos, fecha_desde, fecha_hasta,consolidar_dolares):
    try:
        nombre_archivo = f'Subdiario_Ventas_{fecha_desde}_al_{fecha_hasta}.xlsx'
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Subdiario_ventas")

        # Encabezado superior
        title = f"Ventas entre el {fecha_desde} y el {fecha_hasta}"
        worksheet.merge_range('A1:AD1', title, workbook.add_format({'bold': True, 'align': 'left'}))

        # Encabezados de columnas (desde la fila 2, índice 1)
        encabezados = [
            'Fecha', 'Tipo', 'Boleta', 'Cliente', 'Nombre', 'Detalle del movimiento', 'Exento', 'Gravado', 'I.V.A.',
            'Total', 'T. Cambio', 'Paridad', 'Referencia', 'Cancel.', 'Posición', 'Cuenta',
            'Vendedor', 'Vto.', 'Cobro', 'Tca. Cob.', 'Moneda Original', 'R.U.T.', 'Vapor',
            'Viaje', 'Seguimiento', 'Master', 'House', 'Embarcador', 'Consignatario', 'Flete', 'ETD', 'ETA', 'Imputada',
            'Orden cliente', 'Agente', 'Origen', 'Destino',
            'Operación', 'Movimiento', 'Depósito', 'WR', 'Transportista'
        ]

        worksheet.set_column(0, 0, 8)  # Fecha
        worksheet.set_column(17, 18, 8)  # Vto. y Cobro
        worksheet.set_column(29, 30, 8)  # ETD, ETA, Imputada

        header_format = workbook.add_format({'bold': True, 'bg_color': '#d9d9d9', 'border': 1})
        normal_format = workbook.add_format({'border': 1})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        datos_convertidos = []
        for fila in datos:
            fila = list(fila)
            if consolidar_dolares:
                try:
                    if fila[20]=='DOLARES USA':
                        moneda_origen=2
                    else:
                        moneda_origen=1

                    moneda_destino = 2
                    arbitraje = Decimal(fila[10] or 1)
                    paridad = Decimal(fila[11] or 1)

                    if moneda_origen != moneda_destino:
                        # Índices a convertir
                        for idx in [6, 7, 8, 9]:  # exento, gravado, iva, total
                            monto = Decimal(fila[idx] or 0)
                            fila[idx] = convertir_monto(monto, moneda_origen, moneda_destino, arbitraje, paridad)

                except Exception as e:
                    print(f"Error al convertir moneda: {e}")
            datos_convertidos.append(fila)

        for col_num, header in enumerate(encabezados):
            worksheet.write(1, col_num, header, header_format)

        anchos = {i: len(encabezado) for i, encabezado in enumerate(encabezados)}

        columnas_fecha = [0, 17, 18, 29,30]

        row_num = 2
        for fila in datos_convertidos:
            col_excel = 0
            for col_num in range(len(encabezados)):
                if col_num == 2:  # Columna "Boleta"
                    serie = fila[-2]
                    prefijo = fila[-1]
                    numero = fila[2]
                    valor = f"{serie}{prefijo}-{numero}"
                else:
                    valor = fila[col_num]

                # Aplicar formato de fecha si corresponde
                if col_excel==31:
                    print(valor)
                if col_num in columnas_fecha and isinstance(valor, (datetime.date, datetime.datetime)):
                    worksheet.write(row_num, col_excel, valor, date_format)
                else:
                    worksheet.write(row_num, col_excel, valor, normal_format)

                # Autoajuste de ancho
                longitud = len(str(valor)) if valor is not None else 0
                if longitud > anchos[col_excel]:
                    anchos[col_excel] = longitud

                col_excel += 1
            row_num += 1

        # Ajustar ancho de columnas al contenido
        for col_num, ancho in anchos.items():
            worksheet.set_column(col_num, col_num, ancho + 2)  # +2 para márgenes

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
        return response

    except Exception as e:
        raise RuntimeError(f"Error al generar el Excel: {e}")

def convertir_monto(monto, origen, destino, arbitraje, paridad):
    """
    Convierte un monto desde 'origen' a 'destino' utilizando arbitraje y paridad.
    origen y destino son enteros representando códigos de moneda:
    1 = moneda nacional, 2 = dólar, otros = otras monedas (ej: euro)
    """

    try:
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