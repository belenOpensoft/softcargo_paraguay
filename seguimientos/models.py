from django.contrib.auth.models import User
from django.db import models
from mantenimientos.models import Clientes, Monedas, Vendedores, Depositos, Vapores, Productos
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField


class MyModel(models.Model):
    history = AuditlogHistoryField()
    # Model definition goes here


auditlog.register(MyModel)


class Attachhijo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.FileField(upload_to='documents/', blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True,
                                         null=True)  # Field name made lowercase.
    idusuario = models.IntegerField(blank=True, null=True)


class Attachhijopo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.


class Bl(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', max_length=35, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=22, blank=True, null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', max_length=22, blank=True,
                                 null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    cliente1 = models.CharField(db_column='Cliente1', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente2 = models.CharField(db_column='Cliente2', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente3 = models.CharField(db_column='Cliente3', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente4 = models.CharField(db_column='Cliente4', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    consigna = models.CharField(db_column='Consigna', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    direcconsigna = models.CharField(db_column='DirecConsigna', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    localconsigna = models.CharField(db_column='LocalConsigna', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    teleconsigna = models.CharField(db_column='TeleConsigna', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    otralinea = models.CharField(db_column='Otralinea', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    notif = models.CharField(db_column='Notif', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dirnotif = models.CharField(db_column='DirNotif', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    otralinea2 = models.CharField(db_column='Otralinea2', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    telnotif = models.CharField(db_column='TelNotif', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    tipoflete = models.CharField(db_column='TipoFlete', max_length=50, blank=True,
                                 null=True, )  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    salede = models.CharField(db_column='Salede', max_length=35, blank=True, null=True)  # Field name made lowercase.
    vapor = models.CharField(db_column='Vapor', max_length=35, blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=35, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=60, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=35, blank=True,
                                 null=True)  # Field name made lowercase.
    delivery = models.CharField(db_column='Delivery', max_length=35, blank=True,
                                null=True)  # Field name made lowercase.
    transterms = models.CharField(db_column='TransTerms', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.
    simbolo = models.CharField(db_column='Simbolo', max_length=4, blank=True, null=True)  # Field name made lowercase.
    condentrega = models.CharField(db_column='CondEntrega', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.
    tipomov = models.CharField(db_column='TipoMov', max_length=15, blank=True, null=True)  # Field name made lowercase.
    carriage = models.CharField(db_column='Carriage', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    custom = models.CharField(db_column='Custom', max_length=10, blank=True, null=True)  # Field name made lowercase.
    valseguro = models.CharField(db_column='ValSeguro', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    goods = models.TextField(db_column='Goods', blank=True,
                             null=True)  # Field name made lowercase. This field type is a guess.
    free1 = models.CharField(db_column='Free1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    free2 = models.CharField(db_column='Free2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    free3 = models.CharField(db_column='Free3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    signature2 = models.CharField(db_column='Signature2', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    signature3 = models.CharField(db_column='Signature3', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    nbls = models.CharField(db_column='Nbls', max_length=2, blank=True, null=True)  # Field name made lowercase.
    payable = models.CharField(db_column='Payable', max_length=15, blank=True, null=True)  # Field name made lowercase.
    board = models.CharField(db_column='Board', max_length=15, blank=True, null=True)  # Field name made lowercase.
    clean = models.CharField(db_column='Clean', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fechaemi = models.CharField(db_column='FechaEmi', max_length=12, blank=True,
                                null=True)  # Field name made lowercase.
    restotext = models.CharField(db_column='RestoText', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    portext = models.CharField(db_column='PorText', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vadeclared = models.BooleanField(db_column='VaDeclared', blank=True, null=True)  # Field name made lowercase.
    cliente5 = models.CharField(db_column='Cliente5', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    otranotif = models.CharField(db_column='OtraNotif', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    signature4 = models.CharField(db_column='Signature4', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    signature5 = models.CharField(db_column='Signature5', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    booking = models.CharField(db_column='Booking', max_length=30, blank=True, null=True)  # Field name made lowercase.
    position2 = models.CharField(db_column='Position2', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    origin = models.CharField(db_column='Origin', max_length=35, blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', max_length=35, blank=True,
                                   null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=3, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=3, blank=True,
                                     null=True)  # Field name made lowercase.
    awb = models.CharField(db_column='AWB', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawb = models.CharField(db_column='HAWB', max_length=50, blank=True, null=True)  # Field name made lowercase.
    totalkilos = models.FloatField(db_column='TotalKilos', blank=True, null=True)  # Field name made lowercase.
    totalpaquetes = models.IntegerField(db_column='TotalPaquetes', blank=True, null=True)  # Field name made lowercase.
    tipodocumento = models.CharField(db_column='TipoDocumento', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    consolidado = models.BooleanField(db_column='Consolidado', blank=True, null=True)  # Field name made lowercase.
    mensaje1 = models.BooleanField(db_column='Mensaje1', blank=True, null=True)  # Field name made lowercase.
    mensaje2 = models.BooleanField(db_column='Mensaje2', blank=True, null=True)  # Field name made lowercase.
    label6 = models.CharField(db_column='Label6', max_length=50, blank=True, null=True)  # Field name made lowercase.
    texto = models.TextField(db_column='Texto', blank=True,
                             null=True)  # Field name made lowercase. This field type is a guess.
    consigna6 = models.CharField(db_column='Consigna6', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    consigna7 = models.CharField(db_column='Consigna7', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    consigna8 = models.CharField(db_column='Consigna8', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    precarriage = models.CharField(db_column='PreCarriage', max_length=35, blank=True,
                                   null=True)  # Field name made lowercase.


class Bl2(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    marks = models.CharField(db_column='Marks', max_length=30, blank=True, null=True)  # Field name made lowercase.
    packages = models.CharField(db_column='Packages', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    gross = models.CharField(db_column='Gross', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tare = models.CharField(db_column='Tare', max_length=30, blank=True, null=True)  # Field name made lowercase.


class Bl3(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    servicio = models.CharField(db_column='Servicio', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    prepaid = models.CharField(db_column='Prepaid', max_length=10, blank=True, null=True)  # Field name made lowercase.
    collect = models.CharField(db_column='Collect', max_length=10, blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', max_length=3, blank=True, null=True)  # Field name made lowercase.


class Bookenv(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    marks = models.CharField(max_length=30, blank=True, null=True)
    packages = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    gross = models.CharField(max_length=30, blank=True, null=True)
    tare = models.CharField(max_length=30, blank=True, null=True)


class Booking(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    empresa = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    pais = models.CharField(max_length=15, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    comboembarca = models.IntegerField(blank=True, null=True)
    cliente2 = models.CharField(max_length=45, blank=True, null=True)
    cliente3 = models.CharField(max_length=45, blank=True, null=True)
    cliente4 = models.CharField(max_length=45, blank=True, null=True)
    comboconsig = models.IntegerField(blank=True, null=True)
    direcconsigna = models.CharField(max_length=45, blank=True, null=True)
    localconsigna = models.CharField(max_length=45, blank=True, null=True)
    teleconsigna = models.CharField(max_length=45, blank=True, null=True)
    otralinea = models.CharField(max_length=45, blank=True, null=True)
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
    net = models.TextField(blank=True, null=True)  # This field type is a guess.
    sold = models.TextField(blank=True, null=True)  # This field type is a guess.
    profit = models.TextField(blank=True, null=True)  # This field type is a guess.
    remarks = models.TextField(blank=True, null=True)  # This field type is a guess.
    giro = models.CharField(max_length=30, blank=True, null=True)
    despachante = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    terminal = models.CharField(max_length=30, blank=True, null=True)
    direccterminal = models.CharField(max_length=30, blank=True, null=True)
    telterminal = models.CharField(max_length=30, blank=True, null=True)
    contactoterminal = models.CharField(db_column='ContactoTerminal', max_length=30, blank=True,
                                        null=True)  # Field name made lowercase.
    bandera = models.CharField(max_length=30, blank=True, null=True)


class Booking2(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    empresa = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    pais = models.CharField(max_length=15, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    comboembarca = models.IntegerField(blank=True, null=True)
    cliente2 = models.CharField(max_length=45, blank=True, null=True)
    cliente3 = models.CharField(max_length=45, blank=True, null=True)
    cliente4 = models.CharField(max_length=45, blank=True, null=True)
    comboconsig = models.IntegerField(blank=True, null=True)
    direcconsigna = models.CharField(max_length=45, blank=True, null=True)
    localconsigna = models.CharField(max_length=45, blank=True, null=True)
    teleconsigna = models.CharField(max_length=45, blank=True, null=True)
    otralinea = models.CharField(max_length=45, blank=True, null=True)
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
    tipomov = models.CharField(max_length=30, blank=True, null=True)
    combotransport = models.IntegerField(blank=True, null=True)
    comboproduc = models.SmallIntegerField(blank=True, null=True)
    bultos = models.FloatField(blank=True, null=True)
    pesobruto = models.FloatField(blank=True, null=True)
    combounidad = models.CharField(max_length=3, blank=True, null=True)
    combotipo = models.CharField(max_length=15, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    net = models.TextField(blank=True, null=True)  # This field type is a guess.
    sold = models.TextField(blank=True, null=True)  # This field type is a guess.
    profit = models.TextField(blank=True, null=True)  # This field type is a guess.
    remarks = models.TextField(blank=True, null=True)  # This field type is a guess.
    vaporcli2 = models.BooleanField()
    vaporcli = models.BooleanField()


class Crt(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', max_length=35, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=22, blank=True, null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', max_length=22, blank=True,
                                 null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    cliente1 = models.CharField(db_column='Cliente1', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente2 = models.CharField(db_column='Cliente2', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente3 = models.CharField(db_column='Cliente3', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente4 = models.CharField(db_column='Cliente4', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    destina = models.CharField(db_column='Destina', max_length=50, blank=True, null=True)  # Field name made lowercase.
    direcdestina = models.CharField(db_column='DirecDestina', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    localdestina = models.CharField(db_column='LocalDestina', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    teledestina = models.CharField(db_column='TeleDestina', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    consigna = models.CharField(db_column='Consigna', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    direcconsigna = models.CharField(db_column='DirecConsigna', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    localconsigna = models.CharField(db_column='LocalConsigna', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    teleconsigna = models.CharField(db_column='TeleConsigna', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    notif = models.CharField(db_column='Notif', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dirnotif = models.CharField(db_column='DirNotif', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    otralinea2 = models.CharField(db_column='Otralinea2', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    telnotif = models.CharField(db_column='TelNotif', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    salede = models.CharField(db_column='Salede', max_length=80, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=80, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=80, blank=True,
                                 null=True)  # Field name made lowercase.
    porte1 = models.CharField(db_column='Porte1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    porte2 = models.CharField(db_column='Porte2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    porte3 = models.CharField(db_column='Porte3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    declaravalor = models.CharField(db_column='DeclaraValor', max_length=15, blank=True,
                                    null=True)  # Field name made lowercase.
    documanexo1 = models.CharField(db_column='DocumAnexo1', max_length=45, blank=True,
                                   null=True)  # Field name made lowercase.
    documanexo2 = models.CharField(db_column='DocumAnexo2', max_length=45, blank=True,
                                   null=True)  # Field name made lowercase.
    documanexo3 = models.CharField(db_column='DocumAnexo3', max_length=45, blank=True,
                                   null=True)  # Field name made lowercase.
    documanexo4 = models.CharField(db_column='DocumAnexo4', max_length=45, blank=True,
                                   null=True)  # Field name made lowercase.
    aduana1 = models.CharField(db_column='Aduana1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    aduana2 = models.CharField(db_column='Aduana2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    aduana3 = models.CharField(db_column='Aduana3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    aduana4 = models.CharField(db_column='Aduana4', max_length=45, blank=True, null=True)  # Field name made lowercase.
    aduana5 = models.CharField(db_column='Aduana5', max_length=45, blank=True, null=True)  # Field name made lowercase.
    declara1 = models.CharField(db_column='Declara1', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    declara2 = models.CharField(db_column='Declara2', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    declara3 = models.CharField(db_column='Declara3', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    declara4 = models.CharField(db_column='Declara4', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    declara5 = models.CharField(db_column='Declara5', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    destina1 = models.CharField(db_column='Destina1', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    destina2 = models.CharField(db_column='Destina2', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    destina3 = models.CharField(db_column='Destina3', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    fleteexterno = models.CharField(db_column='FleteExterno', max_length=12, blank=True,
                                    null=True)  # Field name made lowercase.
    reembolso = models.CharField(db_column='Reembolso', max_length=12, blank=True,
                                 null=True)  # Field name made lowercase.
    remite1 = models.CharField(db_column='Remite1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    remite2 = models.CharField(db_column='Remite2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    remite3 = models.CharField(db_column='Remite3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    signature2 = models.CharField(db_column='Signature2', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.
    fechaemi = models.CharField(db_column='FechaEmi', max_length=15, blank=True,
                                null=True)  # Field name made lowercase.


class Crt2(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=55, blank=True,
                                   null=True)  # Field name made lowercase.


class Cabezalocc(models.Model):
    numero = models.IntegerField()
    orden = models.CharField(max_length=30, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    cliente = models.IntegerField(blank=True, null=True)
    proveedor = models.IntegerField(blank=True, null=True)
    vaporcli2 = models.CharField(max_length=1, blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    despachante = models.IntegerField(blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)  # This field type is a guess.
    valor = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    estimadorecepcion = models.DateTimeField(blank=True, null=True)
    recepcion = models.DateTimeField(blank=True, null=True)
    recepcionado = models.CharField(max_length=1, blank=True, null=True)
    lugar = models.CharField(max_length=300, blank=True, null=True)
    embarcado = models.CharField(max_length=1, blank=True, null=True)
    periodo = models.CharField(max_length=20, blank=True, null=True)
    agevtas = models.IntegerField(blank=True, null=True)
    agecomp = models.IntegerField(blank=True, null=True)
    centro = models.CharField(max_length=25, blank=True, null=True)
    refproveedor = models.CharField(max_length=50, blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    comienzo = models.DateTimeField(blank=True, null=True)
    formapago = models.CharField(max_length=30, blank=True, null=True)
    expedir = models.CharField(db_column='Expedir', max_length=15, blank=True, null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    consignatario = models.IntegerField(db_column='Consignatario', blank=True, null=True)  # Field name made lowercase.
    cartaaprobacion = models.CharField(db_column='CartaAprobacion', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    ultimocomienzoembarque = models.DateTimeField(db_column='UltimoComienzoEmbarque', blank=True,
                                                  null=True)  # Field name made lowercase.


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
                                 related_name='prod_carga')
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True, choices=choice_tipo)
    cbm = models.FloatField(blank=True, null=True)
    mercaderia = models.TextField(db_column='Mercaderia', blank=True,
                                  null=True)  # Field name made lowercase. This field type is a guess.
    marcas = models.CharField(db_column='Marcas', max_length=150, blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=15, blank=True,
                                     null=True)  # Field name made lowercase.
    materialreceipt = models.CharField(db_column='MaterialReceipt', max_length=30, blank=True,
                                       null=True)  # Field name made lowercase.
    sobredimensionada = models.CharField(db_column='Sobredimensionada', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.


class VCargaaerea(models.Model):
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
    producto = models.IntegerField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True, choices=choice_tipo)
    cbm = models.FloatField(blank=True, null=True)
    mercaderia = models.TextField(db_column='Mercaderia', blank=True,
                                  null=True)  # Field name made lowercase. This field type is a guess.
    marcas = models.CharField(db_column='Marcas', max_length=150, blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=15, blank=True,
                                     null=True)  # Field name made lowercase.
    materialreceipt = models.CharField(db_column='MaterialReceipt', max_length=30, blank=True,
                                       null=True)  # Field name made lowercase.
    sobredimensionada = models.CharField(db_column='Sobredimensionada', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.

    def __str__(self, ):
        return str(self.numero)

    class Meta:
        managed = False
        db_table = 'seguimientos_cargaaerea'


class Cargaaereaaduana(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    producto = models.SmallIntegerField(db_column='Producto', blank=True, null=True)  # Field name made lowercase.
    bultos = models.IntegerField(db_column='Bultos', blank=True, null=True)  # Field name made lowercase.
    bruto = models.FloatField(db_column='Bruto', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    fechamanifiesto = models.DateTimeField(db_column='FechaManifiesto', blank=True,
                                           null=True)  # Field name made lowercase.
    enviado = models.CharField(db_column='Enviado', max_length=1, blank=True, null=True)  # Field name made lowercase.


class Claveguia(models.Model):
    awb = models.CharField(db_column='AWB', max_length=30)  # Field name made lowercase.


class Clavehawb(models.Model):
    hawb = models.CharField(db_column='HAWB', max_length=25)  # Field name made lowercase.


class Claveposicion(models.Model):
    posicion = models.CharField(db_column='Posicion', max_length=15)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=2)  # Field name made lowercase.


class Conexreserva(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=5, blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    salida = models.DateTimeField(db_column='Salida', blank=True, null=True)  # Field name made lowercase.
    llegada = models.DateTimeField(db_column='Llegada', blank=True, null=True)  # Field name made lowercase.
    cia = models.CharField(db_column='Cia', max_length=75, blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=15, blank=True, null=True)  # Field name made lowercase.


class Cronologia(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cantrecibida = models.CharField(db_column='CantRecibida', max_length=20, blank=True,
                                    null=True)  # Field name made lowercase.
    cantembarcado = models.CharField(db_column='CantEmbarcado', max_length=20, blank=True,
                                     null=True)  # Field name made lowercase.
    cantroto = models.CharField(db_column='CantRoto', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    cantperdido = models.CharField(db_column='CantPerdido', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.
    inspeccionadopor = models.CharField(db_column='InspeccionadoPor', max_length=50, blank=True,
                                        null=True)  # Field name made lowercase.
    recibidopor = models.CharField(db_column='RecibidoPor', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    trucknbr = models.CharField(db_column='TruckNbr', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.


class Detalleocc(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    codigo = models.CharField(max_length=40, blank=True, null=True)
    descripcion = models.CharField(max_length=400, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    costounit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    pesounit = models.FloatField(blank=True, null=True)
    contrato = models.CharField(max_length=40, blank=True, null=True)
    estilo = models.CharField(max_length=40, blank=True, null=True)
    seccion = models.CharField(max_length=40, blank=True, null=True)
    unidad = models.CharField(max_length=10, blank=True, null=True)
    talla = models.CharField(max_length=5, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    sku = models.CharField(max_length=30, blank=True, null=True)
    descripcion2 = models.CharField(db_column='Descripcion2', max_length=400, blank=True,
                                    null=True)  # Field name made lowercase.
    cantidadbkd = models.FloatField(db_column='CantidadBKD', blank=True, null=True)  # Field name made lowercase.
    volumen = models.FloatField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    bultos = models.IntegerField(db_column='Bultos', blank=True, null=True)  # Field name made lowercase.
    cantidadpre = models.FloatField(db_column='CantidadPRE', blank=True, null=True)  # Field name made lowercase.


class Entregadoc(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    entreguese = models.CharField(db_column='Entreguese', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    nombreentrega = models.CharField(db_column='NombreEntrega', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    direccionentrega = models.CharField(db_column='DireccionEntrega', max_length=50, blank=True,
                                        null=True)  # Field name made lowercase.
    ciudadentrega = models.CharField(db_column='CiudadEntrega', max_length=30, blank=True,
                                     null=True)  # Field name made lowercase.
    telefonoentrega = models.CharField(db_column='TelefonoEntrega', max_length=30, blank=True,
                                       null=True)  # Field name made lowercase.
    original = models.CharField(db_column='Original', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lista = models.CharField(db_column='Lista', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certorigen = models.CharField(db_column='CertOrigen', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    declara = models.CharField(db_column='Declara', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certflete = models.CharField(db_column='CertFlete', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    cerseguro = models.CharField(db_column='CerSeguro', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    copiahbl = models.CharField(db_column='CopiaHBL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    otros = models.CharField(db_column='Otros', max_length=1, blank=True, null=True)  # Field name made lowercase.
    detotros = models.CharField(db_column='DetOtros', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    detotros2 = models.CharField(db_column='DetOtros2', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    ordendep = models.CharField(db_column='OrdenDep', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certgastos = models.CharField(db_column='CertGastos', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    libre = models.CharField(db_column='Libre', max_length=1, blank=True, null=True)  # Field name made lowercase.
    eur1 = models.CharField(db_column='Eur1', max_length=1, blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(db_column='Factura', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nuestra = models.CharField(db_column='Nuestra', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certcalidad = models.CharField(db_column='CertCalidad', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    cumplido = models.CharField(db_column='Cumplido', max_length=1, blank=True, null=True)  # Field name made lowercase.
    transfer = models.CharField(db_column='Transfer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certpeligroso = models.CharField(db_column='CertPeligroso', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    imprimecom = models.CharField(db_column='ImprimeCom', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=80, blank=True, null=True)  # Field name made lowercase.
    remarks2 = models.CharField(db_column='Remarks2', max_length=80, blank=True,
                                null=True)  # Field name made lowercase.
    facturacom = models.CharField(db_column='FacturaCom', max_length=40, blank=True,
                                  null=True)  # Field name made lowercase.


class Entregaorden(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)
    codigo = models.CharField(max_length=40, blank=True, null=True)
    descripcion = models.CharField(max_length=400, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    entrega = models.DateTimeField(blank=True, null=True)
    entregareal = models.DateTimeField(blank=True, null=True)
    unidad = models.CharField(max_length=10, blank=True, null=True)
    arribo = models.DateTimeField(blank=True, null=True)
    materialreceipt = models.CharField(db_column='MaterialReceipt', max_length=30, blank=True,
                                       null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=15, blank=True,
                                     null=True)  # Field name made lowercase.


class Entregasocc(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    codigo = models.CharField(max_length=40, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    entrega = models.DateTimeField(blank=True, null=True)
    arribo = models.DateTimeField(blank=True, null=True)
    embarcar = models.CharField(db_column='Embarcar', max_length=1, blank=True, null=True)  # Field name made lowercase.
    materialreceipt = models.CharField(db_column='MaterialReceipt', max_length=30, blank=True,
                                       null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    boxempacado = models.DateTimeField(db_column='BoxEmpacado', blank=True, null=True)  # Field name made lowercase.
    boxmedidas = models.CharField(db_column='BoxMedidas', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    boxpeso = models.FloatField(db_column='BoxPeso', blank=True, null=True)  # Field name made lowercase.


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

    cantidad = models.FloatField()
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True,default=0)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True,default=0)
    marcas = models.CharField(max_length=50, blank=True, null=True,default='S/I')
    precinto = models.CharField(max_length=100, blank=True, null=True,default='S/I')
    tara = models.FloatField(blank=True, null=True,default=0)
    bonifcli = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True,default=0)
    envase = models.CharField(db_column='Envase', max_length=15, choices=choice_envase,default='S/I')  # Field name made lowercase.
    bultos = models.IntegerField()
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.

    profit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True,default=0)
    nrocontenedor = models.CharField(max_length=100, blank=True, null=True,default='S/I')
    volumen = models.FloatField(db_column='Volumen', blank=True, null=True,default=0)  # Field name made lowercase.
    temperatura = models.FloatField(db_column='Temperatura', blank=True, null=True,default=0)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True,default='N')  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', max_length=1, blank=True,
                                  null=True,default='C')  # Field name made lowercase.
    condespeciales = models.CharField(db_column='CondEspeciales', max_length=100, blank=True,
                                      null=True)  # Field name made lowercase.
    nomchofer = models.CharField(db_column='NomChofer', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    telchofer = models.CharField(db_column='TelChofer', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    horacitacion = models.CharField(db_column='HoraCitacion', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    horallegada = models.CharField(db_column='HoraLlegada', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    depositoretiro = models.IntegerField(db_column='DepositoRetiro', blank=True,
                                         null=True)  # Field name made lowercase.
    depositodev = models.IntegerField(db_column='DepositoDev', blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.IntegerField(db_column='Cotizacion', blank=True, null=True)  # Field name made lowercase.
    rucchofer = models.CharField(db_column='RucChofer', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    fechallegadaplanta = models.DateTimeField(db_column='FechaLlegadaPlanta', blank=True,
                                              null=True)  # Field name made lowercase.
    direccionentrega = models.SmallIntegerField(db_column='DireccionEntrega', blank=True,
                                                null=True)  # Field name made lowercase.
    fechacitacion = models.DateTimeField(db_column='FechaCitacion', blank=True, null=True)  # Field name made lowercase.
    ventilacion = models.CharField(db_column='Ventilacion', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.
    genset = models.CharField(db_column='GenSet', max_length=1, blank=True, null=True,default='N')  # Field name made lowercase.
    atmosferacontrolada = models.CharField(db_column='AtmosferaControlada', max_length=1, blank=True,
                                           null=True,default='N')  # Field name made lowercase.
    consolidacion = models.SmallIntegerField(db_column='Consolidacion', blank=True,
                                             null=True,default=0)  # Field name made lowercase.
    tipoventilacion = models.CharField(db_column='TipoVentilacion', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    pesovgm = models.FloatField(db_column='PesoVGM', blank=True, null=True)  # Field name made lowercase.
    humedad = models.SmallIntegerField(db_column='Humedad', blank=True, null=True,default=0)  # Field name made lowercase.


class Faxes(models.Model):
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
    notas = models.TextField(blank=True, null=True)  # This field type is a guess.
    asunto = models.TextField(blank=True, null=True)  # This field type is a guess.
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, blank=True, null=True)


class Faxesoc(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)  # This field type is a guess.
    asunto = models.TextField(blank=True, null=True)  # This field type is a guess.
    tipo = models.CharField(max_length=2, blank=True, null=True)


class Fisico(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    marcas = models.CharField(db_column='Marcas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    precinto = models.CharField(db_column='Precinto', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    tara = models.IntegerField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True,
                                null=True)  # Field name made lowercase.
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    deposito = models.SmallIntegerField(db_column='Deposito', blank=True, null=True)  # Field name made lowercase.


class Gastoshijos(models.Model):
    cliente = models.IntegerField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.
    codigo = models.SmallIntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True,
                                null=True)  # Field name made lowercase.
    tipogasto = models.CharField(db_column='TipoGasto', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.


class Guiasgrabadas(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', max_length=35, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=22, blank=True, null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', max_length=22, blank=True,
                                 null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    cliente1 = models.CharField(db_column='Cliente1', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente2 = models.CharField(db_column='Cliente2', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente3 = models.CharField(db_column='Cliente3', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente4 = models.CharField(db_column='Cliente4', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    consigna = models.CharField(db_column='Consigna', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    direcconsigna = models.CharField(db_column='DirecConsigna', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    localconsigna = models.CharField(db_column='LocalConsigna', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    teleconsigna = models.CharField(db_column='TeleConsigna', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    otralinea = models.CharField(db_column='Otralinea', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    empresa2 = models.CharField(db_column='Empresa2', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    otracarrier = models.CharField(db_column='OtraCarrier', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    localidad2 = models.CharField(db_column='Localidad2', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    otrosdeagente = models.CharField(db_column='OtrosdeAgente', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    iata = models.CharField(db_column='Iata', max_length=15, blank=True, null=True)  # Field name made lowercase.
    salede = models.CharField(db_column='Salede', max_length=25, blank=True, null=True)  # Field name made lowercase.
    cadenaaerea = models.CharField(db_column='CadenaAerea', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.
    tipoflete = models.CharField(db_column='TipoFlete', max_length=18, blank=True,
                                 null=True)  # Field name made lowercase.
    numerolc = models.CharField(db_column='Numerolc', max_length=26, blank=True,
                                null=True)  # Field name made lowercase.
    notif = models.CharField(db_column='Notif', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dirnotif = models.CharField(db_column='DirNotif', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    otralinea2 = models.CharField(db_column='Otralinea2', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    telnotif = models.CharField(db_column='TelNotif', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    otralinea3 = models.CharField(db_column='Otralinea3', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    otralinea4 = models.CharField(db_column='Otralinea4', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=3, blank=True, null=True)  # Field name made lowercase.
    idtransport = models.CharField(db_column='Idtransport', max_length=2, blank=True,
                                   null=True)  # Field name made lowercase.
    to1 = models.CharField(db_column='To1', max_length=3, blank=True, null=True)  # Field name made lowercase.
    by1 = models.CharField(db_column='By1', max_length=2, blank=True, null=True)  # Field name made lowercase.
    to2 = models.CharField(db_column='To2', max_length=3, blank=True, null=True)  # Field name made lowercase.
    by2 = models.CharField(db_column='By2', max_length=2, blank=True, null=True)  # Field name made lowercase.
    simbolo = models.CharField(db_column='Simbolo', max_length=4, blank=True, null=True)  # Field name made lowercase.
    carriage = models.CharField(db_column='Carriage', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    custom = models.CharField(db_column='Custom', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nombredestino = models.CharField(db_column='NombreDestino', max_length=22, blank=True,
                                     null=True)  # Field name made lowercase.
    vuelo1 = models.CharField(db_column='Vuelo1', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vuelo2 = models.CharField(db_column='Vuelo2', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vuelo3 = models.CharField(db_column='Vuelo3', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vuelo4 = models.CharField(db_column='Vuelo4', max_length=15, blank=True, null=True)  # Field name made lowercase.
    valseguro = models.CharField(db_column='ValSeguro', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    cliente5 = models.CharField(db_column='Cliente5', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.


class Guiasgrabadas2(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    marcas = models.CharField(db_column='Marcas', max_length=80, blank=True, null=True)  # Field name made lowercase.
    otraline = models.CharField(db_column='Otraline', max_length=80, blank=True,
                                null=True)  # Field name made lowercase.
    attached = models.CharField(db_column='Attached', max_length=80, blank=True,
                                null=True)  # Field name made lowercase.
    nature1 = models.CharField(db_column='Nature1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature2 = models.CharField(db_column='Nature2', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature3 = models.CharField(db_column='Nature3', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature4 = models.CharField(db_column='Nature4', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature5 = models.CharField(db_column='Nature5', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature6 = models.CharField(db_column='Nature6', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature7 = models.CharField(db_column='Nature7', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature8 = models.CharField(db_column='Nature8', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature9 = models.CharField(db_column='Nature9', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature10 = models.CharField(db_column='Nature10', max_length=25, blank=True,
                                null=True)  # Field name made lowercase.
    nature11 = models.CharField(db_column='Nature11', max_length=25, blank=True,
                                null=True)  # Field name made lowercase.
    nature12 = models.CharField(db_column='Nature12', max_length=25, blank=True,
                                null=True)  # Field name made lowercase.
    free1 = models.CharField(db_column='Free1', max_length=60, blank=True, null=True)  # Field name made lowercase.
    free2 = models.CharField(db_column='Free2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    free3 = models.CharField(db_column='Free3', max_length=60, blank=True, null=True)  # Field name made lowercase.
    free4 = models.CharField(db_column='Free4', max_length=60, blank=True, null=True)  # Field name made lowercase.
    free5 = models.CharField(db_column='Free5', max_length=60, blank=True, null=True)  # Field name made lowercase.
    other1 = models.CharField(db_column='Other1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    other2 = models.CharField(db_column='Other2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    other3 = models.CharField(db_column='Other3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    fechaemi = models.CharField(db_column='Fechaemi', max_length=12, blank=True,
                                null=True)  # Field name made lowercase.
    restotext = models.CharField(db_column='Restotext', max_length=25, blank=True,
                                 null=True)  # Field name made lowercase.
    portext = models.CharField(db_column='Portext', max_length=40, blank=True, null=True)  # Field name made lowercase.
    gastosconiva = models.BooleanField(db_column='GastosconIva', blank=True, null=True)  # Field name made lowercase.
    nature13 = models.CharField(db_column='Nature13', max_length=25, blank=True,
                                null=True)  # Field name made lowercase.
    nature14 = models.CharField(db_column='Nature14', max_length=25, blank=True,
                                null=True)  # Field name made lowercase.
    nature15 = models.CharField(db_column='Nature15', max_length=25, blank=True,
                                null=True)  # Field name made lowercase.
    nature16 = models.CharField(db_column='Nature16', max_length=25, blank=True,
                                null=True)  # Field name made lowercase.
    nature17 = models.CharField(db_column='Nature17', max_length=25, blank=True,
                                null=True)  # Field name made lowercase.
    nature18 = models.CharField(db_column='Nature18', max_length=25, blank=True,
                                null=True)  # Field name made lowercase.
    nature19 = models.CharField(db_column='Nature19', max_length=25, blank=True,
                                null=True)  # Field name made lowercase.
    asagent = models.CharField(db_column='AsAgent', max_length=70, blank=True, null=True)  # Field name made lowercase.
    ofthecarrier = models.CharField(db_column='OfTheCarrier', max_length=70, blank=True,
                                    null=True)  # Field name made lowercase.


class Guiasgrabadas3(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    piezas = models.CharField(db_column='Piezas', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas2 = models.CharField(db_column='Piezas2', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas3 = models.CharField(db_column='Piezas3', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas4 = models.CharField(db_column='Piezas4', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas5 = models.CharField(db_column='Piezas5', max_length=4, blank=True, null=True)  # Field name made lowercase.
    totpiezas = models.CharField(db_column='TotPiezas', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    gross = models.CharField(db_column='Gross', max_length=10, blank=True, null=True)  # Field name made lowercase.
    otrogross = models.CharField(db_column='OtroGross', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    otrogross2 = models.CharField(db_column='OtroGross2', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
    otrogross3 = models.CharField(db_column='OtroGross3', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
    otrogross4 = models.CharField(db_column='OtroGross4', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
    totgross = models.CharField(db_column='TotGross', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
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
    commodity = models.CharField(db_column='Commodity', max_length=8, blank=True,
                                 null=True)  # Field name made lowercase.
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
    totalfinal = models.CharField(db_column='TotalFinal', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
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
    totalprepaid = models.CharField(db_column='TotalPrepaid', max_length=10, blank=True,
                                    null=True)  # Field name made lowercase.
    totalcollect = models.CharField(db_column='TotalCollect', max_length=10, blank=True,
                                    null=True)  # Field name made lowercase.
    totalpprate = models.CharField(db_column='TotalPPRate', max_length=10, blank=True,
                                   null=True)  # Field name made lowercase.
    totalccrate = models.CharField(db_column='TotalCCRate', max_length=10, blank=True,
                                   null=True)  # Field name made lowercase.
    cass = models.CharField(db_column='Cass', max_length=30, blank=True, null=True)  # Field name made lowercase.
    chgscode = models.CharField(db_column='ChgsCode', max_length=2, blank=True, null=True)  # Field name made lowercase.
    wtval = models.CharField(db_column='WtVal', max_length=2, blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(db_column='Other', max_length=2, blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    carrierfinal = models.CharField(db_column='CarrierFinal', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.


class Mbl(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', max_length=35, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=22, blank=True, null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', max_length=22, blank=True,
                                 null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    cliente1 = models.CharField(db_column='Cliente1', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente2 = models.CharField(db_column='Cliente2', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente3 = models.CharField(db_column='Cliente3', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente4 = models.CharField(db_column='Cliente4', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    consigna = models.CharField(db_column='Consigna', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    direcconsigna = models.CharField(db_column='DirecConsigna', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    localconsigna = models.CharField(db_column='LocalConsigna', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    teleconsigna = models.CharField(db_column='TeleConsigna', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    otralinea = models.CharField(db_column='Otralinea', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    notif = models.CharField(db_column='Notif', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dirnotif = models.CharField(db_column='DirNotif', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    otralinea2 = models.CharField(db_column='Otralinea2', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    telnotif = models.CharField(db_column='TelNotif', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    tipoflete = models.CharField(db_column='TipoFlete', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    salede = models.CharField(db_column='Salede', max_length=35, blank=True, null=True)  # Field name made lowercase.
    vapor = models.CharField(db_column='Vapor', max_length=35, blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=35, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=35, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=35, blank=True,
                                 null=True)  # Field name made lowercase.
    delivery = models.CharField(db_column='Delivery', max_length=35, blank=True,
                                null=True)  # Field name made lowercase.
    transterms = models.CharField(db_column='TransTerms', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.
    simbolo = models.CharField(db_column='Simbolo', max_length=4, blank=True, null=True)  # Field name made lowercase.
    condentrega = models.CharField(db_column='CondEntrega', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.
    tipomov = models.CharField(db_column='TipoMov', max_length=15, blank=True, null=True)  # Field name made lowercase.
    carriage = models.CharField(db_column='Carriage', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    custom = models.CharField(db_column='Custom', max_length=10, blank=True, null=True)  # Field name made lowercase.
    valseguro = models.CharField(db_column='ValSeguro', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    goods = models.TextField(db_column='Goods', blank=True,
                             null=True)  # Field name made lowercase. This field type is a guess.
    free1 = models.CharField(db_column='Free1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    free2 = models.CharField(db_column='Free2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    free3 = models.CharField(db_column='Free3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    signature2 = models.CharField(db_column='Signature2', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    signature3 = models.CharField(db_column='Signature3', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    nbls = models.CharField(db_column='Nbls', max_length=2, blank=True, null=True)  # Field name made lowercase.
    payable = models.CharField(db_column='Payable', max_length=15, blank=True, null=True)  # Field name made lowercase.
    board = models.CharField(db_column='Board', max_length=15, blank=True, null=True)  # Field name made lowercase.
    clean = models.CharField(db_column='Clean', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fechaemi = models.CharField(db_column='FechaEmi', max_length=12, blank=True,
                                null=True)  # Field name made lowercase.
    restotext = models.CharField(db_column='RestoText', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    vadeclared = models.BooleanField(db_column='VaDeclared', blank=True, null=True)  # Field name made lowercase.
    portext = models.CharField(db_column='PorText', max_length=15, blank=True, null=True)  # Field name made lowercase.


class Mbl2(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    marks = models.CharField(db_column='Marks', max_length=30, blank=True, null=True)  # Field name made lowercase.
    packages = models.CharField(db_column='Packages', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    gross = models.CharField(db_column='Gross', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tare = models.CharField(db_column='Tare', max_length=30, blank=True, null=True)  # Field name made lowercase.


class Madresgrabadas(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', max_length=35, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=22, blank=True, null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', max_length=22, blank=True,
                                 null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    cliente1 = models.CharField(db_column='Cliente1', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente2 = models.CharField(db_column='Cliente2', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente3 = models.CharField(db_column='Cliente3', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    cliente4 = models.CharField(db_column='Cliente4', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    consigna = models.CharField(db_column='Consigna', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    direcconsigna = models.CharField(db_column='DirecConsigna', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    localconsigna = models.CharField(db_column='LocalConsigna', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    teleconsigna = models.CharField(db_column='TeleConsigna', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    otralinea = models.CharField(db_column='Otralinea', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    empresa2 = models.CharField(db_column='Empresa2', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    otracarrier = models.CharField(db_column='OtraCarrier', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    localidad2 = models.CharField(db_column='Localidad2', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    otrosdeagente = models.CharField(db_column='OtrosdeAgente', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    iata = models.CharField(db_column='Iata', max_length=15, blank=True, null=True)  # Field name made lowercase.
    salede = models.CharField(db_column='Salede', max_length=25, blank=True, null=True)  # Field name made lowercase.
    cadenaaerea = models.CharField(db_column='CadenaAerea', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.
    tipoflete = models.CharField(db_column='TipoFlete', max_length=18, blank=True,
                                 null=True)  # Field name made lowercase.
    notif = models.CharField(db_column='Notif', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dirnotif = models.CharField(db_column='DirNotif', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    otralinea2 = models.CharField(db_column='Otralinea2', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    telnotif = models.CharField(db_column='TelNotif', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    otralinea3 = models.CharField(db_column='Otralinea3', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    otralinea4 = models.CharField(db_column='Otralinea4', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=3, blank=True, null=True)  # Field name made lowercase.
    idtransport = models.CharField(db_column='Idtransport', max_length=2, blank=True,
                                   null=True)  # Field name made lowercase.
    to1 = models.CharField(db_column='To1', max_length=3, blank=True, null=True)  # Field name made lowercase.
    by1 = models.CharField(db_column='By1', max_length=2, blank=True, null=True)  # Field name made lowercase.
    to2 = models.CharField(db_column='To2', max_length=3, blank=True, null=True)  # Field name made lowercase.
    by2 = models.CharField(db_column='By2', max_length=2, blank=True, null=True)  # Field name made lowercase.
    simbolo = models.CharField(db_column='Simbolo', max_length=4, blank=True, null=True)  # Field name made lowercase.
    carriage = models.CharField(db_column='Carriage', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    custom = models.CharField(db_column='Custom', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nombredestino = models.CharField(db_column='NombreDestino', max_length=22, blank=True,
                                     null=True)  # Field name made lowercase.
    vuelo1 = models.CharField(db_column='Vuelo1', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vuelo2 = models.CharField(db_column='Vuelo2', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vuelo3 = models.CharField(db_column='Vuelo3', max_length=15, blank=True, null=True)  # Field name made lowercase.
    vuelo4 = models.CharField(db_column='Vuelo4', max_length=15, blank=True, null=True)  # Field name made lowercase.
    valseguro = models.CharField(db_column='ValSeguro', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    marcas = models.CharField(db_column='Marcas', max_length=80, blank=True, null=True)  # Field name made lowercase.
    otraline = models.CharField(db_column='Otraline', max_length=80, blank=True,
                                null=True)  # Field name made lowercase.
    attached = models.CharField(db_column='Attached', max_length=80, blank=True,
                                null=True)  # Field name made lowercase.
    nature2 = models.CharField(db_column='Nature2', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nature3 = models.CharField(db_column='Nature3', max_length=25, blank=True, null=True)  # Field name made lowercase.
    houses = models.CharField(db_column='Houses', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses2 = models.CharField(db_column='Houses2', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses3 = models.CharField(db_column='Houses3', max_length=28, blank=True, null=True)  # Field name made lowercase.
    free1 = models.CharField(db_column='Free1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    free2 = models.CharField(db_column='Free2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    free3 = models.CharField(db_column='Free3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    free4 = models.CharField(db_column='Free4', max_length=45, blank=True, null=True)  # Field name made lowercase.
    free5 = models.CharField(db_column='Free5', max_length=45, blank=True, null=True)  # Field name made lowercase.
    other1 = models.CharField(db_column='Other1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    other2 = models.CharField(db_column='Other2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    other3 = models.CharField(db_column='Other3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    fechaemi = models.CharField(db_column='Fechaemi', max_length=12, blank=True,
                                null=True)  # Field name made lowercase.
    restotext = models.CharField(db_column='RestoText', max_length=25, blank=True,
                                 null=True)  # Field name made lowercase.
    portext = models.CharField(db_column='PorText', max_length=40, blank=True, null=True)  # Field name made lowercase.
    houses4 = models.CharField(db_column='Houses4', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses5 = models.CharField(db_column='Houses5', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses6 = models.CharField(db_column='Houses6', max_length=28, blank=True, null=True)  # Field name made lowercase.
    asagent = models.CharField(db_column='AsAgent', max_length=70, blank=True, null=True)  # Field name made lowercase.
    ofthecarrier = models.CharField(db_column='OfTheCarrier', max_length=70, blank=True,
                                    null=True)  # Field name made lowercase.


class Madresgrabadas3(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    piezas = models.CharField(db_column='Piezas', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas2 = models.CharField(db_column='Piezas2', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas3 = models.CharField(db_column='Piezas3', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas4 = models.CharField(db_column='Piezas4', max_length=4, blank=True, null=True)  # Field name made lowercase.
    piezas5 = models.CharField(db_column='Piezas5', max_length=4, blank=True, null=True)  # Field name made lowercase.
    totpiezas = models.CharField(db_column='TotPiezas', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    gross = models.CharField(db_column='Gross', max_length=10, blank=True, null=True)  # Field name made lowercase.
    otrogross = models.CharField(db_column='OtroGross', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    otrogross2 = models.CharField(db_column='OtroGross2', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
    otrogross3 = models.CharField(db_column='OtroGross3', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
    otrogross4 = models.CharField(db_column='OtroGross4', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
    totgross = models.CharField(db_column='TotGross', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
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
    commodity = models.CharField(db_column='Commodity', max_length=8, blank=True,
                                 null=True)  # Field name made lowercase.
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
    totalfinal = models.CharField(db_column='TotalFinal', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
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
    totalprepaid = models.CharField(db_column='TotalPrepaid', max_length=10, blank=True,
                                    null=True)  # Field name made lowercase.
    totalcollect = models.CharField(db_column='TotalCollect', max_length=10, blank=True,
                                    null=True)  # Field name made lowercase.
    totalpprate = models.CharField(db_column='TotalPPRate', max_length=10, blank=True,
                                   null=True)  # Field name made lowercase.
    totalccrate = models.CharField(db_column='TotalCCRate', max_length=10, blank=True,
                                   null=True)  # Field name made lowercase.
    cass = models.CharField(db_column='Cass', max_length=30, blank=True, null=True)  # Field name made lowercase.
    chgscode = models.CharField(db_column='ChgsCode', max_length=2, blank=True, null=True)  # Field name made lowercase.
    wtval = models.CharField(db_column='WtVal', max_length=2, blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(db_column='Other', max_length=2, blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    carrierfinal = models.CharField(db_column='CarrierFinal', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.


class Reservas(models.Model):
    numero = models.IntegerField()
    transportista = models.IntegerField(blank=True, null=True)
    armador = models.IntegerField(blank=True, null=True)
    agente = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    awb = models.CharField(max_length=40, blank=True, null=True, unique=True)
    cotizacion = models.SmallIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    vapor = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(max_length=20, blank=True, null=True)
    aplicable = models.FloatField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    modo = models.CharField(max_length=20, blank=True, null=True)
    embarque = models.IntegerField(blank=True, null=True)
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    pagoflete = models.CharField(db_column='PagoFlete', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    arbitraje = models.FloatField(db_column='Arbitraje', blank=True, null=True)  # Field name made lowercase.
    tomopeso = models.SmallIntegerField(db_column='TomoPeso', blank=True, null=True)  # Field name made lowercase.
    tarifaawb = models.DecimalField(db_column='TarifaAWB', max_digits=19, decimal_places=4, blank=True,
                                    null=True)  # Field name made lowercase.
    kilos = models.FloatField(db_column='Kilos', blank=True, null=True)  # Field name made lowercase.
    volumen = models.FloatField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    tarifafija = models.CharField(db_column='TarifaFija', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.


class VGrillaSeguimientos(models.Model):
    numero = models.IntegerField()
    modo = models.CharField(max_length=20, blank=True, null=True)
    cliente = models.CharField(max_length=500, blank=True, null=True)
    direccion_cliente = models.CharField(max_length=500, blank=True, null=True)
    telefono_cliente = models.CharField(max_length=500, blank=True, null=True)
    cliente_codigo = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    origen_text = models.CharField(max_length=50, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    destino_text = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    notas = models.CharField(max_length=1000, blank=True, null=True)
    consignatario = models.CharField(max_length=1000, blank=True, null=True)
    consignatario_codigo = models.IntegerField(blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    agente = models.CharField(max_length=1000, blank=True, null=True)
    agente_codigo = models.IntegerField(blank=True, null=True)
    embarcador = models.CharField(max_length=1000, blank=True, null=True)
    embarcador_codigo = models.IntegerField(blank=True, null=True)
    vaporcli = models.CharField(db_column='Vaporcli', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vencimiento = models.DateTimeField(blank=True, null=True)
    embarque = models.IntegerField(blank=True, null=True)
    vapor = models.CharField(max_length=200, blank=True, null=True)
    vapor_codigo = models.CharField(max_length=30, blank=True, null=True)
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=40, blank=True, null=True)
    volumen = models.FloatField(blank=True, null=True)
    tarifaventa = models.FloatField(blank=True, null=True)
    tarifacompra = models.FloatField(blank=True, null=True)
    pago = models.CharField(max_length=10, blank=True, null=True)
    refcliente = models.CharField(max_length=1024, blank=True, null=True)
    transportista = models.CharField(max_length=1000, blank=True, null=True)
    transportista_codigo = models.IntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=30, blank=True, null=True)
    cotizacion = models.IntegerField(blank=True, null=True)
    cotizacion1 = models.IntegerField(blank=True, null=True)
    vaporcli2 = models.CharField(max_length=1, blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    vendedor = models.CharField(max_length=500, blank=True, null=True)
    vendedor_codigo = models.SmallIntegerField(blank=True, null=True)
    despachante = models.IntegerField(blank=True, null=True)
    agecompras = models.CharField(max_length=500, blank=True, null=True)
    agecompras_codigo = models.IntegerField(blank=True, null=True)
    ageventas = models.CharField(max_length=500, blank=True, null=True)
    ageventas_codigo = models.IntegerField(blank=True, null=True)
    deposito = models.CharField(max_length=500, blank=True, null=True)
    deposito_codigo = models.IntegerField(blank=True, null=True)
    recepcion = models.DateTimeField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    nrodespacho = models.CharField(max_length=20, blank=True, null=True)
    aduana = models.CharField(max_length=20, blank=True, null=True)
    fecacepta = models.DateTimeField(blank=True, null=True)
    fecentrega = models.DateTimeField(blank=True, null=True)
    fecretiro = models.DateTimeField(blank=True, null=True)
    totalgiro = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    nroguiadesp = models.CharField(max_length=20, blank=True, null=True)
    aplicable = models.FloatField(blank=True, null=True)
    refproveedor = models.CharField(max_length=250, blank=True, null=True)
    estimadorecepcion = models.DateTimeField(blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)
    etd = models.DateTimeField(blank=True, null=True)
    recepcionado = models.CharField(max_length=1, blank=True, null=True)
    lugar = models.CharField(max_length=30, blank=True, null=True)
    fecaduana = models.DateTimeField(db_column='Fecaduana', blank=True, null=True)  # Field name made lowercase.
    fecdocage = models.DateTimeField(db_column='Fecdocage', blank=True, null=True)  # Field name made lowercase.
    fecrecdoc = models.DateTimeField(blank=True, null=True)
    fecemision = models.DateTimeField(blank=True, null=True)
    fecseguro = models.DateTimeField(blank=True, null=True)
    nroseguro = models.CharField(max_length=10, blank=True, null=True)
    valor = models.CharField(max_length=20, blank=True, null=True)
    manifiesto = models.CharField(max_length=20, blank=True, null=True)
    ubicacion = models.CharField(max_length=20, blank=True, null=True)
    fecpagoder = models.DateTimeField(blank=True, null=True)
    tarifafija = models.CharField(max_length=1, blank=True, null=True)
    tomopeso = models.SmallIntegerField(blank=True, null=True)
    fecpresdi = models.DateTimeField(blank=True, null=True)
    prima = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    centro = models.CharField(max_length=25, blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    transportelocal = models.IntegerField(blank=True, null=True)
    estimadopup = models.DateTimeField(blank=True, null=True)
    realpup = models.DateTimeField(blank=True, null=True)
    estimadodelivery = models.DateTimeField(blank=True, null=True)
    realdelivery = models.DateTimeField(blank=True, null=True)
    referencialocal = models.CharField(max_length=50, blank=True, null=True)
    modolocal = models.CharField(max_length=10, blank=True, null=True)
    fecguiadesp = models.DateTimeField(blank=True, null=True)
    tarifaprofit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    armador = models.CharField(max_length=1000, blank=True, null=True)
    armador_codigo = models.CharField(max_length=1000, blank=True, null=True)
    notificar = models.CharField(max_length=1000, blank=True, null=True)
    notificar_codigo = models.IntegerField(blank=True, null=True)
    fechaonhand = models.DateTimeField(db_column='FechaOnHand', blank=True, null=True)  # Field name made lowercase.
    booking = models.CharField(max_length=30, blank=True, null=True)
    propia = models.CharField(db_column='Propia', max_length=1, blank=True, null=True)  # Field name made lowercase.
    trafico = models.SmallIntegerField(db_column='Trafico', blank=True, null=True)  # Field name made lowercase.
    trafico_codigo = models.SmallIntegerField(blank=True, null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    proyecto_codigo = models.SmallIntegerField(blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    modificado = models.CharField(db_column='Modificado', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    depcontenedoringreso = models.SmallIntegerField(db_column='DepContenedorIngreso', blank=True,
                                                    null=True)  # Field name made lowercase.
    depcontenedorvacios = models.SmallIntegerField(db_column='DepContenedorVacios', blank=True,
                                                   null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    deadborrador = models.DateTimeField(db_column='DeadBorrador', blank=True, null=True)  # Field name made lowercase.
    deaddocumentos = models.DateTimeField(db_column='DeadDocumentos', blank=True,
                                          null=True)  # Field name made lowercase.
    deadentrega = models.DateTimeField(db_column='DeadEntrega', blank=True, null=True)  # Field name made lowercase.
    deadliberacion = models.DateTimeField(db_column='DeadLiberacion', blank=True,
                                          null=True)  # Field name made lowercase.
    retiravacio = models.DateTimeField(db_column='RetiraVacio', blank=True, null=True)  # Field name made lowercase.
    retiralleno = models.DateTimeField(db_column='RetiraLleno', blank=True, null=True)  # Field name made lowercase.
    arriboreal = models.DateTimeField(db_column='ArriboReal', blank=True, null=True)  # Field name made lowercase.
    pagoenfirme = models.DateTimeField(db_column='PagoenFirme', blank=True, null=True)  # Field name made lowercase.
    recepcionprealert = models.DateTimeField(db_column='RecepcionPrealert', blank=True,
                                             null=True)  # Field name made lowercase.
    bltipo = models.CharField(db_column='BLTipo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    credito = models.CharField(db_column='Credito', max_length=50, blank=True, null=True)  # Field name made lowercase.
    revalidacion = models.DateTimeField(db_column='Revalidacion', blank=True, null=True)  # Field name made lowercase.
    almacenajelibrehasta = models.DateTimeField(db_column='AlmacenajeLibreHasta', blank=True,
                                                null=True)  # Field name made lowercase.
    demoraslibrehasta = models.DateTimeField(db_column='DemorasLibreHasta', blank=True,
                                             null=True)  # Field name made lowercase.
    entregavacio = models.DateTimeField(db_column='EntregaVacio', blank=True, null=True)  # Field name made lowercase.
    tipobonifcli = models.CharField(db_column='TipoBonifCli', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    bonifcli = models.FloatField(db_column='BonifCli', blank=True, null=True)  # Field name made lowercase.
    originales = models.CharField(db_column='Originales', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    consolidado = models.SmallIntegerField(db_column='Consolidado', blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    demora = models.SmallIntegerField(db_column='Demora', blank=True, null=True)  # Field name made lowercase.
    valordemoravta = models.DecimalField(db_column='ValorDemoraVTA', max_digits=19, decimal_places=4, blank=True,
                                         null=True)  # Field name made lowercase.
    valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=19, decimal_places=4, blank=True,
                                         null=True)  # Field name made lowercase.
    rotulosincorrectos = models.CharField(db_column='RotulosIncorrectos', max_length=1, blank=True,
                                          null=True)  # Field name made lowercase.
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    actividad_codigo = models.IntegerField(blank=True, null=True)
    entregadoa = models.CharField(db_column='EntregadoA', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    loadingdate = models.DateTimeField(db_column='LoadingDate', blank=True, null=True)  # Field name made lowercase.
    diasalmacenaje = models.SmallIntegerField(db_column='DiasAlmacenaje', blank=True,
                                              null=True)  # Field name made lowercase.
    muestroflete = models.DecimalField(db_column='MuestroFlete', max_digits=19, decimal_places=4, blank=True,
                                       null=True)  # Field name made lowercase.
    choice_op = (("IMPORTACION", "IMPORTACION"),
                 ("EXPORTACION", "EXPORTACION"),
                 ("EXPORTACION FCL", "EXPORTACION FCL"),
                 ("IMPORTACION LCL", "IMPORTACION LCL"),
                 ("IMPORTACION FCL", "IMPORTACION FCL"),
                 ("EXPORTACION CONSOLIDADA", "EXPORTACION CONSOLIDADA"),
                 ("IMPORTACION PART CONT.", "IMPORTACION PART CONT."),
                 ("TRANSITO FCL", "TRANSITO FCL"),
                 ("IMPORTACION CONSOLIDADA", "IMPORTACION CONSOLIDADA"),
                 ("REEMBARCO", "REEMBARCO"),
                 ("COURIER", "COURIER"),
                 ("TRANSITO", "TRANSITO"),
                 ("EXPORTACION LCL", "EXPORTACION LCL"),
                 ("EXPORTACION PART CONT.", "EXPORTACION PART CONT."),
                 ("DUA", "DUA"),
                 ("TRASLADO", "TRASLADO"),
                 ("MUESTRA", "MUESTRA"),
                 ("", ""),
                 )
    operacion = models.CharField(db_column='Operacion', max_length=25, blank=True, null=True,
                                 choices=choice_op)  # Field name made lowercase.
    enviointtrabk = models.CharField(db_column='EnvioInttraBK', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    enviointtrasi = models.CharField(db_column='EnvioInttraSI', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    maerskbk = models.CharField(db_column='MaerskBK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    maersksi = models.CharField(db_column='MaerskSI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wwanumerobooking = models.IntegerField(db_column='WWANumeroBooking', blank=True,
                                           null=True)  # Field name made lowercase.
    envioeasipassbk = models.CharField(db_column='EnvioEASIPASSBK', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    envioeasipasssi = models.CharField(db_column='EnvioEASIPASSSI', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    fechastacking = models.DateTimeField(db_column='FechaStacking', blank=True, null=True)  # Field name made lowercase.
    horastacking = models.CharField(db_column='HoraStacking', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    fechafinstacking = models.DateTimeField(db_column='FechaFinStacking', blank=True,
                                            null=True)  # Field name made lowercase.
    horafinstacking = models.CharField(db_column='HoraFinStacking', max_length=30, blank=True,
                                       null=True)  # Field name made lowercase.
    fechacutoff = models.DateTimeField(db_column='FechaCutOff', blank=True, null=True)  # Field name made lowercase.
    horacutoff = models.CharField(db_column='HoraCutOff', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    tieneseguro = models.CharField(db_column='TieneSeguro', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    fechacutoffvgm = models.DateTimeField(db_column='FechaCutOffVGM', blank=True,
                                          null=True)  # Field name made lowercase.
    horacutoffvgm = models.CharField(db_column='HoraCutOffVGM', max_length=30, blank=True,
                                     null=True)  # Field name made lowercase.
    nroreferedi = models.IntegerField(db_column='NroReferEDI', blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    deaddocumentoshora = models.CharField(db_column='DeadDocumentosHora', max_length=10, blank=True,
                                          null=True)  # Field name made lowercase.
    emailem = models.CharField(db_column='emailEM', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailea = models.CharField(db_column='emailEA', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailet = models.CharField(db_column='emailET', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailim = models.CharField(db_column='emailIM', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailia = models.CharField(db_column='emailIA', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailit = models.CharField(db_column='emailIT', max_length=500, blank=True, null=True)  # Field name made lowercase.
    buque_viaje = models.CharField(db_column='buque_viaje', max_length=500, blank=True, null=True)  # Field name made lowercase.

    def __str__(self, ):
        return self.modo + ' - ' + str(self.numero)

    class Meta:
        managed = False
        db_table = 'VGrillaSeguimientos'


#
# class Seguimiento(models.Model):
#     numero = models.IntegerField(unique=True)
#     cliente = models.IntegerField(blank=True, null=True)
#     consignatario = models.IntegerField(blank=True, null=True)
#     origen = models.CharField(max_length=5, blank=True, null=True)
#     destino = models.CharField(max_length=5, blank=True, null=True)
#     terminos = models.CharField(max_length=3, blank=True, null=True)
#     observaciones = models.TextField( blank=True, null=True)  # This field type is a guess.
#     # status = models.CharField(max_length=20, blank=True, null=True)
#     # agente = models.IntegerField(blank=True, null=True)
#     # embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
#     status = models.CharField(max_length=20, choices=(("Collect", "Collect"), ("Prepaid", "Prepaid"),), blank=True,
#                               null=True)
#     agente = models.ForeignKey(Clientes,to_field='codigo',on_delete=models.PROTECT,db_column='agente',blank=True,null=True,related_name='cli8')
#     embarcador = models.ForeignKey(Clientes,to_field='codigo', db_column='Embarcador',on_delete=models.PROTECT,blank=True,null=True,related_name='cli2')  # Field name made lowercase.
#     vaporcli = models.CharField(db_column='Vaporcli', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     modo = models.CharField(max_length=20, blank=True, null=True)
#     fecha = models.DateTimeField(blank=True, null=True)
#     vencimiento = models.DateTimeField(blank=True, null=True)
#     embarque = models.IntegerField(blank=True, null=True)
#     vapor = models.CharField(max_length=30, blank=True, null=True)
#     # vapor = models.ForeignKey(Vapores, to_field='codigo', on_delete=models.PROTECT, db_column='vapor', blank=True,null=True, related_name='vapor')
#     awb = models.CharField(max_length=40, blank=True, null=True)
#     hawb = models.CharField(max_length=40, blank=True, null=True)
#     volumen = models.FloatField(blank=True, null=True)
#     tarifaventa = models.FloatField(blank=True, null=True)
#     tarifacompra = models.FloatField(blank=True, null=True)
#     pago = models.CharField(max_length=10, blank=True, null=True)
#     refcliente = models.CharField(max_length=1024, blank=True, null=True)
#     transportista = models.IntegerField(blank=True, null=True)
#     posicion = models.CharField(max_length=30, blank=True, null=True)
#     cotizacion = models.IntegerField(blank=True, null=True)
#     cotizacion1 = models.IntegerField(blank=True, null=True)
#     vaporcli2 = models.CharField(max_length=1, blank=True, null=True)
#     # moneda = models.SmallIntegerField(blank=True, null=True)
#     # arbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
#     # vendedor = models.SmallIntegerField(blank=True, null=True)
#     moneda = models.ForeignKey(Monedas, to_field='codigo', on_delete=models.PROTECT, db_column='moneda', blank=True,null=True, related_name='moneda')
#     arbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
#     vendedor = models.ForeignKey(Vendedores, to_field='codigo', on_delete=models.PROTECT, db_column='vendedor',blank=True, null=True, related_name='vendedor')
#     despachante = models.IntegerField(blank=True, null=True)
#     agecompras = models.IntegerField(blank=True, null=True)
#     ageventas = models.IntegerField(blank=True, null=True)
#     deposito = models.SmallIntegerField(blank=True, null=True)
#     recepcion = models.DateTimeField(blank=True, null=True)
#     iniciales = models.CharField(max_length=3, blank=True, null=True)
#     nrodespacho = models.CharField(max_length=20, blank=True, null=True)
#     aduana = models.CharField(max_length=20, blank=True, null=True)
#     fecacepta = models.DateTimeField(blank=True, null=True)
#     fecentrega = models.DateTimeField(blank=True, null=True)
#     fecretiro = models.DateTimeField(blank=True, null=True)
#     totalgiro = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
#     nroguiadesp = models.CharField(max_length=20, blank=True, null=True)
#     aplicable = models.FloatField(blank=True, null=True)
#     refproveedor = models.CharField(max_length=250, blank=True, null=True)
#     estimadorecepcion = models.DateTimeField(blank=True, null=True)
#     eta = models.DateTimeField(blank=True, null=True)
#     etd = models.DateTimeField(blank=True, null=True)
#     recepcionado = models.CharField(max_length=1, blank=True, null=True)
#     lugar = models.CharField(max_length=30, blank=True, null=True)
#     fecaduana = models.DateTimeField(db_column='Fecaduana', blank=True, null=True)  # Field name made lowercase.
#     fecdocage = models.DateTimeField(db_column='Fecdocage', blank=True, null=True)  # Field name made lowercase.
#     fecrecdoc = models.DateTimeField(blank=True, null=True)
#     fecemision = models.DateTimeField(blank=True, null=True)
#     fecseguro = models.DateTimeField(blank=True, null=True)
#     nroseguro = models.CharField(max_length=10, blank=True, null=True)
#     valor = models.CharField(max_length=20, blank=True, null=True)
#     manifiesto = models.CharField(max_length=20, blank=True, null=True)
#     ubicacion = models.CharField(max_length=20, blank=True, null=True)
#     fecpagoder = models.DateTimeField(blank=True, null=True)
#     tarifafija = models.CharField(max_length=1, blank=True, null=True)
#     tomopeso = models.SmallIntegerField(blank=True, null=True)
#     fecpresdi = models.DateTimeField(blank=True, null=True)
#     prima = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
#     centro = models.CharField(max_length=25, blank=True, null=True)
#     multimodal = models.CharField(max_length=1, blank=True, null=True)
#     transportelocal = models.IntegerField(blank=True, null=True)
#     estimadopup = models.DateTimeField(blank=True, null=True)
#     realpup = models.DateTimeField(blank=True, null=True)
#     estimadodelivery = models.DateTimeField(blank=True, null=True)
#     realdelivery = models.DateTimeField(blank=True, null=True)
#     referencialocal = models.CharField(max_length=50, blank=True, null=True)
#     modolocal = models.CharField(max_length=10, blank=True, null=True)
#     fecguiadesp = models.DateTimeField(blank=True, null=True)
#     tarifaprofit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
#     armador = models.IntegerField(blank=True, null=True)
#     notificar = models.IntegerField(db_column='Notificar', blank=True, null=True)  # Field name made lowercase.
#     fechaonhand = models.DateTimeField(db_column='FechaOnHand', blank=True, null=True)  # Field name made lowercase.
#     booking = models.CharField(max_length=30, blank=True, null=True)
#     propia = models.CharField(db_column='Propia', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     trafico = models.SmallIntegerField(db_column='Trafico', blank=True, null=True)  # Field name made lowercase.
#     proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
#     unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     modificado = models.CharField(db_column='Modificado', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     depcontenedoringreso = models.SmallIntegerField(db_column='DepContenedorIngreso', blank=True, null=True)  # Field name made lowercase.
#     depcontenedorvacios = models.SmallIntegerField(db_column='DepContenedorVacios', blank=True, null=True)  # Field name made lowercase.
#     loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)  # Field name made lowercase.
#     discharge = models.CharField(db_column='Discharge', max_length=5, blank=True, null=True)  # Field name made lowercase.
#     deadborrador = models.DateTimeField(db_column='DeadBorrador', blank=True, null=True)  # Field name made lowercase.
#     deaddocumentos = models.DateTimeField(db_column='DeadDocumentos', blank=True, null=True)  # Field name made lowercase.
#     deadentrega = models.DateTimeField(db_column='DeadEntrega', blank=True, null=True)  # Field name made lowercase.
#     deadliberacion = models.DateTimeField(db_column='DeadLiberacion', blank=True, null=True)  # Field name made lowercase.
#     retiravacio = models.DateTimeField(db_column='RetiraVacio', blank=True, null=True)  # Field name made lowercase.
#     retiralleno = models.DateTimeField(db_column='RetiraLleno', blank=True, null=True)  # Field name made lowercase.
#     arriboreal = models.DateTimeField(db_column='ArriboReal', blank=True, null=True)  # Field name made lowercase.
#     pagoenfirme = models.DateTimeField(db_column='PagoenFirme', blank=True, null=True)  # Field name made lowercase.
#     recepcionprealert = models.DateTimeFi506340eld(db_column='RecepcionPrealert', blank=True, null=True)  # Field name made lowercase.
#     bltipo = models.CharField(db_column='BLTipo', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     credito = models.CharField(db_column='Credito', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     revalidacion = models.DateTimeField(db_column='Revalidacion', blank=True, null=True)  # Field name made lowercase.
#     almacenajelibrehasta = models.DateTimeField(db_column='AlmacenajeLibreHasta', blank=True, null=True)  # Field name made lowercase.
#     demoraslibrehasta = models.DateTimeField(db_column='DemorasLibreHasta', blank=True, null=True)  # Field name made lowercase.
#     entregavacio = models.DateTimeField(db_column='EntregaVacio', blank=True, null=True)  # Field name made lowercase.
#     tipobonifcli = models.CharField(db_column='TipoBonifCli', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     bonifcli = models.FloatField(db_column='BonifCli', blank=True, null=True)  # Field name made lowercase.
#     originales = models.CharField(db_column='Originales', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
#     wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     consolidado = models.SmallIntegerField(db_column='Consolidado', blank=True, null=True)  # Field name made lowercase.
#     viaje = models.CharField(db_column='Viaje', max_length=20, blank=True, null=True)  # Field name made lowercase.
#     hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True, null=True)  # Field name made lowercase.
#     demora = models.SmallIntegerField(db_column='Demora', blank=True, null=True)  # Field name made lowercase.
#     valordemoravta = models.DecimalField(db_column='ValorDemoraVTA', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
#     valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
#     rotulosincorrectos = models.CharField(db_column='RotulosIncorrectos', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
#     entregadoa = models.CharField(db_column='EntregadoA', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     loadingdate = models.DateTimeField(db_column='LoadingDate', blank=True, null=True)  # Field name made lowercase.
#     diasalmacenaje = models.SmallIntegerField(db_column='DiasAlmacenaje', blank=True, null=True)  # Field name made lowercase.
#     muestroflete = models.DecimalField(db_column='MuestroFlete', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
#     operacion = models.CharField(db_column='Operacion', max_length=25, blank=True, null=True)  # Field name made lowercase.
#     enviointtrabk = models.CharField(db_column='EnvioInttraBK', max_length=10, blank=True, null=True)  # Field name made lowercase.
#     enviointtrasi = models.CharField(db_column='EnvioInttraSI', max_length=10, blank=True, null=True)  # Field name made lowercase.
#     maerskbk = models.CharField(db_column='MaerskBK', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     maersksi = models.CharField(db_column='MaerskSI', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     wwanumerobooking = models.IntegerField(db_column='WWANumeroBooking', blank=True, null=True)  # Field name made lowercase.
#     envioeasipassbk = models.CharField(db_column='EnvioEASIPASSBK', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     envioeasipasssi = models.CharField(db_column='EnvioEASIPASSSI', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     fechastacking = models.DateTimeField(db_column='FechaStacking', blank=True, null=True)  # Field name made lowercase.
#     horastacking = models.CharField(db_column='HoraStacking', max_length=30, blank=True, null=True)  # Field name made lowercase.
#     fechafinstacking = models.DateTimeField(db_column='FechaFinStacking', blank=True, null=True)  # Field name made lowercase.
#     horafinstacking = models.CharField(db_column='HoraFinStacking', max_length=30, blank=True, null=True)  # Field name made lowercase.
#     fechacutoff = models.DateTimeField(db_column='FechaCutOff', blank=True, null=True)  # Field name made lowercase.
#     horacutoff = models.CharField(db_column='HoraCutOff', max_length=30, blank=True, null=True)  # Field name made lowercase.
#     tieneseguro = models.CharField(db_column='TieneSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)  # Field name made lowercase.
#     contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)  # Field name made lowercase.
#     fechacutoffvgm = models.DateTimeField(db_column='FechaCutOffVGM', blank=True, null=True)  # Field name made lowercase.
#     horacutoffvgm = models.CharField(db_column='HoraCutOffVGM', max_length=30, blank=True, null=True)  # Field name made lowercase.
#     nroreferedi = models.IntegerField(db_column='NroReferEDI', blank=True, null=True)  # Field name made lowercase.
#     trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     deaddocumentoshora = models.CharField(db_column='DeadDocumentosHora', max_length=10, blank=True, null=True)  # Field name made lowercase.
#
# class Seguimiento(models.Model):
#     numero = models.IntegerField()
#     cliente = models.IntegerField(blank=True, null=True)
#     consignatario = models.ForeignKey(Clientes,to_field='codigo',on_delete=models.PROTECT,db_column='consignatario',blank=True,null=True,related_name='cli1')
#     origen = models.CharField(max_length=5, blank=True, null=True)
#     destino = models.CharField(max_length=5, blank=True, null=True)
#     terminos = models.CharField(max_length=3, blank=True, null=True)
#     observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
#     status = models.CharField(max_length=20, choices=(("Collect","Collect"),("Prepaid","Prepaid"),),blank=True, null=True)
#     agente = models.ForeignKey(Clientes,to_field='codigo',on_delete=models.PROTECT,db_column='agente',blank=True,null=True,related_name='cli8')
#     embarcador = models.ForeignKey(Clientes,to_field='codigo', db_column='Embarcador',on_delete=models.PROTECT,blank=True,null=True,related_name='cli2')  # Field name made lowercase.
#     vaporcli = models.CharField(db_column='Vaporcli', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     modo = models.CharField(max_length=20, blank=True, null=True)
#     fecha = models.DateTimeField(blank=True, null=True)
#     vencimiento = models.DateTimeField(blank=True, null=True)
#     embarque = models.IntegerField(blank=True, null=True)
#     vapor = models.CharField(max_length=30, blank=True, null=True)
#     # vapor = models.ForeignKey(Vapores,to_field='codigo',on_delete=models.PROTECT,db_column='vapor',blank=True,null=True,related_name='vapor')
#     awb = models.CharField(max_length=40, blank=True, null=True)
#     hawb = models.CharField(max_length=40, blank=True, null=True)
#     volumen = models.FloatField(blank=True, null=True)
#     tarifaventa = models.FloatField(blank=True, null=True)
#     tarifacompra = models.FloatField(blank=True, null=True)
#     pago = models.CharField(max_length=10, blank=True, null=True)
#     refcliente = models.CharField(max_length=1024, blank=True, null=True)
#     transportista = models.ForeignKey(Clientes,to_field='codigo',db_column='transportista',on_delete=models.PROTECT,blank=True,null=True,related_name='cli3')
#     posicion = models.CharField(max_length=30, blank=True, null=True)
#     cotizacion = models.IntegerField(blank=True, null=True)
#     cotizacion1 = models.IntegerField(blank=True, null=True)
#     vaporcli2 = models.CharField(max_length=1, blank=True, null=True)
#     # moneda = models.SmallIntegerField(blank=True, null=True)
#     moneda = models.ForeignKey(Monedas, to_field='codigo', on_delete=models.PROTECT, db_column='moneda', blank=True,null=True, related_name='moneda')
#     arbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
#     vendedor = models.ForeignKey(Vendedores,to_field='codigo',on_delete=models.PROTECT,db_column='vendedor',blank=True,null=True,related_name='vendedor')
#     # vendedor = models.SmallIntegerField(blank=True, null=True)
#     despachante = models.ForeignKey(Clientes,to_field='codigo',on_delete=models.PROTECT,db_column='despachante',blank=True,null=True,related_name='cli9')
#     agecompras = models.ForeignKey(Clientes,to_field='codigo',on_delete=models.PROTECT,db_column='agecompras',blank=True,null=True,related_name='cli7')
#     ageventas = models.ForeignKey(Clientes,to_field='codigo',on_delete=models.PROTECT,db_column='ageventas',blank=True,null=True,related_name='cli6')
#     deposito = models.ForeignKey(Depositos,to_field='codigo',on_delete=models.PROTECT,db_column='deposito',blank=True,null=True,related_name='deposito')
#     recepcion = models.DateTimeField(blank=True, null=True)
#     iniciales = models.CharField(max_length=3, blank=True, null=True)
#     nrodespacho = models.CharField(max_length=20, blank=True, null=True)
#     aduana = models.CharField(max_length=20, blank=True, null=True)
#     fecacepta = models.DateTimeField(blank=True, null=True)
#     fecentrega = models.DateTimeField(blank=True, null=True)
#     fecretiro = models.DateTimeField(blank=True, null=True)
#     totalgiro = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
#     nroguiadesp = models.CharField(max_length=20, blank=True, null=True)
#     aplicable = models.FloatField(blank=True, null=True)
#     refproveedor = models.CharField(max_length=250, blank=True, null=True)
#     estimadorecepcion = models.DateField(blank=True, null=True)
#     eta = models.DateTimeField(blank=True, null=True)
#     etd = models.DateTimeField(blank=True, null=True)
#     recepcionado = models.CharField(max_length=1, blank=True, null=True)
#     lugar = models.CharField(max_length=30, blank=True, null=True)
#     fecaduana = models.DateTimeField(db_column='Fecaduana', blank=True, null=True)  # Field name made lowercase.
#     fecdocage = models.DateTimeField(db_column='Fecdocage', blank=True, null=True)  # Field name made lowercase.
#     fecrecdoc = models.DateTimeField(blank=True, null=True)
#     fecemision = models.DateTimeField(blank=True, null=True)
#     fecseguro = models.DateTimeField(blank=True, null=True)
#     nroseguro = models.CharField(max_length=10, blank=True, null=True)
#     valor = models.CharField(max_length=20, blank=True, null=True)
#     manifiesto = models.CharField(max_length=20, blank=True, null=True)
#     ubicacion = models.CharField(max_length=20, blank=True, null=True)
#     fecpagoder = models.DateTimeField(blank=True, null=True)
#     tarifafija = models.CharField(max_length=1, blank=True, null=True)
#     tomopeso = models.SmallIntegerField(blank=True, null=True)
#     fecpresdi = models.DateTimeField(blank=True, null=True)
#     prima = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
#     centro = models.CharField(max_length=25, blank=True, null=True)
#     multimodal = models.CharField(max_length=1, blank=True, null=True)
#     transportelocal = models.IntegerField(blank=True, null=True)
#     estimadopup = models.DateTimeField(blank=True, null=True)
#     realpup = models.DateTimeField(blank=True, null=True)
#     estimadodelivery = models.DateTimeField(blank=True, null=True)
#     realdelivery = models.DateTimeField(blank=True, null=True)
#     referencialocal = models.CharField(max_length=50, blank=True, null=True)
#     modolocal = models.CharField(max_length=10, blank=True, null=True)
#     fecguiadesp = models.DateTimeField(blank=True, null=True)
#     tarifaprofit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
#     # armador = models.ForeignKey(Clientes,to_field='codigo',db_column='armador',on_delete=models.PROTECT,blank=True,null=True,related_name='cli4')
#     armador = models.SmallIntegerField(blank=True, null=True)
#     # notificar = models.ForeignKey(Clientes,to_field='codigo',db_column='notificar',on_delete=models.PROTECT,blank=True,null=True,related_name='cli5') # Field name made lowercase.
#     fechaonhand = models.DateTimeField(db_column='FechaOnHand', blank=True, null=True)  # Field name made lowercase.
#     booking = models.CharField(max_length=30, blank=True, null=True)
#     propia = models.CharField(db_column='Propia', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     trafico = models.SmallIntegerField(db_column='Trafico', blank=True, null=True)  # Field name made lowercase.
#     proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
#     unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
#                                   null=True)  # Field name made lowercase.
#     unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
#                                      null=True)  # Field name made lowercase.
#     modificado = models.CharField(db_column='Modificado', max_length=1, blank=True,
#                                   null=True)  # Field name made lowercase.
#     depcontenedoringreso = models.SmallIntegerField(db_column='DepContenedorIngreso', blank=True,
#                                                     null=True)  # Field name made lowercase.
#     depcontenedorvacios = models.SmallIntegerField(db_column='DepContenedorVacios', blank=True,
#                                                    null=True)  # Field name made lowercase.
#     loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)  # Field name made lowercase.
#     discharge = models.CharField(db_column='Discharge', max_length=5, blank=True,
#                                  null=True)  # Field name made lowercase.
#     deadborrador = models.DateTimeField(db_column='DeadBorrador', blank=True, null=True)  # Field name made lowercase.
#     deaddocumentos = models.DateTimeField(db_column='DeadDocumentos', blank=True,
#                                           null=True)  # Field name made lowercase.
#     deadentrega = models.DateTimeField(db_column='DeadEntrega', blank=True, null=True)  # Field name made lowercase.
#     deadliberacion = models.DateTimeField(db_column='DeadLiberacion', blank=True,
#                                           null=True)  # Field name made lowercase.
#     retiravacio = models.DateTimeField(db_column='RetiraVacio', blank=True, null=True)  # Field name made lowercase.
#     retiralleno = models.DateTimeField(db_column='RetiraLleno', blank=True, null=True)  # Field name made lowercase.
#     arriboreal = models.DateTimeField(db_column='ArriboReal', blank=True, null=True)  # Field name made lowercase.
#     pagoenfirme = models.DateTimeField(db_column='PagoenFirme', blank=True, null=True)  # Field name made lowercase.
#     recepcionprealert = models.DateTimeField(db_column='RecepcionPrealert', blank=True,
#                                              null=True)  # Field name made lowercase.
#     bltipo = models.CharField(db_column='BLTipo', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     credito = models.CharField(db_column='Credito', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     revalidacion = models.DateTimeField(db_column='Revalidacion', blank=True, null=True)  # Field name made lowercase.
#     almacenajelibrehasta = models.DateTimeField(db_column='AlmacenajeLibreHasta', blank=True,
#                                                 null=True)  # Field name made lowercase.
#     demoraslibrehasta = models.DateTimeField(db_column='DemorasLibreHasta', blank=True,
#                                              null=True)  # Field name made lowercase.
#     entregavacio = models.DateTimeField(db_column='EntregaVacio', blank=True, null=True)  # Field name made lowercase.
#     tipobonifcli = models.CharField(db_column='TipoBonifCli', max_length=1, blank=True,
#                                     null=True)  # Field name made lowercase.
#     bonifcli = models.FloatField(db_column='BonifCli', blank=True, null=True)  # Field name made lowercase.
#     originales = models.CharField(db_column='Originales', max_length=1, blank=True,null=True,choices=(("S","S"),("N","N"),),default='N')  # Field name made lowercase.
#     editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
#     wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True,
#                                 null=True)  # Field name made lowercase.
#     consolidado = models.SmallIntegerField(db_column='Consolidado', blank=True, null=True)  # Field name made lowercase.
#     viaje = models.CharField(db_column='Viaje', max_length=20, blank=True, null=True)  # Field name made lowercase.
#     hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
#                                 null=True)  # Field name made lowercase.
#     demora = models.SmallIntegerField(db_column='Demora', blank=True, null=True)  # Field name made lowercase.
#     valordemoravta = models.DecimalField(db_column='ValorDemoraVTA', max_digits=19, decimal_places=4, blank=True,
#                                          null=True)  # Field name made lowercase.
#     valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=19, decimal_places=4, blank=True,
#                                          null=True)  # Field name made lowercase.
#     rotulosincorrectos = models.CharField(db_column='RotulosIncorrectos', max_length=1, blank=True,
#                                           null=True)  # Field name made lowercase.
#     actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
#     entregadoa = models.CharField(db_column='EntregadoA', max_length=50, blank=True,
#                                   null=True)  # Field name made lowercase.
#     loadingdate = models.DateTimeField(db_column='LoadingDate', blank=True, null=True)  # Field name made lowercase.
#     diasalmacenaje = models.SmallIntegerField(db_column='DiasAlmacenaje', blank=True,
#                                               null=True)  # Field name made lowercase.
#     muestroflete = models.DecimalField(db_column='MuestroFlete', max_digits=19, decimal_places=4, blank=True,
#                                        null=True)  # Field name made lowercase.
#     operacion = models.CharField(db_column='Operacion', max_length=25, blank=True,
#                                  null=True)  # Field name made lowercase.
#     enviointtrabk = models.CharField(db_column='EnvioInttraBK', max_length=10, blank=True,
#                                      null=True)  # Field name made lowercase.
#     enviointtrasi = models.CharField(db_column='EnvioInttraSI', max_length=10, blank=True,
#                                      null=True)  # Field name made lowercase.
#     maerskbk = models.CharField(db_column='MaerskBK', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     maersksi = models.CharField(db_column='MaerskSI', max_length=1, blank=True, null=True)  # Field name made lowercase.
#     wwanumerobooking = models.IntegerField(db_column='WWANumeroBooking', blank=True,
#                                            null=True)  # Field name made lowercase.
#     envioeasipassbk = models.CharField(db_column='EnvioEASIPASSBK', max_length=1, blank=True,
#                                        null=True)  # Field name made lowercase.
#     envioeasipasssi = models.CharField(db_column='EnvioEASIPASSSI', max_length=1, blank=True,
#                                        null=True)  # Field name made lowercase.
#     fechastacking = models.DateTimeField(db_column='FechaStacking', blank=True, null=True)  # Field name made lowercase.
#     horastacking = models.CharField(db_column='HoraStacking', max_length=30, blank=True,
#                                     null=True)  # Field name made lowercase.
#     fechafinstacking = models.DateTimeField(db_column='FechaFinStacking', blank=True,
#                                             null=True)  # Field name made lowercase.
#     horafinstacking = models.CharField(db_column='HoraFinStacking', max_length=30, blank=True,
#                                        null=True)  # Field name made lowercase.
#     fechacutoff = models.DateTimeField(db_column='FechaCutOff', blank=True, null=True)  # Field name made lowercase.
#     horacutoff = models.CharField(db_column='HoraCutOff', max_length=30, blank=True,
#                                   null=True)  # Field name made lowercase.
#     tieneseguro = models.CharField(db_column='TieneSeguro', max_length=1, blank=True,
#                                    null=True)  # Field name made lowercase.
#     contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
#                                    null=True)  # Field name made lowercase.
#     contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
#                                    null=True)  # Field name made lowercase.
#     fechacutoffvgm = models.DateTimeField(db_column='FechaCutOffVGM', blank=True,
#                                           null=True)  # Field name made lowercase.
#     horacutoffvgm = models.CharField(db_column='HoraCutOffVGM', max_length=30, blank=True,
#                                      null=True)  # Field name made lowercase.
#     nroreferedi = models.IntegerField(db_column='NroReferEDI', blank=True, null=True)  # Field name made lowercase.
#     trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     deaddocumentoshora = models.CharField(db_column='DeadDocumentosHora', max_length=10, blank=True,
#                                           null=True)  # Field name made lowercase.

class Seguimiento(models.Model):
    numero = models.IntegerField()
    cliente = models.IntegerField(blank=True, null=True)
    consignatario = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.CharField(max_length=20, choices=(
    ("ARRIBADO", "ARRIBADO"), ("CONFIRMADO", "CONFIRMADO"), ("CANCELADO", "CANCELADO"), ("RESERVADO", "RESERVADO"),
    ("UNIFICADO", "UNIFICADO"), ("CERRADO", "CERRADO"),), blank=True, null=True)
    agente = models.IntegerField(blank=True, null=True)
    embarcador = models.IntegerField(blank=True, null=True)
    vaporcli = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=20)
    fecha = models.DateTimeField(blank=True, null=True)
    vencimiento = models.DateTimeField(blank=True, null=True)
    embarque = models.IntegerField(blank=True, null=True)
    vapor = models.CharField(max_length=30, blank=True, null=True)
    # vapor = models.ForeignKey(Vapores,to_field='codigo',on_delete=models.PROTECT,db_column='vapor',blank=True,null=True,related_name='vapor')
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=40, blank=True, null=True)
    volumen = models.FloatField(blank=True, null=True)
    tarifaventa = models.FloatField(blank=True, null=True)
    tarifacompra = models.FloatField(blank=True, null=True)
    pago = models.CharField(max_length=10, blank=True, null=True,
                            choices=(("Collect", "Collect"), ("Prepaid", "Prepaid")))
    refcliente = models.CharField(max_length=1024, blank=True, null=True)
    transportista = models.IntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=30, blank=True, null=True)
    cotizacion = models.IntegerField(blank=True, null=True)
    cotizacion1 = models.IntegerField(blank=True, null=True)
    vaporcli2 = models.CharField(max_length=1, blank=True, null=True)
    # moneda = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    vendedor = models.IntegerField(blank=True, null=True)
    # vendedor = models.SmallIntegerField(blank=True, null=True)
    despachante = models.IntegerField(blank=True, null=True)
    agecompras = models.IntegerField(blank=True, null=True)
    ageventas = models.IntegerField(blank=True, null=True)
    deposito = models.IntegerField(blank=True, null=True)
    recepcion = models.DateTimeField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    nrodespacho = models.CharField(max_length=20, blank=True, null=True)
    aduana = models.CharField(max_length=20, blank=True, null=True)
    fecacepta = models.DateTimeField(blank=True, null=True)
    fecentrega = models.DateTimeField(blank=True, null=True)
    fecretiro = models.DateTimeField(blank=True, null=True)
    totalgiro = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    nroguiadesp = models.CharField(max_length=20, blank=True, null=True)
    aplicable = models.FloatField(blank=True, null=True)
    refproveedor = models.CharField(max_length=250, blank=True, null=True)
    estimadorecepcion = models.DateField(blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)
    etd = models.DateTimeField(blank=True, null=True)
    recepcionado = models.CharField(max_length=1, blank=True, null=True)
    lugar = models.CharField(max_length=30, blank=True, null=True)
    fecaduana = models.DateTimeField(db_column='Fecaduana', blank=True, null=True)  # Field name made lowercase.
    fecdocage = models.DateTimeField(db_column='Fecdocage', blank=True, null=True)  # Field name made lowercase.
    fecrecdoc = models.DateTimeField(blank=True, null=True)
    fecemision = models.DateTimeField(blank=True, null=True)
    fecseguro = models.DateTimeField(blank=True, null=True)
    nroseguro = models.CharField(max_length=10, blank=True, null=True)
    valor = models.CharField(max_length=20, blank=True, null=True)
    manifiesto = models.CharField(max_length=20, blank=True, null=True)
    ubicacion = models.CharField(max_length=20, blank=True, null=True)
    fecpagoder = models.DateTimeField(blank=True, null=True)
    tarifafija = models.CharField(max_length=1, blank=True, null=True)
    tomopeso = models.SmallIntegerField(blank=True, null=True)
    fecpresdi = models.DateTimeField(blank=True, null=True)
    prima = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    centro = models.CharField(max_length=25, blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    transportelocal = models.IntegerField(blank=True, null=True)
    estimadopup = models.DateTimeField(blank=True, null=True)
    realpup = models.DateTimeField(blank=True, null=True)
    estimadodelivery = models.DateTimeField(blank=True, null=True)
    realdelivery = models.DateTimeField(blank=True, null=True)
    referencialocal = models.CharField(max_length=50, blank=True, null=True)
    modolocal = models.CharField(max_length=10, blank=True, null=True)
    fecguiadesp = models.DateTimeField(blank=True, null=True)
    tarifaprofit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    # armador = models.ForeignKey(Clientes,to_field='codigo',db_column='armador',on_delete=models.PROTECT,blank=True,null=True,related_name='cli4')
    armador = models.SmallIntegerField(blank=True, null=True)
    # notificar = models.ForeignKey(Clientes,to_field='codigo',db_column='notificar',on_delete=models.PROTECT,blank=True,null=True,related_name='cli5') # Field name made lowercase.
    notificar = models.IntegerField(blank=True, null=True)

    fechaonhand = models.DateTimeField(db_column='FechaOnHand', blank=True, null=True)  # Field name made lowercase.
    booking = models.CharField(max_length=30, blank=True, null=True)
    propia = models.CharField(db_column='Propia', max_length=1, blank=True, null=True)  # Field name made lowercase.
    trafico = models.SmallIntegerField(db_column='Trafico', blank=True, null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    modificado = models.CharField(db_column='Modificado', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    depcontenedoringreso = models.SmallIntegerField(db_column='DepContenedorIngreso', blank=True,
                                                    null=True)  # Field name made lowercase.
    depcontenedorvacios = models.SmallIntegerField(db_column='DepContenedorVacios', blank=True,
                                                   null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    deadborrador = models.DateTimeField(db_column='DeadBorrador', blank=True, null=True)  # Field name made lowercase.
    deaddocumentos = models.DateTimeField(db_column='DeadDocumentos', blank=True,
                                          null=True)  # Field name made lowercase.
    deadentrega = models.DateTimeField(db_column='DeadEntrega', blank=True, null=True)  # Field name made lowercase.
    deadliberacion = models.DateTimeField(db_column='DeadLiberacion', blank=True,
                                          null=True)  # Field name made lowercase.
    retiravacio = models.DateTimeField(db_column='RetiraVacio', blank=True, null=True)  # Field name made lowercase.
    retiralleno = models.DateTimeField(db_column='RetiraLleno', blank=True, null=True)  # Field name made lowercase.
    arriboreal = models.DateTimeField(db_column='ArriboReal', blank=True, null=True)  # Field name made lowercase.
    pagoenfirme = models.DateTimeField(db_column='PagoenFirme', blank=True, null=True)  # Field name made lowercase.
    recepcionprealert = models.DateTimeField(db_column='RecepcionPrealert', blank=True,
                                             null=True)  # Field name made lowercase.
    bltipo = models.CharField(db_column='BLTipo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    credito = models.CharField(db_column='Credito', max_length=50, blank=True, null=True)  # Field name made lowercase.
    revalidacion = models.DateTimeField(db_column='Revalidacion', blank=True, null=True)  # Field name made lowercase.
    almacenajelibrehasta = models.DateTimeField(db_column='AlmacenajeLibreHasta', blank=True,
                                                null=True)  # Field name made lowercase.
    demoraslibrehasta = models.DateTimeField(db_column='DemorasLibreHasta', blank=True,
                                             null=True)  # Field name made lowercase.
    entregavacio = models.DateTimeField(db_column='EntregaVacio', blank=True, null=True)  # Field name made lowercase.
    tipobonifcli = models.CharField(db_column='TipoBonifCli', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    bonifcli = models.FloatField(db_column='BonifCli', blank=True, null=True)  # Field name made lowercase.
    originales = models.CharField(db_column='Originales', max_length=1, blank=True, null=True,
                                  choices=(("S", "S"), ("N", "N"),), default='N')  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    consolidado = models.SmallIntegerField(db_column='Consolidado', blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    demora = models.SmallIntegerField(db_column='Demora', blank=True, null=True)  # Field name made lowercase.
    valordemoravta = models.DecimalField(db_column='ValorDemoraVTA', max_digits=19, decimal_places=4, blank=True,
                                         null=True)  # Field name made lowercase.
    valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=19, decimal_places=4, blank=True,
                                         null=True)  # Field name made lowercase.
    rotulosincorrectos = models.CharField(db_column='RotulosIncorrectos', max_length=1, blank=True,
                                          null=True)  # Field name made lowercase.
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    entregadoa = models.CharField(db_column='EntregadoA', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    loadingdate = models.DateTimeField(db_column='LoadingDate', blank=True, null=True)  # Field name made lowercase.
    diasalmacenaje = models.SmallIntegerField(db_column='DiasAlmacenaje', blank=True,
                                              null=True)  # Field name made lowercase.
    muestroflete = models.DecimalField(db_column='MuestroFlete', max_digits=19, decimal_places=4, blank=True,
                                       null=True)  # Field name made lowercase.
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
    operacion = models.CharField(db_column='Operacion', max_length=30, choices=choice_op, blank=True, null=True)
    enviointtrabk = models.CharField(db_column='EnvioInttraBK', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    enviointtrasi = models.CharField(db_column='EnvioInttraSI', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    maerskbk = models.CharField(db_column='MaerskBK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    maersksi = models.CharField(db_column='MaerskSI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wwanumerobooking = models.IntegerField(db_column='WWANumeroBooking', blank=True,
                                           null=True)  # Field name made lowercase.
    envioeasipassbk = models.CharField(db_column='EnvioEASIPASSBK', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    envioeasipasssi = models.CharField(db_column='EnvioEASIPASSSI', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    fechastacking = models.DateTimeField(db_column='FechaStacking', blank=True, null=True)  # Field name made lowercase.
    horastacking = models.CharField(db_column='HoraStacking', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    fechafinstacking = models.DateTimeField(db_column='FechaFinStacking', blank=True,
                                            null=True)  # Field name made lowercase.
    horafinstacking = models.CharField(db_column='HoraFinStacking', max_length=30, blank=True,
                                       null=True)  # Field name made lowercase.
    fechacutoff = models.DateTimeField(db_column='FechaCutOff', blank=True, null=True)  # Field name made lowercase.
    horacutoff = models.CharField(db_column='HoraCutOff', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    tieneseguro = models.CharField(db_column='TieneSeguro', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    fechacutoffvgm = models.DateTimeField(db_column='FechaCutOffVGM', blank=True,
                                          null=True)  # Field name made lowercase.
    horacutoffvgm = models.CharField(db_column='HoraCutOffVGM', max_length=30, blank=True,
                                     null=True)  # Field name made lowercase.
    nroreferedi = models.IntegerField(db_column='NroReferEDI', blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    deaddocumentoshora = models.CharField(db_column='DeadDocumentosHora', max_length=10, blank=True,
                                          null=True)  # Field name made lowercase.

    def __str__(self, ):
        return self.modo + ' - ' + str(self.numero)


class Servireserva(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notomaprofit = models.BooleanField()
    repartir = models.CharField(max_length=1, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.


class Traceop(models.Model):
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=250, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.


class Conexaerea(models.Model):
    choice_accion = (
        ("DELIVERY", "DELIVERY"),
        ("DISCHARGE", "DISCHARGE"),
        ("RECEIPT", "RECEIPT"),
        ("TRANSIT", "TRANSIT"),
    )
    choice_modo = (
        ("MARITIMO", "MARITIMO"),
        ("FLUVIAL", "FLUVIAL"),
        ("TERRESTRE", "TERRESTRE"),
        ("AEREO", "AEREO"),
    )
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    salida = models.DateField(blank=True, null=True)
    llegada = models.DateField(blank=True, null=True)
    cia = models.CharField(max_length=50, blank=True, null=True)
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(max_length=15, choices=choice_modo)
    accion = models.CharField(db_column='Accion', max_length=15, choices=choice_accion, blank=True,
                              null=True)  # Field name made lowercase.

    def _get_seguimiento(self, ):
        try:
            return Seguimiento.objects.get(numero=self.numero)
        except:
            return None

    seguimiento = property(_get_seguimiento)


class Serviceaereo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True, choices=(("P", "Prepaid"), ("C", "Collect")))
    servicio = models.SmallIntegerField()
    moneda = models.SmallIntegerField()
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True, choices=(("S", "SI"), ("N", "NO"),))
    notomaprofit = models.BooleanField()
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.


class VGrillaServiceaereo(models.Model):
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
        db_table = 'VGrillaServiceaereo'


class PreferenciasReporteOp(models.Model):
    opciones = models.TextField(verbose_name="Opciones")
    usuario = models.ForeignKey(
        User,
        db_column='usuario',
        on_delete=models.CASCADE,
        verbose_name="Usuario"
    )

    class Meta:
        db_table = 'preferencias_reporte_op'


from inspect import getmembers
from auditlog.registry import auditlog
from seguimientos import models

tablas = getmembers(models)
for t in tablas:
    try:
        auditlog.register(t[1], serialize_data=True)
    except Exception as e:
        pass


