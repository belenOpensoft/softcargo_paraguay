from django import forms
import datetime
from django.forms import RadioSelect
from mantenimientos.models import Monedas
from administracion_contabilidad.models import Dolar

data = datetime.datetime.now().date()

try:
    dolar = Dolar.objects.get(ufecha=data)
    arbitraje_valor = dolar.uvalor
except Dolar.DoesNotExist:
    arbitraje_valor = 0.0000

try:
    dolar = Dolar.objects.get(ufecha=data)
    paridad_valor = dolar.paridad
except Dolar.DoesNotExist:
    paridad_valor = 0.0000


class Factura(forms.Form):
    CHOICE_TIPO = (
        ('11', 'Factura'),
        ('20', 'Nota de débito'),
        ('21', 'Nota de crédito'),
        ('23', 'eticket'),
        ('24', 'eticket N/C'),
    )

    tipo = forms.ChoiceField(
        initial='11',
        choices=CHOICE_TIPO,
        label='',
        widget=forms.Select(attrs={'class': 'form-control', 'autofocus': True}),
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


    # numero = forms.CharField(
    #     max_length=10,
    #     required=True,
    #     label="",
    #     initial=0,
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el número de factura'}),
    #     error_messages={
    #         'required': 'Este campo es obligatorio',
    #         'invalid': 'Por favor, ingresa un número válido'
    #     }
    # )

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
            'type': 'date',
        }),
        input_formats=["%Y-%m-%d"],
        error_messages={
            'required': 'La fecha es obligatoria',
            'invalid': 'Ingresa una fecha válida en formato DD/MM/YY'
        }
    )

    arbitraje = forms.FloatField(
        required=False,
        label="Arbitraje",
        initial=arbitraje_valor,
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    paridad = forms.FloatField(
        required=False,
        label="Paridad",
        initial=paridad_valor,
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
        required=True,
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


class ProveedoresGastos(forms.Form):
    CHOICE_TIPO = (
        ('contado', 'Contado'),
        ('factura', 'Factura'),
        ('devolucion_contado', 'Devolución contado'),
        ('nota_de_debito', 'Nota de débito'),
        ('nota_de_credito', 'Nota de crédito'),
    )

    CHOICE_FACTURA = (
        ('e_factura', 'eFactura'),
        ('e_ticket', 'eTicket')
    )

    CHOICE_TCOBRO = (
        ('local_charges', 'Local Charges'),
        ('due_agent', 'Due Agent'),
        ('due_carrier', 'Due Carrier'),
        ('tax', 'Tax'),
        ('valuation_charges', 'Valuation Charges'),
        ('other', 'Other')
    )

    CHOICE_COBRO = {
        ('P', 'Prepaid'),
        ('C', 'Collect')
    }

    tipo = forms.ChoiceField(
        initial='factura',
        choices=CHOICE_TIPO,
        label='',
        widget=forms.Select(attrs={'class': 'form-control'}),
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

    prefijo = forms.CharField(
        max_length=4,
        required=True,
        label="",
        initial="0000",
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
        initial="0000000000",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el número de factura'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número válido'
        }
    )

    tipo_factura = forms.ChoiceField(
        initial='eFactura',
        choices=CHOICE_FACTURA,
        label='',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    moneda = forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        required=True,
        label="Moneda",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )

    fecha_registro = forms.DateField(
        required=True,
        label="Fecha de registro",
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

    fecha_documento = forms.DateField(
        required=True,
        label="Fecha documento",
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

    vencimiento = forms.DateField(
        required=True,
        label="Fecha de vencimiento",
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
        initial=arbitraje_valor,
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    paridad = forms.FloatField(
        required=False,
        label="Paridad",
        initial=paridad_valor,
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    proveedor = forms.CharField(
        required=True,
        label="Seleccionar Proveedor",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    tercerizado = forms.BooleanField(
        required=False,
        label="Por cuenta y orden de",
    )

    proveedor2 = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar cliente'}),
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

    item = forms.ChoiceField(
        required=False,
        label="Item",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    descripcion = forms.CharField(
        required=False,
        label="Descripcion",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    tipo_cobro = forms.ChoiceField(
        required=True,
        choices=CHOICE_TCOBRO,
        label='Tipo',
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )

    cobro = forms.ChoiceField(
        choices=CHOICE_COBRO,
        label='',
        widget=forms.Select(attrs={'class': 'form-control'}),
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


class Cobranza(forms.Form):
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

    prefijo = forms.CharField(
        max_length=4,
        required=True,
        label="",
        initial="0000",
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
        initial="0000000000",
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

    cliente = forms.CharField(
        required=True,
        label="Seleccionar Cliente",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    arbitraje = forms.FloatField(
        required=False,
        label="Arbitraje",
        initial=arbitraje_valor,
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    paridad = forms.FloatField(
        required=False,
        label="Paridad",
        initial=paridad_valor,
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
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

    importe = forms.FloatField(
        required=False,
        label="Importe",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    a_imputar = forms.FloatField(
        required=False,
        label="A imputar",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        error_messages={
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    Factura = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    saldo = forms.FloatField(
        required=False,
        label="Saldo",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
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


class OrdenPago(forms.Form):

    CHOICE_TIPO = [
        ('intencion', 'Intencion'),
        ('definitivo', 'Definitivo'),
    ]

    numero = forms.CharField(
        max_length=10,
        required=True,
        label="",
        initial="00000",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el número de factura'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número válido'
        }
    )

    tipo = forms.TypedChoiceField(
        choices=CHOICE_TIPO,
        widget=RadioSelect()
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
        initial=arbitraje_valor,
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    paridad = forms.FloatField(
        required=False,
        label="Paridad",
        initial=paridad_valor,
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    saldo = forms.FloatField(
        required=False,
        label="Saldo",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    a_imputar = forms.FloatField(
        required=False,
        label="A imputar",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        error_messages={
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    factura = forms.CharField(
        max_length=10,
        required=True,
        label="Factura",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el número de factura'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número válido'
        }
    )

    saldo = forms.FloatField(
        required=False,
        label="Saldo",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    se_imputaran = forms.FloatField(
        required=False,
        label="Se imputarán",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )
