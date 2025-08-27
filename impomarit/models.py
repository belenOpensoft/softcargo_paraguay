from auditlog.models import AuditlogHistoryField
from django.contrib.auth.models import User
from django.db import models

from mantenimientos.models import Productos


class Anulados(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)


class Attachhijo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impmarit_attachhijo'


class Attachmadre(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)


class Cargaaerea(models.Model):
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
    numero = models.IntegerField(blank=True, null=True)
    producto = models.ForeignKey(Productos, to_field='codigo', on_delete=models.PROTECT, db_column='producto',
                                 related_name='prod_carga_im')
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True, choices=choice_tipo)
    fechaembarque = models.DateTimeField(blank=True, null=True)
    cbm = models.FloatField(blank=True, null=True)
    mercaderia = models.TextField(blank=True, null=True)  # This field type is a guess.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impmarit_cargaaerea'


class Clavenrohouse(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True)
    embarque = models.IntegerField(db_column='Embarque', blank=True, null=True)


class Claveposicion(models.Model):
    posicion = models.CharField(unique=True, max_length=15)
    numeroorden = models.SmallIntegerField(db_column='NumeroOrden', blank=True, null=True)


class Conexreserva(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vapor = models.CharField(max_length=30, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=50, blank=True, null=True)
    viaje = models.CharField(max_length=10, blank=True, null=True)
    modo = models.CharField(max_length=15, blank=True, null=True)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True, null=True)
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True, null=True)


class Embarqueaereo(models.Model):
    numero = models.IntegerField(unique=True)
    cliente = models.IntegerField(blank=True, null=True)
    consignatario = models.IntegerField(blank=True, null=True)
    despachante = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    consolidado = models.SmallIntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=20, blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    aduana = models.CharField(max_length=30, blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    pago = models.SmallIntegerField(blank=True, null=True)
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=50, blank=True, null=True)
    transportista = models.IntegerField(blank=True, null=True)
    valortransporte = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valoraduana = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    fechaembarque = models.DateTimeField(blank=True, null=True)
    fecharetiro = models.DateTimeField(blank=True, null=True)
    pagoflete = models.CharField(max_length=1, blank=True, null=True)
    notas = models.TextField(db_column='Notas', blank=True, null=True)
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
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)
    notificar = models.IntegerField(db_column='Notificar', blank=True, null=True)
    vaporcli = models.CharField(db_column='Vaporcli', max_length=1, blank=True, null=True)
    vaporcli2 = models.CharField(db_column='Vaporcli2', max_length=1, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)
    terminal = models.SmallIntegerField(blank=True, null=True)
    tipovend = models.CharField(db_column='Tipovend', max_length=1, blank=True, null=True)
    vendedor = models.SmallIntegerField(db_column='Vendedor', blank=True, null=True)
    comivend = models.FloatField(db_column='Comivend', blank=True, null=True)
    aplicaprofit = models.IntegerField(db_column='Aplicaprofit', blank=True, null=True)
    nroreferedi = models.IntegerField(blank=True, null=True)
    notomaprofit = models.BooleanField(blank=True, null=True)
    ordencliente = models.CharField(max_length=850, blank=True, null=True)
    desconsolida = models.CharField(max_length=60, blank=True, null=True)
    armador = models.IntegerField(blank=True, null=True)
    viaje = models.CharField(max_length=20, blank=True, null=True)
    propia = models.BooleanField(blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    fechaentrega = models.DateTimeField(blank=True, null=True)
    aquienentrega = models.CharField(max_length=30, blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    originales = models.CharField(max_length=1, blank=True, null=True)
    fechalimitedemora = models.DateTimeField(db_column='FechaLimiteDemora', blank=True, null=True)
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=250, blank=True, null=True)
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=250, blank=True, null=True)
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True, null=True)
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True, null=True)
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=19, decimal_places=4, blank=True,
                                           null=True)
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)
    loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True, null=True)
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)
    tieneacta = models.CharField(db_column='TieneActa', max_length=1, blank=True, null=True)
    refproveedor = models.CharField(db_column='RefProveedor', max_length=250, blank=True, null=True)
    deaddocumentos = models.DateTimeField(db_column='DeadDocumentos', blank=True, null=True)
    deadentrega = models.DateTimeField(db_column='DeadEntrega', blank=True, null=True)
    hblcorp = models.IntegerField(db_column='HBLCorp', blank=True, null=True)
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)
    desconsolidadeposito = models.CharField(db_column='DesconsolidaDeposito', max_length=1, blank=True, null=True)
    demora = models.SmallIntegerField(db_column='Demora', blank=True, null=True)
    valordemoravta = models.DecimalField(db_column='ValorDemoraVTA', max_digits=19, decimal_places=4, blank=True,
                                         null=True)
    valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=19, decimal_places=4, blank=True,
                                         null=True)
    enviointercomex = models.CharField(db_column='EnvioIntercomex', max_length=1, blank=True, null=True)
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)
    arribosim = models.DateTimeField(db_column='ArriboSIM', blank=True, null=True)
    presentasim = models.DateTimeField(db_column='PresentaSIM', blank=True, null=True)
    cierresim = models.DateTimeField(db_column='CierreSIM', blank=True, null=True)
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=50, blank=True, null=True)
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=50, blank=True, null=True)
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=50, blank=True, null=True)
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=50, blank=True, null=True)
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=50, blank=True, null=True)
    manifiesto = models.CharField(db_column='Manifiesto', max_length=30, blank=True, null=True)
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)
    emisionbl = models.DateTimeField(db_column='EmisionBL', blank=True, null=True)
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    fechafinoperativa = models.DateTimeField(db_column='FechaFinOperativa', blank=True, null=True)
    horafinoperativa = models.CharField(db_column='HoraFinOperativa', max_length=8, blank=True, null=True)
    fechadocsdisp = models.DateTimeField(db_column='FechaDocsDisp', blank=True, null=True)
    horadocsdisp = models.CharField(db_column='HoraDocsDisp', max_length=8, blank=True, null=True)
    fechadocsret = models.DateTimeField(db_column='FechaDocsRet', blank=True, null=True)
    horadocsret = models.CharField(db_column='HoraDocsRet', max_length=8, blank=True, null=True)
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)
    tipobl = models.CharField(db_column='TipoBL', max_length=10, blank=True, null=True)
    emitebloriginal = models.CharField(db_column='EmiteBLOriginal', max_length=1, blank=True, null=True)
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)
    eta = models.DateTimeField(db_column='ETA', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impmarit_embarqueaereo'

    def get_number(self):
        embarque_l = Embarqueaereo.objects.order_by('id').last()
        if embarque_l:
            nuevo_numero = embarque_l.numero + 1
        else:
            nuevo_numero = 1

        return nuevo_numero


class VEmbarqueaereo(models.Model):
    numero = models.IntegerField(unique=True)
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    transportista = models.CharField(max_length=255, blank=True, null=True)  # Nombre del transportista
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=255, blank=True, null=True)  # Nombre del agente
    consignatario = models.CharField(max_length=255, blank=True, null=True)  # Nombre del consignatario
    consignatario_codigo = models.IntegerField()
    consignatario_id = models.IntegerField()
    armador = models.CharField(max_length=255, blank=True, null=True)  # Nombre del armador
    vapor = models.CharField(max_length=30, blank=True, null=True)
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
        db_table = 'VEmbarqueAereo'

class VEmbarqueaereoDirecto(models.Model):
    numero = models.IntegerField(unique=True)
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    transportista = models.CharField(max_length=255, blank=True, null=True)  # Nombre del transportista
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=255, blank=True, null=True)  # Nombre del agente
    consignatario = models.CharField(max_length=255, blank=True, null=True)  # Nombre del consignatario
    consignatario_codigo = models.IntegerField()
    consignatario_id = models.IntegerField()
    armador = models.CharField(max_length=255, blank=True, null=True)  # Nombre del armador
    vapor = models.CharField(max_length=30, blank=True, null=True)
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
        db_table = 'VEmbarqueAereoDirecto'


class Entregadoc(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)
    entreguese = models.CharField(db_column='Entreguese', max_length=1, blank=True, null=True)
    nombreentrega = models.CharField(db_column='NombreEntrega', max_length=50, blank=True, null=True)
    direccionentrega = models.CharField(db_column='DireccionEntrega', max_length=50, blank=True, null=True)
    ciudadentrega = models.CharField(db_column='CiudadEntrega', max_length=30, blank=True, null=True)
    telefonoentrega = models.CharField(db_column='TelefonoEntrega', max_length=30, blank=True, null=True)
    original = models.CharField(db_column='Original', max_length=1, blank=True, null=True)
    lista = models.CharField(db_column='Lista', max_length=1, blank=True, null=True)
    certorigen = models.CharField(db_column='CertOrigen', max_length=1, blank=True, null=True)
    declara = models.CharField(db_column='Declara', max_length=1, blank=True, null=True)
    certflete = models.CharField(db_column='CertFlete', max_length=1, blank=True, null=True)
    cerseguro = models.CharField(db_column='CerSeguro', max_length=1, blank=True, null=True)
    copiahbl = models.CharField(db_column='CopiaHBL', max_length=1, blank=True, null=True)
    otros = models.CharField(db_column='Otros', max_length=1, blank=True, null=True)
    detotros = models.CharField(db_column='DetOtros', max_length=50, blank=True, null=True)
    detotros2 = models.CharField(db_column='DetOtros2', max_length=50, blank=True, null=True)
    ordendep = models.CharField(db_column='OrdenDep', max_length=1, blank=True, null=True)
    certgastos = models.CharField(db_column='CertGastos', max_length=1, blank=True, null=True)
    libre = models.CharField(db_column='Libre', max_length=1, blank=True, null=True)
    eur1 = models.CharField(db_column='Eur1', max_length=1, blank=True, null=True)
    factura = models.CharField(db_column='Factura', max_length=1, blank=True, null=True)
    nuestra = models.CharField(db_column='Nuestra', max_length=1, blank=True, null=True)
    certcalidad = models.CharField(db_column='CertCalidad', max_length=1, blank=True, null=True)
    cumplido = models.CharField(db_column='Cumplido', max_length=1, blank=True, null=True)
    transfer = models.CharField(db_column='Transfer', max_length=1, blank=True, null=True)
    certpeligroso = models.CharField(db_column='CertPeligroso', max_length=1, blank=True, null=True)
    imprimecom = models.CharField(db_column='ImprimeCom', max_length=1, blank=True, null=True)
    remarks = models.CharField(db_column='Remarks', max_length=80, blank=True, null=True)
    remarks2 = models.CharField(db_column='Remarks2', max_length=80, blank=True, null=True)
    facturacom = models.CharField(db_column='FacturaCom', max_length=40, blank=True, null=True)
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True, null=True)
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True, null=True)
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', max_length=40, blank=True, null=True)
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True, null=True)
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', max_length=40, blank=True, null=True)
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)
    crtnumero = models.CharField(db_column='CRTNumero', max_length=40, blank=True, null=True)
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True, null=True)
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', max_length=40, blank=True,
                                               null=True)
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)
    micdtanumero = models.CharField(db_column='MicDtaNumero', max_length=40, blank=True, null=True)
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)
    papeletanumero = models.CharField(db_column='PapeletaNumero', max_length=40, blank=True, null=True)
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True, null=True)
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', max_length=40, blank=True, null=True)
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', max_length=40, blank=True, null=True)
    certorigennumero = models.CharField(db_column='CertOrigenNumero', max_length=40, blank=True, null=True)
    certseguronumero = models.CharField(db_column='CertSeguroNumero', max_length=40, blank=True, null=True)
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', max_length=40, blank=True, null=True)
    detotros3 = models.CharField(db_column='DetOtros3', max_length=50, blank=True, null=True)
    detotros4 = models.CharField(db_column='DetOtros4', max_length=50, blank=True, null=True)


class Envases(models.Model):
    choice_unidad = (
        ("20", "20"),
        ("40", "40"),
        ("45", "45"),
        ("CBM", "CBM"),
        ("CF", "CF"),
        ("TON", "TON"),
        ("M/T", "M/T"),
        ("MIN", "MIN"),
        ("FLAT", "FLAT"),
        ("UNIT", "UNIT"),
        ("LBS", "LBS"),
    )
    choice_tipo = (
        ("Reefer", "Reefer"),
        ("Hi Cube Reefer", "Hi Cube Reefer"),
        ("Box", "Box"),
        ("N.O.R.", "N.O.R."),
        ("Hi Cube", "Hi Cube"),
        ("Dry", "Dry"),
        ("Standard", "Standard"),
        ("Part Container", "Part Container"),
        ("CBM", "CBM"),
        ("Open Top", "Open Top"),
    )
    choice_movimiento = (
        ("FCL/FCL", "FCL/FCL"),
        ("FCL/LCL", "FCL/LCL"),
        ("LCL/FCL", "LCL/FCL"),
        ("LCL/LCL", "LCL/LCL"),
        ("CY/CY", "CY/CY"),
        ("CY/SD", "CY/SD"),
        ("SD/SD", "SD/SD"),
        ("SD/CY", "SD/CY"),
        ("SD/CY", "SD/CY"),
        ("Break Bulk", "Break Bulk"),
        ("Ro/Ro", "Ro/Ro"),
    )
    choice_terminos = (
        ("FILO", "FILO"),
        ("FIOS", "FIOS"),
        ("FLT", "FLT"),
        ("LIFO", "LIFO"),
        ("LT", "LT"),
    )
    choice_envase = (
        ("S/I", "Seleccionar"),
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
    numero = models.IntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=25, choices=choice_unidad)
    tipo = models.CharField(max_length=20, choices=choice_tipo)
    movimiento = models.CharField(max_length=30, choices=choice_movimiento)
    terminos = models.CharField(max_length=5, choices=choice_terminos)
    cantidad = models.FloatField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    marcas = models.CharField(max_length=200, blank=True, null=True)
    precinto = models.CharField(max_length=100, blank=True, null=True)
    tara = models.FloatField(blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    envase = models.CharField(db_column='Envase', max_length=15, choices=choice_envase,default='S/I')  # Field name made lowercase.
    bultos = models.IntegerField(blank=True, null=True)
    peso = models.FloatField(db_column='Peso', blank=True, null=True)
    profit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    nrocontenedor = models.CharField(max_length=100, blank=True, null=True)
    volumen = models.FloatField(blank=True, null=True)
    status = models.SmallIntegerField(db_column='Status', blank=True, null=True)
    fechadevol = models.DateTimeField(db_column='FechaDevol', blank=True, null=True)
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True, null=True)
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impmarit_envases'


class Faxes(models.Model):
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
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impmarit_faxes'


class Fisico(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)
    detalle = models.CharField(db_column='Detalle', max_length=100, blank=True, null=True)
    marcas = models.CharField(db_column='Marcas', max_length=100, blank=True, null=True)
    precinto = models.CharField(db_column='Precinto', max_length=100, blank=True, null=True)
    tara = models.IntegerField(db_column='Tara', blank=True, null=True)
    precio = models.DecimalField(db_column='Precio', max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True, null=True)
    imo = models.CharField(max_length=1, blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)
    ata = models.DateTimeField(blank=True, null=True)
    carpetaras = models.CharField(max_length=15, blank=True, null=True)
    carpetaplus = models.CharField(max_length=15, blank=True, null=True)
    aco = models.DateTimeField(blank=True, null=True)
    solicheque = models.DateTimeField(blank=True, null=True)
    transfer = models.DateTimeField(blank=True, null=True)
    orden = models.DateTimeField(blank=True, null=True)
    devolucion = models.CharField(max_length=50, blank=True, null=True)
    retirocont = models.DateTimeField(blank=True, null=True)
    devolcont = models.DateTimeField(blank=True, null=True)
    dnafecha = models.DateTimeField(blank=True, null=True)
    dnahora = models.CharField(max_length=15, blank=True, null=True)
    traslado = models.IntegerField(blank=True, null=True)
    bahia = models.IntegerField(blank=True, null=True)
    docdeposfecha = models.DateTimeField(blank=True, null=True)
    docdeposhora = models.CharField(max_length=15, blank=True, null=True)
    entregafecha = models.DateTimeField(blank=True, null=True)
    entregahora = models.CharField(max_length=15, blank=True, null=True)
    entrada = models.DateTimeField(blank=True, null=True)
    vaciado = models.DateTimeField(blank=True, null=True)
    deposito = models.SmallIntegerField(blank=True, null=True)
    cliente = models.IntegerField(db_column='Cliente', blank=True, null=True)


class Gastosmadre(models.Model):
    cliente = models.SmallIntegerField(blank=True, null=True)
    codigo = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=15, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=3, blank=True, null=True)
    sucursal = models.SmallIntegerField(db_column='Sucursal', blank=True, null=True)
    unidad = models.CharField(db_column='Unidad', max_length=5, blank=True, null=True)
    tipo = models.CharField(db_column='Tipo', max_length=20, blank=True, null=True)
    operacion = models.CharField(db_column='Operacion', max_length=25, blank=True, null=True)


class Gastoshijos(models.Model):
    cliente = models.IntegerField(blank=True, null=True)
    codigo = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True, null=True)
    statushijos = models.SmallIntegerField(db_column='StatusHijos', blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)
    movimiento = models.CharField(db_column='Movimiento', max_length=10, blank=True, null=True)


class Guiasgrabadas(models.Model):
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
    goods = models.TextField(blank=True, null=True)  # This field type is a guess.
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
    portext = models.CharField(max_length=50, blank=True, null=True)
    vadeclared = models.BooleanField(blank=True, null=True)
    precarriage = models.CharField(db_column='PreCarriage', max_length=35, blank=True, null=True)
    consigna6 = models.CharField(db_column='Consigna6', max_length=50, blank=True, null=True)
    consigna7 = models.CharField(db_column='Consigna7', max_length=50, blank=True, null=True)
    consigna8 = models.CharField(db_column='Consigna8', max_length=50, blank=True, null=True)
    cliente5 = models.CharField(db_column='Cliente5', max_length=50, blank=True, null=True)
    otranotif = models.CharField(db_column='Otranotif', max_length=50, blank=True, null=True)


class Guiasgrabadas2(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    marks = models.CharField(max_length=30, blank=True, null=True)
    packages = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    gross = models.CharField(max_length=30, blank=True, null=True)
    tare = models.CharField(max_length=30, blank=True, null=True)


class Nietos(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    nieto = models.SmallIntegerField(blank=True, null=True)
    conocimiento = models.CharField(max_length=25, blank=True, null=True)
    embarcador = models.CharField(max_length=50, blank=True, null=True)
    consignatario = models.CharField(max_length=50, blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    cbm = models.FloatField(blank=True, null=True)
    kilos = models.FloatField(blank=True, null=True)
    marcas = models.CharField(max_length=150, blank=True, null=True)
    notas = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    notificar = models.CharField(max_length=50, blank=True, null=True)
    peso = models.FloatField(db_column='Peso', blank=True, null=True)
    tipo = models.CharField(db_column='Tipo', max_length=12, blank=True, null=True)
    producto = models.CharField(db_column='Producto', max_length=150, blank=True, null=True)
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True, null=True)


class Reservas(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True)
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)
    loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True, null=True)
    fecha = models.DateField(db_column='Fecha', blank=True, null=True)
    kilos = models.FloatField(db_column='Kilos', blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    awb = models.CharField(max_length=40, blank=True, null=True, unique=True)
    agente = models.IntegerField(blank=True, null=True)
    consignatario = models.IntegerField(blank=True, null=True)
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.TextField(db_column='Notas', blank=True, null=True)
    volumen = models.FloatField(db_column='Volumen', blank=True, null=True)
    cotizacion = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
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
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)
    viaje = models.CharField(db_column='Viaje', max_length=20, blank=True, null=True)
    posicion = models.CharField(db_column='Posicion', max_length=30, blank=True, null=True)
    envioedi = models.CharField(max_length=1, blank=True, null=True)
    nroreferedi = models.IntegerField(blank=True, null=True)
    ciep = models.CharField(max_length=30, blank=True, null=True)
    kilosmadre = models.FloatField(blank=True, null=True)
    bultosmadre = models.IntegerField(blank=True, null=True)
    deposito = models.SmallIntegerField(blank=True, null=True)
    armador = models.IntegerField(blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    orden = models.CharField(max_length=50, blank=True, null=True)
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)
    viajefluvial = models.CharField(db_column='ViajeFluvial', max_length=30, blank=True, null=True)
    awbfluvial = models.CharField(db_column='AwbFluvial', max_length=30, blank=True, null=True)
    prefijofluvial = models.CharField(db_column='PrefijoFluvial', max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impmarit_reservas'

    def get_number(self):
        reserva_l = Reservas.objects.order_by('id').last()
        if reserva_l:
            nuevo_numero = reserva_l.numero + 1
        else:
            nuevo_numero = 1

        return nuevo_numero


class Servireserva(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=40, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notomaprofit = models.BooleanField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    prorrateo = models.CharField(db_column='Prorrateo', max_length=10, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impmarit_servireserva'


class Traceop(models.Model):
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)
    nomusuario = models.CharField(db_column='NomUsuario', max_length=30, blank=True, null=True)
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)
    detalle = models.CharField(db_column='Detalle', max_length=250, blank=True, null=True)
    formulario = models.CharField(db_column='Formulario', max_length=20, blank=True, null=True)
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)


class Conexaerea(models.Model):
    choice_modo = (
        ("MARITIMO", "MARITIMO"),
        ("FLUVIAL", "FLUVIAL"),
        ("TERRESTRE", "TERRESTRE"),
        ("AEREO", "AEREO"),
    )
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=50, blank=True, null=True)
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)
    modo = models.CharField(max_length=15, choices=choice_modo)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True, null=True)
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impmarit_conexaerea'


class Serviceaereo(models.Model):
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
    notomaprofit = models.BooleanField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)
    socio = models.IntegerField(db_column='Socio', blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'impmarit_serviceaereo'


""" VISTAS """


class Master(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True)
    transportista = models.CharField(max_length=400, blank=True, null=True)
    agente = models.CharField(max_length=400, blank=True, null=True)
    embarcador = models.CharField(db_column='consignatario', max_length=400, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=400, blank=True, null=True)
    origen = models.CharField(max_length=400, blank=True, null=True)
    destino = models.CharField(max_length=400, blank=True, null=True)
    status = models.CharField(max_length=400, blank=True, null=True)
    armador = models.CharField(max_length=400, blank=True, null=True)
    awb = models.CharField(max_length=400, blank=True, null=True)
    llegada = models.DateField(blank=True, null=True)
    seguimientos = models.TextField( blank=True, null=True)
    hawbs = models.TextField( blank=True, null=True)

    def __str__(self, ):
        return self.numero

    class Meta:
        managed = False
        db_table = 'VImpMaritMaster'


class VGastosMaster(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True, choices=(("P", "Prepaid"), ("C", "Collect")))
    servicio = models.CharField(max_length=500, blank=True, null=True)
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

    def __str__(self, ):
        return self.modo + ' - ' + str(self.numero)

    class Meta:
        managed = False
        db_table = 'VGastosMaster'


class VGastosHouse(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True, choices=(("P", "Prepaid"), ("C", "Collect")))
    servicio = models.CharField(max_length=500, blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    notomaprofit = models.BooleanField()
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)
    id_servicio = models.SmallIntegerField()
    id_moneda = models.SmallIntegerField()
    id_socio = models.SmallIntegerField()

    def __str__(self, ):
        return self.modo + ' - ' + str(self.numero)

    class Meta:
        managed = False
        db_table = 'VGastosHouse'

class VistaEventosCalendario(models.Model):
    posicion = models.CharField(max_length=255, null=True)
    awb = models.CharField(max_length=255, null=True)
    hawb = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    origen = models.CharField(max_length=255, null=True)
    destino = models.CharField(max_length=255, null=True)
    fecharetiro = models.DateField(null=True)
    consignatario = models.CharField(max_length=255, null=True)
    transportista = models.CharField(max_length=255, null=True)
    source = models.CharField(max_length=255, null=True)

    class Meta:
        managed = False  # No intentes modificar la tabla
        db_table = 'vista_eventos_calendario'

class VistaOperativas(models.Model):
    modo = models.CharField(max_length=255, null=True)
    posicion = models.CharField(max_length=255, null=True)
    tipo_operacion = models.CharField(max_length=255, null=True)
    numero = models.IntegerField(primary_key=True)
    nroarmador = models.CharField(max_length=255, null=True)
    armador = models.CharField(max_length=255, null=True)
    nrotransportista = models.CharField(max_length=255, null=True)
    nrovendedor = models.CharField(max_length=255, null=True)
    nrocliente = models.CharField(max_length=255, null=True)
    nroconsignatario = models.CharField(max_length=255, null=True)
    transportista = models.CharField(max_length=255, null=True)
    embarcador = models.CharField(max_length=255, null=True)
    consignatario = models.CharField(max_length=255, null=True)
    cliente = models.CharField(max_length=255, null=True)
    vapor = models.CharField(max_length=255, null=True)
    operacion = models.CharField(max_length=255, null=True)
    origen = models.CharField(max_length=255, null=True)
    destino = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    vendedor = models.CharField(max_length=255, null=True)
    fecha_embarque = models.DateField(blank=True, null=True)
    fecha_retiro = models.DateField(blank=True, null=True)
    etd = models.DateField(blank=True, null=True)
    eta = models.DateField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    nrodespachante = models.CharField(max_length=255, null=True)
    despachante = models.CharField(max_length=255, null=True)
    house = models.CharField(max_length=255, null=True)
    master = models.CharField(max_length=255, null=True)
    tipo = models.CharField(max_length=255, null=True)
    pago = models.CharField(max_length=255, null=True)
    flete = models.CharField(max_length=255, null=True)
    comision = models.CharField(max_length=255, null=True)
    viaje = models.CharField(max_length=255, null=True)
    loading = models.CharField(max_length=255, null=True)
    discharge = models.CharField(max_length=255, null=True)
    cotizacion = models.CharField(max_length=255, null=True)
    volumen = models.CharField(max_length=255, null=True)
    volumen_total = models.CharField(max_length=255, null=True)
    bultos = models.CharField(max_length=255, null=True)
    peso_bruto = models.CharField(max_length=255, null=True)
    producto = models.CharField(max_length=255, null=True)
    seguimiento = models.CharField(max_length=255, null=True)
    agente = models.CharField(max_length=255, null=True)
    nroagente = models.CharField(max_length=255, null=True)
    movimiento = models.CharField(max_length=255, null=True)
    tipo_contenedor = models.CharField(max_length=255, null=True)
    contenedor = models.CharField(max_length=255, null=True)
    aplicable = models.CharField(max_length=255, null=True)
    proft_final = models.CharField(max_length=255, null=True)
    porcentaje_profit = models.CharField(max_length=255, null=True)
    otros_ingresos = models.CharField(max_length=255, null=True)
    propio = models.CharField(max_length=255, null=True)
    pais = models.CharField(max_length=255, null=True)
    fecha_facturacion = models.DateField(max_length=255, null=True)
    customer = models.CharField(max_length=255, null=True)
    usuario = models.CharField(max_length=255, null=True)


    class Meta:
        managed = False  # No intentes modificar la tabla
        db_table = 'VOperativas'

class VistaOperativasGastos(models.Model):
    numero = models.IntegerField(primary_key=True)
    due_carrier = models.CharField(max_length=255, null=True)
    local_charges = models.CharField(max_length=255, null=True)
    due_agent = models.CharField(max_length=255, null=True)
    others = models.CharField(max_length=255, null=True)
    operacion = models.CharField(max_length=255, null=True)
    tipo = models.CharField(max_length=255, null=True)
    eta = models.DateField(blank=True, null=True)
    etd = models.DateField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False  # No intentes modificar la tabla
        db_table = 'VOperativasGastos'

"""Vista general para bloqueo"""

class BloqueoEdicion(models.Model):
    referencia = models.CharField(max_length=100)  # ID lógico del objeto a editar
    formulario = models.CharField(max_length=100)  # Nombre del formulario
    modulo = models.CharField(max_length=100)      # App o módulo del sistema
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()  # Fecha límite para el bloqueo
    activo = models.BooleanField(default=True)

    class Meta:
        managed = False  # No intentes modificar la tabla
        db_table = 'bloqueo_edicion'


from auditlog.registry import auditlog

class MyModel(models.Model):
    history = AuditlogHistoryField()
    # Model definition goes here


auditlog.register(MyModel)

from inspect import getmembers
from auditlog.registry import auditlog
from impomarit import models

tablas = getmembers(models)
for t in tablas:
    try:
        auditlog.register(t[1], serialize_data=True)
    except Exception as e:
        pass

