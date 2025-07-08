from auditlog.models import AuditlogHistoryField
from django.db import models

from mantenimientos.models import Productos


class ImpterraAnulados(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impterra_anulados'


class ImpterraAttachhijo(models.Model):
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
        db_table = 'impterra_attachhijo'


class ImpterraAttachmadre(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_attachmadre'


class ImpterraCargaaerea(models.Model):
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
    producto = models.ForeignKey(Productos, to_field='codigo', on_delete=models.PROTECT, db_column='producto',related_name='prod_carga_it')
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True,choices=choice_tipo)
    fechaembarque = models.DateTimeField(blank=True, null=True)
    cbm = models.FloatField(blank=True, null=True)
    mercaderia = models.TextField(db_column='Mercaderia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_cargaaerea'


class ImpterraClaveposicion(models.Model):
    posicion = models.CharField(primary_key=True, max_length=15)
    numeroorden = models.SmallIntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_claveposicion'


class ImpterraConexaerea(models.Model):
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
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=3, blank=True, null=True)
    modo = models.CharField(max_length=15,choices=choice_modo)
    viaje = models.CharField(max_length=10, blank=True, null=True)
    vuelo = models.CharField(max_length=30, blank=True, null=True)
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    consignatario = models.IntegerField(db_column='Consignatario', blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    horasalida = models.CharField(db_column='HoraSalida', max_length=12, blank=True, null=True)  # Field name made lowercase.
    horallegada = models.CharField(db_column='HoraLlegada', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_conexaerea'


class ImpterraConexreserva(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impterra_conexreserva'


class ImpterraEmbarqueaereo(models.Model):
    choice_terminos = (
        ("FOB","FOB"),
        ("FCA","FCA"),
    )
    terminos = models.CharField(max_length=5, choices=choice_terminos)
    numero = models.IntegerField(primary_key=True)
    cliente = models.IntegerField(blank=True, null=True)
    consignatario = models.IntegerField(blank=True, null=True)
    despachante = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    localint = models.CharField(max_length=20, blank=True, null=True)
    consolidado = models.SmallIntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=20, blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    aduana = models.CharField(max_length=30, blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    pago = models.SmallIntegerField(blank=True, null=True)
    awb = models.CharField(max_length=20, blank=True, null=True)
    hawb = models.CharField(max_length=50, blank=True, null=True)
    transportista = models.IntegerField(blank=True, null=True)
    valortransporte = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valoraduana = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    fechaembarque = models.DateTimeField(blank=True, null=True)
    fecharetiro = models.DateTimeField(blank=True, null=True)
    pagoflete = models.CharField(max_length=1, blank=True, null=True)
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
    notifcliente = models.DateTimeField(blank=True, null=True)
    aquien = models.CharField(max_length=30, blank=True, null=True)
    transfcliente = models.DateTimeField(blank=True, null=True)
    notifagente = models.DateTimeField(blank=True, null=True)
    observadoc = models.TextField(blank=True, null=True)
    completo = models.CharField(max_length=1, blank=True, null=True)
    observado = models.CharField(max_length=1, blank=True, null=True)
    detcompleto = models.CharField(max_length=50, blank=True, null=True)
    detobservado = models.CharField(max_length=50, blank=True, null=True)
    facturado = models.CharField(max_length=1, blank=True, null=True)
    profitage = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    notificar = models.IntegerField(db_column='Notificar', blank=True, null=True)  # Field name made lowercase.
    vaporcli = models.CharField(db_column='Vaporcli', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vaporcli2 = models.CharField(db_column='Vaporcli2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    terminal = models.SmallIntegerField(blank=True, null=True)
    terminal2 = models.SmallIntegerField(blank=True, null=True)
    tipovend = models.CharField(db_column='Tipovend', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendedor = models.SmallIntegerField(db_column='Vendedor', blank=True, null=True)  # Field name made lowercase.
    comivend = models.FloatField(db_column='Comivend', blank=True, null=True)  # Field name made lowercase.
    aplicaprofit = models.IntegerField(db_column='Aplicaprofit', blank=True, null=True)  # Field name made lowercase.
    aduanasalida = models.CharField(max_length=3, blank=True, null=True)
    aduanallegada = models.CharField(max_length=3, blank=True, null=True)
    documanexo = models.TextField(blank=True, null=True)
    matriculas = models.CharField(max_length=50, blank=True, null=True)
    registros = models.CharField(max_length=50, blank=True, null=True)
    precintos = models.CharField(max_length=50, blank=True, null=True)
    advalvta = models.FloatField(blank=True, null=True)
    advalcto = models.FloatField(blank=True, null=True)
    nroreferedi = models.IntegerField(blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    ordencliente = models.CharField(db_column='OrdenCliente', max_length=850, blank=True, null=True)  # Field name made lowercase.
    propia = models.IntegerField(blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    aquienentrega = models.CharField(max_length=30, blank=True, null=True)
    fechaentrega = models.DateTimeField(blank=True, null=True)
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=250, blank=True, null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=250, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True, null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    despafrontera = models.IntegerField(db_column='DespaFrontera', blank=True, null=True)  # Field name made lowercase.
    sociotransfer = models.IntegerField(db_column='SocioTransfer', blank=True, null=True)  # Field name made lowercase.
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
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.DateTimeField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_embarqueaereo'

    def get_number(self):
        embarque_l = ImpterraEmbarqueaereo.objects.order_by('numero').last()
        if embarque_l:
            nuevo_numero = embarque_l.numero + 1
        else:
            nuevo_numero = 1

        return nuevo_numero


class ImpterraEntregadoc(models.Model):
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
        db_table = 'impterra_entregadoc'


class ImpterraEnvases(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=25, blank=True, null=True)
    tipo = models.CharField(max_length=30, blank=True, null=True)
    movimiento = models.CharField(max_length=30, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    marcas = models.CharField(max_length=50, blank=True, null=True)
    volumen = models.FloatField(blank=True, null=True)
    tara = models.FloatField(blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    envase = models.CharField(db_column='Envase', max_length=15, blank=True, null=True,default='S/I')  # Field name made lowercase.
    bultos = models.SmallIntegerField(blank=True, null=True)
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    profit = models.FloatField(blank=True, null=True)
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=100, blank=True, null=True)  # Field name made lowercase.
    precinto = models.CharField(db_column='Precinto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    temperatura = models.FloatField(db_column='Temperatura', blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    condespeciales = models.CharField(db_column='CondEspeciales', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nomchofer = models.CharField(db_column='NomChofer', max_length=100, blank=True, null=True)  # Field name made lowercase.
    telchofer = models.CharField(db_column='TelChofer', max_length=30, blank=True, null=True)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=20, blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    horacitacion = models.CharField(db_column='HoraCitacion', max_length=30, blank=True, null=True)  # Field name made lowercase.
    horallegada = models.CharField(db_column='HoraLlegada', max_length=30, blank=True, null=True)  # Field name made lowercase.
    depositoretiro = models.IntegerField(db_column='DepositoRetiro', blank=True, null=True)  # Field name made lowercase.
    depositodev = models.IntegerField(db_column='DepositoDev', blank=True, null=True)  # Field name made lowercase.
    direccionentrega = models.SmallIntegerField(db_column='DireccionEntrega', blank=True, null=True)  # Field name made lowercase.
    rucchofer = models.CharField(db_column='RucChofer', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechallegadaplanta = models.DateTimeField(db_column='FechaLlegadaPlanta', blank=True, null=True)  # Field name made lowercase.
    fechacitacion = models.DateTimeField(db_column='FechaCitacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_envases'



class ImpterraFaxes(models.Model):
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
        db_table = 'impterra_faxes'


class ImpterraFisico(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=60, blank=True, null=True)  # Field name made lowercase.
    volumen = models.FloatField(blank=True, null=True)
    tara = models.IntegerField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_fisico'


class ImpterraGastoshijos(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    cliente = models.IntegerField(blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    statushijos = models.SmallIntegerField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_gastoshijos'


class ImpterraGuiasgrabadas(models.Model):
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
    destina = models.CharField(max_length=45, blank=True, null=True)
    direcdestina = models.CharField(max_length=45, blank=True, null=True)
    localdestina = models.CharField(max_length=45, blank=True, null=True)
    teledestina = models.CharField(max_length=45, blank=True, null=True)
    consigna = models.CharField(max_length=45, blank=True, null=True)
    direcconsigna = models.CharField(max_length=45, blank=True, null=True)
    localconsigna = models.CharField(max_length=45, blank=True, null=True)
    teleconsigna = models.CharField(max_length=45, blank=True, null=True)
    notif = models.CharField(max_length=45, blank=True, null=True)
    dirnotif = models.CharField(max_length=45, blank=True, null=True)
    otralinea2 = models.CharField(max_length=45, blank=True, null=True)
    telnotif = models.CharField(max_length=45, blank=True, null=True)
    salede = models.CharField(max_length=35, blank=True, null=True)
    loading = models.CharField(max_length=35, blank=True, null=True)
    discharge = models.CharField(max_length=35, blank=True, null=True)
    porte1 = models.CharField(max_length=45, blank=True, null=True)
    porte2 = models.CharField(max_length=45, blank=True, null=True)
    porte3 = models.CharField(max_length=45, blank=True, null=True)
    declaravalor = models.CharField(max_length=15, blank=True, null=True)
    documanexo1 = models.CharField(max_length=45, blank=True, null=True)
    documanexo2 = models.CharField(max_length=45, blank=True, null=True)
    documanexo3 = models.CharField(max_length=45, blank=True, null=True)
    documanexo4 = models.CharField(max_length=45, blank=True, null=True)
    aduana1 = models.CharField(max_length=45, blank=True, null=True)
    aduana2 = models.CharField(max_length=45, blank=True, null=True)
    aduana3 = models.CharField(max_length=45, blank=True, null=True)
    aduana4 = models.CharField(max_length=45, blank=True, null=True)
    aduana5 = models.CharField(max_length=45, blank=True, null=True)
    declara1 = models.CharField(max_length=45, blank=True, null=True)
    declara2 = models.CharField(max_length=45, blank=True, null=True)
    declara3 = models.CharField(max_length=45, blank=True, null=True)
    declara4 = models.CharField(max_length=45, blank=True, null=True)
    declara5 = models.CharField(max_length=45, blank=True, null=True)
    destina1 = models.CharField(max_length=45, blank=True, null=True)
    destina2 = models.CharField(max_length=45, blank=True, null=True)
    destina3 = models.CharField(max_length=10, blank=True, null=True)
    fleteexterno = models.CharField(max_length=12, blank=True, null=True)
    reembolso = models.CharField(max_length=12, blank=True, null=True)
    remite1 = models.CharField(max_length=45, blank=True, null=True)
    remite2 = models.CharField(max_length=45, blank=True, null=True)
    remite3 = models.CharField(max_length=15, blank=True, null=True)
    signature = models.CharField(max_length=45, blank=True, null=True)
    signature2 = models.CharField(max_length=45, blank=True, null=True)
    fechaemi = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impterra_guiasgrabadas'


class ImpterraGuiasgrabadas2(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=55, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impterra_guiasgrabadas2'


class ImpterraReservas(models.Model):
    numero = models.IntegerField(db_column='Numero', primary_key=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
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
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    volumen = models.FloatField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    aduana = models.CharField(max_length=30, blank=True, null=True)
    preaviso = models.CharField(max_length=1, blank=True, null=True)
    notirecibo = models.DateTimeField(blank=True, null=True)
    porquien = models.CharField(max_length=30, blank=True, null=True)
    completo = models.CharField(max_length=1, blank=True, null=True)
    observado = models.CharField(max_length=1, blank=True, null=True)
    detcompleto = models.CharField(max_length=50, blank=True, null=True)
    detobservado = models.CharField(max_length=50, blank=True, null=True)
    observadoc = models.TextField(blank=True, null=True)
    profitage = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifapl = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    posicion = models.CharField(db_column='Posicion', max_length=30, blank=True, null=True)  # Field name made lowercase.
    envioedi = models.CharField(max_length=1, blank=True, null=True)
    aduanallegada = models.CharField(max_length=3, blank=True, null=True)
    aduanasalida = models.CharField(max_length=3, blank=True, null=True)
    matriculas = models.CharField(max_length=50, blank=True, null=True)
    precintos = models.CharField(max_length=50, blank=True, null=True)
    registros = models.CharField(max_length=50, blank=True, null=True)
    documanexo = models.TextField(blank=True, null=True)
    terminal = models.SmallIntegerField(blank=True, null=True)
    terminal2 = models.SmallIntegerField(blank=True, null=True)
    nroreferedi = models.IntegerField(blank=True, null=True)
    kilosmadre = models.FloatField(blank=True, null=True)
    bultosmadre = models.IntegerField(blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_reservas'

    def get_number(self):
        reserva_l = ImpterraReservas.objects.order_by('numero').last()
        if reserva_l:
            nuevo_numero = reserva_l.numero + 1
        else:
            nuevo_numero = 1

        return nuevo_numero


class ImpterraServiceaereo(models.Model):
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
        db_table = 'impterra_serviceaereo'


class ImpterraServireserva(models.Model):
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
    repartir = models.CharField(max_length=1, blank=True, null=True)
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
        db_table = 'impterra_servireserva'


class ImpterraTraceop(models.Model):
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
        db_table = 'impterra_traceop'


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
    localint = models.CharField(max_length=30, blank=True, null=True)
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
        db_table = 'VImpTerrestreEmbarqueAereo'

class VEmbarqueaereoDirecto(models.Model):
    numero = models.IntegerField(unique=True, primary_key=True)
    consignatario_id = models.IntegerField()
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)
    consignatario_codigo = models.IntegerField()

    transportista = models.CharField(max_length=255, blank=True, null=True)  # Nombre del transportista
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=255, blank=True, null=True)  # Nombre del agente
    consignatario = models.CharField(max_length=255, blank=True, null=True)  # Nombre del consignatario
    localint = models.CharField(max_length=30, blank=True, null=True)
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
        db_table = 'VImpTerrestreEmbarqueAereoDirecto'

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

    def __str__(self,):
        return self.numero

    class Meta:
        managed = False
        db_table = 'VImpTerraMaster'

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
        db_table = 'VImpTerrestreGastosMaster'

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
        db_table = 'VImpTerrestreGastosHouse'


from auditlog.registry import auditlog

class MyModel(models.Model):
    history = AuditlogHistoryField()
    # Model definition goes here


auditlog.register(MyModel)

from inspect import getmembers
from auditlog.registry import auditlog
from impterrestre import models

tablas = getmembers(models)
for t in tablas:
    try:
        auditlog.register(t[1], serialize_data=True)
    except Exception as e:
        pass