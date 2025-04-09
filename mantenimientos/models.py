from inspect import getmembers
from django.db import models


class Actividades(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name_plural = "Actividades"


class Attachsocio(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    archivo = models.CharField(db_column='Archivo', max_length=250, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=50, blank=True, null=True)  # Field name made lowercase.
    web = models.CharField(db_column='Web', max_length=1, blank=True, null=True)  # Field name made lowercase.


class Bancos(models.Model):
    codigo = models.SmallIntegerField(db_column='Codigo', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True,null=True)  # Field name made lowercase.
    edi = models.CharField(db_column='EDI', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nombrechino = models.CharField(db_column='NombreChino', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    rut = models.CharField(db_column='RUT', max_length=30, blank=True, null=True)  # Field name made lowercase.


    def __str__(self):
        return self.nombre


class Bandejaefreight(models.Model):
    de = models.CharField(db_column='De', max_length=100, blank=True, null=True)  # Field name made lowercase.
    asunto = models.CharField(db_column='Asunto', max_length=300, blank=True, null=True)  # Field name made lowercase.
    mensaje = models.TextField(db_column='Mensaje', blank=True,
                               null=True)  # Field name made lowercase. This field type is a guess.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    fechaprocesado = models.DateTimeField(db_column='FechaProcesado', blank=True,
                                          null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True,
                             null=True)  # Field name made lowercase. This field type is a guess.


class Budget(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    ano = models.SmallIntegerField(db_column='Ano', blank=True, null=True)  # Field name made lowercase.
    ventat1 = models.DecimalField(db_column='VentaT1', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    ventat2 = models.DecimalField(db_column='VentaT2', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    ventat3 = models.DecimalField(db_column='VentaT3', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    ventat4 = models.DecimalField(db_column='VentaT4', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    pesoeat1 = models.FloatField(db_column='PesoEAT1', blank=True, null=True)  # Field name made lowercase.
    pesoeat2 = models.FloatField(db_column='PesoEAT2', blank=True, null=True)  # Field name made lowercase.
    pesoeat3 = models.FloatField(db_column='PesoEAT3', blank=True, null=True)  # Field name made lowercase.
    pesoeat4 = models.FloatField(db_column='PesoEAT4', blank=True, null=True)  # Field name made lowercase.
    pesoiat1 = models.FloatField(db_column='PesoIAT1', blank=True, null=True)  # Field name made lowercase.
    pesoiat2 = models.FloatField(db_column='PesoIAT2', blank=True, null=True)  # Field name made lowercase.
    pesoiat3 = models.FloatField(db_column='PesoIAT3', blank=True, null=True)  # Field name made lowercase.
    pesoiat4 = models.FloatField(db_column='PesoIAT4', blank=True, null=True)  # Field name made lowercase.
    teusemt1 = models.IntegerField(db_column='TeusEMT1', blank=True, null=True)  # Field name made lowercase.
    teusemt2 = models.IntegerField(db_column='TeusEMT2', blank=True, null=True)  # Field name made lowercase.
    teusemt3 = models.IntegerField(db_column='TeusEMT3', blank=True, null=True)  # Field name made lowercase.
    teusemt4 = models.IntegerField(db_column='TeusEMT4', blank=True, null=True)  # Field name made lowercase.
    teusimt1 = models.IntegerField(db_column='TeusIMT1', blank=True, null=True)  # Field name made lowercase.
    teusimt2 = models.IntegerField(db_column='TeusIMT2', blank=True, null=True)  # Field name made lowercase.
    teusimt3 = models.IntegerField(db_column='TeusIMT3', blank=True, null=True)  # Field name made lowercase.
    teusimt4 = models.IntegerField(db_column='TeusIMT4', blank=True, null=True)  # Field name made lowercase.
    lclemt1 = models.FloatField(db_column='LclEMT1', blank=True, null=True)  # Field name made lowercase.
    lclemt2 = models.FloatField(db_column='LclEMT2', blank=True, null=True)  # Field name made lowercase.
    lclemt3 = models.FloatField(db_column='LclEMT3', blank=True, null=True)  # Field name made lowercase.
    lclemt4 = models.FloatField(db_column='LclEMT4', blank=True, null=True)  # Field name made lowercase.
    lclimt1 = models.FloatField(db_column='LclIMT1', blank=True, null=True)  # Field name made lowercase.
    lclimt2 = models.FloatField(db_column='LclIMT2', blank=True, null=True)  # Field name made lowercase.
    lclimt3 = models.FloatField(db_column='LclIMT3', blank=True, null=True)  # Field name made lowercase.
    lclimt4 = models.FloatField(db_column='LclIMT4', blank=True, null=True)  # Field name made lowercase.
    pesoett1 = models.FloatField(db_column='PesoETT1', blank=True, null=True)  # Field name made lowercase.
    pesoett2 = models.FloatField(db_column='PesoETT2', blank=True, null=True)  # Field name made lowercase.
    pesoett3 = models.FloatField(db_column='PesoETT3', blank=True, null=True)  # Field name made lowercase.
    pesoett4 = models.FloatField(db_column='PesoETT4', blank=True, null=True)  # Field name made lowercase.
    pesoitt1 = models.FloatField(db_column='PesoITT1', blank=True, null=True)  # Field name made lowercase.
    pesoitt2 = models.FloatField(db_column='PesoITT2', blank=True, null=True)  # Field name made lowercase.
    pesoitt3 = models.FloatField(db_column='PesoITT3', blank=True, null=True)  # Field name made lowercase.
    pesoitt4 = models.FloatField(db_column='PesoITT4', blank=True, null=True)  # Field name made lowercase.


class Claveposicionmm(models.Model):
    posicion = models.CharField(db_column='Posicion', max_length=15)  # Field name made lowercase.
    numeroorden = models.SmallIntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.


class Clicontactos(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cargo = models.CharField(db_column='Cargo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    celular = models.CharField(db_column='Celular', max_length=50, blank=True, null=True)  # Field name made lowercase.
    skype = models.CharField(db_column='Skype', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.


class Clifaxes(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True,
                             null=True)  # Field name made lowercase. This field type is a guess.
    asunto = models.TextField(db_column='Asunto', blank=True,
                              null=True)  # Field name made lowercase. This field type is a guess.
    tipo = models.CharField(db_column='Tipo', max_length=2, blank=True, null=True)  # Field name made lowercase.


class Clireldep(models.Model):
    idcli = models.IntegerField(db_column='IDCli', blank=True, null=True)  # Field name made lowercase.
    idrep = models.IntegerField(db_column='IDRep', blank=True, null=True)  # Field name made lowercase.


class Clirelacion(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    relacionado = models.IntegerField(db_column='Relacionado', blank=True, null=True)  # Field name made lowercase.


class Clitipodocumento(models.Model):
    numero = models.CharField(db_column='Numero', max_length=10, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True,
                                   null=True)  # Field name made lowercase.


class Clitipooperacion(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    tipooperacion = models.SmallIntegerField(db_column='TipoOperacion', blank=True,
                                             null=True)  # Field name made lowercase.


class Clitraficos(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    trafico = models.SmallIntegerField(db_column='Trafico', blank=True, null=True)  # Field name made lowercase.


class Config(models.Model):
    dato = models.SmallIntegerField(blank=True, null=True)
    dato2 = models.SmallIntegerField(blank=True, null=True)
    detalle = models.CharField(max_length=30, blank=True, null=True)


class Contratoscli(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    numcontrato = models.CharField(db_column='NumContrato', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=5, blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.


class Depositos(models.Model):
    codigo = models.SmallIntegerField(unique=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=30, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    cpostal = models.CharField(max_length=10, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    contactos = models.TextField(blank=True, null=True)  # This field type is a guess.
    ruc = models.CharField(max_length=20, blank=True, null=True)
    aduana = models.CharField(db_column='Aduana', max_length=20, blank=True, null=True)  # Field name made lowercase.
    empresachino = models.CharField(db_column='EmpresaChino', max_length=100, blank=True,
                                    null=True)  # Field name made lowercase.
    direccionchino = models.CharField(db_column='DireccionChino', max_length=100, blank=True,
                                      null=True)  # Field name made lowercase.

    class Meta:
        verbose_name_plural = "Depositos"


class Direccionentregas(models.Model):
    codigo = models.IntegerField(blank=True, null=True)
    iddireccion = models.SmallIntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=50, blank=True, null=True)
    cpostal = models.CharField(max_length=30, blank=True, null=True)
    pais = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    telefono2 = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    fax2 = models.CharField(max_length=30, blank=True, null=True)
    contacto = models.CharField(db_column='Contacto', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    centrocosto = models.CharField(db_column='CentroCosto', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=1, blank=True, null=True)  # Field name made lowercase.


class Empresa(models.Model):
    dnombre = models.CharField(max_length=50)
    drazonsocial = models.CharField(max_length=50, blank=True, null=True)
    ddireccion = models.CharField(max_length=50, blank=True, null=True)
    dtelefono = models.CharField(max_length=30, blank=True, null=True)
    dlocalidad = models.CharField(max_length=30, blank=True, null=True)
    dfax = models.CharField(max_length=30, blank=True, null=True)
    druc = models.CharField(max_length=20, blank=True, null=True)
    dcpostal = models.CharField(max_length=20, blank=True, null=True)
    dvtodgi = models.DateTimeField(blank=True, null=True)
    dvtobps = models.DateTimeField(blank=True, null=True)
    dvtobse = models.DateTimeField(blank=True, null=True)
    dnroiata = models.CharField(max_length=20, blank=True, null=True)
    dciudadbase = models.CharField(max_length=5, blank=True, null=True)
    dnomciudadbase = models.CharField(max_length=20, blank=True, null=True)
    usastock = models.BooleanField(blank=True, null=True)
    usaposicion = models.BooleanField(blank=True, null=True)
    cass = models.CharField(max_length=15, blank=True, null=True)
    pasagastos = models.BooleanField(blank=True, null=True)
    vaciudad = models.BooleanField(blank=True, null=True)
    nroata = models.CharField(max_length=15, blank=True, null=True)
    prefijohouse = models.CharField(max_length=5, blank=True, null=True)
    heredaposhijo = models.BooleanField(blank=True, null=True)
    usacontrolhawb = models.BooleanField(db_column='usacontrolHAWB', blank=True,
                                         null=True)  # Field name made lowercase.
    servidores = models.CharField(max_length=1, blank=True, null=True)
    graboimagen = models.BooleanField(blank=True, null=True)
    unidadpeso = models.CharField(max_length=1, blank=True, null=True)
    multiplestarifas = models.CharField(max_length=1, blank=True, null=True)
    verarbitrajes = models.CharField(db_column='Verarbitrajes', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    correo = models.CharField(max_length=1, blank=True, null=True)
    ultragestion = models.CharField(max_length=1, blank=True, null=True)
    formatofecha = models.CharField(max_length=10, blank=True, null=True)
    sucursalenposicion = models.CharField(db_column='SucursalEnPosicion', max_length=1, blank=True,
                                          null=True)  # Field name made lowercase.
    bloqueoarbitraje = models.CharField(db_column='BloqueoArbitraje', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    costosengastos = models.CharField(db_column='CostosEnGastos', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    iata = models.CharField(db_column='Iata', max_length=1, blank=True, null=True)  # Field name made lowercase.
    onlineorders = models.CharField(db_column='OnlineOrders', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    determinounidades = models.CharField(db_column='DeterminoUnidades', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.
    confirmaritemsembarcar = models.CharField(db_column='ConfirmarItemsEmbarcar', max_length=1, blank=True,
                                              null=True)  # Field name made lowercase.
    aesactivo = models.CharField(db_column='AESActivo', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    brokernumber = models.CharField(db_column='BrokerNumber', max_length=3, blank=True,
                                    null=True)  # Field name made lowercase.
    transmitterid = models.CharField(db_column='TransmitterID', max_length=9, blank=True,
                                     null=True)  # Field name made lowercase.
    transmitteridtype = models.CharField(db_column='TransmitterIDType', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.
    aes_option = models.IntegerField(db_column='AES_Option', blank=True, null=True)  # Field name made lowercase.
    datacenterportcode = models.CharField(db_column='DataCenterPortCode', max_length=4, blank=True,
                                          null=True)  # Field name made lowercase.
    sixdigitpassword = models.CharField(db_column='SixDigitPassword', max_length=6, blank=True,
                                        null=True)  # Field name made lowercase.
    eightdigitpassword = models.CharField(db_column='EightDigitPassword', max_length=8, blank=True,
                                          null=True)  # Field name made lowercase.
    remotenumber = models.CharField(db_column='RemoteNumber', max_length=4, blank=True,
                                    null=True)  # Field name made lowercase.
    xidnumber = models.CharField(db_column='XIDNumber', max_length=7, blank=True,
                                 null=True)  # Field name made lowercase.
    transmittertype = models.CharField(db_column='TransmitterType', max_length=3, blank=True,
                                       null=True)  # Field name made lowercase.
    transmissionnumber = models.BigIntegerField(db_column='TransmissionNumber', blank=True,
                                                null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nextsednumber = models.IntegerField(db_column='NextSEDNumber', blank=True, null=True)  # Field name made lowercase.
    abiofficecode = models.CharField(db_column='ABIOfficeCode', max_length=2, blank=True,
                                     null=True)  # Field name made lowercase.
    support_pms = models.BooleanField(db_column='Support_PMS', blank=True, null=True)  # Field name made lowercase.
    statementtype = models.CharField(db_column='StatementType', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    processach_ap = models.BooleanField(db_column='ProcessACH_AP', blank=True, null=True)  # Field name made lowercase.
    payersunitnumber = models.CharField(db_column='PayersUnitNumber', max_length=10, blank=True,
                                        null=True)  # Field name made lowercase.
    checkseb = models.BooleanField(db_column='CheckSEB', blank=True, null=True)  # Field name made lowercase.
    bondproducernumber = models.CharField(db_column='BondProducerNumber', max_length=10, blank=True,
                                          null=True)  # Field name made lowercase.
    checkpoa = models.BooleanField(db_column='CheckPOA', blank=True, null=True)  # Field name made lowercase.
    systemtimezone = models.CharField(db_column='SystemTimeZone', max_length=3, blank=True,
                                      null=True)  # Field name made lowercase.
    highwaypermitfeeschargecode = models.SmallIntegerField(db_column='HighwayPermitFeesChargeCode', blank=True,
                                                           null=True)  # Field name made lowercase.
    userfeeschargecode = models.SmallIntegerField(db_column='UserFeesChargeCode', blank=True,
                                                  null=True)  # Field name made lowercase.
    freightchargecode = models.SmallIntegerField(db_column='FreightChargeCode', blank=True,
                                                 null=True)  # Field name made lowercase.
    driverfeeschargecode = models.SmallIntegerField(db_column='DriverFeesChargeCode', blank=True,
                                                    null=True)  # Field name made lowercase.
    otherfeeschargecode = models.SmallIntegerField(db_column='OtherFeesChargeCode', blank=True,
                                                   null=True)  # Field name made lowercase.
    highwayfeevendornumber = models.SmallIntegerField(db_column='HighwayFeeVendorNumber', blank=True,
                                                      null=True)  # Field name made lowercase.
    userfeesvendornumber = models.SmallIntegerField(db_column='UserFeesVendorNumber', blank=True,
                                                    null=True)  # Field name made lowercase.
    driverfeesvendornumber = models.SmallIntegerField(db_column='DriverFeesVendorNumber', blank=True,
                                                      null=True)  # Field name made lowercase.
    freightchecksvendornumber = models.SmallIntegerField(db_column='FreightChecksVendorNumber', blank=True,
                                                         null=True)  # Field name made lowercase.
    defaultcustomercode = models.SmallIntegerField(db_column='DefaultCustomerCode', blank=True,
                                                   null=True)  # Field name made lowercase.
    dwebsite = models.CharField(db_column='dWebSite', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    gastoscondetalle = models.CharField(db_column='GastosConDetalle', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    posicionporsucursal = models.CharField(db_column='PosicionPorSucursal', max_length=1, blank=True,
                                           null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=5, blank=True,
                                       null=True)  # Field name made lowercase.
    controlcters = models.CharField(db_column='ControlCters', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    solocomprasdefinitivas = models.CharField(db_column='SoloComprasDefinitivas', max_length=1, blank=True,
                                              null=True)  # Field name made lowercase.
    multiempresa = models.CharField(db_column='MultiEmpresa', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    origendestino = models.CharField(db_column='OrigenDestino', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    usamsoffice = models.CharField(db_column='UsaMSOffice', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    codigosat = models.CharField(db_column='CodigoSAT', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    consecutivosat = models.CharField(db_column='ConsecutivoSAT', max_length=20, blank=True,
                                      null=True)  # Field name made lowercase.
    usacodigocorp = models.CharField(db_column='UsaCodigoCorp', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    solicitudpagoalgrabar = models.CharField(db_column='SolicitudPagoalGrabar', max_length=1, blank=True,
                                             null=True)  # Field name made lowercase.
    totall = models.SmallIntegerField(db_column='TotalL', blank=True, null=True)  # Field name made lowercase.
    sc = models.CharField(db_column='SC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nrointtra = models.CharField(db_column='NroInttra', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    cantdecimalesea = models.CharField(db_column='CantDecimalesEA', max_length=5, blank=True,
                                       null=True)  # Field name made lowercase.
    intercomex = models.CharField(db_column='Intercomex', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    numempresa = models.SmallIntegerField(db_column='NumEmpresa', blank=True, null=True)  # Field name made lowercase.
    statusseguimiento = models.CharField(db_column='StatusSeguimiento', max_length=20, blank=True,
                                         null=True)  # Field name made lowercase.
    campoactividadobligatorio = models.CharField(db_column='CampoActividadObligatorio', max_length=1, blank=True,
                                                 null=True)  # Field name made lowercase.
    fuentemail = models.CharField(db_column='FuenteMail', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    fuentetamanomail = models.SmallIntegerField(db_column='FuenteTamanoMail', blank=True,
                                                null=True)  # Field name made lowercase.
    tsa = models.CharField(db_column='TSA', max_length=30, blank=True, null=True)  # Field name made lowercase.
    smtp = models.CharField(db_column='SMTP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    port = models.IntegerField(db_column='Port', blank=True, null=True)  # Field name made lowercase.
    datosfemsa = models.CharField(db_column='DatosFEMSA', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    controldefechas = models.CharField(db_column='ControlDeFechas', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    asuntomailresumido = models.CharField(db_column='AsuntoMailResumido', max_length=1, blank=True,
                                          null=True)  # Field name made lowercase.
    controlcterhouse = models.CharField(db_column='ControlCterHouse', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    anpworks = models.CharField(db_column='ANPWorks', max_length=1, blank=True, null=True)  # Field name made lowercase.
    usacodigoedi = models.CharField(db_column='UsaCodigoEDI', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    usacostoinicial = models.CharField(db_column='UsaCostoInicial', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    urltracking = models.CharField(db_column='URLTracking', max_length=200, blank=True,
                                   null=True)  # Field name made lowercase.
    usersmtp = models.CharField(db_column='UserSMTP', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    passsmtp = models.CharField(db_column='PassSMTP', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    emailrespuesta = models.CharField(db_column='EmailRespuesta', max_length=200, blank=True,
                                      null=True)  # Field name made lowercase.
    selclienteconsolidar = models.CharField(db_column='SelClienteConsolidar', max_length=1, blank=True,
                                            null=True)  # Field name made lowercase.
    nromaersk = models.CharField(db_column='NroMaersk', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    utilizacartaaprobacion = models.CharField(db_column='UtilizaCartaAprobacion', max_length=1, blank=True,
                                              null=True)  # Field name made lowercase.
    nrosafmarine = models.CharField(db_column='NroSafmarine', max_length=20, blank=True,
                                    null=True)  # Field name made lowercase.
    nomempresaawb = models.CharField(db_column='NomEmpresaAWB', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.
    impsegcotivencida = models.CharField(db_column='ImpSegCotiVencida', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.
    lugarnotify = models.CharField(db_column='LugarNotify', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    largominpassword = models.SmallIntegerField(db_column='LargoMinPassword', blank=True,
                                                null=True)  # Field name made lowercase.
    complejidad = models.CharField(db_column='Complejidad', max_length=10, blank=True,
                                   null=True)  # Field name made lowercase.
    intentosfallidos = models.SmallIntegerField(db_column='IntentosFallidos', blank=True,
                                                null=True)  # Field name made lowercase.
    tiempoinactividad = models.SmallIntegerField(db_column='TiempoInactividad', blank=True,
                                                 null=True)  # Field name made lowercase.
    bloqueoriesgoso = models.CharField(db_column='BloqueoRiesgoso', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    usacontrolseguro = models.CharField(db_column='UsaControlSeguro', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    dnombrechino = models.CharField(db_column='dNombreChino', max_length=100, blank=True,
                                    null=True)  # Field name made lowercase.
    stockawbempresa = models.CharField(db_column='StockAWBEmpresa', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    posicionmes = models.CharField(db_column='PosicionMes', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    emitebloriginal = models.CharField(db_column='EmiteBLOriginal', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    cantdecimalespeso = models.CharField(db_column='CantDecimalesPeso', max_length=5, blank=True,
                                         null=True)  # Field name made lowercase.
    dashboardeawb = models.CharField(db_column='DashboardEAWB', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    binaryattach = models.BooleanField(db_column='BinaryAttach', blank=True, null=True)  # Field name made lowercase.
    campotraficoobligatorio = models.CharField(db_column='CampoTraficoObligatorio', max_length=1, blank=True,
                                               null=True)  # Field name made lowercase.

    def __str__(self):
        return self.dnombre


class Estados(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.


class Formapago(models.Model):
    codigo = models.SmallIntegerField(db_column='Codigo', unique=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True,
                                   null=True)  # Field name made lowercase.


class Grupos(models.Model):
    grupo = models.CharField(max_length=50)
    detalle = models.TextField(blank=True, null=True)  # This field type is a guess.


class Guiascentro(models.Model):
    transportista = models.SmallIntegerField(db_column='Transportista', unique=True)  # Field name made lowercase.
    prefijo = models.SmallIntegerField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    estado = models.SmallIntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    refmaster = models.SmallIntegerField(db_column='RefMaster', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.


class Houses(models.Model):
    contador = models.FloatField(blank=True, null=True)
    em = models.FloatField(db_column='EM', blank=True, null=True)  # Field name made lowercase.
    et = models.FloatField(db_column='ET', blank=True, null=True)  # Field name made lowercase.


class Interfaces(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    tipointerface = models.CharField(db_column='TipoInterface', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    formato = models.CharField(db_column='Formato', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cabezal = models.CharField(db_column='Cabezal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    delimitador = models.CharField(db_column='Delimitador', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.


class Interfacesatributos(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombrecampo = models.CharField(db_column='NombreCampo', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    entradato = models.CharField(db_column='EntraDato', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    saledato = models.CharField(db_column='SaleDato', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.


class Interfacesdetalle(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombrecampo = models.CharField(db_column='NombreCampo', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    tipodato = models.CharField(db_column='TipoDato', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    sube = models.CharField(db_column='Sube', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nombrecomo = models.CharField(db_column='NombreComo', max_length=100, blank=True,
                                  null=True)  # Field name made lowercase.
    posicion = models.SmallIntegerField(db_column='Posicion', blank=True, null=True)  # Field name made lowercase.
    formato = models.CharField(db_column='Formato', max_length=100, blank=True, null=True)  # Field name made lowercase.


class Llegadas(models.Model):
    vapor = models.CharField(db_column='Vapor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    llegada = models.DateTimeField(db_column='Llegada', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True,
                             null=True)  # Field name made lowercase. This field type is a guess.
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)  # Field name made lowercase.
    semana = models.IntegerField(db_column='Semana', blank=True, null=True)  # Field name made lowercase.
    fechastacking = models.DateTimeField(db_column='FechaStacking', blank=True, null=True)  # Field name made lowercase.
    horastacking = models.CharField(db_column='HoraStacking', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    fechacutoff = models.DateTimeField(db_column='FechaCutOff', blank=True, null=True)  # Field name made lowercase.
    horacutoff = models.CharField(db_column='HoraCutOff', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    fechacutoffvgm = models.DateTimeField(db_column='FechaCutOffVGM', blank=True,
                                          null=True)  # Field name made lowercase.
    horacutoffvgm = models.CharField(db_column='HoraCutOffVGM', max_length=30, blank=True,
                                     null=True)  # Field name made lowercase.


class Llegadasdetalle(models.Model):
    idllegadas = models.IntegerField(db_column='IDLlegadas')  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.


class Monedas(models.Model):
    codigo = models.SmallIntegerField(unique=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    pais = models.CharField(max_length=30, blank=True, null=True)
    simbolo = models.CharField(max_length=3, blank=True, null=True)
    solicitar = models.CharField(max_length=1, blank=True, null=True)
    alias = models.SmallIntegerField(blank=True, null=True)
    valorminimo = models.DecimalField(db_column='ValorMinimo', max_digits=19, decimal_places=4, blank=True,
                                      null=True)  # Field name made lowercase.
    valormaximo = models.DecimalField(db_column='ValorMaximo', max_digits=19, decimal_places=4, blank=True,
                                      null=True)  # Field name made lowercase.
    paridadminima = models.DecimalField(db_column='ParidadMinima', max_digits=19, decimal_places=4, blank=True,
                                        null=True)  # Field name made lowercase.
    paridadmaxima = models.DecimalField(db_column='ParidadMaxima', max_digits=19, decimal_places=4, blank=True,
                                        null=True)  # Field name made lowercase.
    busquedaweb = models.CharField(db_column='BusquedaWeb', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    corporativo = models.CharField(db_column='Corporativo', max_length=15, blank=True,
                                   null=True)  # Field name made lowercase.

    def __str__(self):
        return '%s' % self.nombre


class Notificaciones(models.Model):
    codigo = models.SmallIntegerField(db_column='Codigo', unique=True)  # Field name made lowercase.
    titulo = models.CharField(db_column='Titulo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    desde = models.CharField(db_column='Desde', max_length=1, blank=True, null=True)  # Field name made lowercase.
    destinatario = models.CharField(db_column='Destinatario', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    razonsocial = models.CharField(db_column='RazonSocial', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ruc = models.CharField(db_column='Ruc', max_length=1, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=1, blank=True, null=True)  # Field name made lowercase.
    texto = models.TextField(db_column='Texto', blank=True,
                             null=True)  # Field name made lowercase. This field type is a guess.
    tipo = models.CharField(db_column='Tipo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    idioma = models.SmallIntegerField(db_column='Idioma', blank=True, null=True)  # Field name made lowercase.
    salida = models.CharField(db_column='Salida', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enviodatoshouse = models.CharField(db_column='EnvioDatosHouse', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.


class Nromensaje(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.


class Organiza(models.Model):
    codigo = models.SmallIntegerField()
    empresa = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=3, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    cpostal = models.CharField(max_length=10, blank=True, null=True)
    contactos = models.TextField(blank=True, null=True)  # This field type is a guess.


class Otrosservicios(models.Model):
    codigo = models.SmallIntegerField(db_column='Codigo', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True,
                                   null=True)  # Field name made lowercase.


class Passsocios(models.Model):
    pnombre = models.CharField(db_column='Pnombre', max_length=30, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.


class Password(models.Model):
    pnombre = models.CharField(max_length=30)
    pword = models.CharField(max_length=30, blank=True, null=True)
    pnivel = models.SmallIntegerField(blank=True, null=True)
    accaltas = models.CharField(max_length=1, blank=True, null=True)
    accbajas = models.CharField(max_length=1, blank=True, null=True)
    acceditar = models.CharField(max_length=1, blank=True, null=True)
    accexpaerea = models.CharField(max_length=1, blank=True, null=True)
    accexpmarit = models.CharField(max_length=1, blank=True, null=True)
    accexpterra = models.CharField(max_length=1, blank=True, null=True)
    accimpaerea = models.CharField(max_length=1, blank=True, null=True)
    accimpmarit = models.CharField(max_length=1, blank=True, null=True)
    accimpterra = models.CharField(max_length=1, blank=True, null=True)
    accadmin = models.CharField(max_length=1, blank=True, null=True)
    acccotiz = models.CharField(max_length=1, blank=True, null=True)
    acccexaerea = models.CharField(max_length=1, blank=True, null=True)
    acccexmarit = models.CharField(max_length=1, blank=True, null=True)
    acccexterra = models.CharField(max_length=1, blank=True, null=True)
    acccimaerea = models.CharField(max_length=1, blank=True, null=True)
    acccimmarit = models.CharField(max_length=1, blank=True, null=True)
    acccimterra = models.CharField(max_length=1, blank=True, null=True)
    accconsul = models.CharField(max_length=1, blank=True, null=True)
    accconver = models.CharField(max_length=1, blank=True, null=True)
    accnuevo = models.CharField(max_length=1, blank=True, null=True)
    accedita = models.CharField(max_length=1, blank=True, null=True)
    accborra = models.CharField(max_length=1, blank=True, null=True)
    accver = models.CharField(max_length=1, blank=True, null=True)
    accpreventa = models.CharField(max_length=1, blank=True, null=True)
    accdocum = models.CharField(max_length=1, blank=True, null=True)
    accrenta = models.CharField(max_length=1, blank=True, null=True)
    accedi = models.CharField(max_length=1, blank=True, null=True)
    accbonif = models.CharField(max_length=1, blank=True, null=True)
    accfacturar = models.CharField(max_length=1, blank=True, null=True)
    acccobrar = models.CharField(max_length=1, blank=True, null=True)
    accprovee = models.CharField(max_length=1, blank=True, null=True)
    accpagar = models.CharField(max_length=1, blank=True, null=True)
    accorden = models.CharField(max_length=1, blank=True, null=True)
    acccontab = models.CharField(max_length=1, blank=True, null=True)
    accseguir = models.CharField(max_length=1, blank=True, null=True)
    acctransito = models.CharField(max_length=1, blank=True, null=True)
    inicial = models.CharField(max_length=3, blank=True, null=True)
    nombre = models.CharField(max_length=40, blank=True, null=True)
    mail = models.CharField(max_length=50, blank=True, null=True)
    grupo = models.CharField(max_length=50, blank=True, null=True)
    accbloqueo = models.CharField(max_length=1, blank=True, null=True)
    accingcheques = models.CharField(max_length=1, blank=True, null=True)
    accingdocum = models.CharField(max_length=1, blank=True, null=True)
    accbajacheques = models.CharField(max_length=1, blank=True, null=True)
    accbajadocum = models.CharField(max_length=1, blank=True, null=True)
    accvtocheemi = models.CharField(max_length=1, blank=True, null=True)
    accvtodocemi = models.CharField(max_length=1, blank=True, null=True)
    acccontrol = models.CharField(max_length=1, blank=True, null=True)
    accnotacredito = models.CharField(max_length=1, blank=True, null=True)
    accsocios = models.CharField(max_length=1, blank=True, null=True)
    accservicios = models.CharField(max_length=1, blank=True, null=True)
    accvendedores = models.CharField(max_length=1, blank=True, null=True)
    accorganiza = models.CharField(max_length=1, blank=True, null=True)
    accdepositos = models.CharField(max_length=1, blank=True, null=True)
    accmonedas = models.CharField(max_length=1, blank=True, null=True)
    accpaises = models.CharField(max_length=1, blank=True, null=True)
    accproductos = models.CharField(max_length=1, blank=True, null=True)
    accplan = models.CharField(max_length=1, blank=True, null=True)
    acctextos = models.CharField(max_length=1, blank=True, null=True)
    acctraficos = models.CharField(max_length=1, blank=True, null=True)
    accvapores = models.CharField(max_length=1, blank=True, null=True)
    accareas = models.CharField(max_length=1, blank=True, null=True)
    accfondos = models.CharField(max_length=1, blank=True, null=True)
    caja = models.BigIntegerField(blank=True, null=True)
    sucursal = models.SmallIntegerField(blank=True, null=True)
    accsoccli = models.CharField(max_length=1, blank=True, null=True)
    accsocpro = models.CharField(max_length=1, blank=True, null=True)
    accsocmix = models.CharField(max_length=1, blank=True, null=True)
    accsoctra = models.CharField(max_length=1, blank=True, null=True)
    accsocage = models.CharField(max_length=1, blank=True, null=True)
    accsocarm = models.CharField(max_length=1, blank=True, null=True)
    accsocdes = models.CharField(max_length=1, blank=True, null=True)
    accsocotr = models.CharField(max_length=1, blank=True, null=True)
    accediprev = models.CharField(max_length=1, blank=True, null=True)
    acceliprev = models.CharField(max_length=1, blank=True, null=True)
    accgendocdef = models.CharField(max_length=1, blank=True, null=True)
    accversucursales = models.CharField(db_column='AccVerSucursales', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    accborrodoc = models.CharField(db_column='AccBorroDoc', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accctacodif = models.CharField(db_column='AccCtaCodif', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accvertodo = models.CharField(db_column='AccVerTodo', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    accexportar = models.CharField(db_column='AccExportar', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accverbonifcli = models.CharField(db_column='AccVerBonifCli', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    acceditacerrado = models.CharField(db_column='AccEditaCerrado', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    idioma = models.SmallIntegerField(db_column='Idioma', blank=True, null=True)  # Field name made lowercase.
    accfaceleclotes = models.CharField(db_column='AccFacElecLotes', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    masterkey = models.CharField(db_column='MasterKey', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    accentregaorden = models.CharField(db_column='accEntregaOrden', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    accciudades = models.CharField(db_column='accCiudades', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accproyectos = models.CharField(db_column='accProyectos', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accscheduleb = models.CharField(db_column='accScheduleb', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accports = models.CharField(db_column='accPorts', max_length=1, blank=True, null=True)  # Field name made lowercase.
    acccodes = models.CharField(db_column='accCodes', max_length=1, blank=True, null=True)  # Field name made lowercase.
    accimppurgescheduleb = models.CharField(db_column='accImpPurgeScheduleb', max_length=1, blank=True,
                                            null=True)  # Field name made lowercase.
    accaes = models.CharField(db_column='accAES', max_length=1, blank=True, null=True)  # Field name made lowercase.
    diascambio = models.SmallIntegerField(db_column='DiasCambio', blank=True, null=True)  # Field name made lowercase.
    fechaultimacambio = models.DateTimeField(db_column='FechaUltimaCambio', blank=True,
                                             null=True)  # Field name made lowercase.
    securityiata = models.CharField(db_column='SecurityIata', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    cargo = models.CharField(db_column='Cargo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    acccontrolprov = models.CharField(db_column='AccControlProv', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    accselecvendedor = models.CharField(db_column='AccSelecVendedor', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    accinfocontable = models.CharField(db_column='AccInfoContable', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    accborrarattach = models.CharField(db_column='AccBorrarAttach', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    accprefactura = models.CharField(db_column='AccPreFactura', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    acceditafollowup = models.CharField(db_column='AccEditaFollowUp', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    accmodposicion = models.CharField(db_column='AccModPosicion', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    accmoddocumentos = models.CharField(db_column='AccModDocumentos', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    internodirecto = models.CharField(db_column='InternoDirecto', max_length=30, blank=True,
                                      null=True)  # Field name made lowercase.
    clientemail = models.CharField(db_column='ClienteMail', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accmanten = models.CharField(db_column='AccManten', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    acceditaeditados = models.CharField(db_column='AccEditaEditados', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    acctrace = models.CharField(db_column='AccTrace', max_length=1, blank=True, null=True)  # Field name made lowercase.
    accdepuradores = models.CharField(db_column='AccDepuradores', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    acceditafinanzas = models.CharField(db_column='AccEditaFinanzas', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    acccambiausuario = models.CharField(db_column='AccCambiaUsuario', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    accimprimir = models.CharField(db_column='AccImprimir', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    acccambiafecha = models.CharField(db_column='AccCambiaFecha', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    accinfotracking = models.CharField(db_column='AccInfoTracking', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    accvertodoop = models.CharField(db_column='AccVerTodoOP', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accvertodosc = models.CharField(db_column='AccVerTodoSC', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accmodsegvinculado = models.CharField(db_column='AccModSegVinculado', max_length=1, blank=True,
                                          null=True)  # Field name made lowercase.
    accmodimpu = models.CharField(db_column='AccModImpu', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    accfechavto = models.CharField(db_column='AccFechaVto', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accfechacoti = models.CharField(db_column='AccFechaCoti', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    acceditacotizacion = models.CharField(db_column='AccEditaCotizacion', max_length=1, blank=True,
                                          null=True)  # Field name made lowercase.
    usersmtp = models.CharField(db_column='UserSMTP', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    passsmtp = models.CharField(db_column='PassSMTP', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    correo = models.CharField(db_column='Correo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    acctodosusrretransmiten95 = models.CharField(db_column='AccTodosUsrRetransmiten95', max_length=1, blank=True,
                                                 null=True)  # Field name made lowercase.
    acceditatodose = models.CharField(db_column='accEditaTodoSE', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    accreenviofacelec = models.CharField(db_column='accReenvioFacElec', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.
    accsocioactivo = models.CharField(db_column='accSocioActivo', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    accreimprimeoriginal = models.CharField(db_column='accReimprimeOriginal', max_length=1, blank=True,
                                            null=True)  # Field name made lowercase.
    acceditaaceptada = models.CharField(db_column='accEditaAceptada', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    encargadocuenta = models.CharField(db_column='EncargadoCuenta', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    accfacdefinitiva = models.CharField(db_column='accFacDefinitiva', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    accfacprovision = models.CharField(db_column='accFacProvision', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    accpasarprovdef = models.CharField(db_column='accPasarProvDef', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    accsolovariables = models.CharField(db_column='accSoloVariables', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    accbodega = models.CharField(db_column='accBodega', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    accwr = models.CharField(db_column='accWR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    accegresowr = models.CharField(db_column='accEgresoWR', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accpickwr = models.CharField(db_column='accPickWR', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    accasistwr = models.CharField(db_column='accAsistWR', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    accdistribuwr = models.CharField(db_column='accDistribuWR', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    accfraccionwr = models.CharField(db_column='accFraccionWR', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    accagruparwr = models.CharField(db_column='accAgruparWR', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accendosowr = models.CharField(db_column='accEndosoWR', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accrepackwr = models.CharField(db_column='accRepackWR', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accajustewr = models.CharField(db_column='accAjusteWR', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accnacionalwr = models.CharField(db_column='accNacionalWR', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    accubicarwr = models.CharField(db_column='accUbicarWR', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accremitowr = models.CharField(db_column='accRemitoWR', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    acctarifaswr = models.CharField(db_column='accTarifasWR', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accestadiswr = models.CharField(db_column='accEstadisWR', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accinventwr = models.CharField(db_column='accInventWR', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accfichawr = models.CharField(db_column='accFichaWR', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    acceventoswr = models.CharField(db_column='accEventosWR', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accfamiliawr = models.CharField(db_column='accFamiliaWR', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accitemswr = models.CharField(db_column='accItemsWR', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    accbodegaswr = models.CharField(db_column='accBodegasWR', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accoperawr = models.CharField(db_column='accOperaWR', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    acctareaswr = models.CharField(db_column='accTareasWR', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accinsumoswr = models.CharField(db_column='accInsumosWR', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accequiposwr = models.CharField(db_column='accEquiposWR', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accvehiwr = models.CharField(db_column='accVehiWR', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    accstatuswr = models.CharField(db_column='accStatusWR', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    acccompwr = models.CharField(db_column='accCompWR', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    cuentabloqueada = models.CharField(db_column='CuentaBloqueada', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    ultimaactividad = models.DateTimeField(db_column='UltimaActividad', blank=True,
                                           null=True)  # Field name made lowercase.
    skype = models.CharField(db_column='Skype', max_length=50, blank=True, null=True)  # Field name made lowercase.
    celular = models.CharField(db_column='Celular', max_length=20, blank=True, null=True)  # Field name made lowercase.
    acccostos = models.CharField(db_column='accCostos', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    accoservicios = models.CharField(db_column='AccOServicios', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    acctruck = models.CharField(db_column='AccTruck', max_length=1, blank=True, null=True)  # Field name made lowercase.
    estacion = models.CharField(db_column='Estacion', max_length=4, blank=True, null=True)  # Field name made lowercase.
    aprobarvalormin = models.DecimalField(db_column='AprobarValorMin', max_digits=19, decimal_places=4, blank=True,
                                          null=True)  # Field name made lowercase.
    aprobarvalormax = models.DecimalField(db_column='AprobarValorMax', max_digits=19, decimal_places=4, blank=True,
                                          null=True)  # Field name made lowercase.
    accniif = models.CharField(db_column='accNIIF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    accactivofijo = models.CharField(db_column='accActivoFijo', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    accmodifpicking = models.CharField(db_column='accModifPicking', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    accmodifegreso = models.CharField(db_column='accModifEgreso', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    accfechacorte = models.CharField(db_column='accFechaCorte', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    acclimitecredito = models.CharField(db_column='accLimiteCredito', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    accaduanawr = models.CharField(db_column='AccAduanaWR', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    accpedidoswr = models.CharField(db_column='AccPedidosWR', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    accreacpedidoswr = models.CharField(db_column='AccReacPedidosWR', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    accveotodoattach = models.CharField(db_column='AccVeoTodoAttach', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    accmodhouse = models.CharField(db_column='AccModHouse', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.


class Passwordhistorial(models.Model):
    pnombre = models.CharField(max_length=30, blank=True, null=True)
    pword = models.CharField(max_length=30, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.


class Permisosterr(models.Model):
    cliente = models.IntegerField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=30, blank=True, null=True)  # Field name made lowercase.
    peroriginal = models.CharField(db_column='PerOriginal', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.
    percomplem = models.CharField(db_column='PerComplem', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    contrif = models.CharField(db_column='Contrif', max_length=20, blank=True, null=True)  # Field name made lowercase.


class Prefijos(models.Model):
    prefijo = models.CharField(max_length=2, blank=True, null=True)
    detalle = models.CharField(max_length=30, blank=True, null=True)


class Provincias(models.Model):
    codigo = models.IntegerField(db_column='Codigo', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    abreviacion = models.CharField(db_column='Abreviacion', max_length=10, blank=True,
                                   null=True)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.


class Proyectos(models.Model):
    codigo = models.SmallIntegerField(db_column='Codigo', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True,
                                     null=True)  # Field name made lowercase. This field type is a guess.
    status = models.SmallIntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name_plural = "Proyectos"


class Retenciones(models.Model):
    servicio = models.SmallIntegerField(blank=True, null=True)
    cuenta = models.BigIntegerField(blank=True, null=True)
    aplica = models.CharField(max_length=1, blank=True, null=True)
    comentario = models.CharField(max_length=50, blank=True, null=True)
    porcentaje = models.FloatField(blank=True, null=True)
    tipocli = models.SmallIntegerField(db_column='TipoCli', blank=True, null=True)  # Field name made lowercase.
    baseminima = models.FloatField(db_column='BaseMinima', blank=True, null=True)  # Field name made lowercase.
    contracuenta = models.BigIntegerField(db_column='ContraCuenta', blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    autorretenedor = models.CharField(db_column='Autorretenedor', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    suma = models.BooleanField(db_column='Suma', blank=True, null=True)  # Field name made lowercase.
    basemaxima = models.FloatField(db_column='BaseMaxima', blank=True, null=True)  # Field name made lowercase.


class Servrelacion(models.Model):
    codigovta = models.SmallIntegerField(db_column='CodigoVTA', blank=True, null=True)  # Field name made lowercase.
    codigocpa = models.SmallIntegerField(db_column='CodigoCPA', blank=True, null=True)  # Field name made lowercase.


class Servvariables(models.Model):
    codigo = models.SmallIntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    tipovariable = models.CharField(db_column='TipoVariable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    variablecada = models.SmallIntegerField(db_column='VariableCada', blank=True,
                                            null=True)  # Field name made lowercase.
    baseminima = models.IntegerField(db_column='BaseMinima', blank=True, null=True)  # Field name made lowercase.
    redondea = models.CharField(db_column='Redondea', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sociocomercial = models.IntegerField(db_column='SocioComercial', blank=True,
                                         null=True)  # Field name made lowercase.
    tiposocio = models.CharField(db_column='TipoSocio', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=5, blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    tarifa = models.CharField(db_column='Tarifa', max_length=1, blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
    minimo = models.DecimalField(db_column='Minimo', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
    maximo = models.DecimalField(db_column='Maximo', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    producto = models.SmallIntegerField(db_column='Producto', blank=True, null=True)  # Field name made lowercase.
    unidad = models.CharField(db_column='Unidad', max_length=3, blank=True, null=True)  # Field name made lowercase.
    unidadvol = models.CharField(db_column='UnidadVol', max_length=3, blank=True,
                                 null=True)  # Field name made lowercase.
    desdevalor = models.DecimalField(db_column='DesdeValor', max_digits=19, decimal_places=4, blank=True,
                                     null=True)  # Field name made lowercase.


class Servicios(models.Model):
    codigo = models.SmallIntegerField(unique=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    gravado = models.SmallIntegerField(blank=True, null=True)
    tasa = models.CharField(max_length=1, blank=True, null=True)
    refparam = models.SmallIntegerField(blank=True, null=True)
    prefijo = models.CharField(max_length=10, blank=True, null=True)
    contable = models.BigIntegerField(blank=True, null=True)
    contiva = models.IntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    imputar = models.CharField(max_length=1, blank=True, null=True)
    tipogasto = models.CharField(max_length=1, blank=True, null=True)
    variable = models.BooleanField(default=False)
    tipovariable = models.CharField(max_length=1, blank=True, null=True)
    variablecada = models.FloatField(blank=True, null=True)
    redondea = models.BooleanField(default=False)
    baseminima = models.FloatField(blank=True, null=True)
    ctaorden = models.BooleanField(default=False)
    modo = models.CharField(max_length=1, blank=True, null=True)
    ibruto = models.BooleanField(default=False)
    minimo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    maximo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    operacion = models.CharField(max_length=1, blank=True, null=True)
    transito = models.CharField(max_length=1, blank=True, null=True)
    maritimo = models.CharField(max_length=1, blank=True, null=True)
    preciob = models.DecimalField(db_column='precioB', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    precioc = models.DecimalField(db_column='precioC', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    preciod = models.DecimalField(db_column='precioD', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    corporativo = models.CharField(max_length=15, blank=True, null=True)
    ctaordeniva = models.BooleanField(default=False)
    repartir = models.CharField(max_length=1, blank=True, null=True)
    tipoitem = models.CharField(max_length=1, blank=True, null=True)
    itemstock = models.CharField(max_length=1, blank=True, null=True)
    codigostock = models.CharField(max_length=30, blank=True, null=True)
    ctavtastock = models.IntegerField(blank=True, null=True)
    ctacomstock = models.IntegerField(blank=True, null=True)
    familia = models.SmallIntegerField(blank=True, null=True)
    cofis = models.CharField(max_length=1, blank=True, null=True)
    unistock = models.CharField(max_length=10, blank=True, null=True)
    minimob = models.DecimalField(db_column='minimoB', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    maximob = models.DecimalField(db_column='maximoB', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    minimoc = models.DecimalField(db_column='minimoC', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    maximoc = models.DecimalField(db_column='maximoC', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    minimod = models.DecimalField(db_column='minimoD', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    maximod = models.DecimalField(db_column='maximoD', max_digits=19, decimal_places=4, blank=True,
                                  null=True)  # Field name made lowercase.
    nombreingles = models.CharField(max_length=100, blank=True, null=True)
    tomarcomoiva = models.CharField(db_column='TomarComoIVA', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    activa = models.CharField(db_column='Activa', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recuperogastos = models.CharField(db_column='RecuperoGastos', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    servicioscliente = models.CharField(db_column='ServiciosCliente', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    extracosto = models.CharField(db_column='ExtraCosto', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    catsat = models.CharField(db_column='catSAT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    claveunidadsat = models.CharField(db_column='ClaveUnidadSAT', max_length=4, blank=True,
                                      null=True)  # Field name made lowercase.
    montonoaplicaretencion = models.DecimalField(db_column='MontoNoAplicaRetencion', max_digits=19, decimal_places=4,
                                                 blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.nombre

    def get_codigo(self):
        codigo = Servicios.objects.order_by('-codigo').values('codigo').first()
        return codigo['codigo'] + 1


class Sociosweb(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    codigoweb = models.IntegerField(db_column='CodigoWeb', blank=True, null=True)  # Field name made lowercase.


class Status(models.Model):
    status = models.CharField(max_length=20, blank=True, null=True)
    costos = models.CharField(max_length=1, blank=True, null=True)


class Statussocios(models.Model):
    numero = models.SmallIntegerField(unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)


class Sucursales(models.Model):
    nrosucursal = models.SmallIntegerField(db_column='NroSucursal', unique=True)  # Field name made lowercase.
    factura = models.IntegerField(db_column='Factura', blank=True, null=True)  # Field name made lowercase.
    notacredito = models.IntegerField(db_column='NotaCredito', blank=True, null=True)  # Field name made lowercase.
    recibo = models.IntegerField(db_column='Recibo', blank=True, null=True)  # Field name made lowercase.
    contado = models.IntegerField(db_column='Contado', blank=True, null=True)  # Field name made lowercase.
    notadebito = models.IntegerField(db_column='NotaDebito', blank=True, null=True)  # Field name made lowercase.
    devolcontado = models.IntegerField(db_column='DevolContado', blank=True, null=True)  # Field name made lowercase.
    nombresucursal = models.CharField(db_column='NombreSucursal', max_length=30, blank=True,
                                      null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='DRuc', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=5, blank=True,
                                       null=True)  # Field name made lowercase.
    serie = models.CharField(db_column='Serie', max_length=1, blank=True, null=True)  # Field name made lowercase.
    keydosificacion = models.CharField(db_column='KeyDosificacion', max_length=255, blank=True,
                                       null=True)  # Field name made lowercase.
    noautorizacion = models.CharField(db_column='NoAutorizacion', max_length=255, blank=True,
                                      null=True)  # Field name made lowercase.
    fechalimiteemision = models.DateTimeField(db_column='FechaLimiteEmision', blank=True,
                                              null=True)  # Field name made lowercase.
    prefijo = models.IntegerField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.


class Sucursalesargentina(models.Model):
    nrosucursal = models.SmallIntegerField(db_column='NroSucursal', unique=True, blank=True,
                                           null=True)  # Field name made lowercase.
    factura = models.IntegerField(blank=True, null=True)
    notacredito = models.IntegerField(blank=True, null=True)
    recibo = models.IntegerField(blank=True, null=True)
    contado = models.IntegerField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', max_length=30, blank=True,
                                      null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=5, blank=True,
                                       null=True)  # Field name made lowercase.
    prefijo = models.IntegerField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    notadebito = models.IntegerField(db_column='NotaDebito', blank=True, null=True)  # Field name made lowercase.
    facelectronica = models.CharField(db_column='FacElectronica', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.


class Sucursalesbrasil(models.Model):
    nrosucursal = models.SmallIntegerField(db_column='NroSucursal', unique=True, blank=True,
                                           null=True)  # Field name made lowercase.
    factura = models.IntegerField(blank=True, null=True)
    notacredito = models.IntegerField(blank=True, null=True)
    recibo = models.IntegerField(blank=True, null=True)
    contado = models.IntegerField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', max_length=30, blank=True,
                                      null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=5, blank=True,
                                       null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.


class Sucursaleschile(models.Model):
    nrosucursal = models.SmallIntegerField(db_column='NroSucursal', unique=True)  # Field name made lowercase.
    fachilea = models.IntegerField(db_column='FaChileA', blank=True, null=True)  # Field name made lowercase.
    fachileb = models.IntegerField(db_column='FaChileB', blank=True, null=True)  # Field name made lowercase.
    ncchilea = models.IntegerField(db_column='NcChileA', blank=True, null=True)  # Field name made lowercase.
    ncchileb = models.IntegerField(db_column='NcChileB', blank=True, null=True)  # Field name made lowercase.
    ndchilea = models.IntegerField(db_column='NdChileA', blank=True, null=True)  # Field name made lowercase.
    ndchileb = models.IntegerField(db_column='NdChileB', blank=True, null=True)  # Field name made lowercase.
    nombresucursal = models.CharField(db_column='NombreSucursal', max_length=30, blank=True,
                                      null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=5, blank=True,
                                       null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.


class Sucursalesdominicana(models.Model):
    nrosucursal = models.SmallIntegerField(db_column='NroSucursal', unique=True, blank=True,
                                           null=True)  # Field name made lowercase.
    factura = models.IntegerField(blank=True, null=True)
    notacredito = models.IntegerField(blank=True, null=True)
    recibo = models.IntegerField(blank=True, null=True)
    contado = models.IntegerField(blank=True, null=True)
    notadebito = models.IntegerField(db_column='Notadebito', blank=True, null=True)  # Field name made lowercase.
    devolcontado = models.IntegerField(db_column='Devolcontado', blank=True, null=True)  # Field name made lowercase.
    nombresucursal = models.CharField(db_column='NombreSucursal', max_length=30, blank=True,
                                      null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=5, blank=True,
                                       null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.


class Sucursalesmexico(models.Model):
    nrosucursal = models.SmallIntegerField(db_column='NroSucursal', unique=True, blank=True,
                                           null=True)  # Field name made lowercase.
    facturamx = models.IntegerField(blank=True, null=True)
    notacreditomx = models.IntegerField(blank=True, null=True)
    recibofletemx = models.IntegerField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', max_length=30, blank=True,
                                      null=True)  # Field name made lowercase.
    facturamxusd = models.IntegerField(blank=True, null=True)
    ddireccion = models.CharField(db_column='DDireccion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    facturad = models.IntegerField(db_column='FacturaD', blank=True, null=True)  # Field name made lowercase.
    notacreditod = models.IntegerField(db_column='NotaCreditoD', blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=5, blank=True,
                                       null=True)  # Field name made lowercase.
    notacreditousd = models.IntegerField(db_column='NotaCreditoUSD', blank=True,
                                         null=True)  # Field name made lowercase.
    notadebito = models.IntegerField(db_column='NotaDebito', blank=True, null=True)  # Field name made lowercase.
    notadebitousd = models.IntegerField(db_column='NotaDebitoUSD', blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.


class Sucursalesparaguay(models.Model):
    nrosucursal = models.SmallIntegerField(db_column='NroSucursal', unique=True, blank=True,
                                           null=True)  # Field name made lowercase.
    factura = models.IntegerField(blank=True, null=True)
    notacredito = models.IntegerField(blank=True, null=True)
    recibo = models.IntegerField(blank=True, null=True)
    contado = models.IntegerField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', max_length=30, blank=True,
                                      null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=5, blank=True,
                                       null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.


class Sucursalesperu(models.Model):
    nrosucursal = models.SmallIntegerField(db_column='NroSucursal', unique=True, blank=True,
                                           null=True)  # Field name made lowercase.
    factura = models.IntegerField(blank=True, null=True)
    notacredito = models.IntegerField(blank=True, null=True)
    recibo = models.IntegerField(blank=True, null=True)
    contado = models.IntegerField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', max_length=30, blank=True,
                                      null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=5, blank=True,
                                       null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.


class Sucursalesuruguay(models.Model):
    nrosucursal = models.SmallIntegerField(db_column='NroSucursal', unique=True, blank=True,
                                           null=True)  # Field name made lowercase.
    factura = models.IntegerField(blank=True, null=True)
    notacredito = models.IntegerField(blank=True, null=True)
    recibo = models.IntegerField(blank=True, null=True)
    contado = models.IntegerField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', max_length=30, blank=True,
                                      null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=5, blank=True,
                                       null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.


class Sucursalesusa(models.Model):
    nrosucursal = models.SmallIntegerField(db_column='NroSucursal', unique=True, blank=True,
                                           null=True)  # Field name made lowercase.
    factura = models.IntegerField(blank=True, null=True)
    notacredito = models.IntegerField(blank=True, null=True)
    recibo = models.IntegerField(blank=True, null=True)
    contado = models.IntegerField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', max_length=30, blank=True,
                                      null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=5, blank=True,
                                       null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', max_length=35, blank=True,
                                  null=True)  # Field name made lowercase.


class Tipoindustria(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=150, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True,
                                     null=True)  # Field name made lowercase. This field type is a guess.


class Tipooperacion(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=150, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True,
                                     null=True)  # Field name made lowercase. This field type is a guess.


class Trace(models.Model):
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=250, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(db_column='Factura', max_length=50, blank=True, null=True)  # Field name made lowercase.


class Traceinterface(models.Model):
    fechahora = models.DateTimeField(db_column='FechaHora', blank=True, null=True)  # Field name made lowercase.
    embarque = models.IntegerField(db_column='Embarque', blank=True, null=True)  # Field name made lowercase.
    orden = models.CharField(db_column='Orden', max_length=500, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cliente = models.CharField(db_column='Cliente', max_length=50, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=500, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.


class Trackingdetalles(models.Model):
    usuario = models.IntegerField(db_column='Usuario', blank=True, null=True)  # Field name made lowercase.
    idsociocomercial = models.IntegerField(db_column='IDSocioComercial', blank=True,
                                           null=True)  # Field name made lowercase.


class Trackinglogin(models.Model):
    sociocomercial = models.IntegerField(db_column='SocioComercial', blank=True,
                                         null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechain = models.DateTimeField(db_column='FechaIN', blank=True, null=True)  # Field name made lowercase.
    fechaout = models.DateTimeField(db_column='FechaOUT', blank=True, null=True)  # Field name made lowercase.
    horain = models.CharField(db_column='HoraIN', max_length=5, blank=True, null=True)  # Field name made lowercase.
    horaout = models.CharField(db_column='HoraOUT', max_length=5, blank=True, null=True)  # Field name made lowercase.


class Trackingterceros(models.Model):
    email = models.CharField(db_column='Email', unique=True, max_length=200)  # Field name made lowercase.
    passw = models.CharField(db_column='PassW', max_length=30, blank=True, null=True)  # Field name made lowercase.
    cliente = models.IntegerField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    consignatario = models.IntegerField(db_column='Consignatario', blank=True, null=True)  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', max_length=5, blank=True, null=True)  # Field name made lowercase.
    enviomail = models.CharField(db_column='EnvioMail', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    enviosocial = models.CharField(db_column='EnvioSocial', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.


class Trackingusuarios(models.Model):
    codsociocomercial = models.IntegerField(db_column='CodSocioComercial', blank=True,
                                            null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=12, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=12, blank=True,
                                null=True)  # Field name made lowercase.


class Traficos(models.Model):
    codigo = models.SmallIntegerField()
    nombre = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    diasim = models.SmallIntegerField(db_column='DiasIM', blank=True, null=True)  # Field name made lowercase.
    diasia = models.SmallIntegerField(db_column='DiasIA', blank=True, null=True)  # Field name made lowercase.
    diasit = models.SmallIntegerField(db_column='DiasIT', blank=True, null=True)  # Field name made lowercase.
    diasem = models.SmallIntegerField(db_column='DiasEM', blank=True, null=True)  # Field name made lowercase.
    diasea = models.SmallIntegerField(db_column='DiasEA', blank=True, null=True)  # Field name made lowercase.
    diaset = models.SmallIntegerField(db_column='DiasET', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name_plural = "Traficos"


class Vapores(models.Model):
    codigo = models.SmallIntegerField(unique=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    bandera = models.CharField(max_length=50, blank=True, null=True)
    deposito = models.SmallIntegerField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    imo = models.CharField(db_column='IMO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fechaactualizado = models.DateTimeField(db_column='FechaActualizado', blank=True,
                                            null=True)  # Field name made lowercase.

    class Meta:
        ordering = ['nombre', ]

    def __str__(self):
        return '%s' % self.nombre

    def get_codigo(self):
        ultimo_vapor = Vapores.objects.order_by('-codigo').first()
        if ultimo_vapor:
            ultimo_codigo = int(ultimo_vapor.codigo)
            nuevo_codigo = str(ultimo_codigo + 1)
        else:
            nuevo_codigo = '1'

        return nuevo_codigo


class Vendedores(models.Model):
    codigo = models.SmallIntegerField(unique=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    cpostal = models.CharField(max_length=10, blank=True, null=True)
    ciudad = models.CharField(max_length=3, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    condiciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    comiexport = models.FloatField(blank=True, null=True)
    comimport = models.FloatField(blank=True, null=True)
    refparam = models.SmallIntegerField(blank=True, null=True)
    tipoexport = models.CharField(max_length=1, blank=True, null=True)
    tipoimport = models.CharField(max_length=1, blank=True, null=True)
    tipomarexp = models.CharField(max_length=1, blank=True, null=True)
    tipomarimp = models.CharField(max_length=1, blank=True, null=True)
    comimarexp = models.FloatField(blank=True, null=True)
    comimarimp = models.FloatField(blank=True, null=True)
    tipoterexp = models.CharField(max_length=1, blank=True, null=True)
    tipoterimp = models.CharField(max_length=1, blank=True, null=True)
    comiterexp = models.FloatField(blank=True, null=True)
    comiterimp = models.FloatField(blank=True, null=True)
    iniciales = models.CharField(db_column='Iniciales', max_length=3, blank=True,
                                 null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        ordering = ['nombre', ]

    def __str__(self):
        return '%s' % self.nombre


class Vuelos(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    vuelo = models.CharField(db_column='Vuelo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=5, blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True,
                                  null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True,
                                   null=True)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True,
                                     null=True)  # Field name made lowercase. This field type is a guess.
    lunes = models.CharField(db_column='Lunes', max_length=1, blank=True, null=True)  # Field name made lowercase.
    martes = models.CharField(db_column='Martes', max_length=1, blank=True, null=True)  # Field name made lowercase.
    miercoles = models.CharField(db_column='Miercoles', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    jueves = models.CharField(db_column='Jueves', max_length=1, blank=True, null=True)  # Field name made lowercase.
    viernes = models.CharField(db_column='Viernes', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sabado = models.CharField(db_column='Sabado', max_length=1, blank=True, null=True)  # Field name made lowercase.
    domingo = models.CharField(db_column='Domingo', max_length=1, blank=True, null=True)  # Field name made lowercase.


class Ciudades(models.Model):
    codigo = models.CharField(max_length=5,unique=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    codedi = models.CharField(max_length=5, blank=True, null=True)
    codaduana = models.CharField(db_column='Codaduana', max_length=10, blank=True,null=True)  # Field name made lowercase.
    paises_idinternacional = models.CharField(db_column='Paises_IdInternacional', max_length=5, blank=True,null=True)  # Field name made lowercase.
    estado = models.SmallIntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    fechaactualizado = models.DateTimeField(db_column='FechaActualizado', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.codigo


class Clientes(models.Model):
    codigo = models.IntegerField(unique=True)
    empresa = models.CharField(blank=True,max_length=50)
    razonsocial = models.CharField(max_length=50)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=5, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.SmallIntegerField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=500, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    cpostal = models.CharField(max_length=20, blank=True, null=True)
    ruc = models.CharField(max_length=30, blank=True, null=True)
    contactos = models.TextField(blank=True, null=True)  # This field type is a guess.
    activo = models.CharField(max_length=1, blank=True, null=True)
    vendedor = models.SmallIntegerField(blank=True, null=True)
    refparam = models.SmallIntegerField(blank=True, null=True)
    organizacion = models.SmallIntegerField(blank=True, null=True)
    comagente = models.SmallIntegerField(blank=True, null=True)
    comagenteimport = models.SmallIntegerField(blank=True, null=True)
    comagemarexp = models.SmallIntegerField(blank=True, null=True)
    comagemarimp = models.SmallIntegerField(blank=True, null=True)
    idinternacional = models.CharField(max_length=15, blank=True, null=True)
    prefijoguia = models.CharField(max_length=10, blank=True, null=True)
    comisiontransp = models.FloatField(blank=True, null=True)
    bonifica = models.FloatField(blank=True, null=True)
    critico = models.SmallIntegerField(blank=True, null=True)
    socio = models.CharField(max_length=1, blank=True, null=True)
    tipocli = models.SmallIntegerField(blank=True, null=True)
    ctavta = models.BigIntegerField(blank=True, null=True)
    ctacomp = models.BigIntegerField(blank=True, null=True)
    comageterrexp = models.SmallIntegerField(blank=True, null=True)
    comageterrimp = models.SmallIntegerField(blank=True, null=True)
    refestudio = models.FloatField(blank=True, null=True)
    jurisdiccion = models.SmallIntegerField(blank=True, null=True)
    plazo = models.SmallIntegerField(blank=True, null=True)
    limite = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    giro = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.CharField(max_length=8, blank=True, null=True)
    password = models.CharField(max_length=8, blank=True, null=True)
    facturarle = models.CharField(max_length=1, blank=True, null=True)
    tarifa = models.CharField(max_length=1, blank=True, null=True)
    direccioncia = models.CharField(max_length=50, blank=True, null=True)
    ciudadcia = models.CharField(max_length=40, blank=True, null=True)
    telefonocia = models.CharField(max_length=30, blank=True, null=True)
    faxcia = models.CharField(max_length=30, blank=True, null=True)
    corporativo = models.CharField(max_length=15, blank=True, null=True)
    emailad = models.CharField(db_column='emailAD', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailem = models.CharField(db_column='emailEM', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailea = models.CharField(db_column='emailEA', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailet = models.CharField(db_column='emailET', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailim = models.CharField(db_column='emailIM', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailia = models.CharField(db_column='emailIA', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailit = models.CharField(db_column='emailIT', max_length=500, blank=True, null=True)  # Field name made lowercase.
    fecalta = models.DateTimeField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    despachante = models.CharField(max_length=50, blank=True, null=True)
    motivodespa = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=50, blank=True, null=True)
    motivoage = models.CharField(max_length=50, blank=True, null=True)
    deposito = models.CharField(max_length=50, blank=True, null=True)
    motivodep = models.CharField(max_length=50, blank=True, null=True)
    expectativa = models.TextField(blank=True, null=True)  # This field type is a guess.
    condiciones = models.CharField(max_length=50, blank=True, null=True)
    usuario2 = models.CharField(max_length=8, blank=True, null=True)
    password2 = models.CharField(max_length=8, blank=True, null=True)
    sociomadre = models.IntegerField(blank=True, null=True)
    plazoea = models.SmallIntegerField(db_column='plazoEA', blank=True, null=True)  # Field name made lowercase.
    plazoia = models.SmallIntegerField(db_column='plazoIA', blank=True, null=True)  # Field name made lowercase.
    plazoem = models.SmallIntegerField(db_column='plazoEM', blank=True, null=True)  # Field name made lowercase.
    plazoim = models.SmallIntegerField(db_column='plazoIM', blank=True, null=True)  # Field name made lowercase.
    plazoet = models.SmallIntegerField(db_column='plazoET', blank=True, null=True)  # Field name made lowercase.
    plazoit = models.SmallIntegerField(db_column='plazoIT', blank=True, null=True)  # Field name made lowercase.
    plazomu = models.SmallIntegerField(db_column='plazoMU', blank=True, null=True)  # Field name made lowercase.
    riesgo = models.CharField(max_length=1, blank=True, null=True)
    web = models.CharField(max_length=60, blank=True, null=True)
    contactoim = models.CharField(db_column='ContactoIM', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactoia = models.CharField(db_column='ContactoIA', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactoit = models.CharField(db_column='ContactoIT', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactoem = models.CharField(db_column='ContactoEM', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactoea = models.CharField(db_column='ContactoEA', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactoet = models.CharField(db_column='ContactoET', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactoad = models.CharField(db_column='ContactoAD', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactogral = models.CharField(db_column='ContactoGRAL', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    dicvta = models.CharField(max_length=10, blank=True, null=True)
    diccpa = models.CharField(max_length=10, blank=True, null=True)
    aduana = models.CharField(db_column='Aduana', max_length=20, blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(blank=True, null=True)
    fletesocioim = models.IntegerField(db_column='FleteSocioIM', blank=True, null=True)  # Field name made lowercase.
    fletesocioia = models.IntegerField(db_column='FleteSocioIA', blank=True, null=True)  # Field name made lowercase.
    fletesocioit = models.IntegerField(db_column='FleteSocioIT', blank=True, null=True)  # Field name made lowercase.
    fletesocioem = models.IntegerField(db_column='FleteSocioEM', blank=True, null=True)  # Field name made lowercase.
    fletesocioea = models.IntegerField(db_column='FleteSocioEA', blank=True, null=True)  # Field name made lowercase.
    fletesocioet = models.IntegerField(db_column='FleteSocioET', blank=True, null=True)  # Field name made lowercase.
    direccion2 = models.CharField(db_column='Direccion2', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    origencliente = models.CharField(db_column='OrigenCliente', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    casillero = models.CharField(db_column='Casillero', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    cedulaid = models.CharField(db_column='CedulaID', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
    inscripcion = models.DateTimeField(db_column='Inscripcion', blank=True, null=True)  # Field name made lowercase.
    vtoinscripcion = models.DateTimeField(db_column='VtoInscripcion', blank=True,
                                          null=True)  # Field name made lowercase.
    facturaelectronica = models.CharField(db_column='FacturaElectronica', max_length=1, blank=True,
                                          null=True)  # Field name made lowercase.
    emailfe = models.CharField(db_column='eMailFe', max_length=200, blank=True, null=True)  # Field name made lowercase.
    telefonocasa = models.CharField(db_column='TelefonoCasa', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    telefonocelular = models.CharField(db_column='TelefonoCelular', max_length=30, blank=True,
                                       null=True)  # Field name made lowercase.
    fechacumple = models.DateTimeField(db_column='FechaCumple', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='Municipio', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    inscestadual = models.CharField(db_column='InscEstadual', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    inscmunicipal = models.CharField(db_column='InscMunicipal', max_length=30, blank=True,
                                     null=True)  # Field name made lowercase.
    solocontado = models.CharField(db_column='SoloContado', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    iibbbue = models.CharField(db_column='IIBBBue', max_length=1, blank=True, null=True)  # Field name made lowercase.
    estaxid = models.CharField(db_column='EsTaxID', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enviocc = models.CharField(db_column='EnvioCC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    modoenviocc = models.CharField(db_column='ModoEnvioCC', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadnombre = models.CharField(db_column='CiudadNombre', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    idestado = models.CharField(db_column='IDEstado', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    idpais = models.CharField(db_column='IDPais', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tccambioar = models.DecimalField(db_column='TcCambioAR', max_digits=19, decimal_places=4, blank=True,
                                     null=True)  # Field name made lowercase.
    paiscia = models.CharField(db_column='PaisCia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    encargadocuenta = models.CharField(db_column='EncargadoCuenta', max_length=3, blank=True,
                                       null=True)  # Field name made lowercase.
    bancoproveedor = models.CharField(db_column='BancoProveedor', max_length=250, blank=True,
                                      null=True)  # Field name made lowercase.
    profitea = models.CharField(db_column='ProfitEA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitem = models.CharField(db_column='ProfitEM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitet = models.CharField(db_column='ProfitET', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitia = models.CharField(db_column='ProfitIA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitim = models.CharField(db_column='ProfitIM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitit = models.CharField(db_column='ProfitIT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nroibb = models.CharField(db_column='NroIBB', max_length=20, blank=True, null=True)  # Field name made lowercase.
    interes = models.FloatField(db_column='Interes', blank=True, null=True)  # Field name made lowercase.
    emailcb = models.CharField(db_column='EmailCB', max_length=500, blank=True, null=True)  # Field name made lowercase.
    contactocb = models.CharField(db_column='ContactoCB', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    nroata = models.CharField(db_column='NroATA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    preferido = models.SmallIntegerField(db_column='Preferido', blank=True, null=True)  # Field name made lowercase.
    razonsocial2 = models.CharField(db_column='RazonSocial2', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    emaillg = models.CharField(db_column='EmailLG', max_length=500, blank=True, null=True)  # Field name made lowercase.
    contactolg = models.CharField(db_column='ContactoLG', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    nrointtra = models.CharField(db_column='NroInttra', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    limiteautorizado = models.CharField(db_column='LimiteAutorizado', max_length=50, blank=True,
                                        null=True)  # Field name made lowercase.
    limitedisponible = models.CharField(db_column='LimiteDisponible', max_length=50, blank=True,
                                        null=True)  # Field name made lowercase.
    terminos = models.CharField(db_column='Terminos', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tipoindustria = models.IntegerField(db_column='TipoIndustria', blank=True, null=True)  # Field name made lowercase.
    fechaactualizado = models.DateTimeField(db_column='FechaActualizado', blank=True,
                                            null=True)  # Field name made lowercase.
    coddespachante = models.IntegerField(db_column='CodDespachante', blank=True,
                                         null=True)  # Field name made lowercase.
    codagente = models.IntegerField(db_column='CodAgente', blank=True, null=True)  # Field name made lowercase.
    coddeposito = models.SmallIntegerField(db_column='CodDeposito', blank=True, null=True)  # Field name made lowercase.
    envioiata = models.CharField(db_column='EnvioIATA', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    emailefreight = models.CharField(db_column='EmailEFreight', max_length=200, blank=True,
                                     null=True)  # Field name made lowercase.
    usdenegado = models.CharField(db_column='UsDenegado', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    fechadenegado = models.DateTimeField(db_column='FechaDenegado', blank=True, null=True)  # Field name made lowercase.
    fecharevusdenegado = models.DateTimeField(db_column='FechaRevUsDenegado', blank=True,
                                              null=True)  # Field name made lowercase.
    ctarembvta = models.BigIntegerField(db_column='CtaRembVta', blank=True, null=True)  # Field name made lowercase.
    ctarembcpa = models.BigIntegerField(db_column='CtaRembCpa', blank=True, null=True)  # Field name made lowercase.
    pima = models.CharField(db_column='PIMA', max_length=35, blank=True, null=True)  # Field name made lowercase.
    envelope = models.CharField(db_column='Envelope', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idtipodocumento = models.SmallIntegerField(db_column='idTipoDocumento', blank=True,
                                               null=True)  # Field name made lowercase.
    comportamientoplazo = models.CharField(db_column='ComportamientoPlazo', max_length=1, blank=True,
                                           null=True)  # Field name made lowercase.
    comisioncalcula = models.CharField(db_column='ComisionCalcula', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    bonificacionincluyeiva = models.CharField(db_column='BonificacionIncluyeIVA', max_length=1, blank=True,
                                              null=True)  # Field name made lowercase.
    comisionincluyeiva = models.CharField(db_column='ComisionIncluyeIVA', max_length=1, blank=True,
                                          null=True)  # Field name made lowercase.
    tipocuentabanco = models.CharField(db_column='TipoCuentaBanco', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    numerocuentabanco = models.CharField(db_column='NumeroCuentaBanco', max_length=30, blank=True,
                                         null=True)  # Field name made lowercase.
    tipotransferbanco = models.CharField(db_column='TipoTransferBanco', max_length=3, blank=True,
                                         null=True)  # Field name made lowercase.
    qbli = models.CharField(db_column='QBLi', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cainro = models.CharField(db_column='CaiNro', max_length=50, blank=True, null=True)  # Field name made lowercase.
    caivto = models.DateTimeField(db_column='CaiVto', blank=True, null=True)  # Field name made lowercase.
    coordinador = models.CharField(db_column='Coordinador', max_length=3, blank=True,
                                   null=True)  # Field name made lowercase.
    empresachino = models.CharField(db_column='EmpresaChino', max_length=100, blank=True,
                                    null=True)  # Field name made lowercase.
    direccionchino = models.CharField(db_column='DireccionChino', max_length=50, blank=True,
                                      null=True)  # Field name made lowercase.
    direccionchino2 = models.CharField(db_column='DireccionChino2', max_length=50, blank=True,
                                       null=True)  # Field name made lowercase.
    preferenciales = models.CharField(db_column='Preferenciales', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    plazolg = models.SmallIntegerField(db_column='PlazoLG', blank=True, null=True)  # Field name made lowercase.
    pagodocumentado = models.CharField(db_column='PagoDocumentado', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    formapago = models.SmallIntegerField(db_column='FormaPago', blank=True, null=True)  # Field name made lowercase.
    iibbcap = models.CharField(db_column='IIBBCap', max_length=1, blank=True, null=True)  # Field name made lowercase.
    chequeado = models.CharField(db_column='Chequeado', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    formadepagosat = models.CharField(db_column='FormaDePagoSAT', max_length=2, blank=True,
                                      null=True)  # Field name made lowercase.
    metododepagosat = models.CharField(db_column='MetodoDePagoSAT', max_length=3, blank=True,
                                       null=True)  # Field name made lowercase.
    usocfdisat = models.CharField(db_column='UsoCFDISAT', max_length=3, blank=True,null=True)  # Field name made lowercase.
    webope = models.CharField(db_column='WebOpe', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webser = models.CharField(db_column='WebSer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webord = models.CharField(db_column='WebOrd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webbod = models.CharField(db_column='WebBod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webadm = models.CharField(db_column='WebAdm', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appope = models.CharField(db_column='AppOpe', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appbod = models.CharField(db_column='AppBod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appadm = models.CharField(db_column='AppAdm', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        ordering = ['empresa', ]

    def __str__(self):
        return '%s - %s' % (self.empresa, self.ruc)

    def get_codigo(self):
        ultimo_cliente = Clientes.objects.order_by('-codigo').first()
        if ultimo_cliente:
            ultimo_codigo = int(ultimo_cliente.codigo)
            nuevo_codigo = str(ultimo_codigo + 1)
        else:
            nuevo_codigo = '1'

        return nuevo_codigo


class VSociosComerciales(models.Model):
    codigo = models.IntegerField(unique=True)
    empresa = models.CharField(max_length=50)
    razonsocial = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=5, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.CharField(blank=True, null=True,max_length=500)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=500, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    cpostal = models.CharField(max_length=20, blank=True, null=True)
    ruc = models.CharField(max_length=30, blank=True, null=True)
    contactos = models.TextField(blank=True, null=True)  # This field type is a guess.
    activo = models.CharField(max_length=1, blank=True, null=True)
    vendedor = models.SmallIntegerField(blank=True, null=True)
    refparam = models.SmallIntegerField(blank=True, null=True)
    organizacion = models.SmallIntegerField(blank=True, null=True)
    comagente = models.SmallIntegerField(blank=True, null=True)
    comagenteimport = models.SmallIntegerField(blank=True, null=True)
    comagemarexp = models.SmallIntegerField(blank=True, null=True)
    comagemarimp = models.SmallIntegerField(blank=True, null=True)
    idinternacional = models.CharField(max_length=15, blank=True, null=True)
    prefijoguia = models.CharField(max_length=10, blank=True, null=True)
    comisiontransp = models.FloatField(blank=True, null=True)
    bonifica = models.FloatField(blank=True, null=True)
    critico = models.SmallIntegerField(blank=True, null=True)
    socio = models.CharField(max_length=1, blank=True, null=True)
    tipocli = models.SmallIntegerField(blank=True, null=True)
    ctavta = models.BigIntegerField(blank=True, null=True)
    ctacomp = models.BigIntegerField(blank=True, null=True)
    comageterrexp = models.SmallIntegerField(blank=True, null=True)
    comageterrimp = models.SmallIntegerField(blank=True, null=True)
    refestudio = models.FloatField(blank=True, null=True)
    jurisdiccion = models.SmallIntegerField(blank=True, null=True)
    plazo = models.SmallIntegerField(blank=True, null=True)
    limite = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    giro = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.CharField(max_length=8, blank=True, null=True)
    password = models.CharField(max_length=8, blank=True, null=True)
    facturarle = models.CharField(max_length=1, blank=True, null=True)
    tarifa = models.CharField(max_length=1, blank=True, null=True)
    direccioncia = models.CharField(max_length=50, blank=True, null=True)
    ciudadcia = models.CharField(max_length=40, blank=True, null=True)
    telefonocia = models.CharField(max_length=30, blank=True, null=True)
    faxcia = models.CharField(max_length=30, blank=True, null=True)
    corporativo = models.CharField(max_length=15, blank=True, null=True)
    emailad = models.CharField(db_column='emailAD', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailem = models.CharField(db_column='emailEM', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailea = models.CharField(db_column='emailEA', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailet = models.CharField(db_column='emailET', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailim = models.CharField(db_column='emailIM', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailia = models.CharField(db_column='emailIA', max_length=500, blank=True, null=True)  # Field name made lowercase.
    emailit = models.CharField(db_column='emailIT', max_length=500, blank=True, null=True)  # Field name made lowercase.
    fecalta = models.DateTimeField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    despachante = models.CharField(max_length=50, blank=True, null=True)
    motivodespa = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=50, blank=True, null=True)
    motivoage = models.CharField(max_length=50, blank=True, null=True)
    deposito = models.CharField(max_length=50, blank=True, null=True)
    motivodep = models.CharField(max_length=50, blank=True, null=True)
    expectativa = models.TextField(blank=True, null=True)  # This field type is a guess.
    condiciones = models.CharField(max_length=50, blank=True, null=True)
    usuario2 = models.CharField(max_length=8, blank=True, null=True)
    password2 = models.CharField(max_length=8, blank=True, null=True)
    sociomadre = models.IntegerField(blank=True, null=True)
    plazoea = models.SmallIntegerField(db_column='plazoEA', blank=True, null=True)  # Field name made lowercase.
    plazoia = models.SmallIntegerField(db_column='plazoIA', blank=True, null=True)  # Field name made lowercase.
    plazoem = models.SmallIntegerField(db_column='plazoEM', blank=True, null=True)  # Field name made lowercase.
    plazoim = models.SmallIntegerField(db_column='plazoIM', blank=True, null=True)  # Field name made lowercase.
    plazoet = models.SmallIntegerField(db_column='plazoET', blank=True, null=True)  # Field name made lowercase.
    plazoit = models.SmallIntegerField(db_column='plazoIT', blank=True, null=True)  # Field name made lowercase.
    plazomu = models.SmallIntegerField(db_column='plazoMU', blank=True, null=True)  # Field name made lowercase.
    riesgo = models.CharField(max_length=1, blank=True, null=True)
    web = models.CharField(max_length=60, blank=True, null=True)
    contactoim = models.CharField(db_column='ContactoIM', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactoia = models.CharField(db_column='ContactoIA', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactoit = models.CharField(db_column='ContactoIT', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactoem = models.CharField(db_column='ContactoEM', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactoea = models.CharField(db_column='ContactoEA', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactoet = models.CharField(db_column='ContactoET', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactoad = models.CharField(db_column='ContactoAD', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    contactogral = models.CharField(db_column='ContactoGRAL', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    dicvta = models.CharField(max_length=10, blank=True, null=True)
    diccpa = models.CharField(max_length=10, blank=True, null=True)
    aduana = models.CharField(db_column='Aduana', max_length=20, blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(blank=True, null=True)
    fletesocioim = models.IntegerField(db_column='FleteSocioIM', blank=True, null=True)  # Field name made lowercase.
    fletesocioia = models.IntegerField(db_column='FleteSocioIA', blank=True, null=True)  # Field name made lowercase.
    fletesocioit = models.IntegerField(db_column='FleteSocioIT', blank=True, null=True)  # Field name made lowercase.
    fletesocioem = models.IntegerField(db_column='FleteSocioEM', blank=True, null=True)  # Field name made lowercase.
    fletesocioea = models.IntegerField(db_column='FleteSocioEA', blank=True, null=True)  # Field name made lowercase.
    fletesocioet = models.IntegerField(db_column='FleteSocioET', blank=True, null=True)  # Field name made lowercase.
    direccion2 = models.CharField(db_column='Direccion2', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    origencliente = models.CharField(db_column='OrigenCliente', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    casillero = models.CharField(db_column='Casillero', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    cedulaid = models.CharField(db_column='CedulaID', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
    inscripcion = models.DateTimeField(db_column='Inscripcion', blank=True, null=True)  # Field name made lowercase.
    vtoinscripcion = models.DateTimeField(db_column='VtoInscripcion', blank=True,
                                          null=True)  # Field name made lowercase.
    facturaelectronica = models.CharField(db_column='FacturaElectronica', max_length=1, blank=True,
                                          null=True)  # Field name made lowercase.
    emailfe = models.CharField(db_column='eMailFe', max_length=200, blank=True, null=True)  # Field name made lowercase.
    telefonocasa = models.CharField(db_column='TelefonoCasa', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    telefonocelular = models.CharField(db_column='TelefonoCelular', max_length=30, blank=True,
                                       null=True)  # Field name made lowercase.
    fechacumple = models.DateTimeField(db_column='FechaCumple', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='Municipio', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    inscestadual = models.CharField(db_column='InscEstadual', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    inscmunicipal = models.CharField(db_column='InscMunicipal', max_length=30, blank=True,
                                     null=True)  # Field name made lowercase.
    solocontado = models.CharField(db_column='SoloContado', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    iibbbue = models.CharField(db_column='IIBBBue', max_length=1, blank=True, null=True)  # Field name made lowercase.
    estaxid = models.CharField(db_column='EsTaxID', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enviocc = models.CharField(db_column='EnvioCC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    modoenviocc = models.CharField(db_column='ModoEnvioCC', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    ciudadnombre = models.CharField(db_column='CiudadNombre', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    idestado = models.CharField(db_column='IDEstado', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    idpais = models.CharField(db_column='IDPais', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tccambioar = models.DecimalField(db_column='TcCambioAR', max_digits=19, decimal_places=4, blank=True,
                                     null=True)  # Field name made lowercase.
    paiscia = models.CharField(db_column='PaisCia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    encargadocuenta = models.CharField(db_column='EncargadoCuenta', max_length=3, blank=True,
                                       null=True)  # Field name made lowercase.
    bancoproveedor = models.CharField(db_column='BancoProveedor', max_length=250, blank=True,
                                      null=True)  # Field name made lowercase.
    profitea = models.CharField(db_column='ProfitEA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitem = models.CharField(db_column='ProfitEM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitet = models.CharField(db_column='ProfitET', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitia = models.CharField(db_column='ProfitIA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitim = models.CharField(db_column='ProfitIM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitit = models.CharField(db_column='ProfitIT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nroibb = models.CharField(db_column='NroIBB', max_length=20, blank=True, null=True)  # Field name made lowercase.
    interes = models.FloatField(db_column='Interes', blank=True, null=True)  # Field name made lowercase.
    emailcb = models.CharField(db_column='EmailCB', max_length=500, blank=True, null=True)  # Field name made lowercase.
    contactocb = models.CharField(db_column='ContactoCB', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    nroata = models.CharField(db_column='NroATA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    preferido = models.SmallIntegerField(db_column='Preferido', blank=True, null=True)  # Field name made lowercase.
    razonsocial2 = models.CharField(db_column='RazonSocial2', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    emaillg = models.CharField(db_column='EmailLG', max_length=500, blank=True, null=True)  # Field name made lowercase.
    contactolg = models.CharField(db_column='ContactoLG', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    nrointtra = models.CharField(db_column='NroInttra', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    limiteautorizado = models.CharField(db_column='LimiteAutorizado', max_length=50, blank=True,
                                        null=True)  # Field name made lowercase.
    limitedisponible = models.CharField(db_column='LimiteDisponible', max_length=50, blank=True,
                                        null=True)  # Field name made lowercase.
    terminos = models.CharField(db_column='Terminos', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tipoindustria = models.IntegerField(db_column='TipoIndustria', blank=True, null=True)  # Field name made lowercase.
    fechaactualizado = models.DateTimeField(db_column='FechaActualizado', blank=True,
                                            null=True)  # Field name made lowercase.
    coddespachante = models.IntegerField(db_column='CodDespachante', blank=True,
                                         null=True)  # Field name made lowercase.
    codagente = models.IntegerField(db_column='CodAgente', blank=True, null=True)  # Field name made lowercase.
    coddeposito = models.SmallIntegerField(db_column='CodDeposito', blank=True, null=True)  # Field name made lowercase.
    envioiata = models.CharField(db_column='EnvioIATA', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    emailefreight = models.CharField(db_column='EmailEFreight', max_length=200, blank=True,
                                     null=True)  # Field name made lowercase.
    usdenegado = models.CharField(db_column='UsDenegado', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    fechadenegado = models.DateTimeField(db_column='FechaDenegado', blank=True, null=True)  # Field name made lowercase.
    fecharevusdenegado = models.DateTimeField(db_column='FechaRevUsDenegado', blank=True,
                                              null=True)  # Field name made lowercase.
    ctarembvta = models.BigIntegerField(db_column='CtaRembVta', blank=True, null=True)  # Field name made lowercase.
    ctarembcpa = models.BigIntegerField(db_column='CtaRembCpa', blank=True, null=True)  # Field name made lowercase.
    pima = models.CharField(db_column='PIMA', max_length=35, blank=True, null=True)  # Field name made lowercase.
    envelope = models.CharField(db_column='Envelope', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idtipodocumento = models.SmallIntegerField(db_column='idTipoDocumento', blank=True,
                                               null=True)  # Field name made lowercase.
    comportamientoplazo = models.CharField(db_column='ComportamientoPlazo', max_length=1, blank=True,
                                           null=True)  # Field name made lowercase.
    comisioncalcula = models.CharField(db_column='ComisionCalcula', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    bonificacionincluyeiva = models.CharField(db_column='BonificacionIncluyeIVA', max_length=1, blank=True,
                                              null=True)  # Field name made lowercase.
    comisionincluyeiva = models.CharField(db_column='ComisionIncluyeIVA', max_length=1, blank=True,
                                          null=True)  # Field name made lowercase.
    tipocuentabanco = models.CharField(db_column='TipoCuentaBanco', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    numerocuentabanco = models.CharField(db_column='NumeroCuentaBanco', max_length=30, blank=True,
                                         null=True)  # Field name made lowercase.
    tipotransferbanco = models.CharField(db_column='TipoTransferBanco', max_length=3, blank=True,
                                         null=True)  # Field name made lowercase.
    qbli = models.CharField(db_column='QBLi', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cainro = models.CharField(db_column='CaiNro', max_length=50, blank=True, null=True)  # Field name made lowercase.
    caivto = models.DateTimeField(db_column='CaiVto', blank=True, null=True)  # Field name made lowercase.
    coordinador = models.CharField(db_column='Coordinador', max_length=3, blank=True,
                                   null=True)  # Field name made lowercase.
    empresachino = models.CharField(db_column='EmpresaChino', max_length=100, blank=True,
                                    null=True)  # Field name made lowercase.
    direccionchino = models.CharField(db_column='DireccionChino', max_length=50, blank=True,
                                      null=True)  # Field name made lowercase.
    direccionchino2 = models.CharField(db_column='DireccionChino2', max_length=50, blank=True,
                                       null=True)  # Field name made lowercase.
    preferenciales = models.CharField(db_column='Preferenciales', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    plazolg = models.SmallIntegerField(db_column='PlazoLG', blank=True, null=True)  # Field name made lowercase.
    pagodocumentado = models.CharField(db_column='PagoDocumentado', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    formapago = models.SmallIntegerField(db_column='FormaPago', blank=True, null=True)  # Field name made lowercase.
    iibbcap = models.CharField(db_column='IIBBCap', max_length=1, blank=True, null=True)  # Field name made lowercase.
    chequeado = models.CharField(db_column='Chequeado', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    formadepagosat = models.CharField(db_column='FormaDePagoSAT', max_length=2, blank=True,
                                      null=True)  # Field name made lowercase.
    metododepagosat = models.CharField(db_column='MetodoDePagoSAT', max_length=3, blank=True,
                                       null=True)  # Field name made lowercase.
    usocfdisat = models.CharField(db_column='UsoCFDISAT', max_length=3, blank=True,null=True)  # Field name made lowercase.
    webope = models.CharField(db_column='WebOpe', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webser = models.CharField(db_column='WebSer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webord = models.CharField(db_column='WebOrd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webbod = models.CharField(db_column='WebBod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webadm = models.CharField(db_column='WebAdm', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appope = models.CharField(db_column='AppOpe', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appbod = models.CharField(db_column='AppBod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appadm = models.CharField(db_column='AppAdm', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        ordering = ['empresa', ]
        db_table = 'VSociosComerciales2'

    def __str__(self):
        return '%s - %s' % (self.empresa, self.ruc)


class Dtproperties(models.Model):
    objectid = models.IntegerField(blank=True, null=True)
    property = models.CharField(max_length=64)
    value = models.CharField(max_length=255, blank=True, null=True)
    lvalue = models.BinaryField(blank=True, null=True)
    version = models.IntegerField()
    uvalue = models.CharField(max_length=255, blank=True, null=True)


class Edimonedas(models.Model):
    agente = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    codorigen = models.SmallIntegerField(blank=True, null=True)
    coddestino = models.SmallIntegerField(blank=True, null=True)


class Ediproductos(models.Model):
    agente = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    codorigen = models.SmallIntegerField(blank=True, null=True)
    coddestino = models.SmallIntegerField(blank=True, null=True)


class Ediservicios(models.Model):
    agente = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    codorigen = models.SmallIntegerField(blank=True, null=True)
    coddestino = models.SmallIntegerField(blank=True, null=True)


class Edisocios(models.Model):
    agente = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    codorigen = models.IntegerField(blank=True, null=True)
    coddestino = models.IntegerField(blank=True, null=True)


class Guias(models.Model):
    transportista = models.IntegerField(blank=True, null=True)
    prefijo = models.CharField(max_length=10, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    estado = models.SmallIntegerField(blank=True, null=True)
    refmaster = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(blank=True, null=True)
    sucursal = models.SmallIntegerField(db_column='Sucursal', blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.


class VGrillaGuias(models.Model):
    transportista = models.IntegerField(blank=True, null=True)
    empresa = models.CharField(db_column="nom_empresa",max_length=250,blank=True, null=True)
    posicion = models.CharField(db_column="posicion",max_length=250,blank=True, null=True)
    guia = models.CharField(max_length=25, blank=True, null=True)
    prefijo = models.CharField(max_length=10, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    estado = models.CharField(db_column='estados',max_length=150,blank=True, null=True)
    refmaster = models.IntegerField(db_column='referencia',blank=True, null=True)
    tipo = models.CharField(max_length=1,db_column='tipodoc', blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(blank=True, null=True)
    sucursal = models.SmallIntegerField(db_column='Sucursal', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VGrillaGuias'


class Paises(models.Model):
    nombre = models.CharField(max_length=50)
    continente = models.SmallIntegerField(blank=True, null=True)
    iata = models.SmallIntegerField(blank=True, null=True)
    idinternacional = models.CharField(max_length=3, blank=True, null=True)
    cuit = models.CharField(max_length=20, blank=True, null=True)
    cartelef = models.SmallIntegerField(blank=True, null=True)
    edi = models.CharField(db_column='EDI', max_length=3, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return  self.nombre


class Productos(models.Model):

    codigo = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    peligroso = models.SmallIntegerField(blank=True, null=True)
    familia = models.SmallIntegerField(blank=True, null=True)
    valioso = models.SmallIntegerField(blank=True, null=True)
    perecedero = models.SmallIntegerField(blank=True, null=True)
    nrocomm = models.IntegerField(blank=True, null=True)
    corporativo = models.CharField(max_length=10, blank=True, null=True)
    schedulebnumber = models.CharField(db_column='ScheduleBNumber', max_length=12, blank=True,
                                       null=True)  # Field name made lowercase.
    class_field = models.CharField(db_column='Class', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    un = models.CharField(db_column='UN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    packing = models.CharField(db_column='Packing', max_length=20, blank=True, null=True)  # Field name made lowercase.
    subrisk = models.CharField(db_column='SubRisk', max_length=20, blank=True, null=True)  # Field name made lowercase.
    aduanaentrada = models.CharField(db_column='AduanaEntrada', max_length=20, blank=True,
                                     null=True)  # Field name made lowercase.
    aduanasalida = models.CharField(db_column='AduanaSalida', max_length=20, blank=True,
                                    null=True)  # Field name made lowercase.
    temperatura = models.FloatField(db_column='Temperatura', blank=True, null=True)  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    hazardpage = models.CharField(db_column='HazardPage', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    hazardcodever = models.CharField(db_column='HazardCodeVer', max_length=20, blank=True,
                                     null=True)  # Field name made lowercase.
    ems = models.CharField(db_column='EMS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    termcard = models.CharField(db_column='TermCard', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    imocode2 = models.CharField(db_column='ImoCode2', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    imocode3 = models.CharField(db_column='ImoCode3', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    psn = models.CharField(db_column='PSN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechaactualizado = models.DateTimeField(db_column='FechaActualizado', blank=True,
                                            null=True)  # Field name made lowercase.
    ncm = models.CharField(db_column='NCM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shc = models.CharField(db_column='SHC', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dgc = models.CharField(db_column='DGC', max_length=100, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.pk:
            self.codigo = Productos.objects.all().order_by('-codigo')[0].codigo + 1
        super().save(*args, **kwargs)  # Guarda el objeto



class Sysregisedits(models.Model):
    numerolic = models.IntegerField(db_column='NumeroLic', unique=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    equipo = models.CharField(db_column='Equipo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    registro = models.CharField(db_column='Registro', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
    vigencia = models.DateTimeField(db_column='Vigencia', blank=True, null=True)  # Field name made lowercase.
    estado = models.SmallIntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.


class Textos(models.Model):
    deposito = models.TextField(blank=True, null=True)  # This field type is a guess.
    agente = models.TextField(blank=True, null=True)  # This field type is a guess.
    cliente = models.TextField(blank=True, null=True)  # This field type is a guess.
    cotizaim = models.TextField(blank=True, null=True)  # This field type is a guess.
    cotizaia = models.TextField(blank=True, null=True)  # This field type is a guess.
    cotizaem = models.TextField(blank=True, null=True)  # This field type is a guess.
    cotizaea = models.TextField(blank=True, null=True)  # This field type is a guess.
    clienteia = models.TextField(blank=True, null=True)  # This field type is a guess.
    clienteit = models.TextField(blank=True, null=True)  # This field type is a guess.
    cotizait = models.TextField(blank=True, null=True)  # This field type is a guess.
    cotizaet = models.TextField(blank=True, null=True)  # This field type is a guess.
    clienteexa = models.TextField(blank=True, null=True)  # This field type is a guess.
    clienteexm = models.TextField(blank=True, null=True)  # This field type is a guess.
    clienteext = models.TextField(blank=True, null=True)  # This field type is a guess.
    cotgenerica = models.TextField(blank=True, null=True)  # This field type is a guess.
    seguircli = models.TextField(blank=True, null=True)  # This field type is a guess.
    seguirclii = models.TextField(blank=True, null=True)  # This field type is a guess.
    seguirage = models.TextField(blank=True, null=True)  # This field type is a guess.
    seguiragei = models.TextField(blank=True, null=True)  # This field type is a guess.
    general = models.TextField(blank=True, null=True)  # This field type is a guess.

    booking = models.TextField(db_column='Booking', blank=True,
                               null=True)  # Field name made lowercase. This field type is a guess.
    textoaging = models.TextField(db_column='TextoAging', blank=True,
                                  null=True)  # Field name made lowercase. This field type is a guess.
    textoestadocuenta = models.TextField(db_column='TextoEstadoCuenta', blank=True,
                                         null=True)  # Field name made lowercase. This field type is a guess.


from inspect import getmembers
from auditlog.registry import auditlog
from mantenimientos import models


tablas = getmembers(models)
for t in tablas:
    try:
        auditlog.register(t[1], serialize_data=True)
    except Exception as e:
        pass