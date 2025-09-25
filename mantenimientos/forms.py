# -*- encoding: utf-8 -*-
import datetime
from cProfile import label

from django import forms
from django.forms import ModelChoiceField

from administracion_contabilidad.models import Cuentas
from mantenimientos.models import Paises, Clientes, Vapores, Vendedores, Servicios, Ciudades, Empresa
from mantenimientos.views.validador import email_o_si

choice_SINO = (('SI','Si'),('NO','No'))
choice_SN = (('S','Si'),('N','No'))


class add_ciudad_form(forms.Form):
    codigo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 5 },),max_length=5,required=True,label="Código")
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'max_length': 30, }),label="Nombre", max_length=30)
    pais = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'pais-select'}),
        label="País",
        required=False
    )
    codedi = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 5 },),max_length=5,required=True,label="Código EDI")
    codaduana = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 5 },),max_length=5,required=True,label="Código Aduana")
    paises_idinternacional = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly','id': 'idinternacional',"autocomplete" :"off",'required': True,'max_length': 50},),max_length=50,required=True,label="ID Pais")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pais'].choices = [('', 'Seleccione un país')] + [(pais.nombre, pais.nombre) for pais in Paises.objects.all()]


class edit_ciudad_form(forms.Form):
    codigo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 5 },),max_length=5,required=True,label="Código")
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'max_length': 30, }),label="Nombre", max_length=30)
    pais = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'pais-select'}),
        label="País",
        required=False
    )
    codedi = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 5 },),max_length=5,required=True,label="Código EDI")
    codaduana = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 5 },),max_length=5,required=True,label="Código Aduana")
    paises_idinternacional = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly','id': 'idinternacional',"autocomplete" :"off",'required': True,'max_length': 50},),max_length=50,required=True,label="ID Pais")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pais'].choices = [('', 'Seleccione un país')] + [(pais.nombre, pais.nombre) for pais in Paises.objects.all()]

class add_vendedor_form(forms.Form):
    #codigo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 5}, ),max_length=5, required=True, label="Código")
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 25, }),label="Nombre", max_length=25)
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 300, }),label="Direccion", max_length=300)
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, }),label="Teléfono", max_length=50)
    localidad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, }),label="Localidad", max_length=50, required=False)
    ciudad = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'pais-select'}),
        label="Ciudad",
        required=False
    )
    pais = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'pais-select'}),
        label="País",
        required=False
    )
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 20, }),label="Email", max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pais'].choices = [('', 'Seleccione un país')] + [(pais.nombre, pais.nombre) for pais in Paises.objects.all()]
        self.fields['ciudad'].choices = [('', 'Seleccione una ciudad')] + [(ciudad.codigo, ciudad.nombre) for ciudad in Ciudades.objects.all()]




class edit_vendedor_form(forms.Form):
    codigo = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 5}, ), max_length=5,
                             required=True, label="Código")
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 25, }),
        label="Nombre", max_length=25)
    direccion = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 300, }),
        label="Direccion", max_length=300)
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, }),
        label="Teléfono", max_length=50)
    localidad = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, }),
        label="Localidad", max_length=50, required=False)
    ciudad = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'pais-select'}),
        label="Ciudad",
        required=False
    )
    pais = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'pais-select'}),
        label="País",
        required=False
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 20, }),
        label="Email", max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pais'].choices = [('', 'Seleccione un país')] + [(pais.nombre, pais.nombre) for pais in
                                                                      Paises.objects.all()]
        self.fields['ciudad'].choices = [('', 'Seleccione una ciudad')] + [(ciudad.codigo, ciudad.nombre) for ciudad in
                                                                           Ciudades.objects.all()]

class add_cliente_form_old_last(forms.Form):
    tipo = forms.ChoiceField(
        choices=[
            (1, 'Cliente'),
            (2, 'Proveedor'),
            (3, 'Mixto'),
            (4, 'Armador'),
            (5, 'Transportista'),
            (6, 'Agente de carga'),
            (7, 'Despachante'),
            (8, 'Otro tipo'),
        ],
        widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        label="Tipo"
    )
    empresa = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        label="Empresa",
        required=False
    )
    razonsocial = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'max_length': 100}),
        label="Razón Social",
        max_length=100,
        required=True
    )
    direccion = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'max_length': 150}),
        label="Dirección",
        max_length=150,
        required=True
    )
    localidad = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'max_length': 100}),
        label="Localidad",
        max_length=100,
        required=True
    )
    cpostal = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'max_length': 10}),
        label="Código Postal",
        max_length=10,
        required=False
    )
    ruc = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'max_length': 20}),
        label="RUT",
        max_length=20,
    )
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'max_length': 20}),
        label="Teléfono",
        max_length=20,
        required=True
    )
    fecalta = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Fecha de Alta",
        required=True
    )
    contactos = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'max_length': 100}),
        label="Contactos",
        max_length=100,
        required=False
    )
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'autocomplete': 'off', 'rows': 3}),
        label="Observaciones",
        required=False
    )
    ciudad = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'ciudad-select'}),
        label="Ciudad",
        required=False
    )
    pais = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'pais-select'}),
        label="País",
        required=False
    )

    # ✅ Añadiendo los campos de email
    emailad = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        label="Email Administrativo",
        required=False
    )
    emailem = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        label="Email Exportación Marítima",
        required=False
    )
    emailea = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        label="Email Exportación Aérea",
        required=False
    )
    emailet = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        label="Email Exportación Terrestre",
        required=False
    )
    emailim = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        label="Email Importación Marítima",
        required=False
    )
    emailia = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        label="Email Importación Aérea",
        required=False
    )
    emailit = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        label="Email Importación Terrestre",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pais'].choices = [('', 'Seleccione un país')] + [(pais.nombre, pais.nombre) for pais in Paises.objects.all()]
        self.fields['ciudad'].choices = [('', 'Seleccione una ciudad')] + [(ciudad.codigo, ciudad.nombre) for ciudad in Ciudades.objects.all()]

class add_cliente_form(forms.Form):

    empresa = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Empresa",
                              required=True)
    razonsocial = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Razón Social",
                                  max_length=100, required=True)
    ruc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="RUT", max_length=20,
                          required=False)

    # Campos opcionales
    prefijoguia = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Prefijo Guia",
                                  required=False)
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Dirección",
                                max_length=150, required=False)
    localidad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Localidad",
                                max_length=100, required=False)
    cpostal = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Código Postal",
                              max_length=10, required=False)
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Teléfono",
                               max_length=20, required=False)
    fecalta = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                              label="Fecha de Alta", required=False)
    contactos = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Contactos",
                                max_length=100, required=False)
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                                    label="Observaciones", required=False)

    ciudad = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'id': 'ciudad-select'}),
                               label="Ciudad", required=False)
    pais = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'id': 'pais-select'}),
                             label="País", required=False)

    # **Nuevos Campos**
    activo = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                label="Activo")
    tipo = forms.ChoiceField(
        choices=[
            (1, 'Cliente'),
            (2, 'Proveedor'),
            (3, 'Mixto'),
            (4, 'Armador'),
            (5, 'Transportista'),
            (6, 'Agente de carga'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tipo de Socio",
        required=False
    )
    vendedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Vendedor",
                               required=False)

    # **Pestaña Emails**
    emailad = forms.CharField(label="Email Administrativo", required=False, validators=[email_o_si],
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    emailem = forms.CharField(label="Email Exportación Marítima", required=False, validators=[email_o_si],
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    emailea = forms.CharField(label="Email Exportación Aérea", required=False, validators=[email_o_si],
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    emailet = forms.CharField(label="Email Exportación Terrestre", required=False, validators=[email_o_si],
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    emailim = forms.CharField(label="Email Importación Marítima", required=False, validators=[email_o_si],
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    emailia = forms.CharField(label="Email Importación Aérea", required=False, validators=[email_o_si],
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    emailit = forms.CharField(label="Email Importación Terrestre", required=False, validators=[email_o_si],
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    # **Pestaña Datos Contables**
    plazo = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                               label="Plazo Crédito (días)", required=False)
    limite = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                              label="Límite de Crédito (USD)", required=False)

    ctavta = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Cuenta de Venta",
                               required=False,initial=0)
    ctacomp = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Cuenta de Compra",
                                required=False,initial=0)

    vendedor_input = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'vendedor_input'}),
        required=False,
        initial=0
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['autocomplete'] = 'off'

        # Cargar opciones en los selects con un valor por defecto opcional
        self.fields['pais'].choices = [('', 'Seleccione un país')] + [
            (pais.nombre.strip(), pais.nombre.strip()) for pais in Paises.objects.all()
        ]
        self.fields['ciudad'].choices = [('', 'Seleccione una ciudad')] + [(ciudad.codigo, ciudad.nombre) for ciudad
                                                                           in Ciudades.objects.all()]
        self.fields['ctavta'].choices = [('0', 'Seleccione una cuenta')] + [(c.xcodigo, c.xnombre) for c in
                                                                           Cuentas.objects.all()]
        self.fields['ctacomp'].choices = [('0', 'Seleccione una cuenta')] + [(c.xcodigo, c.xnombre) for c in
                                                                            Cuentas.objects.all()]


class add_banco_form(forms.Form):
    codigo = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'min': 0, 'max': 99}, ), required=True,
                                label="Código")
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 15, }),
        label="Nombre", max_length=15)
    edi = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 3}, ), max_length=3,
                          required=False, label="Código EDI")
    pais = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'pais-select'}),
        label="País",
        required=False
    )
    rut = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 15}, ), max_length=15,
                          required=False, label="R.U.T.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pais'].choices = [('', 'Seleccione un país')] + [(pais.nombre, pais.nombre) for pais in
                                                                      Paises.objects.all()]

class edit_banco_form(forms.Form):
    codigo = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 5, "readonly": True}, ),
                                required=True, label="Código")
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 15, }),
        label="Nombre", max_length=15)
    edi = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 3}, ), max_length=3,
                          required=False, label="Código EDI")
    pais = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'pais-select'}),
        label="País",
        required=False
    )
    rut = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 15}, ), max_length=15,
                          required=False, label="R.U.T.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pais'].choices = [('', 'Seleccione un país')] + [(pais.nombre, pais.nombre) for pais in Paises.objects.all()]

class add_pais_form(forms.Form):
    CONTINENTE_CHOICES = {
        (1, 'Sudamérica'),
        (2, 'Norteamérica'),
        (3, 'Centroamérica'),
        (4, 'Europa'),
        (5, 'Asia'),
        (6, 'África'),
        (7, 'Oceanía')
    }
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, }),
        label="Nombre", max_length=50)
    continente = forms.ChoiceField(
        choices=CONTINENTE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': True}),
        label="Continente"
    )
    iata = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 1}, ), required=True,
                              label="Cod IATA")
    idinternacional = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 3}),
        label="Cod. Internac.", max_length=3)
    cuit = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 3}, ), required=True,
                              label="Cod. ISO3166.")
    edi = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 3}, ), max_length=3,
                          required=False, label="Código EDI")

class edit_pais_form(forms.Form):
    CONTINENTE_CHOICES = {
        (1, 'Sudamérica'),
        (2,'Norteamérica'),
        (3,'Centroamérica'),
        (4, 'Europa'),
        (5, 'Asia'),
        (6, 'África'),
        (7,'Oceanía')
    }

    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, }),
        label="Nombre", max_length=50)

    continente = forms.ChoiceField(
        choices=CONTINENTE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': True}),
        label="Continente"
    )
    iata = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 1}, ), required=True,
                              label="Cod IATA")
    idinternacional = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 3}),
        label="Cod. Internac.", max_length=3)
    cuit = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 3}, ), required=True,
                              label="Cod. ISO3166.")
    edi = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off",'max_length': 3}, ), max_length=3,
                          required=False, label="Código EDI")

class add_moneda_form(forms.Form):
    codigo = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'min': 0, 'max': 999}, ),
                                required=True, label="Código")
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 24, 'required': True, }), label="Nombre",
                             max_length=24)
    pais = forms.ModelChoiceField(queryset = Paises.objects.all().order_by('nombre') , widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, }), label="Pais", required=True)
    simbolo = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 3}, ), required=True,
                              label="Símbolo", max_length=3)
    solicitar = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 1}, ), required=True,
                                label="Solicitar?", choices = choice_SN)
    alias = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 3,'required':False}), label="Alias.",
        max_length=3)
    valorminimo = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4}, ), max_digits=12,
                                     decimal_places=4, required=False, label="Valor Mínimo")
    valormaximo = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4}, ), max_digits=12,
                                     decimal_places=4, required=False, label="Valor Máximo")
    paridadminima = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4}, ), max_digits=12,
                                       decimal_places=4, required=False, label="Paridad Mínima")
    paridadmaxima = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4}, ), max_digits=12,
                                       decimal_places=4, required=False, label="Paridad Máxima")
    corporativo = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 3}, ), required=True,
                                  label="Corporativo", max_length=3)

class edit_moneda_form(forms.Form):
    codigo = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'min': 0, 'max': 999,
               "readonly": True}, ), required=True, label="Código")
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 24, 'required': True, }), label="Nombre",
                             max_length=24)
    pais = forms.ModelChoiceField(queryset = Paises.objects.all().order_by('nombre') , widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, }), label="Pais", required=True)
    simbolo = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 3}, ), required=True,
                              label="Símbolo", max_length=3)
    solicitar = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 1}, ), required=True,
                                label="Solicitar?", choices = choice_SN )
    alias = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 3,'required':False}), label="Alias.",
        max_length=3)
    valorminimo = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4}, ), max_digits=12,
                                     decimal_places=4, required=False, label="Valor Mínimo")
    valormaximo = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4}, ), max_digits=12,
                                     decimal_places=4, required=False, label="Valor Máximo")
    paridadminima = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4}, ), max_digits=12,
                                       decimal_places=4, required=False, label="Paridad Mínima")
    paridadmaxima = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4}, ), max_digits=12,
                                       decimal_places=4, required=False, label="Paridad Máxima")
    corporativo = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 3}, ), required=True,
                                  label="Corporativo", max_length=3)

class add_producto_form(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, 'required': True, }), label="Nombre",
                             max_length=50)
    descripcion = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, 'required': True, }),
                                  label="Descripcion", max_length=50)

class edit_producto_form(forms.Form):
    codigo = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'min': 0, 'max': 999, "readonly": True, }, ),
                                required=True, label="Código")
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, 'required': True, }), label="Nombre",
                             max_length=50)
    descripcion = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, 'required': True, }),
                                  label="Descripcion", max_length=50)

class add_buque_form(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, 'required': True, }),
        label="Nombre", max_length=50)
    bandera = forms.ModelChoiceField(queryset=Paises.objects.all().order_by('nombre'), widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, }), label="Bandera", required=False)
    observaciones = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 50}, ), required=False,
        label="Observaciones", max_length=50)

class edit_buque_form(forms.Form):
    codigo = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'min': 0, 'max': 999}, ),
        required=True, label="Código")
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, 'required': True, }),
        label="Nombre", max_length=50)
    bandera = forms.ModelChoiceField(queryset=Paises.objects.all().order_by('nombre'), widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, }), label="Bandera", required=False)
    observaciones = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 50}, ), required=False,
        label="Observaciones", max_length=50)


class ClienteModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.empresa + ' (' + obj.prefijoguia + ')'

class edit_buque_form(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        banderas = [("", "---"), ] + list(Paises.objects.all().order_by('nombre').values_list('nombre', 'nombre'))
        self.fields['bandera'].choices = banderas

    codigo = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'min': 0, 'max': 999,
               "readonly": True}, ), required=True, label="Código")
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'max_length': 50, 'required': True, }),
        label="Nombre", max_length=50)
    bandera = forms.ChoiceField(choices=list(), widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, }), label="Bandera", required=True)
    observaciones = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 50}, ), required=True,
        label="Observaciones", max_length=50)


class add_guia_form(forms.Form):
    empresa = ClienteModelChoiceField(queryset=Clientes.objects.all().exclude(prefijoguia="S/I").order_by('empresa') , widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': True, }), label="Cia.Aerea", required=True)
    numeracion = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'min': 0, 'max': 999999999}, ),
        required=True, label="Numeracion de AWB de comienzo")
    cantidad = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'min': 0, 'max': 999}, ),
        required=True, label="Total de AWB's")

class reporte_seguimiento_form(forms.Form):
    # desde = forms.DateField(
    #     label="Desde",
    #     widget=forms.DateInput(attrs={'class': 'form-control mb-3'}),
    # )
    desde = forms.DateField(widget= forms.DateInput(attrs={"type":'date','required': True,"onkeypress":"return tabular(event,this)","class":"form-control mb-3",'autofocus':True}),label="Desde",initial=datetime.datetime.now().strftime("%Y-%m-%d"), required = True)
    hasta = forms.DateField(widget= forms.DateInput(attrs={"type":'date','required': True,"onkeypress":"return tabular(event,this)","class":"form-control mb-3"}),label="Hasta",initial=datetime.datetime.now().strftime("%Y-%m-%d"), required = True)
    filtros = (
        ('', '---------'),
        ('eta', 'Fecha llegada'),
        ('modo', 'Modo'),
        ('operacion', 'Operación'),
        ('vendedor', 'Vendedor'),
        ('tipo_de_operacion', 'Tipo de Operación'),
        ('origen', 'Origen'),
        ('destino', 'Destino'),
        ('status', 'Status'),
        ('buque', 'Buque'),
    )
    MODO_CHOICES = (
        ('', 'Todos'),
        ('aereo', 'Aéreo'),
        ('maritimo', 'Marítimo'),
        ('terrestre', 'Terrestre'),
    )
    modo = forms.ChoiceField(
        choices=MODO_CHOICES,
        label="Modo",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    OPERACION_CHOICES = (
        ('', 'Todos'),
        ('importacion', 'Importación'),
        ('exportacion', 'Exportación'),
    )
    operacion = forms.ChoiceField(
        choices=OPERACION_CHOICES,
        label="Operación",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    vendedor = forms.ModelChoiceField(
        queryset=Vendedores.objects.all(),
        label="Vendedor",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    choice_op = (("", "Todos"),
                 ("IMPORTACION", "IMPORTACION"),
                 ("EXPORTACION", "EXPORTACION"),
                 ("IMPORTACION LCL", "IMPORTACION LCL"),
                 ("IMPORTACION FCL", "IMPORTACION FCL"),
                 ("IMPORTACION PART CONT.", "IMPORTACION PART CONT."),
                 ("TRANSITO FCL", "TRANSITO FCL"),
                 ("IMPORTACION CONSOLIDADA", "IMPORTACION CONSOLIDADA"),
                 ("REEMBARCO", "REEMBARCO"),
                 ("TRANSITO", "TRANSITO"),
                 ("TRASLADO", "TRASLADO"),
                 ("MUESTRA", "MUESTRA"),

                 )

    tipo_de_operacion = forms.ChoiceField(
        choices=choice_op,
        label="Tipo de Operación",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )

    origen = forms.ModelChoiceField(
        queryset=Ciudades.objects.all().order_by('nombre'),
        label="Origen",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    destino = forms.ModelChoiceField(
        queryset=Ciudades.objects.all().order_by('nombre'),
        label="Destino",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3 mb-3'}),
    )

    STATUS_CHOICES = (("","Todos"),("ARRIBADO","ARRIBADO"),("CONFIRMADO","CONFIRMADO"),("CANCELADO","CANCELADO"),("RESERVADO","RESERVADO"),("UNIFICADO","UNIFICADO"),("CERRADO","CERRADO"),)
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label="Status",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    buque = forms.ModelChoiceField(
        queryset=Vapores.objects.all(),
        label="Buque",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    cliente = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        label="Cliente",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    embarcador = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        label="Embarcador",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    consignatario = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        label="Consignatario",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    filtro1 = forms.ChoiceField(
        choices=filtros,
        label="Orden 1",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    filtro2 = forms.ChoiceField(
        choices=filtros,
        label="Orden 2",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    filtro3 = forms.ChoiceField(
        choices=filtros,
        label="Orden 3",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )

class reporte_operativas_form(forms.Form):

    desde = forms.DateField(widget= forms.DateInput(attrs={"type":'date','required': True,"onkeypress":"return tabular(event,this)","class":"form-control mb-3",'autofocus':True}),label="Desde",initial=datetime.datetime.now().strftime("%Y-%m-%d"), required = True)
    hasta = forms.DateField(widget= forms.DateInput(attrs={"type":'date','required': True,"onkeypress":"return tabular(event,this)","class":"form-control mb-3"}),label="Hasta",initial=datetime.datetime.now().strftime("%Y-%m-%d"), required = True)
    filtros = (
        ('', '---------'),
        ('eta', 'Fecha llegada'),
        ('modo', 'Modo'),
        ('tipo_operacion', 'Operación'),
        ('vendedor', 'Vendedor'),
        ('operacion', 'Tipo de Operación'),
        ('origen', 'Origen'),
        ('destino', 'Destino'),
        ('status', 'Status'),
    )
    MODO_CHOICES = (
        ('', 'Todos'),
        ('aereo', 'Aéreo'),
        ('maritimo', 'Marítimo'),
        ('terrestre', 'Terrestre'),
    )
    modo = forms.ChoiceField(
        choices=MODO_CHOICES,
        label="Modo",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    OPERACION_CHOICES = (
        ('', 'Todos'),
        ('importacion', 'Importación'),
        ('exportacion', 'Exportación'),
    )
    operacion = forms.ChoiceField(
        choices=OPERACION_CHOICES,
        label="Operación",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    vendedor = forms.ModelChoiceField(
        queryset=Vendedores.objects.all(),
        label="Vendedor",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    choice_op = (("", "Todos"),
                 ("IMPORTACION", "IMPORTACION"),
                 ("EXPORTACION", "EXPORTACION"),
                 ("IMPORTACION LCL", "IMPORTACION LCL"),
                 ("IMPORTACION FCL", "IMPORTACION FCL"),
                 ("IMPORTACION PART CONT.", "IMPORTACION PART CONT."),
                 ("TRANSITO FCL", "TRANSITO FCL"),
                 ("IMPORTACION CONSOLIDADA", "IMPORTACION CONSOLIDADA"),
                 ("REEMBARCO", "REEMBARCO"),
                 ("TRANSITO", "TRANSITO"),
                 ("TRASLADO", "TRASLADO"),
                 ("MUESTRA", "MUESTRA"),

                 )

    tipo_de_operacion = forms.ChoiceField(
        choices=choice_op,
        label="Tipo de Operación",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )

    origen = forms.ModelChoiceField(
        queryset=Ciudades.objects.all().order_by('nombre'),
        label="Origen",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    destino = forms.ModelChoiceField(
        queryset=Ciudades.objects.all().order_by('nombre'),
        label="Destino",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3 mb-3'}),
    )

    STATUS_CHOICES = (("","Todos"),("ARRIBADO","ARRIBADO"),("CONFIRMADO","CONFIRMADO"),("CANCELADO","CANCELADO"),("RESERVADO","RESERVADO"),("UNIFICADO","UNIFICADO"),("CERRADO","CERRADO"),)
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label="Status",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    # buque = forms.ModelChoiceField(
    #     queryset=Vapores.objects.all(),
    #     label="Buque",
    #     required=False,
    #     widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    # )
    cliente = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        label="Cliente",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    embarcador = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        label="Embarcador",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    consignatario = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        label="Consignatario",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    transportista = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        label="Transportista",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    filtro1 = forms.ChoiceField(
        choices=filtros,
        label="Orden 1",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    filtro2 = forms.ChoiceField(
        choices=filtros,
        label="Orden 2",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    filtro3 = forms.ChoiceField(
        choices=filtros,
        label="Orden 3",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )

class desconsolidacion_form(forms.Form):
    cia = forms.CharField(
        label='Codigo Aerolinea',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    numero_vuelo = forms.CharField(
        label='N° Vuelo',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    llegada = forms.DateField(widget= forms.DateInput(attrs={"type":'date','class': 'form-control',}),label='Llegada',input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],initial=datetime.datetime.now().strftime("%Y-%m-%d"))

class add_servicio_form(forms.Form):
    OPCIONES = [
        ('V', 'Venta'),
        ('C', 'Compra'),
    ]
    OPCIONES_2 = [
        ('S', 'SÍ'),
        ('N', 'NO'),
    ]
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", }),
        label="Nombre")

    contable = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Cuenta", required=False)


    tipo_gasto = forms.ChoiceField(
        choices=OPCIONES,
        widget=forms.Select(attrs={'class': 'form-control'}),label='Tipo Servicio'
    )
    imputable = forms.ChoiceField(
        choices=OPCIONES_2,
        widget=forms.Select(attrs={'class': 'form-control'}),label='Imputable a Embarques'
    )

    tasa = forms.ChoiceField(
        choices=[
            ('B', 'Básico'),
            ('X', 'Exento'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="IVA"
    )
    nombreingles = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", }),
        label="Inglés")

    activa = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label="Servicio activo")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contable'].choices = [('', 'Seleccione una cuenta')] + [(c.xcodigo, c.xnombre) for c in Cuentas.objects.all()]

class edit_servicio_form(forms.Form):
    OPCIONES = [
        ('V', 'Venta'),
        ('C', 'Compra'),
    ]
    OPCIONES_2 = [
        ('S', 'SÍ'),
        ('N', 'NO'),
    ]

    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", }),
        label="Nombre")

    contable = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Cuenta", required=False)

    tipo_gasto = forms.ChoiceField(
        choices=OPCIONES,
        widget=forms.Select(attrs={'class': 'form-control'}), label='Tipo Servicio'
    )
    imputable = forms.ChoiceField(
        choices=OPCIONES_2,
        widget=forms.Select(attrs={'class': 'form-control'}),label='Imputable a Embarques'
    )
    tasa = forms.ChoiceField(
        choices=[
            ('B', 'Básico'),
            ('X', 'Exento'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="IVA"
    )
    nombreingles = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "autocomplete": "off", }),
        label="Inglés")

    activa = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                label="Servicio activo")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contable'].choices = [('', 'Seleccione una cuenta')] + [(c.xcodigo, c.xnombre) for c in
                                                                             Cuentas.objects.all()]