
from bootstrap_modal_forms.forms import BSModalModelForm
from mantenimientos.models import Clientes, Monedas, Depositos, Servicios
from seguimientos.models import Seguimiento, VGrillaSeguimientos, Envases, Cargaaerea, Serviceaereo, Attachhijo, \
    Conexaerea, Faxes
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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


class pdfForm(BSModalModelForm):
    class Meta:
        model = Seguimiento
        fields = ['observaciones',]  # Agrega los campos que deseas actualizar

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))

    observaciones = forms.CharField(widget=forms.Textarea(attrs={"id": 'pdf_add_input', "autocomplete": "off", 'required': False, 'max_length': 500, "rows": "25"," cols": "100", "class": "form-control"}, ), required=False, label="Notas", max_length=500)


class seguimientoForm(BSModalModelForm):
    class Meta:
        model = Seguimiento
        fields = ['cliente',
                  'embarcador',
                  'consignatario',
                  'notificar',
                  'agente',
                  'transportista',
                  'armador',
                  'agecompras',
                  'ageventas',
                  'origen',
                  'destino',
                  'status',
                  'moneda',
                  'loading',
                  'discharge',
                  'posicion',
                  'pago',
                  'vendedor',
                  'deposito',
                  'vapor',
                  'viaje',
                  'awb',
                  'hawb',
                  'operacion',
                  'arbitraje',
                  'ubicacion',
                  'booking',
                  'trackid',
                  'proyecto',
                  'actividad',
                  'demora',
                  'diasalmacenaje',
                  'wreceipt',
                  'valor',
                  'modo',
                  'terminos',
                  'fecha',
                  'vencimiento',
                  'loadingdate',
                  'tomopeso',
                  'despachante',
                  'volumen',
                  'iniciales',
                  'recepcionado',
                  'tarifafija',
                  'multimodal',
                  'unidadpeso',
                  'unidadvolumen',
                  'tipobonifcli',
                  'editado',
                  'observaciones',
                  'contratotra',

                  ]  # Agrega los campos que deseas actualizar
        labels = {
            'awb': 'Master',
            'hawb': 'House',
            'wreceipt': 'WR',
            'Trackid': 'Track ID',
            'pago': 'Pago flete',
            'diasalmacenaje': 'Dias de almacenaje',
            'demora': 'Dias de demora',
            'contratotra': 'Contrato transport.',
        }
        MODOS_CHOICES = [
            ('IMPORT MARITIMO', 'IMPORT MARÍTIMO'),
            ('EXPORT MARITIMO', 'EXPORT MARÍTIMO'),
            ('IMPORT AEREO', 'IMPORT AÉREO'),
            ('EXPORT AEREO', 'EXPORT AÉREO'),
            ('IMPORT TERRESTRE', 'IMPORT TERRESTRE'),
            ('EXPORT TERRESTRE', 'EXPORT TERRESTRE'),
        ]
        widgets = {
            'modo': forms.Select(choices=MODOS_CHOICES, attrs={'class': 'form-control form-control-sm'}),
        }
        attrs = {
            'deposito' : "tabindex=16;",
            'awb' : "tabindex=17;",
            'wreceipt' : "tabindex=18;",
            'status' : "tabindex=19;",
            'operacion' : "tabindex=12;",
        }

        # Asignación de tabindex en el orden que especificaste

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'update-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))
        self.fields['arbitraje'].required = False

        for field_name, field in self.fields.items():
            # Verificar el tipo de widget para no sobreescribir
            if isinstance(field.widget, forms.CheckboxInput):  # Si es un checkbox
                field.widget.attrs['class'] = 'form-check-input'
            else:  # Para otros tipos de campos
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['attr'] = 'data-id'
                field.required = False

            # Configuración específica para el campo 'moneda'
            if field_name == 'moneda':
                monedas = [("", "---")] + list(Monedas.objects.all().order_by('nombre').values_list('codigo', 'nombre'))
                field.choices = monedas

        campos_autocomplete = [
            'cliente', 'despachante', 'embarcador', 'consignatario', 'notificar',
            'agente', 'transportista', 'armador', 'agecompras', 'ageventas',
            'origen', 'destino', 'vendedor', 'deposito', 'vapor',
            'loading', 'discharge'
        ]

        EXCLUIR_VALIDACION_AUTOCOMPLETE = ['vapor']

        for nombre in campos_autocomplete:
            if nombre in self.fields:
                clases_actuales = self.fields[nombre].widget.attrs.get('class', '')

                if nombre not in EXCLUIR_VALIDACION_AUTOCOMPLETE:
                    clases_actuales += ' autocomplete-validable'

                self.fields[nombre].widget.attrs['class'] = clases_actuales.strip()

    def clean_arbitraje(self):
        value = self.cleaned_data.get('arbitraje')
        if not value:
            return 1
        return value

    choice_op = (("", ""),
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

    CHOICE_TERMINOS = (("", ""),
                       ("FOB", "FOB"),
                       ("EXW", "EXW"),
                       ("DDU", "DDU"),
                       ("FCA", "FCA"),
                       ("DDP", "DDP"),
                       ("DAP", "DAP"),
                       ("CIF", "CIF"),
                       ("CFR", "CFR"),
                       ("DAF", "DAF"),
                       ("DAT", "DAT"),
                       ("CPT", "CPT"),
                       ("CIP", "CIP"),
                       )

    # primera columna
    cliente = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'cliente_add'}))
    despachante = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'despachante_add'}))
    observaciones = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'observaciones'}))
    embarcador = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'embarcador_add'}))
    consignatario = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'consignatario_add'}))
    notificar = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'notificar_add'}),label='Notificar a:')
    agente = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'agente_add'}))
    transportista = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'transportista_add'}))
    armador = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'armador_add','required': False}),required=False)
    agecompras = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'agecompras_add',"required":False}),required=False,label='Ag.Compras')
    ageventas = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'ageventas_add',"required":False}),required=False,label='Ag.Ventas')
    refproveedor = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',"required":False}),required=False,label='Ref. Proveedor')
    refcliente = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',"required":False}),required=False,label='Ref. Cliente')
    # segunda columna
    deposito = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required': False,'id':'deposito_add'}),required=False)
    origen = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'origen_add'}))
    destino = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'destino_add'}))
    operacion = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete":"off",'required': True,'id':'id_operacion_seg'}),required=True,label="Operacion",choices=choice_op,initial='')
    moneda = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete":"off",'required': True}),required=True,label="Moneda", choices=(),initial='')
    vendedor = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'vendedor_add'}))
    vapor = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required': False,'id':'vapor_add'}),required=False)
    # tercer columna
    loading = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'loading_add', 'required': False}),required=False)
    discharge = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'discharge_add', 'required': False}),required=False)
    proyecto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'proyecto_add', 'required': False}),required=False)
    trafico = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_trafico_seg', 'required': False}),required=False)
    actividad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'actividad_add', 'required': False}),required=False)
    terminos = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'id': 'terminos', 'required': True}),required=True,choices=CHOICE_TERMINOS)
    # observaciones = forms.CharField(widget=forms.Textarea(attrs={"id": 'notas_seguimiento',"autocomplete": "off", 'required': False, 'max_length': 500,"rows":"5"," cols":"10","class":"form-control"}, ), required=False,label="Notas", max_length=500)
    id = forms.IntegerField(widget=forms.HiddenInput(attrs={"autocomplete": "off", 'required': False}), required=False, label="ID")
    propia = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'propia', 'required': True}),
        required=True,
        label="Propia"  # Cambia el texto según necesites
    )
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True,
        label="Fecha"
    )
    vencimiento = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True,
        label="Vencimiento"
    )
    loadingdate = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True,
        label="Fecha Loading"
    )
    tomopeso = forms.BooleanField(widget=forms.CheckboxInput(attrs={"autocomplete": "off", 'required': False,"class": "d-none"}), required=False, label="Tomo peso",initial=1)
    iniciales = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'iniciales', 'required': False}),required=False)
    recepcionado = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'recepcionado', 'required': False}),required=False,initial='N')
    tarifafija = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'tarifafija', 'required': False}),required=False,initial='N')
    multimodal = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'multimodal', 'required': False}),required=False,initial='N')
    unidadpeso = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'unidadpeso', 'required': False}),required=False,initial='K')
    unidadvolumen = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'unidadvolumen', 'required': False}),required=False,initial='B')
    tipobonifcli = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'tipobonifcli', 'required': False}),required=False,initial='P')
    editado = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'editado', 'required': False}),required=False)
    volumen = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_volumen_seg', 'required': False}),
        required=False,
        initial=0.00
    )


class cronologiaForm(BSModalModelForm):
    class Meta:
        model = Seguimiento
        fields = [
            'fecha',
            'etd',
            'eta',
            'originales',

        ]  # Agrega los campos que deseas actualizar
        labels = {
            'fecha': 'Activacion del seguimiento',
            'etd': 'ETD',
            'eta': 'ETA',
            'originales': 'Hay documentos originales',
            # 'hawb': 'House',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'id': 'id_fecha_crono', 'tabindex': 1}),
            'etd': forms.DateInput(attrs={'type': 'date', 'tabindex': 2}),
            'eta': forms.DateInput(attrs={'type': 'date', 'tabindex': 3}),
            'originales': forms.Select(attrs={'tabindex': 4}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'cronologia-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class envasesForm(BSModalModelForm):
    class Meta:
        model = Envases
        fields = [
            'id',
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
            'precio': forms.NumberInput(attrs={'min': '0', 'value': '0'}),
            'cantidad': forms.NumberInput(attrs={'min': '0', 'value': '0'}),
            'peso': forms.NumberInput(attrs={'min': '0', 'value': '0'}),
            'volumen': forms.NumberInput(attrs={'min': '0', 'value': '0'}),
            'bultos': forms.NumberInput(attrs={'min': '0', 'value': '0'}),
            'tara': forms.NumberInput(attrs={'min': '0', 'value': '0'}),
            'bonifcli': forms.NumberInput(attrs={'min': '0', 'value': '0'}),
            'profit': forms.NumberInput(attrs={'min': '0', 'value': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'envases-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.required = True

    id = forms.IntegerField(widget=forms.HiddenInput(attrs={"autocomplete": "off", 'required': False,'id':'id_envase_id'}), required=False,label="ID")

class aplicableForm(BSModalModelForm):
    OPCIONES = (
        ('1', 'Bruto'),
        ('2', 'Volumen'),
        ('3', 'Manual'),
    )

    tomopeso = forms.ChoiceField(
        choices=OPCIONES,
        widget=forms.RadioSelect(attrs={
            'onchange': 'return recalculo_embarques();'
        }),
        label='Peso'
    )

    bruto = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control campo-estrecho',
            "autocomplete": "off"
        }),
        max_digits=12, decimal_places=4, required=False, label="Peso"
    )


    class Meta:
        model = Seguimiento
        fields = [
            'aplicable',
            'tarifacompra',
            'tarifaventa',
            'volumen',
            'muestroflete',
        ]
        labels = {
            'aplicable': 'Aplicable',
            'volumen': 'Volumen',
            'muestroflete': 'Flete',
            'tarifaventa': 'Tarifa Venta',
            'tarifacompra': 'Tarifa Compra',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        for field_name, field in self.fields.items():
            if field_name != 'tomopeso':
                field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['id'] = f'id_{field_name}_ap'


class embarquesForm(BSModalModelForm):
    class Meta:
        model = Cargaaerea
        fields = [
            'id',
            'bultos',
            'bruto',
            'medidas',
            'tipo',
            'cbm',
            'mercaderia',
            'materialreceipt',

        ]  # Agrega los campos que deseas actualizar
        labels = {
            'materialreceipt': 'MR',
            'cbm': 'Volumen',
            'bruto': 'Peso bruto',
            'tipo': 'Tipo',
            'mercaderia':'Detalle'
        }
        widgets = {
            # 'id': forms.HiddenInput(attrs={'id':'id_embarque_id',}),
            'tipo': forms.Select(attrs={'id':'id_tipo_embarque',}),
            'mercaderia': forms.Textarea(attrs={'rows':'2',}),
            'bultos': forms.NumberInput(attrs={'id':'id_bultos_embarque','min': '0'}),
            'bruto': forms.NumberInput(attrs={'id':'id_bruto_embarque','min': '0'}),
            'cbm': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'envases-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))
        for field in self.fields:
            if field not in ['tomopeso','tipobonifcli','tarifafija']:
                self.fields[field].widget.attrs['class'] = 'form-control'

    id = forms.IntegerField(widget=forms.HiddenInput(attrs={"autocomplete": "off", 'required': False,'id':'id_embarque_id'}), required=False,label="ID")
    """
    aplicable = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12,'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Aplicable")
    tarifaprofit = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Tarifa informar")
    tarifaventa = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False,'onchange':'return recalculo_embarques();'}, ), max_digits=12,decimal_places=4, required=False, label="Tarifa venta")
    tarifacompra = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Tarifa compra")
    #muestroflete = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Flete")
    #numero = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Numero")
    #volumen = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'id':'volumen','max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Volumen")
    #bonifcli = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="bonifcli")
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
    """

    producto = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

class gastosForm(BSModalModelForm):
    class Meta:
        model = Serviceaereo
        fields = [
            'id',
            'modo',
            'servicio',
            'moneda',
            'tipogasto',
            'arbitraje',
            'detalle',
            'secomparte',
            'pinformar',
            'notomaprofit',
            'socio',
        ]  # Agrega los campos que deseas actualizar
        labels = {
            'pinformar': 'A informar',
            'modo': 'Pago',
            'notomaprofit': 'Excluir del profit share',
            'secomparte' : 'Se comparte',
        }
        widgets = {
            'modo': forms.Select(attrs={'id': 'id_modo_id'}),
            'arbitraje': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'envases-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.required = True
        servicios = [("", "---------"), ] + list(Servicios.objects.all().order_by('nombre').values_list('codigo', 'nombre'))
        self.fields['servicio'].choices = servicios
        monedas = [("", "---------"), ] + list(Monedas.objects.all().order_by('nombre').values_list('codigo', 'nombre'))
        self.fields['moneda'].choices = monedas
        socios = [("0", "---------"), ] + list(Clientes.objects.all().order_by('empresa').values_list('codigo', 'empresa'))
        self.fields['socio'].choices = socios

        self.fields['secomparte'].widget = forms.HiddenInput()
        self.fields['notomaprofit'].widget = forms.HiddenInput()

    CHOICES = [
        ('N','--------'),
        ('C', 'Compra'),
        ('V', 'Venta '),
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
    id = forms.IntegerField(widget=forms.HiddenInput(attrs={"autocomplete": "off", 'required': False,'id':'id_gasto_id'}), required=False,label="ID")
    compra_venta = forms.CharField(widget=forms.Select(choices=CHOICES),label='Tipo movimiento')
    tipogasto = forms.CharField(widget=forms.Select(choices=CHOICES_TG),label='Tipo')
    servicio = forms.ChoiceField(choices=list(), widget=forms.Select(
        attrs={'class': 'form-control', "autocomplete": "off", 'required': True, }), label="Servicio", required=True)
    importe = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4,"required":True,'min': '0'}, ), max_digits=12,decimal_places=4, required=True, label="Importe",initial=0)
    pinformar = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4,"required":True,'min': '0'}, ), max_digits=12,decimal_places=4, required=True, label="A informar",initial=0)
    arbitraje = forms.DecimalField(widget=forms.HiddenInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4,"id":"id_arbitraje_id","required":False,'min': '0'}, ), max_digits=12,decimal_places=4, required=False, label="Arbitraje",initial=0)
    moneda = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off", 'required': True, "tabindex": "13","id":"id_moneda_id"}),
                               required=True, label="Moneda", choices=(), initial='2')
    socio = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off",}),
                             label="Socio comercial", choices=(), initial='0',required=False)


class archivosForm(forms.ModelForm):
    class Meta:
        model = Attachhijo
        fields = ('numero', 'archivo', 'detalle', 'restringido')



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
        ("FAC", "Factura Comercial"),
        ("NDB", "Nota de débito"),
        ("FFT", "Factura flete terrestre"),
        ("CSA", "Certificado Sanitario"),
        ("COR", "Certificado de origen"),
        ("PIC", "Fotos / Imágenes"),
        ("PRE", "Pre-alerta"),
        ("FPR", "Factura Proveedor"),
        ("WHR", "Warehouse Receipt"),
        ("NCA", "N/C Agente"),
        ("BKC", "Booking Confirmation"),
        ("PKL", "Packing list"),
        ("PPQ", "PPQ"),
        ("MST", "Master"),
        ("HUS", "House"),
        ("GRA", "Docs. Generales"),
        ("COM", "Docs. Comerciales"),
        ("IMO", "Documentos IMO"),
        ("MCA", "Manifiesto de Carga"),
        ("CDS", "Certificado de Seguro"),
        ("PUO", "Purchase Order"),
        ("POD", "P.O.D."),
        ("ODP", "Comprobante electronico"),
        ("VAE", "Validacion electronica"),
        ("DAD", "Documento aduanero"),
        ("FAG", "Factura agente"),
        ("CHO", "Canje House"),
        ("SDA", "SDA"),
        ("EDD", "Entrega de documentos"),
        ("CAR", "Carta de reclamo"),
        ("CRF", "Certificacion de fecha"),
        ("OTR", "Otro tipo"),
    )

    prueba = list(choice_detalle).sort(key=lambda x: x[1], reverse=True)
    detalle = forms.ChoiceField(
        widget=forms.Select(attrs={"autocomplete": "off", 'required': True, "tabindex": "12", 'id': 'id_operacion'}),
        required=True, label="Detalle (tipo archivo)", choices=choice_detalle, initial='')


class rutasForm(forms.ModelForm):
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
                  'accion',
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
        self.helper.form_id = 'rutas-form'
        self.helper.form_method = 'post'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    id = forms.IntegerField(widget=forms.HiddenInput(attrs={"autocomplete": "off", 'required': False, 'id': 'id_ruta_id'}), required=False,label="ID")


class clonarForm(forms.Form):
    yes_no_choices = [
        ('SI', 'SI'),
        ('NO', 'NO'),
    ]

    embarques = forms.ChoiceField(
        label='¿Clonar datos de la carga?',
        choices=yes_no_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    envases = forms.ChoiceField(
        label='¿Clonar envases?',
        choices=yes_no_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    gastos = forms.ChoiceField(
        label='¿Clonar gastos?',
        choices=yes_no_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    rutas = forms.ChoiceField(
        label='¿Clonar rutas?',
        choices=yes_no_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    cronologia = forms.ChoiceField(
        label='¿Clonar cronologia?',
        choices=yes_no_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

