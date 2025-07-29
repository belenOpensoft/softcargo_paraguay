from auditlog.models import AuditlogHistoryField
from django.db import models

from mantenimientos.models import Productos


class ImportAnulados(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'import_anulados'


class ImportAttachhijo(models.Model):
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
        db_table = 'import_attachhijo'


class ImportAttachmadre(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_attachmadre'


class ImportCargaaerea(models.Model):
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
    producto = models.ForeignKey(Productos, to_field='codigo', on_delete=models.PROTECT, db_column='producto',related_name='prod_carga_ia')
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True,choices=choice_tipo)
    fechaembarque = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'import_cargaaerea'


class ImportCargaaereaaduana(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    producto = models.SmallIntegerField(db_column='Producto', blank=True, null=True)  # Field name made lowercase.
    bultos = models.IntegerField(db_column='Bultos', blank=True, null=True)  # Field name made lowercase.
    bruto = models.FloatField(db_column='Bruto', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechamanifiesto = models.DateTimeField(db_column='FechaManifiesto', blank=True, null=True)  # Field name made lowercase.
    enviado = models.CharField(db_column='Enviado', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_cargaaereaaduana'


class ImportClaveposicion(models.Model):
    posicion = models.CharField(primary_key=True, max_length=15)
    numeroorden = models.SmallIntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_claveposicion'


class ImportConexaerea(models.Model):
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
        db_table = 'import_conexaerea'


class ImportConexreserva(models.Model):
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
        db_table = 'import_conexreserva'


class ImportEmbarqueaereo(models.Model):
    numero = models.IntegerField(primary_key=True)
    cliente = models.IntegerField(blank=True, null=True)
    consignatario = models.IntegerField(blank=True, null=True)
    despachante = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    consolidado = models.SmallIntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=20, blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    aduana = models.CharField(max_length=30, blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    pago = models.SmallIntegerField(blank=True, null=True)
    awb = models.CharField(max_length=20, blank=True, null=True)
    hawb = models.CharField(max_length=50, blank=True, null=True)
    transportista = models.SmallIntegerField(blank=True, null=True)
    valortransporte = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valoraduana = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    fechaembarque = models.DateTimeField(blank=True, null=True)
    fecharetiro = models.DateTimeField(blank=True, null=True)
    pagoflete = models.CharField(max_length=1, blank=True, null=True)
    marcas = models.CharField(max_length=50, blank=True, null=True)
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
    agente = models.SmallIntegerField(blank=True, null=True)
    transdestino = models.SmallIntegerField(blank=True, null=True)
    notifcliente = models.DateTimeField(blank=True, null=True)
    aquien = models.CharField(max_length=30, blank=True, null=True)
    transftransport = models.DateTimeField(blank=True, null=True)
    transfcliente = models.DateTimeField(blank=True, null=True)
    retirada = models.CharField(max_length=30, blank=True, null=True)
    notifagente = models.DateTimeField(blank=True, null=True)
    observadoc = models.CharField(max_length=500, blank=True, null=True)
    completo = models.CharField(max_length=1, blank=True, null=True)
    observado = models.CharField(max_length=1, blank=True, null=True)
    detcompleto = models.CharField(max_length=50, blank=True, null=True)
    detobservado = models.CharField(max_length=50, blank=True, null=True)
    facturado = models.CharField(max_length=1, blank=True, null=True)
    profitage = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifafija = models.CharField(max_length=1, blank=True, null=True)
    embarcador = models.SmallIntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    notificar = models.SmallIntegerField(db_column='Notificar', blank=True, null=True)  # Field name made lowercase.
    vaporcli = models.CharField(db_column='Vaporcli', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vaporcli2 = models.CharField(db_column='Vaporcli2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tipobonifcli = models.CharField(max_length=1, blank=True, null=True)
    bonifcli = models.FloatField(blank=True, null=True)
    tipovend = models.CharField(max_length=1, blank=True, null=True)
    vendedor = models.SmallIntegerField(db_column='Vendedor', blank=True, null=True)  # Field name made lowercase.
    comivend = models.FloatField(blank=True, null=True)
    tarifaprofit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    aplitransp = models.FloatField(blank=True, null=True)
    nroreferedi = models.IntegerField(blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    ordencliente = models.CharField(max_length=850, blank=True, null=True)
    propia = models.IntegerField(blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    fechaentrega = models.DateTimeField(blank=True, null=True)
    aquienentrega = models.CharField(max_length=30, blank=True, null=True)
    terminal = models.CharField(max_length=25, blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    originales = models.CharField(max_length=1, blank=True, null=True)
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=250, blank=True, null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=250, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mercaderia = models.TextField(db_column='Mercaderia', blank=True, null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    tieneacta = models.CharField(db_column='TieneActa', max_length=1, blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=250, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enviointercomex = models.CharField(db_column='EnvioIntercomex', max_length=1, blank=True, null=True)  # Field name made lowercase.
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emisionawb = models.DateTimeField(db_column='EmisionAWB', blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    fechalibdoc = models.DateTimeField(db_column='FechaLibDoc', blank=True, null=True)  # Field name made lowercase.
    horalibdoc = models.CharField(db_column='HoraLibDoc', max_length=8, blank=True, null=True)  # Field name made lowercase.
    fechapresmanif = models.DateTimeField(db_column='FechaPresManif', blank=True, null=True)  # Field name made lowercase.
    horapresmanif = models.CharField(db_column='HoraPresManif', max_length=8, blank=True, null=True)  # Field name made lowercase.
    fechacierremanif = models.DateTimeField(db_column='FechaCierreManif', blank=True, null=True)  # Field name made lowercase.
    horacierremanif = models.CharField(db_column='HoraCierreManif', max_length=8, blank=True, null=True)  # Field name made lowercase.
    fechadesconso = models.DateTimeField(db_column='FechaDesconso', blank=True, null=True)  # Field name made lowercase.
    horadesconso = models.CharField(db_column='HoraDesconso', max_length=8, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.DateTimeField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_embarqueaereo'

    def get_number(self):
        reserva_l = ImportEmbarqueaereo.objects.order_by('numero').last()
        if reserva_l:
            nuevo_numero = reserva_l.numero + 1
        else:
            nuevo_numero = 1

        return nuevo_numero


class ImportEntregadoc(models.Model):
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
        db_table = 'import_entregadoc'


class ImportFaxes(models.Model):
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
        db_table = 'import_faxes'

class ImportGastoshijos(models.Model):
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
        db_table = 'import_gastoshijos'


class ImportGuiasgrabadas(models.Model):
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
    vuelo1 = models.CharField(max_length=13, blank=True, null=True)
    vuelo2 = models.CharField(max_length=13, blank=True, null=True)
    vuelo3 = models.CharField(max_length=13, blank=True, null=True)
    vuelo4 = models.CharField(max_length=13, blank=True, null=True)
    valseguro = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'import_guiasgrabadas'


class ImportGuiasgrabadas2(models.Model):
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
    asagent = models.CharField(db_column='AsAgent', max_length=70, blank=True, null=True)  # Field name made lowercase.
    ofthecarrier = models.CharField(db_column='OfTheCarrier', max_length=70, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_guiasgrabadas2'


class ImportGuiasgrabadas3(models.Model):
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
        db_table = 'import_guiasgrabadas3'


class ImportReservas(models.Model):
    numero = models.IntegerField(db_column='Numero', primary_key=True)  # Field name made lowercase.
    transportista = models.SmallIntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    vuelo = models.CharField(db_column='Vuelo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    kilos = models.FloatField(db_column='Kilos', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    awb = models.CharField(max_length=20, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    volumen = models.FloatField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    tomopeso = models.SmallIntegerField(blank=True, null=True)
    aplicable = models.FloatField(blank=True, null=True)
    aduana = models.CharField(max_length=30, blank=True, null=True)
    preaviso = models.CharField(max_length=1, blank=True, null=True)
    notirecibo = models.DateTimeField(blank=True, null=True)
    porquien = models.CharField(max_length=30, blank=True, null=True)
    transfrecibo = models.DateTimeField(blank=True, null=True)
    completo = models.CharField(max_length=1, blank=True, null=True)
    observado = models.CharField(max_length=1, blank=True, null=True)
    detcompleto = models.CharField(max_length=50, blank=True, null=True)
    detobservado = models.CharField(max_length=50, blank=True, null=True)
    observadoc = models.CharField(max_length=500, blank=True, null=True)
    profitage = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifapl = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    posicion = models.CharField(max_length=30, blank=True, null=True)
    envioedi = models.CharField(max_length=1, blank=True, null=True)
    nroreferedi = models.IntegerField(blank=True, null=True)
    kilosmadre = models.FloatField(blank=True, null=True)
    bultosmadre = models.IntegerField(blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    tarifafija = models.CharField(max_length=1, blank=True, null=True)
    manifiesto = models.CharField(max_length=30, blank=True, null=True)
    emision = models.DateTimeField(blank=True, null=True)
    terminal = models.SmallIntegerField(blank=True, null=True)
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_reservas'

    def get_number(self):
        reserva_l = ImportReservas.objects.order_by('numero').last()
        if reserva_l:
            nuevo_numero = reserva_l.numero + 1
        else:
            nuevo_numero = 1

        return nuevo_numero


class ImportServiceaereo(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=40, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_serviceaereo'


class ImportServireserva(models.Model):
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
    prorrateo = models.CharField(db_column='Prorrateo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_servireserva'


class ImportTraceop(models.Model):
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
        db_table = 'import_traceop'

class Master(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True,primary_key=True)
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
        db_table = 'VImpAereatMaster'


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
        db_table = 'VImpAereaGastosMaster'

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
        db_table = 'VImpAereaGastosHouse'

class VEmbarqueaereo(models.Model):
    numero = models.IntegerField(unique=True, primary_key=True)
    consignatario_id = models.IntegerField()
    consignatario_codigo = models.IntegerField()
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)

    transportista = models.CharField(max_length=255, blank=True, null=True)  # Nombre del transportista
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=255, blank=True, null=True)  # Nombre del agente
    consignatario = models.CharField(max_length=255, blank=True, null=True)  # Nombre del consignatario
   # cliente = models.CharField(max_length=255, blank=True, null=True)  # Nombre del consignatario
    #armador = models.CharField(max_length=255, blank=True, null=True)  # Nombre del armador
    #vapor = models.CharField(max_length=30, blank=True, null=True)
    posicion = models.CharField(max_length=20, blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    fecha_embarque = models.DateTimeField(blank=True, null=True)
    fecha_retiro = models.DateTimeField(blank=True, null=True)
    notificar_agente = models.DateTimeField(blank=True, null=True)
    notificar_cliente = models.DateTimeField(blank=True, null=True)
    valor_transporte = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valor_aduana = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifa_venta = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifa_compra = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    volumen_cubico = models.FloatField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    #viaje = models.CharField(max_length=20, null=True, blank=True, default=None)
    referencia = models.IntegerField(null=True, blank=True, default=None)
    seguimiento = models.IntegerField(null=True, blank=True, default=None)
    aplicable = models.IntegerField(null=True, blank=True, default=None)
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
        db_table = 'VImpAereaEmbarqueAereo'

class VEmbarqueaereoDirecto(models.Model):
    numero = models.IntegerField(unique=True, primary_key=True)
    consignatario_id = models.IntegerField()
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    aplicable = models.IntegerField(null=True, blank=True, default=None)
    consignatario_codigo = models.IntegerField()

    transportista = models.CharField(max_length=255, blank=True, null=True)  # Nombre del transportista
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=255, blank=True, null=True)  # Nombre del agente
    consignatario = models.CharField(max_length=255, blank=True, null=True)  # Nombre del consignatario
   # cliente = models.CharField(max_length=255, blank=True, null=True)  # Nombre del consignatario
    #armador = models.CharField(max_length=255, blank=True, null=True)  # Nombre del armador
    #vapor = models.CharField(max_length=30, blank=True, null=True)
    posicion = models.CharField(max_length=20, blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    fecha_embarque = models.DateTimeField(blank=True, null=True)
    fecha_retiro = models.DateTimeField(blank=True, null=True)
    notificar_agente = models.DateTimeField(blank=True, null=True)
    notificar_cliente = models.DateTimeField(blank=True, null=True)
    valor_transporte = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valor_aduana = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifa_venta = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifa_compra = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    volumen_cubico = models.FloatField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    #viaje = models.CharField(max_length=20, null=True, blank=True, default=None)
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
        db_table = 'VImpAereaEmbarqueAereoDirecto'

from auditlog.registry import auditlog

class MyModel(models.Model):
    history = AuditlogHistoryField()
    # Model definition goes here


auditlog.register(MyModel)

from inspect import getmembers
from auditlog.registry import auditlog
from impaerea import models

tablas = getmembers(models)
for t in tablas:
    try:
        auditlog.register(t[1], serialize_data=True)
    except Exception as e:
        pass