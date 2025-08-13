from collections import defaultdict

from django.db.models import Sum
from django.shortcuts import render
from reportlab.pdfbase.pdfmetrics import stringWidth
from administracion_contabilidad.models import Asientos, Cuentas, Movims, Factudif, Dolar, Impuvtas, Impucompras
from consultas_administrativas.forms import LibroDiarioForm, FichaEmbarqueForm
from expaerea.models import ExportEmbarqueaereo, ExportConexaerea
from expmarit.models import ExpmaritEmbarqueaereo
from expterrestre.models import ExpterraEmbarqueaereo
from impaerea.models import ImportEmbarqueaereo, ImportConexaerea
from impomarit.models import Embarqueaereo
from impterrestre.models import ImpterraEmbarqueaereo
from mantenimientos.models import Clientes, Monedas, Ciudades, Servicios
import io
import xlsxwriter
from decimal import Decimal
from datetime import datetime
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import grey, black
from datetime import date

def ficha_embarque(request):
    resultados = []
    total_ingresos = Decimal('0')
    total_egresos = Decimal('0')
    rentabilidad = Decimal('0')
    error_msg = None
    datos = {
        'conocimiento': '', 'origen': '', 'destino': '', 'vapor': '',
        'viaje': '', 'embarcador': '', 'agente': '', 'status': '',
        'transportista': '', 'interno': '', 'detalle': ''
    }
    asientos = None
    movimientos = None
    puede_exportar = False
    preventas = None
    total_preventa = Decimal('0')
    detallar_preventas=False
    moneda_general= 2
    cobro = pago=autogen_cobro=autogen_pago= pago_cobro=None

    try:

        if request.method == 'POST' and request.POST.get('accion') == 'excel':
            cache = request.session.get("ficha_embarque_cache")
            if not cache:
                return HttpResponse("No hay datos para exportar.", status=400)

            resultados_cache = [{
                **r,
                "ingresos": Decimal(r["ingresos"]),
                "egresos": Decimal(r["egresos"]),
            } for r in cache["resultados"]]

            return generar_excel_ficha_embarque(
                resultados_cache,
                Decimal(cache["total_ingresos"]),
                Decimal(cache["total_egresos"]),
                Decimal(cache["total_preventa"]),
                Decimal(cache["detallar_preventas"]),
                Decimal(cache["rentabilidad"]),
                cache["moneda_general"]
            )

        if request.method == 'POST' and request.POST.get('accion') == 'imprimir':
            cache = request.session.get("ficha_embarque_cache")
            if not cache:
                return HttpResponse("No hay datos para imprimir.", status=400)

            # Datos de cabecera directamente desde la cache
            datos_pdf = cache.get("datos", {})
            # Filas ya listas para el PDF
            filas = cache.get("resultados", [])

            # Totales (a Decimal por seguridad)
            total_ingresos = Decimal(cache.get("total_ingresos", "0"))
            total_egresos = Decimal(cache.get("total_egresos", "0"))
            total_preventa = Decimal(cache.get("total_preventa", "0"))
            detallar_preventas = Decimal(cache.get("detallar_preventas", "0"))
            rentabilidad = Decimal(cache.get("rentabilidad", "0"))

            # Etiqueta de consolidación tal como la guardaste
            consolidado = cache.get("consolidacion", "USD")

            return generar_pdf_ficha_embarque(
                datos=datos_pdf,
                filas=filas,
                total_ingresos=total_ingresos,
                total_egresos=total_egresos,
                total_preventa=total_preventa,
                detallar_preventas=detallar_preventas,
                rentabilidad=rentabilidad,
                consolidado=consolidado
            )

        form = FichaEmbarqueForm(request.POST or None)

        if request.method == 'POST' and form.is_valid():
            operativa = form.cleaned_data['operativa']
            master = form.cleaned_data['master']
            house = form.cleaned_data['house']
            posicion = form.cleaned_data['posicion']
            seguimiento = form.cleaned_data['seguimiento']
            detallar_preventas = form.cleaned_data['detallar_preventas']
            expresar_moneda_nac = form.cleaned_data['expresar_moneda_nac']

            if expresar_moneda_nac:
                moneda_general=1

            embarque = None
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
                    if master: filtros['awb'] = master
                    if house: filtros['hawb'] = house
                    if seguimiento: filtros['seguimiento'] = seguimiento

                    embarque = modelo.objects.filter(**filtros).first()
                    asientos = Asientos.objects.filter(
                        posicion=embarque.posicion if embarque else posicion
                    ).values_list('autogenerado', flat=True)
                else:
                    error_msg = 'No se encontró el modelo'
            else:
                error_msg = 'Debe seleccionar la operativa'

            # Buscar por prefijo si no se encontró por operativa
            if posicion and not embarque and not error_msg:
                prefijos = {
                    'IM': Embarqueaereo, 'IA': ImportEmbarqueaereo, 'IT': ImpterraEmbarqueaereo,
                    'EM': ExpmaritEmbarqueaereo, 'EA': ExportEmbarqueaereo, 'ET': ExpterraEmbarqueaereo,
                }
                modelo = prefijos.get(posicion[:2])
                if not modelo:
                    error_msg = 'No se encontró el modelo'
                else:
                    embarque = modelo.objects.filter(posicion=posicion).first()
                    asientos = Asientos.objects.filter(posicion=posicion).values_list('autogenerado', flat=True)

            # Datos de cabecera
            if embarque and not error_msg:
                conex = None
                if operativa == 'importacion_aerea':
                    conex = ImportConexaerea.objects.filter(numero=embarque.numero).first()
                elif operativa == 'exportacion_aerea':
                    conex = ExportConexaerea.objects.filter(numero=embarque.numero).first()

                embarcador = Clientes.objects.filter(codigo=embarque.embarcador).first() if embarque.embarcador else None
                agente = Clientes.objects.filter(codigo=embarque.agente).first() if embarque.agente else None
                transportista = Clientes.objects.filter(codigo=embarque.transportista).first() if embarque.transportista else None

                origen = Ciudades.objects.filter(codigo=embarque.origen).first() if embarque.origen else None
                destino = Ciudades.objects.filter(codigo=embarque.destino).first() if embarque.destino else None

                if detallar_preventas:
                    preventas = Factudif.objects.filter(zseguimiento=embarque.seguimiento)
                    if preventas.exists():
                        total_preventa = preventas.aggregate(suma=Sum('zmonto'))['suma'] or Decimal('0')

                datos = {
                    'posicion': embarque.posicion,
                    'conocimiento': f"{embarque.awb or ''}{embarque.hawb or ''}",
                    'origen': (origen.nombre if origen else '') or '',
                    'destino': (destino.nombre if destino else '') or '',
                    'vapor': embarque.vapor if operativa not in ('importacion_aerea','exportacion_aerea') else (conex.ciavuelo if conex else 'S/I'),
                    'viaje': embarque.viaje if operativa not in ('importacion_aerea','exportacion_aerea') else (conex.viaje if conex else 'S/I'),
                    'embarcador': embarcador.empresa if embarcador else '',
                    'agente': agente.empresa if agente else '',
                    'status': embarque.status,
                    'transportista': transportista.empresa if transportista else '',
                    'interno': embarque.numero,
                    'seguimiento': embarque.seguimiento,
                    'detalle': ''
                }

            elif not error_msg:
                error_msg = 'No se encontró embarque'

            # Movimientos (asientos + cobranzas + pagos)
            if not error_msg and asientos:
                asientos_list = list(asientos)
                autogens_totales = list({*asientos_list})
                movimientos = Movims.objects.filter(mautogen__in=autogens_totales).order_by('mfechamov', 'mboleta')

            if not error_msg and (not movimientos or not movimientos.exists()):
                error_msg = 'No se encontraron movimientos'
                movimientos = []


            if movimientos:
                #obtener los servicios asociados a las facturas

                mautogens = [m.mautogen for m in movimientos]

                asientos_rows = (
                    Asientos.objects
                    .filter(autogenerado__in=mautogens)
                    .exclude(nroserv__isnull=True)
                    .values('autogenerado', 'nroserv')
                    .distinct()
                )

                nroserv_por_mautogen = defaultdict(set)
                codigos_servicios = set()

                for row in asientos_rows:
                    nro = str(row['nroserv'])  # cast a str para comparar homogéneo
                    nroserv_por_mautogen[row['autogenerado']].add(nro)
                    codigos_servicios.add(nro)

                servicios_map = dict(
                    (str(cod), nombre)
                    for cod, nombre in Servicios.objects
                    .filter(codigo__in=codigos_servicios)
                    .values_list('codigo', 'nombre')
                )

                # Filas
                for m in movimientos:
                    autogen_cobro = Impuvtas.objects.only('autogen').filter(autofac=m.mautogen).first()
                    autogen_pago = Impucompras.objects.only('autogen').filter(autofac=m.mautogen).first()

                    if autogen_cobro:
                        cobro = Movims.objects.only('mfechamov').filter(mautogen=autogen_cobro.autogen).first()

                    if autogen_pago:
                        pago = Movims.objects.only('mfechamov').filter(mautogen=autogen_pago.autogen).first()

                    if cobro:
                        pago_cobro = cobro.mfechamov.strftime('%d/%m/%Y') if cobro.mfechamov else None

                    if pago:
                        pago_cobro = pago.mfechamov.strftime('%d/%m/%Y') if cobro.mfechamov else None

                    #moneda = Monedas.objects.only('nombre').filter(codigo=m.mmoneda).first()
                    tipo = int(m.mtipo)

                    monto = m.mmonto if tipo not in (25, 45) else m.mtotal
                    monto = monto or Decimal('0')

                    if not form.cleaned_data['expresar_moneda_nac']:
                        if m.mmoneda !=2:
                            monto = convertir_monto(monto, m.mmoneda, 2, m.marbitraje, m.mparidad)
                    else:
                        if m.mmoneda !=1:
                            monto = convertir_monto(monto, m.mmoneda, 1, m.marbitraje, m.mparidad)

                    if tipo in (20, 41, 25, 23, 24):
                        ingresos, egresos = monto, Decimal('0')
                    elif tipo in (40, 21, 45):
                        ingresos, egresos = Decimal('0'), monto
                    else:
                        ingresos, egresos = Decimal('0'), Decimal('0')

                    codigos_de_este_mautogen = sorted(nroserv_por_mautogen.get(m.mautogen, []))
                    nombres_servicios = [
                        servicios_map.get(str(cod), str(cod))  # si no se encuentra, dejamos el código
                        for cod in codigos_de_este_mautogen
                    ]
                    detalle_servicios = ";".join(nombres_servicios)

                    caracter = '*' if m.msaldo == 0 else '+'
                    resultados.append({
                        'tipo': f"{m.mnombremov} ({caracter})" if m.mtipo not in [45,25] else f"{m.mnombremov}",
                        'tipo_numero': m.mtipo,
                        'numero': m.mboleta,
                        'fecha': m.mfechamov.strftime('%d/%m/%Y') if m.mfechamov else '',
                        'socio': m.mnombre,
                        'ingresos': ingresos,
                        'egresos': egresos,
                        'detalle': detalle_servicios,
                        'pago_cobro': pago_cobro,
                        'moneda': 'USD' if moneda_general == 2 else 'M/N',
                    })

                # Totales (excluyendo 25 y 45)
                excluir = {25, 45}
                total_ingresos = sum((r['ingresos'] for r in resultados if r['tipo_numero'] not in excluir), Decimal('0'))
                total_egresos  = sum((r['egresos']  for r in resultados if r['tipo_numero'] not in excluir), Decimal('0'))
                rentabilidad   = total_ingresos - total_egresos

                # 3) Guardar en sesión solo si hay datos válidos
                if not error_msg and resultados:
                    puede_exportar = True
                    consol_label = "CONSOLIDADO A USD" if not expresar_moneda_nac else "CONSOLIDADO A MONEDA NACIONAL"
                    cache = {
                        "resultados": [
                            {
                                "tipo": r["tipo"],
                                "tipo_numero": r["tipo_numero"],
                                "numero": r["numero"],
                                "fecha": r["fecha"],
                                "socio": r["socio"],
                                "ingresos": str(r["ingresos"]),
                                "egresos": str(r["egresos"]),
                                "detalle": r["detalle"],
                                "pago_cobro": r["pago_cobro"],
                                "moneda": r["moneda"],
                            } for r in resultados
                        ],
                        "total_ingresos": str(total_ingresos),
                        "total_egresos": str(total_egresos),
                        "total_preventa": str(total_preventa),
                        "detallar_preventas": detallar_preventas,
                        "moneda_general": moneda_general,
                        "rentabilidad": str(rentabilidad),
                        "datos": {
                            "posicion": datos.get("posicion") or "",
                            "conocimiento": datos.get("conocimiento") or "",
                            "origen": datos.get("origen") or "",
                            "destino": datos.get("destino") or "",
                            "transportista": datos.get("transportista") or "",
                            "agente": datos.get("agente") or "",
                            "status": datos.get("status") or "",
                            "vapor": datos.get("vapor") or "",
                            "viaje": datos.get("viaje") or "",
                        },
                        "consolidacion": consol_label,
                    }
                    request.session["ficha_embarque_cache"] = cache
                    request.session.modified = True
                else:
                    # búsqueda sin resultados o con error
                    puede_exportar = False
                    request.session.pop("ficha_embarque_cache", None)

        return render(request, 'cargas_ca/ficha_embarque.html', {
            'form': form,
            'resultados': resultados,
            'total_ingresos': total_ingresos,
            'total_egresos': total_egresos,
            'rentabilidad': rentabilidad,
            'error_msg': error_msg,
            'puede_exportar': puede_exportar,
            'total_preventa': str(total_preventa),
            'detallar_preventas': detallar_preventas,
            "moneda_general": moneda_general,
            **datos,
        })
    except Exception as e:
        raise TypeError('Error', str(e))

def generar_excel_ficha_embarque(resultados, total_ingresos, total_egresos,total_preventa,detallar_preventas, rentabilidad,moneda_general):

    nombre_archivo = f'Ficha_Embarque_{date.today().isoformat()}.xlsx'
    output = io.BytesIO()
    wb = xlsxwriter.Workbook(output, {'in_memory': True})
    ws = wb.add_worksheet("Ficha")

    # Estilos
    head = wb.add_format({'bold': True, 'bg_color': '#d9d9d9', 'border': 1, 'align': 'center'})
    cell = wb.add_format({'border': 1})
    cell_right = wb.add_format({'border': 1, 'align': 'right'})
    numfmt = wb.add_format({'border': 1, 'num_format': '#,##0.00', 'align': 'right'})
    total_fmt = wb.add_format({'border': 1, 'bold': True, 'num_format': '#,##0.00', 'align': 'right'})
    total_lbl = wb.add_format({'border': 1, 'bold': True})
    datefmt = wb.add_format({'border': 1, 'num_format': 'dd/mm/yyyy'})

    # Encabezados (como en la tabla)
    headers = ['Tipo', 'Número', 'Fecha', 'Socio Comercial', 'Ingresos', 'Egresos','Cobro/Pago', 'Detalle', 'Moneda']
    for c, h in enumerate(headers):
        ws.write(0, c, h, head)

    # Filas
    row = 1
    for r in resultados:
        # Sanear tipos y convertir Decimals a float para Excel
        tipo = r.get('tipo') or ''
        numero = r.get('numero') or ''
        fecha_str = r.get('fecha') or ''  # ya viene como string dd/mm/yyyy en tu tabla
        socio = r.get('socio') or ''
        ingresos = r.get('ingresos') or Decimal('0')
        egresos = r.get('egresos') or Decimal('0')
        pago_cobro = r.get('pago_cobro') or ''
        detalle = r.get('detalle') or ''
        moneda = 'USD' if moneda_general == 2 else 'M/N'

        # Escribir celdas
        ws.write(row, 0, tipo, cell)
        ws.write(row, 1, numero, cell)

        try:
            if fecha_str:
                d, m, y = fecha_str.split('/')
                ws.write_datetime(row, 2, datetime(int(y), int(m), int(d)), datefmt)
            else:
                ws.write(row, 2, '', cell)
        except Exception:
            ws.write(row, 2, fecha_str, cell)  # si no parsea, va como texto

        ws.write(row, 3, socio, cell)
        # E: Ingresos (vacío si 0)
        if ingresos != Decimal('0'):
            ws.write_number(row, 4, float(ingresos), numfmt)
        else:
            ws.write(row, 4, None, cell_right)  # celda vacía

        # F: Egresos (vacío si 0)
        if egresos != Decimal('0'):
            ws.write_number(row, 5, float(egresos), numfmt)
        else:
            ws.write(row, 5, None, cell_right)  # celda vacía

        ws.write(row, 6, pago_cobro, cell)
        ws.write(row, 7, detalle, cell)
        ws.write(row, 8, moneda, cell)
        row += 1

    # Totales
    ws.write(row, 3, "Totales:", total_lbl)
    ws.write_number(row, 4, float(total_ingresos or 0), total_fmt)
    ws.write_number(row, 5, float(total_egresos or 0), total_fmt)
    ws.write(row, 6, "Rentabilidad:", total_lbl)
    ws.write_number(row, 7, float((rentabilidad or 0)), total_fmt)

    # Fila "Total Preventa" si cache detallar_preventa=True
    if detallar_preventas:
        # Etiqueta y valor (misma alineación que Totales)
        ws.write(row, 3, "Total Preventa:", total_lbl)
        ws.write_number(row, 4, float(total_preventa or 0), total_fmt)
        row += 1

    # Anchos de columnas
    ws.set_column('A:A', 16)  # Tipo
    ws.set_column('B:B', 14)  # Número
    ws.set_column('C:C', 12)  # Fecha
    ws.set_column('D:D', 30)  # Socio Comercial
    ws.set_column('E:F', 16)  # Ingresos / Egresos
    ws.set_column('G:G', 12)  # Cobro/Pago (fecha)
    ws.set_column('H:H', 40)  # Detalle
    ws.set_column('I:I', 16)  # Moneda

    wb.close()
    output.seek(0)
    return HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
    )

def convertir_monto(monto, origen, destino, arbitraje, paridad):
    from decimal import Decimal, ROUND_HALF_UP

    try:
        monto = Decimal(monto)
        if arbitraje is not None:
            arbitraje = Decimal(arbitraje)
        if paridad is not None:
            paridad = Decimal(paridad)

        if arbitraje is None:
            dolar = Dolar.objects.filter(ufecha__date=datetime.date.today()).first()
            if dolar:
                arbitraje = Decimal(dolar.uvalor)

        if origen == destino or monto == 0:
            return monto.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if destino == 1:  # moneda nacional
            if origen == 2 and arbitraje:
                return (monto * arbitraje).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            elif origen not in [1, 2] and arbitraje and paridad:
                dolares = monto / paridad
                return (dolares * arbitraje).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        elif destino == 2:  # dólares
            if origen == 1 and arbitraje:
                return (monto / arbitraje).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            elif origen not in [1, 2] and paridad:
                return (monto / paridad).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        else:  # otra moneda
            if origen == 1 and arbitraje and paridad:
                dolares = monto / arbitraje
                return (dolares * paridad).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            elif origen == 2 and paridad:
                return (monto * paridad).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            elif origen == destino:
                return monto.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return monto.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except Exception as e:
        return Decimal('0.00')

def _fmt_money(val):
    if val is None or val == "":
        return "0.00"
    if isinstance(val, str):
        try:
            val = Decimal(val)
        except:
            return val
    return f"{val:,.2f}"

def _truncate_to_width(text, font_name, font_size, max_width):
    """Corta el texto para que quepa en max_width (no agrega '…' para evitar pisar columnas)."""
    if not text:
        return ""
    w = stringWidth(text, font_name, font_size)
    if w <= max_width:
        return text
    # Búsqueda lineal hacia abajo (rápida y suficiente)
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi) // 2
        if stringWidth(text[:mid], font_name, font_size) <= max_width:
            lo = mid + 1
        else:
            hi = mid
    # lo-1 es el último que entra
    return text[:max(0, lo-1)]

def generar_pdf_ficha_embarque(datos, filas, total_ingresos, total_egresos,total_preventa,detallar_preventas, rentabilidad, consolidado="USD"):
    """
    datos: dict -> {'posicion','conocimiento','origen','destino','transportista','agente','status','vapor','viaje'}
    filas: list[dict] -> {'tipo','numero','fecha','socio','ingresos','egresos','detalle','moneda','tc'(opcional)}
    """
    # Normalizamos datos para evitar None
    safe = lambda v: "" if v is None else str(v)
    d = {k: safe(datos.get(k, "")) for k in [
        "posicion","conocimiento","origen","destino","transportista",
        "agente","status","vapor","viaje"
    ]}

    response = HttpResponse(content_type='application/pdf')
    nombre = f"ficha_embarque_{d.get('posicion','')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{nombre}"; filename*=UTF-8\'\'{nombre}'

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Márgenes
    left   = 15 * mm
    right  = width - 15 * mm
    top    = height - 15 * mm
    bottom = 15 * mm

    # Config fuente
    body_font = "Helvetica"
    body_size = 9
    bold_font = "Helvetica-Bold"
    small_font = 8

    # Diseño columnas (imitando tu PDF de referencia)
    # Tipo | Documento | Fecha | Socio | Ingresos | Egresos | Detalle | M. y T.C.
    x_tipo      = left
    x_doc       = left + 22 * mm
    x_fecha     = left + 40 * mm
    x_socio     = left + 60 * mm
    x_ing       = left + 90 * mm  # números a la derecha
    x_egr       = left + 110 * mm  # números a la derecha
    x_detalle   = left + 140 * mm  # inicio para detalle (ajustado para no pisar importes)
    socio_max_width = (x_ing - 1 * mm) - x_socio + 15
    detalle_max_width = (right - 2 * mm) - x_detalle

    row_height = 5.5 * mm
    min_y_for_totals = bottom + 30 * mm

    def draw_header(page_num):
        y = top
        # Línea de arriba con fecha y página
        c.setFont(body_font, small_font)
        c.setFillColor(black)
        c.drawRightString(right, y, f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}    Pág.: {page_num:02d}")

        # Título
        y -= 8 * mm
        c.setFont(bold_font, 11)
        pos = d.get('posicion') or "S/I"
        c.drawString(left, y, f"ANÁLISIS EXTENDIDO DE LA POSICIÓN {pos} - {consolidado}")

        # Nota (según estado de facturas: excluye cobros 25 y pagos 45)
        y -= 5 * mm
        c.setFont(body_font, body_size)

        # Nos quedamos con filas que NO sean cobros ni pagos
        tipos_excluir = {"25", "45"}  # usar strings por seguridad
        facturas = [r for r in filas if str(r.get("tipo_numero") or "").strip() not in tipos_excluir]

        # Marcadas con "(* )" en el texto de tipo => canceladas
        marcadas_canceladas = [("(*)" in (r.get("tipo") or "")) for r in facturas]

        if facturas and all(marcadas_canceladas):
            mensaje_cancelacion = "(*) Documento ya cancelado"
        elif facturas and any(marcadas_canceladas):
            mensaje_cancelacion = "(+) Documento parcialmente cancelado"
        else:
            mensaje_cancelacion = ""  # ninguna cancelada -> no mostramos nada

        if mensaje_cancelacion:
            c.drawString(left, y, mensaje_cancelacion)

        c.line(left, y - 2*mm, right, y - 2*mm)

        # Datos del embarque
        y -= 8 * mm
        c.setFont(body_font, body_size)
        c.drawString(left, y, f"Conocimiento    : {d['conocimiento']}")
        y -= 5 * mm
        c.drawString(left, y, f"Origen/Destino  : {d['origen']}/{d['destino']}")
        y -= 5 * mm
        c.drawString(left, y, f"Transportista   : {d['transportista']}")
        y -= 5 * mm
        c.drawString(left, y, f"Agente          : {d['agente']}")
        y -= 5 * mm
        c.drawString(left, y, f"Status          : {d['status']}")
        y -= 5 * mm
        c.drawString(left, y, f"Vapor           : {d['vapor']}")
        y -= 5 * mm
        c.drawString(left, y, f"Viaje           : {d['viaje']}")

        # Encabezado de tabla
        y -= 7 * mm
        c.line(left, y, right, y)
        y -= 5 * mm
        c.setFont(bold_font, body_size)
        c.drawString(x_tipo,  y, "Tipo")
        c.drawString(x_doc,   y, "Documento")
        c.drawString(x_fecha, y, "Fecha")
        c.drawString(x_socio, y, "Socio comercial")
        c.drawRightString(x_ing + 25*mm, y, "Ingresos")
        c.drawRightString(x_egr + 25*mm, y, "Egresos")
        c.drawString(x_detalle, y, "Detalle")
        c.setFont(body_font, body_size)
        c.line(left, y - 2*mm, right, y - 2*mm)
        return y - 6 * mm

    page = 1
    y = draw_header(page)

    # Cuerpo
    for r in filas:
        if y < min_y_for_totals:
            c.showPage()
            page += 1
            y = draw_header(page)

        tipo = (r.get("tipo") or "").strip()
        doc  = (r.get("numero") or "").strip()
        fec  = (r.get("fecha") or "").strip()
        socio = (r.get("socio") or "").strip()
        ing  = _fmt_money(r.get("ingresos"))
        egr  = _fmt_money(r.get("egresos"))
        det  = (r.get("detalle") or "").strip()

        # Truncados por ancho
        socio_txt = _truncate_to_width(socio, body_font, body_size, socio_max_width)
        # Wrap para detalle
        lineas_detalle = _wrap_text(det, body_font, body_size, detalle_max_width)

        # Si no hay espacio suficiente para TODAS las líneas del detalle en esta página, saltamos
        necesario = row_height * max(1, len(lineas_detalle))
        if y - necesario < min_y_for_totals:
            c.showPage()
            page += 1
            y = draw_header(page)

        # Primera línea: se dibujan todas las columnas
        c.setFont(body_font, body_size)
        c.drawString(x_tipo, y, tipo)
        c.drawString(x_doc, y, doc)
        c.drawString(x_fecha, y, fec)
        c.drawString(x_socio, y, socio_txt)
        if ing != "0.00":
            c.drawRightString(x_ing + 25 * mm, y, ing)
        if egr != "0.00":
            c.drawRightString(x_egr + 25 * mm, y, egr)
        c.drawString(x_detalle, y, lineas_detalle[0])
        y -= row_height

        # Líneas extra: sólo en la columna Detalle
        for linea in lineas_detalle[1:]:
            # Si te podés quedar corto de espacio a mitad del detalle, controlá salto aquí también:
            if y - row_height < min_y_for_totals:
                c.showPage()
                page += 1
                y = draw_header(page)
            c.drawString(x_detalle, y, linea)
            y -= row_height

    # Totales
    if y < bottom + 20 * mm:
        c.showPage()
        page += 1
        y = draw_header(page)

    y -= 4 * mm
    c.line(left, y, right, y)
    y -= 7 * mm

    c.setFont(bold_font, 10)
    c.drawString(left, y, "TOTAL")
    c.drawRightString(x_ing + 25*mm, y, _fmt_money(total_ingresos))
    c.drawRightString(x_egr + 25*mm, y, _fmt_money(total_egresos))

    # === NUEVO: Total Preventa opcional ===
    if detallar_preventas:
        if y < bottom + 10 * mm:
            c.showPage()
            page += 1
            y = draw_header(page)
        c.setFont(bold_font, 10)
        c.drawString(left, y, "TOTAL PREVENTA")
        c.drawRightString(x_ing + 25 * mm, y, _fmt_money(total_preventa or Decimal('0')))
        y -= 10 * mm
    # === FIN NUEVO ===

    y -= 10 * mm
    c.setFont(bold_font, 10)
    c.drawString(left, y, "RENTABILIDAD FISCAL")
    c.drawRightString(x_egr + 25*mm, y, _fmt_money(rentabilidad))

    c.showPage()
    c.save()
    return response


def _wrap_text(texto, font_name, font_size, max_width):
    """Devuelve lista de líneas que entran en max_width."""
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    for palabra in palabras:
        test_linea = palabra if not linea_actual else linea_actual + " " + palabra
        if stringWidth(test_linea, font_name, font_size) <= max_width:
            linea_actual = test_linea
        else:
            if linea_actual:
                lineas.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        lineas.append(linea_actual)
    return lineas