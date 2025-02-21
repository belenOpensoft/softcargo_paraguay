from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
import datetime
from django.forms import RadioSelect
from mantenimientos.models import Monedas, Bancos
from administracion_contabilidad.models import Dolar, Infofactura, Cuentas
from django.db.models import Q

class EJEMPLO(forms.Form):
    numero = forms.CharField(
        label="Número",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        error_messages={
            'invalid': 'Por favor, ingresa un número válido'
        }
    )

    moneda = forms.CharField(
        required=True,
        label="Moneda",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    prefijo = forms.CharField(
        max_length=4,
        required=True,
        label="",
        initial="0001",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el número de factura'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número válido'
        }
    )

    voucher = forms.CharField(
        label="Voucher",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    alta_de = forms.CharField(
        label="Alta de",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    detalle = forms.CharField(
        label="Detalle",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    fecha = forms.DateField(
        label="Fecha",
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
        required=True
    )
    documento = forms.CharField(
        label="Documento",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    arbitraje = forms.CharField(
        label="Arbitraje",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    importe = forms.DecimalField(
        label="Importe",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        max_digits=10,
        decimal_places=2
    )
    por_imputar = forms.DecimalField(
        label="Por imputar",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        max_digits=10,
        decimal_places=2
    )
    paridad = forms.DecimalField(
        label="Paridad",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        max_digits=10,
        decimal_places=6
    )

    autogenerado = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    buscar_ajuste_acr = forms.BooleanField(
        label="Buscar ajuste de cuenta proveedora",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    buscar_ajuste_dif = forms.BooleanField(
        label="Buscar ajuste de diferecncia de cambio",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    mov_efectivo = forms.CharField(
        label="Movimiento de efectivo recibido",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    moneda_f = forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        required=True,
        label="Moneda",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )


