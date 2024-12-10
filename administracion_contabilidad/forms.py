from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
import datetime
from django.forms import RadioSelect
from mantenimientos.models import Monedas, Bancos
from administracion_contabilidad.models import Dolar, Infofactura, Cuentas
from django.db.models import Q


def get_arbitraje():
    try:
        data = datetime.datetime.now().date()
        dolar = Dolar.objects.get(ufecha=data)
        arbitraje_valor = dolar.uvalor
    except Dolar.DoesNotExist:
        arbitraje_valor = 0.0000
    return arbitraje_valor


def get_paridad():
    try:
        data = datetime.datetime.now().date()
        dolar = Dolar.objects.get(ufecha=data)
        paridad_valor = dolar.paridad
    except Dolar.DoesNotExist:
        paridad_valor = 0.0000
    return paridad_valor


class Factura(forms.Form):
    CHOICE_TIPO = (
        ('20', 'Factura'),
        ('0', 'Nota de débito'),
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
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    paridad = forms.FloatField(
        required=False,
        label="Paridad",
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
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'id': 'id_precio_fac'}),
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

    def __init__(self, *args, **kwargs):
        super(Factura, self).__init__(*args, **kwargs)

        # Obtener valores de arbitraje y paridad
        self.arbitraje_valor = get_arbitraje()
        self.paridad_valor = get_paridad()

        # Asignar valores iniciales a los campos de arbitraje y paridad
        self.fields['arbitraje'].initial = self.arbitraje_valor
        self.fields['paridad'].initial = self.paridad_valor


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
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    paridad = forms.FloatField(
        required=False,
        label="Paridad",
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

    def __init__(self, *args, **kwargs):
        super(ProveedoresGastos, self).__init__(*args, **kwargs)

        # Obtener valores de arbitraje y paridad
        self.arbitraje_valor = get_arbitraje()
        self.paridad_valor = get_paridad()

        # Asignar valores iniciales a los campos de arbitraje y paridad
        self.fields['arbitraje'].initial = self.arbitraje_valor
        self.fields['paridad'].initial = self.paridad_valor


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
        widget=forms.TextInput(attrs={'class': 'form-control'}),
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
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número válido'
        }
    )

    moneda = forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        label="Moneda",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )

    moneda_efectivo = forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        label="Moneda",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )

    moneda_transferencia= forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        label="Moneda",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )

    moneda_deposito = forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        label="Moneda",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )
    moneda_cheque= forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        label="Moneda",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )

    moneda_otro = forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        label="Moneda",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )

    cuenta_efectivo = forms.ModelChoiceField(
        queryset=Cuentas.objects.filter(xnivel1__contains="111"),
        label="Cuenta",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'},
        to_field_name='xcodigo'
    )


    cuenta_cheque = forms.ModelChoiceField(
        queryset=Cuentas.objects.filter(Q(xcodigo="11113") | Q(xcodigo="11114")),
        label="Cuenta",
        initial="11113",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'},
        to_field_name='xcodigo'
    )

    cuenta_transferencia = forms.ModelChoiceField(
        queryset=Cuentas.objects.filter(xcodigo__range=("11120", "11125")),
        label="Cuenta",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'},
        to_field_name='xcodigo'
    )

    cuenta_deposito = forms.ModelChoiceField(
        queryset=Cuentas.objects.filter(xcodigo__range=("11120", "11125")),
        label="Cuenta",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'},
        to_field_name='xcodigo'
    )

    cuenta_observaciones = forms.ModelChoiceField(
        queryset=Cuentas.objects.all(),
        label="Cuenta",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'},
        to_field_name='xcodigo'
    )

    cuenta_otro = forms.ModelChoiceField(
        queryset=Cuentas.objects.all(),
        label="Cuenta",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'},
        to_field_name='xcodigo'
    )

    banco_cheque = forms.ModelChoiceField(
        queryset=Bancos.objects.all(),
        label="Banco",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )
    banco_transferencia = forms.ModelChoiceField(
        queryset=Bancos.objects.all(),
        label="Banco",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )
    banco_deposito = forms.ModelChoiceField(
        queryset=Bancos.objects.all(),
        label="Banco",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )
    banco_otro = forms.ModelChoiceField(
        queryset=Bancos.objects.all(),
        label="Banco",
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
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    paridad = forms.FloatField(
        required=False,
        label="Paridad",
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

    def __init__(self, *args, **kwargs):
        super(Cobranza, self).__init__(*args, **kwargs)

        # Obtener valores de arbitraje y paridad
        self.arbitraje_valor = get_arbitraje()
        self.paridad_valor = get_paridad()

        # Asignar valores iniciales a los campos de arbitraje y paridad
        self.fields['arbitraje'].initial = self.arbitraje_valor
        self.fields['paridad'].initial = self.paridad_valor


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
        widget=forms.NumberInput(attrs={'step': '0.0001', 'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    paridad = forms.FloatField(
        required=False,
        label="Paridad",
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

    def __init__(self, *args, **kwargs):
        super(OrdenPago, self).__init__(*args, **kwargs)

        # Obtener valores de arbitraje y paridad
        self.arbitraje_valor = get_arbitraje()
        self.paridad_valor = get_paridad()

        # Asignar valores iniciales a los campos de arbitraje y paridad
        self.fields['arbitraje'].initial = self.arbitraje_valor
        self.fields['paridad'].initial = self.paridad_valor

class pdfForm(BSModalModelForm):
    class Meta:
        model = Infofactura
        fields = ['observaciones',]  # Agrega los campos que deseas actualizar

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))

    observaciones = forms.CharField(widget=forms.Textarea(attrs={"id": 'pdf_add_input', "autocomplete": "off", 'required': False, 'max_length': 500, "rows": "25"," cols": "100", "class": "form-control"}, ), required=False, label="Notas", max_length=500)


class EditarConsultarPagos(forms.Form):

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


# class ArbitrajeParidad(forms.Form):
#     tipo_moneda = forms.ModelChoiceField(
#         queryset=Monedas.objects.all(),
#         required=True,
#         label="Moneda",
#         initial=2,
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         error_messages={'required': 'Este campo es obligatorio'}
#     )
#
#     valor_arbitraje = forms.DecimalField(
#         label="Arbitraje",
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=True,
#         max_digits=10,
#         decimal_places=2
#     )
#
#     valor_paridad = forms.DecimalField(
#         label="Paridad",
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=True,
#         max_digits=10,
#         decimal_places=2
#     )
#
#     valor_pizarra = forms.DecimalField(
#         label="Pizarra",
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=True,
#         max_digits=10,
#         decimal_places=2
#     )
