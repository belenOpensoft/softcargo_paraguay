import datetime
import io


import xlsxwriter
from django.http import HttpResponse
from django.shortcuts import render

from administracion_contabilidad.models import Impuvtas, Movims, Factudif, Asientos, Boleta
from consultas_administrativas.forms import ReporteMovimientosForm, UtilidadMensualPosicionForm
from expaerea.models import ExportEmbarqueaereo, ExportServiceaereo, ExportReservas, ExportCargaaerea
from expmarit.models import ExpmaritEmbarqueaereo, ExpmaritServiceaereo, ExpmaritReservas, ExpmaritCargaaerea, \
    ExpmaritEnvases
from expterrestre.models import ExpterraEmbarqueaereo, ExpterraServiceaereo, ExpterraReservas, ExpterraCargaaerea, \
    ExpterraEnvases
from impaerea.models import ImportEmbarqueaereo, ImportServiceaereo, ImportReservas, ImportCargaaerea
from impomarit.models import VistaOperativas, Embarqueaereo, Serviceaereo, Reservas, Cargaaerea, Envases
from django.utils import timezone
from impterrestre.models import ImpterraEmbarqueaereo, ImpterraServiceaereo, ImpterraReservas, ImpterraCargaaerea, \
    ImpterraEnvases
from collections import defaultdict
from mantenimientos.models import Clientes, Vendedores, Servicios
from django.utils import timezone

def utilidad_mensual_posicion(request):
    if request.method == 'POST':
        form = UtilidadMensualPosicionForm(request.POST)
        if form.is_valid():
            mes = form.cleaned_data['mes']
            anio = form.cleaned_data['anio']
            operativas = form.cleaned_data['operativa']
            moneda_nacional = form.cleaned_data['moneda_nacional']
            apertura_por_posicion = form.cleaned_data['apertura_por_posicion']

            # acumulador global
            data_final = {}

            # diccionarios de modelos
            modelos = {
                'imp_maritima': Embarqueaereo,
                'imp_aerea': ImportEmbarqueaereo,
                'imp_terrestre': ImpterraEmbarqueaereo,
                'exp_maritima': ExpmaritEmbarqueaereo,
                'exp_aerea': ExportEmbarqueaereo,
                'exp_terrestre': ExpterraEmbarqueaereo,
            }
            modelos_reserva = {
                'imp_maritima': Reservas,
                'imp_aerea': ImportReservas,
                'imp_terrestre': ImpterraReservas,
                'exp_maritima': ExpmaritReservas,
                'exp_aerea': ExportReservas,
                'exp_terrestre': ExpterraReservas,
            }
            modelos_carga = {
                'imp_maritima': Cargaaerea,
                'imp_aerea': ImportCargaaerea,
                'imp_terrestre': ImpterraCargaaerea,
                'exp_maritima': ExpmaritCargaaerea,
                'exp_aerea': ExportCargaaerea,
                'exp_terrestre': ExpterraCargaaerea,
            }
            modelos_envases = {
                'imp_maritima': Envases,
                'imp_terrestre': ImpterraEnvases,
                'exp_maritima': ExpmaritEnvases,
                'exp_terrestre': ExpterraEnvases,
            }

            for op in operativas:
                modelo = modelos.get(op)
                modelo_reserva = modelos_reserva.get(op)
                if not modelo or not modelo_reserva:
                    continue

                mes_str = str(mes).zfill(2)  # "05"
                anio_str = str(anio)  # "2025"

                pattern = rf"^[A-Z]{{2}}{mes_str}-\d+-{anio_str}$"

                embarques = modelo.objects.only('numero', 'vendedor', 'hawb').filter(posicion__regex=pattern)
                reservas = modelo_reserva.objects.filter(posicion__regex=pattern)

                emb_por_pos = defaultdict(list)
                for e in embarques:
                    emb_por_pos[e.posicion].append(e)

                data_consolidada = consolidar_por_posicion(
                    reservas,
                    emb_por_pos,
                    modelos_carga,
                    modelos_envases,
                    op,
                    apertura_por_posicion
                )

                # acumular en el dict global
                data_final.update(data_consolidada)

            # valores de ejemplo para arbitraje/paridad (ajustar según tu sistema)
            arbitraje = 42.0
            paridad = 0.92

            output = generar_excel_utilidad_mensual(
                data_final,
                mes,
                anio,
                expresar_en_moneda_nacional=moneda_nacional,
                arbitraje=arbitraje,
                paridad=paridad,
                apertura_por_posicion=apertura_por_posicion
            )

            response = HttpResponse(
                output,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = f'attachment; filename=\"utilidad_mensual_{anio}_{mes}.xlsx\"'
            return response

    else:
        form = UtilidadMensualPosicionForm(initial={
            'anio': timezone.now().year,
            'mes': timezone.now().month
        })

    return render(request, 'cargas_ca/utilidad_mensual_posicion.html', {'form': form})
def normalizar_numero(valor):
    """
    Convierte un valor a string sin '.0' si es un número entero,
    o lo deja como está si tiene letras.
    """
    if valor is None:
        return ""

    # Si viene como float (ej: 123.0)
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))

    # Si viene como int
    if isinstance(valor, int):
        return str(valor)

    # Si viene como string
    if isinstance(valor, str):
        try:
            num = float(valor)
            if num.is_integer():
                return str(int(num))
            return str(num)  # ejemplo: "123.45"
        except ValueError:
            return valor.strip()  # no es número, devolver como string limpio

    # fallback
    return str(valor)

def consolidar_por_posicion(reservas, embarques_por_pos, modelos_carga, modelos_envases, op,apertura):
    """
    Genera un único vector por cada posición con datos de reserva + sumatorias
    de embarques, gastos, cargas y envases.
    """
    resultado = {}

    # --- loop por cada reserva ---
    for res in reservas:
        pos = res.posicion
        lista_emb = embarques_por_pos.get(pos, [])

        # Vector base con datos de la reserva
        agente = Clientes.objects.only('empresa').filter(codigo=res.agente).first() if res.agente else None
        transportista = Clientes.objects.only('empresa').filter(codigo=res.transportista).first() if res.transportista else None
        cliente = Clientes.objects.only('empresa').filter(codigo=res.consignatario).first() if res.consignatario else None
        vector = {
            "posicion": pos,
            "preventas": 0,
            "ingresos": 0,
            "egresos": 0,
            "utilidad": 0,
            "porcentaje": 0,
            "pago_master": getattr(res, "pagoflete", ""),
            "agente": agente.empresa if agente else '',
            "origen": getattr(res, "origen", ""),
            "destino": getattr(res, "destino", ""),
            "transportista": transportista.empresa if cliente else '',
            "fecha": res.fechaingreso.strftime('%d/%m/%Y') if res.fechaingreso else '',
            "vapor": getattr(res, "vapor", ""),
            "viaje": getattr(res, "viaje", ""),
            "master": getattr(res, "awb", ""),
            "houses": '',
            "vendedores": '',
            "cliente": cliente.empresa if cliente else '',
            "peso": 0,
            "movimientos": '',
            "contenedores": '',
            "volumen": 0,
            "operativa": op,
            "facturas": [],
        }

        autogenerados = (
            Asientos.objects.filter(posicion=res.posicion)
            .values_list("autogenerado", flat=True)
            .distinct()
        )

        movimientos = Movims.objects.filter(mautogen__in=autogenerados,mtipo__in=(40,41))
        boletas = Boleta.objects.filter(autogenerado__in=autogenerados,tipo__in=(20,21,23,24))
        lista_movimientos = []
        if movimientos:
            for m in movimientos:
                nro_completo = ""
                if m.mserie and m.mprefijo and m.mboleta:
                    s = str(m.mserie)
                    p = str(m.mprefijo)

                    tz = len(s) - len(s.rstrip('0'))
                    lz = len(p) - len(p.lstrip('0'))

                    sep = '0' * max(0, 3 - (tz + lz))

                    nro_completo = f" {s}{sep}{p}-{normalizar_numero(m.mboleta)}"

                nombre = str(m.mnombremov if m.mnombremov else '') + nro_completo
                l={
                    'numero':nombre,
                    'ingreso':m.mmonto if m.mtipo == 41 else 0,
                    'egreso':m.mmonto if m.mtipo == 40 else 0,
                    'fecha':m.mfechamov.strftime('%d/%m/%Y') if m.mfechamov else '',
                    'cliente':m.mnombre if m.mnombre else '',
                    'concepto':'',
                }
                serv = Asientos.objects.only('nroserv').filter(autogenerado=m.mautogen)
                servicios_text=''
                for s in serv:
                    servicio = Servicios.objects.filter(codigo=s.nroserv).first()
                    if servicio:
                        servicios_text+=str(servicio.nombre)+';'

                l['concepto']=servicios_text

                lista_movimientos.append(l)
        if boletas:
            for m in boletas:
                nro_completo = ""
                if m.serie and m.prefijo and m.numero:
                    s = str(m.serie)
                    p = str(m.prefijo)

                    tz = len(s) - len(s.rstrip('0'))
                    lz = len(p) - len(p.lstrip('0'))

                    sep = '0' * max(0, 3 - (tz + lz))

                    nro_completo = f" {s}{sep}{p}-{normalizar_numero(m.numero)}"

                nombre = 'FACTURA' + nro_completo
                l={
                    'numero':nombre,
                    'ingreso':m.precio if m.tipo == 20 else 0,
                    'egreso':m.precio if m.tipo == 21 else 0,
                    'fecha':m.fecha.strftime('%d/%m/%Y') if m.fecha else '',
                    'cliente':m.cliente if m.cliente else '',
                    'concepto':m.concepto if m.concepto else '',
                }
                lista_movimientos.append(l)

        vector["facturas"] = lista_movimientos
        # ahora ingresos/egresos salen de las facturas
        vector["ingresos"] = sum(f["ingreso"] for f in lista_movimientos)
        vector["egresos"] = sum(f["egreso"] for f in lista_movimientos)

        houses = ''
        vendedores = ''
        # --- sumar datos de embarques asociados ---
        for emb in lista_emb:
            houses += str(emb.hawb) + ';'
            v=Vendedores.objects.only('nombre').filter(codigo=emb.vendedor).first() if emb.vendedor else None
            vendedores += str(v.nombre) + ';' if v else ''
            vector["vendedores"]=vendedores
            vector["houses"]=houses

            prev = Factudif.objects.filter(zrefer=emb.numero).only('zmonto')
            preventas=0
            if prev:
                preventas = sum(float(getattr(g, "zmonto", 0) or 0) for g in prev)

            # modelo de gastos asociado a esta operativa
            # gasto_model = modelos_gastos[op]
            # gastos = gasto_model.objects.only('precio','costo').filter(numero=emb.numero)
            #
            # ingresos = sum(float(getattr(g, "precio", 0) or 0) for g in gastos)
            # egresos = sum(float(getattr(g, "costo", 0) or 0) for g in gastos)
            # vector["ingresos"] += ingresos
            # vector["egresos"] += egresos

            # modelo de cargas asociado
            carga_model = modelos_carga[op]
            cargas = carga_model.objects.filter(numero=emb.numero)
            vector["peso"] += sum(float(getattr(c, "bruto", 0) or 0) for c in cargas)
            vector["volumen"] += sum(float(getattr(c, "cbm", 0) or 0) for c in cargas) if pos not in ['imp_aerea','exp_aerea'] else 0

            if op in ['imp_aerea','exp_aerea']:
                vol = 0
                for c in cargas:
                    medidas = c.medidas.split('*') if c.medidas else []
                    if len(medidas) > 2:
                        vol += medidas[0]*medidas[1]*medidas[2]
                vector["volumen"] += vol

            # modelo de envases asociado (solo para marítimos y terrestres en tu diccionario)
            envase_model = modelos_envases.get(op)
            if envase_model:
                envases = envase_model.objects.only('nrocontenedor','movimiento').filter(numero=emb.numero)
                contenedores_str = ";".join([str(e.nrocontenedor) for e in envases if e.nrocontenedor])
                movimientos_str = ";".join([str(e.movimiento) for e in envases if e.movimiento])

                vector["contenedores"] += contenedores_str + ";" if contenedores_str else ""
                vector["movimientos"] += movimientos_str + ";" if movimientos_str else ""

        # --- calculados ---
        vector["utilidad"] = vector["ingresos"] - vector["egresos"]
        vector["porcentaje"] = (vector["utilidad"] / vector["ingresos"] * 100) if vector["ingresos"] > 0 else 0


        resultado[pos] = vector

    return resultado


NOMBRES_OPERATIVAS = {
    "imp_maritima": "IMPORTACIÓN MARÍTIMA",
    "exp_maritima": "EXPORTACIÓN MARÍTIMA",
    "imp_aerea": "IMPORTACIÓN AÉREA",
    "exp_aerea": "EXPORTACIÓN AÉREA",
    "imp_terrestre": "IMPORTACIÓN TERRESTRE",
    "exp_terrestre": "EXPORTACIÓN TERRESTRE",
}

def generar_excel_utilidad_mensual(
    data_consolidada,
    mes,
    anio,
    expresar_en_moneda_nacional=False,
    arbitraje=None,
    paridad=None,
    apertura_por_posicion=False
):
    """
    Genera un Excel de utilidad mensual consolidado:
    - Separa bloques por operativa con subtítulo.
    - Agrega totales por operativa.
    - Agrega un total general al final.
    - Si apertura_por_posicion=True, muestra facturas/movimientos debajo de cada posición.
      Solo respeta columnas de ingresos/egresos; el resto se escribe corrido desde la col 6.
    """
    output = io.BytesIO()
    wb = xlsxwriter.Workbook(output, {"in_memory": True})
    ws = wb.add_worksheet("Reporte")

    # --- formatos ---
    fmt_title = wb.add_format({"bold": True, "align": "center", "font_size": 14})
    fmt_subtitle = wb.add_format({"bold": True, "align": "left", "font_size": 12, "bg_color": "#F2F2F2"})
    fmt_header = wb.add_format({"bold": True, "bg_color": "#D9D9D9", "border": 1})
    fmt_money = wb.add_format({"num_format": "#,##0.00", "border": 1})
    fmt_percent = wb.add_format({"num_format": "0.00%", "border": 1})
    fmt_text = wb.add_format({"border": 1})
    fmt_date = wb.add_format({"num_format": "yyyy-mm-dd", "border": 1})
    fmt_total_op = wb.add_format({"bold": True, "bg_color": "#92c2fd", "border": 1})
    fmt_total = wb.add_format({"bold": True, "bg_color": "#FFD966", "border": 1})

    # formato para facturas/movimientos
    fmt_factura = wb.add_format({"border": 1, "bg_color": "#F8CBAD"})
    fmt_factura_money = wb.add_format({"num_format": "#,##0.00", "border": 1, "bg_color": "#F8CBAD"})

    # --- título ---
    titulo = f"UTILIDAD MENSUAL - {anio}-{str(mes).zfill(2)}"
    ws.merge_range("A1:V1", titulo, fmt_title)

    # --- encabezados ---
    headers = [
        "Posición", "Preventas", "Ingresos", "Egresos", "Utilidad", "%",
        "Master", "Pago Master", "Agente", "Origen", "Destino",
        "Transportista", "Fecha Ingreso", "Vapor", "Viaje",
        "Houses", "Vendedores", "Cliente", "Peso",
        "Movimientos", "Contenedores", "Volumen", "Operativa"
    ]

    row = 3
    total_general = {"preventas": 0, "ingresos": 0, "egresos": 0, "utilidad": 0}

    for op, nombre_op in NOMBRES_OPERATIVAS.items():
        data_op = {k: v for k, v in data_consolidada.items() if v["operativa"] == op}
        if not data_op:
            continue

        # subtítulo
        ws.merge_range(row, 0, row, len(headers)-1, nombre_op, fmt_subtitle)
        row += 1

        # encabezados
        for col, h in enumerate(headers):
            ws.write(row, col, h, fmt_header)
        row += 1

        # acumuladores por operativa
        tot_preventas = tot_ingresos = tot_egresos = 0

        # filas de esa operativa
        for pos, v in sorted(data_op.items()):
            ingresos = v["ingresos"]
            egresos = v["egresos"]

            if expresar_en_moneda_nacional:
                ingresos = convertir_monto(ingresos, origen=2, destino=1, arbitraje=arbitraje, paridad=paridad)
                egresos = convertir_monto(egresos, origen=2, destino=1, arbitraje=arbitraje, paridad=paridad)

            utilidad = ingresos - egresos
            porcentaje = utilidad / ingresos if ingresos else 0

            fila = [
                v["posicion"], v["preventas"], ingresos, egresos, utilidad, porcentaje,
                v["master"], v["pago_master"], v["agente"], v["origen"], v["destino"],
                v["transportista"], v["fecha"], v["vapor"], v["viaje"],
                v["houses"], v["vendedores"], v["cliente"], v["peso"],
                v["movimientos"], v["contenedores"], v["volumen"], v["operativa"]
            ]

            for col, val in enumerate(fila):
                if col in [1, 2, 3, 4, 18, 21]:
                    ws.write_number(row, col, float(val) if val else 0, fmt_money)
                elif col == 5:
                    ws.write_number(row, col, float(val), fmt_percent)
                elif col == 12 and isinstance(val, datetime.datetime):
                    ws.write_datetime(row, col, val, fmt_date)
                else:
                    ws.write(row, col, val if val is not None else "", fmt_text)

            row += 1

            # si hay apertura y facturas/movimientos
            if apertura_por_posicion and v.get("facturas"):
                for f in v["facturas"]:
                    # ingresos/egresos en columnas originales
                    ws.write(row, 1, f["numero"], fmt_factura)
                    ws.write_number(row, 2, float(f["ingreso"]), fmt_factura_money)
                    ws.write_number(row, 3, float(f["egreso"]), fmt_factura_money)

                    # resto de datos de corrido desde col 6
                    extra_data = [f["fecha"], f["cliente"], f["concepto"]]
                    for idx, val in enumerate(extra_data):
                        ws.write(row, 4 + idx, val, fmt_factura)

                    row += 1

                # fila en blanco entre posiciones
                row += 1

            tot_preventas += v["preventas"]
            tot_ingresos += ingresos
            tot_egresos += egresos

        tot_utilidad = tot_ingresos - tot_egresos

        # fila de total por operativa
        ws.write(row, 0, f"TOTAL", fmt_total_op)
        ws.write_number(row, 1, tot_preventas, fmt_total_op)
        ws.write_number(row, 2, tot_ingresos, fmt_total_op)
        ws.write_number(row, 3, tot_egresos, fmt_total_op)
        ws.write_number(row, 4, tot_utilidad, fmt_total_op)
        row += 2

        # acumular en total general
        total_general["preventas"] += tot_preventas
        total_general["ingresos"] += tot_ingresos
        total_general["egresos"] += tot_egresos
        total_general["utilidad"] += tot_utilidad

    # --- total general ---
    ws.write(row, 0, "TOTAL GENERAL", fmt_total)
    ws.write_number(row, 1, total_general["preventas"], fmt_total)
    ws.write_number(row, 2, total_general["ingresos"], fmt_total)
    ws.write_number(row, 3, total_general["egresos"], fmt_total)
    ws.write_number(row, 4, total_general["utilidad"], fmt_total)

    # ajuste de anchos
    ws.set_column("A:A", 18)
    ws.set_column("B:E", 14)
    ws.set_column("F:F", 8)
    ws.set_column("G:H", 18)
    ws.set_column("I:K", 18)
    ws.set_column("L:L", 22)
    ws.set_column("M:M", 12)
    ws.set_column("N:O", 14)
    ws.set_column("P:R", 20)
    ws.set_column("S:U", 25)
    ws.set_column("V:V", 12)

    wb.close()
    output.seek(0)
    return output


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