from django import forms
import datetime
from mantenimientos.models import Monedas


class Factura(forms.Form):

    CHOICE_TIPO = (
        ("C", "COMPRA"),
        ("V", "VENTA"),
    )

    autogenerado = forms.CharField(

    )

    serie = forms.CharField(
        max_length=1,
        required=True,
        label="Serie",
        initial="A",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de serie'
            }
        ),
        error_messages={
            'required': 'Este campo es obligatorio',
            'max_length': 'El número de serie no puede tener más de 1 caracter'
        }
    )

    tipo = forms.ChoiceField(
        choices=CHOICE_TIPO,
        required=True,
        initial="V",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
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

    numero = forms.CharField(
        max_length=10,
        required=True,
        label="",
        initial="0000000001",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el número de factura'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número válido'
        }
    )

    moneda = forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        required=True,
        label="Moneda",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )

    fecha = forms.DateField(
        required=True,
        label="Fecha",
        initial=datetime.date.today,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'DD/MM/YY'
        }),
        input_formats=['%d/%m/%y'],
        error_messages={
            'required': 'La fecha es obligatoria',
            'invalid': 'Ingresa una fecha válida en formato DD/MM/YY'
        }
    )

    arbitraje = forms.FloatField(
        required=False,
        label="Arbitraje",
        initial=0.0000,
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    paridad = forms.FloatField(
        required=False,
        label="Paridad",
        initial=0.0000,
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    mes_anio_actual = datetime.datetime.now().strftime('%m/%Y')

    imputar = forms.CharField(
        label="Imputar",
        initial=mes_anio_actual,
        widget=forms.TextInput(attrs={'placeholder': 'MM/YYYY', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa una fecha válida en formato MM/YYYY'
        }
    )

    cliente = forms.CharField(
        required=False,
        label="Seleccionar Cliente",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    item = forms.ChoiceField(
        required=False,
        label="Item",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    descripcion_item = forms.CharField(
        required=False,
        label="Descripción",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa la descripción'}),
    )

    precio = forms.FloatField(
        required=False,
        label="Precio",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    neto = forms.FloatField(
        required=False,
        label="Neto",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    iva = forms.FloatField(
        required=False,
        label="IVA",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control text-right'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    total = forms.FloatField(
        required=False,
        label="Total",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

