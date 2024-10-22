from bootstrap_modal_forms.forms import BSModalModelForm
from mantenimientos.models import Clientes, Monedas, Depositos, Servicios
from seguimientos.models import Seguimiento, VGrillaSeguimientos, Envases, Cargaaerea, Serviceaereo, Attachhijo, \
    Conexaerea
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class notasForm(BSModalModelForm):
    class Meta:
        model = Seguimiento
        fields = ['observaciones',]  # Agrega los campos que deseas actualizar

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'update-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))

    observaciones = forms.CharField(widget=forms.Textarea(attrs={"id": 'notas_add_input',"autocomplete": "off", 'required': False, 'max_length': 500,"rows":"25"," cols":"100","class":"form-control"}, ), required=False,label="Notas", max_length=500)


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
                  'trafico',
                  'proyecto',
                  'actividad',
                  'demora',
                  'diasalmacenaje',
                  'wreceipt',
                  'valor',
                  'modo',
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
            'awb' : "tabindex=17;",
            'wreceipt' : "tabindex=18;",
            'status' : "tabindex=19;",
            'operacion' : "tabindex=12;",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'update-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Actualizar'))
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['attr'] = 'data-id'
            if field == 'operacion':
                self.fields[field].widget.attrs['tabindex'] = '12'
            elif field == 'moneda':
                monedas = [("","---"),] + list(Monedas.objects.all().order_by('nombre').values_list('codigo','nombre'))
                self.fields[field].choices = monedas
            elif field == 'deposito':
                self.fields[field].widget.attrs['tabindex'] = '19'
            elif field == 'awb':
                self.fields[field].widget.attrs['tabindex'] = '20'
            elif field == 'hawb':
                self.fields[field].widget.attrs['tabindex'] = '21'
            elif field == 'wreceipt':
                self.fields[field].widget.attrs['tabindex'] = '22'
            elif field == 'valor':
                self.fields[field].widget.attrs['tabindex'] = '23'
            elif field == 'status':
                self.fields[field].widget.attrs['tabindex'] = '24'
            elif field == 'loading':
                self.fields[field].widget.attrs['tabindex'] = '25'
            elif field == 'Discharge':
                self.fields[field].widget.attrs['tabindex'] = '26'
            elif field == 'posicion':
                self.fields[field].widget.attrs['tabindex'] = '27'
            elif field == 'artibtraje':
                self.fields[field].widget.attrs['tabindex'] = '28'
            elif field == 'pago':
                self.fields[field].widget.attrs['tabindex'] = '29'
            elif field == 'viaje':
                self.fields[field].widget.attrs['tabindex'] = '30'
            elif field == 'ubicacion':
                self.fields[field].widget.attrs['tabindex'] = '31'
            elif field == 'booking':
                self.fields[field].widget.attrs['tabindex'] = '32'
            elif field == 'trackid':
                self.fields[field].widget.attrs['tabindex'] = '33'
            elif field == 'proyecto':
                self.fields[field].widget.attrs['tabindex'] = '34'
            elif field == 'trafico':
                self.fields[field].widget.attrs['tabindex'] = '35'
            elif field == 'actividad':
                self.fields[field].widget.attrs['tabindex'] = '36'
            elif field == 'demora':
                self.fields[field].widget.attrs['tabindex'] = '37'
            elif field == 'diasalmacenaje':
                self.fields[field].widget.attrs['tabindex'] = '38'

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
    # primer columna
    cliente = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'cliente_add',"tabindex":"1"}))
    embarcador = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'embarcador_add',"tabindex":"2"}))
    consignatario = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'consignatario_add',"tabindex":"3"}))
    notificar = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'notificar_add',"tabindex":"4"}),label='Notificar a:')
    agente = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'agente_add',"tabindex":"5"}))
    transportista = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'transportista_add',"tabindex":"6"}))
    armador = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'armador_add',"tabindex":"7",'required': False}),required=False)
    agecompras = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'agecompras_add',"required":False,"tabindex":"8"}),required=False,label='Ag.Compras')
    ageventas = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'ageventas_add',"required":False,"tabindex":"9"}),required=False,label='Ag.Ventas')
    # segunda columna
    deposito = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required': False,'id':'deposito_add',"tabindex":"19"}),required=False)
    origen = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'origen_add',"tabindex":"10"}))
    destino = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'destino_add',"tabindex":"11"}))
    operacion = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete":"off",'required': True,"tabindex":"12",'id':'id_operacion'}),required=True,label="Operacion",choices=choice_op,initial='')
    moneda = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete":"off",'required': True,"tabindex":"13"}),required=True,label="Moneda", choices=(),initial='')
    vendedor = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'vendedor_add',"tabindex":"14"}))
    vapor = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required': False,'id':'vapor_add',"tabindex":"15"}),required=False)
    # tercer columna
    loading = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'loading_add', 'required': False, "tabindex": "25"}),required=False)
    discharge = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'discharge_add', 'required': False, "tabindex": "26"}),required=False)
    proyecto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'proyecto_add', 'required': False, "tabindex": "34"}),required=False)
    trafico = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'trafico_add', 'required': False, "tabindex": "35"}),required=False)
    actividad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'actividad_add', 'required': False, "tabindex": "36"}),required=False)
    # observaciones = forms.CharField(widget=forms.Textarea(attrs={"id": 'notas_seguimiento',"autocomplete": "off", 'required': False, 'max_length': 500,"rows":"5"," cols":"10","class":"form-control"}, ), required=False,label="Notas", max_length=500)
    id = forms.IntegerField(widget=forms.HiddenInput(attrs={"autocomplete":"off",'required': False}),required=False,label="ID")


class cronologiaForm(BSModalModelForm):
    class Meta:
        model = Seguimiento
        fields = [
            'fecha',
            'estimadorecepcion',
            'recepcion',
            'fecemision',
            'fecseguro',
            'fecdocage',
            'loadingdate',
            'arriboreal',
            'fecaduana',
            'pagoenfirme',
            'vencimiento',
            'etd',
            'eta',
            'fechaonhand',
            'fecrecdoc',
            'recepcionprealert',
            'lugar',
            'nroseguro',
            'bltipo',
            'manifiesto',
            'credito',
            'prima',
            'originales',
            'observaciones',

        ]  # Agrega los campos que deseas actualizar
        labels = {
            'fecha': 'Activacion del seguimiento',
            'estimadorecepcion': 'Entrega mercaderia proveedor',
            'recepcion': 'Recepcion efectiva de mercaderia',
            'fecemision': 'Emision conocimiento',
            'fecseguro': 'Seguro',
            'fecdocage': 'Envio de documentos',
            'loadingdate': 'Fecha de carga',
            'arriboreal': 'Arribo real',
            'fecaduana': 'Ingreso DNA',
            'pagoenfirme': 'Pago en firme',
            'fechaonhand': 'On Hand',
            'fecrecdoc': 'Recepcion de documentos',
            'recepcionprealert': 'Recepcion prealert',
            'lugar': 'Recepcionado en',
            'nroseguro': 'N° seguro',
            'bltipo': 'B/L tipo',
            'prima': 'Prima USD',
            'etd': 'ETD',
            'eta': 'ETA',
            'observaciones': 'Notas',
            'originales': 'Hay documentos originales',
            # 'hawb': 'House',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'estimadorecepcion': forms.DateInput(attrs={'type': 'date'}),
            'recepcion': forms.DateInput(attrs={'type': 'date'}),
            'fecemision': forms.DateInput(attrs={'type': 'date'}),
            'fecseguro': forms.DateInput(attrs={'type': 'date'}),
            'fecdocage': forms.DateInput(attrs={'type': 'date'}),
            'loadingdate': forms.DateInput(attrs={'type': 'date'}),
            'arriboreal': forms.DateInput(attrs={'type': 'date'}),
            'fecaduana': forms.DateInput(attrs={'type': 'date'}),
            'pagoenfirme': forms.DateInput(attrs={'type': 'date'}),
            'vencimiento': forms.DateInput(attrs={'type': 'date'}),
            'etd': forms.DateInput(attrs={'type': 'date'}),
            'eta': forms.DateInput(attrs={'type': 'date'}),
            'fechaonhand': forms.DateInput(attrs={'type': 'date'}),
            'fecrecdoc': forms.DateInput(attrs={'type': 'date'}),
            'recepcionprealert': forms.DateInput(attrs={'type': 'date'}),
            'originales': forms.Select(attrs={'type': 'date'})
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
            self.fields[field].widget.required = True

    id = forms.IntegerField(widget=forms.HiddenInput(attrs={"autocomplete": "off", 'required': False,'id':'id_envase_id'}), required=False,label="ID")


class embarquesForm(BSModalModelForm):
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
            'materialreceipt',

        ]  # Agrega los campos que deseas actualizar
        labels = {
            'materialreceipt': 'MR',
            'cbm': 'Volumen',
            'bruto': 'Peso bruto',
            'tipo': 'Tipo',
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
    aplicable = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12,'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Aplicable")
    tarifaprofit = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Tarifa informar")
    tarifaventa = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False,'onchange':'return recalculo_embarques();'}, ), max_digits=12,decimal_places=4, required=False, label="Tarifa venta")
    tarifacompra = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Tarifa compra")
    muestroflete = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Flete")
    numero = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 1,"required":False}, ), max_digits=12,decimal_places=4, required=False, label="Numero")
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
            'pinformar': forms.NumberInput(attrs={'min': '0'}),  # Evita números negativos
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
        socios = [("", "---------"), ] + list(Clientes.objects.all().order_by('empresa').values_list('codigo', 'empresa'))
        self.fields['socio'].choices = socios

    CHOICES = [
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
    importe = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4,"required":True,'min': '0'}, ), max_digits=12,decimal_places=4, required=True, label="Importe")
    arbitraje = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', "autocomplete": "off", 'max_digits': 12, 'decimal_places': 4,"id":"id_arbitraje_id","required":False,'min': '0'}, ), max_digits=12,decimal_places=4, required=False, label="Arbitraje")
    moneda = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off", 'required': True, "tabindex": "13","id":"id_moneda_id"}),
                               required=True, label="Moneda", choices=(), initial='')
    socio = forms.ChoiceField(widget=forms.Select(attrs={"autocomplete": "off", 'required': True, "tabindex": "13"}),
                               required=True, label="Socio comercial", choices=(), initial='')


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
        label='¿Clonar embarques?',
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
    trasbordo = forms.ChoiceField(
        label='¿Clonar trasbordo?',
        choices=yes_no_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
