from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
import datetime
from django.forms import RadioSelect
from mantenimientos.models import Monedas, Bancos, Clientes
from administracion_contabilidad.models import Dolar, Infofactura, Cuentas
from django.db.models import Q
#ventas
class ReporteMovimientosForm(forms.Form):
    fecha_desde = forms.DateField(
        label="Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    fecha_hasta = forms.DateField(
        label="Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    todas_monedas = forms.BooleanField(
        required=False,
        label="Todas las monedas",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    consolidar_dolares = forms.BooleanField(
        required=False,
        label="Consolidar en dólares",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    socio_comercial = forms.CharField(
        label="Solo movimientos del socio comercial",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    socio_comercial_i = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'class': 'form-control form-control-sm','id':'id_cliente_hidden'})
    )
    movimiento = forms.ChoiceField(
        label="Movimiento",
        choices=[('todos', 'Todos'), (10, 'Contado'), (11, 'Dev. Contado'), (20, 'Factura'), (21, 'Not. Credito')],
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    estado = forms.ChoiceField(
        label="Estado",
        choices=[
            ('todo', 'Todo'),
            ('canceladas', 'Canceladas'),
            ('pendientes', 'Pendientes')
        ],
        widget=forms.RadioSelect()
    )

class BalanceCuentasCobrarForm(forms.Form):
    fecha_hasta = forms.DateField(
        label="Generar saldos hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    consolidar_moneda_nac = forms.BooleanField(
        required=False,
        label="Consolidar en moneda nacional",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    consolidar_dolares = forms.BooleanField(
        required=False,
        label="Consolidar en dólares",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class ReporteCobranzasForm(forms.Form):
    fecha_desde = forms.DateField(
        label="Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    fecha_hasta = forms.DateField(
        label="Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    consolidar_moneda_nac = forms.BooleanField(
        required=False,
        label="Consolidar en moneda nacional",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    consolidar_dolares = forms.BooleanField(
        required=False,
        label="Consolidar en dólares",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    ver_detalle = forms.BooleanField(
        required=False,
        label="Ver detalle del cobro",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    ver_anuladas = forms.BooleanField(
        required=False,
        label="Ver cobranzas anuladas",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class AntiguedadSaldosForm(forms.Form):
    BASE_CALCULO_CHOICES = [
        ('vencimiento', 'Vencimiento del documento'),
        ('emision', 'Emisión del documento'),
    ]

    RANGO_CHOICES = [
        ('rango1', 'En fecha, 30, 60, 90, 120, más de 120 días'),
        ('rango2', 'En fecha, 15, 30, 45, 60, más de 60 días'),
        ('rango3', 'En fecha, 30, 90, 180, 360, más de 360 días'),
    ]

    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    base_calculo = forms.ChoiceField(
        label="Calcular en base a",
        choices=BASE_CALCULO_CHOICES,
        widget=forms.RadioSelect
    )

    rango = forms.ChoiceField(
        label="Rango de antigüedad",
        choices=RANGO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

class EstadoCuentaForm(forms.Form):
    TIPO_CONSULTA_CHOICES = [
        ('general', 'General'),
        ('individual', 'Individual'),
    ]

    FILTRO_TIPO_CHOICES = [
        ('todos', 'Todos'),
        ('clientes', 'Solo Clientes'),
        ('agentes', 'Solo Agentes'),
        ('transportistas', 'Solo Transportistas'),
    ]

    tipo_consulta = forms.ChoiceField(
        choices=TIPO_CONSULTA_CHOICES,
        widget=forms.RadioSelect,
        initial='general',
        label="Tipo de consulta"
    )

    # General e individual
    fecha_desde = forms.DateField(
        label="Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    fecha_hasta = forms.DateField(
        label="Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    # Individual
    cliente = forms.CharField(
        label="Cliente",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    cliente_codigo=forms.CharField(widget=forms.HiddenInput(),required=False)
    todas_las_monedas = forms.BooleanField(
        required=False,
        label="Todas las monedas",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # General
    filtro_tipo = forms.ChoiceField(
        choices=FILTRO_TIPO_CHOICES,
        widget=forms.RadioSelect,
        initial='todos',
        label="Filtrar por tipo",
        required=False
    )
    consolidar_moneda_nac = forms.BooleanField(
        required=False,
        label="Consolidar en moneda nacional",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    consolidar_dolares = forms.BooleanField(
        required=False,
        label="Consolidar en dólares",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    omitir_saldos_cero = forms.BooleanField(
        required=False,
        label="No mostrar saldos en 0",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

#compras
class ReporteMovimientosComprasForm(forms.Form):
    fecha_desde = forms.DateField(
        label="Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    fecha_hasta = forms.DateField(
        label="Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    todas_monedas = forms.BooleanField(
        required=False,
        label="Todas las monedas",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    consolidar_dolares = forms.BooleanField(
        required=False,
        label="Consolidar en dólares",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    socio_comercial = forms.CharField(
        label="Solo movimientos del socio comercial",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    socio_comercial_i = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'class': 'form-control form-control-sm','id':'id_cliente_hidden'})
    )
    movimiento = forms.ChoiceField(
        label="Movimiento",
        choices=[('todos', 'Todos'), (10, 'Contado'), (11, 'Dev. Contado'), (20, 'Factura'), (21, 'Not. Credito')],
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    estado = forms.ChoiceField(
        label="Estado",
        choices=[
            ('todo', 'Todo'),
            ('canceladas', 'Canceladas'),
            ('pendientes', 'Pendientes')
        ],
        widget=forms.RadioSelect()
    )

class BalanceCuentasPagarForm(forms.Form):
    fecha_hasta = forms.DateField(
        label="Generar saldos hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    consolidar_moneda_nac = forms.BooleanField(
        required=False,
        label="Consolidar en moneda nacional",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    consolidar_dolares = forms.BooleanField(
        required=False,
        label="Consolidar en dólares",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class ReportePagosForm(forms.Form):
    fecha_desde = forms.DateField(
        label="Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    fecha_hasta = forms.DateField(
        label="Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    consolidar_moneda_nac = forms.BooleanField(
        required=False,
        label="Consolidar en moneda nacional",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    consolidar_dolares = forms.BooleanField(
        required=False,
        label="Consolidar en dólares",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    ver_detalle = forms.BooleanField(
        required=False,
        label="Ver detalle del Pago",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    ver_anuladas = forms.BooleanField(
        required=False,
        label="Ver pagos anulados",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class AntiguedadSaldosComprasForm(forms.Form):
    BASE_CALCULO_CHOICES = [
        ('vencimiento', 'Vencimiento del documento'),
        ('emision', 'Emisión del documento'),
    ]

    RANGO_CHOICES = [
        ('rango1', 'En fecha, 30, 60, 90, 120, más de 120 días'),
        ('rango2', 'En fecha, 15, 30, 45, 60, más de 60 días'),
        ('rango3', 'En fecha, 30, 90, 180, 360, más de 360 días'),
    ]

    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    base_calculo = forms.ChoiceField(
        label="Calcular en base a",
        choices=BASE_CALCULO_CHOICES,
        widget=forms.RadioSelect
    )

    rango = forms.ChoiceField(
        label="Rango de antigüedad",
        choices=RANGO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

class EstadoCuentaComprasForm(forms.Form):
    TIPO_CONSULTA_CHOICES = [
        ('general', 'General'),
        ('individual', 'Individual'),
    ]

    FILTRO_TIPO_CHOICES = [
        ('todos', 'Todos'),
        ('proveedor', 'Solo Proveedores'),
        ('agentes', 'Solo Agentes'),
        ('transportistas', 'Solo Transportistas'),
    ]

    tipo_consulta = forms.ChoiceField(
        choices=TIPO_CONSULTA_CHOICES,
        widget=forms.RadioSelect,
        initial='general',
        label="Tipo de consulta"
    )

    # General e individual
    fecha_desde = forms.DateField(
        label="Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    fecha_hasta = forms.DateField(
        label="Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    # Individual
    cliente = forms.CharField(
        label="Cliente",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    cliente_codigo=forms.CharField(widget=forms.HiddenInput())
    todas_las_monedas = forms.BooleanField(
        required=False,
        label="Todas las monedas",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # General
    filtro_tipo = forms.ChoiceField(
        choices=FILTRO_TIPO_CHOICES,
        widget=forms.RadioSelect,
        initial='todos',
        label="Filtrar por tipo",
        required=False
    )
    consolidar_moneda_nac = forms.BooleanField(
        required=False,
        label="Consolidar en moneda nacional",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    consolidar_dolares = forms.BooleanField(
        required=False,
        label="Consolidar en dólares",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    omitir_saldos_cero = forms.BooleanField(
        required=False,
        label="No mostrar saldos en 0",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

#mixtas

class BalanceMixtasForm(forms.Form):
    fecha_hasta = forms.DateField(
        label="Generar saldos hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    consolidar_moneda_nac = forms.BooleanField(
        required=False,
        label="Consolidar en moneda nacional",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    consolidar_dolares = forms.BooleanField(
        required=False,
        label="Consolidar en dólares",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
class EstadoCuentaMixtasForm(forms.Form):
    TIPO_CONSULTA_CHOICES = [
        ('general', 'General'),
        ('individual', 'Individual'),
    ]

    FILTRO_TIPO_CHOICES = [
        ('todos', 'Todos'),
        ('clientes', 'Solo Clientes'),
        ('agentes', 'Solo Agentes'),
        ('transportistas', 'Solo Transportistas'),
    ]

    tipo_consulta = forms.ChoiceField(
        choices=TIPO_CONSULTA_CHOICES,
        widget=forms.RadioSelect,
        initial='general',
        label="Tipo de consulta"
    )

    # General e individual
    fecha_desde = forms.DateField(
        label="Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    fecha_hasta = forms.DateField(
        label="Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    # Individual
    cliente = forms.CharField(
        label="Cliente",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    cliente_codigo=forms.CharField(widget=forms.HiddenInput(),required=False)

    todas_las_monedas = forms.BooleanField(
        required=False,
        label="Todas las monedas",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # General
    filtro_tipo = forms.ChoiceField(
        choices=FILTRO_TIPO_CHOICES,
        widget=forms.RadioSelect,
        initial='todos',
        label="Filtrar por tipo",
        required=False
    )
    consolidar_moneda_nac = forms.BooleanField(
        required=False,
        label="Consolidar en moneda nacional",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    consolidar_dolares = forms.BooleanField(
        required=False,
        label="Consolidar en dólares",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    omitir_saldos_cero = forms.BooleanField(
        required=False,
        label="No mostrar saldos en 0",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
class AntiguedadSaldosMixtasForm(forms.Form):
    BASE_CALCULO_CHOICES = [
        ('vencimiento', 'Vencimiento del documento'),
        ('emision', 'Emisión del documento'),
    ]

    RANGO_CHOICES = [
        ('rango1', 'En fecha, 30, 60, 90, 120, más de 120 días'),
        ('rango2', 'En fecha, 15, 30, 45, 60, más de 60 días'),
        ('rango3', 'En fecha, 30, 90, 180, 360, más de 360 días'),
    ]

    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    base_calculo = forms.ChoiceField(
        label="Calcular en base a",
        choices=BASE_CALCULO_CHOICES,
        widget=forms.RadioSelect
    )

    rango = forms.ChoiceField(
        label="Rango de antigüedad",
        choices=RANGO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

#contabilidad
class ConsultaArbitrajesForm(forms.Form):
    fecha_desde = forms.DateField(
        label="Fecha desde",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )

    fecha_hasta = forms.DateField(
        label="Fecha hasta",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )

    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
class LibroDiarioForm(forms.Form):
    TIPO_CONSULTA_CHOICES = [
        ('todos', 'Todos'),
        ('ventas', 'Solo ventas'),
        ('compras', 'Solo compras'),
        ('cobros', 'Solo cobros'),
        ('pagos', 'Solo pagos'),
        ('sin_ventas_compras', 'Sin compras o ventas'),
    ]

    fecha_desde = forms.DateField(
        label="Fecha desde",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )

    fecha_hasta = forms.DateField(
        label="Fecha hasta",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )

    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    consolidar_dolares = forms.BooleanField(
        label="Consolidar en dólares",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    consolidar_moneda_nac = forms.BooleanField(
        label="Consolidar en moneda nacional",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    tipo_consulta = forms.ChoiceField(
        label="Filtrar por",
        choices=TIPO_CONSULTA_CHOICES,
        widget=forms.RadioSelect
    )
class BalanceEvolutivoForm(forms.Form):
    desde = forms.DateField(
        label="Desde",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    consolidar_moneda_nac = forms.BooleanField(
        label="Consolidar Moneda Nacional",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    consolidar_dolares = forms.BooleanField(
        label="Consolidar Dólares",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
class MayoresAnaliticosForm(forms.Form):

    banco = forms.ModelChoiceField(
        label="Cuenta",
        required=False,
        queryset=Cuentas.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    cuenta_desde = forms.IntegerField(
        label="Desde la cuenta",
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
    )

    cuenta_hasta = forms.IntegerField(
        label="Hasta la cuenta",
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
    )

    fecha_desde = forms.DateField(
        label="Fecha desde",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )

    fecha_hasta = forms.DateField(
        label="Fecha hasta",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )

    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    consolidar_moneda_nac = forms.BooleanField(
        label="Consolidar en moneda nacional",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    consolidar_dolares = forms.BooleanField(
        label="Consolidar en dólares",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

#cargas
class FichaEmbarqueForm(forms.Form):
    OPERATIVAS = [
        ('importacion_maritima', 'IMPORT MARÍTIMO'),
        ('exportacion_maritima', 'EXPORT MARÍTIMO'),
        ('importacion_aerea', 'IMPORT AÉREO'),
        ('exportacion_aerea', 'EXPORT AÉREO'),
        ('importacion_terrestre', 'IMPORT TERRESTRE'),
        ('exportacion_terrestre', 'EXPORT TERRESTRE'),
    ]

    operativa = forms.ChoiceField(
        choices=OPERATIVAS,
        label="Tipo de Operativa",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )

    master = forms.CharField(
        required=False,
        label="Master",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'id_master'})
    )
    house = forms.CharField(
        required=False,
        label="House",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'id_house'})
    )

    posicion = forms.CharField(
        required=False,
        label="Posición",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'id_posicion'})
    )

    seguimiento = forms.CharField(
        required=False,
        label="Seguimiento",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'id_seguimiento'})
    )

    detallar_preventas = forms.BooleanField(
        required=False,
        label="Detallar preventas",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    expresar_moneda_nac = forms.BooleanField(
        required=False,
        label="Expresar en moneda nacional",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

MESES = [
    ("1", "Enero"), ("2", "Febrero"), ("3", "Marzo"), ("4", "Abril"),
    ("5", "Mayo"), ("6", "Junio"), ("7", "Julio"), ("8", "Agosto"),
    ("9", "Setiembre"), ("10", "Octubre"), ("11", "Noviembre"), ("12", "Diciembre"),
]

OPERATIVAS = [
    ("imp_maritima", "Importación marítima"),
    ("exp_maritima", "Exportación marítima"),
    ("imp_aerea", "Importación aérea"),
    ("exp_aerea", "Exportación aérea"),
    ("imp_terrestre", "Importación terrestre"),
    ("exp_terrestre", "Exportación terrestre"),
]
from django.utils import timezone
def _anios_choices(desde=2015):
    actual = timezone.now().year
    return [(str(y), str(y)) for y in range(actual, desde - 1, -1)]

class UtilidadMensualPosicionForm(forms.Form):
    mes = forms.ChoiceField(choices=MESES, label="Mes", widget=forms.Select(attrs={"class": "form-control"}))
    anio = forms.ChoiceField(choices=_anios_choices(), label="Año", widget=forms.Select(attrs={"class": "form-control"}))

    operativa = forms.MultipleChoiceField(
        choices=OPERATIVAS,
        label="Operativas",
        widget=forms.CheckboxSelectMultiple
    )

    moneda_nacional = forms.BooleanField(
        required=False,
        label="Expresar en moneda nacional",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    apertura_por_posicion = forms.BooleanField(
        required=False,
        label="Apertura de movimientos por posición",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

