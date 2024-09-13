# -*- encoding: utf-8 -*-
from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms

from impomarit.models import Reservas, Embarqueaereo
from mantenimientos.models import Clientes, Vapores, Ciudades, Monedas

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
                    'id': 'posicion_g',
                    'placeholder': 'Pulse sobre el campo para generar'
                }
            ),
        )

    #codigo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 5 },),max_length=5,required=True,label="Código")
    agente = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required':True, 'id': 'agente_add', 'name':'otro'}),
        required=False)
    aduana = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False }),
        required=False)
    awd = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        required=False)
    consignatario = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required':True, 'id': 'consignatario_add', 'name':'otro' }),
        required=False)
    armador = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required':True, 'id': 'armador_add', 'name':'otro'}),
        required=False)
    transportista= forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required':True, 'id': 'transportista_add', 'name':'otro'}),
        required=False)
    vapor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'id': 'vapor_add'}),
        required=False)
    viaje = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 20, 'type': 'number' },),max_length=20,required=True,label="Viaje")
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
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',  # Campo de solo lectura
            'id': 'transportista_i',
            'name': 'transportista_i',
        }),
        required=False
    )
    agente_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'agente_i',
            'name': 'agente_i',
        }),
        required=False
    )
    consignatario_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
            'readonly': 'readonly',
            'id': 'consignatario_i',
            'name': 'consignatario_i',
        }),
        required=False
    )
    armador_i = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:50px; margin-right:2px;',
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
                  'vendedor',
                  'deposito',
                  'vapor',
                  'hawb',
                  'operacion',
                  'arbitraje',
                  'trackid',
                  'wreceipt',


                  ]  # Agrega los campos que deseas actualizar
        labels = {
            'awb': 'Master',
            'hawb': 'House',
            'wreceipt': 'WR',
            'Trackid': 'Track ID',
            'pago': 'Pago flete',
            'diasalmacenaje': 'Dias de almacenaje',
            'demora': 'Dias de demora',
        }
        widgets = {
            # 'cliente': autocomplete.ModelSelect2(url='cliente_autocomplete')

            'modo': forms.HiddenInput(),
        }
        attrs = {
            'deposito' : "tabindex=16;",
            'awb' : "id=id_awbhijo",
            'wreceipt' : "tabindex=18;",
            'status' : "tabindex=19;",
            'operacion' : "tabindex=12;",
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['attr'] = 'data-id'
            if field == 'operacion':
                self.fields[field].widget.attrs['tabindex'] = '12'
            elif field == 'moneda':
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
    cliente = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'cliente_addh','required':True,"tabindex":"1"}))
    house = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'house_addh', "tabindex": "1"}))
    embarcador = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'embarcador_addh',"tabindex":"2", 'required':True}))
    consignatario = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'consignatario_addh',"tabindex":"3", 'required':True}))
    notificar_cliente = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'notificar_cliente',
            'tabindex': '4',
            'type': 'date'
        }),
        label='Notificar Cliente'
    )

    notificar_agente = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'notificar_agente',
            'tabindex': '5',
            'type': 'date'
        }),
        label='Notificar Agente'
    )
    posicion = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'required': True,
                'maxlength': 20,
                'readonly': True,
                'id': 'posicion_gh'
            }
        ),
    )
    agente = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'agente_addh',"tabindex":"5", 'required':True}))
    transportista = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'transportista_addh',"tabindex":"6", 'required':True}))
    armador = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'armador_addh',"tabindex":"7",'required':True}),required=False)
    agecompras = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'agecompras_addh',"required":False,"tabindex":"8"}),required=False,label='Ag.Compras')
    ageventas = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sobrepasar','id':'ageventas_addh',"required":False,"tabindex":"9"}),required=False,label='Ag.Ventas')
    # segunda columna
    viaje = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': True,'max_length': 20, 'type': 'number' },),max_length=20,required=True,label="Viaje")
    deposito = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required': False,'id':'deposito_addh',"tabindex":"19"}),required=False)
    origen = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'origen_addh',"tabindex":"10"}))
    destino = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'destino_addh',"tabindex":"11"}))
    operacion = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete":"off",'required': True,"tabindex":"12",'id':'id_operacion'}),required=True,label="Operacion",choices=choice_op,initial='')
    moneda = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete":"off",'required': True,"tabindex":"13"}),required=True,label="Moneda", choices=(),initial='')
    vendedor = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'vendedor_addh','type': 'number'}))
    vapor = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required': False,'id':'vapor_addh',"tabindex":"15"}),required=False)
    # tercer columna
    demora = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"autocomplete" :"off",'required': False,'max_length': 20, 'type': 'number' },),max_length=20,required=True,label="Días de demora")
    status = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, 'max_length': 1,
               "style": "width:100%;"}, ), required=True, label="Estado", choices=choice_status)
    loading = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'loading_addh', 'required': False, "tabindex": "25"}),required=False)
    discharge = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'discharge_addh', 'required': False, "tabindex": "26"}),required=False)
    trafico = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'trafico_addh', 'required': False, "tabindex": "35"}),required=False)
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


