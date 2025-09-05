# consultas_administrativas/views.py
import json
from django.db.models import Q, Value as V
from django.db.models.functions import Concat
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.timezone import make_aware
from datetime import datetime, time, timedelta
from django.apps import apps
from auditlog.models import LogEntry

from administracion_contabilidad.forms import AuditLogFilterForm
import io
import xlsxwriter

# Página con filtros + tabla
def audit_logs_page(request):
    form = AuditLogFilterForm(request.GET or None)
    return render(request, "logs.html", {"form": form})

# consultas_administrativas/views.py



def audit_logs_data_old(request):
    """
    Endpoint server-side para DataTables.
    Agrupa logs por mautogen de Movims. La fila principal es el Movim,
    y debajo se despliegan TODOS los modelos que compartan ese autogenerado.
    La columna 'Factura' siempre muestra el nro de factura armado desde Movims,
    excepto factudif que muestra 'SEG <seguimiento>'.
    """
    # Parámetros DataTables
    draw   = int(request.GET.get("draw", 1))
    start  = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 25))
    search_value = request.GET.get("search[value]", "").strip()

    # Filtros
    date_from = request.GET.get("date_from") or None
    date_to   = request.GET.get("date_to") or None
    user_id   = request.GET.get("user") or None

    # Query base
    base_qs = (
        LogEntry.objects
        .select_related("content_type", "actor")
        .filter(content_type__app_label="administracion_contabilidad")
    ).order_by("-timestamp")

    # Filtro fechas
    if date_from:
        try:
            dt_from = make_aware(datetime.combine(datetime.fromisoformat(date_from).date(), time.min))
            base_qs = base_qs.filter(timestamp__gte=dt_from)
        except Exception:
            pass
    if date_to:
        try:
            dt_to = make_aware(datetime.combine(datetime.fromisoformat(date_to).date(), time.max))
            base_qs = base_qs.filter(timestamp__lte=dt_to)
        except Exception:
            pass

    # Filtro usuario
    if user_id:
        base_qs = base_qs.filter(actor_id=user_id)

    # Búsqueda global
    if search_value:
        base_qs = base_qs.filter(
            Q(content_type__app_label__icontains=search_value) |
            Q(content_type__model__icontains=search_value) |
            Q(actor__username__icontains=search_value) |
            Q(actor__email__icontains=search_value) |
            Q(changes__icontains=search_value)
        )

    records_total = LogEntry.objects.filter(content_type__app_label="administracion_contabilidad").count()
    records_filtered = base_qs.count()

    # Paginación
    page_qs = base_qs[start:start + length]

    # Agrupación
    groups = {}
    Movims = apps.get_model("administracion_contabilidad", "Movims")
    Factudif = apps.get_model("administracion_contabilidad", "Factudif")

    def format_movim_number(movim):
        """
        Formatea el nro de factura a partir del Movims.
        """
        nro_completo = ""
        if movim.mserie and movim.mprefijo and movim.mboleta:
            s = str(movim.mserie)
            p = str(movim.mprefijo)
            n = str(movim.mboleta)

            tz = len(s) - len(s.rstrip('0'))  # ceros al final de serie
            lz = len(p) - len(p.lstrip('0'))  # ceros al inicio de prefijo
            sep = '0' * max(0, 3 - (tz + lz))

            tipo_txt = (str(movim.mnombremov).strip() + " ") if movim.mtipo else ""
            nro_completo = f"{tipo_txt}{s}{sep}{p}-{n}"
        return nro_completo or "--"

    for e in page_qs:
        model = e.content_type.model_class()
        if not model:
            continue

        obj = model.objects.filter(pk=e.object_pk).first()
        if not obj:
            continue

        table = model._meta.db_table.lower()
        factura_txt = "--"
        tabla_txt = table
        mautogen = None

        if table == "dataset_movims":
            mautogen = getattr(obj, "mautogen", None)
            factura_txt = format_movim_number(obj)

        elif table == "dataset_factudif":
            factura_txt = f"SEG {getattr(obj, 'zseguimiento', '--')} - {getattr(obj, 'zposicion', '--')}"
            tabla_txt = f"preventa-{getattr(obj, 'znumero', '--')}"
            mautogen = f"factudif-{obj.pk}"

        else:
            # Buscar Movims asociado por autogenerado
            autogen = getattr(obj, "autogenerado", None) or getattr(obj, "mautogen", None) or getattr(obj, "mautofac", None)
            if autogen:
                movim = Movims.objects.filter(mautogen=autogen).first()
                if movim:
                    mautogen = movim.mautogen
                    factura_txt = format_movim_number(movim)

        if not mautogen:
            mautogen = f"extra-{e.id}"

        # Inicializar grupo
        if mautogen not in groups:
            groups[mautogen] = {
                "mautogen": factura_txt,
                "tabla": tabla_txt if table in ["dataset_movims", "dataset_factudif"] else "--",
                "fecha": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "usuario": (
                    e.actor.get_username() if e.actor and hasattr(e.actor, "get_username")
                    else (e.actor.email if e.actor and getattr(e.actor, "email", None) else None)
                ) or "—",
                "detalles": []
            }

        # Agregar como detalle si no es movims ni factudif
        if table not in ["dataset_movims", "dataset_factudif"]:
            groups[mautogen]["detalles"].append({
                "tabla": table,
                "fecha": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "usuario": (
                    e.actor.get_username() if e.actor and hasattr(e.actor, "get_username")
                    else (e.actor.email if e.actor and getattr(e.actor, "email", None) else None)
                ) or "—",
                "cambios": e.changes or "--"
            })

    response = {
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": list(groups.values()),
    }
    return JsonResponse(response)



def audit_logs_data(request):
    """
    Endpoint server-side para DataTables.
    - Movims: fila principal con nro de factura (armado desde Movims) y detalles de relacionados.
    - Factudif: fila principal independiente ("SEG <seguimiento> - <posicion>") y detalle con cambios.
    - Otros modelos con autogenerado apuntando a Movims: van como detalles del grupo Movims.
    - Otros sin relación: fila normal independiente; si es dataset_asientos, 'Factura' = asiento.detalle.
      En ambos casos, muestran un detalle con sus cambios.
    """
    # Parámetros DataTables
    draw   = int(request.GET.get("draw", 1))
    start  = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 100))
    search_value = request.GET.get("search[value]", "").strip()

    # Filtros
    date_from = request.GET.get("date_from") or None
    date_to   = request.GET.get("date_to") or None


    user_id   = request.GET.get("user") or None

    # Query base (solo app administracion_contabilidad)
    base_qs = (
        LogEntry.objects
        .select_related("content_type", "actor")
        .filter(content_type__app_label="administracion_contabilidad")
        .order_by("-timestamp")
    )

    # Filtro fechas
    if date_from:
        try:
            df = datetime.strptime(date_from, "%Y-%m-%d").date()
            base_qs = base_qs.filter(timestamp__date__gte=df)
        except Exception:
            pass

    if date_to:
        try:
            dt = datetime.strptime(date_to, "%Y-%m-%d").date()
            base_qs = base_qs.filter(timestamp__date__lte=dt)
        except Exception:
            pass

    # Filtro usuario
    if user_id:
        base_qs = base_qs.filter(actor_id=user_id)

    # Búsqueda global
    if search_value:
        base_qs = base_qs.filter(
            Q(content_type__app_label__icontains=search_value) |
            Q(content_type__model__icontains=search_value) |
            Q(actor__username__icontains=search_value) |
            Q(actor__email__icontains=search_value) |
            Q(changes__icontains=search_value)
        )

    records_total = LogEntry.objects.filter(content_type__app_label="administracion_contabilidad").count()
    records_filtered = base_qs.count()

    # Paginación
    page_qs = base_qs[start:start + length]

    # Modelos y helpers
    Movims    = apps.get_model("administracion_contabilidad", "Movims")
    Factudif  = apps.get_model("administracion_contabilidad", "Factudif")
    Asientos  = apps.get_model("administracion_contabilidad", "Asientos")

    def format_movim_number(movim):
        """Formatea el nro de factura a partir de Movims."""
        nro_completo = ""
        if getattr(movim, "mserie", None) and getattr(movim, "mprefijo", None) and getattr(movim, "mboleta", None):
            s = str(movim.mserie)
            p = str(movim.mprefijo)
            n = str(movim.mboleta)
            tz = len(s) - len(s.rstrip('0'))  # ceros al final de serie
            lz = len(p) - len(p.lstrip('0'))  # ceros al inicio de prefijo
            sep = '0' * max(0, 3 - (tz + lz))
            tipo_txt = (str(getattr(movim, "mnombremov", "")).strip() + " ") if getattr(movim, "mtipo", None) else ""
            nro_completo = f"{tipo_txt}{s}{sep}{p}-{n}"
        return nro_completo or "--"

    groups = {}  # grupos por mautogen (solo Movims)
    rows   = []  # filas independientes (Factudif y sueltos)

    for e in page_qs:
        model = e.content_type.model_class()
        if not model:
            continue

        obj = model.objects.filter(pk=e.object_pk).first()
        if not obj:
            continue

        table = model._meta.db_table.lower()
        tabla_txt   = table
        factura_txt = "--"
        mautogen    = None

        # 1) MOVIMS → agrupador
        if table == "dataset_movims":
            mautogen = getattr(obj, "mautogen", None)
            factura_txt = format_movim_number(obj)
            if mautogen not in groups:
                groups[mautogen] = {
                    "mautogen": factura_txt,
                    "tabla": "movims",
                    "fecha": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "usuario": (
                        e.actor.get_username() if e.actor and hasattr(e.actor, "get_username")
                        else (e.actor.email if e.actor and getattr(e.actor, "email", None) else None)
                    ) or "—",
                    "detalles": []
                }

        # 2) FACTUDIF → fila independiente + detalle con cambios
        elif table == "dataset_factudif":
            factura_txt = f"SEG {getattr(obj, 'zseguimiento', '--')} - {getattr(obj, 'zposicion', '--')}"
            tabla_txt = f"preventa-{getattr(obj, 'znumero', '--')}"
            rows.append({
                "mautogen": factura_txt,
                "tabla": tabla_txt,
                "fecha": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "usuario": (
                    e.actor.get_username() if e.actor and hasattr(e.actor, "get_username")
                    else (e.actor.email if e.actor and getattr(e.actor, "email", None) else None)
                ) or "—",
                "detalles": [{
                    "tabla": table,
                    "fecha": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "usuario": (
                        e.actor.get_username() if e.actor and hasattr(e.actor, "get_username")
                        else (e.actor.email if e.actor and getattr(e.actor, "email", None) else None)
                    ) or "—",
                    "cambios": e.changes or "--"
                }]
            })

        # 3) OTROS MODELOS
        else:
            # ¿Se relaciona a un Movims por autogenerado?
            autogen = (
                getattr(obj, "autogenerado", None)
                or getattr(obj, "mautogen", None)
                or getattr(obj, "mautofac", None)
            )
            if autogen:
                movim = Movims.objects.filter(mautogen=autogen).first()
                if movim:
                    # Va como detalle del grupo Movims
                    mautogen = movim.mautogen
                    factura_txt = format_movim_number(movim)
                    if mautogen not in groups:
                        groups[mautogen] = {
                            "mautogen": factura_txt,
                            "tabla": "movims",
                            "fecha": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                            "usuario": (
                                e.actor.get_username() if e.actor and hasattr(e.actor, "get_username")
                                else (e.actor.email if e.actor and getattr(e.actor, "email", None) else None)
                            ) or "—",
                            "detalles": []
                        }
                    groups[mautogen]["detalles"].append({
                        "tabla": table,
                        "fecha": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "usuario": (
                            e.actor.get_username() if e.actor and hasattr(e.actor, "get_username")
                            else (e.actor.email if e.actor and getattr(e.actor, "email", None) else None)
                        ) or "—",
                        "cambios": e.changes or "--"
                    })
                else:
                    # No hay Movim → fila independiente (y mostrar cambios en detalle)
                    if table == "dataset_asientos":
                        factura_txt = getattr(obj, "detalle", None) or "--"
                    rows.append({
                        "mautogen": factura_txt,  # "--" o asiento.detalle
                        "tabla": table,
                        "fecha": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "usuario": (
                            e.actor.get_username() if e.actor and hasattr(e.actor, "get_username")
                            else (e.actor.email if e.actor and getattr(e.actor, "email", None) else None)
                        ) or "—",
                        "detalles": [{
                            "tabla": table,
                            "fecha": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                            "usuario": (
                                e.actor.get_username() if e.actor and hasattr(e.actor, "get_username")
                                else (e.actor.email if e.actor and getattr(e.actor, "email", None) else None)
                            ) or "—",
                            "cambios": e.changes or "--"
                        }]
                    })
            else:
                # Sin autogenerado → fila independiente (y mostrar cambios en detalle)
                if table == "dataset_asientos":
                    factura_txt = getattr(obj, "detalle", None) or "--"
                rows.append({
                    "mautogen": factura_txt,  # "--" o asiento.detalle
                    "tabla": table,
                    "fecha": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "usuario": (
                        e.actor.get_username() if e.actor and hasattr(e.actor, "get_username")
                        else (e.actor.email if e.actor and getattr(e.actor, "email", None) else None)
                    ) or "—",
                    "detalles": [{
                        "tabla": table,
                        "fecha": e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "usuario": (
                            e.actor.get_username() if e.actor and hasattr(e.actor, "get_username")
                            else (e.actor.email if e.actor and getattr(e.actor, "email", None) else None)
                        ) or "—",
                        "cambios": e.changes or "--"
                    }]
                })

    # Combinar: grupos (con detalles) + filas independientes
    data = list(groups.values()) + rows

    response = {
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data,
    }
    return JsonResponse(response)
import io
from datetime import datetime, time, timedelta
from django.http import HttpResponse
from django.apps import apps
from django.db.models import Q
import xlsxwriter
from auditlog.models import LogEntry


def export_logs_administracion(request):
    date_from = request.GET.get("date_from") or None
    date_to   = request.GET.get("date_to") or None
    user_id   = request.GET.get("user") or None

    qs = (
        LogEntry.objects
        .select_related("content_type", "actor")
        .filter(content_type__app_label="administracion_contabilidad")
    )

    # --- Filtro de fechas (naive, sin tz, MySQL friendly) ---
    def _to_date(s: str):
        try:
            return datetime.strptime(s.strip(), "%Y-%m-%d").date()
        except Exception:
            return None

    df = _to_date(date_from) if date_from else None
    dt = _to_date(date_to)   if date_to   else None

    if df and dt:
        # [df 00:00:00, dt+1 00:00:00)
        start_dt = datetime.combine(df, time(0, 0, 0))
        end_dt   = datetime.combine(dt, time(0, 0, 0)) + timedelta(days=1)
        qs = qs.filter(timestamp__gte=start_dt, timestamp__lt=end_dt)
    elif df and not dt:
        # Sólo df
        start_dt = datetime.combine(df, time(0, 0, 0))
        end_dt   = start_dt + timedelta(days=1)
        qs = qs.filter(timestamp__gte=start_dt, timestamp__lt=end_dt)
    elif dt and not df:
        # Hasta dt inclusive
        end_dt = datetime.combine(dt, time(0, 0, 0)) + timedelta(days=1)
        qs = qs.filter(timestamp__lt=end_dt)
    # --------------------------------------------------------

    if user_id:
        qs = qs.filter(actor_id=user_id)

    # Modelos que necesitamos
    Movims   = apps.get_model("administracion_contabilidad", "Movims")
    Factudif = apps.get_model("administracion_contabilidad", "Factudif")
    Asientos = apps.get_model("administracion_contabilidad", "Asientos")

    # Helpers
    def user_display(actor):
        if not actor:
            return "—"
        if hasattr(actor, "get_username"):
            u = actor.get_username()
            if u:
                return u
        return getattr(actor, "email", None) or "—"

    def format_movim_number(movim):
        """
        Formatea el nro de factura a partir de Movims.
        Serie + 3 ceros "compartidos" entre serie/prefijo + prefijo - número.
        Si hay mtipo/mnombremov, lo antepone.
        """
        nro_completo = ""
        if getattr(movim, "mserie", None) and getattr(movim, "mprefijo", None) and getattr(movim, "mboleta", None):
            s = str(movim.mserie)
            p = str(movim.mprefijo)
            n = str(movim.mboleta)

            tz = len(s) - len(s.rstrip('0'))  # ceros al final de serie
            lz = len(p) - len(p.lstrip('0'))  # ceros al inicio de prefijo
            sep = '0' * max(0, 3 - (tz + lz))  # total 3 ceros entre serie y prefijo

            tipo_txt = (str(getattr(movim, "mnombremov", "")).strip() + " ") if getattr(movim, "mtipo", None) else ""
            nro_completo = f"{tipo_txt}{s}{sep}{p}-{n}"
        return nro_completo or "--"

    def format_changes(entry: LogEntry):
        """
        Devuelve cambios legibles:
        campo: old → new
        Si no hay changes_dict, usa 'changes' crudo.
        """
        try:
            cd = entry.changes_dict
        except Exception:
            cd = None

        if cd:
            parts = []
            for field, pair in cd.items():
                # pair es [old, new] (puede ser None)
                try:
                    old_val, new_val = pair
                except Exception:
                    old_val, new_val = None, None
                old_txt = "—" if old_val in [None, ""] else str(old_val)
                new_txt = "—" if new_val in [None, ""] else str(new_val)
                parts.append(f"{field}: {old_txt} → {new_txt}")
            return "\n".join(parts)
        return entry.changes or "--"

    def factura_for_entry(entry: LogEntry) -> str:
        """
        Determina el texto de 'Factura' para un log en particular:
        - Movims: número armado.
        - Factudif: 'SEG <zseguimiento> - <zposicion>'.
        - Otros:
            - Si relaciona con Movims por autogenerado/mautogen/mautofac → nro de ese movim.
            - Si es Asientos y no relaciona → detalle.
            - Caso contrario → '--'.
        """
        model = entry.content_type.model_class()
        if not model:
            return "--"

        obj = model.objects.filter(pk=entry.object_pk).first()
        if not obj:
            return "--"

        table = model._meta.db_table.lower()

        # Movims
        if table == "dataset_movims":
            return format_movim_number(obj)

        # Factudif
        if table == "dataset_factudif":
            seg = getattr(obj, "zseguimiento", None) or "--"
            pos = getattr(obj, "zposicion", None) or "--"
            return f"SEG {seg} - {pos}"

        # Otros: intentar relacionar con Movims
        autogen = (
            getattr(obj, "autogenerado", None)
            or getattr(obj, "mautogen", None)
            or getattr(obj, "mautofac", None)
        )
        if autogen:
            movim = Movims.objects.filter(mautogen=autogen).first()
            if movim:
                return format_movim_number(movim)

        # Asientos suelto
        if table == "dataset_asientos":
            return getattr(obj, "detalle", None) or "--"

        return "--"

    # Crear XLSX en memoria
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Logs")

    # Estilos
    hdr = workbook.add_format({'bold': True, 'bg_color': '#D9E1F2', 'border': 1})
    cell = workbook.add_format({'border': 1})
    cell_wrap = workbook.add_format({'border': 1, 'text_wrap': True})

    # Anchos de columnas
    worksheet.set_column(0, 0, 28)  # Tabla
    worksheet.set_column(1, 1, 32)  # Factura
    worksheet.set_column(2, 2, 19)  # Fecha
    worksheet.set_column(3, 3, 22)  # Usuario
    worksheet.set_column(4, 4, 80)  # Cambios

    # Encabezados
    headers = ["Tabla", "Informacion", "Fecha", "Usuario", "Cambios"]
    for col, h in enumerate(headers):
        worksheet.write(0, col, h, hdr)

    # Datos
    row = 1
    for e in qs.order_by("-timestamp"):
        tabla   = f"{e.content_type.app_label}.{e.content_type.model}"
        factura = factura_for_entry(e)
        fecha   = e.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        usuario = user_display(e.actor)
        cambios = format_changes(e)

        worksheet.write(row, 0, tabla,   cell)
        worksheet.write(row, 1, factura, cell)
        worksheet.write(row, 2, fecha,   cell)
        worksheet.write(row, 3, usuario, cell)
        worksheet.write(row, 4, cambios, cell_wrap)
        row += 1

    workbook.close()
    output.seek(0)
    resp = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    resp['Content-Disposition'] = 'attachment; filename="logs_administracion.xlsx"'
    return resp
