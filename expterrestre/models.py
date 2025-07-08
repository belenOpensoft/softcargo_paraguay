# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from mantenimientos.models import Productos


class ExpterraAnulados(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expterra_anulados'


class ExpterraAttachhijo(models.Model):
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
        db_table = 'expterra_attachhijo'


class ExpterraAttachmadre(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_attachmadre'


class ExpterraCargaaerea(models.Model):
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
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True,choices=choice_tipo)
    producto = models.ForeignKey(Productos, to_field='codigo', on_delete=models.PROTECT, db_column='producto',related_name='prod_carga_et')
    fechaembarque = models.DateTimeField(blank=True, null=True)
    cbm = models.FloatField(blank=True, null=True)
    mercaderia = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expterra_cargaaerea'


class ExpterraClaveposicion(models.Model):
    posicion = models.CharField(primary_key=True, max_length=15)
    numeroorden = models.SmallIntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_claveposicion'


class ExpterraConexaerea(models.Model):
    choice_modo = (
        ("MARITIMO", "MARITIMO"),
        ("FLUVIAL", "FLUVIAL"),
        ("TERRESTRE", "TERRESTRE"),
        ("AEREO", "AEREO"),
    )
    modo = models.CharField(max_length=15,choices=choice_modo)
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=3, blank=True, null=True)
    viaje = models.CharField(max_length=10, blank=True, null=True)
    vuelo = models.CharField(max_length=30, blank=True, null=True)
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    consignatario = models.IntegerField(db_column='Consignatario', blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    horasalida = models.CharField(db_column='HoraSalida', max_length=12, blank=True, null=True)  # Field name made lowercase.
    horallegada = models.CharField(db_column='HoraLlegada', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_conexaerea'


class ExpterraConexreserva(models.Model):
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
        db_table = 'expterra_conexreserva'


class ExpterraDeclaracion(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    ncorr = models.CharField(db_column='Ncorr', max_length=13, blank=True, null=True)  # Field name made lowercase.
    nintdespacho = models.CharField(db_column='NintDespacho', max_length=11, blank=True, null=True)  # Field name made lowercase.
    codfisc = models.CharField(db_column='CodFisc', max_length=6, blank=True, null=True)  # Field name made lowercase.
    coddeclaracion = models.CharField(db_column='CodDeclaracion', max_length=2, blank=True, null=True)  # Field name made lowercase.
    nomdeclaracion = models.CharField(db_column='NomDeclaracion', max_length=15, blank=True, null=True)  # Field name made lowercase.
    aduana = models.CharField(db_column='Aduana', max_length=24, blank=True, null=True)  # Field name made lowercase.
    codaduana = models.CharField(db_column='CodAduana', max_length=3, blank=True, null=True)  # Field name made lowercase.
    regimen = models.CharField(db_column='Regimen', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codregimen = models.CharField(db_column='CodRegimen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tipotramite = models.CharField(db_column='TipoTramite', max_length=24, blank=True, null=True)  # Field name made lowercase.
    codtramite = models.CharField(db_column='CodTramite', max_length=3, blank=True, null=True)  # Field name made lowercase.
    aduana2 = models.CharField(db_column='Aduana2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codaduana2 = models.CharField(db_column='CodAduana2', max_length=3, blank=True, null=True)  # Field name made lowercase.
    numero2 = models.CharField(db_column='Numero2', max_length=26, blank=True, null=True)  # Field name made lowercase.
    despachador = models.CharField(db_column='Despachador', max_length=24, blank=True, null=True)  # Field name made lowercase.
    coddespachador = models.CharField(db_column='CodDespachador', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numerodeclaracion = models.CharField(db_column='NumeroDeclaracion', max_length=12, blank=True, null=True)  # Field name made lowercase.
    fechadeclaracion = models.CharField(db_column='FechaDeclaracion', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=26, blank=True, null=True)  # Field name made lowercase.
    consignatario = models.CharField(db_column='Consignatario', max_length=37, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=37, blank=True, null=True)  # Field name made lowercase.
    almacenista = models.CharField(db_column='Almacenista', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codalmacenista = models.CharField(db_column='CodAlmacenista', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codtipo = models.CharField(db_column='CodTipo', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rut = models.CharField(db_column='Rut', max_length=14, blank=True, null=True)  # Field name made lowercase.
    fecharecepcion = models.CharField(db_column='FechaRecepcion', max_length=12, blank=True, null=True)  # Field name made lowercase.
    consignante = models.CharField(db_column='Consignante', max_length=37, blank=True, null=True)  # Field name made lowercase.
    ubicacion = models.CharField(db_column='Ubicacion', max_length=26, blank=True, null=True)  # Field name made lowercase.
    aduanadestino = models.CharField(db_column='AduanaDestino', max_length=16, blank=True, null=True)  # Field name made lowercase.
    codaduanadestino = models.CharField(db_column='CodAduanaDestino', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ubicacion2 = models.CharField(db_column='Ubicacion2', max_length=26, blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', max_length=16, blank=True, null=True)  # Field name made lowercase.
    codpaisdestino = models.CharField(db_column='CodPaisDestino', max_length=3, blank=True, null=True)  # Field name made lowercase.
    paisorigen = models.CharField(db_column='PaisOrigen', max_length=24, blank=True, null=True)  # Field name made lowercase.
    codpaisorigen = models.CharField(db_column='CodPaisOrigen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    viatransporte = models.CharField(db_column='ViaTransporte', max_length=20, blank=True, null=True)  # Field name made lowercase.
    codviatransporte = models.CharField(db_column='CodViaTransporte', max_length=5, blank=True, null=True)  # Field name made lowercase.
    paisorigen2 = models.CharField(db_column='PaisOrigen2', max_length=24, blank=True, null=True)  # Field name made lowercase.
    codpaisorigen2 = models.CharField(db_column='CodPaisOrigen2', max_length=3, blank=True, null=True)  # Field name made lowercase.
    garantia = models.CharField(db_column='Garantia', max_length=26, blank=True, null=True)  # Field name made lowercase.
    texto1 = models.CharField(db_column='Texto1', max_length=26, blank=True, null=True)  # Field name made lowercase.
    paisorigen3 = models.CharField(db_column='PaisOrigen3', max_length=24, blank=True, null=True)  # Field name made lowercase.
    codpaisorigen3 = models.CharField(db_column='CodPaisOrigen3', max_length=3, blank=True, null=True)  # Field name made lowercase.
    garantia2 = models.CharField(db_column='Garantia2', max_length=26, blank=True, null=True)  # Field name made lowercase.
    texto2 = models.CharField(db_column='Texto2', max_length=26, blank=True, null=True)  # Field name made lowercase.
    texto3 = models.CharField(db_column='Texto3', max_length=26, blank=True, null=True)  # Field name made lowercase.
    puertoembarque = models.CharField(db_column='PuertoEmbarque', max_length=24, blank=True, null=True)  # Field name made lowercase.
    codpuertoembarque = models.CharField(db_column='CodPuertoEmbarque', max_length=3, blank=True, null=True)  # Field name made lowercase.
    puertodesembarque = models.CharField(db_column='PuertoDesembarque', max_length=24, blank=True, null=True)  # Field name made lowercase.
    codpuertodesembarque = models.CharField(db_column='CodPuertoDesembarque', max_length=3, blank=True, null=True)  # Field name made lowercase.
    valorfob = models.CharField(db_column='ValorFob', max_length=16, blank=True, null=True)  # Field name made lowercase.
    viatransporte2 = models.CharField(db_column='ViaTransporte2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    codviatransporte2 = models.CharField(db_column='CodViaTransporte2', max_length=5, blank=True, null=True)  # Field name made lowercase.
    flete = models.CharField(db_column='Flete', max_length=16, blank=True, null=True)  # Field name made lowercase.
    codflete = models.CharField(db_column='CodFlete', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_declaracion'


class ExpterraDeclaracion2(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    conocembarque = models.CharField(db_column='ConocEmbarque', max_length=19, blank=True, null=True)  # Field name made lowercase.
    fechaemision = models.CharField(db_column='FechaEmision', max_length=10, blank=True, null=True)  # Field name made lowercase.
    emisor = models.CharField(db_column='Emisor', max_length=7, blank=True, null=True)  # Field name made lowercase.
    seguro = models.CharField(db_column='Seguro', max_length=16, blank=True, null=True)  # Field name made lowercase.
    codseguro = models.CharField(db_column='CodSeguro', max_length=3, blank=True, null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', max_length=37, blank=True, null=True)  # Field name made lowercase.
    valorcif = models.CharField(db_column='ValorCif', max_length=16, blank=True, null=True)  # Field name made lowercase.
    texto4 = models.CharField(db_column='Texto4', max_length=90, blank=True, null=True)  # Field name made lowercase.
    texto5 = models.CharField(db_column='Texto5', max_length=90, blank=True, null=True)  # Field name made lowercase.
    texto6 = models.CharField(db_column='Texto6', max_length=90, blank=True, null=True)  # Field name made lowercase.
    texto7 = models.CharField(db_column='Texto7', max_length=90, blank=True, null=True)  # Field name made lowercase.
    infref = models.CharField(db_column='InfRef', max_length=45, blank=True, null=True)  # Field name made lowercase.
    idbultos = models.CharField(db_column='IdBultos', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantbultos = models.CharField(db_column='CantBultos', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codbultos = models.CharField(db_column='CodBultos', max_length=5, blank=True, null=True)  # Field name made lowercase.
    infref2 = models.CharField(db_column='InfRef2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    idbultos2 = models.CharField(db_column='IdBultos2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantbultos2 = models.CharField(db_column='CantBultos2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codbultos2 = models.CharField(db_column='CodBultos2', max_length=5, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos3 = models.CharField(db_column='IdBultos3', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantbultos3 = models.CharField(db_column='CantBultos3', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codbultos3 = models.CharField(db_column='CodBultos3', max_length=5, blank=True, null=True)  # Field name made lowercase.
    variedad = models.CharField(db_column='Variedad', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos4 = models.CharField(db_column='IdBultos4', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantbultos4 = models.CharField(db_column='CantBultos4', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codbultos4 = models.CharField(db_column='CodBultos4', max_length=5, blank=True, null=True)  # Field name made lowercase.
    marca = models.CharField(db_column='Marca', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos5 = models.CharField(db_column='IdBultos5', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantbultos5 = models.CharField(db_column='CantBultos5', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codbultos5 = models.CharField(db_column='CodBultos5', max_length=5, blank=True, null=True)  # Field name made lowercase.
    otrosant = models.CharField(db_column='OtrosAnt', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos6 = models.CharField(db_column='IdBultos6', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantbultos6 = models.CharField(db_column='CantBultos6', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codbultos6 = models.CharField(db_column='CodBultos6', max_length=5, blank=True, null=True)  # Field name made lowercase.
    obs = models.CharField(db_column='Obs', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos7 = models.CharField(db_column='IdBultos7', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantbultos7 = models.CharField(db_column='CantBultos7', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codbultos7 = models.CharField(db_column='CodBultos7', max_length=5, blank=True, null=True)  # Field name made lowercase.
    obs2 = models.CharField(db_column='Obs2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos8 = models.CharField(db_column='IdBultos8', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantbultos8 = models.CharField(db_column='CantBultos8', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codbultos8 = models.CharField(db_column='CodBultos8', max_length=5, blank=True, null=True)  # Field name made lowercase.
    obs3 = models.CharField(db_column='Obs3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos9 = models.CharField(db_column='IdBultos9', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantbultos9 = models.CharField(db_column='CantBultos9', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codbultos9 = models.CharField(db_column='CodBultos9', max_length=5, blank=True, null=True)  # Field name made lowercase.
    obs4 = models.CharField(db_column='Obs4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos10 = models.CharField(db_column='IdBultos10', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantbultos10 = models.CharField(db_column='CantBultos10', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codbultos10 = models.CharField(db_column='CodBultos10', max_length=5, blank=True, null=True)  # Field name made lowercase.
    codnab = models.CharField(db_column='CodNab', max_length=14, blank=True, null=True)  # Field name made lowercase.
    esp = models.CharField(db_column='Esp', max_length=8, blank=True, null=True)  # Field name made lowercase.
    adval = models.CharField(db_column='AdVal', max_length=12, blank=True, null=True)  # Field name made lowercase.
    stasa = models.CharField(db_column='Stasa', max_length=14, blank=True, null=True)  # Field name made lowercase.
    idbultos11 = models.CharField(db_column='IdBultos11', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantbultos11 = models.CharField(db_column='CantBultos11', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codbultos11 = models.CharField(db_column='CodBultos11', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cantmerc = models.CharField(db_column='CantMerc', max_length=14, blank=True, null=True)  # Field name made lowercase.
    punit = models.CharField(db_column='Punit', max_length=20, blank=True, null=True)  # Field name made lowercase.
    umed = models.CharField(db_column='Umed', max_length=15, blank=True, null=True)  # Field name made lowercase.
    pesobruto = models.CharField(db_column='PesoBruto', max_length=14, blank=True, null=True)  # Field name made lowercase.
    valorcif2 = models.CharField(db_column='ValorCif2', max_length=14, blank=True, null=True)  # Field name made lowercase.
    totalbultos = models.CharField(db_column='TotalBultos', max_length=9, blank=True, null=True)  # Field name made lowercase.
    totalacumulado = models.CharField(db_column='TotalAcumulado', max_length=14, blank=True, null=True)  # Field name made lowercase.
    totalacumulado2 = models.CharField(db_column='TotalAcumulado2', max_length=14, blank=True, null=True)  # Field name made lowercase.
    totalacumulado3 = models.CharField(db_column='TotalAcumulado3', max_length=9, blank=True, null=True)  # Field name made lowercase.
    totalitem = models.CharField(db_column='TotalItem', max_length=5, blank=True, null=True)  # Field name made lowercase.
    totalhojas = models.CharField(db_column='TotalHojas', max_length=5, blank=True, null=True)  # Field name made lowercase.
    totalfinal = models.CharField(db_column='TotalFinal', max_length=14, blank=True, null=True)  # Field name made lowercase.
    totalfinal2 = models.CharField(db_column='TotalFinal2', max_length=14, blank=True, null=True)  # Field name made lowercase.
    totalfinal3 = models.CharField(db_column='TotalFinal3', max_length=9, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_declaracion2'


class ExpterraEmbarqueaereo(models.Model):
    choice_terminos = (
        ("FOB", "FOB"),
        ("FCA", "FCA"),
    )
    terminos = models.CharField(max_length=5, choices=choice_terminos)
    numero = models.IntegerField(primary_key=True)
    cliente = models.IntegerField(blank=True, null=True)
    consignatario = models.IntegerField(blank=True, null=True)
    despachante = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    localint = models.CharField(max_length=20, blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
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
    ordencliente = models.CharField(db_column='OrdenCliente', max_length=850, blank=True, null=True)  # Field name made lowercase.
    propia = models.IntegerField(blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    vapor = models.CharField(max_length=30, blank=True, null=True)
    conocimiento = models.CharField(max_length=20, blank=True, null=True)
    origenawb = models.CharField(max_length=3, blank=True, null=True)
    destinoawb = models.CharField(max_length=3, blank=True, null=True)
    salidaawb = models.DateTimeField(blank=True, null=True)
    llegadaawb = models.DateTimeField(blank=True, null=True)
    viaje = models.CharField(max_length=20, blank=True, null=True)
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
    booking = models.CharField(db_column='Booking', max_length=30, blank=True, null=True)  # Field name made lowercase.
    diasalmacenaje = models.SmallIntegerField(db_column='DiasAlmacenaje', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.DateTimeField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_embarqueaereo'

    def get_number(self):
        embarque_l = ExpterraEmbarqueaereo.objects.order_by('numero').last()
        if embarque_l:
            nuevo_numero = embarque_l.numero + 1
        else:
            nuevo_numero = 1

        return nuevo_numero


class ExpterraEntregadoc(models.Model):
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
        db_table = 'expterra_entregadoc'


class ExpterraEnvases(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=25, blank=True, null=True)
    tipo = models.CharField(max_length=30, blank=True, null=True)
    movimiento = models.CharField(max_length=30, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    marcas = models.CharField(max_length=100, blank=True, null=True)
    volumen = models.FloatField(blank=True, null=True)
    tara = models.FloatField(blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    envase = models.CharField(db_column='Envase', max_length=15, blank=True, null=True,default='S/I')  # Field name made lowercase.
    bultos = models.SmallIntegerField(blank=True, null=True)
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    profit = models.FloatField(blank=True, null=True)
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
    cotizacion = models.IntegerField(db_column='Cotizacion', blank=True, null=True)  # Field name made lowercase.
    direccionentrega = models.SmallIntegerField(db_column='DireccionEntrega', blank=True, null=True)  # Field name made lowercase.
    rucchofer = models.CharField(db_column='RucChofer', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechallegadaplanta = models.DateTimeField(db_column='FechaLlegadaPlanta', blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=100, blank=True, null=True)  # Field name made lowercase.
    precinto = models.CharField(db_column='Precinto', max_length=100, blank=True, null=True)  # Field name made lowercase.
    autogenenvase = models.CharField(db_column='AutogenEnvase', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechacitacion = models.DateTimeField(db_column='FechaCitacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_envases'


class ExpterraFaxes(models.Model):
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
        db_table = 'expterra_faxes'


class ExpterraFisico(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=60, blank=True, null=True)  # Field name made lowercase.
    volumen = models.FloatField(blank=True, null=True)
    tara = models.IntegerField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_fisico'


class ExpterraGastoshijos(models.Model):
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
        db_table = 'expterra_gastoshijos'


class ExpterraGuiasgrabadas(models.Model):
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
    salede = models.CharField(max_length=80, blank=True, null=True)
    loading = models.CharField(max_length=80, blank=True, null=True)
    discharge = models.CharField(max_length=80, blank=True, null=True)
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
        db_table = 'expterra_guiasgrabadas'


class ExpterraGuiasgrabadas2(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=55, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expterra_guiasgrabadas2'


class ExpterraReservas(models.Model):
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
    operacion = models.CharField(max_length=25, blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
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
        db_table = 'expterra_reservas'

    def get_number(self):
        reserva_l = ExpterraReservas.objects.order_by('numero').last()
        if reserva_l:
            nuevo_numero = reserva_l.numero + 1
        else:
            nuevo_numero = 1

        return nuevo_numero


class ExpterraServiceaereo(models.Model):
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
    notomaprofit = models.IntegerField(db_column='Notomaprofit', blank=True, null=True)  # Field name made lowercase.
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    autogenenvase = models.CharField(db_column='AutogenEnvase', max_length=50, blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_serviceaereo'


class ExpterraServireserva(models.Model):
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
    repartir = models.CharField(max_length=1, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_servireserva'


class ExpterraTraceop(models.Model):
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
        db_table = 'expterra_traceop'


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
        db_table = 'VExpTerrestreEmbarqueAereo'

class VEmbarqueaereoDirecto(models.Model):
    numero = models.IntegerField(unique=True, primary_key=True)
    consignatario_codigo = models.IntegerField()
    consignatario_id = models.IntegerField()
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)

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
        db_table = 'VExpTerrestreEmbarqueAereoDirecto'
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
        db_table = 'VExpTerraMaster'

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
        db_table = 'VExpTerrestreGastosMaster'

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
        db_table = 'VExpTerrestreGastosHouse'


from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

class MyModel(models.Model):
    history = AuditlogHistoryField()
    # Model definition goes here


auditlog.register(MyModel)

from inspect import getmembers
from auditlog.registry import auditlog
from expterrestre import models

tablas = getmembers(models)
for t in tablas:
    try:
        auditlog.register(t[1], serialize_data=True)
    except Exception as e:
        pass

