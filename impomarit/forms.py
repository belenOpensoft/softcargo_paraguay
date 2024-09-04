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
choice_op = (("IMPORTACION","IMPORTACION"),
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
                 ("",""),
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
            'posicion',
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
            'transportista',
            'awb',
            'operacion',
            'arbitraje',
        )
    codigo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 5 },),max_length=5,required=True,label="Código")
    agente = forms.ModelChoiceField(
        queryset=None,
        label="Agente",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width:500px'}),
    )
    embarcador = forms.ModelChoiceField(
        queryset=None,
        label="Embarcador",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),
    )
    armador = forms.ModelChoiceField(
        queryset=None,
        label="Armador",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control','tabindex':"-1",'style':'height:60px;'}),
    )
    transportista = forms.ModelChoiceField(
        queryset=None,
        label="Armador",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control','id':'add_armador','tabindex':"-1",'style':'height:60px;width:250px;'}),
    )
    vapor = forms.ModelChoiceField(
        queryset=Vapores.objects.all(),
        label="Vapor",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mb-3',"style":"height:150px;"}),
    )
    viaje = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 20 },),max_length=20,required=True,label="Viaje")
    moneda = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off", 'required': True,"class":'form-control'}),
                     required=True, label="Moneda", choices=((1,'USD'),(2,'EURO'),(3,'PESOS')), initial='')
    fecha = forms.DateField(widget= forms.DateInput(attrs={"type":'date','required': True,"onkeypress":"return tabular(event,this)","class":"form-control mb-3",}),label="Llegada",required=True)

    origen = forms.ModelChoiceField(
        queryset=Ciudades.objects.all().order_by('codigo'),
        label="Origen",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control',"style":"width:100%;"}),
    )
    destino = forms.ModelChoiceField(
        queryset=Ciudades.objects.all().order_by('codigo'),
        label="Destino",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control',"style":"width:100%;"}),
    )
    loading = forms.ModelChoiceField(
            queryset=Ciudades.objects.all().order_by('codigo'),
            label="Loading",
            required=False,
            widget=forms.Select(attrs={'class': 'form-control',"style":"width:100%;"}),
    )
    discharge = forms.ModelChoiceField(
            queryset=Ciudades.objects.all().order_by('codigo'),
            label="Discharge",
            required=False,
            widget=forms.Select(attrs={'class': 'form-control',"style":"width:100%;"}),
    )
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 1,"style":"width:100%;"},),required=True,label="Estado",choices=choice_status)
    operacion = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 1,"style":"width:100%;"},),required=True,label="Operacion",choices=choice_op)
    pagoflete = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 1,"style":"width:100%;"},),required=True,label="Pago",choices=(("Collect","Collect"),("Prepaid","Prepaid")))




    def __init__(self, *args, **kwargs):
        lista_clientes = Clientes.objects.none()
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['awb'].label = 'Master'
        self.fields['fecha'].label = 'Llegada'
        self.fields['awb'].widget.attrs['autocomplete'] = 'off'
        self.fields['transportista'] = forms.ModelChoiceField(queryset=lista_clientes)
        self.fields['embarcador'] = forms.ModelChoiceField(queryset=lista_clientes)
        self.fields['armador'] = forms.ModelChoiceField(queryset=lista_clientes)
        self.fields['agente'] = forms.ModelChoiceField(queryset=lista_clientes)
