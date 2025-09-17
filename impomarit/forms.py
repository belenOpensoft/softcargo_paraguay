# -*- encoding: utf-8 -*-
from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms

from impomarit.models import Reservas, Embarqueaereo, Servireserva, Conexaerea, Envases, Cargaaerea, Attachhijo,Faxes
from mantenimientos.models import Clientes, Vapores, Ciudades, Monedas, Servicios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

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
choice_op = (
                 ('','---'),
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


class NotasForm(BSModalModelForm):
    class Meta:
        model = Faxes
        fields = ['fecha', 'notas', 'asunto', 'tipo']

    # Define el ChoiceField para el campo 'tipo'
    tipo = forms.ChoiceField(
        choices=Faxes.TIPO_CHOICES,
        widget=forms.Select(attrs={
            "id": 'id_tipo_notas',
            "class": "form-control"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'update-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))

        # Configuración de widgets personalizados en el __init__
        self.fields['fecha'].widget = forms.DateInput(
            attrs={"type": "date", "class": "form-control", 'id': 'id_fecha_notas'}
        )
        self.fields['notas'].widget = forms.Textarea(
            attrs={
                "id": 'notas_add_input',
                "autocomplete": "off",
                "rows": "5",
                "cols": "100",
                "class": "form-control"
            }
        )
        self.fields['asunto'].widget = forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "max_length": 100
            }
        )

class add_im_form(forms.Form):
    awb_number = forms.CharField(
        label='Número de Master',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el número Master'
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
            'awb',
            'operacion',
            'arbitraje',
        )
    agente = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required':False, 'id': 'agente_add', 'name':'otro'}),
        required=False)
    aduana = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False }),
        required=False)
    awb = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        required=True)
    consignatario = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required':False, 'id': 'consignatario_add', 'name':'otro' }),
        required=False,label='Embarcador')
    armador = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required':False, 'id': 'armador_add', 'name':'otro'}),
        required=False)
    transportista= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required':False, 'id': 'transportista_add', 'name':'otro'}),
        required=False)
    vapor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'vapor_add'}),
        required=False)
    viaje = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': False,'max_length': 20,'id':'id_viaje_master' },),max_length=20,required=False,label="Viaje")
    moneda = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off", 'required': False,"class":'form-control'}),
                     required=True, label="Moneda", choices=((2,'USD'),(3,'EURO'),(1,'PESOS')), initial='')
    fecha = forms.DateField(widget= forms.DateInput(attrs={"type":'date','required': False,"onkeypress":"return tabular(event,this)","class":"form-control mb-3",}),label="Llegada",required=True)

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
    deposito = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'deposito_master_add'}),
        required=False,label="Deposito")
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 1,"style":"width:100%;"},),required=False,label="Estado",choices=choice_status)
    operacion = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 1,"style":"width:100%;"},),required=True,label="Operacion",choices=choice_op)
    pagoflete = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 1,"style":"width:100%;"},),required=True,label="Pago",choices=(("C","Collect"),("P","Prepaid")))
    transportista_i = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',  # Campo de solo lectura
            'id': 'transportista_i',
            'name': 'transportista_i',
        }),
        required=False
    )
    agente_i = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'agente_i',
            'name': 'agente_i',
        }),
        required=False
    )
    consignatario_i = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'consignatario_i',
            'name': 'consignatario_i',
        }),
        required=False, initial=835
    )
    armador_i = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'armador_i',
            'name': 'armador_i',
        }),
        required=False
    )
    deposito_nro = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'deposito_master_nro_add', 'name': 'deposito_master_nro_add','required': False,}), required=False)
    def __init__(self, *args, **kwargs):
       # lista_clientes = Clientes.objects.none()
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['fecha'].required = False
        self.fields['awb'].label = 'Master'
        self.fields['fecha'].label = 'Llegada'
        self.fields['arbitraje'].initial = 0
        self.fields['aduana'].initial = 0
        self.fields['trafico'].initial = 0
        self.fields['cotizacion'].initial = 0
        self.fields['bultosmadre'].initial = 0
        self.fields['kilosmadre'].initial = 0
        self.fields['tarifa'].initial = 0

class edit_form(BSModalModelForm):
    class Meta:
        model = Reservas
        fields = (

        )
    posicion_e = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'required': True,
                    'maxlength': 20,
                    'readonly': True,
                    'id': 'posicion_e',

                }
            ),
        required=True,
    label = "Posición"
        )

    tarifa_e = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}),
        required=False,  # No obligatorio
        label="Tarifa"
    )
    arbitraje_e = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autocomplete': 'off', 'max_length': 20, 'type': 'number'}),
        max_length=20,
        required=False,  # No obligatorio
        label="Arbitraje", initial=0
    )

    kilosmadre_e = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'type': 'number'
        }),
        required=False,
        label="Kilos",
        initial=0,
        decimal_places=2,
        max_digits=10,
    )

    bultosmadre_e = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autocomplete': 'off', 'max_length': 20, 'type': 'number'}),
        max_length=20,
        required=False,  # Obligatorio
        label="Bultos", initial=0
    )
    trafico_e = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autocomplete': 'off', 'max_length': 20, 'type': 'number'}),
        max_length=20,
        required=False,  # No obligatorio
        label="Tráfico",initial=0
    )
    cotizacion_e = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autocomplete': 'off', 'max_length': 20, 'type': 'number'}),
        max_length=20,
        required=False,  # No obligatorio
        label="Cotización",initial=0
    )
    agente_e = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required':False, 'id': 'agente_edit', 'name':'otro'}),
        required=False,label="Agente")
    aduana_e = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False }),
        required=False,label="Aduana")
    awd_e = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        required=False,label="Máster")
    consignatario_e = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required':False, 'id': 'consignatario_edit', 'name':'otro' }),
        required=False,label="Embarcador")
    armador_e = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required':False, 'id': 'armador_edit', 'name':'otro'}),
        required=False,label="Armador")
    transportista_e= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required':False, 'id': 'transportista_edit', 'name':'otro'}),
        required=False,label="Transportista")
    vapor_e = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'vapor_edit'}),
        required=False,label="Vapor")
    viaje_e = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': False,'max_length': 20},),max_length=20,required=False,label="Viaje")
    moneda_e = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off", 'required': False,"class":'form-control'}),
                     required=True, label="Moneda", choices=((1,'PESOS'),(2,'USD'),(3,'EURO')), initial='')
    fecha_e = forms.DateField(widget= forms.DateInput(attrs={"type":'date','required': False,"onkeypress":"return tabular(event,this)","class":"form-control mb-3",}),label="Llegada",required=True)

    origen_e = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'origen_edit'}),
        required=False,label="Orígen")
    destino_e = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'destino_edit'}),
        required=False,label="Destino")
    loading_e = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'loading_edit'}),
        required=False,label="Loading")
    discharge_e = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'discharge_edit'}),
        required=False,label="Discharge")
    deposito = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'deposito_master'}),
        required=False,label="Deposito")
    status_e = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 1,"style":"width:100%;"},),required=True,label="Estado",choices=choice_status)
    operacion_e = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 1,"style":"width:100%;"},),required=True,label="Operacion",choices=choice_op)
    pagoflete_e = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 1,"style":"width:100%;"},),required=True,label="Pago",choices=(("C","Collect"),("P","Prepaid")))
    transportista_ie = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'transportista_ie',
            'name': 'transportista_ie',
        }),
        required=False
    )
    agente_ie = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'agente_ie',
            'name': 'agente_ie',
        }),
        required=False
    )
    consignatario_ie = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'consignatario_ie',
            'name': 'consignatario_ie',
        }),
        required=False
    )
    armador_ie = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'armador_ie',
            'name': 'armador_ie',
        }),
        required=False
    )
    deposito_nro = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'deposito_master_nro', 'name': 'deposito_master_nro','required': False,}), required=False)

    def __init__(self, *args, **kwargs):
       # lista_clientes = Clientes.objects.none()
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['awd_e'].label = 'Master'

class add_house(BSModalModelForm):
    class Meta:
        model = Embarqueaereo
        fields = [
                  'notificar',
                  'origen',
                  'destino',
                  'moneda',
                  'loading',
                  'discharge',
                  'pago',
                  'vapor',
                  'operacion',
                  'arbitraje',
                  'trackid',
                  'wreceipt',


                  ]  # Agrega los campos que deseas actualizar
        labels = {
            'wreceipt': 'WR',
            'Trackid': 'Track ID',
            'pago': 'Pago flete',
            'diasalmacenaje': 'Dias de almacenaje',
            'demora': 'Dias de demora',
        }
        widgets = {
            # 'cliente': autocomplete.ModelSelect2(url='cliente_autocomplete')
            'pago': forms.NumberInput(attrs={'id': 'pago_house'}),
            'arbitraje': forms.NumberInput(attrs={'id': 'arbitraje_house'}),
            'modo': forms.HiddenInput(),
        }




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['attr'] = 'data-id'
            if field == 'moneda':
                monedas = [("","---"),] + list(Monedas.objects.all().order_by('nombre').values_list('codigo','nombre'))
                self.fields[field].choices = monedas



    choice_op = (("", "---"),
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
    # primer columna
    awb = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'id_awbhijo'}),label='Master')
    cliente = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'cliente_addh','required':True}))
    house = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'house_addh',}))
    embarcador = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'embarcador_addh', 'required':False}))
    vendedor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sobrepasar', 'id': 'vendedor_addh', 'required': False}), required=False, label='Vendedor')
    consignatario = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'consignatario_addh','required':False}))
    notificar_cliente = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'notificar_cliente',
            'type': 'date','required':False
        }),
        label='Notificar Cliente'
    )

    notificar_agente = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'notificar_agente',
            'type': 'date','required':False
        }),
        label='Notificar Agente'
    )
    fecha_embarque = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'fecha_embarque',
            'type': 'date','required':False
        }),
        label='Fecha Embarque'
    )

    fecha_retiro = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'fecha_retiro',
            'type': 'date','required':False
        }),
        label='Fecha Retiro'
    )
    posicion_h = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'required': True,
                'name':'posicion_h',
                'maxlength': 20,
                'readonly': True,
                'id': 'posicion_gh'
            }
        ),
        label='Posición'

    )
    agente = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'agente_addh', 'required':False}))
    transportista = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'transportista_addh', 'required':False}))
    armador = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'armador_addh','required':False}),required=False)
    agecompras = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'agecompras_addh',"required":False}),required=False,label='Ag.Compras')
    ageventas = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'ageventas_addh',"required":False}),required=False,label='Ag.Ventas')
    # segunda columna
    viaje = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': False,'max_length': 20,'id':'viaje_house' },),max_length=20,required=True,label="Viaje")
    origen = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'origen_addh'}))
    destino = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'destino_addh'}))
    operacion = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete":"off",'required': False,'id':'id_operacion'}),required=False,label="Operacion",choices=choice_op,initial='')
    moneda = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete":"off",'required': True,}),required=True,label="Moneda", choices=(),initial='')
    vapor = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required': False,'id':'vapor_addh',}),required=False)
    # tercer columna
    demora = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': False,'max_length': 20, 'type': 'number','id':'dias_demora' },),max_length=20,required=True,label="Días de demora",initial=0)
    status_h = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 1,
               "style": "width:100%;", 'name':'status_h'}, ), required=True, label="Estado", choices=choice_status)
    loading = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'loading_addh', 'required': False, }),required=False)
    discharge = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'discharge_addh', 'required': False,}),required=False)
    trafico = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'trafico_addh', 'required': False,}),required=False,initial=0)
    # observaciones = forms.CharField(widget=forms.Textarea(attrs={"id": 'notas_seguimiento',"autocomplete": "off", 'required': False, 'max_length': 500,"rows":"5"," cols":"10","class":"form-control"}, ), required=False,label="Notas", max_length=500)
    id = forms.IntegerField(widget=forms.HiddenInput(attrs={"autocomplete":"off",'required': False}),required=False,label="ID")

    #inputs
    transportista_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',  # Campo de solo lectura
            'id': 'transportista_ih',
            'name': 'transportista_ih',
        }),
        required=False
    )
    vendedor_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',  # Campo de solo lectura
            'id': 'vendedor_ih',
            'name': 'vendedor_ih',
        }),
        required=False
    )
    agente_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width: 50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'agente_ih',
            'name': 'agente_ih',
        }),
        required=False
    )
    consignatario_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'consignatario_ih',
            'name': 'consignatario_ih',
        }),
        required=False
    )
    armador_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'armador_ih',
            'name': 'armador_ih',
        }),
        required=False
    )
    cliente_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'cliente_ih',
            'name': 'cliente_ih',
        }),
        required=False
    )
    agventas_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'agventas_ih',
            'name': 'agventas_ih',
        }),
        required=False
    )
    agcompras_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'agcompras_ih',
            'name': 'agcompras_ih',
        }),
        required=False
    )
    embarcador_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'embarcador_ih',
            'name': 'embarcador_ih',
        }),
        required=False
    )
    deposito_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'deposito_ih',
            'name': 'deposito_ih',
        }),
        required=False
    )

class edit_house(BSModalModelForm):
    class Meta:
        model = Embarqueaereo
        fields = [
            'notificar',
            'origen',
            'destino',
            'moneda',
            'loading',
            'discharge',
            'vapor',
            'operacion',
            'arbitraje',
            'wreceipt',
        ]

        labels = {
            'wreceipt': 'WR',
            'pago': 'Pago flete',
            'diasalmacenaje': 'Dias de almacenaje',
            'demora': 'Dias de demora',
        }

        widgets = {
            'pago': forms.NumberInput(attrs={'id': 'pago_house_e'}),
            'arbitraje': forms.NumberInput(attrs={'id': 'arbitraje_house_e'}),
            'wreceipt': forms.TextInput(attrs={'id': 'wreceipt_he'}),
            'operacion': forms.TextInput(attrs={'id': 'operacion_he'}),
            'modo': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['attr'] = 'data-id'
            if field == 'moneda':
                monedas = [("", "---"), ] + list(
                    Monedas.objects.all().order_by('nombre').values_list('codigo', 'nombre'))
                self.fields[field].choices = monedas

    choice_op = (("", "---"),
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

    # primer columna
    pago = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 1,"style":"width:100%;"},),required=True,label="Pago",choices=(("","-------"),("C","Collect"),("P","Prepaid")))

    awb = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_awbhijo_e'}), label='Master')
    cliente = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'cliente_addh_e', 'required': False}), required=False)
    house = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'house_addh_e', 'required': False}),
        required=False)
    embarcador = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'embarcador_addh_e', 'required': False}), required=False)
    vendedor = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'vendedor_addh_e', 'required': False}), required=False,
                               label='Vendedor')
    consignatario = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'consignatario_addh_e', 'required': False}), required=False)
    notificar_cliente = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'notificar_cliente_e', 'type': 'date'}),
        label='Notificar Cliente', required=False)
    notificar_agente = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'notificar_agente_e', 'type': 'date'}),
        label='Notificar Agente', required=False)
    etd = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'etd_e', 'type': 'date'}),
        label='ETD', required=False)
    eta = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'eta_e', 'type': 'date'}),
        label='ETA', required=False)
    posicion_h = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'required': True, 'name': 'posicion_h', 'maxlength': 20,
               'readonly': True, 'id': 'posicion_gh_e'}),
        label='Posición'
    )

    agente = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'agente_addh_e', 'required': False}))
    transportista = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'transportista_addh_e', 'required': False}))
    armador = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'armador_addh_e', 'required': False}), required=False)
    agecompras = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'agecompras_addh_e', 'required': False}), required=False,
                                 label='Ag.Compras')
    ageventas = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'ageventas_addh_e', 'required': False}), required=False,
                                label='Ag.Ventas')

    # segunda columna
    viaje = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'maxlength': 20,
               'id': 'viaje_house_e'}), max_length=20, required=False, label="Viaje")
    origen = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'origen_addh_e'}))
    destino = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'destino_addh_e'}))
    operacion = forms.ChoiceField(
        widget=forms.Select(attrs={"autocomplete": "off", 'required': False, 'id': 'operacion_editar'}), required=False,
        label="Operacion", choices=choice_op, initial='')
    moneda = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off", 'required': False, 'id': 'moneda_e'}),
                               required=False, label="Moneda", choices=(), initial='')
    vapor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'vapor_addh_e'}),
        required=False)

    # tercer columna
    demora = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'maxlength': 20, 'type': 'number',
               'id': 'dias_demora_e'}), max_length=20, required=False, label="Días de demora",initial=0)
    status_h = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'maxlength': 1, "style": "width:100%;",
               'name': 'status_h_e','id':'status_h_e'}), required=False, label="Estado", choices=choice_status)
    loading = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'loading_addh_e', 'required': False}),
        required=False)
    discharge = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'discharge_addh_e', 'required': False}),
        required=False)
    trafico = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'trafico_addh_e', 'required': False}),
        required=False,initial=0)

    # inputs
    transportista_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'transportista_ih_e', 'name': 'transportista_ih'}), required=False)
    vendedor_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'vendedor_ih_e', 'name': 'vendedor_ih'}), required=False)
    agente_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width: 50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'agente_ih_e', 'name': 'agente_ih'}), required=False)
    consignatario_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'consignatario_ih_e', 'name': 'consignatario_ih'}), required=False)
    armador_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'armador_ih_e', 'name': 'armador_ih'}), required=False)
    cliente_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'cliente_ih_e', 'name': 'cliente_ih'}), required=False)
    agventas_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'agventas_ih_e', 'name': 'agventas_ih'}), required=False)
    agcompras_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'agcompras_ih_e', 'name': 'agcompras_ih'}), required=False)
    embarcador_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'embarcador_ih_e', 'name': 'embarcador_ih'}), required=False)

class edit_house_general(BSModalModelForm):
    class Meta:
        model = Embarqueaereo
        fields = [
            'notificar',
            'origen',
            'destino',
            'moneda',
            'loading',
            'discharge',
            'vapor',
            'operacion',
            'arbitraje',
            'wreceipt',
        ]

        labels = {
            'wreceipt': 'WR',
            'pago': 'Pago flete',
            'diasalmacenaje': 'Dias de almacenaje',
            'demora': 'Dias de demora',
        }

        widgets = {
            'pago': forms.NumberInput(attrs={'id': 'pago_house_e'}),
            'arbitraje': forms.NumberInput(attrs={'id': 'arbitraje_house_e'}),
            'wreceipt': forms.TextInput(attrs={'id': 'wreceipt_he'}),
            'operacion': forms.TextInput(attrs={'id': 'operacion_he'}),
            'modo': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # Asignar clase por defecto si no está
            field.widget.attrs.setdefault('class', 'form-control')

            # Agregar prefijo "_general" al id
            if 'id' in field.widget.attrs:
                field.widget.attrs['id'] = field.widget.attrs['id'] + '_general'
            else:
                field.widget.attrs['id'] = field_name + '_general'

            # Asignar atributo 'attr' personalizado si querés mantenerlo
            field.widget.attrs['attr'] = 'data-id'

        # Cargar choices de moneda (como ya hacías)
        if 'moneda' in self.fields:
            monedas = [("", "---")] + list(Monedas.objects.all().order_by('nombre').values_list('codigo', 'nombre'))
            self.fields['moneda'].choices = monedas

    choice_op = (("", "---"),
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

    # primer columna
    pago = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'max_length': 1,"style":"width:100%;"},),required=True,label="Pago",choices=(("","-------"),("C","Collect"),("P","Prepaid")))

    awb = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_awbhijo_e'}), label='Master')
    cliente = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'cliente_addh_e', 'required': False}), required=False)
    house = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'house_addh_e', 'required': False}),
        required=False)
    embarcador = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'embarcador_addh_e', 'required': False}), required=False)
    vendedor = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'vendedor_addh_e', 'required': False}), required=False,
                               label='Vendedor')
    consignatario = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'consignatario_addh_e', 'required': False}), required=False)
    notificar_cliente = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'notificar_cliente_e', 'type': 'date'}),
        label='Notificar Cliente', required=False)
    notificar_agente = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'notificar_agente_e', 'type': 'date'}),
        label='Notificar Agente', required=False)
    etd = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'etd_e', 'type': 'date'}),
        label='ETD', required=False)
    eta = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'id': 'eta_e', 'type': 'date'}),
        label='ETA', required=False)
    posicion_h = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'required': True, 'name': 'posicion_h', 'maxlength': 20,
               'readonly': True, 'id': 'posicion_gh_e'}),
        label='Posición'
    )

    agente = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'agente_addh_e', 'required': False}))
    transportista = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'transportista_addh_e', 'required': False}))
    armador = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'armador_addh_e', 'required': False}), required=False)
    agecompras = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'agecompras_addh_e', 'required': False}), required=False,
                                 label='Ag.Compras')
    ageventas = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-sobrepasar', 'id': 'ageventas_addh_e', 'required': False}), required=False,
                                label='Ag.Ventas')

    # segunda columna
    viaje = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'maxlength': 20,
               'id': 'viaje_house_e'}), max_length=20, required=False, label="Viaje")
    origen = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'origen_addh_e'}))
    destino = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'destino_addh_e'}))
    operacion = forms.ChoiceField(
        widget=forms.Select(attrs={"autocomplete": "off", 'required': False, 'id': 'operacion_editar'}), required=False,
        label="Operacion", choices=choice_op, initial='')
    moneda = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off", 'required': False, 'id': 'moneda_e'}),
                               required=False, label="Moneda", choices=(), initial='')
    vapor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'vapor_addh_e'}),
        required=False)

    # tercer columna
    demora = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'maxlength': 20, 'type': 'number',
               'id': 'dias_demora_e'}), max_length=20, required=False, label="Días de demora",initial=0)
    status_h = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': False, 'maxlength': 1, "style": "width:100%;",
               'name': 'status_h_e','id':'status_h_e'}), required=False, label="Estado", choices=choice_status)
    loading = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'loading_addh_e', 'required': False}),
        required=False)
    discharge = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'discharge_addh_e', 'required': False}),
        required=False)
    trafico = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'trafico_addh_e', 'required': False}),
        required=False,initial=0)

    # inputs
    transportista_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'transportista_ih_e', 'name': 'transportista_ih'}), required=False)
    vendedor_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'vendedor_ih_e', 'name': 'vendedor_ih'}), required=False)
    agente_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width: 50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'agente_ih_e', 'name': 'agente_ih'}), required=False)
    consignatario_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'consignatario_ih_e', 'name': 'consignatario_ih'}), required=False)
    armador_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'armador_ih_e', 'name': 'armador_ih'}), required=False)
    cliente_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'cliente_ih_e', 'name': 'cliente_ih'}), required=False)
    agventas_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'agventas_ih_e', 'name': 'agventas_ih'}), required=False)
    agcompras_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'agcompras_ih_e', 'name': 'agcompras_ih'}), required=False)
    embarcador_i = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'style': 'width:50px; margin-right:2px;', 'readonly': 'readonly',
               'id': 'embarcador_ih_e', 'name': 'embarcador_ih'}), required=False)

class gastosForm(BSModalModelForm):
    class Meta:
        model = Servireserva
        fields = [
            'numero',
            'servicio',
            'moneda',
            'modo',
           # 'costo',
            'detalle',
            'tipogasto',
            'arbitraje',
            'notomaprofit',
            'secomparte',
            'descripcion',
            'precio',
            'prorrateo',
            'empresa',
            'reembolsable',
            'socio',
        ]
        # Agrega los campos que deseas actualizar
        labels = {
            'modo': 'Pago',
            'notomaprofit': 'Excluir del profit share',
            'secomparte' : 'Se comparte',
        }
        #widgets = {
        #   'modo': forms.Select(attrs={'id': 'id_modo_id'}),
        #}
        widgets = {
            'arbitraje': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
            'costo': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'envases-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        servicios = [("", "---------"), ] + list(Servicios.objects.all().order_by('nombre').values_list('codigo', 'nombre'))
        self.fields['servicio'].choices = servicios
        monedas = [("", "---------"), ] + list(Monedas.objects.all().order_by('nombre').values_list('codigo', 'nombre'))
        self.fields['moneda'].choices = monedas
        socios = [("", "---------"), ] + list(Clientes.objects.all().order_by('empresa').values_list('id', 'empresa'))
        self.fields['socio'].choices = socios

    CHOICES = [
        ('C', 'Compra'),
        ('V', 'Venta '),
    ]
    CHOICES_R = [
        ('S', 'Si'),
        ('N', 'No '),
    ]
    CHOICES_P = [
        ('COLLECT', 'COLLECT'),
        ('TODOS', 'TODOS '),
        ('PREPAID', 'PREPAID'),
    ]
    CHOICES_M = [
        ('C', 'COLLECT'),
        ('P', 'PREPAID'),
    ]
    CHOICES_SC = [
        ('S', 'Si'),
        ('N', 'No '),
    ]
    CHOICES_E = [
        ('1', 'Si'),
        ('0', 'No '),
    ]
    CHOICES_TG = [
        ('DUE AGENT', 'DUE AGENT'),
        ('DUE CARRIER', 'DUE CARRIER '),
        ('TAX', 'TAX '),
        ('VALUATION CHARGES', 'VALUATION CHARGES '),
        ('OTHER', 'OTHER '),
        ('LOCAL CHARGES', 'LOCAL CHARGES '),
    ]
    Servicios()
    numero = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'numero_gasto_master',
            'readonly': 'readonly'
        }),
        label='Numero'
    )
    #id = forms.IntegerField(widget=forms.HiddenInput(attrs={"autocomplete": "off", 'required': False,'id':'id_gasto_id'}), required=False,label="ID")
    #compra_venta = forms.CharField(widget=forms.Select(choices=CHOICES),label='Tipo movimiento')
    tipogasto = forms.CharField(widget=forms.Select(choices=CHOICES_TG),label='Tipo')
    reembolsable = forms.CharField(widget=forms.Select(choices=CHOICES_R), label='Reembolsable')
    secomparte = forms.CharField(widget=forms.Select(choices=CHOICES_SC), label='Se comparte')
    prorrateo = forms.CharField(widget=forms.Select(choices=CHOICES_P), label='Prorrateo')
    empresa = forms.CharField(widget=forms.Select(choices=CHOICES_E), label='Empresa')
    modo = forms.CharField(widget=forms.Select(choices=CHOICES_M))
    servicio = forms.ChoiceField(choices=list(), widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, }), label="Servicio", )
    costo = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4,"required":True}, ), max_digits=12,decimal_places=4, required=True, label="Costo")
    arbitraje = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4,"id":"id_arbitraje_id","required":False}, ), max_digits=12,decimal_places=4, label="Arbitraje", initial='0')
    moneda = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off", 'required': True, "tabindex": "13","id":"id_moneda_id",}),
                               required=True, label="Moneda", choices=(), initial='2')
    socio = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off", 'required': True, "tabindex": "13"}),
                                label="Socio comercial", choices=())

class gastosFormHouse(BSModalModelForm):
    class Meta:
        model = Servireserva
        fields = [
            'numero',
            'servicio',
            'moneda',
            'modo',
            'costo',
            'detalle',
            'tipogasto',
            'arbitraje',
            'notomaprofit',
            'secomparte',
            'descripcion',
            'precio',
            'empresa',
            'reembolsable',
            'socio',
        ]
        labels = {
            'modo': 'Pago',
            'notomaprofit': 'Excluir del profit share',
            'secomparte': 'Se comparte',
        }
        widgets = {
            'arbitraje': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
            'precio': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'envases-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))

        # en __init__, dentro del bucle de ocultos
        ocultos_con_id = {
            'numero': 'numero_gasto_house',  # 👈 acá le pongo el id que querés
            'secomparte': 'id_secomparte_h',
            'empresa': 'id_empresa_h',
            'arbitraje': 'id_arbitraje_h',
            'reembolsable': 'id_reembolsable_h',
            'notomaprofit': 'id_notomaprofit_h',
        }
        for campo, el_id in ocultos_con_id.items():
            if campo in self.fields:
                self.fields[campo].widget = forms.HiddenInput(attrs={'id': el_id})

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Actualizando los widgets con el ID correspondiente
        self.fields['servicio'].widget.attrs['id'] = 'id_servicio_h'
        self.fields['moneda'].widget.attrs['id'] = 'id_moneda_h'
        self.fields['modo'].widget.attrs['id'] = 'id_modo_h'
        self.fields['precio'].widget.attrs['id'] = 'id_precio_h'
        self.fields['detalle'].widget.attrs['id'] = 'id_detalle_h'
        self.fields['tipogasto'].widget.attrs['id'] = 'id_tipogasto_h'
        self.fields['arbitraje'].widget.attrs['id'] = 'id_arbitraje_h'
        self.fields['notomaprofit'].widget.attrs['id'] = 'id_notomaprofit_h'
        self.fields['secomparte'].widget.attrs['id'] = 'id_secomparte_h'
        self.fields['descripcion'].widget.attrs['id'] = 'id_descripcion_h'
        self.fields['precio'].widget.attrs['id'] = 'id_precio_h'
        self.fields['empresa'].widget.attrs['id'] = 'id_empresa_h'
        self.fields['reembolsable'].widget.attrs['id'] = 'id_reembolsable_h'
        self.fields['socio'].widget.attrs['id'] = 'id_socio_h'

        # Actualizando las opciones para 'servicio', 'moneda', y 'socio'
        servicios = [("", "---------"), ] + list(Servicios.objects.all().order_by('nombre').values_list('codigo', 'nombre'))
        self.fields['servicio'].choices = servicios

        monedas = [("", "---------"), ] + list(Monedas.objects.all().order_by('nombre').values_list('codigo', 'nombre'))
        self.fields['moneda'].choices = monedas

        socios = [("", "---------"), ] + list(Clientes.objects.all().order_by('empresa').values_list('id', 'empresa'))
        self.fields['socio'].choices = socios


        # 🔹 Inicializar valores por defecto
        self.fields['empresa'].initial = '0'
        self.fields['arbitraje'].initial = 0
        self.fields['reembolsable'].initial = 'N'
        self.fields['secomparte'].initial = 'N'
        self.fields['notomaprofit'].initial = '0'

    CHOICES = [
        ('C', 'Compra'),
        ('V', 'Venta'),
    ]
    CHOICES_R = [
        ('S', 'Si'),
        ('N', 'No'),
    ]
    CHOICES_M = [
        ('C', 'COLLECT'),
        ('P', 'PREPAID'),
    ]
    CHOICES_SC = [
        ('S', 'Si'),
        ('N', 'No'),
    ]
    CHOICES_E = [
        ('1', 'Si'),
        ('0', 'No'),
    ]
    CHOICES_TG = [
        ('DUE AGENT', 'DUE AGENT'),
        ('DUE CARRIER', 'DUE CARRIER'),
        ('TAX', 'TAX'),
        ('VALUATION CHARGES', 'VALUATION CHARGES'),
        ('OTHER', 'OTHER'),
        ('LOCAL CHARGES', 'LOCAL CHARGES'),
    ]

    numero = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'numero_gasto_house',
            'readonly': 'readonly'
        }),
        label='Numero'
    )
    tipogasto = forms.CharField(widget=forms.Select(choices=CHOICES_TG, attrs={'id': 'id_tipogasto_h'}), label='Tipo')
    reembolsable = forms.CharField(widget=forms.Select(choices=CHOICES_R, attrs={'id': 'id_reembolsable_h'}),
                                   label='Reembolsable')
    secomparte = forms.CharField(widget=forms.Select(choices=CHOICES_SC, attrs={'id': 'id_secomparte_h'}),
                                 label='Se comparte')
    empresa = forms.CharField(widget=forms.Select(choices=CHOICES_E, attrs={'id': 'id_empresa_h'}), label='Empresa')
    modo = forms.CharField(widget=forms.Select(choices=CHOICES_M, attrs={'id': 'id_modo_h'}))
    servicio = forms.ChoiceField(choices=list(), widget=forms.Select(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'id_servicio_h'}), label='Servicio')
    precio = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'max_digits': 12, 'decimal_places': 4, 'required': True, 'id': 'id_precio_h'}), max_digits=12, decimal_places=4, label='Precio')
    costo = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'max_digits': 12, 'decimal_places': 4, 'required': True, 'id': 'id_costo_h'}), max_digits=12, decimal_places=4, label='Costo')
    arbitraje = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'max_digits': 12, 'decimal_places': 4, 'id': 'id_arbitraje_h'}), max_digits=12, decimal_places=4, label='Arbitraje', initial='0')
    pinformar = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'max_digits': 12, 'decimal_places': 4, 'id': 'id_pinformar_h'}), max_digits=12, decimal_places=4, label='Informar', initial='0')
    moneda = forms.ChoiceField(widget=forms.Select(attrs={'autocomplete': 'off', 'required': True,  'id': 'id_moneda_h'}), label='Moneda', choices=(), initial='2')
    socio = forms.ChoiceField(widget=forms.Select(attrs={'autocomplete': 'off', 'required': True, 'id': 'id_socio_h'}), label='Socio comercial', choices=())

class rutasFormHouse(forms.ModelForm):
    class Meta:
        model = Conexaerea
        fields = ('origen',
                  'destino',
                  'vapor',
                  'salida',
                  'llegada',
                  'cia',
                  'viaje',
                  'modo',
                  )

        widgets = {
            'salida': forms.DateInput(attrs={'type': 'date'}),
            'llegada': forms.DateInput(attrs={'type': 'date'}),
            'viaje': forms.TextInput(attrs={'id': 'id_viaje_ruta'}),
            'modo': forms.Select(attrs={'id': 'id_modo_ruta'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
#ocultar este campo
    numero = forms.IntegerField(
        widget=forms.TextInput(attrs={"autocomplete": "off", 'required': True, 'id': 'id_ruta_id','readonly': 'readonly',}), required=True,
        label="Numero")

class emailsForm(forms.Form):
    # class Meta:
    #     model = Seguimiento
    #     fields = ['observaciones',]  # Agrega los campos que deseas actualizar

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_id = 'update-form'
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Actualizar'))

    to = forms.EmailField(label='Para',widget=forms.EmailInput(attrs={'class': 'form-control'}))
    cc = forms.EmailField(label='CC',widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False)
    cco = forms.EmailField(label='CCO',widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False)
    subject = forms.CharField(label='Asunto',widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    email = forms.CharField(widget=forms.Textarea(attrs={"id": 'email_add_input',"autocomplete": "off", 'required': False, 'max_length': 500,"rows":"5"," cols":"100","class":"form-control"}, ), required=False,label="Email", max_length=500)

class archivosForm(forms.ModelForm):
    class Meta:
        model = Attachhijo
        fields = ('numero', 'archivo','detalle', 'restringido' )



    def __init__(self, *args, **kwargs):

        super(archivosForm, self).__init__(*args, **kwargs)
        self.fields['detalle'].widget.attrs['class'] = 'form-control'
        self.fields['detalle'].widget.attrs['style'] = 'width:400px'
        self.fields['restringido'].widget.attrs['class'] = 'form-control'
        self.fields['restringido'].widget.attrs['style'] = 'width:400px'
        self.fields['archivo'].widget.attrs['class'] = 'form-control'
        self.fields['archivo'].label = 'Documento'
        self.fields['archivo'].widget.attrs['style'] = 'width:400px'
        self.fields['numero'].widget.attrs['style'] = 'visibility:hidden'
        self.fields['numero'].widget = forms.HiddenInput()

    choice_detalle = (
        ("OTR", "Otro tipo"),
        ("CRF", "Certificacion de fecha"),
        ("CAR", "Carta de reclamo"),
        ("EDD", "Entrega de documentos"),
        ("SDA", "SDA"),
        ("CHO", "Canje House"),
        ("FAG", "Factura agente"),
        ("DAD", "Documento aduanero"),
        ("VAE", "Validacion electronica"),
        ("ODP", "Comprobante electronico"),
        ("PKL", "Packing list"),
    )
    prueba = list(choice_detalle).sort(key = lambda x: x[1], reverse=True)
    detalle = forms.ChoiceField(
        widget=forms.Select(attrs={"autocomplete": "off", 'required': True, "tabindex": "12", 'id': 'id_operacion'}),
        required=True, label="Detalle (tipo archivo)", choices=choice_detalle, initial='')

class envasesFormHouse(BSModalModelForm):
    class Meta:
        model = Envases
        fields = [
            'id',
            'numero',
            'unidad',
            'tipo',
            'precio',
            'movimiento',
            'terminos',
            'nrocontenedor',
            'precio',
            'marcas',
            'precinto',
            'cantidad',
            'bultos',
            'envase',
            'volumen',
            'peso',
            'tara',
            'bonifcli',
            'tara',
            'profit',
        ]  # Agrega los campos que deseas actualizar
        labels = {
            'nrocontenedor': 'Contenedor',
            'bonifcli': 'Bonif',
            'profit': 'A informar',
            'unidad': 'Unid/Vta',
        }
        widgets = {
            # 'id': forms.HiddenInput(attrs={'id':'id_envase_id',}),
             'numero': forms.TextInput(attrs={'id':'numero_envase','readonly':'readonly'}),
            'precio': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
            'cantidad': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
            'peso': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
            'volumen': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
            'bultos': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
            'tara': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
            'bonifcli': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
            'profit': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'envases-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    id = forms.IntegerField(widget=forms.HiddenInput(attrs={"autocomplete": "off", 'required': False,'id':'id_envase_id'}), required=False,label="ID")

class embarquesFormHouse(BSModalModelForm):
    class Meta:
        model = Cargaaerea
        fields = [
            'id',
            'producto',
            'bultos',
            'bruto',
            'medidas',
            'tipo',
            'cbm',
            'mercaderia',

        ]  # Agrega los campos que deseas actualizar
        labels = {
            'cbm': 'Volumen',
            'bruto': 'Peso bruto',
            'tipo': 'Tipo',
        }
        # widgets = {
        #     'tipo': forms.Select(attrs={'id':'id_tipo_embarque',}),
        #     'mercaderia': forms.Textarea(attrs={'rows':'2',}),
        #     'bultos': forms.NumberInput(attrs={'id':'id_bultos_embarque',}),
        #     'bruto': forms.NumberInput(attrs={'id':'id_bruto_embarque',}),
        # }
        widgets = {
            # 'id': forms.HiddenInput(attrs={'id':'id_embarque_id',}),
            'tipo': forms.Select(attrs={'id':'id_tipo_embarque',}),
            'mercaderia': forms.Textarea(attrs={'rows':'2',}),
            'bultos': forms.NumberInput(attrs={'id':'id_bultos_embarque','min': '0'}),
            'bruto': forms.NumberInput(attrs={'id':'id_bruto_embarque','min': '0'}),
            'cbm': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
        }

    producto = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'envases-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))
        for field in self.fields:
            if field not in ['tomopeso','tipobonifcli','tarifafija']:
                self.fields[field].widget.attrs['class'] = 'form-control'

    numero = forms.IntegerField(widget=forms.TextInput(attrs={"autocomplete": "off", 'id':'numero_embarque', 'readonly':'readonly'}), required=False,label="Número")
    id = forms.IntegerField(widget=forms.HiddenInput(attrs={"autocomplete": "off", 'required': False,'id':'id_embarque_id'}), required=False,label="ID")
    aplicable = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12,'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Aplicable")
    tarifaprofit = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Tarifa informar")
    tarifaventa = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False,'onchange':'return recalculo_embarques();'}, ), max_digits=12,decimal_places=4, required=False, label="Tarifa venta")
    tarifacompra = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Tarifa compra")
    muestroflete = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Flete")
    numero_e = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Numero")
    volumen = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'id':'volumen','max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Volumen")
    bonifcli = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="bonifcli")
    OPCIONES = (
        ('1', 'Bruto'),
        ('2', 'Volumen'),
        ('3', 'Manual'),
    )

    tomopeso = forms.ChoiceField(
        choices=OPCIONES,
        widget=forms.RadioSelect(attrs={'style':'width:50px;','onchange':'return recalculo_embarques();'}),
        label='Peso'
    )
    OPCIONES2 = (
        ('P', 'Porcentual tarifa venta'),
        ('V', 'Monto fijo p/peso aplicable'),
        ('M', 'Monto fijo embarque'),
    )

    tipobonifcli = forms.ChoiceField(
        choices=OPCIONES2,
        widget=forms.RadioSelect(attrs={'style':'width:50px;'}),
    )
    tarifafija = forms.BooleanField(label="Tarifa fija")

class GenerarDocumentoForm(forms.Form):
    OPERATIVAS = [
        ('IM', 'Importación Marítima'),
        ('IA', 'Importación Aérea'),
        ('IT', 'Importación Terrestre'),
    ]

    seguimiento = forms.CharField(
        label='Seguimiento',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de seguimiento'
        })
    )

    operativa = forms.ChoiceField(
        label='Operativa',
        required=False,
        choices=[('', '---------')] + OPERATIVAS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class EntregaDocumentacionForm(forms.Form):
    # Datos generales
    embarcador = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cliente = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    orden = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    rut = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    modo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mbl_awb = forms.CharField(label="MBL / AWB", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    origen = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    destino = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    posicion = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Entregar a
    entregar_a = forms.ChoiceField(
        choices=[('cliente', 'Cliente'), ('despachante', 'Despachante')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    nombre_entrega = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion_entrega = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ciudad_entrega = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono_entrega = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Comentarios
    imprimir_comentarios = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    comentarios = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    # Documentos adjuntos
    documentos_adjuntos = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        choices=[
            ('cert_origen', 'Certificado de origen'),
            ('dec_embarque', 'Declaración de embarque'),
            ('cert_seguro', 'Certificado de seguro'),
            ('factura_comercial', 'Factura comercial'),
            ('nuestras_facturas', 'Nuestras facturas'),
            ('cumplido', 'Cumplido aduanero'),
            ('factura_seguro', 'Factura del seguro'),
            ('crt', 'CRT'),
            ('micdta', 'MIC/DTA'),
            ('papeleta', 'Papeleta'),
            ('documentaria', 'Documentaria'),
            ('parte_recepcion', 'Parte de recepción'),
            ('factura_transporte', 'Factura de transporte'),
            ('otros', 'Otros documentos'),
            ('original_conocimiento', 'Original conocimiento'),
            ('lista_empaque', 'Lista de empaque'),
            ('cert_flete', 'Certificación de flete'),
            ('copia_conocimiento', 'Copia de conocimiento'),
            ('carta_temp', 'Carta temperatura'),
            ('orden_deposito', 'Orden a depósito'),
            ('cert_gastos', 'Certificación de gastos'),
            ('libre_deuda', 'Libre deuda'),
            ('eur1', 'EUR 1'),
            ('cert_calidad', 'Certificado de calidad'),
            ('transferencia', 'Transferencia'),
            ('cert_peligrosa', 'Certificado carga peligrosa')
        ]
    )

