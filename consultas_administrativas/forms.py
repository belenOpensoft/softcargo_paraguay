from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
import datetime
from django.forms import RadioSelect
from mantenimientos.models import Monedas, Bancos
from administracion_contabilidad.models import Dolar, Infofactura, Cuentas
from django.db.models import Q

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


