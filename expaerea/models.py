from auditlog.models import AuditlogHistoryField
from django.db import models

from mantenimientos.models import Productos


class ExportAnulados(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'export_anulados'


class ExportAttachhijo(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_attachhijo'


class ExportAttachmadre(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_attachmadre'


class ExportCargaaerea(models.Model):

    choice_tipo = (
        ("", "---------"),
        ("Bags", "Bags"),
        ("Bales", "Bales"),
        ("Big bags", "Big bags"),
        ("Bing", "Bing"),
        ("Boxes", "Boxes"),
        ("Bulk", "Bulk"),
        ("Bundles", "Bundles"),
        ("Cartons", "Cartons"),
        ("Cases", "Cases"),
        ("Container", "Container"),
        ("Crates", "Crates"),
        ("Cylinder", "Cylinder"),
        ("Declared", "Declared"),
        ("Drums", "Drums"),
        ("Envelope", "Envelope"),
        ("Fireboard", "Fireboard"),
        ("Flexitank", "Flexitank"),
        ("Gallons", "Gallons"),
        ("Jumbo", "Jumbo"),
        ("Lot", "Lot"),
        ("Packages", "Packages"),
        ("Pallets", "Pallets"),
        ("Pieces", "Pieces"),
        ("Pipe", "Pipe"),
        ("Platforms", "Platforms"),
        ("Plywood case", "Plywood case"),
        ("Reels", "Reels"),
        ("Rolls", "Rolls"),
        ("Sacks", "Sacks"),
        ("Set", "Set"),
        ("Skids", "Skids"),
        ("Steel Pallets", "Steel Pallets"),
        ("Tank", "Tank"),
        ("Units", "Units"),
        ("Wooden case", "Wooden case"),
        ("Wooden rack", "Wooden rack"),
    )
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    producto = models.ForeignKey(Productos, to_field='codigo', on_delete=models.PROTECT, db_column='producto',related_name='prod_carga_ea')
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True,choices=choice_tipo)
    fechaembarque = models.DateTimeField(blank=True, null=True)
    tarifa = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    aplicable = models.FloatField(blank=True, null=True)
    unidad = models.CharField(db_column='Unidad', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tara = models.FloatField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_cargaaerea'


class ExportClaveguia(models.Model):
    id = models.BigAutoField(primary_key=True)
    awb = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'export_claveguia'


class ExportClavehawb(models.Model):
    id = models.BigAutoField(primary_key=True)
    hawb = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'export_clavehawb'


class ExportClaveposicion(models.Model):
    id = models.BigAutoField(primary_key=True)
    posicion = models.CharField(max_length=15)
    numeroorden = models.SmallIntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_claveposicion'


class ExportConexaerea(models.Model):

    choice_modo = (
        ("MARITIMO", "MARITIMO"),
        ("FLUVIAL", "FLUVIAL"),
        ("TERRESTRE", "TERRESTRE"),
        ("AEREO", "AEREO"),
    )
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vuelo = models.CharField(max_length=30, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    ciavuelo = models.CharField(max_length=3, blank=True, null=True)
    viaje = models.CharField(max_length=10, blank=True, null=True)
    modo = models.CharField(max_length=15,choices=choice_modo)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True, null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_conexaerea'


class ExportConexreserva(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vuelo = models.CharField(max_length=30, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    ciavuelo = models.CharField(max_length=2, blank=True, null=True)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True, null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_conexreserva'


class ExportEmbarqueaereo(models.Model):
    numero = models.IntegerField(primary_key=True)
    cliente = models.IntegerField(blank=True, null=True)
    consignatario = models.IntegerField(blank=True, null=True)
    notificante = models.IntegerField(blank=True, null=True)
    despachante = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    consolidado = models.SmallIntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=20, blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    aduana = models.CharField(max_length=100, blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    pago = models.SmallIntegerField(blank=True, null=True)
    awb = models.CharField(max_length=20, blank=True, null=True)
    hawb = models.CharField(max_length=40, blank=True, null=True)
    transportista = models.IntegerField(blank=True, null=True)
    valortransporte = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valoraduana = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    fechaembarque = models.DateTimeField(blank=True, null=True)
    fecharetiro = models.DateTimeField(blank=True, null=True)
    pagoflete = models.CharField(max_length=1, blank=True, null=True)
    marcas = models.CharField(max_length=100, blank=True, null=True)
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    valorseguro = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tomopeso = models.SmallIntegerField(blank=True, null=True)
    aplicable = models.FloatField(blank=True, null=True)
    tarifaventa = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifacompra = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    volumencubico = models.FloatField(blank=True, null=True)
    cotizacion = models.IntegerField(blank=True, null=True)
    cotitransp = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    aplitransp = models.FloatField(blank=True, null=True)
    facturado = models.CharField(max_length=1, blank=True, null=True)
    profitage = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifafija = models.CharField(max_length=1, blank=True, null=True)
    tipobonifcli = models.CharField(max_length=1, blank=True, null=True)
    bonifcli = models.FloatField(blank=True, null=True)
    over = models.FloatField(blank=True, null=True)
    tipoover = models.CharField(max_length=1, blank=True, null=True)
    comision = models.FloatField(blank=True, null=True)
    tipovend = models.CharField(db_column='Tipovend', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendedor = models.SmallIntegerField(blank=True, null=True)
    comivend = models.FloatField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    reporteada = models.IntegerField(blank=True, null=True)
    nroreferedi = models.IntegerField(blank=True, null=True)
    impresiones = models.SmallIntegerField(blank=True, null=True)
    ordencliente = models.CharField(max_length=850, blank=True, null=True)
    propia = models.IntegerField(blank=True, null=True)
    embarcador = models.IntegerField(blank=True, null=True)
    vaporcli = models.CharField(max_length=1, blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    agente = models.IntegerField(db_column='Agente', blank=True, null=True)  # Field name made lowercase.
    tarifaprofit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=250, blank=True, null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=250, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mercaderia = models.TextField(db_column='Mercaderia', blank=True, null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    datosnotificante = models.CharField(db_column='DatosNotificante', max_length=250, blank=True, null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    arbitrajecass = models.DecimalField(db_column='ArbitrajeCASS', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=250, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)  # Field name made lowercase.
    servicelevel = models.CharField(max_length=20, blank=True, null=True)
    serviceleveltype = models.CharField(max_length=20, blank=True, null=True)
    stthawb = models.CharField(max_length=30, blank=True, null=True)
    sttawb = models.CharField(max_length=30, blank=True, null=True)
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    fechaentrega = models.DateTimeField(db_column='FechaEntrega', blank=True, null=True)  # Field name made lowercase.
    aquienentrega = models.CharField(db_column='aQuienEntrega', max_length=30, blank=True, null=True)  # Field name made lowercase.
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    deposito = models.SmallIntegerField(db_column='Deposito', blank=True, null=True)  # Field name made lowercase.
    autogenfletecpa = models.CharField(db_column='AutogenFleteCPA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    envioiata = models.CharField(db_column='EnvioIATA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    documentos = models.CharField(db_column='Documentos', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.DateTimeField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_embarqueaereo'

    def get_number(self):
        embarque_l = ExportEmbarqueaereo.objects.order_by('numero').last()
        if embarque_l:
            nuevo_numero = embarque_l.numero + 1
        else:
            nuevo_numero = 1

        return nuevo_numero


class ExportEntregadoc(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    entreguese = models.CharField(db_column='Entreguese', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nombreentrega = models.CharField(db_column='NombreEntrega', max_length=50, blank=True, null=True)  # Field name made lowercase.
    direccionentrega = models.CharField(db_column='DireccionEntrega', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ciudadentrega = models.CharField(db_column='CiudadEntrega', max_length=30, blank=True, null=True)  # Field name made lowercase.
    telefonoentrega = models.CharField(db_column='TelefonoEntrega', max_length=30, blank=True, null=True)  # Field name made lowercase.
    original = models.CharField(db_column='Original', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lista = models.CharField(db_column='Lista', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certorigen = models.CharField(db_column='CertOrigen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    declara = models.CharField(db_column='Declara', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certflete = models.CharField(db_column='CertFlete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cerseguro = models.CharField(db_column='CerSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    copiahbl = models.CharField(db_column='CopiaHBL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    otros = models.CharField(db_column='Otros', max_length=1, blank=True, null=True)  # Field name made lowercase.
    detotros = models.CharField(db_column='DetOtros', max_length=50, blank=True, null=True)  # Field name made lowercase.
    detotros2 = models.CharField(db_column='DetOtros2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ordendep = models.CharField(db_column='OrdenDep', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certgastos = models.CharField(db_column='CertGastos', max_length=1, blank=True, null=True)  # Field name made lowercase.
    libre = models.CharField(db_column='Libre', max_length=1, blank=True, null=True)  # Field name made lowercase.
    eur1 = models.CharField(db_column='Eur1', max_length=1, blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(db_column='Factura', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nuestra = models.CharField(db_column='Nuestra', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certcalidad = models.CharField(db_column='CertCalidad', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cumplido = models.CharField(db_column='Cumplido', max_length=1, blank=True, null=True)  # Field name made lowercase.
    transfer = models.CharField(db_column='Transfer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certpeligroso = models.CharField(db_column='CertPeligroso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    imprimecom = models.CharField(db_column='ImprimeCom', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=80, blank=True, null=True)  # Field name made lowercase.
    remarks2 = models.CharField(db_column='Remarks2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    facturacom = models.CharField(db_column='FacturaCom', max_length=40, blank=True, null=True)  # Field name made lowercase.
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', max_length=40, blank=True, null=True)  # Field name made lowercase.
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', max_length=40, blank=True, null=True)  # Field name made lowercase.
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crtnumero = models.CharField(db_column='CRTNumero', max_length=40, blank=True, null=True)  # Field name made lowercase.
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', max_length=40, blank=True, null=True)  # Field name made lowercase.
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    micdtanumero = models.CharField(db_column='MicDtaNumero', max_length=40, blank=True, null=True)  # Field name made lowercase.
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    papeletanumero = models.CharField(db_column='PapeletaNumero', max_length=40, blank=True, null=True)  # Field name made lowercase.
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True, null=True)  # Field name made lowercase.
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', max_length=40, blank=True, null=True)  # Field name made lowercase.
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', max_length=40, blank=True, null=True)  # Field name made lowercase.
    certorigennumero = models.CharField(db_column='CertOrigenNumero', max_length=40, blank=True, null=True)  # Field name made lowercase.
    certseguronumero = models.CharField(db_column='CertSeguroNumero', max_length=40, blank=True, null=True)  # Field name made lowercase.
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', max_length=40, blank=True, null=True)  # Field name made lowercase.
    detotros3 = models.CharField(db_column='DetOtros3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    detotros4 = models.CharField(db_column='DetOtros4', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_entregadoc'



class ExportFaxes(models.Model):
    # Define las opciones de choices
    TIPO_CHOICES = [
        ('CL', 'CLIENTE'),
        ('IN', 'INTERNO'),
        ('FF', 'AGENTE CARGA'),
        ('TR', 'TRANSPORTISTA'),
        ('AV', 'AGENTE VENTAS'),
        ('AC', 'AGENTE COMPRAS'),
        ('TK', 'TRACKING'),
        ('EM', 'EMBARCADOR'),
        ('AD', 'ADUANA'),
        ('DE', 'DESPACHANTE'),

    ]

    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, blank=True, null=True)  # Agrega choices al campo

    class Meta:
        managed = False
        db_table = 'export_faxes'


class ExportGastoshijos(models.Model):
    id = models.BigAutoField(primary_key=True)
    cliente = models.IntegerField(blank=True, null=True)
    codigo = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    statushijos = models.SmallIntegerField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_gastoshijos'


class ExportGuiasgrabadas(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    empresa = models.CharField(max_length=35, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    pais = models.CharField(max_length=22, blank=True, null=True)
    localidad = models.CharField(max_length=22, blank=True, null=True)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    cliente1 = models.CharField(max_length=45, blank=True, null=True)
    cliente2 = models.CharField(max_length=45, blank=True, null=True)
    cliente3 = models.CharField(max_length=45, blank=True, null=True)
    cliente4 = models.CharField(max_length=45, blank=True, null=True)
    consigna = models.CharField(max_length=45, blank=True, null=True)
    direcconsigna = models.CharField(max_length=45, blank=True, null=True)
    localconsigna = models.CharField(max_length=45, blank=True, null=True)
    teleconsigna = models.CharField(max_length=45, blank=True, null=True)
    otralinea = models.CharField(max_length=45, blank=True, null=True)
    empresa2 = models.CharField(max_length=45, blank=True, null=True)
    otracarrier = models.CharField(max_length=45, blank=True, null=True)
    localidad2 = models.CharField(max_length=45, blank=True, null=True)
    otrosdeagente = models.CharField(max_length=45, blank=True, null=True)
    iata = models.CharField(max_length=15, blank=True, null=True)
    salede = models.CharField(max_length=25, blank=True, null=True)
    cadenaaerea = models.CharField(max_length=20, blank=True, null=True)
    tipoflete = models.CharField(max_length=18, blank=True, null=True)
    numerolc = models.CharField(max_length=26, blank=True, null=True)
    notif = models.CharField(max_length=45, blank=True, null=True)
    dirnotif = models.CharField(max_length=45, blank=True, null=True)
    otralinea2 = models.CharField(max_length=45, blank=True, null=True)
    telnotif = models.CharField(max_length=45, blank=True, null=True)
    otralinea3 = models.CharField(max_length=45, blank=True, null=True)
    otralinea4 = models.CharField(max_length=45, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    idtransport = models.CharField(max_length=2, blank=True, null=True)
    to1 = models.CharField(max_length=3, blank=True, null=True)
    by1 = models.CharField(max_length=2, blank=True, null=True)
    to2 = models.CharField(max_length=3, blank=True, null=True)
    by2 = models.CharField(max_length=2, blank=True, null=True)
    simbolo = models.CharField(max_length=4, blank=True, null=True)
    carriage = models.CharField(max_length=10, blank=True, null=True)
    custom = models.CharField(max_length=10, blank=True, null=True)
    nombredestino = models.CharField(max_length=22, blank=True, null=True)
    vuelo1 = models.CharField(max_length=15, blank=True, null=True)
    vuelo2 = models.CharField(max_length=15, blank=True, null=True)
    vuelo3 = models.CharField(max_length=15, blank=True, null=True)
    vuelo4 = models.CharField(max_length=15, blank=True, null=True)
    valseguro = models.CharField(max_length=10, blank=True, null=True)
    cliente5 = models.CharField(db_column='Cliente5', max_length=45, blank=True, null=True)  # Field name made lowercase.
    consigna6 = models.CharField(db_column='Consigna6', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_guiasgrabadas'


class ExportGuiasgrabadas2(models.Model):
    id = models.BigAutoField(primary_key=True)
    marcas = models.CharField(max_length=80, blank=True, null=True)
    otraline = models.CharField(max_length=80, blank=True, null=True)
    attached = models.CharField(max_length=80, blank=True, null=True)
    nature1 = models.CharField(max_length=25, blank=True, null=True)
    nature2 = models.CharField(max_length=25, blank=True, null=True)
    nature3 = models.CharField(max_length=25, blank=True, null=True)
    nature4 = models.CharField(max_length=25, blank=True, null=True)
    nature5 = models.CharField(max_length=25, blank=True, null=True)
    nature6 = models.CharField(max_length=25, blank=True, null=True)
    nature7 = models.CharField(max_length=25, blank=True, null=True)
    nature8 = models.CharField(max_length=25, blank=True, null=True)
    nature9 = models.CharField(max_length=25, blank=True, null=True)
    free1 = models.CharField(max_length=60, blank=True, null=True)
    free2 = models.CharField(max_length=60, blank=True, null=True)
    free3 = models.CharField(max_length=60, blank=True, null=True)
    free4 = models.CharField(max_length=60, blank=True, null=True)
    free5 = models.CharField(max_length=60, blank=True, null=True)
    other1 = models.CharField(max_length=50, blank=True, null=True)
    other2 = models.CharField(max_length=50, blank=True, null=True)
    other3 = models.CharField(max_length=50, blank=True, null=True)
    signature = models.CharField(max_length=45, blank=True, null=True)
    fechaemi = models.CharField(max_length=12, blank=True, null=True)
    restotext = models.CharField(max_length=25, blank=True, null=True)
    portext = models.CharField(max_length=40, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    nature10 = models.CharField(max_length=25, blank=True, null=True)
    nature11 = models.CharField(max_length=25, blank=True, null=True)
    nature12 = models.CharField(max_length=25, blank=True, null=True)
    gastosconiva = models.IntegerField(blank=True, null=True)
    nature13 = models.CharField(db_column='Nature13', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature14 = models.CharField(db_column='Nature14', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature15 = models.CharField(db_column='Nature15', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature16 = models.CharField(db_column='Nature16', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature17 = models.CharField(db_column='Nature17', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature18 = models.CharField(db_column='Nature18', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature19 = models.CharField(db_column='Nature19', max_length=25, blank=True, null=True)  # Field name made lowercase.
    asagent = models.CharField(db_column='AsAgent', max_length=70, blank=True, null=True)  # Field name made lowercase.
    ofthecarrier = models.CharField(db_column='OfTheCarrier', max_length=70, blank=True, null=True)  # Field name made lowercase.
    chargesatdestination = models.DecimalField(db_column='ChargesAtDestination', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    totalcollectcharges = models.DecimalField(db_column='TotalCollectCharges', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_guiasgrabadas2'


class ExportGuiasgrabadas3(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    piezas = models.CharField(db_column='Piezas', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas2 = models.CharField(db_column='Piezas2', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas3 = models.CharField(db_column='Piezas3', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas4 = models.CharField(db_column='Piezas4', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas5 = models.CharField(db_column='Piezas5', max_length=4, blank=True, null=True)  # Field name made lowercase.
    totpiezas = models.CharField(db_column='TotPiezas', max_length=5, blank=True, null=True)  # Field name made lowercase.
    gross = models.CharField(db_column='Gross', max_length=10, blank=True, null=True)  # Field name made lowercase.
    otrogross = models.CharField(db_column='OtroGross', max_length=10, blank=True, null=True)  # Field name made lowercase.
    otrogross2 = models.CharField(db_column='OtroGross2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    otrogross3 = models.CharField(db_column='OtroGross3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    otrogross4 = models.CharField(db_column='OtroGross4', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totgross = models.CharField(db_column='TotGross', max_length=10, blank=True, null=True)  # Field name made lowercase.
    k = models.CharField(db_column='K', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k2 = models.CharField(db_column='K2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k3 = models.CharField(db_column='K3', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k4 = models.CharField(db_column='K4', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k5 = models.CharField(db_column='K5', max_length=1, blank=True, null=True)  # Field name made lowercase.
    r = models.CharField(db_column='R', max_length=1, blank=True, null=True)  # Field name made lowercase.
    r2 = models.CharField(db_column='R2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    r3 = models.CharField(db_column='R3', max_length=1, blank=True, null=True)  # Field name made lowercase.
    r4 = models.CharField(db_column='R4', max_length=1, blank=True, null=True)  # Field name made lowercase.
    r5 = models.CharField(db_column='R5', max_length=1, blank=True, null=True)  # Field name made lowercase.
    commodity = models.CharField(db_column='Commodity', max_length=8, blank=True, null=True)  # Field name made lowercase.
    comm2 = models.CharField(db_column='Comm2', max_length=8, blank=True, null=True)  # Field name made lowercase.
    comm3 = models.CharField(db_column='Comm3', max_length=8, blank=True, null=True)  # Field name made lowercase.
    comm4 = models.CharField(db_column='Comm4', max_length=8, blank=True, null=True)  # Field name made lowercase.
    comm5 = models.CharField(db_column='Comm5', max_length=8, blank=True, null=True)  # Field name made lowercase.
    chw = models.CharField(db_column='Chw', max_length=10, blank=True, null=True)  # Field name made lowercase.
    asvol = models.CharField(db_column='AsVol', max_length=10, blank=True, null=True)  # Field name made lowercase.
    chw3 = models.CharField(db_column='Chw3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    chw4 = models.CharField(db_column='Chw4', max_length=10, blank=True, null=True)  # Field name made lowercase.
    chw5 = models.CharField(db_column='Chw5', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rate = models.CharField(db_column='Rate', max_length=7, blank=True, null=True)  # Field name made lowercase.
    rate2 = models.CharField(db_column='Rate2', max_length=7, blank=True, null=True)  # Field name made lowercase.
    rate3 = models.CharField(db_column='Rate3', max_length=7, blank=True, null=True)  # Field name made lowercase.
    rate4 = models.CharField(db_column='Rate4', max_length=7, blank=True, null=True)  # Field name made lowercase.
    rate5 = models.CharField(db_column='Rate5', max_length=7, blank=True, null=True)  # Field name made lowercase.
    total = models.CharField(db_column='Total', max_length=10, blank=True, null=True)  # Field name made lowercase.
    total2 = models.CharField(db_column='Total2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    total3 = models.CharField(db_column='Total3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    total4 = models.CharField(db_column='Total4', max_length=10, blank=True, null=True)  # Field name made lowercase.
    total5 = models.CharField(db_column='Total5', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalfinal = models.CharField(db_column='TotalFinal', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalpp = models.CharField(db_column='TotalPP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalcc = models.CharField(db_column='TotalCC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    valpp = models.CharField(db_column='ValPP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    valcc = models.CharField(db_column='ValCC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    taxpp = models.CharField(db_column='TaxPP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    taxcc = models.CharField(db_column='TaxCC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dapp = models.CharField(db_column='DaPP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dacc = models.CharField(db_column='DaCC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dcpp = models.CharField(db_column='DcPP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dccc = models.CharField(db_column='DcCC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalprepaid = models.CharField(db_column='TotalPrepaid', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalcollect = models.CharField(db_column='TotalCollect', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalpprate = models.CharField(db_column='TotalPPRate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalccrate = models.CharField(db_column='TotalCCRate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cass = models.CharField(db_column='Cass', max_length=30, blank=True, null=True)  # Field name made lowercase.
    chgscode = models.CharField(db_column='ChgsCode', max_length=2, blank=True, null=True)  # Field name made lowercase.
    wtval = models.CharField(db_column='WtVal', max_length=2, blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(db_column='Other', max_length=2, blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', max_length=50, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=20, blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    carrierfinal = models.CharField(db_column='CarrierFinal', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_guiasgrabadas3'


class ExportMadresgrabadas(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    empresa = models.CharField(max_length=35, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    pais = models.CharField(max_length=22, blank=True, null=True)
    localidad = models.CharField(max_length=22, blank=True, null=True)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    cliente1 = models.CharField(max_length=45, blank=True, null=True)
    cliente2 = models.CharField(max_length=45, blank=True, null=True)
    cliente3 = models.CharField(max_length=45, blank=True, null=True)
    cliente4 = models.CharField(max_length=45, blank=True, null=True)
    consigna = models.CharField(max_length=45, blank=True, null=True)
    direcconsigna = models.CharField(max_length=45, blank=True, null=True)
    localconsigna = models.CharField(max_length=45, blank=True, null=True)
    teleconsigna = models.CharField(max_length=45, blank=True, null=True)
    otralinea = models.CharField(max_length=45, blank=True, null=True)
    empresa2 = models.CharField(max_length=45, blank=True, null=True)
    otracarrier = models.CharField(max_length=45, blank=True, null=True)
    localidad2 = models.CharField(max_length=45, blank=True, null=True)
    otrosdeagente = models.CharField(max_length=45, blank=True, null=True)
    iata = models.CharField(max_length=15, blank=True, null=True)
    salede = models.CharField(max_length=25, blank=True, null=True)
    cadenaaerea = models.CharField(max_length=20, blank=True, null=True)
    tipoflete = models.CharField(max_length=18, blank=True, null=True)
    notif = models.CharField(max_length=45, blank=True, null=True)
    dirnotif = models.CharField(max_length=45, blank=True, null=True)
    otralinea2 = models.CharField(max_length=45, blank=True, null=True)
    telnotif = models.CharField(max_length=45, blank=True, null=True)
    otralinea3 = models.CharField(max_length=45, blank=True, null=True)
    otralinea4 = models.CharField(max_length=45, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    idtransport = models.CharField(max_length=2, blank=True, null=True)
    to1 = models.CharField(max_length=3, blank=True, null=True)
    by1 = models.CharField(max_length=2, blank=True, null=True)
    to2 = models.CharField(max_length=3, blank=True, null=True)
    by2 = models.CharField(max_length=2, blank=True, null=True)
    simbolo = models.CharField(max_length=4, blank=True, null=True)
    carriage = models.CharField(max_length=10, blank=True, null=True)
    custom = models.CharField(max_length=10, blank=True, null=True)
    nombredestino = models.CharField(max_length=22, blank=True, null=True)
    vuelo1 = models.CharField(max_length=15, blank=True, null=True)
    vuelo2 = models.CharField(max_length=15, blank=True, null=True)
    vuelo3 = models.CharField(max_length=15, blank=True, null=True)
    vuelo4 = models.CharField(max_length=15, blank=True, null=True)
    valseguro = models.CharField(max_length=10, blank=True, null=True)
    marcas = models.CharField(max_length=80, blank=True, null=True)
    otraline = models.CharField(max_length=80, blank=True, null=True)
    attached = models.CharField(max_length=80, blank=True, null=True)
    nature2 = models.CharField(max_length=25, blank=True, null=True)
    nature3 = models.CharField(max_length=25, blank=True, null=True)
    houses = models.CharField(max_length=28, blank=True, null=True)
    houses2 = models.CharField(max_length=28, blank=True, null=True)
    houses3 = models.CharField(max_length=28, blank=True, null=True)
    free1 = models.CharField(max_length=45, blank=True, null=True)
    free2 = models.CharField(max_length=45, blank=True, null=True)
    free3 = models.CharField(max_length=45, blank=True, null=True)
    free4 = models.CharField(max_length=45, blank=True, null=True)
    free5 = models.CharField(max_length=45, blank=True, null=True)
    other1 = models.CharField(max_length=50, blank=True, null=True)
    other2 = models.CharField(max_length=50, blank=True, null=True)
    other3 = models.CharField(max_length=50, blank=True, null=True)
    signature = models.CharField(max_length=45, blank=True, null=True)
    fechaemi = models.CharField(max_length=12, blank=True, null=True)
    restotext = models.CharField(max_length=25, blank=True, null=True)
    portext = models.CharField(max_length=40, blank=True, null=True)
    houses4 = models.CharField(db_column='Houses4', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses5 = models.CharField(db_column='Houses5', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses6 = models.CharField(db_column='Houses6', max_length=28, blank=True, null=True)  # Field name made lowercase.
    asagent = models.CharField(db_column='AsAgent', max_length=70, blank=True, null=True)  # Field name made lowercase.
    ofthecarrier = models.CharField(db_column='OfTheCarrier', max_length=70, blank=True, null=True)  # Field name made lowercase.
    gastosconiva = models.SmallIntegerField(db_column='GastosConIVA', blank=True, null=True)  # Field name made lowercase.
    houses7 = models.CharField(db_column='Houses7', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses8 = models.CharField(db_column='Houses8', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses9 = models.CharField(db_column='Houses9', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses10 = models.CharField(db_column='Houses10', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses11 = models.CharField(db_column='Houses11', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses12 = models.CharField(db_column='Houses12', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses13 = models.CharField(db_column='Houses13', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses14 = models.CharField(db_column='Houses14', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses15 = models.CharField(db_column='Houses15', max_length=28, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_madresgrabadas'


class ExportMadresgrabadas3(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    piezas = models.CharField(db_column='Piezas', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas2 = models.CharField(db_column='Piezas2', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas3 = models.CharField(db_column='Piezas3', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas4 = models.CharField(db_column='Piezas4', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas5 = models.CharField(db_column='Piezas5', max_length=4, blank=True, null=True)  # Field name made lowercase.
    totpiezas = models.CharField(db_column='TotPiezas', max_length=5, blank=True, null=True)  # Field name made lowercase.
    gross = models.CharField(db_column='Gross', max_length=10, blank=True, null=True)  # Field name made lowercase.
    otrogross = models.CharField(db_column='OtroGross', max_length=10, blank=True, null=True)  # Field name made lowercase.
    otrogross2 = models.CharField(db_column='OtroGross2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    otrogross3 = models.CharField(db_column='OtroGross3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    otrogross4 = models.CharField(db_column='OtroGross4', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totgross = models.CharField(db_column='TotGross', max_length=10, blank=True, null=True)  # Field name made lowercase.
    k = models.CharField(db_column='K', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k2 = models.CharField(db_column='K2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k3 = models.CharField(db_column='K3', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k4 = models.CharField(db_column='K4', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k5 = models.CharField(db_column='K5', max_length=1, blank=True, null=True)  # Field name made lowercase.
    r = models.CharField(db_column='R', max_length=1, blank=True, null=True)  # Field name made lowercase.
    r2 = models.CharField(db_column='R2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    r3 = models.CharField(db_column='R3', max_length=1, blank=True, null=True)  # Field name made lowercase.
    r4 = models.CharField(db_column='R4', max_length=1, blank=True, null=True)  # Field name made lowercase.
    r5 = models.CharField(db_column='R5', max_length=1, blank=True, null=True)  # Field name made lowercase.
    commodity = models.CharField(db_column='Commodity', max_length=8, blank=True, null=True)  # Field name made lowercase.
    comm2 = models.CharField(db_column='Comm2', max_length=8, blank=True, null=True)  # Field name made lowercase.
    comm3 = models.CharField(db_column='Comm3', max_length=8, blank=True, null=True)  # Field name made lowercase.
    comm4 = models.CharField(db_column='Comm4', max_length=8, blank=True, null=True)  # Field name made lowercase.
    comm5 = models.CharField(db_column='Comm5', max_length=8, blank=True, null=True)  # Field name made lowercase.
    chw = models.CharField(db_column='Chw', max_length=10, blank=True, null=True)  # Field name made lowercase.
    asvol = models.CharField(db_column='AsVol', max_length=10, blank=True, null=True)  # Field name made lowercase.
    chw3 = models.CharField(db_column='Chw3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    chw4 = models.CharField(db_column='Chw4', max_length=10, blank=True, null=True)  # Field name made lowercase.
    chw5 = models.CharField(db_column='Chw5', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rate = models.CharField(db_column='Rate', max_length=7, blank=True, null=True)  # Field name made lowercase.
    rate2 = models.CharField(db_column='Rate2', max_length=7, blank=True, null=True)  # Field name made lowercase.
    rate3 = models.CharField(db_column='Rate3', max_length=7, blank=True, null=True)  # Field name made lowercase.
    rate4 = models.CharField(db_column='Rate4', max_length=7, blank=True, null=True)  # Field name made lowercase.
    rate5 = models.CharField(db_column='Rate5', max_length=7, blank=True, null=True)  # Field name made lowercase.
    total = models.CharField(db_column='Total', max_length=10, blank=True, null=True)  # Field name made lowercase.
    total2 = models.CharField(db_column='Total2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    total3 = models.CharField(db_column='Total3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    total4 = models.CharField(db_column='Total4', max_length=10, blank=True, null=True)  # Field name made lowercase.
    total5 = models.CharField(db_column='Total5', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalfinal = models.CharField(db_column='TotalFinal', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalpp = models.CharField(db_column='TotalPP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalcc = models.CharField(db_column='TotalCC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    valpp = models.CharField(db_column='ValPP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    valcc = models.CharField(db_column='ValCC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    taxpp = models.CharField(db_column='TaxPP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    taxcc = models.CharField(db_column='TaxCC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dapp = models.CharField(db_column='DaPP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dacc = models.CharField(db_column='DaCC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dcpp = models.CharField(db_column='DcPP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dccc = models.CharField(db_column='DcCC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalprepaid = models.CharField(db_column='TotalPrepaid', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalcollect = models.CharField(db_column='TotalCollect', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalpprate = models.CharField(db_column='TotalPPRate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totalccrate = models.CharField(db_column='TotalCCRate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cass = models.CharField(db_column='Cass', max_length=30, blank=True, null=True)  # Field name made lowercase.
    chgscode = models.CharField(db_column='ChgsCode', max_length=2, blank=True, null=True)  # Field name made lowercase.
    wtval = models.CharField(db_column='WtVal', max_length=2, blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(db_column='Other', max_length=2, blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', max_length=50, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=20, blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    carrierfinal = models.CharField(db_column='CarrierFinal', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_madresgrabadas3'


class ExportReservas(models.Model):
    numero = models.IntegerField(db_column='Numero', primary_key=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    vuelo = models.CharField(db_column='Vuelo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    kilos = models.FloatField(db_column='Kilos', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    awb = models.CharField(max_length=20, blank=True, null=True)
    agente = models.IntegerField(blank=True, null=True)
    consignatario = models.IntegerField(blank=True, null=True)
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    tarifaawb = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    volumen = models.FloatField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    tomopeso = models.SmallIntegerField(blank=True, null=True)
    aplicable = models.FloatField(blank=True, null=True)
    aduana = models.CharField(max_length=30, blank=True, null=True)
    tarifapl = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    profitage = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    plfacturado = models.CharField(max_length=1, blank=True, null=True)
    tipoover = models.CharField(db_column='Tipoover', max_length=1, blank=True, null=True)  # Field name made lowercase.
    over = models.FloatField(db_column='Over', blank=True, null=True)  # Field name made lowercase.
    comision = models.FloatField(db_column='Comision', blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(max_length=30, blank=True, null=True)
    envioedi = models.CharField(max_length=1, blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    reporteada = models.IntegerField(blank=True, null=True)
    nroreferedi = models.IntegerField(blank=True, null=True)
    impresiones = models.SmallIntegerField(blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    tarifafija = models.CharField(max_length=1, blank=True, null=True)
    fechareport = models.DateTimeField(blank=True, null=True)
    manifiesto = models.CharField(max_length=15, blank=True, null=True)
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    arbitrajecass = models.DecimalField(db_column='ArbitrajeCASS', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sttawb = models.CharField(max_length=30, blank=True, null=True)
    autogenfletecpa = models.CharField(db_column='AutogenFleteCPA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    envioiata = models.CharField(db_column='EnvioIATA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    esagente = models.CharField(db_column='esAgente', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    documentos = models.CharField(db_column='Documentos', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)  # Field name made lowercase.
    deposito = models.SmallIntegerField(db_column='Deposito', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_reservas'

    def get_number(self):
        reserva_l = ExportReservas.objects.order_by('numero').last()
        if reserva_l:
            nuevo_numero = reserva_l.numero + 1
        else:
            nuevo_numero = 1

        return nuevo_numero


class ExportServiceaereo(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=40, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_serviceaereo'


class ExportServireserva(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=40, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_servireserva'


class ExportTraceop(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=30, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=250, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=20, blank=True, null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_traceop'


class Master(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True, primary_key=True)  # Añadir primary_key=True
    transportista = models.CharField(max_length=400,blank=True, null=True)
    agente = models.CharField(max_length=400,blank=True, null=True)
    embarcador = models.CharField(db_column='consignatario',max_length=400,blank=True, null=True)
    origen = models.CharField(max_length=400,blank=True, null=True)
    destino = models.CharField(max_length=400,blank=True, null=True)
    status = models.CharField(max_length=400,blank=True, null=True)
    awb = models.CharField(max_length=400, blank=True, null=True)
    llegada = models.DateField(blank=True, null=True)
    seguimientos = models.TextField( blank=True, null=True)
    hawbs = models.TextField( blank=True, null=True)

    def __str__(self,):
        return self.numero

    class Meta:
        managed = False
        db_table = 'VExpAereaMaster'



class VEmbarqueaereo(models.Model):
    numero = models.IntegerField(unique=True, primary_key=True)
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)

    transportista = models.CharField(max_length=255, blank=True, null=True)  # Nombre del transportista
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=255, blank=True, null=True)  # Nombre del agente
    consignatario = models.CharField(max_length=255, blank=True, null=True)
    consignatario_id = models.IntegerField()
    consignatario_codigo = models.IntegerField()
    # Nombre del consignatario
    posicion = models.CharField(max_length=20, blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    fecha_embarque = models.DateTimeField(blank=True, null=True)
    fecha_retiro = models.DateTimeField(blank=True, null=True)
    valor_transporte = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valor_aduana = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifa_venta = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifa_compra = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    volumen_cubico = models.FloatField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    referencia = models.IntegerField(null=True, blank=True, default=None)
    seguimiento = models.IntegerField(null=True, blank=True, default=None)
    orden_cliente = models.CharField(max_length=850, null=True, blank=True, default=None)
    ref_proveedor = models.CharField(max_length=250, null=True, blank=True, default=None)
    embarcador = models.CharField(max_length=50, null=True, blank=True, default=None)
    direccion_embarcador = models.CharField(max_length=50, null=True, blank=True, default=None)
    ciudad_embarcador = models.CharField(max_length=5, null=True, blank=True, default=None)
    pais_embarcador = models.CharField(max_length=50, null=True, blank=True, default=None)
    direccion_consignatario = models.CharField(max_length=50, null=True, blank=True, default=None)
    ciudad_consignatario = models.CharField(max_length=5, null=True, blank=True, default=None)
    pais_consignatario = models.CharField(max_length=50, null=True, blank=True, default=None)
    terminos = models.CharField(max_length=3, null=True, blank=True, default=None)
    pago_flete = models.CharField(max_length=1, null=True, blank=True, default=None)
    consolidado = models.CharField(max_length=1, null=True, blank=True, default=None)
    etd = models.DateTimeField(db_column='etd', blank=True, null=True)
    eta = models.DateTimeField(db_column='eta', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'VExpAereaEmbarqueAereo'

class VEmbarqueaereoDirecto(models.Model):
    consignatario_codigo = models.IntegerField()
    numero = models.IntegerField(unique=True, primary_key=True)
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    transportista = models.CharField(max_length=255, blank=True, null=True)  # Nombre del transportista
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=255, blank=True, null=True)  # Nombre del agente
    consignatario = models.CharField(max_length=255, blank=True, null=True)
    consignatario_id = models.IntegerField()
    # Nombre del consignatario
    posicion = models.CharField(max_length=20, blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    fecha_embarque = models.DateTimeField(blank=True, null=True)
    fecha_retiro = models.DateTimeField(blank=True, null=True)
    valor_transporte = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valor_aduana = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifa_venta = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifa_compra = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    volumen_cubico = models.FloatField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    referencia = models.IntegerField(null=True, blank=True, default=None)
    seguimiento = models.IntegerField(null=True, blank=True, default=None)
    orden_cliente = models.CharField(max_length=850, null=True, blank=True, default=None)
    ref_proveedor = models.CharField(max_length=250, null=True, blank=True, default=None)
    embarcador = models.CharField(max_length=50, null=True, blank=True, default=None)
    direccion_embarcador = models.CharField(max_length=50, null=True, blank=True, default=None)
    ciudad_embarcador = models.CharField(max_length=5, null=True, blank=True, default=None)
    pais_embarcador = models.CharField(max_length=50, null=True, blank=True, default=None)
    direccion_consignatario = models.CharField(max_length=50, null=True, blank=True, default=None)
    ciudad_consignatario = models.CharField(max_length=5, null=True, blank=True, default=None)
    pais_consignatario = models.CharField(max_length=50, null=True, blank=True, default=None)
    terminos = models.CharField(max_length=3, null=True, blank=True, default=None)
    pago_flete = models.CharField(max_length=1, null=True, blank=True, default=None)
    consolidado = models.CharField(max_length=1, null=True, blank=True, default=None)
    etd = models.DateTimeField(db_column='etd', blank=True, null=True)
    eta = models.DateTimeField(db_column='eta', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'VExpAereaEmbarqueAereoDirecto'

class VGastosMaster(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True,choices=(("P","Prepaid"),("C","Collect")))
    servicio = models.CharField(max_length=500,blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    notomaprofit = models.BooleanField()
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.
    id_servicio = models.SmallIntegerField()
    id_moneda = models.SmallIntegerField()
    id_socio = models.SmallIntegerField()

    def __str__(self,):
        return self.modo + ' - ' + str(self.numero)

    class Meta:
        managed = False
        db_table = 'VExpAereaGastosMaster'

class VGastosHouse(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True,choices=(("P","Prepaid"),("C","Collect")))
    servicio = models.CharField(max_length=500,blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    notomaprofit = models.BooleanField()
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.
    id_servicio = models.SmallIntegerField()
    id_moneda = models.SmallIntegerField()
    id_socio = models.SmallIntegerField()

    def __str__(self,):
        return self.modo + ' - ' + str(self.numero)

    class Meta:
        managed = False
        db_table = 'VExpAereaGastosHouse'


class GuiasHijas(models.Model):
    numero = models.CharField(max_length=100)

    # Numéricos (pueden ser Decimal si necesitás precisión en dinero)
    total_bultos = models.IntegerField(default=0)
    total_pesos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    volumen_total_embarque = models.DecimalField(max_digits=12, decimal_places=4, default=0)

    valppd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valcol = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prepaid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    collect = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taxppd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taxcol = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    agentppd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    agentcol = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    carrierppd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    carriercol = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_prepaid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_collect = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Textos (sin límite)
    posicion = models.TextField(blank=True)
    consignatario = models.TextField(blank=True)
    shipper = models.TextField(blank=True)
    awb_sf = models.TextField(blank=True)
    awb1 = models.TextField(blank=True)
    awb2 = models.TextField(blank=True)
    awb3 = models.TextField(blank=True)
    hawb = models.TextField(blank=True)
    empresa = models.TextField(blank=True)
    info = models.TextField(blank=True)
    vuelos1 = models.TextField(blank=True)
    vuelos2 = models.TextField(blank=True)
    airport_departure = models.TextField(blank=True)
    airport_final = models.TextField(blank=True)
    final = models.TextField(blank=True)
    by_cia_1 = models.TextField(blank=True)
    by_cia_2 = models.TextField(blank=True)
    by_cia_3 = models.TextField(blank=True)
    to_1 = models.TextField(blank=True)
    to_2 = models.TextField(blank=True)
    to_3 = models.TextField(blank=True)
    by_first_carrier = models.TextField(blank=True)
    array_destinos = models.TextField(blank=True)
    modopago = models.TextField(blank=True)
    cc1 = models.TextField(blank=True)
    cc2 = models.TextField(blank=True)
    pp1 = models.TextField(blank=True)
    pp2 = models.TextField(blank=True)
    pago_code = models.TextField(blank=True)
    otros_gastos = models.TextField(blank=True)
    shipper_signature = models.TextField(blank=True)
    carrier_signature = models.TextField(blank=True)
    amount_insurance = models.TextField(blank=True)
    handling = models.TextField(blank=True)
    declared_value_for_carriage = models.TextField(blank=True)
    declared_value_for_customs = models.TextField(blank=True)
    iata_code_agente = models.TextField(blank=True)
    account_nro = models.TextField(blank=True)
    notify = models.TextField(blank=True)
    currency = models.TextField(blank=True)
    fecha_ingreso = models.DateTimeField(blank=True, null=True)

    # Otros posibles campos como JSON (si querés guardar estructuras)
    mercaderias = models.JSONField(blank=True, null=True)
    medidas_text = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'guias_hijas'

class GuiasMadres(models.Model):
    numero = models.CharField(max_length=100)

    # Numéricos (pueden ser Decimal si necesitás precisión en dinero)
    total_bultos = models.IntegerField(default=0)
    total_pesos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    volumen_total_embarque = models.DecimalField(max_digits=12, decimal_places=4, default=0)

    valppd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valcol = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prepaid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    collect = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taxppd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taxcol = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    agentppd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    agentcol = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    carrierppd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    carriercol = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_prepaid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_collect = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Textos (sin límite)
    posicion = models.TextField(blank=True)
    consignatario = models.TextField(blank=True)
    shipper = models.TextField(blank=True)
    awb_sf = models.TextField(blank=True)
    awb1 = models.TextField(blank=True)
    awb2 = models.TextField(blank=True)
    awb3 = models.TextField(blank=True)
    hawb = models.TextField(blank=True)
    empresa = models.TextField(blank=True)
    info = models.TextField(blank=True)
    vuelos1 = models.TextField(blank=True)
    vuelos2 = models.TextField(blank=True)
    airport_departure = models.TextField(blank=True)
    airport_final = models.TextField(blank=True)
    final = models.TextField(blank=True)
    by_cia_1 = models.TextField(blank=True)
    by_cia_2 = models.TextField(blank=True)
    by_cia_3 = models.TextField(blank=True)
    to_1 = models.TextField(blank=True)
    to_2 = models.TextField(blank=True)
    to_3 = models.TextField(blank=True)
    by_first_carrier = models.TextField(blank=True)
    array_destinos = models.TextField(blank=True)
    modopago = models.TextField(blank=True)
    cc1 = models.TextField(blank=True)
    cc2 = models.TextField(blank=True)
    pp1 = models.TextField(blank=True)
    pp2 = models.TextField(blank=True)
    pago_code = models.TextField(blank=True)
    otros_gastos = models.TextField(blank=True)
    shipper_signature = models.TextField(blank=True)
    carrier_signature = models.TextField(blank=True)
    amount_insurance = models.TextField(blank=True)
    handling = models.TextField(blank=True)
    declared_value_for_carriage = models.TextField(blank=True)
    declared_value_for_customs = models.TextField(blank=True)
    iata_code_agente = models.TextField(blank=True)
    account_nro = models.TextField(blank=True)
    notify = models.TextField(blank=True)
    currency = models.TextField(blank=True)
    fecha_ingreso = models.DateTimeField(blank=True, null=True)

    # Otros posibles campos como JSON (si querés guardar estructuras)
    mercaderias = models.JSONField(blank=True, null=True)
    medidas_text = models.JSONField(blank=True, null=True)
    issuing_carrier = models.TextField(blank=True, null=True)
    descripcion_mercaderias = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'guias_madres'

from auditlog.registry import auditlog

class MyModel(models.Model):
    history = AuditlogHistoryField()
    # Model definition goes here


auditlog.register(MyModel)

from inspect import getmembers
from auditlog.registry import auditlog
from expaerea import models

tablas = getmembers(models)
for t in tablas:
    try:
        auditlog.register(t[1], serialize_data=True)
    except Exception as e:
        pass