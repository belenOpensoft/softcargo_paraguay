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
        ('22', 'Nota de débito'),
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
        label="Prefijo",
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
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control text-end','readonly':True}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    iva = forms.FloatField(
        required=False,
        label="IVA",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control text-right text-end','readonly':True}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    total = forms.FloatField(
        required=False,
        label="Total",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control text-end','readonly':True}),
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


class RegistroCargaForm(forms.Form):
    referencia = forms.CharField(label="Referencia", max_length=100)
    seguimiento = forms.CharField(label="Seguimiento", max_length=100)
    peso = forms.DecimalField(label="Peso", max_digits=10, decimal_places=2)
    aplicable = forms.CharField(label="Aplicable", max_length=100)
    volumen = forms.DecimalField(label="Volumen", max_digits=10, decimal_places=2)
    bultos = forms.DecimalField(label="Bultos", max_digits=10, decimal_places=2)
    posicion = forms.CharField(label="Posicion")

    transportista = forms.CharField(label="Transportista", max_length=100)
    vuelo_vapor = forms.CharField(label="Vuelo/Vapor", max_length=100)
    mawb = forms.CharField(label="MAWB/MBL/MCRT", max_length=100)
    hawb = forms.CharField(label="HAWB/HBL/HCRT", max_length=100)

    origen = forms.CharField(label="Origen", max_length=100)
    destino = forms.CharField(label="Destino", max_length=100)
    fecha_llegada_salida = forms.DateField(
        label="Fecha Llegada/Salida",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    consignatario = forms.CharField(label="Consignatario", max_length=100)

    commodity = forms.CharField(label="Commodity", max_length=100)
    wr = forms.CharField(label="WR", max_length=100)
    shipper = forms.CharField(label="Shipper", max_length=100)
    incoterms = forms.CharField(label="Incoterms", max_length=100)
    pago = forms.CharField(label="Pago", max_length=100)
    agente = forms.CharField(label="Agente", max_length=100)

    observaciones = forms.CharField(
        label="Observaciones",
        widget=forms.Textarea(attrs={'rows': 4})
    )

    servicio = forms.ChoiceField(
        label="Servicio",
        choices=[
            ("aereo", "Aéreo"),
            ("terrestre", "Terrestre"),
            ("maritimo", "Marítimo"),
            ("courier", "Courier"),
            ("servicios", "Servicios"),
            ("mudanza", "Mudanza"),
            ("almacenaje", "Almacenaje"),
            ("general", "General"),
        ],
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if field_name == 'observaciones':
                widget.attrs['class'] = widget.attrs.get('class', '') + ' form-control bg-warning'
                widget.attrs.pop('readonly', None)
            elif isinstance(widget, (forms.TextInput, forms.Textarea, forms.NumberInput, forms.DateInput)):
                widget.attrs['readonly'] = 'readonly'
                widget.attrs['class'] = 'form-control'
            elif isinstance(widget, forms.RadioSelect):
                widget.attrs['disabled'] = True


class ProveedoresGastos(forms.Form):
    CHOICE_TIPO = (
        (40, 'Factura'),
        (10, 'Contado'),
        (11, 'Devolución contado'),
        (0, 'Nota de débito'),
        (41, 'Nota de crédito'),
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
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Esto convierte el campo en un calendario
        }),
        error_messages={
            'required': 'La fecha es obligatoria',
            'invalid': 'Ingresa una fecha válida'
        }
    )

    fecha_documento = forms.DateField(
        required=True,
        label="Fecha documento",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Campo de calendario
        }),
        error_messages={
            'required': 'La fecha es obligatoria',
            'invalid': 'Ingresa una fecha válida'
        }
    )

    vencimiento = forms.DateField(
        required=True,
        label="Fecha de vencimiento",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'  # Campo de calendario
        }),
        error_messages={
            'required': 'La fecha es obligatoria',
            'invalid': 'Ingresa una fecha válida'
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
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control text-end','readonly':True}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    iva = forms.FloatField(
        required=False,
        label="IVA",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control text-end','readonly':True}),
        error_messages={
            'required': 'Este campo es obligatorio',
            'invalid': 'Por favor, ingresa un número decimal válido'
        }
    )

    total = forms.FloatField(
        required=False,
        label="Total",
        initial=0.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control text-end','readonly':True}),
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
        initial="0001",
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
        initial="0000001234",
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

    moneda_transferencia = forms.ModelChoiceField(
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
    moneda_cheque = forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        label="Moneda",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )
    moneda_cheque_terceros = forms.ModelChoiceField(
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
    cuenta_cheque_terceros = forms.ModelChoiceField(
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
        widget=forms.DateInput(attrs={
            'type':'date','class': 'form-control'
        }),
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
        initial="0000001234",
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

    moneda_transferencia = forms.ModelChoiceField(
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
    moneda_cheque = forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        label="Moneda",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es obligatorio'}
    )
    moneda_cheque_terceros = forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        label="Moneda",
        initial=2,
        widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
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
        widget=forms.DateInput(attrs={
            'type': 'date', 'class': 'form-control'
        }),
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
    CHOICE_TIPO = [
        ('intencion', 'Intencion'),
        ('definitivo', 'Definitivo'),
    ]
    tipo = forms.TypedChoiceField(
        choices=CHOICE_TIPO,
        widget=RadioSelect()
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
        fields = ['observaciones', ]  # Agrega los campos que deseas actualizar

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))

    observaciones = forms.CharField(widget=forms.Textarea(
        attrs={"id": 'pdf_add_input', "autocomplete": "off", 'required': False, 'max_length': 500, "rows": "25",
               " cols": "100", "class": "form-control"}, ), required=False, label="Notas", max_length=500)


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


class EditarConsultarCompras(forms.Form):
    omitir_fechas = forms.BooleanField(required=False, label="Omitir fechas")
    fecha_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    monedas = forms.ModelChoiceField(queryset=Monedas.objects.all(), required=False, label="Moneda")

    monto = forms.DecimalField(required=False, max_digits=12, decimal_places=2, label="Monto")
    proveedor = forms.CharField(required=False, max_length=100, label="Proveedor")
    documento = forms.CharField(required=False, max_length=100, label="Documento")
    posicion = forms.CharField(required=False, max_length=100, label="Posición")
    proveedor_codigo = forms.CharField(widget=forms.HiddenInput(), required=False)
    TIPO_CHOICES = [
        ('FACTURA', 'Factura'),
        ('CONTADO', 'Contado'),
        ('NOTA DEB.', 'Nota Débito'),
        ('NOTA CRED.', 'Nota Crédito'),
        ('DEVOLUCION', 'Devol Contado'),
    ]
    tipo = forms.ChoiceField(widget=forms.RadioSelect, choices=TIPO_CHOICES, required=False, label="Tipo")

    ESTADO_CHOICES = [
        ('todas', 'Todas'),
        ('pendientes', 'Pendientes'),
        ('cerradas', 'Cerradas'),
    ]
    estado = forms.ChoiceField(widget=forms.RadioSelect, choices=ESTADO_CHOICES, required=False, label="Estado")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            widget = field.widget
            # Aplicar `form-control` solo a campos que no sean Checkbox o Radio
            if not isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                existing_classes = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{existing_classes} form-control'.strip()

class ComprasDetalle(forms.Form):
    prefijo = forms.CharField(
        label="Prefijo",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'readonly': True
        })
    )
    serie = forms.CharField(
        label="Serie",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'readonly': True
        })
    )
    numero = forms.CharField(
        label="Número",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'readonly': True,
            'id':'numero_detalle_compra'
        })
    )

    tipo = forms.CharField(
        label="Tipo",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'readonly': True
        })
    )

    moneda = forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        label="Moneda",
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm',
            'disabled': True,  # Select usa disabled en lugar de readonly
            'id': 'id_moneda_detalle_compra'
        })
    )

    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control form-control-sm bg-warning',
            'id': 'id_fecha_detalle_compra'
        })
    )
    fecha_ingreso = forms.DateField(
        label="Fecha Ingreso",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control form-control-sm bg-warning'
        })
    )
    fecha_vencimiento = forms.DateField(
        label="Vencimiento",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control form-control-sm bg-warning'
        })
    )

    paridad = forms.FloatField(
        label="Paridad",
        required=False,
        widget=forms.NumberInput(attrs={
            'step': '0.0001',
            'class': 'form-control form-control-sm bg-warning',
            'id': 'id_paridad_detalle_compra'

        })
    )
    arbitraje = forms.FloatField(
        label="Arbitraje",
        required=False,
        widget=forms.NumberInput(attrs={
            'step': '0.0001',
            'class': 'form-control form-control-sm bg-warning',
            'id': 'id_arbitraje_detalle_compra'

        })
    )

    proveedor = forms.CharField(
        label="Proveedor",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'id':'id_proveedor_detalle',
            'readonly': True
        })
    )
    detalle = forms.CharField(
        label="Detalle",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm bg-warning',
            'id': 'id_detalle_detalle_compra'

        })
    )

    total = forms.FloatField(
        label="Total",
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'class': 'form-control form-control-sm',
            'readonly': True
        })
    )
    imputable = forms.CharField(
        label="Imputable",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'readonly': True
        })
    )

class ComprasDetallePago(forms.Form):
    numero = forms.CharField(
        label="Nro",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'disabled': True  # los selects usan disabled, no readonly
        })
    )

    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'readonly': True
        })
    )

    arbitraje = forms.FloatField(
        label="Arbitraje",
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    importe = forms.FloatField(
        label="Importe",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    por_imputar = forms.FloatField(
        label="Por Imputar",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    paridad = forms.FloatField(
        label="Paridad",
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    proveedor = forms.CharField(
        label="Proveedor",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    detalle = forms.CharField(
        label="Detalle",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    autogenerado = forms.CharField(widget=forms.HiddenInput())

class DetalleEmbarqueForm(forms.Form):
    cliente = forms.CharField(label="Cliente", widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    embarcador = forms.CharField(label="Embarcador", widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    consignatario = forms.CharField(label="Consignatario", widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    agente = forms.CharField(label="Agente", widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    transportista = forms.CharField(label="Transportista", widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    vapor_vuelo = forms.CharField(label="Vapor/Vuelo", widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    etd_eta = forms.DateField(label="ETD/ETA", widget=forms.DateInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    embarque = forms.DateField(label="Fecha Embarque", widget=forms.DateInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    posicion = forms.CharField(label="Posición", widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    mbl = forms.CharField(label="MBL", widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    hbl = forms.CharField(label="HBL", widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    origen = forms.CharField(label="Origen", widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    destino = forms.CharField(label="Destino", widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))


class EditarConsultarVentas(forms.Form):
    omitir_fechas = forms.BooleanField(required=False, label="Omitir fechas")
    fecha_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    monedas = forms.ModelChoiceField(queryset=Monedas.objects.all(), required=False, label="Moneda")

    monto = forms.DecimalField(required=False, max_digits=12, decimal_places=2, label="Monto")
    cliente = forms.CharField(required=False, max_length=100, label="Cliente")
    documento = forms.CharField(required=False, max_length=100, label="Documento")
    posicion = forms.CharField(required=False, max_length=100, label="Posición")
    cliente_codigo = forms.CharField(widget=forms.HiddenInput(), required=False)
    TIPO_CHOICES = [
        ('FACTURA', 'Factura'),
        ('CONTADO', 'Contado'),
        ('NOTA DEB.', 'Nota Débito'),
        ('NOTA CRED.', 'Nota Crédito'),
        ('DEVOLUCION', 'Devol Contado'),
        ('BOLETA', 'eTicket'),
        ('NOTACONTCRE', 'N/C eTicket'),
    ]
    tipo = forms.ChoiceField(widget=forms.RadioSelect, choices=TIPO_CHOICES, required=False, label="Tipo")

    ESTADO_CHOICES = [
        ('todas', 'Todas'),
        ('pendientes', 'Pendientes'),
        ('cerradas', 'Cerradas'),
    ]
    estado = forms.ChoiceField(widget=forms.RadioSelect, choices=ESTADO_CHOICES, required=False, label="Estado")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            widget = field.widget
            if not isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                existing_classes = widget.attrs.get('class', '')
                widget.attrs['class'] = f'{existing_classes} form-control'.strip()
class VentasDetalle(forms.Form):
    prefijo = forms.CharField(
        label="Prefijo",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'readonly': True
        })
    )
    serie = forms.CharField(
        label="Serie",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'readonly': True
        })
    )
    numero = forms.CharField(
        label="Número",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'readonly': True,
            'id':'numero_detalle_venta'
        })
    )

    tipo = forms.CharField(
        label="Tipo",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'readonly': True
        })
    )

    moneda = forms.ModelChoiceField(
        queryset=Monedas.objects.all(),
        label="Moneda",
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm',
            'disabled': True,  # Select usa disabled en lugar de readonly
            'id': 'id_moneda_detalle_venta'
        })
    )

    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'readonly': True,

            'class': 'form-control form-control-sm',
            'id': 'id_fecha_detalle_venta'
        })
    )
    fecha_ingreso = forms.DateField(
        label="Fecha Ingreso",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'readonly': True,

            'class': 'form-control form-control-sm'
        })
    )
    fecha_vencimiento = forms.DateField(
        label="Vencimiento",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'readonly': True,

            'class': 'form-control form-control-sm'
        })
    )

    paridad = forms.FloatField(
        label="Paridad",
        required=False,
        widget=forms.NumberInput(attrs={
            'step': '0.0001',
            'class': 'form-control form-control-sm bg-warning',
            'id': 'id_paridad_detalle_venta'

        })
    )
    arbitraje = forms.FloatField(
        label="Arbitraje",
        required=False,
        widget=forms.NumberInput(attrs={
            'step': '0.0001',
            'class': 'form-control form-control-sm bg-warning',
            'id': 'id_arbitraje_detalle_venta'

        })
    )

    cliente = forms.CharField(
        label="Cliente",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'id':'id_proveedor_detalle',
            'readonly': True
        })
    )
    detalle = forms.CharField(
        label="Detalle",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm bg-warning',
            'id': 'id_detalle_detalle_venta'

        })
    )

    total = forms.FloatField(
        label="Total",
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'class': 'form-control form-control-sm',
            'readonly': True
        })
    )
    posicion = forms.CharField(
        label="Posicion",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'readonly': True,
            'id': 'id_posicion_venta'

        })
    )
    cae = forms.CharField(
        label="CAE",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'readonly': True
        })
    )
    observaciones = forms.CharField(
        label="Observaciones",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm bg-warning',
            'readonly': True
        })
    )
class VentasDetallePago(forms.Form):
    numero = forms.CharField(
        label="Nro",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    moneda = forms.ModelChoiceField(
        label="Moneda",
        queryset=Monedas.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'disabled': True  # los selects usan disabled, no readonly
        })
    )

    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'readonly': True
        })
    )

    arbitraje = forms.FloatField(
        label="Arbitraje",
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    importe = forms.FloatField(
        label="Importe",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    por_imputar = forms.FloatField(
        label="Por Imputar",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    paridad = forms.FloatField(
        label="Paridad",
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    cliente = forms.CharField(
        label="Cliente",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )

    detalle = forms.CharField(
        label="Detalle",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )
    efectivo_recibido = forms.CharField(
        label="Movimiento de efectivo recibido",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True
        })
    )
    autogenerado = forms.CharField(widget=forms.HiddenInput())