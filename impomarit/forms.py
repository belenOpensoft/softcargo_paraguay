# -*- encoding: utf-8 -*-
from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms

from impomarit.models import Reservas, Embarqueaereo
from mantenimientos.models import Clientes, Vapores, Ciudades

choice_SINO = (('SI','Si'),('NO','No'))
choice_SN = (('S','Si'),('N','No'))
choice_status = (
    ('','---'),
    ('RESERVADO','RESERVADO'),
    ('CONFIRMADO','CONFIRMADO'),
    ('EN CURSO','EN CURSO'),
    ('ARRIBADO','ARRIBADO'),
    ('CERRADO','CERRADO'),
    ('CANCELADO','CANCELADO'),
    ('ARCHIVADO','ARCHIVADO'),
    ('FINANZAS','FINANZAS'),
    ('PERDIDO','PERDIDO'),
    ('DEMORADO','DEMORADO'),
    ('EN ADUANA','EN ADUANA'),
    ('LIBERADO','LIBERADO'),
    ('EN FRONTERA','EN FRONTERA'),
    ('EN DESCARGA','EN DESCARGA'),
)
choice_op = (('','---'),
    ("IMPORTACION","IMPORTACION"),
                 ("EXPORTACION","EXPORTACION"),
                 ("EXPORTACION FCL","EXPORTACION FCL"),
                 ("IMPORTACION LCL","IMPORTACION LCL"),
                 ("IMPORTACION FCL","IMPORTACION FCL"),
                 ("EXPORTACION CONSOLIDADA","EXPORTACION CONSOLIDADA"),
                 ("IMPORTACION PART CONT.","IMPORTACION PART CONT."),
                 ("TRANSITO FCL","TRANSITO FCL"),
                 ("IMPORTACION CONSOLIDADA","IMPORTACION CONSOLIDADA"),
                 ("REEMBARCO","REEMBARCO"),
                 ("COURIER","COURIER"),
                 ("TRANSITO","TRANSITO"),
                 ("EXPORTACION LCL","EXPORTACION LCL"),
                 ("EXPORTACION PART CONT.","EXPORTACION PART CONT."),
                 ("DUA","DUA"),
                 ("TRASLADO","TRASLADO"),
                 ("MUESTRA","MUESTRA"),
                 )

class add_im_form(forms.Form):
    awb_number = forms.CharField(
        label='Número AWB',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el número AWB'
        })
    )

class add_form(BSModalModelForm):
    class Meta:
        model = Reservas
        fields = (
            'aduana',
            'operacion',
            'kilosmadre',
            'tarifa',
            'bultosmadre',
            'origen',
            'destino',
            'discharge',
            'loading',
            'cotizacion',
            'fecha',
            'status',
            'pagoflete',
            'trafico',
            'aduana',
            'awb',
            'operacion',
            'arbitraje',
        )
    posicion = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'required': True,
                    'maxlength': 20,
                    'readonly': True,
                    'id': 'posicion_g'
                }
            ),
        )

    #codigo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 5 },),max_length=5,required=True,label="Código")
    agente = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'agente_add', 'name':'otro'}),
        required=False)
    aduana = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False }),
        required=False)
    awd = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        required=False)
    consignatario = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required': False, 'id': 'consignatario_add', 'name':'otro' }),
        required=False)
    armador = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required': False, 'id': 'armador_add', 'name':'otro'}),
        required=False)
    transportista= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'transportista_add', 'name':'otro'}),
        required=False)
    vapor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'vapor_add'}),
        required=False)
    viaje = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 20 },),max_length=20,required=True,label="Viaje")
    moneda = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off", 'required': True,"class":'form-control'}),
                     required=True, label="Moneda", choices=((1,'USD'),(2,'EURO'),(3,'PESOS')), initial='')
    fecha = forms.DateField(widget= forms.DateInput(attrs={"type":'date','required': True,"onkeypress":"return tabular(event,this)","class":"form-control mb-3",}),label="Llegada",required=True)

    origen = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'origen_add'}),
        required=False)
    destino = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'destino_add'}),
        required=False)
    loading = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'loading_add'}),
        required=False)
    discharge = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'discharge_add'}),
        required=False)
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 1,"style":"width:100%;"},),required=True,label="Estado",choices=choice_status)
    operacion = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 1,"style":"width:100%;"},),required=True,label="Operacion",choices=choice_op)
    pagoflete = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 1,"style":"width:100%;"},),required=True,label="Pago",choices=(("C","Collect"),("P","Prepaid")))
    transportista_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:5px;',
            'readonly': 'readonly',  # Campo de solo lectura
            'id': 'transportista_i',
            'name': 'transportista_i',
        }),
        required=False
    )
    agente_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:5px;',
            'readonly': 'readonly',
            'id': 'agente_i',
            'name': 'agente_i',
        }),
        required=False
    )
    consignatario_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:5px;',
            'readonly': 'readonly',
            'id': 'consignatario_i',
            'name': 'consignatario_i',
        }),
        required=False
    )
    armador_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:5px;',
            'readonly': 'readonly',
            'id': 'armador_i',
            'name': 'armador_i',
        }),
        required=False
    )




    def __init__(self, *args, **kwargs):
       # lista_clientes = Clientes.objects.none()
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['awb'].label = 'Master'
        self.fields['fecha'].label = 'Llegada'
        #self.fields['awb'].widget.attrs['autocomplete'] = 'off'

