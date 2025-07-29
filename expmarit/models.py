# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from auditlog.models import AuditlogHistoryField
from django.db import models

from mantenimientos.models import Productos


class ExpmaritAnulados(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expmarit_anulados'


class ExpmaritAttachhijo(models.Model):
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
        db_table = 'expmarit_attachhijo'


class ExpmaritAttachmadre(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_attachmadre'


class ExpmaritBookenv(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    marks = models.CharField(max_length=30, blank=True, null=True)
    packages = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    gross = models.CharField(max_length=30, blank=True, null=True)
    tare = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expmarit_bookenv'


class ExpmaritBooking(models.Model):
    numero = models.IntegerField(primary_key=True)
    empresa = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    pais = models.CharField(max_length=15, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    comboembarca = models.IntegerField(blank=True, null=True)
    cliente2 = models.CharField(max_length=50, blank=True, null=True)
    cliente3 = models.CharField(max_length=50, blank=True, null=True)
    cliente4 = models.CharField(max_length=50, blank=True, null=True)
    comboconsig = models.IntegerField(blank=True, null=True)
    direcconsigna = models.CharField(max_length=50, blank=True, null=True)
    localconsigna = models.CharField(max_length=50, blank=True, null=True)
    teleconsigna = models.CharField(max_length=50, blank=True, null=True)
    otralinea = models.CharField(max_length=50, blank=True, null=True)
    nrobooking = models.CharField(max_length=30, blank=True, null=True)
    dia = models.DateTimeField(blank=True, null=True)
    salede = models.CharField(max_length=30, blank=True, null=True)
    loading = models.CharField(max_length=30, blank=True, null=True)
    discharge = models.CharField(max_length=30, blank=True, null=True)
    delivery = models.CharField(max_length=30, blank=True, null=True)
    vapor = models.CharField(max_length=30, blank=True, null=True)
    etapod = models.DateTimeField(blank=True, null=True)
    etapol = models.DateTimeField(blank=True, null=True)
    viaje = models.CharField(max_length=30, blank=True, null=True)
    payable = models.CharField(max_length=30, blank=True, null=True)
    combotransport = models.IntegerField(blank=True, null=True)
    comboproduc = models.SmallIntegerField(blank=True, null=True)
    bultos = models.FloatField(blank=True, null=True)
    pesobruto = models.FloatField(blank=True, null=True)
    net = models.TextField(blank=True, null=True)
    sold = models.TextField(blank=True, null=True)
    profit = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    giro = models.CharField(max_length=30, blank=True, null=True)
    despachante = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    terminal = models.CharField(max_length=30, blank=True, null=True)
    direccterminal = models.CharField(max_length=30, blank=True, null=True)
    telterminal = models.CharField(max_length=30, blank=True, null=True)
    contactoterminal = models.CharField(db_column='ContactoTerminal', max_length=30, blank=True, null=True)  # Field name made lowercase.
    bandera = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expmarit_booking'


class ExpmaritCargaaerea(models.Model):

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
    producto = models.ForeignKey(Productos, to_field='codigo', on_delete=models.PROTECT, db_column='producto',related_name='prod_carga_em')
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True,choices=choice_tipo)
    fechaembarque = models.DateTimeField(blank=True, null=True)
    cbm = models.FloatField(blank=True, null=True)
    mercaderia = models.TextField(blank=True, null=True)
    marcas = models.CharField(db_column='Marcas', max_length=150, blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=15, blank=True, null=True)  # Field name made lowercase.
    sobredimensionada = models.CharField(db_column='Sobredimensionada', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_cargaaerea'


class ExpmaritClavenrohouse(models.Model):
    numero = models.IntegerField(db_column='Numero', primary_key=True)  # Field name made lowercase.
    embarque = models.IntegerField(db_column='Embarque', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_clavenrohouse'


class ExpmaritClaveposicion(models.Model):
    posicion = models.CharField(primary_key=True, max_length=15)
    numeroorden = models.SmallIntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_claveposicion'


class ExpmaritConexaerea(models.Model):
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
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=50, blank=True, null=True)
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(max_length=15,choices=choice_modo)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True, null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_conexaerea'


class ExpmaritConexreserva(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vapor = models.CharField(max_length=30, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(max_length=10, blank=True, null=True)
    modo = models.CharField(max_length=15, blank=True, null=True)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True, null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_conexreserva'


class ExpmaritEmbarqueaereo(models.Model):
    numero = models.IntegerField(primary_key=True)
    cliente = models.IntegerField(blank=True, null=True)
    consignatario = models.IntegerField(blank=True, null=True)
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
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=40, blank=True, null=True)
    transportista = models.IntegerField(blank=True, null=True)
    valortransporte = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valoraduana = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    fechaembarque = models.DateTimeField(blank=True, null=True)
    fecharetiro = models.DateTimeField(blank=True, null=True)
    pagoflete = models.CharField(max_length=10, blank=True, null=True)
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    valorseguro = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifaventa = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifacompra = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    volumencubico = models.FloatField(blank=True, null=True)
    cotizacion = models.IntegerField(blank=True, null=True)
    cotitransp = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    agente = models.IntegerField(blank=True, null=True)
    transdestino = models.IntegerField(blank=True, null=True)
    facturado = models.CharField(max_length=1, blank=True, null=True)
    profitage = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    notificar = models.IntegerField(db_column='Notificar', blank=True, null=True)  # Field name made lowercase.
    vaporcli = models.CharField(db_column='Vaporcli', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vaporcli2 = models.CharField(db_column='Vaporcli2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tipovend = models.CharField(db_column='Tipovend', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendedor = models.SmallIntegerField(db_column='Vendedor', blank=True, null=True)  # Field name made lowercase.
    comivend = models.FloatField(db_column='Comivend', blank=True, null=True)  # Field name made lowercase.
    aplicaprofit = models.IntegerField(db_column='Aplicaprofit', blank=True, null=True)  # Field name made lowercase.
    nroreferedi = models.IntegerField(blank=True, null=True)
    ordencliente = models.CharField(max_length=850, blank=True, null=True)
    armador = models.IntegerField(blank=True, null=True)
    viaje = models.CharField(max_length=20, blank=True, null=True)
    propia = models.IntegerField(blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    booking = models.CharField(max_length=30, blank=True, null=True)
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=250, blank=True, null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=250, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    depcontenedoringreso = models.SmallIntegerField(db_column='DepContenedorIngreso', blank=True, null=True)  # Field name made lowercase.
    depcontenedorvacios = models.SmallIntegerField(db_column='DepContenedorVacios', blank=True, null=True)  # Field name made lowercase.
    agenteportuario = models.IntegerField(db_column='AgentePortuario', blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    deadborrador = models.DateTimeField(db_column='DeadBorrador', blank=True, null=True)  # Field name made lowercase.
    deaddocumentos = models.DateTimeField(db_column='DeadDocumentos', blank=True, null=True)  # Field name made lowercase.
    deadentrega = models.DateTimeField(db_column='DeadEntrega', blank=True, null=True)  # Field name made lowercase.
    deadliberacion = models.DateTimeField(db_column='DeadLiberacion', blank=True, null=True)  # Field name made lowercase.
    retiravacio = models.DateTimeField(db_column='RetiraVacio', blank=True, null=True)  # Field name made lowercase.
    retiralleno = models.DateTimeField(db_column='RetiraLleno', blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=250, blank=True, null=True)  # Field name made lowercase.
    imprimiobl = models.CharField(db_column='ImprimioBL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hblcorp = models.IntegerField(db_column='HBLCorp', blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)  # Field name made lowercase.
    datosnotificante = models.CharField(db_column='DatosNotificante', max_length=250, blank=True, null=True)  # Field name made lowercase.
    contactoemergencia = models.CharField(db_column='ContactoEmergencia', max_length=100, blank=True, null=True)  # Field name made lowercase.
    numerocomunicacion = models.CharField(db_column='NumeroComunicacion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    fechaentrega = models.DateTimeField(db_column='FechaEntrega', blank=True, null=True)  # Field name made lowercase.
    aquienentrega = models.CharField(db_column='aQuienEntrega', max_length=30, blank=True, null=True)  # Field name made lowercase.
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    salidasim = models.DateTimeField(db_column='SalidaSIM', blank=True, null=True)  # Field name made lowercase.
    presentasim = models.DateTimeField(db_column='PresentaSIM', blank=True, null=True)  # Field name made lowercase.
    cierresim = models.DateTimeField(db_column='CierreSIM', blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    imprimioorig = models.CharField(db_column='ImprimioOrig', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enviointtrabk = models.CharField(db_column='EnvioInttraBK', max_length=10, blank=True, null=True)  # Field name made lowercase.
    enviointtrasi = models.CharField(db_column='EnvioInttraSI', max_length=10, blank=True, null=True)  # Field name made lowercase.
    maerskbk = models.CharField(db_column='MaerskBK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    maersksi = models.CharField(db_column='MaerskSI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tipobl = models.CharField(db_column='TipoBL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechacutoff = models.DateTimeField(db_column='FechaCutOff', blank=True, null=True)  # Field name made lowercase.
    horacutoff = models.CharField(db_column='HoraCutOff', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fecharetiromercaderia = models.DateTimeField(db_column='FechaRetiroMercaderia', blank=True, null=True)  # Field name made lowercase.
    fechainiciostacking = models.DateTimeField(db_column='FechaInicioStacking', blank=True, null=True)  # Field name made lowercase.
    horainiciostacking = models.CharField(db_column='HoraInicioStacking', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fechafinstacking = models.DateTimeField(db_column='FechaFinStacking', blank=True, null=True)  # Field name made lowercase.
    horafinstacking = models.CharField(db_column='HoraFinStacking', max_length=30, blank=True, null=True)  # Field name made lowercase.
    emisionbl = models.DateTimeField(db_column='EmisionBL', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)  # Field name made lowercase.
    envioeasipassbk = models.CharField(db_column='EnvioEASIPASSBK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    envioeasipasssi = models.CharField(db_column='EnvioEASIPASSSI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    demora = models.SmallIntegerField(db_column='Demora', blank=True, null=True)  # Field name made lowercase.
    valordemoravta = models.DecimalField(db_column='ValorDemoraVTA', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    truckerarrivaltime = models.CharField(db_column='TruckerArrivalTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    fechacutoffvgm = models.DateTimeField(db_column='FechaCutOffVGM', blank=True, null=True)  # Field name made lowercase.
    horacutoffvgm = models.CharField(db_column='HoraCutOffVGM', max_length=30, blank=True, null=True)  # Field name made lowercase.
    emitebloriginal = models.CharField(db_column='EmiteBLOriginal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.DateTimeField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_embarqueaereo'

    def get_number(self):
        embarque_l = ExpmaritEmbarqueaereo.objects.order_by('numero').last()
        if embarque_l:
            nuevo_numero = embarque_l.numero + 1
        else:
            nuevo_numero = 1

        return nuevo_numero

class ExpmaritEntregadoc(models.Model):
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
        db_table = 'expmarit_entregadoc'


class ExpmaritEnvases(models.Model):

    choice_unidad = (
        ("20","20"),
        ("40","40"),
        ("45","45"),
        ("CBM","CBM"),
        ("CF","CF"),
        ("TON","TON"),
        ("M/T","M/T"),
        ("MIN","MIN"),
        ("FLAT","FLAT"),
        ("UNIT","UNIT"),
        ("LBS","LBS"),
    )
    choice_tipo = (
        ("Reefer","Reefer"),
        ("Hi Cube Reefer","Hi Cube Reefer"),
        ("Box","Box"),
        ("N.O.R.","N.O.R."),
        ("Hi Cube","Hi Cube"),
        ("Dry","Dry"),
        ("Standard","Standard"),
        ("Part Container","Part Container"),
        ("CBM","CBM"),
        ("Open Top","Open Top"),
    )
    choice_movimiento = (
        ("FCL/FCL","FCL/FCL"),
        ("FCL/LCL","FCL/LCL"),
        ("LCL/FCL","LCL/FCL"),
        ("LCL/LCL","LCL/LCL"),
        ("CY/CY","CY/CY"),
        ("CY/SD","CY/SD"),
        ("SD/SD","SD/SD"),
        ("SD/CY","SD/CY"),
        ("SD/CY","SD/CY"),
        ("Break Bulk","Break Bulk"),
        ("Ro/Ro","Ro/Ro"),
    )
    choice_terminos = (
        ("FILO","FILO"),
        ("FIOS","FIOS"),
        ("FLT","FLT"),
        ("LIFO","LIFO"),
        ("LT","LT"),
    )
    choice_envase = (
        ("S/I","Seleccionar"),
        ("Bags","Bags"),
        ("Bales","Bales"),
        ("Big bags","Big bags"),
        ("Bing","Bing"),
        ("Boxes","Boxes"),
        ("Bulk","Bulk"),
        ("Bundles","Bundles"),
        ("Cartons","Cartons"),
        ("Cases","Cases"),
        ("Container","Container"),
        ("Crates","Crates"),
        ("Cylinder","Cylinder"),
        ("Declared","Declared"),
        ("Drums","Drums"),
        ("Envelope","Envelope"),
        ("Fireboard","Fireboard"),
        ("Flexitank","Flexitank"),
        ("Gallons","Gallons"),
        ("Jumbo","Jumbo"),
        ("Lot","Lot"),
        ("Packages","Packages"),
        ("Pallets","Pallets"),
        ("Pieces","Pieces"),
        ("Pipe","Pipe"),
        ("Platforms","Platforms"),
        ("Plywood case","Plywood case"),
        ("Reels","Reels"),
        ("Rolls","Rolls"),
        ("Sacks","Sacks"),
        ("Set","Set"),
        ("Skids","Skids"),
        ("Steel Pallets","Steel Pallets"),
        ("Tank","Tank"),
        ("Units","Units"),
        ("Wooden case","Wooden case"),
        ("Wooden rack","Wooden rack"),
    )
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=25,choices=choice_unidad)
    tipo = models.CharField(max_length=20, choices=choice_tipo)
    movimiento = models.CharField(max_length=30, choices=choice_movimiento)
    terminos = models.CharField(max_length=5, choices=choice_terminos)
    cantidad = models.FloatField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    marcas = models.CharField(max_length=250, blank=True, null=True)
    precinto = models.CharField(max_length=100, blank=True, null=True)
    tara = models.FloatField(blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    envase = models.CharField(db_column='Envase', max_length=15,choices=choice_envase,default='S/I')  # Field name made lowercase.
    bultos = models.IntegerField(blank=True, null=True)
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(max_length=100, blank=True, null=True)
    volumen = models.FloatField(blank=True, null=True)
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    temperatura = models.FloatField(db_column='Temperatura', blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ventilacion = models.CharField(db_column='Ventilacion', max_length=20, blank=True, null=True)  # Field name made lowercase.
    genset = models.CharField(db_column='GenSet', max_length=1, blank=True, null=True)  # Field name made lowercase.
    atmosferacontrolada = models.CharField(db_column='AtmosferaControlada', max_length=1, blank=True, null=True)  # Field name made lowercase.
    consolidacion = models.SmallIntegerField(db_column='Consolidacion', blank=True, null=True)  # Field name made lowercase.
    tipoventilacion = models.CharField(db_column='TipoVentilacion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pesovgm = models.FloatField(db_column='PesoVGM', blank=True, null=True)  # Field name made lowercase.
    humedad = models.SmallIntegerField(db_column='Humedad', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_envases'


class ExpmaritFaxes(models.Model):
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
        db_table = 'expmarit_faxes'


class ExpmaritFisico(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    marcas = models.CharField(db_column='Marcas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    precinto = models.CharField(db_column='Precinto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tara = models.IntegerField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    detalle2 = models.CharField(max_length=50, blank=True, null=True)
    cliente = models.IntegerField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_fisico'


class ExpmaritGastoshijos(models.Model):
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
    movimiento = models.CharField(db_column='Movimiento', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_gastoshijos'


class ExpmaritGuiasgrabadas(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    empresa = models.CharField(max_length=35, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    pais = models.CharField(max_length=22, blank=True, null=True)
    localidad = models.CharField(max_length=22, blank=True, null=True)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    cliente1 = models.CharField(max_length=50, blank=True, null=True)
    cliente2 = models.CharField(max_length=50, blank=True, null=True)
    cliente3 = models.CharField(max_length=50, blank=True, null=True)
    cliente4 = models.CharField(max_length=50, blank=True, null=True)
    consigna = models.CharField(max_length=50, blank=True, null=True)
    direcconsigna = models.CharField(max_length=50, blank=True, null=True)
    localconsigna = models.CharField(max_length=50, blank=True, null=True)
    teleconsigna = models.CharField(max_length=50, blank=True, null=True)
    otralinea = models.CharField(max_length=50, blank=True, null=True)
    notif = models.CharField(max_length=50, blank=True, null=True)
    dirnotif = models.CharField(max_length=50, blank=True, null=True)
    otralinea2 = models.CharField(max_length=50, blank=True, null=True)
    telnotif = models.CharField(max_length=50, blank=True, null=True)
    tipoflete = models.CharField(max_length=45, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    salede = models.CharField(max_length=35, blank=True, null=True)
    vapor = models.CharField(max_length=35, blank=True, null=True)
    viaje = models.CharField(max_length=35, blank=True, null=True)
    loading = models.CharField(max_length=35, blank=True, null=True)
    discharge = models.CharField(max_length=35, blank=True, null=True)
    delivery = models.CharField(max_length=35, blank=True, null=True)
    transterms = models.CharField(max_length=35, blank=True, null=True)
    simbolo = models.CharField(max_length=4, blank=True, null=True)
    condentrega = models.CharField(max_length=20, blank=True, null=True)
    tipomov = models.CharField(max_length=15, blank=True, null=True)
    carriage = models.CharField(max_length=10, blank=True, null=True)
    custom = models.CharField(max_length=10, blank=True, null=True)
    valseguro = models.CharField(max_length=10, blank=True, null=True)
    goods = models.TextField(blank=True, null=True)
    free1 = models.CharField(max_length=45, blank=True, null=True)
    free2 = models.CharField(max_length=45, blank=True, null=True)
    free3 = models.CharField(max_length=45, blank=True, null=True)
    signature = models.CharField(max_length=50, blank=True, null=True)
    signature2 = models.CharField(max_length=50, blank=True, null=True)
    signature3 = models.CharField(max_length=50, blank=True, null=True)
    nbls = models.CharField(max_length=2, blank=True, null=True)
    payable = models.CharField(max_length=40, blank=True, null=True)
    board = models.CharField(max_length=15, blank=True, null=True)
    clean = models.CharField(max_length=30, blank=True, null=True)
    fechaemi = models.CharField(max_length=12, blank=True, null=True)
    restotext = models.CharField(max_length=45, blank=True, null=True)
    portext = models.CharField(max_length=50, blank=True, null=True)
    vadeclared = models.IntegerField(blank=True, null=True)
    cliente5 = models.CharField(max_length=50, blank=True, null=True)
    otranotif = models.CharField(max_length=50, blank=True, null=True)
    signature4 = models.CharField(max_length=50, blank=True, null=True)
    signature5 = models.CharField(max_length=50, blank=True, null=True)
    booking = models.CharField(max_length=30, blank=True, null=True)
    position2 = models.CharField(max_length=50, blank=True, null=True)
    origin = models.CharField(db_column='Origin', max_length=35, blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', max_length=35, blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=3, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    awb = models.CharField(db_column='AWB', max_length=40, blank=True, null=True)  # Field name made lowercase.
    hawb = models.CharField(db_column='HAWB', max_length=50, blank=True, null=True)  # Field name made lowercase.
    totalkilos = models.FloatField(db_column='TotalKilos', blank=True, null=True)  # Field name made lowercase.
    totalpaquetes = models.IntegerField(db_column='TotalPaquetes', blank=True, null=True)  # Field name made lowercase.
    tipodocumento = models.CharField(db_column='TipoDocumento', max_length=1, blank=True, null=True)  # Field name made lowercase.
    consolidado = models.IntegerField(db_column='Consolidado', blank=True, null=True)  # Field name made lowercase.
    mensaje1 = models.IntegerField(db_column='Mensaje1', blank=True, null=True)  # Field name made lowercase.
    mensaje2 = models.IntegerField(db_column='Mensaje2', blank=True, null=True)  # Field name made lowercase.
    label6 = models.CharField(db_column='Label6', max_length=50, blank=True, null=True)  # Field name made lowercase.
    texto = models.TextField(db_column='Texto', blank=True, null=True)  # Field name made lowercase.
    consigna6 = models.CharField(db_column='Consigna6', max_length=50, blank=True, null=True)  # Field name made lowercase.
    consigna7 = models.CharField(db_column='Consigna7', max_length=50, blank=True, null=True)  # Field name made lowercase.
    consigna8 = models.CharField(db_column='Consigna8', max_length=50, blank=True, null=True)  # Field name made lowercase.
    precarriage = models.CharField(db_column='PreCarriage', max_length=35, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_guiasgrabadas'


class ExpmaritGuiasgrabadas2(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    marks = models.CharField(max_length=30, blank=True, null=True)
    packages = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    gross = models.CharField(max_length=30, blank=True, null=True)
    tare = models.CharField(max_length=30, blank=True, null=True)
    tara2 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expmarit_guiasgrabadas2'


class ExpmaritGuiasgrabadas3(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    servicio = models.CharField(db_column='Servicio', max_length=50, blank=True, null=True)  # Field name made lowercase.
    prepaid = models.CharField(db_column='Prepaid', max_length=10, blank=True, null=True)  # Field name made lowercase.
    collect = models.CharField(db_column='Collect', max_length=10, blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_guiasgrabadas3'


class ExpmaritMadresgrabadas(models.Model):
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
    notif = models.CharField(max_length=45, blank=True, null=True)
    dirnotif = models.CharField(max_length=45, blank=True, null=True)
    otralinea2 = models.CharField(max_length=45, blank=True, null=True)
    telnotif = models.CharField(max_length=45, blank=True, null=True)
    tipoflete = models.CharField(max_length=45, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    salede = models.CharField(max_length=35, blank=True, null=True)
    vapor = models.CharField(max_length=35, blank=True, null=True)
    viaje = models.CharField(max_length=35, blank=True, null=True)
    loading = models.CharField(max_length=35, blank=True, null=True)
    discharge = models.CharField(max_length=35, blank=True, null=True)
    delivery = models.CharField(max_length=35, blank=True, null=True)
    transterms = models.CharField(max_length=35, blank=True, null=True)
    simbolo = models.CharField(max_length=4, blank=True, null=True)
    condentrega = models.CharField(max_length=20, blank=True, null=True)
    tipomov = models.CharField(max_length=15, blank=True, null=True)
    carriage = models.CharField(max_length=10, blank=True, null=True)
    custom = models.CharField(max_length=10, blank=True, null=True)
    valseguro = models.CharField(max_length=10, blank=True, null=True)
    goods = models.TextField(blank=True, null=True)
    free1 = models.CharField(max_length=45, blank=True, null=True)
    free2 = models.CharField(max_length=45, blank=True, null=True)
    free3 = models.CharField(max_length=45, blank=True, null=True)
    signature = models.CharField(max_length=45, blank=True, null=True)
    signature2 = models.CharField(max_length=45, blank=True, null=True)
    signature3 = models.CharField(max_length=45, blank=True, null=True)
    nbls = models.CharField(max_length=2, blank=True, null=True)
    payable = models.CharField(max_length=15, blank=True, null=True)
    board = models.CharField(max_length=15, blank=True, null=True)
    clean = models.CharField(max_length=30, blank=True, null=True)
    fechaemi = models.CharField(max_length=12, blank=True, null=True)
    restotext = models.CharField(max_length=45, blank=True, null=True)
    portext = models.CharField(max_length=15, blank=True, null=True)
    vadeclared = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expmarit_madresgrabadas'


class ExpmaritMadresgrabadas2(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    marks = models.CharField(max_length=30, blank=True, null=True)
    packages = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    gross = models.CharField(max_length=30, blank=True, null=True)
    tare = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expmarit_madresgrabadas2'


class ExpmaritReservas(models.Model):
    numero = models.IntegerField(db_column='Numero', primary_key=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    kilos = models.FloatField(db_column='Kilos', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    awb = models.CharField(max_length=40, blank=True, null=True)
    agente = models.IntegerField(blank=True, null=True)
    consignatario = models.IntegerField(blank=True, null=True)
    pagoflete = models.CharField(db_column='Pagoflete', max_length=10, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    volumen = models.FloatField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    aduana = models.CharField(max_length=30, blank=True, null=True)
    profitage = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifapl = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=20, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=30, blank=True, null=True)  # Field name made lowercase.
    envioedi = models.CharField(max_length=1, blank=True, null=True)
    nroreferedi = models.IntegerField(blank=True, null=True)
    ciep = models.CharField(max_length=15, blank=True, null=True)
    armador = models.IntegerField(blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    plfacturado = models.CharField(max_length=1, blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enviointtrabk = models.CharField(db_column='EnvioInttraBK', max_length=10, blank=True, null=True)  # Field name made lowercase.
    enviointtrasi = models.CharField(db_column='EnvioInttraSI', max_length=10, blank=True, null=True)  # Field name made lowercase.
    maerskbk = models.CharField(db_column='MaerskBK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    maersksi = models.CharField(db_column='MaerskSI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    esagente = models.CharField(db_column='esAgente', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    tipobl = models.CharField(db_column='TipoBL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', max_length=30, blank=True, null=True)  # Field name made lowercase.
    deposito = models.SmallIntegerField(db_column='Deposito', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_reservas'

    def get_number(self):
        reserva_l = ExpmaritReservas.objects.order_by('numero').last()
        if reserva_l:
            nuevo_numero = reserva_l.numero + 1
        else:
            nuevo_numero = 1

        return nuevo_numero


class ExpmaritServiceaereo(models.Model):
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
        db_table = 'expmarit_serviceaereo'


class ExpmaritServireserva(models.Model):
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
        db_table = 'expmarit_servireserva'


class ExpmaritTraceop(models.Model):
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
        db_table = 'expmarit_traceop'

class Master(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True, primary_key=True)  # Añadir primary_key=True
    transportista = models.CharField(max_length=400,blank=True, null=True)
    agente = models.CharField(max_length=400,blank=True, null=True)
    embarcador = models.CharField(db_column='consignatario',max_length=400,blank=True, null=True)
    vapor = models.CharField(db_column='Vapor',max_length=400,blank=True, null=True)
    origen = models.CharField(max_length=400,blank=True, null=True)
    destino = models.CharField(max_length=400,blank=True, null=True)
    status = models.CharField(max_length=400,blank=True, null=True)
    armador = models.CharField(max_length=400,blank=True, null=True)
    awb = models.CharField(max_length=400, blank=True, null=True)
    llegada = models.DateField(blank=True, null=True)
    seguimientos = models.TextField( blank=True, null=True)
    hawbs = models.TextField( blank=True, null=True)

    def __str__(self,):
        return self.numero

    class Meta:
        managed = False
        db_table = 'VExpMaritMaster'

class VEmbarqueaereo(models.Model):
    numero = models.IntegerField(unique=True, primary_key=True)
    consignatario_id = models.IntegerField()
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    consignatario_codigo = models.IntegerField()

    transportista = models.CharField(max_length=255, blank=True, null=True)  # Nombre del transportista
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=255, blank=True, null=True)  # Nombre del agente
    consignatario = models.CharField(max_length=255, blank=True, null=True)  # Nombre del consignatario
    armador = models.CharField(max_length=255, blank=True, null=True)  # Nombre del armador
    vapor = models.CharField(max_length=30, blank=True, null=True)
    posicion = models.CharField(max_length=20, blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    fecha_embarque = models.DateTimeField(blank=True, null=True)
    fecha_retiro = models.DateTimeField(blank=True, null=True)
    agenteportuario = models.DateTimeField(blank=True, null=True)
    valor_transporte = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valor_aduana = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifa_venta = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifa_compra = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    volumen_cubico = models.FloatField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    viaje = models.CharField(max_length=20, null=True, blank=True, default=None)
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
        db_table = 'VExpMaritEmbarqueAereo'
class VEmbarqueaereoDirecto(models.Model):
    consignatario_codigo = models.IntegerField()
    numero = models.IntegerField(unique=True, primary_key=True)
    consignatario_id = models.IntegerField()
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)

    transportista = models.CharField(max_length=255, blank=True, null=True)  # Nombre del transportista
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=255, blank=True, null=True)  # Nombre del agente
    consignatario = models.CharField(max_length=255, blank=True, null=True)  # Nombre del consignatario
    armador = models.CharField(max_length=255, blank=True, null=True)  # Nombre del armador
    vapor = models.CharField(max_length=30, blank=True, null=True)
    posicion = models.CharField(max_length=20, blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    fecha_embarque = models.DateTimeField(blank=True, null=True)
    fecha_retiro = models.DateTimeField(blank=True, null=True)
    agenteportuario = models.DateTimeField(blank=True, null=True)
    valor_transporte = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valor_aduana = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifa_venta = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifa_compra = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    volumen_cubico = models.FloatField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    viaje = models.CharField(max_length=20, null=True, blank=True, default=None)
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
        db_table = 'VExpMaritEmbarqueAereoDirecto'
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
        db_table = 'VExpMaritGastosMaster'

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
        db_table = 'VExpMaritGastosHouse'

from auditlog.registry import auditlog

class MyModel(models.Model):
    history = AuditlogHistoryField()
    # Model definition goes here


auditlog.register(MyModel)

from inspect import getmembers
from auditlog.registry import auditlog
from expmarit import models

tablas = getmembers(models)
for t in tablas:
    try:
        auditlog.register(t[1], serialize_data=True)
    except Exception as e:
        pass