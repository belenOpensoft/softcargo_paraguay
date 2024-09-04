# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AgendaAccreclamos(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    accion = models.TextField(blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agenda.AccReclamos'


class AgendaDescreclamos(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agenda.Descreclamos'


class AgendaFuentereclamo(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=19, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agenda.FuenteReclamo'


class AgendaOrganize(models.Model):
    fecha = models.CharField(max_length=19, blank=True, null=True)
    begintime = models.CharField(max_length=5, blank=True, null=True)
    endtime = models.CharField(max_length=5, blank=True, null=True)
    horacompleta = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    usuario = models.CharField(max_length=11, blank=True, null=True)
    sociocomercial = models.SmallIntegerField(blank=True, null=True)
    tipotarea = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=9, blank=True, null=True)
    aviso = models.CharField(max_length=7, blank=True, null=True)
    comentarios = models.CharField(blank=True, null=True)
    origen = models.CharField(db_column='Origen', blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agenda.Organize'


class AgendaReclamos(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    sociocomercial = models.SmallIntegerField(blank=True, null=True)
    tiporeclamo = models.CharField(max_length=9, blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    fuentereclamo = models.CharField(max_length=19, blank=True, null=True)
    nombrereclama = models.CharField(max_length=29, blank=True, null=True)
    usuario = models.CharField(max_length=9, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    asignado = models.CharField(max_length=9, blank=True, null=True)
    correctiva = models.CharField(db_column='Correctiva', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vto = models.CharField(db_column='Vto', max_length=19, blank=True, null=True)  # Field name made lowercase.
    accioncorrectiva = models.CharField(db_column='AccionCorrectiva', max_length=172, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agenda.Reclamos'


class AgendaStatus(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=10, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agenda.Status'


class AgendaStatusreclamo(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=10, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agenda.StatusReclamo'


class AgendaTareas(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=10, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agenda.Tareas'


class AgendaTiporeclamo(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=20, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agenda.TipoReclamo'


class Actividades(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Actividades'


class Attachsocio(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    archivo = models.CharField(db_column='Archivo', max_length=250, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=3, blank=True, null=True)  # Field name made lowercase.
    web = models.CharField(db_column='Web', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.AttachSocio'


class Bancos(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=15, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=3, blank=True, null=True)  # Field name made lowercase.
    edi = models.CharField(db_column='EDI', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=7, blank=True, null=True)  # Field name made lowercase.
    nombrechino = models.CharField(db_column='NombreChino', blank=True, null=True)  # Field name made lowercase.
    rut = models.CharField(db_column='RUT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Bancos'


class Bandejaefreight(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    de = models.CharField(db_column='De', blank=True, null=True)  # Field name made lowercase.
    asunto = models.CharField(db_column='Asunto', blank=True, null=True)  # Field name made lowercase.
    mensaje = models.CharField(db_column='Mensaje', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    fechaprocesado = models.CharField(db_column='FechaProcesado', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.BandejaEFreight'


class Budget(models.Model):
    codigo = models.SmallIntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    ano = models.IntegerField(db_column='Ano', blank=True, null=True)  # Field name made lowercase.
    ventat1 = models.DecimalField(db_column='VentaT1', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ventat2 = models.DecimalField(db_column='VentaT2', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ventat3 = models.DecimalField(db_column='VentaT3', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ventat4 = models.DecimalField(db_column='VentaT4', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pesoeat1 = models.DecimalField(db_column='PesoEAT1', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoeat2 = models.DecimalField(db_column='PesoEAT2', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoeat3 = models.DecimalField(db_column='PesoEAT3', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoeat4 = models.DecimalField(db_column='PesoEAT4', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoiat1 = models.DecimalField(db_column='PesoIAT1', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoiat2 = models.DecimalField(db_column='PesoIAT2', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoiat3 = models.DecimalField(db_column='PesoIAT3', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoiat4 = models.DecimalField(db_column='PesoIAT4', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    teusemt1 = models.IntegerField(db_column='TeusEMT1', blank=True, null=True)  # Field name made lowercase.
    teusemt2 = models.IntegerField(db_column='TeusEMT2', blank=True, null=True)  # Field name made lowercase.
    teusemt3 = models.IntegerField(db_column='TeusEMT3', blank=True, null=True)  # Field name made lowercase.
    teusemt4 = models.IntegerField(db_column='TeusEMT4', blank=True, null=True)  # Field name made lowercase.
    teusimt1 = models.IntegerField(db_column='TeusIMT1', blank=True, null=True)  # Field name made lowercase.
    teusimt2 = models.IntegerField(db_column='TeusIMT2', blank=True, null=True)  # Field name made lowercase.
    teusimt3 = models.IntegerField(db_column='TeusIMT3', blank=True, null=True)  # Field name made lowercase.
    teusimt4 = models.IntegerField(db_column='TeusIMT4', blank=True, null=True)  # Field name made lowercase.
    lclemt1 = models.DecimalField(db_column='LclEMT1', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    lclemt2 = models.DecimalField(db_column='LclEMT2', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    lclemt3 = models.DecimalField(db_column='LclEMT3', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    lclemt4 = models.DecimalField(db_column='LclEMT4', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    lclimt1 = models.DecimalField(db_column='LclIMT1', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    lclimt2 = models.DecimalField(db_column='LclIMT2', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    lclimt3 = models.DecimalField(db_column='LclIMT3', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    lclimt4 = models.DecimalField(db_column='LclIMT4', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoett1 = models.DecimalField(db_column='PesoETT1', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoett2 = models.DecimalField(db_column='PesoETT2', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoett3 = models.DecimalField(db_column='PesoETT3', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoett4 = models.DecimalField(db_column='PesoETT4', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoitt1 = models.DecimalField(db_column='PesoITT1', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoitt2 = models.DecimalField(db_column='PesoITT2', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoitt3 = models.DecimalField(db_column='PesoITT3', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    pesoitt4 = models.DecimalField(db_column='PesoITT4', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Budget'


class Claveposicionmm(models.Model):
    posicion = models.CharField(db_column='Posicion', max_length=9, blank=True, null=True)  # Field name made lowercase.
    numeroorden = models.IntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.ClavePosicionMM'


class Clicontactos(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    cargo = models.CharField(db_column='Cargo', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', blank=True, null=True)  # Field name made lowercase.
    celular = models.CharField(db_column='Celular', blank=True, null=True)  # Field name made lowercase.
    skype = models.CharField(db_column='Skype', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.CliContactos'


class Clifaxes(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=3, blank=True, null=True)  # Field name made lowercase.
    asunto = models.CharField(db_column='Asunto', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.CliFaxes'


class Clireldep(models.Model):
    idcli = models.CharField(db_column='IDCli', blank=True, null=True)  # Field name made lowercase.
    idrep = models.CharField(db_column='IDRep', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.CliRelDep'


class Clirelacion(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    relacionado = models.CharField(db_column='Relacionado', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.CliRelacion'


class Clitipodocumento(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.CliTipoDocumento'


class Clitipooperacion(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    tipooperacion = models.CharField(db_column='TipoOperacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.CliTipoOperacion'


class Clitraficos(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    trafico = models.CharField(db_column='Trafico', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.CliTraficos'


class Config(models.Model):
    dato = models.IntegerField(blank=True, null=True)
    dato2 = models.IntegerField(blank=True, null=True)
    detalle = models.CharField(max_length=29, blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '.Config'


class Contratoscli(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    numcontrato = models.CharField(db_column='NumContrato', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.ContratosCli'


class Depositos(models.Model):
    codigo = models.IntegerField(blank=True, null=True)
    empresa = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=29, blank=True, null=True)
    localidad = models.CharField(max_length=10, blank=True, null=True)
    ciudad = models.CharField(max_length=3, blank=True, null=True)
    pais = models.CharField(max_length=7, blank=True, null=True)
    telefono = models.CharField(max_length=8, blank=True, null=True)
    fax = models.CharField(max_length=3, blank=True, null=True)
    email = models.CharField(max_length=3, blank=True, null=True)
    cpostal = models.CharField(max_length=3, blank=True, null=True)
    observaciones = models.CharField(max_length=3, blank=True, null=True)
    contactos = models.CharField(max_length=3, blank=True, null=True)
    ruc = models.CharField(max_length=3, blank=True, null=True)
    aduana = models.CharField(db_column='Aduana', max_length=3, blank=True, null=True)  # Field name made lowercase.
    empresachino = models.CharField(db_column='EmpresaChino', max_length=3, blank=True, null=True)  # Field name made lowercase.
    direccionchino = models.CharField(db_column='DireccionChino', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Depositos'


class Direccionentregas(models.Model):
    codigo = models.CharField(blank=True, null=True)
    iddireccion = models.CharField(blank=True, null=True)
    direccion = models.CharField(blank=True, null=True)
    localidad = models.CharField(blank=True, null=True)
    cpostal = models.CharField(blank=True, null=True)
    pais = models.CharField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True)
    telefono2 = models.CharField(blank=True, null=True)
    fax = models.CharField(blank=True, null=True)
    fax2 = models.CharField(blank=True, null=True)
    contacto = models.CharField(db_column='Contacto', blank=True, null=True)  # Field name made lowercase.
    centrocosto = models.CharField(db_column='CentroCosto', blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.DireccionEntregas'


class Empresa(models.Model):
    dnombre = models.CharField(max_length=20, blank=True, null=True)
    drazonsocial = models.CharField(max_length=20, blank=True, null=True)
    ddireccion = models.CharField(max_length=20, blank=True, null=True)
    dtelefono = models.CharField(max_length=13, blank=True, null=True)
    dlocalidad = models.CharField(max_length=10, blank=True, null=True)
    dfax = models.CharField(max_length=13, blank=True, null=True)
    druc = models.BigIntegerField(blank=True, null=True)
    dcpostal = models.IntegerField(blank=True, null=True)
    dvtodgi = models.CharField(max_length=19, blank=True, null=True)
    dvtobps = models.CharField(max_length=19, blank=True, null=True)
    dvtobse = models.CharField(max_length=19, blank=True, null=True)
    dnroiata = models.CharField(max_length=3, blank=True, null=True)
    dciudadbase = models.CharField(max_length=3, blank=True, null=True)
    dnomciudadbase = models.CharField(max_length=10, blank=True, null=True)
    usastock = models.IntegerField(blank=True, null=True)
    usaposicion = models.IntegerField(blank=True, null=True)
    cass = models.CharField(max_length=3, blank=True, null=True)
    pasagastos = models.IntegerField(blank=True, null=True)
    vaciudad = models.IntegerField(blank=True, null=True)
    nroata = models.CharField(max_length=3, blank=True, null=True)
    prefijohouse = models.CharField(max_length=3, blank=True, null=True)
    heredaposhijo = models.IntegerField(blank=True, null=True)
    usacontrolhawb = models.IntegerField(db_column='usacontrolHAWB', blank=True, null=True)  # Field name made lowercase.
    servidores = models.CharField(max_length=1, blank=True, null=True)
    graboimagen = models.IntegerField(blank=True, null=True)
    unidadpeso = models.CharField(max_length=1, blank=True, null=True)
    multiplestarifas = models.CharField(max_length=1, blank=True, null=True)
    verarbitrajes = models.CharField(db_column='Verarbitrajes', max_length=1, blank=True, null=True)  # Field name made lowercase.
    correo = models.CharField(max_length=1, blank=True, null=True)
    ultragestion = models.CharField(max_length=1, blank=True, null=True)
    formatofecha = models.CharField(max_length=10, blank=True, null=True)
    sucursalenposicion = models.CharField(db_column='SucursalEnPosicion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bloqueoarbitraje = models.CharField(db_column='BloqueoArbitraje', max_length=1, blank=True, null=True)  # Field name made lowercase.
    costosengastos = models.CharField(db_column='CostosEnGastos', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=3, blank=True, null=True)  # Field name made lowercase.
    iata = models.CharField(db_column='Iata', max_length=1, blank=True, null=True)  # Field name made lowercase.
    onlineorders = models.CharField(db_column='OnlineOrders', max_length=1, blank=True, null=True)  # Field name made lowercase.
    determinounidades = models.CharField(db_column='DeterminoUnidades', max_length=1, blank=True, null=True)  # Field name made lowercase.
    confirmaritemsembarcar = models.CharField(db_column='ConfirmarItemsEmbarcar', max_length=1, blank=True, null=True)  # Field name made lowercase.
    aesactivo = models.CharField(db_column='AESActivo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    brokernumber = models.CharField(db_column='BrokerNumber', blank=True, null=True)  # Field name made lowercase.
    transmitterid = models.CharField(db_column='TransmitterID', blank=True, null=True)  # Field name made lowercase.
    transmitteridtype = models.CharField(db_column='TransmitterIDType', blank=True, null=True)  # Field name made lowercase.
    aes_option = models.CharField(db_column='AES_Option', blank=True, null=True)  # Field name made lowercase.
    datacenterportcode = models.CharField(db_column='DataCenterPortCode', blank=True, null=True)  # Field name made lowercase.
    sixdigitpassword = models.CharField(db_column='SixDigitPassword', blank=True, null=True)  # Field name made lowercase.
    eightdigitpassword = models.CharField(db_column='EightDigitPassword', blank=True, null=True)  # Field name made lowercase.
    remotenumber = models.CharField(db_column='RemoteNumber', blank=True, null=True)  # Field name made lowercase.
    xidnumber = models.CharField(db_column='XIDNumber', blank=True, null=True)  # Field name made lowercase.
    transmittertype = models.CharField(db_column='TransmitterType', blank=True, null=True)  # Field name made lowercase.
    transmissionnumber = models.CharField(db_column='TransmissionNumber', blank=True, null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=3, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=3, blank=True, null=True)  # Field name made lowercase.
    nextsednumber = models.CharField(db_column='NextSEDNumber', blank=True, null=True)  # Field name made lowercase.
    abiofficecode = models.CharField(db_column='ABIOfficeCode', blank=True, null=True)  # Field name made lowercase.
    support_pms = models.IntegerField(db_column='Support_PMS', blank=True, null=True)  # Field name made lowercase.
    statementtype = models.CharField(db_column='StatementType', blank=True, null=True)  # Field name made lowercase.
    processach_ap = models.IntegerField(db_column='ProcessACH_AP', blank=True, null=True)  # Field name made lowercase.
    payersunitnumber = models.CharField(db_column='PayersUnitNumber', blank=True, null=True)  # Field name made lowercase.
    checkseb = models.IntegerField(db_column='CheckSEB', blank=True, null=True)  # Field name made lowercase.
    bondproducernumber = models.CharField(db_column='BondProducerNumber', blank=True, null=True)  # Field name made lowercase.
    checkpoa = models.IntegerField(db_column='CheckPOA', blank=True, null=True)  # Field name made lowercase.
    systemtimezone = models.CharField(db_column='SystemTimeZone', blank=True, null=True)  # Field name made lowercase.
    highwaypermitfeeschargecode = models.CharField(db_column='HighwayPermitFeesChargeCode', blank=True, null=True)  # Field name made lowercase.
    userfeeschargecode = models.CharField(db_column='UserFeesChargeCode', blank=True, null=True)  # Field name made lowercase.
    freightchargecode = models.CharField(db_column='FreightChargeCode', blank=True, null=True)  # Field name made lowercase.
    driverfeeschargecode = models.CharField(db_column='DriverFeesChargeCode', blank=True, null=True)  # Field name made lowercase.
    otherfeeschargecode = models.CharField(db_column='OtherFeesChargeCode', blank=True, null=True)  # Field name made lowercase.
    highwayfeevendornumber = models.CharField(db_column='HighwayFeeVendorNumber', blank=True, null=True)  # Field name made lowercase.
    userfeesvendornumber = models.CharField(db_column='UserFeesVendorNumber', blank=True, null=True)  # Field name made lowercase.
    driverfeesvendornumber = models.CharField(db_column='DriverFeesVendorNumber', blank=True, null=True)  # Field name made lowercase.
    freightchecksvendornumber = models.CharField(db_column='FreightChecksVendorNumber', blank=True, null=True)  # Field name made lowercase.
    defaultcustomercode = models.CharField(db_column='DefaultCustomerCode', blank=True, null=True)  # Field name made lowercase.
    dwebsite = models.CharField(db_column='dWebSite', max_length=3, blank=True, null=True)  # Field name made lowercase.
    gastoscondetalle = models.CharField(db_column='GastosConDetalle', max_length=1, blank=True, null=True)  # Field name made lowercase.
    posicionporsucursal = models.CharField(db_column='PosicionPorSucursal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=3, blank=True, null=True)  # Field name made lowercase.
    controlcters = models.CharField(db_column='ControlCters', max_length=1, blank=True, null=True)  # Field name made lowercase.
    solocomprasdefinitivas = models.CharField(db_column='SoloComprasDefinitivas', max_length=1, blank=True, null=True)  # Field name made lowercase.
    multiempresa = models.CharField(db_column='MultiEmpresa', max_length=1, blank=True, null=True)  # Field name made lowercase.
    origendestino = models.CharField(db_column='OrigenDestino', max_length=1, blank=True, null=True)  # Field name made lowercase.
    usamsoffice = models.CharField(db_column='UsaMSOffice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    codigosat = models.CharField(db_column='CodigoSAT', max_length=3, blank=True, null=True)  # Field name made lowercase.
    consecutivosat = models.IntegerField(db_column='ConsecutivoSAT', blank=True, null=True)  # Field name made lowercase.
    usacodigocorp = models.CharField(db_column='UsaCodigoCorp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    solicitudpagoalgrabar = models.CharField(db_column='SolicitudPagoalGrabar', max_length=1, blank=True, null=True)  # Field name made lowercase.
    totall = models.SmallIntegerField(db_column='TotalL', blank=True, null=True)  # Field name made lowercase.
    sc = models.CharField(db_column='SC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nrointtra = models.CharField(db_column='NroInttra', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cantdecimalesea = models.SmallIntegerField(db_column='CantDecimalesEA', blank=True, null=True)  # Field name made lowercase.
    intercomex = models.CharField(db_column='Intercomex', max_length=1, blank=True, null=True)  # Field name made lowercase.
    numempresa = models.IntegerField(db_column='NumEmpresa', blank=True, null=True)  # Field name made lowercase.
    statusseguimiento = models.CharField(db_column='StatusSeguimiento', max_length=9, blank=True, null=True)  # Field name made lowercase.
    campoactividadobligatorio = models.CharField(db_column='CampoActividadObligatorio', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fuentemail = models.CharField(db_column='FuenteMail', max_length=11, blank=True, null=True)  # Field name made lowercase.
    fuentetamanomail = models.IntegerField(db_column='FuenteTamanoMail', blank=True, null=True)  # Field name made lowercase.
    tsa = models.CharField(db_column='TSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    smtp = models.CharField(db_column='SMTP', max_length=3, blank=True, null=True)  # Field name made lowercase.
    port = models.IntegerField(db_column='Port', blank=True, null=True)  # Field name made lowercase.
    datosfemsa = models.CharField(db_column='DatosFEMSA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    controldefechas = models.CharField(db_column='ControlDeFechas', max_length=1, blank=True, null=True)  # Field name made lowercase.
    asuntomailresumido = models.CharField(db_column='AsuntoMailResumido', max_length=1, blank=True, null=True)  # Field name made lowercase.
    controlcterhouse = models.CharField(db_column='ControlCterHouse', max_length=1, blank=True, null=True)  # Field name made lowercase.
    anpworks = models.CharField(db_column='ANPWorks', max_length=1, blank=True, null=True)  # Field name made lowercase.
    usacodigoedi = models.CharField(db_column='UsaCodigoEDI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    usacostoinicial = models.CharField(db_column='UsaCostoInicial', max_length=1, blank=True, null=True)  # Field name made lowercase.
    urltracking = models.CharField(db_column='URLTracking', max_length=3, blank=True, null=True)  # Field name made lowercase.
    usersmtp = models.CharField(db_column='UserSMTP', max_length=3, blank=True, null=True)  # Field name made lowercase.
    passsmtp = models.CharField(db_column='PassSMTP', max_length=3, blank=True, null=True)  # Field name made lowercase.
    emailrespuesta = models.CharField(db_column='EmailRespuesta', max_length=3, blank=True, null=True)  # Field name made lowercase.
    selclienteconsolidar = models.CharField(db_column='SelClienteConsolidar', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nromaersk = models.CharField(db_column='NroMaersk', max_length=3, blank=True, null=True)  # Field name made lowercase.
    utilizacartaaprobacion = models.CharField(db_column='UtilizaCartaAprobacion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nrosafmarine = models.CharField(db_column='NroSafmarine', max_length=3, blank=True, null=True)  # Field name made lowercase.
    nomempresaawb = models.CharField(db_column='NomEmpresaAWB', max_length=1, blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    impsegcotivencida = models.CharField(db_column='ImpSegCotiVencida', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lugarnotify = models.CharField(db_column='LugarNotify', max_length=1, blank=True, null=True)  # Field name made lowercase.
    largominpassword = models.IntegerField(db_column='LargoMinPassword', blank=True, null=True)  # Field name made lowercase.
    complejidad = models.CharField(db_column='Complejidad', max_length=8, blank=True, null=True)  # Field name made lowercase.
    intentosfallidos = models.IntegerField(db_column='IntentosFallidos', blank=True, null=True)  # Field name made lowercase.
    tiempoinactividad = models.IntegerField(db_column='TiempoInactividad', blank=True, null=True)  # Field name made lowercase.
    bloqueoriesgoso = models.CharField(db_column='BloqueoRiesgoso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    usacontrolseguro = models.CharField(db_column='UsaControlSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dnombrechino = models.CharField(db_column='dNombreChino', blank=True, null=True)  # Field name made lowercase.
    stockawbempresa = models.IntegerField(db_column='StockAWBEmpresa', blank=True, null=True)  # Field name made lowercase.
    posicionmes = models.CharField(db_column='PosicionMes', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emitebloriginal = models.CharField(db_column='EmiteBLOriginal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cantdecimalespeso = models.IntegerField(db_column='CantDecimalesPeso', blank=True, null=True)  # Field name made lowercase.
    dashboardeawb = models.CharField(db_column='DashboardEAWB', max_length=1, blank=True, null=True)  # Field name made lowercase.
    binaryattach = models.IntegerField(db_column='BinaryAttach', blank=True, null=True)  # Field name made lowercase.
    campotraficoobligatorio = models.CharField(db_column='CampoTraficoObligatorio', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Empresa'


class Estados(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=3, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=6, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Estados'


class Formapago(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.FormaPago'


class Grupos(models.Model):
    grupo = models.CharField(blank=True, null=True)
    detalle = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '.Grupos'


class Guiascentro(models.Model):
    transportista = models.CharField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    prefijo = models.CharField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    refmaster = models.CharField(db_column='RefMaster', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.GuiasCentro'


class Houses(models.Model):
    contador = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    em = models.DecimalField(db_column='EM', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    et = models.DecimalField(db_column='ET', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '.Houses'


class Interfaces(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    tipointerface = models.CharField(db_column='TipoInterface', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    formato = models.CharField(db_column='Formato', blank=True, null=True)  # Field name made lowercase.
    cabezal = models.CharField(db_column='Cabezal', blank=True, null=True)  # Field name made lowercase.
    delimitador = models.CharField(db_column='Delimitador', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Interfaces'


class Interfacesatributos(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombrecampo = models.CharField(db_column='NombreCampo', blank=True, null=True)  # Field name made lowercase.
    entradato = models.CharField(db_column='EntraDato', blank=True, null=True)  # Field name made lowercase.
    saledato = models.CharField(db_column='SaleDato', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.InterfacesAtributos'


class Interfacesdetalle(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombrecampo = models.CharField(db_column='NombreCampo', blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.
    tipodato = models.CharField(db_column='TipoDato', blank=True, null=True)  # Field name made lowercase.
    sube = models.CharField(db_column='Sube', blank=True, null=True)  # Field name made lowercase.
    nombrecomo = models.CharField(db_column='NombreComo', blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', blank=True, null=True)  # Field name made lowercase.
    formato = models.CharField(db_column='Formato', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.InterfacesDetalle'


class Llegadas(models.Model):
    vapor = models.CharField(db_column='Vapor', blank=True, null=True)  # Field name made lowercase.
    llegada = models.CharField(db_column='Llegada', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', blank=True, null=True)  # Field name made lowercase.
    semana = models.CharField(db_column='Semana', blank=True, null=True)  # Field name made lowercase.
    fechastacking = models.CharField(db_column='FechaStacking', blank=True, null=True)  # Field name made lowercase.
    horastacking = models.CharField(db_column='HoraStacking', blank=True, null=True)  # Field name made lowercase.
    fechacutoff = models.CharField(db_column='FechaCutOff', blank=True, null=True)  # Field name made lowercase.
    horacutoff = models.CharField(db_column='HoraCutOff', blank=True, null=True)  # Field name made lowercase.
    fechacutoffvgm = models.CharField(db_column='FechaCutOffVGM', blank=True, null=True)  # Field name made lowercase.
    horacutoffvgm = models.CharField(db_column='HoraCutOffVGM', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Llegadas'


class Llegadasdetalle(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    idllegadas = models.CharField(db_column='IDLlegadas', blank=True, null=True)  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.LlegadasDetalle'


class Monedas(models.Model):
    codigo = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=24, blank=True, null=True)
    pais = models.CharField(max_length=12, blank=True, null=True)
    simbolo = models.CharField(max_length=3, blank=True, null=True)
    solicitar = models.CharField(max_length=1, blank=True, null=True)
    alias = models.CharField(blank=True, null=True)
    valorminimo = models.DecimalField(db_column='ValorMinimo', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    valormaximo = models.DecimalField(db_column='ValorMaximo', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    paridadminima = models.DecimalField(db_column='ParidadMinima', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    paridadmaxima = models.DecimalField(db_column='ParidadMaxima', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    busquedaweb = models.CharField(db_column='BusquedaWeb', max_length=3, blank=True, null=True)  # Field name made lowercase.
    corporativo = models.CharField(db_column='Corporativo', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Monedas'


class Notificaciones(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    titulo = models.CharField(db_column='Titulo', max_length=88, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    desde = models.CharField(db_column='Desde', max_length=1, blank=True, null=True)  # Field name made lowercase.
    destinatario = models.CharField(db_column='Destinatario', max_length=1, blank=True, null=True)  # Field name made lowercase.
    razonsocial = models.CharField(db_column='RazonSocial', blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', blank=True, null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', blank=True, null=True)  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    ruc = models.CharField(db_column='Ruc', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', blank=True, null=True)  # Field name made lowercase.
    texto = models.TextField(db_column='Texto', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    idioma = models.IntegerField(db_column='Idioma', blank=True, null=True)  # Field name made lowercase.
    salida = models.CharField(db_column='Salida', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enviodatoshouse = models.CharField(db_column='EnvioDatosHouse', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Notificaciones'


class Nromensaje(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.NroMensaje'


class Organiza(models.Model):
    codigo = models.CharField(blank=True, null=True)
    empresa = models.CharField(blank=True, null=True)
    direccion = models.CharField(blank=True, null=True)
    localidad = models.CharField(blank=True, null=True)
    ciudad = models.CharField(blank=True, null=True)
    pais = models.CharField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True)
    fax = models.CharField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    observaciones = models.CharField(blank=True, null=True)
    cpostal = models.CharField(blank=True, null=True)
    contactos = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '.Organiza'


class Otrosservicios(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=24, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.OtrosServicios'


class Passsocios(models.Model):
    pnombre = models.CharField(db_column='Pnombre', blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.PassSocios'


class Password(models.Model):
    pnombre = models.CharField(max_length=11, blank=True, null=True)
    pword = models.CharField(max_length=9, blank=True, null=True)
    pnivel = models.IntegerField(blank=True, null=True)
    accaltas = models.IntegerField(blank=True, null=True)
    accbajas = models.IntegerField(blank=True, null=True)
    acceditar = models.IntegerField(blank=True, null=True)
    accexpaerea = models.IntegerField(blank=True, null=True)
    accexpmarit = models.IntegerField(blank=True, null=True)
    accexpterra = models.IntegerField(blank=True, null=True)
    accimpaerea = models.IntegerField(blank=True, null=True)
    accimpmarit = models.IntegerField(blank=True, null=True)
    accimpterra = models.IntegerField(blank=True, null=True)
    accadmin = models.IntegerField(blank=True, null=True)
    acccotiz = models.IntegerField(blank=True, null=True)
    acccexaerea = models.IntegerField(blank=True, null=True)
    acccexmarit = models.IntegerField(blank=True, null=True)
    acccexterra = models.IntegerField(blank=True, null=True)
    acccimaerea = models.IntegerField(blank=True, null=True)
    acccimmarit = models.IntegerField(blank=True, null=True)
    acccimterra = models.IntegerField(blank=True, null=True)
    accconsul = models.IntegerField(blank=True, null=True)
    accconver = models.IntegerField(blank=True, null=True)
    accnuevo = models.IntegerField(blank=True, null=True)
    accedita = models.IntegerField(blank=True, null=True)
    accborra = models.IntegerField(blank=True, null=True)
    accver = models.IntegerField(blank=True, null=True)
    accpreventa = models.IntegerField(blank=True, null=True)
    accdocum = models.IntegerField(blank=True, null=True)
    accrenta = models.IntegerField(blank=True, null=True)
    accedi = models.IntegerField(blank=True, null=True)
    accbonif = models.IntegerField(blank=True, null=True)
    accfacturar = models.IntegerField(blank=True, null=True)
    acccobrar = models.IntegerField(blank=True, null=True)
    accprovee = models.IntegerField(blank=True, null=True)
    accpagar = models.IntegerField(blank=True, null=True)
    accorden = models.IntegerField(blank=True, null=True)
    acccontab = models.IntegerField(blank=True, null=True)
    accseguir = models.IntegerField(blank=True, null=True)
    acctransito = models.IntegerField(blank=True, null=True)
    inicial = models.CharField(max_length=3, blank=True, null=True)
    nombre = models.CharField(max_length=22, blank=True, null=True)
    mail = models.CharField(max_length=36, blank=True, null=True)
    grupo = models.CharField(blank=True, null=True)
    accbloqueo = models.IntegerField(blank=True, null=True)
    accingcheques = models.IntegerField(blank=True, null=True)
    accingdocum = models.IntegerField(blank=True, null=True)
    accbajacheques = models.IntegerField(blank=True, null=True)
    accbajadocum = models.IntegerField(blank=True, null=True)
    accvtocheemi = models.IntegerField(blank=True, null=True)
    accvtodocemi = models.IntegerField(blank=True, null=True)
    acccontrol = models.IntegerField(blank=True, null=True)
    accnotacredito = models.IntegerField(blank=True, null=True)
    accsocios = models.IntegerField(blank=True, null=True)
    accservicios = models.IntegerField(blank=True, null=True)
    accvendedores = models.IntegerField(blank=True, null=True)
    accorganiza = models.IntegerField(blank=True, null=True)
    accdepositos = models.IntegerField(blank=True, null=True)
    accmonedas = models.IntegerField(blank=True, null=True)
    accpaises = models.IntegerField(blank=True, null=True)
    accproductos = models.IntegerField(blank=True, null=True)
    accplan = models.IntegerField(blank=True, null=True)
    acctextos = models.IntegerField(blank=True, null=True)
    acctraficos = models.IntegerField(blank=True, null=True)
    accvapores = models.IntegerField(blank=True, null=True)
    accareas = models.IntegerField(blank=True, null=True)
    accfondos = models.IntegerField(blank=True, null=True)
    caja = models.IntegerField(blank=True, null=True)
    sucursal = models.IntegerField(blank=True, null=True)
    accsoccli = models.IntegerField(blank=True, null=True)
    accsocpro = models.IntegerField(blank=True, null=True)
    accsocmix = models.IntegerField(blank=True, null=True)
    accsoctra = models.IntegerField(blank=True, null=True)
    accsocage = models.IntegerField(blank=True, null=True)
    accsocarm = models.IntegerField(blank=True, null=True)
    accsocdes = models.IntegerField(blank=True, null=True)
    accsocotr = models.IntegerField(blank=True, null=True)
    accediprev = models.IntegerField(blank=True, null=True)
    acceliprev = models.IntegerField(blank=True, null=True)
    accgendocdef = models.IntegerField(blank=True, null=True)
    accversucursales = models.IntegerField(db_column='AccVerSucursales', blank=True, null=True)  # Field name made lowercase.
    accborrodoc = models.IntegerField(db_column='AccBorroDoc', blank=True, null=True)  # Field name made lowercase.
    accctacodif = models.IntegerField(db_column='AccCtaCodif', blank=True, null=True)  # Field name made lowercase.
    accvertodo = models.IntegerField(db_column='AccVerTodo', blank=True, null=True)  # Field name made lowercase.
    accexportar = models.IntegerField(db_column='AccExportar', blank=True, null=True)  # Field name made lowercase.
    accverbonifcli = models.IntegerField(db_column='AccVerBonifCli', blank=True, null=True)  # Field name made lowercase.
    acceditacerrado = models.IntegerField(db_column='AccEditaCerrado', blank=True, null=True)  # Field name made lowercase.
    idioma = models.IntegerField(db_column='Idioma', blank=True, null=True)  # Field name made lowercase.
    accfaceleclotes = models.IntegerField(db_column='AccFacElecLotes', blank=True, null=True)  # Field name made lowercase.
    masterkey = models.CharField(db_column='MasterKey', blank=True, null=True)  # Field name made lowercase.
    accentregaorden = models.IntegerField(db_column='accEntregaOrden', blank=True, null=True)  # Field name made lowercase.
    accciudades = models.IntegerField(db_column='accCiudades', blank=True, null=True)  # Field name made lowercase.
    accproyectos = models.IntegerField(db_column='accProyectos', blank=True, null=True)  # Field name made lowercase.
    accscheduleb = models.IntegerField(db_column='accScheduleb', blank=True, null=True)  # Field name made lowercase.
    accports = models.IntegerField(db_column='accPorts', blank=True, null=True)  # Field name made lowercase.
    acccodes = models.IntegerField(db_column='accCodes', blank=True, null=True)  # Field name made lowercase.
    accimppurgescheduleb = models.IntegerField(db_column='accImpPurgeScheduleb', blank=True, null=True)  # Field name made lowercase.
    accaes = models.IntegerField(db_column='accAES', blank=True, null=True)  # Field name made lowercase.
    diascambio = models.IntegerField(db_column='DiasCambio', blank=True, null=True)  # Field name made lowercase.
    fechaultimacambio = models.CharField(db_column='FechaUltimaCambio', max_length=19, blank=True, null=True)  # Field name made lowercase.
    securityiata = models.CharField(db_column='SecurityIata', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cargo = models.CharField(db_column='Cargo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    acccontrolprov = models.IntegerField(db_column='AccControlProv', blank=True, null=True)  # Field name made lowercase.
    accselecvendedor = models.IntegerField(db_column='AccSelecVendedor', blank=True, null=True)  # Field name made lowercase.
    accinfocontable = models.IntegerField(db_column='AccInfoContable', blank=True, null=True)  # Field name made lowercase.
    accborrarattach = models.IntegerField(db_column='AccBorrarAttach', blank=True, null=True)  # Field name made lowercase.
    accprefactura = models.IntegerField(db_column='AccPreFactura', blank=True, null=True)  # Field name made lowercase.
    acceditafollowup = models.IntegerField(db_column='AccEditaFollowUp', blank=True, null=True)  # Field name made lowercase.
    accmodposicion = models.IntegerField(db_column='AccModPosicion', blank=True, null=True)  # Field name made lowercase.
    accmoddocumentos = models.IntegerField(db_column='AccModDocumentos', blank=True, null=True)  # Field name made lowercase.
    internodirecto = models.CharField(db_column='InternoDirecto', max_length=3, blank=True, null=True)  # Field name made lowercase.
    clientemail = models.CharField(db_column='ClienteMail', max_length=1, blank=True, null=True)  # Field name made lowercase.
    accmanten = models.IntegerField(db_column='AccManten', blank=True, null=True)  # Field name made lowercase.
    acceditaeditados = models.IntegerField(db_column='AccEditaEditados', blank=True, null=True)  # Field name made lowercase.
    acctrace = models.IntegerField(db_column='AccTrace', blank=True, null=True)  # Field name made lowercase.
    accdepuradores = models.IntegerField(db_column='AccDepuradores', blank=True, null=True)  # Field name made lowercase.
    acceditafinanzas = models.IntegerField(db_column='AccEditaFinanzas', blank=True, null=True)  # Field name made lowercase.
    acccambiausuario = models.IntegerField(db_column='AccCambiaUsuario', blank=True, null=True)  # Field name made lowercase.
    accimprimir = models.IntegerField(db_column='AccImprimir', blank=True, null=True)  # Field name made lowercase.
    acccambiafecha = models.IntegerField(db_column='AccCambiaFecha', blank=True, null=True)  # Field name made lowercase.
    accinfotracking = models.IntegerField(db_column='AccInfoTracking', blank=True, null=True)  # Field name made lowercase.
    accvertodoop = models.IntegerField(db_column='AccVerTodoOP', blank=True, null=True)  # Field name made lowercase.
    accvertodosc = models.IntegerField(db_column='AccVerTodoSC', blank=True, null=True)  # Field name made lowercase.
    accmodsegvinculado = models.IntegerField(db_column='AccModSegVinculado', blank=True, null=True)  # Field name made lowercase.
    accmodimpu = models.CharField(db_column='AccModImpu', max_length=1, blank=True, null=True)  # Field name made lowercase.
    accfechavto = models.IntegerField(db_column='AccFechaVto', blank=True, null=True)  # Field name made lowercase.
    accfechacoti = models.IntegerField(db_column='AccFechaCoti', blank=True, null=True)  # Field name made lowercase.
    acceditacotizacion = models.IntegerField(db_column='AccEditaCotizacion', blank=True, null=True)  # Field name made lowercase.
    usersmtp = models.CharField(db_column='UserSMTP', max_length=3, blank=True, null=True)  # Field name made lowercase.
    passsmtp = models.CharField(db_column='PassSMTP', blank=True, null=True)  # Field name made lowercase.
    correo = models.CharField(db_column='Correo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    acctodosusrretransmiten95 = models.IntegerField(db_column='AccTodosUsrRetransmiten95', blank=True, null=True)  # Field name made lowercase.
    acceditatodose = models.IntegerField(db_column='accEditaTodoSE', blank=True, null=True)  # Field name made lowercase.
    accreenviofacelec = models.IntegerField(db_column='accReenvioFacElec', blank=True, null=True)  # Field name made lowercase.
    accsocioactivo = models.IntegerField(db_column='accSocioActivo', blank=True, null=True)  # Field name made lowercase.
    accreimprimeoriginal = models.IntegerField(db_column='accReimprimeOriginal', blank=True, null=True)  # Field name made lowercase.
    acceditaaceptada = models.IntegerField(db_column='accEditaAceptada', blank=True, null=True)  # Field name made lowercase.
    encargadocuenta = models.IntegerField(db_column='EncargadoCuenta', blank=True, null=True)  # Field name made lowercase.
    accfacdefinitiva = models.IntegerField(db_column='accFacDefinitiva', blank=True, null=True)  # Field name made lowercase.
    accfacprovision = models.IntegerField(db_column='accFacProvision', blank=True, null=True)  # Field name made lowercase.
    accpasarprovdef = models.IntegerField(db_column='accPasarProvDef', blank=True, null=True)  # Field name made lowercase.
    accsolovariables = models.IntegerField(db_column='accSoloVariables', blank=True, null=True)  # Field name made lowercase.
    accbodega = models.IntegerField(db_column='accBodega', blank=True, null=True)  # Field name made lowercase.
    accwr = models.IntegerField(db_column='accWR', blank=True, null=True)  # Field name made lowercase.
    accegresowr = models.IntegerField(db_column='accEgresoWR', blank=True, null=True)  # Field name made lowercase.
    accpickwr = models.IntegerField(db_column='accPickWR', blank=True, null=True)  # Field name made lowercase.
    accasistwr = models.IntegerField(db_column='accAsistWR', blank=True, null=True)  # Field name made lowercase.
    accdistribuwr = models.IntegerField(db_column='accDistribuWR', blank=True, null=True)  # Field name made lowercase.
    accfraccionwr = models.IntegerField(db_column='accFraccionWR', blank=True, null=True)  # Field name made lowercase.
    accagruparwr = models.IntegerField(db_column='accAgruparWR', blank=True, null=True)  # Field name made lowercase.
    accendosowr = models.IntegerField(db_column='accEndosoWR', blank=True, null=True)  # Field name made lowercase.
    accrepackwr = models.IntegerField(db_column='accRepackWR', blank=True, null=True)  # Field name made lowercase.
    accajustewr = models.IntegerField(db_column='accAjusteWR', blank=True, null=True)  # Field name made lowercase.
    accnacionalwr = models.IntegerField(db_column='accNacionalWR', blank=True, null=True)  # Field name made lowercase.
    accubicarwr = models.IntegerField(db_column='accUbicarWR', blank=True, null=True)  # Field name made lowercase.
    accremitowr = models.IntegerField(db_column='accRemitoWR', blank=True, null=True)  # Field name made lowercase.
    acctarifaswr = models.IntegerField(db_column='accTarifasWR', blank=True, null=True)  # Field name made lowercase.
    accestadiswr = models.IntegerField(db_column='accEstadisWR', blank=True, null=True)  # Field name made lowercase.
    accinventwr = models.IntegerField(db_column='accInventWR', blank=True, null=True)  # Field name made lowercase.
    accfichawr = models.IntegerField(db_column='accFichaWR', blank=True, null=True)  # Field name made lowercase.
    acceventoswr = models.IntegerField(db_column='accEventosWR', blank=True, null=True)  # Field name made lowercase.
    accfamiliawr = models.IntegerField(db_column='accFamiliaWR', blank=True, null=True)  # Field name made lowercase.
    accitemswr = models.IntegerField(db_column='accItemsWR', blank=True, null=True)  # Field name made lowercase.
    accbodegaswr = models.IntegerField(db_column='accBodegasWR', blank=True, null=True)  # Field name made lowercase.
    accoperawr = models.IntegerField(db_column='accOperaWR', blank=True, null=True)  # Field name made lowercase.
    acctareaswr = models.IntegerField(db_column='accTareasWR', blank=True, null=True)  # Field name made lowercase.
    accinsumoswr = models.IntegerField(db_column='accInsumosWR', blank=True, null=True)  # Field name made lowercase.
    accequiposwr = models.IntegerField(db_column='accEquiposWR', blank=True, null=True)  # Field name made lowercase.
    accvehiwr = models.IntegerField(db_column='accVehiWR', blank=True, null=True)  # Field name made lowercase.
    accstatuswr = models.IntegerField(db_column='accStatusWR', blank=True, null=True)  # Field name made lowercase.
    acccompwr = models.IntegerField(db_column='accCompWR', blank=True, null=True)  # Field name made lowercase.
    cuentabloqueada = models.IntegerField(db_column='CuentaBloqueada', blank=True, null=True)  # Field name made lowercase.
    ultimaactividad = models.CharField(db_column='UltimaActividad', max_length=19, blank=True, null=True)  # Field name made lowercase.
    skype = models.CharField(db_column='Skype', blank=True, null=True)  # Field name made lowercase.
    celular = models.CharField(db_column='Celular', blank=True, null=True)  # Field name made lowercase.
    acccostos = models.IntegerField(db_column='accCostos', blank=True, null=True)  # Field name made lowercase.
    accoservicios = models.IntegerField(db_column='AccOServicios', blank=True, null=True)  # Field name made lowercase.
    acctruck = models.IntegerField(db_column='AccTruck', blank=True, null=True)  # Field name made lowercase.
    estacion = models.IntegerField(db_column='Estacion', blank=True, null=True)  # Field name made lowercase.
    aprobarvalormin = models.DecimalField(db_column='AprobarValorMin', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    aprobarvalormax = models.DecimalField(db_column='AprobarValorMax', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    accniif = models.IntegerField(db_column='accNIIF', blank=True, null=True)  # Field name made lowercase.
    accactivofijo = models.IntegerField(db_column='accActivoFijo', blank=True, null=True)  # Field name made lowercase.
    accmodifpicking = models.IntegerField(db_column='accModifPicking', blank=True, null=True)  # Field name made lowercase.
    accmodifegreso = models.IntegerField(db_column='accModifEgreso', blank=True, null=True)  # Field name made lowercase.
    accfechacorte = models.IntegerField(db_column='accFechaCorte', blank=True, null=True)  # Field name made lowercase.
    acclimitecredito = models.IntegerField(db_column='accLimiteCredito', blank=True, null=True)  # Field name made lowercase.
    accaduanawr = models.IntegerField(db_column='AccAduanaWR', blank=True, null=True)  # Field name made lowercase.
    accpedidoswr = models.IntegerField(db_column='AccPedidosWR', blank=True, null=True)  # Field name made lowercase.
    accreacpedidoswr = models.IntegerField(db_column='AccReacPedidosWR', blank=True, null=True)  # Field name made lowercase.
    accveotodoattach = models.IntegerField(db_column='AccVeoTodoAttach', blank=True, null=True)  # Field name made lowercase.
    accmodhouse = models.IntegerField(db_column='AccModHouse', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Password'


class Passwordhistorial(models.Model):
    pnombre = models.CharField(max_length=10, blank=True, null=True)
    pword = models.CharField(max_length=9, blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.PasswordHistorial'


class Permisosterr(models.Model):
    cliente = models.CharField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    peroriginal = models.CharField(db_column='PerOriginal', blank=True, null=True)  # Field name made lowercase.
    percomplem = models.CharField(db_column='PerComplem', blank=True, null=True)  # Field name made lowercase.
    contrif = models.CharField(db_column='Contrif', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.PermisosTerr'


class Prefijos(models.Model):
    prefijo = models.CharField(max_length=2, blank=True, null=True)
    detalle = models.CharField(max_length=21, blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '.Prefijos'


class Provincias(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    abreviacion = models.CharField(db_column='Abreviacion', blank=True, null=True)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Provincias'


class Proyectos(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Proyectos'


class Retenciones(models.Model):
    servicio = models.CharField(blank=True, null=True)
    cuenta = models.CharField(blank=True, null=True)
    aplica = models.CharField(blank=True, null=True)
    comentario = models.CharField(blank=True, null=True)
    porcentaje = models.CharField(blank=True, null=True)
    tipocli = models.CharField(db_column='TipoCli', blank=True, null=True)  # Field name made lowercase.
    baseminima = models.CharField(db_column='BaseMinima', blank=True, null=True)  # Field name made lowercase.
    contracuenta = models.CharField(db_column='ContraCuenta', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    autorretenedor = models.CharField(db_column='Autorretenedor', blank=True, null=True)  # Field name made lowercase.
    suma = models.CharField(db_column='Suma', blank=True, null=True)  # Field name made lowercase.
    basemaxima = models.CharField(db_column='BaseMaxima', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Retenciones'


class Servrelacion(models.Model):
    codigovta = models.CharField(db_column='CodigoVTA', blank=True, null=True)  # Field name made lowercase.
    codigocpa = models.CharField(db_column='CodigoCPA', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.ServRelacion'


class Servvariables(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    tipovariable = models.CharField(db_column='TipoVariable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    variablecada = models.IntegerField(db_column='VariableCada', blank=True, null=True)  # Field name made lowercase.
    baseminima = models.IntegerField(db_column='BaseMinima', blank=True, null=True)  # Field name made lowercase.
    redondea = models.IntegerField(db_column='Redondea', blank=True, null=True)  # Field name made lowercase.
    sociocomercial = models.SmallIntegerField(db_column='SocioComercial', blank=True, null=True)  # Field name made lowercase.
    tiposocio = models.CharField(db_column='TipoSocio', max_length=1, blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=3, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    tarifa = models.CharField(db_column='Tarifa', max_length=1, blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    minimo = models.DecimalField(db_column='Minimo', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    maximo = models.DecimalField(db_column='Maximo', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    moneda = models.IntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    producto = models.IntegerField(db_column='Producto', blank=True, null=True)  # Field name made lowercase.
    unidad = models.CharField(db_column='Unidad', max_length=3, blank=True, null=True)  # Field name made lowercase.
    unidadvol = models.CharField(db_column='UnidadVol', max_length=3, blank=True, null=True)  # Field name made lowercase.
    desdevalor = models.DecimalField(db_column='DesdeValor', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.ServVariables'


class Servicios(models.Model):
    codigo = models.SmallIntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=57, blank=True, null=True)
    observaciones = models.CharField(max_length=3, blank=True, null=True)
    gravado = models.CharField(blank=True, null=True)
    tasa = models.CharField(max_length=1, blank=True, null=True)
    refparam = models.CharField(blank=True, null=True)
    prefijo = models.CharField(max_length=3, blank=True, null=True)
    contable = models.IntegerField(blank=True, null=True)
    contiva = models.CharField(blank=True, null=True)
    precio = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    imputar = models.CharField(max_length=1, blank=True, null=True)
    tipogasto = models.CharField(max_length=1, blank=True, null=True)
    variable = models.IntegerField(blank=True, null=True)
    tipovariable = models.CharField(max_length=1, blank=True, null=True)
    variablecada = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    redondea = models.IntegerField(blank=True, null=True)
    baseminima = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    ctaorden = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    ibruto = models.IntegerField(blank=True, null=True)
    minimo = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    maximo = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    operacion = models.CharField(max_length=1, blank=True, null=True)
    transito = models.CharField(max_length=1, blank=True, null=True)
    maritimo = models.CharField(max_length=1, blank=True, null=True)
    preciob = models.DecimalField(db_column='precioB', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    precioc = models.DecimalField(db_column='precioC', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    preciod = models.DecimalField(db_column='precioD', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    corporativo = models.IntegerField(blank=True, null=True)
    ctaordeniva = models.IntegerField(blank=True, null=True)
    repartir = models.CharField(max_length=1, blank=True, null=True)
    tipoitem = models.CharField(blank=True, null=True)
    itemstock = models.CharField(max_length=1, blank=True, null=True)
    codigostock = models.CharField(max_length=3, blank=True, null=True)
    ctavtastock = models.CharField(max_length=1, blank=True, null=True)
    ctacomstock = models.CharField(max_length=1, blank=True, null=True)
    familia = models.CharField(max_length=1, blank=True, null=True)
    cofis = models.CharField(max_length=1, blank=True, null=True)
    unistock = models.CharField(max_length=8, blank=True, null=True)
    minimob = models.DecimalField(db_column='minimoB', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    maximob = models.DecimalField(db_column='maximoB', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    minimoc = models.DecimalField(db_column='minimoC', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    maximoc = models.DecimalField(db_column='maximoC', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    minimod = models.DecimalField(db_column='minimoD', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    maximod = models.DecimalField(db_column='maximoD', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    nombreingles = models.CharField(max_length=48, blank=True, null=True)
    tomarcomoiva = models.CharField(db_column='TomarComoIVA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    activa = models.CharField(db_column='Activa', max_length=1, blank=True, null=True)  # Field name made lowercase.
    recuperogastos = models.CharField(db_column='RecuperoGastos', max_length=1, blank=True, null=True)  # Field name made lowercase.
    servicioscliente = models.CharField(db_column='ServiciosCliente', max_length=1, blank=True, null=True)  # Field name made lowercase.
    extracosto = models.CharField(db_column='ExtraCosto', max_length=1, blank=True, null=True)  # Field name made lowercase.
    catsat = models.CharField(db_column='catSAT', blank=True, null=True)  # Field name made lowercase.
    claveunidadsat = models.CharField(db_column='ClaveUnidadSAT', blank=True, null=True)  # Field name made lowercase.
    montonoaplicaretencion = models.DecimalField(db_column='MontoNoAplicaRetencion', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Servicios'


class Sociosweb(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    codigoweb = models.CharField(db_column='CodigoWeb', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.SociosWeb'


class Status(models.Model):
    status = models.CharField(max_length=11, blank=True, null=True)
    costos = models.CharField(max_length=1, blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '.Status'


class Statussocios(models.Model):
    numero = models.CharField(blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '.StatusSocios'


class Sucursales(models.Model):
    nrosucursal = models.CharField(db_column='NroSucursal', blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(db_column='Factura', blank=True, null=True)  # Field name made lowercase.
    notacredito = models.CharField(db_column='NotaCredito', blank=True, null=True)  # Field name made lowercase.
    recibo = models.CharField(db_column='Recibo', blank=True, null=True)  # Field name made lowercase.
    contado = models.CharField(db_column='Contado', blank=True, null=True)  # Field name made lowercase.
    notadebito = models.CharField(db_column='NotaDebito', blank=True, null=True)  # Field name made lowercase.
    devolcontado = models.CharField(db_column='DevolContado', blank=True, null=True)  # Field name made lowercase.
    nombresucursal = models.CharField(db_column='NombreSucursal', blank=True, null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', blank=True, null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', blank=True, null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', blank=True, null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='DRuc', blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', blank=True, null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', blank=True, null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', blank=True, null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', blank=True, null=True)  # Field name made lowercase.
    serie = models.CharField(db_column='Serie', blank=True, null=True)  # Field name made lowercase.
    keydosificacion = models.CharField(db_column='KeyDosificacion', blank=True, null=True)  # Field name made lowercase.
    noautorizacion = models.CharField(db_column='NoAutorizacion', blank=True, null=True)  # Field name made lowercase.
    fechalimiteemision = models.CharField(db_column='FechaLimiteEmision', blank=True, null=True)  # Field name made lowercase.
    prefijo = models.CharField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Sucursales'


class Sucursalesargentina(models.Model):
    nrosucursal = models.CharField(db_column='NroSucursal', blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(blank=True, null=True)
    notacredito = models.CharField(blank=True, null=True)
    recibo = models.CharField(blank=True, null=True)
    contado = models.CharField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', blank=True, null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', blank=True, null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', blank=True, null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', blank=True, null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', blank=True, null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', blank=True, null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', blank=True, null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', blank=True, null=True)  # Field name made lowercase.
    prefijo = models.CharField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    notadebito = models.CharField(db_column='NotaDebito', blank=True, null=True)  # Field name made lowercase.
    facelectronica = models.CharField(db_column='FacElectronica', blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.SucursalesArgentina'


class Sucursalesbrasil(models.Model):
    nrosucursal = models.CharField(db_column='NroSucursal', blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(blank=True, null=True)
    notacredito = models.CharField(blank=True, null=True)
    recibo = models.CharField(blank=True, null=True)
    contado = models.CharField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', blank=True, null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', blank=True, null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', blank=True, null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', blank=True, null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', blank=True, null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', blank=True, null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', blank=True, null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.SucursalesBrasil'


class Sucursaleschile(models.Model):
    nrosucursal = models.IntegerField(db_column='NroSucursal', blank=True, null=True)  # Field name made lowercase.
    fachilea = models.IntegerField(db_column='FaChileA', blank=True, null=True)  # Field name made lowercase.
    fachileb = models.IntegerField(db_column='FaChileB', blank=True, null=True)  # Field name made lowercase.
    ncchilea = models.SmallIntegerField(db_column='NcChileA', blank=True, null=True)  # Field name made lowercase.
    ncchileb = models.IntegerField(db_column='NcChileB', blank=True, null=True)  # Field name made lowercase.
    ndchilea = models.IntegerField(db_column='NdChileA', blank=True, null=True)  # Field name made lowercase.
    ndchileb = models.IntegerField(db_column='NdChileB', blank=True, null=True)  # Field name made lowercase.
    nombresucursal = models.CharField(db_column='NombreSucursal', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', max_length=3, blank=True, null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', max_length=3, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=3, blank=True, null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=3, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=3, blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=3, blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.SucursalesChile'


class Sucursalesdominicana(models.Model):
    nrosucursal = models.CharField(db_column='NroSucursal', blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(blank=True, null=True)
    notacredito = models.CharField(blank=True, null=True)
    recibo = models.CharField(blank=True, null=True)
    contado = models.CharField(blank=True, null=True)
    notadebito = models.CharField(db_column='Notadebito', blank=True, null=True)  # Field name made lowercase.
    devolcontado = models.CharField(db_column='Devolcontado', blank=True, null=True)  # Field name made lowercase.
    nombresucursal = models.CharField(db_column='NombreSucursal', blank=True, null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', blank=True, null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', blank=True, null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', blank=True, null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', blank=True, null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', blank=True, null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', blank=True, null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.SucursalesDominicana'


class Sucursalesmexico(models.Model):
    nrosucursal = models.IntegerField(db_column='NroSucursal', blank=True, null=True)  # Field name made lowercase.
    facturamx = models.IntegerField(blank=True, null=True)
    notacreditomx = models.IntegerField(blank=True, null=True)
    recibofletemx = models.IntegerField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', max_length=9, blank=True, null=True)  # Field name made lowercase.
    facturamxusd = models.IntegerField(blank=True, null=True)
    ddireccion = models.CharField(db_column='DDireccion', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', max_length=3, blank=True, null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', max_length=3, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=3, blank=True, null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', max_length=3, blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', max_length=3, blank=True, null=True)  # Field name made lowercase.
    facturad = models.IntegerField(db_column='FacturaD', blank=True, null=True)  # Field name made lowercase.
    notacreditod = models.IntegerField(db_column='NotaCreditoD', blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', max_length=3, blank=True, null=True)  # Field name made lowercase.
    notacreditousd = models.IntegerField(db_column='NotaCreditoUSD', blank=True, null=True)  # Field name made lowercase.
    notadebito = models.IntegerField(db_column='NotaDebito', blank=True, null=True)  # Field name made lowercase.
    notadebitousd = models.IntegerField(db_column='NotaDebitoUSD', blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.SucursalesMexico'


class Sucursalesparaguay(models.Model):
    nrosucursal = models.CharField(db_column='NroSucursal', blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(blank=True, null=True)
    notacredito = models.CharField(blank=True, null=True)
    recibo = models.CharField(blank=True, null=True)
    contado = models.CharField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', blank=True, null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', blank=True, null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', blank=True, null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', blank=True, null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', blank=True, null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', blank=True, null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', blank=True, null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.SucursalesParaguay'


class Sucursalesperu(models.Model):
    nrosucursal = models.CharField(db_column='NroSucursal', blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(blank=True, null=True)
    notacredito = models.CharField(blank=True, null=True)
    recibo = models.CharField(blank=True, null=True)
    contado = models.CharField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', blank=True, null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', blank=True, null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', blank=True, null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', blank=True, null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', blank=True, null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', blank=True, null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', blank=True, null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.SucursalesPeru'


class Sucursalesuruguay(models.Model):
    nrosucursal = models.CharField(db_column='NroSucursal', blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(blank=True, null=True)
    notacredito = models.CharField(blank=True, null=True)
    recibo = models.CharField(blank=True, null=True)
    contado = models.CharField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', blank=True, null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', blank=True, null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', blank=True, null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', blank=True, null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', blank=True, null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', blank=True, null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', blank=True, null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.SucursalesUruguay'


class Sucursalesusa(models.Model):
    nrosucursal = models.CharField(db_column='NroSucursal', blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(blank=True, null=True)
    notacredito = models.CharField(blank=True, null=True)
    recibo = models.CharField(blank=True, null=True)
    contado = models.CharField(blank=True, null=True)
    nombresucursal = models.CharField(db_column='NombreSucursal', blank=True, null=True)  # Field name made lowercase.
    ddireccion = models.CharField(db_column='DDireccion', blank=True, null=True)  # Field name made lowercase.
    dlocalidad = models.CharField(db_column='DLocalidad', blank=True, null=True)  # Field name made lowercase.
    dtelefono = models.CharField(db_column='DTelefono', blank=True, null=True)  # Field name made lowercase.
    dfax = models.CharField(db_column='DFax', blank=True, null=True)  # Field name made lowercase.
    dcpostal = models.CharField(db_column='DCpostal', blank=True, null=True)  # Field name made lowercase.
    druc = models.CharField(db_column='Druc', blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', blank=True, null=True)  # Field name made lowercase.
    bltext = models.CharField(db_column='BLText', blank=True, null=True)  # Field name made lowercase.
    crttext = models.CharField(db_column='CRTText', blank=True, null=True)  # Field name made lowercase.
    nroiata = models.CharField(db_column='NroIATA', blank=True, null=True)  # Field name made lowercase.
    ciudadaereo = models.CharField(db_column='CiudadAereo', blank=True, null=True)  # Field name made lowercase.
    ciudadmaritimo = models.CharField(db_column='CiudadMaritimo', blank=True, null=True)  # Field name made lowercase.
    ciudadterrestre = models.CharField(db_column='CiudadTerrestre', blank=True, null=True)  # Field name made lowercase.
    senderpima = models.CharField(db_column='SenderPIMA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.SucursalesUsa'


class Tipoindustria(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.TipoIndustria'


class Tipooperacion(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.TipoOperacion'


class Trace(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=21, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=250, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=16, blank=True, null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(db_column='Numero', max_length=5, blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(db_column='Factura', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Trace'


class Traceinterface(models.Model):
    fechahora = models.CharField(db_column='FechaHora', blank=True, null=True)  # Field name made lowercase.
    embarque = models.CharField(db_column='Embarque', blank=True, null=True)  # Field name made lowercase.
    orden = models.CharField(db_column='Orden', blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', blank=True, null=True)  # Field name made lowercase.
    cliente = models.CharField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.TraceInterface'


class Trackingdetalles(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', blank=True, null=True)  # Field name made lowercase.
    idsociocomercial = models.CharField(db_column='IDSocioComercial', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.TrackingDetalles'


class Trackinglogin(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    sociocomercial = models.CharField(db_column='SocioComercial', blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', blank=True, null=True)  # Field name made lowercase.
    fechain = models.CharField(db_column='FechaIN', blank=True, null=True)  # Field name made lowercase.
    fechaout = models.CharField(db_column='FechaOUT', blank=True, null=True)  # Field name made lowercase.
    horain = models.CharField(db_column='HoraIN', blank=True, null=True)  # Field name made lowercase.
    horaout = models.CharField(db_column='HoraOUT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.TrackingLogin'


class Trackingterceros(models.Model):
    email = models.CharField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    passw = models.CharField(db_column='PassW', blank=True, null=True)  # Field name made lowercase.
    cliente = models.CharField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.
    embarcador = models.CharField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    consignatario = models.CharField(db_column='Consignatario', blank=True, null=True)  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', blank=True, null=True)  # Field name made lowercase.
    enviomail = models.CharField(db_column='EnvioMail', blank=True, null=True)  # Field name made lowercase.
    enviosocial = models.CharField(db_column='EnvioSocial', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.TrackingTerceros'


class Trackingusuarios(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    codsociocomercial = models.CharField(db_column='CodSocioComercial', blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.TrackingUsuarios'


class Traficos(models.Model):
    codigo = models.CharField(blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)
    observaciones = models.CharField(blank=True, null=True)
    diasim = models.CharField(db_column='DiasIM', blank=True, null=True)  # Field name made lowercase.
    diasia = models.CharField(db_column='DiasIA', blank=True, null=True)  # Field name made lowercase.
    diasit = models.CharField(db_column='DiasIT', blank=True, null=True)  # Field name made lowercase.
    diasem = models.CharField(db_column='DiasEM', blank=True, null=True)  # Field name made lowercase.
    diasea = models.CharField(db_column='DiasEA', blank=True, null=True)  # Field name made lowercase.
    diaset = models.CharField(db_column='DiasET', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Traficos'


class Vapores(models.Model):
    codigo = models.SmallIntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=22, blank=True, null=True)
    bandera = models.CharField(max_length=3, blank=True, null=True)
    deposito = models.IntegerField(blank=True, null=True)
    observaciones = models.CharField(max_length=16, blank=True, null=True)
    imo = models.CharField(db_column='IMO', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fechaactualizado = models.CharField(db_column='FechaActualizado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Vapores'


class Vendedores(models.Model):
    codigo = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=25, blank=True, null=True)
    direccion = models.CharField(max_length=3, blank=True, null=True)
    localidad = models.CharField(max_length=3, blank=True, null=True)
    telefono = models.CharField(max_length=3, blank=True, null=True)
    fax = models.CharField(max_length=3, blank=True, null=True)
    email = models.CharField(max_length=31, blank=True, null=True)
    cpostal = models.CharField(max_length=1, blank=True, null=True)
    ciudad = models.CharField(max_length=3, blank=True, null=True)
    pais = models.CharField(max_length=3, blank=True, null=True)
    condiciones = models.CharField(max_length=3, blank=True, null=True)
    observaciones = models.CharField(max_length=3, blank=True, null=True)
    comiexport = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    comimport = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    refparam = models.CharField(blank=True, null=True)
    tipoexport = models.CharField(max_length=1, blank=True, null=True)
    tipoimport = models.CharField(max_length=1, blank=True, null=True)
    tipomarexp = models.CharField(max_length=1, blank=True, null=True)
    tipomarimp = models.CharField(max_length=1, blank=True, null=True)
    comimarexp = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    comimarimp = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    tipoterexp = models.CharField(max_length=1, blank=True, null=True)
    tipoterimp = models.CharField(max_length=1, blank=True, null=True)
    comiterexp = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    comiterimp = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    iniciales = models.CharField(db_column='Iniciales', max_length=3, blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Vendedores'


class Vuelos(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    vuelo = models.CharField(db_column='Vuelo', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    horaorigen = models.CharField(db_column='HoraOrigen', blank=True, null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase.
    lunes = models.CharField(db_column='Lunes', blank=True, null=True)  # Field name made lowercase.
    martes = models.CharField(db_column='Martes', blank=True, null=True)  # Field name made lowercase.
    miercoles = models.CharField(db_column='Miercoles', blank=True, null=True)  # Field name made lowercase.
    jueves = models.CharField(db_column='Jueves', blank=True, null=True)  # Field name made lowercase.
    viernes = models.CharField(db_column='Viernes', blank=True, null=True)  # Field name made lowercase.
    sabado = models.CharField(db_column='Sabado', blank=True, null=True)  # Field name made lowercase.
    domingo = models.CharField(db_column='Domingo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.Vuelos'


class Ciudades(models.Model):
    codigo = models.CharField(max_length=5, blank=True, null=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    codedi = models.CharField(max_length=3, blank=True, null=True)
    codaduana = models.CharField(db_column='Codaduana', max_length=5, blank=True, null=True)  # Field name made lowercase.
    paises_idinternacional = models.CharField(db_column='Paises_IdInternacional', blank=True, null=True)  # Field name made lowercase.
    estado = models.IntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    fechaactualizado = models.CharField(db_column='FechaActualizado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.ciudades'


class Clientes(models.Model):
    codigo = models.SmallIntegerField(blank=True, null=True)
    empresa = models.CharField(max_length=50, blank=True, null=True)
    razonsocial = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=17, blank=True, null=True)
    ciudad = models.CharField(max_length=3, blank=True, null=True)
    pais = models.CharField(max_length=25, blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=235, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    cpostal = models.CharField(max_length=15, blank=True, null=True)
    ruc = models.CharField(max_length=30, blank=True, null=True)
    contactos = models.CharField(max_length=234, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)
    vendedor = models.IntegerField(blank=True, null=True)
    refparam = models.IntegerField(blank=True, null=True)
    organizacion = models.IntegerField(blank=True, null=True)
    comagente = models.IntegerField(blank=True, null=True)
    comagenteimport = models.IntegerField(blank=True, null=True)
    comagemarexp = models.IntegerField(blank=True, null=True)
    comagemarimp = models.IntegerField(blank=True, null=True)
    idinternacional = models.CharField(max_length=3, blank=True, null=True)
    prefijoguia = models.CharField(max_length=3, blank=True, null=True)
    comisiontransp = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    bonifica = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    critico = models.IntegerField(blank=True, null=True)
    socio = models.CharField(max_length=1, blank=True, null=True)
    tipocli = models.IntegerField(blank=True, null=True)
    ctavta = models.SmallIntegerField(blank=True, null=True)
    ctacomp = models.SmallIntegerField(blank=True, null=True)
    comageterrexp = models.IntegerField(blank=True, null=True)
    comageterrimp = models.IntegerField(blank=True, null=True)
    refestudio = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    jurisdiccion = models.IntegerField(blank=True, null=True)
    plazo = models.IntegerField(blank=True, null=True)
    limite = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    giro = models.CharField(max_length=3, blank=True, null=True)
    usuario = models.CharField(max_length=3, blank=True, null=True)
    password = models.CharField(max_length=3, blank=True, null=True)
    facturarle = models.CharField(max_length=1, blank=True, null=True)
    tarifa = models.CharField(max_length=1, blank=True, null=True)
    direccioncia = models.CharField(max_length=3, blank=True, null=True)
    ciudadcia = models.CharField(max_length=3, blank=True, null=True)
    telefonocia = models.CharField(max_length=3, blank=True, null=True)
    faxcia = models.CharField(max_length=3, blank=True, null=True)
    corporativo = models.CharField(max_length=3, blank=True, null=True)
    emailad = models.CharField(db_column='emailAD', max_length=235, blank=True, null=True)  # Field name made lowercase.
    emailem = models.CharField(db_column='emailEM', max_length=235, blank=True, null=True)  # Field name made lowercase.
    emailea = models.CharField(db_column='emailEA', max_length=235, blank=True, null=True)  # Field name made lowercase.
    emailet = models.CharField(db_column='emailET', max_length=235, blank=True, null=True)  # Field name made lowercase.
    emailim = models.CharField(db_column='emailIM', max_length=235, blank=True, null=True)  # Field name made lowercase.
    emailia = models.CharField(db_column='emailIA', max_length=235, blank=True, null=True)  # Field name made lowercase.
    emailit = models.CharField(db_column='emailIT', max_length=235, blank=True, null=True)  # Field name made lowercase.
    fecalta = models.CharField(max_length=19, blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    despachante = models.CharField(max_length=3, blank=True, null=True)
    motivodespa = models.CharField(max_length=3, blank=True, null=True)
    agente = models.CharField(max_length=3, blank=True, null=True)
    motivoage = models.CharField(max_length=3, blank=True, null=True)
    deposito = models.CharField(max_length=3, blank=True, null=True)
    motivodep = models.CharField(max_length=3, blank=True, null=True)
    expectativa = models.CharField(max_length=3, blank=True, null=True)
    condiciones = models.CharField(max_length=3, blank=True, null=True)
    usuario2 = models.CharField(max_length=3, blank=True, null=True)
    password2 = models.CharField(max_length=3, blank=True, null=True)
    sociomadre = models.IntegerField(blank=True, null=True)
    plazoea = models.IntegerField(db_column='plazoEA', blank=True, null=True)  # Field name made lowercase.
    plazoia = models.IntegerField(db_column='plazoIA', blank=True, null=True)  # Field name made lowercase.
    plazoem = models.IntegerField(db_column='plazoEM', blank=True, null=True)  # Field name made lowercase.
    plazoim = models.IntegerField(db_column='plazoIM', blank=True, null=True)  # Field name made lowercase.
    plazoet = models.IntegerField(db_column='plazoET', blank=True, null=True)  # Field name made lowercase.
    plazoit = models.IntegerField(db_column='plazoIT', blank=True, null=True)  # Field name made lowercase.
    plazomu = models.IntegerField(db_column='plazoMU', blank=True, null=True)  # Field name made lowercase.
    riesgo = models.CharField(max_length=1, blank=True, null=True)
    web = models.CharField(max_length=35, blank=True, null=True)
    contactoim = models.CharField(db_column='ContactoIM', max_length=44, blank=True, null=True)  # Field name made lowercase.
    contactoia = models.CharField(db_column='ContactoIA', max_length=44, blank=True, null=True)  # Field name made lowercase.
    contactoit = models.CharField(db_column='ContactoIT', max_length=44, blank=True, null=True)  # Field name made lowercase.
    contactoem = models.CharField(db_column='ContactoEM', max_length=44, blank=True, null=True)  # Field name made lowercase.
    contactoea = models.CharField(db_column='ContactoEA', max_length=44, blank=True, null=True)  # Field name made lowercase.
    contactoet = models.CharField(db_column='ContactoET', max_length=44, blank=True, null=True)  # Field name made lowercase.
    contactoad = models.CharField(db_column='ContactoAD', max_length=44, blank=True, null=True)  # Field name made lowercase.
    contactogral = models.CharField(db_column='ContactoGRAL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dicvta = models.CharField(max_length=3, blank=True, null=True)
    diccpa = models.CharField(max_length=3, blank=True, null=True)
    aduana = models.CharField(db_column='Aduana', max_length=3, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(blank=True, null=True)
    fletesocioim = models.IntegerField(db_column='FleteSocioIM', blank=True, null=True)  # Field name made lowercase.
    fletesocioia = models.IntegerField(db_column='FleteSocioIA', blank=True, null=True)  # Field name made lowercase.
    fletesocioit = models.IntegerField(db_column='FleteSocioIT', blank=True, null=True)  # Field name made lowercase.
    fletesocioem = models.IntegerField(db_column='FleteSocioEM', blank=True, null=True)  # Field name made lowercase.
    fletesocioea = models.IntegerField(db_column='FleteSocioEA', blank=True, null=True)  # Field name made lowercase.
    fletesocioet = models.IntegerField(db_column='FleteSocioET', blank=True, null=True)  # Field name made lowercase.
    direccion2 = models.CharField(db_column='Direccion2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    origencliente = models.CharField(db_column='OrigenCliente', max_length=1, blank=True, null=True)  # Field name made lowercase.
    casillero = models.CharField(db_column='Casillero', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cedulaid = models.CharField(db_column='CedulaID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    inscripcion = models.CharField(db_column='Inscripcion', max_length=19, blank=True, null=True)  # Field name made lowercase.
    vtoinscripcion = models.CharField(db_column='VtoInscripcion', max_length=19, blank=True, null=True)  # Field name made lowercase.
    facturaelectronica = models.CharField(db_column='FacturaElectronica', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emailfe = models.CharField(db_column='eMailFe', max_length=37, blank=True, null=True)  # Field name made lowercase.
    telefonocasa = models.CharField(db_column='TelefonoCasa', max_length=3, blank=True, null=True)  # Field name made lowercase.
    telefonocelular = models.CharField(db_column='TelefonoCelular', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fechacumple = models.CharField(db_column='FechaCumple', max_length=19, blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=3, blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='Municipio', max_length=3, blank=True, null=True)  # Field name made lowercase.
    inscestadual = models.CharField(db_column='InscEstadual', max_length=3, blank=True, null=True)  # Field name made lowercase.
    inscmunicipal = models.CharField(db_column='InscMunicipal', max_length=3, blank=True, null=True)  # Field name made lowercase.
    solocontado = models.CharField(db_column='SoloContado', max_length=1, blank=True, null=True)  # Field name made lowercase.
    iibbbue = models.CharField(db_column='IIBBBue', max_length=1, blank=True, null=True)  # Field name made lowercase.
    estaxid = models.CharField(db_column='EsTaxID', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enviocc = models.CharField(db_column='EnvioCC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    modoenviocc = models.CharField(db_column='ModoEnvioCC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ciudadnombre = models.CharField(db_column='CiudadNombre', max_length=25, blank=True, null=True)  # Field name made lowercase.
    idestado = models.CharField(db_column='IDEstado', max_length=9, blank=True, null=True)  # Field name made lowercase.
    idpais = models.CharField(db_column='IDPais', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tccambioar = models.DecimalField(db_column='TcCambioAR', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    paiscia = models.CharField(db_column='PaisCia', max_length=3, blank=True, null=True)  # Field name made lowercase.
    encargadocuenta = models.CharField(db_column='EncargadoCuenta', max_length=3, blank=True, null=True)  # Field name made lowercase.
    bancoproveedor = models.CharField(db_column='BancoProveedor', max_length=3, blank=True, null=True)  # Field name made lowercase.
    profitea = models.CharField(db_column='ProfitEA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitem = models.CharField(db_column='ProfitEM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitet = models.CharField(db_column='ProfitET', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitia = models.CharField(db_column='ProfitIA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitim = models.CharField(db_column='ProfitIM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    profitit = models.CharField(db_column='ProfitIT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nroibb = models.IntegerField(db_column='NroIBB', blank=True, null=True)  # Field name made lowercase.
    interes = models.DecimalField(db_column='Interes', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    emailcb = models.CharField(db_column='EmailCB', max_length=235, blank=True, null=True)  # Field name made lowercase.
    contactocb = models.CharField(db_column='ContactoCB', max_length=44, blank=True, null=True)  # Field name made lowercase.
    nroata = models.CharField(db_column='NroATA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    preferido = models.IntegerField(db_column='Preferido', blank=True, null=True)  # Field name made lowercase.
    razonsocial2 = models.CharField(db_column='RazonSocial2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emaillg = models.CharField(db_column='EmailLG', max_length=235, blank=True, null=True)  # Field name made lowercase.
    contactolg = models.CharField(db_column='ContactoLG', max_length=44, blank=True, null=True)  # Field name made lowercase.
    nrointtra = models.CharField(db_column='NroInttra', blank=True, null=True)  # Field name made lowercase.
    limiteautorizado = models.CharField(db_column='LimiteAutorizado', blank=True, null=True)  # Field name made lowercase.
    limitedisponible = models.CharField(db_column='LimiteDisponible', blank=True, null=True)  # Field name made lowercase.
    terminos = models.CharField(db_column='Terminos', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tipoindustria = models.IntegerField(db_column='TipoIndustria', blank=True, null=True)  # Field name made lowercase.
    fechaactualizado = models.CharField(db_column='FechaActualizado', blank=True, null=True)  # Field name made lowercase.
    coddespachante = models.CharField(db_column='CodDespachante', max_length=1, blank=True, null=True)  # Field name made lowercase.
    codagente = models.CharField(db_column='CodAgente', max_length=1, blank=True, null=True)  # Field name made lowercase.
    coddeposito = models.CharField(db_column='CodDeposito', max_length=1, blank=True, null=True)  # Field name made lowercase.
    envioiata = models.CharField(db_column='EnvioIATA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emailefreight = models.CharField(db_column='EmailEFreight', max_length=3, blank=True, null=True)  # Field name made lowercase.
    usdenegado = models.CharField(db_column='UsDenegado', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechadenegado = models.CharField(db_column='FechaDenegado', max_length=19, blank=True, null=True)  # Field name made lowercase.
    fecharevusdenegado = models.CharField(db_column='FechaRevUsDenegado', max_length=19, blank=True, null=True)  # Field name made lowercase.
    ctarembvta = models.IntegerField(db_column='CtaRembVta', blank=True, null=True)  # Field name made lowercase.
    ctarembcpa = models.IntegerField(db_column='CtaRembCpa', blank=True, null=True)  # Field name made lowercase.
    pima = models.CharField(db_column='PIMA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    envelope = models.CharField(db_column='Envelope', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idtipodocumento = models.IntegerField(db_column='idTipoDocumento', blank=True, null=True)  # Field name made lowercase.
    comportamientoplazo = models.CharField(db_column='ComportamientoPlazo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    comisioncalcula = models.CharField(db_column='ComisionCalcula', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bonificacionincluyeiva = models.CharField(db_column='BonificacionIncluyeIVA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    comisionincluyeiva = models.CharField(db_column='ComisionIncluyeIVA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tipocuentabanco = models.CharField(db_column='TipoCuentaBanco', max_length=1, blank=True, null=True)  # Field name made lowercase.
    numerocuentabanco = models.CharField(db_column='NumeroCuentaBanco', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tipotransferbanco = models.CharField(db_column='TipoTransferBanco', max_length=3, blank=True, null=True)  # Field name made lowercase.
    qbli = models.CharField(db_column='QBLi', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cainro = models.CharField(db_column='CaiNro', max_length=3, blank=True, null=True)  # Field name made lowercase.
    caivto = models.CharField(db_column='CaiVto', max_length=19, blank=True, null=True)  # Field name made lowercase.
    coordinador = models.CharField(db_column='Coordinador', max_length=3, blank=True, null=True)  # Field name made lowercase.
    empresachino = models.CharField(db_column='EmpresaChino', max_length=3, blank=True, null=True)  # Field name made lowercase.
    direccionchino = models.CharField(db_column='DireccionChino', max_length=3, blank=True, null=True)  # Field name made lowercase.
    direccionchino2 = models.CharField(db_column='DireccionChino2', max_length=3, blank=True, null=True)  # Field name made lowercase.
    preferenciales = models.CharField(db_column='Preferenciales', max_length=1, blank=True, null=True)  # Field name made lowercase.
    plazolg = models.CharField(db_column='PlazoLG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pagodocumentado = models.CharField(db_column='PagoDocumentado', max_length=1, blank=True, null=True)  # Field name made lowercase.
    formapago = models.IntegerField(db_column='FormaPago', blank=True, null=True)  # Field name made lowercase.
    iibbcap = models.CharField(db_column='IIBBCap', max_length=1, blank=True, null=True)  # Field name made lowercase.
    chequeado = models.CharField(db_column='Chequeado', max_length=1, blank=True, null=True)  # Field name made lowercase.
    formadepagosat = models.CharField(db_column='FormaDePagoSAT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    metododepagosat = models.CharField(db_column='MetodoDePagoSAT', max_length=3, blank=True, null=True)  # Field name made lowercase.
    usocfdisat = models.CharField(db_column='UsoCFDISAT', max_length=3, blank=True, null=True)  # Field name made lowercase.
    webope = models.CharField(db_column='WebOpe', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webser = models.CharField(db_column='WebSer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webord = models.CharField(db_column='WebOrd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webbod = models.CharField(db_column='WebBod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    webadm = models.CharField(db_column='WebAdm', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appope = models.CharField(db_column='AppOpe', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appbod = models.CharField(db_column='AppBod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    appadm = models.CharField(db_column='AppAdm', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.clientes'


class Dtproperties(models.Model):
    id = models.CharField(blank=True, null=True)
    objectid = models.CharField(blank=True, null=True)
    property = models.CharField(blank=True, null=True)
    value = models.CharField(blank=True, null=True)
    lvalue = models.CharField(blank=True, null=True)
    version = models.CharField(blank=True, null=True)
    uvalue = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '.dtproperties'


class Edimonedas(models.Model):
    agente = models.CharField(blank=True, null=True)
    origen = models.CharField(blank=True, null=True)
    codorigen = models.CharField(blank=True, null=True)
    coddestino = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '.edimonedas'


class Ediproductos(models.Model):
    agente = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    codorigen = models.IntegerField(blank=True, null=True)
    coddestino = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '.ediproductos'


class Ediservicios(models.Model):
    agente = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    codorigen = models.SmallIntegerField(blank=True, null=True)
    coddestino = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '.ediservicios'


class Edisocios(models.Model):
    agente = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    codorigen = models.SmallIntegerField(blank=True, null=True)
    coddestino = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '.edisocios'


class Guias(models.Model):
    transportista = models.SmallIntegerField(blank=True, null=True)
    prefijo = models.SmallIntegerField(blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    refmaster = models.SmallIntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(max_length=19, blank=True, null=True)
    sucursal = models.CharField(db_column='Sucursal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.guias'


class Paises(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    continente = models.IntegerField(blank=True, null=True)
    iata = models.IntegerField(blank=True, null=True)
    idinternacional = models.CharField(max_length=3, blank=True, null=True)
    cuit = models.CharField(max_length=3, blank=True, null=True)
    cartelef = models.CharField(blank=True, null=True)
    edi = models.CharField(db_column='EDI', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.paises'


class Productos(models.Model):
    codigo = models.SmallIntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.CharField(max_length=3, blank=True, null=True)
    peligroso = models.IntegerField(blank=True, null=True)
    familia = models.CharField(blank=True, null=True)
    valioso = models.IntegerField(blank=True, null=True)
    perecedero = models.IntegerField(blank=True, null=True)
    nrocomm = models.IntegerField(blank=True, null=True)
    corporativo = models.CharField(max_length=1, blank=True, null=True)
    schedulebnumber = models.CharField(db_column='ScheduleBNumber', max_length=12, blank=True, null=True)  # Field name made lowercase.
    class_field = models.CharField(db_column='Class', max_length=3, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    un = models.CharField(db_column='UN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    packing = models.CharField(db_column='Packing', max_length=3, blank=True, null=True)  # Field name made lowercase.
    subrisk = models.CharField(db_column='SubRisk', max_length=3, blank=True, null=True)  # Field name made lowercase.
    aduanaentrada = models.CharField(db_column='AduanaEntrada', max_length=3, blank=True, null=True)  # Field name made lowercase.
    aduanasalida = models.CharField(db_column='AduanaSalida', max_length=3, blank=True, null=True)  # Field name made lowercase.
    temperatura = models.DecimalField(db_column='Temperatura', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hazardpage = models.CharField(db_column='HazardPage', max_length=3, blank=True, null=True)  # Field name made lowercase.
    hazardcodever = models.CharField(db_column='HazardCodeVer', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ems = models.CharField(db_column='EMS', max_length=3, blank=True, null=True)  # Field name made lowercase.
    termcard = models.CharField(db_column='TermCard', max_length=3, blank=True, null=True)  # Field name made lowercase.
    imocode2 = models.CharField(db_column='ImoCode2', max_length=3, blank=True, null=True)  # Field name made lowercase.
    imocode3 = models.CharField(db_column='ImoCode3', max_length=3, blank=True, null=True)  # Field name made lowercase.
    psn = models.CharField(db_column='PSN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fechaactualizado = models.CharField(db_column='FechaActualizado', blank=True, null=True)  # Field name made lowercase.
    ncm = models.CharField(db_column='NCM', max_length=3, blank=True, null=True)  # Field name made lowercase.
    shc = models.CharField(db_column='SHC', blank=True, null=True)  # Field name made lowercase.
    dgc = models.CharField(db_column='DGC', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.productos'


class Sysregisedits(models.Model):
    numerolic = models.CharField(db_column='NumeroLic', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    equipo = models.CharField(db_column='Equipo', blank=True, null=True)  # Field name made lowercase.
    registro = models.CharField(db_column='Registro', blank=True, null=True)  # Field name made lowercase.
    vigencia = models.CharField(db_column='Vigencia', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.sysRegisEdits'


class Textos(models.Model):
    deposito = models.CharField(max_length=3, blank=True, null=True)
    agente = models.CharField(max_length=3, blank=True, null=True)
    cliente = models.TextField(blank=True, null=True)
    cotizaim = models.CharField(max_length=3, blank=True, null=True)
    cotizaia = models.CharField(max_length=3, blank=True, null=True)
    cotizaem = models.CharField(max_length=3, blank=True, null=True)
    cotizaea = models.CharField(max_length=3, blank=True, null=True)
    clienteia = models.TextField(blank=True, null=True)
    clienteit = models.CharField(max_length=3, blank=True, null=True)
    cotizait = models.CharField(max_length=20, blank=True, null=True)
    cotizaet = models.CharField(max_length=3, blank=True, null=True)
    clienteexa = models.TextField(blank=True, null=True)
    clienteexm = models.TextField(blank=True, null=True)
    clienteext = models.CharField(max_length=3, blank=True, null=True)
    cotgenerica = models.CharField(max_length=3, blank=True, null=True)
    seguircli = models.TextField(blank=True, null=True)
    seguirclii = models.CharField(max_length=3, blank=True, null=True)
    seguirage = models.CharField(max_length=3, blank=True, null=True)
    seguiragei = models.CharField(max_length=3, blank=True, null=True)
    general = models.CharField(max_length=3, blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)
    booking = models.CharField(db_column='Booking', blank=True, null=True)  # Field name made lowercase.
    textoaging = models.CharField(db_column='TextoAging', blank=True, null=True)  # Field name made lowercase.
    textoestadocuenta = models.CharField(db_column='TextoEstadoCuenta', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '.textos'


class CotizaAerea(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    aplica = models.CharField(max_length=1, blank=True, null=True)
    transportista = models.SmallIntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=5, blank=True, null=True)
    tarifa = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    bonifica = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    tipobonif = models.CharField(max_length=1, blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    aclaraciones = models.CharField(max_length=3, blank=True, null=True)
    directo = models.IntegerField(blank=True, null=True)
    frecuencia = models.CharField(max_length=15, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    aceptada = models.CharField(max_length=1, blank=True, null=True)
    enlace = models.CharField(max_length=1, blank=True, null=True)
    compra = models.IntegerField(blank=True, null=True)
    costo = models.DecimalField(db_column='Costo', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pinformar = models.DecimalField(db_column='Pinformar', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pagoflete = models.CharField(db_column='PagoFlete', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Aerea'


class CotizaAerea2(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    aplica = models.CharField(max_length=1, blank=True, null=True)
    transportista = models.SmallIntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=6, blank=True, null=True)
    tarifa = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    sugerida = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    bonifica = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    tipobonif = models.CharField(max_length=1, blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    aclaraciones = models.CharField(max_length=130, blank=True, null=True)
    comision = models.CharField(blank=True, null=True)
    directo = models.IntegerField(blank=True, null=True)
    frecuencia = models.CharField(max_length=9, blank=True, null=True)
    cliente = models.IntegerField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Aerea2'


class CotizaAttachhijo(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    archivo = models.CharField(db_column='Archivo', max_length=39, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=22, blank=True, null=True)  # Field name made lowercase.
    web = models.CharField(db_column='Web', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.AttachHijo'


class CotizaAttachrecibida(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    archivo = models.CharField(db_column='Archivo', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.AttachRecibida'


class CotizaCabecera(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    cliente = models.SmallIntegerField(blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    vigencia = models.CharField(max_length=19, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    propiaadqui = models.CharField(max_length=1, blank=True, null=True)
    vendedor = models.IntegerField(blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    contrato = models.CharField(max_length=25, blank=True, null=True)
    activa = models.CharField(db_column='Activa', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(max_length=1, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    incoterms = models.CharField(max_length=3, blank=True, null=True)
    contactar = models.CharField(max_length=1, blank=True, null=True)
    fechacontacto = models.CharField(max_length=19, blank=True, null=True)
    producto1 = models.IntegerField(blank=True, null=True)
    producto2 = models.IntegerField(blank=True, null=True)
    producto3 = models.IntegerField(blank=True, null=True)
    producto4 = models.IntegerField(blank=True, null=True)
    producto5 = models.IntegerField(blank=True, null=True)
    producto6 = models.IntegerField(blank=True, null=True)
    revisada = models.CharField(max_length=1, blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    comiexport = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    comimport = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    comimarexp = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    comimarimp = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    comiterexp = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    comiterimp = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    tipoexport = models.CharField(max_length=1, blank=True, null=True)
    tipoimport = models.CharField(max_length=1, blank=True, null=True)
    tipomarexp = models.CharField(max_length=1, blank=True, null=True)
    tipomarimp = models.CharField(max_length=1, blank=True, null=True)
    tipoterexp = models.CharField(max_length=1, blank=True, null=True)
    tipoterimp = models.CharField(max_length=1, blank=True, null=True)
    demora = models.IntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    embarcador = models.SmallIntegerField(blank=True, null=True)
    probabilidad = models.CharField(db_column='Probabilidad', max_length=4, blank=True, null=True)  # Field name made lowercase.
    motivorechazo = models.IntegerField(db_column='MotivoRechazo', blank=True, null=True)  # Field name made lowercase.
    trafico = models.IntegerField(db_column='Trafico', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', blank=True, null=True)  # Field name made lowercase.
    fechageneracion = models.CharField(db_column='FechaGeneracion', max_length=19, blank=True, null=True)  # Field name made lowercase.
    fechaenvio = models.CharField(db_column='FechaEnvio', max_length=19, blank=True, null=True)  # Field name made lowercase.
    refcliente = models.CharField(db_column='RefCliente', max_length=42, blank=True, null=True)  # Field name made lowercase.
    valordemoravta = models.DecimalField(db_column='ValorDemoraVTA', max_digits=8, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=8, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    diasalmacenaje = models.IntegerField(db_column='DiasAlmacenaje', blank=True, null=True)  # Field name made lowercase.
    fechasolicitud = models.CharField(db_column='FechaSolicitud', max_length=19, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=9, blank=True, null=True)  # Field name made lowercase.
    sucursal = models.CharField(db_column='Sucursal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    descmercaderia = models.CharField(db_column='DescMercaderia', max_length=200, blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=16, blank=True, null=True)  # Field name made lowercase.
    actividad = models.IntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Cabecera'


class CotizaCargaaerea(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    medidas = models.CharField(max_length=3, blank=True, null=True)
    tipo = models.CharField(max_length=7, blank=True, null=True)
    cbm = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Cotiza.Cargaaerea'


class CotizaEnvases(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    unidad = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=3, blank=True, null=True)
    movimiento = models.CharField(max_length=7, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    peso = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    volumen = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    pinformar = models.DecimalField(db_column='Pinformar', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Envases'


class CotizaEspecifica(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    modo = models.CharField(max_length=15, blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    volumencubico = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    tomopeso = models.IntegerField(blank=True, null=True)
    aplicable = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    tarifaventa = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    tarifafija = models.CharField(max_length=1, blank=True, null=True)
    tipobonifcli = models.CharField(max_length=1, blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    pagoflete = models.CharField(max_length=1, blank=True, null=True)
    ordencliente = models.CharField(max_length=3, blank=True, null=True)
    enlace = models.CharField(max_length=1, blank=True, null=True)
    aceptada = models.CharField(max_length=1, blank=True, null=True)
    moneda = models.DecimalField(db_column='Moneda', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    compra = models.IntegerField(db_column='Compra', blank=True, null=True)  # Field name made lowercase.
    pinformar = models.DecimalField(db_column='Pinformar', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    tarifacompra = models.DecimalField(db_column='TarifaCompra', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    transportista = models.SmallIntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    aclaraciones = models.CharField(db_column='Aclaraciones', max_length=23, blank=True, null=True)  # Field name made lowercase.
    arbitraje = models.DecimalField(db_column='Arbitraje', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    localint = models.CharField(db_column='LocalInt', blank=True, null=True)  # Field name made lowercase.
    directo = models.IntegerField(db_column='Directo', blank=True, null=True)  # Field name made lowercase.
    frecuencia = models.CharField(db_column='Frecuencia', max_length=3, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=3, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Especifica'


class CotizaFaxes(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.CharField(max_length=95, blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Faxes'


class CotizaFaxesre(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    asunto = models.CharField(db_column='Asunto', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.FaxesRe'


class CotizaGastos(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    filtro = models.CharField(max_length=1, blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    pago = models.CharField(max_length=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=17, blank=True, null=True)
    detalle = models.CharField(max_length=89, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    costo = models.DecimalField(db_column='Costo', max_digits=8, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pinformar = models.DecimalField(db_column='Pinformar', max_digits=8, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    notomaprofit = models.IntegerField(db_column='Notomaprofit', blank=True, null=True)  # Field name made lowercase.
    secomparte = models.CharField(db_column='Secomparte', max_length=1, blank=True, null=True)  # Field name made lowercase.
    costoinicial = models.DecimalField(db_column='CostoInicial', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Gastos'


class CotizaGastos2(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    filtro = models.CharField(max_length=1, blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    pago = models.CharField(max_length=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=13, blank=True, null=True)
    detalle = models.CharField(max_length=29, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    sugerida = models.DecimalField(db_column='Sugerida', max_digits=6, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    costoinicial = models.DecimalField(db_column='CostoInicial', max_digits=6, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Gastos2'


class CotizaGastoshijos(models.Model):
    cliente = models.SmallIntegerField(blank=True, null=True)
    codigo = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    tipogasto = models.CharField(max_length=13, blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=14, blank=True, null=True)
    modulo = models.CharField(max_length=15, blank=True, null=True)
    costo = models.DecimalField(db_column='Costo', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.GastosHijos'


class CotizaMarit2(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    transportista = models.IntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    sugerida = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    bonifica = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    rango1 = models.IntegerField(db_column='Rango1', blank=True, null=True)  # Field name made lowercase.
    rango2 = models.IntegerField(db_column='Rango2', blank=True, null=True)  # Field name made lowercase.
    unidad = models.CharField(db_column='Unidad', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=14, blank=True, null=True)  # Field name made lowercase.
    movimiento = models.CharField(db_column='Movimiento', max_length=7, blank=True, null=True)  # Field name made lowercase.
    terminos = models.CharField(db_column='Terminos', max_length=4, blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    aclaraciones = models.CharField(max_length=3, blank=True, null=True)
    baf = models.CharField(blank=True, null=True)
    porbaf = models.CharField(blank=True, null=True)
    directo = models.IntegerField(blank=True, null=True)
    frecuencia = models.CharField(max_length=7, blank=True, null=True)
    demora = models.IntegerField(db_column='Demora', blank=True, null=True)  # Field name made lowercase.
    valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    cliente = models.IntegerField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=3, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Marit2'


class CotizaMaritima(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    transportista = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    bonifica = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    rango1 = models.IntegerField(db_column='Rango1', blank=True, null=True)  # Field name made lowercase.
    rango2 = models.IntegerField(db_column='Rango2', blank=True, null=True)  # Field name made lowercase.
    unidad = models.CharField(db_column='Unidad', max_length=4, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=14, blank=True, null=True)  # Field name made lowercase.
    movimiento = models.CharField(db_column='Movimiento', max_length=10, blank=True, null=True)  # Field name made lowercase.
    terminos = models.CharField(db_column='Terminos', max_length=4, blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    aclaraciones = models.CharField(max_length=3, blank=True, null=True)
    baf = models.CharField(blank=True, null=True)
    porbaf = models.CharField(blank=True, null=True)
    directo = models.IntegerField(blank=True, null=True)
    frecuencia = models.CharField(max_length=14, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    aceptada = models.CharField(max_length=1, blank=True, null=True)
    enlace = models.CharField(max_length=1, blank=True, null=True)
    compra = models.IntegerField(blank=True, null=True)
    costo = models.DecimalField(db_column='Costo', max_digits=8, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pinformar = models.DecimalField(db_column='Pinformar', max_digits=8, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pagoflete = models.CharField(db_column='PagoFlete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=3, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Maritima'


class CotizaObjetivos(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.
    operacion = models.CharField(db_column='Operacion', blank=True, null=True)  # Field name made lowercase.
    objetivousd = models.CharField(db_column='ObjetivoUSD', blank=True, null=True)  # Field name made lowercase.
    objetivotons = models.CharField(db_column='ObjetivoTons', blank=True, null=True)  # Field name made lowercase.
    objetivocbm = models.CharField(db_column='ObjetivoCBM', blank=True, null=True)  # Field name made lowercase.
    objetivoteus = models.CharField(db_column='ObjetivoTEUS', blank=True, null=True)  # Field name made lowercase.
    objetivo20 = models.CharField(db_column='Objetivo20', blank=True, null=True)  # Field name made lowercase.
    objetivo40 = models.CharField(db_column='Objetivo40', blank=True, null=True)  # Field name made lowercase.
    desde = models.CharField(db_column='Desde', blank=True, null=True)  # Field name made lowercase.
    hasta = models.CharField(db_column='Hasta', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', blank=True, null=True)  # Field name made lowercase.
    organizacion = models.CharField(db_column='Organizacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Objetivos'


class CotizaRecibidas(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    proveedor = models.SmallIntegerField(blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    vigencia = models.CharField(max_length=19, blank=True, null=True)
    observaciones = models.CharField(max_length=42, blank=True, null=True)
    contrato = models.CharField(max_length=9, blank=True, null=True)
    activa = models.CharField(db_column='Activa', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(max_length=1, blank=True, null=True)
    producto1 = models.IntegerField(blank=True, null=True)
    producto2 = models.IntegerField(blank=True, null=True)
    producto3 = models.IntegerField(blank=True, null=True)
    producto4 = models.IntegerField(blank=True, null=True)
    producto5 = models.IntegerField(blank=True, null=True)
    producto6 = models.IntegerField(blank=True, null=True)
    trafico = models.IntegerField(db_column='Trafico', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', blank=True, null=True)  # Field name made lowercase.
    registrointerno = models.CharField(db_column='RegistroInterno', max_length=3, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Recibidas'


class CotizaTierra(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    transportista = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    bonifica = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    rango1 = models.IntegerField(db_column='Rango1', blank=True, null=True)  # Field name made lowercase.
    rango2 = models.IntegerField(db_column='Rango2', blank=True, null=True)  # Field name made lowercase.
    unidad = models.CharField(db_column='Unidad', max_length=12, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=3, blank=True, null=True)  # Field name made lowercase.
    movimiento = models.CharField(db_column='Movimiento', max_length=9, blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    aclaraciones = models.CharField(max_length=3, blank=True, null=True)
    directo = models.IntegerField(blank=True, null=True)
    frecuencia = models.CharField(max_length=3, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    aceptada = models.CharField(max_length=1, blank=True, null=True)
    enlace = models.CharField(max_length=1, blank=True, null=True)
    compra = models.IntegerField(blank=True, null=True)
    costo = models.DecimalField(db_column='Costo', max_digits=6, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pinformar = models.DecimalField(db_column='Pinformar', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    pagoflete = models.CharField(db_column='PagoFlete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    masiva = models.CharField(db_column='MasIVA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    allin = models.CharField(db_column='AllIn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    localint = models.CharField(db_column='LocalInt', max_length=13, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Tierra'


class CotizaTierra2(models.Model):
    numero = models.CharField(blank=True, null=True)
    moneda = models.CharField(blank=True, null=True)
    transportista = models.CharField(blank=True, null=True)
    precio = models.CharField(blank=True, null=True)
    sugerida = models.CharField(blank=True, null=True)
    bonifica = models.CharField(blank=True, null=True)
    rango1 = models.CharField(db_column='Rango1', blank=True, null=True)  # Field name made lowercase.
    rango2 = models.CharField(db_column='Rango2', blank=True, null=True)  # Field name made lowercase.
    unidad = models.CharField(db_column='Unidad', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    movimiento = models.CharField(db_column='Movimiento', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(blank=True, null=True)
    destino = models.CharField(blank=True, null=True)
    aclaraciones = models.CharField(blank=True, null=True)
    directo = models.CharField(blank=True, null=True)
    frecuencia = models.CharField(blank=True, null=True)
    masiva = models.CharField(db_column='MasIVA', blank=True, null=True)  # Field name made lowercase.
    allin = models.CharField(db_column='AllIn', blank=True, null=True)  # Field name made lowercase.
    localint = models.CharField(db_column='LocalInt', blank=True, null=True)  # Field name made lowercase.
    cliente = models.CharField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.Tierra2'


class CotizaTracecm(models.Model):
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=11, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=109, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=7, blank=True, null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cotiza.TraceCM'


class DatasetActivofijo(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.
    autogenerado = models.CharField(db_column='Autogenerado', blank=True, null=True)  # Field name made lowercase.
    grupo = models.CharField(db_column='Grupo', blank=True, null=True)  # Field name made lowercase.
    numeroserie = models.CharField(db_column='NumeroSerie', blank=True, null=True)  # Field name made lowercase.
    garantia = models.CharField(db_column='Garantia', blank=True, null=True)  # Field name made lowercase.
    vtogarantia = models.CharField(db_column='VtoGarantia', blank=True, null=True)  # Field name made lowercase.
    seguro = models.CharField(db_column='Seguro', blank=True, null=True)  # Field name made lowercase.
    aseguradora = models.CharField(db_column='Aseguradora', blank=True, null=True)  # Field name made lowercase.
    poliza = models.CharField(db_column='Poliza', blank=True, null=True)  # Field name made lowercase.
    ubicacion = models.CharField(db_column='Ubicacion', blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', blank=True, null=True)  # Field name made lowercase.
    fechabaja = models.CharField(db_column='FechaBaja', blank=True, null=True)  # Field name made lowercase.
    destinofinal = models.CharField(db_column='DestinoFinal', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    monedavalorminimo = models.CharField(db_column='MonedaValorMinimo', blank=True, null=True)  # Field name made lowercase.
    valorminimo = models.CharField(db_column='ValorMinimo', blank=True, null=True)  # Field name made lowercase.
    anosdepreciacion = models.CharField(db_column='AnosDepreciacion', blank=True, null=True)  # Field name made lowercase.
    porcentaje = models.CharField(db_column='Porcentaje', blank=True, null=True)  # Field name made lowercase.
    anosdepreciacionniif = models.CharField(db_column='AnosDepreciacionNIIF', blank=True, null=True)  # Field name made lowercase.
    porcentajeniif = models.CharField(db_column='PorcentajeNIIF', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    valor = models.CharField(db_column='Valor', blank=True, null=True)  # Field name made lowercase.
    ctaactivo = models.CharField(db_column='CtaActivo', blank=True, null=True)  # Field name made lowercase.
    cuota = models.CharField(db_column='Cuota', blank=True, null=True)  # Field name made lowercase.
    cuotaniif = models.CharField(db_column='CuotaNIIF', blank=True, null=True)  # Field name made lowercase.
    modocalculo = models.CharField(db_column='ModoCalculo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ActivoFijo'


class DatasetAmortactivofijo(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    asiento = models.CharField(db_column='Asiento', blank=True, null=True)  # Field name made lowercase.
    valororiginal = models.CharField(db_column='ValorOriginal', blank=True, null=True)  # Field name made lowercase.
    valornuevo = models.CharField(db_column='ValorNuevo', blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', blank=True, null=True)  # Field name made lowercase.
    niif = models.CharField(db_column='Niif', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.AmortActivoFijo'


class DatasetAreas(models.Model):
    numero = models.CharField(blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Areas'


class DatasetAsientos(models.Model):
    fecha = models.CharField(max_length=19, blank=True, null=True)
    cuenta = models.IntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    monto = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    cambio = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=101, blank=True, null=True)
    asiento = models.CharField(max_length=19, blank=True, null=True)
    imputacion = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    documento = models.CharField(max_length=20, blank=True, null=True)
    vto = models.CharField(max_length=19, blank=True, null=True)
    pasado = models.IntegerField(blank=True, null=True)
    autogenerado = models.CharField(max_length=39, blank=True, null=True)
    cliente = models.SmallIntegerField(blank=True, null=True)
    banco = models.CharField(max_length=25, blank=True, null=True)
    centro = models.CharField(max_length=3, blank=True, null=True)
    mov = models.CharField(max_length=16, blank=True, null=True)
    mesimpu = models.IntegerField(blank=True, null=True)
    anoimpu = models.SmallIntegerField(blank=True, null=True)
    conciliado = models.CharField(max_length=1, blank=True, null=True)
    estacion = models.IntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=15, blank=True, null=True)
    enviado = models.CharField(blank=True, null=True)
    clearing = models.CharField(max_length=19, blank=True, null=True)
    voucher = models.IntegerField(blank=True, null=True)
    revertir = models.CharField(max_length=1, blank=True, null=True)
    fecrevertir = models.CharField(max_length=19, blank=True, null=True)
    area = models.CharField(max_length=1, blank=True, null=True)
    iniciales = models.CharField(db_column='Iniciales', max_length=3, blank=True, null=True)  # Field name made lowercase.
    paridad = models.DecimalField(db_column='Paridad', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    numeroenvio = models.CharField(db_column='NumeroEnvio', blank=True, null=True)  # Field name made lowercase.
    vinculo = models.CharField(db_column='Vinculo', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sociocom = models.CharField(db_column='SocioCom', max_length=1, blank=True, null=True)  # Field name made lowercase.
    monedaorigen = models.CharField(db_column='MonedaOrigen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tccorreccion = models.CharField(db_column='TCCorreccion', blank=True, null=True)  # Field name made lowercase.
    parcorreccion = models.CharField(db_column='ParCorreccion', blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=8, blank=True, null=True)  # Field name made lowercase.
    fechaemision = models.CharField(db_column='FechaEmision', blank=True, null=True)  # Field name made lowercase.
    fechavencimiento = models.CharField(db_column='FechaVencimiento', blank=True, null=True)  # Field name made lowercase.
    nrocomprobante = models.CharField(db_column='NroComprobante', blank=True, null=True)  # Field name made lowercase.
    desretencion = models.CharField(db_column='DesRetencion', blank=True, null=True)  # Field name made lowercase.
    baseimponible = models.CharField(db_column='BaseImponible', max_length=6, blank=True, null=True)  # Field name made lowercase.
    control = models.CharField(db_column='Control', max_length=1, blank=True, null=True)  # Field name made lowercase.
    base = models.CharField(db_column='Base', max_length=9, blank=True, null=True)  # Field name made lowercase.
    jurisdiccion = models.CharField(db_column='Jurisdiccion', blank=True, null=True)  # Field name made lowercase.
    nroserv = models.CharField(db_column='NroServ', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fechacheque = models.CharField(db_column='FechaCheque', max_length=19, blank=True, null=True)  # Field name made lowercase.
    bancooridest = models.CharField(db_column='BancoOriDest', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cuentaoridest = models.CharField(db_column='CuentaOriDest', max_length=10, blank=True, null=True)  # Field name made lowercase.
    linkretencion = models.CharField(db_column='LinkRetencion', blank=True, null=True)  # Field name made lowercase.
    foliofiscal = models.CharField(db_column='FolioFiscal', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Asientos'


class DatasetAsociadosresg(models.Model):
    rautogen = models.CharField(db_column='rAutogen', blank=True, null=True)  # Field name made lowercase.
    rautogenasociado = models.CharField(db_column='rAutogenAsociado', blank=True, null=True)  # Field name made lowercase.
    rformret = models.CharField(db_column='rFormRet', blank=True, null=True)  # Field name made lowercase.
    rcodret = models.CharField(db_column='rCodRet', blank=True, null=True)  # Field name made lowercase.
    rdescripcionret = models.CharField(db_column='rDescripcionRet', blank=True, null=True)  # Field name made lowercase.
    rtasa = models.CharField(db_column='rTasa', blank=True, null=True)  # Field name made lowercase.
    rmoneda = models.CharField(db_column='rMoneda', blank=True, null=True)  # Field name made lowercase.
    rvalor = models.CharField(db_column='rValor', blank=True, null=True)  # Field name made lowercase.
    rmontosujeto = models.CharField(db_column='rMontoSujeto', blank=True, null=True)  # Field name made lowercase.
    rtiporet = models.CharField(db_column='rTipoRet', blank=True, null=True)  # Field name made lowercase.
    rtipo = models.CharField(db_column='rTipo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.AsociadosResg'


class DatasetAttachasientos(models.Model):
    autogenerado = models.CharField(db_column='Autogenerado', blank=True, null=True)  # Field name made lowercase.
    archivo = models.CharField(db_column='Archivo', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.AttachAsientos'


class DatasetBoleta(models.Model):
    autogenerado = models.CharField(db_column='Autogenerado', max_length=26, blank=True, null=True)  # Field name made lowercase.
    tipo = models.IntegerField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    tipo2 = models.IntegerField(db_column='Tipo2', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    vto = models.CharField(db_column='Vto', max_length=19, blank=True, null=True)  # Field name made lowercase.
    sucursal = models.IntegerField(db_column='Sucursal', blank=True, null=True)  # Field name made lowercase.
    tipofactura = models.CharField(db_column='TipoFactura', max_length=1, blank=True, null=True)  # Field name made lowercase.
    serie = models.CharField(db_column='Serie', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prefijo = models.IntegerField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    numero = models.DecimalField(db_column='Numero', max_digits=6, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    linea = models.IntegerField(db_column='Linea', blank=True, null=True)  # Field name made lowercase.
    nrocliente = models.SmallIntegerField(db_column='NroCliente', blank=True, null=True)  # Field name made lowercase.
    cliente = models.CharField(db_column='Cliente', max_length=50, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    direccion2 = models.CharField(db_column='Direccion2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', max_length=24, blank=True, null=True)  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', max_length=21, blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=10, blank=True, null=True)  # Field name made lowercase.
    telefax = models.CharField(db_column='TeleFax', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ruc = models.CharField(db_column='Ruc', max_length=23, blank=True, null=True)  # Field name made lowercase.
    ibruto = models.CharField(db_column='IBruto', max_length=1, blank=True, null=True)  # Field name made lowercase.
    condiciones = models.CharField(db_column='Condiciones', max_length=3, blank=True, null=True)  # Field name made lowercase.
    corporativo = models.CharField(db_column='Corporativo', max_length=3, blank=True, null=True)  # Field name made lowercase.
    refer = models.CharField(db_column='Refer', max_length=8, blank=True, null=True)  # Field name made lowercase.
    carrier = models.CharField(db_column='Carrier', max_length=20, blank=True, null=True)  # Field name made lowercase.
    master = models.CharField(db_column='Master', max_length=20, blank=True, null=True)  # Field name made lowercase.
    house = models.CharField(db_column='House', max_length=42, blank=True, null=True)  # Field name made lowercase.
    vuelo = models.CharField(db_column='Vuelo', max_length=29, blank=True, null=True)  # Field name made lowercase.
    nroservicio = models.SmallIntegerField(db_column='NroServicio', blank=True, null=True)  # Field name made lowercase.
    concepto = models.CharField(db_column='Concepto', max_length=72, blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    iva = models.CharField(db_column='Iva', max_length=6, blank=True, null=True)  # Field name made lowercase.
    monto = models.DecimalField(db_column='Monto', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    monedalinea = models.IntegerField(db_column='MonedaLinea', blank=True, null=True)  # Field name made lowercase.
    totiva = models.DecimalField(db_column='TotIVA', max_digits=8, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    totsobre = models.DecimalField(db_column='TotSobre', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    anticiposcobrados = models.DecimalField(db_column='AnticiposCobrados', max_digits=8, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    moneda = models.IntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    cambio = models.DecimalField(db_column='Cambio', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    paridad = models.DecimalField(db_column='Paridad', max_digits=6, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    montooriginal = models.DecimalField(db_column='MontoOriginal', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=15, blank=True, null=True)  # Field name made lowercase.
    monedaemba = models.IntegerField(db_column='MonedaEmba', blank=True, null=True)  # Field name made lowercase.
    tcaemba = models.DecimalField(db_column='TcaEmba', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    kilos = models.DecimalField(db_column='Kilos', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    aplicable = models.DecimalField(db_column='Aplicable', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    volumen = models.DecimalField(db_column='Volumen', max_digits=8, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    bultos = models.IntegerField(db_column='Bultos', blank=True, null=True)  # Field name made lowercase.
    terminos = models.CharField(db_column='Terminos', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pagoflete = models.CharField(db_column='PagoFlete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=3, blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=28, blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=23, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    seguimiento = models.IntegerField(db_column='Seguimiento', blank=True, null=True)  # Field name made lowercase.
    texto1 = models.CharField(db_column='Texto1', max_length=51, blank=True, null=True)  # Field name made lowercase.
    texto2 = models.CharField(db_column='Texto2', max_length=52, blank=True, null=True)  # Field name made lowercase.
    texto3 = models.CharField(db_column='Texto3', max_length=52, blank=True, null=True)  # Field name made lowercase.
    texto4 = models.CharField(db_column='Texto4', max_length=52, blank=True, null=True)  # Field name made lowercase.
    texto5 = models.CharField(db_column='Texto5', max_length=3, blank=True, null=True)  # Field name made lowercase.
    llegasale = models.CharField(db_column='LlegaSale', max_length=19, blank=True, null=True)  # Field name made lowercase.
    commodity = models.CharField(db_column='Commodity', max_length=39, blank=True, null=True)  # Field name made lowercase.
    embarcador = models.CharField(db_column='Embarcador', max_length=50, blank=True, null=True)  # Field name made lowercase.
    consignatario = models.CharField(db_column='Consignatario', max_length=50, blank=True, null=True)  # Field name made lowercase.
    agente = models.CharField(db_column='Agente', max_length=50, blank=True, null=True)  # Field name made lowercase.
    orden = models.CharField(db_column='Orden', max_length=47, blank=True, null=True)  # Field name made lowercase.
    wr = models.CharField(db_column='Wr', max_length=13, blank=True, null=True)  # Field name made lowercase.
    iniciales = models.CharField(db_column='Iniciales', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ordenbolivia = models.CharField(db_column='OrdenBolivia', max_length=3, blank=True, null=True)  # Field name made lowercase.
    nrosat = models.IntegerField(db_column='NroSAT', blank=True, null=True)  # Field name made lowercase.
    anosat = models.IntegerField(db_column='AnoSAT', blank=True, null=True)  # Field name made lowercase.
    idfiscal = models.CharField(db_column='IdFiscal', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tipocliente = models.CharField(db_column='TipoCliente', max_length=25, blank=True, null=True)  # Field name made lowercase.
    nrosatnc = models.IntegerField(db_column='NroSatNC', blank=True, null=True)  # Field name made lowercase.
    anosatnc = models.IntegerField(db_column='AnoSatNC', blank=True, null=True)  # Field name made lowercase.
    cliente2 = models.CharField(db_column='Cliente2', max_length=4, blank=True, null=True)  # Field name made lowercase.
    aimagen = models.CharField(db_column='Aimagen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cae = models.CharField(db_column='CAE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechavtocae = models.CharField(db_column='FechaVtoCAE', max_length=19, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Boleta'


class DatasetBoletaretenciones(models.Model):
    autogenerado = models.CharField(db_column='Autogenerado', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    monto = models.CharField(db_column='Monto', blank=True, null=True)  # Field name made lowercase.
    autorretenedor = models.CharField(db_column='Autorretenedor', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.BoletaRetenciones'


class DatasetCabreportes(models.Model):
    numero = models.CharField(blank=True, null=True)
    titulo = models.CharField(blank=True, null=True)
    netear = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Cabreportes'


class DatasetChequeorden(models.Model):
    cfecha = models.CharField(max_length=19, blank=True, null=True)
    cbanco = models.IntegerField(blank=True, null=True)
    cnumero = models.IntegerField(blank=True, null=True)
    cvto = models.CharField(max_length=19, blank=True, null=True)
    cmonto = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    corden = models.SmallIntegerField(blank=True, null=True)
    cmoneda = models.IntegerField(blank=True, null=True)
    chequeterceros = models.CharField(db_column='ChequeTerceros', max_length=1, blank=True, null=True)  # Field name made lowercase.
    clienteterceros = models.CharField(db_column='ClienteTerceros', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Chequeorden'


class DatasetChequeras(models.Model):
    estado = models.IntegerField(blank=True, null=True)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    sucursal = models.IntegerField(db_column='Sucursal', blank=True, null=True)  # Field name made lowercase.
    banco = models.IntegerField(db_column='Banco', blank=True, null=True)  # Field name made lowercase.
    cheque = models.CharField(db_column='Cheque', max_length=11, blank=True, null=True)  # Field name made lowercase.
    diferido = models.CharField(db_column='Diferido', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Chequeras'


class DatasetCheques(models.Model):
    cfecha = models.CharField(max_length=19, blank=True, null=True)
    cbanco = models.CharField(max_length=28, blank=True, null=True)
    cnumero = models.CharField(max_length=12, blank=True, null=True)
    cvto = models.CharField(max_length=19, blank=True, null=True)
    cmonto = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    cautogenerado = models.CharField(max_length=27, blank=True, null=True)
    cdetalle = models.CharField(max_length=49, blank=True, null=True)
    cmoneda = models.IntegerField(blank=True, null=True)
    cestado = models.IntegerField(blank=True, null=True)
    ccliente = models.SmallIntegerField(blank=True, null=True)
    cestadobco = models.IntegerField(blank=True, null=True)
    cnrodepos = models.CharField(max_length=18, blank=True, null=True)
    ctipo = models.CharField(max_length=2, blank=True, null=True)
    cproveedor = models.CharField(db_column='cProveedor', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cpago = models.CharField(db_column='cPago', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Cheques'


class DatasetClavefactura(models.Model):
    boleta = models.CharField(db_column='Boleta', max_length=11, blank=True, null=True)  # Field name made lowercase.
    prefijo = models.IntegerField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    tipo = models.IntegerField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    serie = models.CharField(db_column='Serie', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveFactura'


class DatasetClavefacturab(models.Model):
    boleta = models.CharField(blank=True, null=True)
    prefijo = models.CharField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveFacturaB'


class DatasetClavefacturac(models.Model):
    boleta = models.CharField(blank=True, null=True)
    prefijo = models.CharField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveFacturaC'


class DatasetClavefacturad(models.Model):
    boleta = models.CharField(db_column='Boleta', blank=True, null=True)  # Field name made lowercase.
    prefijo = models.CharField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveFacturaD'


class DatasetClavefacturae(models.Model):
    boleta = models.CharField(blank=True, null=True)
    prefijo = models.CharField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveFacturaE'


class DatasetClavefacturaf(models.Model):
    boleta = models.CharField(db_column='Boleta', blank=True, null=True)  # Field name made lowercase.
    prefijo = models.CharField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveFacturaF'


class DatasetClavefacturag(models.Model):
    boleta = models.CharField(db_column='Boleta', blank=True, null=True)  # Field name made lowercase.
    prefijo = models.CharField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveFacturaG'


class DatasetClavefacturah(models.Model):
    boleta = models.CharField(db_column='Boleta', blank=True, null=True)  # Field name made lowercase.
    prefijo = models.CharField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveFacturaH'


class DatasetClaveiibb(models.Model):
    boleta = models.CharField(db_column='Boleta', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveIIBB'


class DatasetClaveorden(models.Model):
    boleta = models.DecimalField(db_column='Boleta', max_digits=5, decimal_places=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveOrden'


class DatasetClavepreventa(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClavePreventa'


class DatasetClaverecibo(models.Model):
    boleta = models.CharField(db_column='Boleta', max_length=11, blank=True, null=True)  # Field name made lowercase.
    prefijo = models.IntegerField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveRecibo'


class DatasetClaverecibom(models.Model):
    boleta = models.DecimalField(db_column='Boleta', max_digits=6, decimal_places=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveReciboM'


class DatasetClavevoucher(models.Model):
    voucher = models.CharField(db_column='Voucher', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ClaveVoucher'


class DatasetCodigocontrol(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    keydosificacion = models.CharField(db_column='KeyDosificacion', blank=True, null=True)  # Field name made lowercase.
    codautorizacion = models.CharField(db_column='CodAutorizacion', blank=True, null=True)  # Field name made lowercase.
    fechainicio = models.CharField(db_column='FechaInicio', blank=True, null=True)  # Field name made lowercase.
    fechalimite = models.CharField(db_column='FechaLimite', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.CodigoControl'


class DatasetCodigossunat(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    signo = models.CharField(db_column='Signo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.CodigosSunat'


class DatasetConcilio(models.Model):
    banco = models.CharField(blank=True, null=True)
    documento = models.CharField(blank=True, null=True)
    tipo = models.CharField(blank=True, null=True)
    monto = models.CharField(blank=True, null=True)
    fecha = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Concilio'


class DatasetConfig(models.Model):
    ktema = models.CharField(max_length=57, blank=True, null=True)
    kdato = models.IntegerField(blank=True, null=True)
    id = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Config'


class DatasetContacompra(models.Model):
    contador = models.SmallIntegerField(db_column='Contador', blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.ContaCompra'


class DatasetCuentasocios(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    cuenta = models.CharField(db_column='Cuenta', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.
    exterior = models.CharField(db_column='Exterior', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.CuentaSocios'


class DatasetCuentas(models.Model):
    xcodigo = models.IntegerField(blank=True, null=True)
    xnombre = models.CharField(max_length=36, blank=True, null=True)
    xtipo = models.IntegerField(blank=True, null=True)
    xobservaciones = models.CharField(max_length=14, blank=True, null=True)
    xgrupo = models.CharField(max_length=10, blank=True, null=True)
    xmoneda = models.IntegerField(blank=True, null=True)
    xcalculadifpesos = models.CharField(blank=True, null=True)
    xcalculadifdolar = models.CharField(max_length=1, blank=True, null=True)
    xnivel1 = models.CharField(max_length=35, blank=True, null=True)
    presupuesto = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    objetivo = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    sobregiro = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    alternativo = models.IntegerField(blank=True, null=True)
    ordinal = models.IntegerField(blank=True, null=True)
    inflacion = models.CharField(max_length=1, blank=True, null=True)
    nombreingles = models.CharField(db_column='NombreIngles', max_length=16, blank=True, null=True)  # Field name made lowercase.
    codificada = models.CharField(db_column='Codificada', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bloqueodirecto = models.CharField(db_column='BloqueoDirecto', max_length=1, blank=True, null=True)  # Field name made lowercase.
    manejasocioscom = models.CharField(db_column='ManejaSociosCom', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vincular = models.CharField(db_column='Vincular', max_length=1, blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    brctaref = models.CharField(db_column='brCtaRef', max_length=3, blank=True, null=True)  # Field name made lowercase.
    compsaldo = models.CharField(db_column='CompSaldo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    xbanco = models.CharField(db_column='xBanco', max_length=1, blank=True, null=True)  # Field name made lowercase.
    xcuentabanco = models.CharField(db_column='xCuentaBanco', blank=True, null=True)  # Field name made lowercase.
    activofijo = models.CharField(db_column='ActivoFijo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cuentaniif = models.CharField(db_column='CuentaNIIF', max_length=5, blank=True, null=True)  # Field name made lowercase.
    aperturaporsocio = models.CharField(db_column='AperturaPorSocio', max_length=1, blank=True, null=True)  # Field name made lowercase.
    aplicacierreterceros = models.CharField(db_column='AplicaCierreTerceros', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Cuentas'


class DatasetCuentasniif(models.Model):
    xcodigo = models.CharField(db_column='xCodigo', blank=True, null=True)  # Field name made lowercase.
    xnombre = models.CharField(db_column='xNombre', blank=True, null=True)  # Field name made lowercase.
    nombreingles = models.CharField(db_column='NombreIngles', blank=True, null=True)  # Field name made lowercase.
    xgrupo = models.CharField(db_column='xGrupo', blank=True, null=True)  # Field name made lowercase.
    xnivel1 = models.CharField(db_column='xNivel1', blank=True, null=True)  # Field name made lowercase.
    xobservaciones = models.CharField(db_column='xObservaciones', blank=True, null=True)  # Field name made lowercase.
    codificada = models.CharField(db_column='Codificada', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.CuentasNIIF'


class DatasetDetallenotasfiscales(models.Model):
    sucursal = models.CharField(db_column='Sucursal', blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', blank=True, null=True)  # Field name made lowercase.
    precio = models.CharField(db_column='Precio', blank=True, null=True)  # Field name made lowercase.
    servicio = models.CharField(db_column='Servicio', blank=True, null=True)  # Field name made lowercase.
    tributa = models.CharField(db_column='Tributa', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.DetalleNotasFiscales'


class DatasetDetreportes(models.Model):
    numero = models.CharField(blank=True, null=True)
    fila = models.CharField(blank=True, null=True)
    tipo = models.CharField(blank=True, null=True)
    contenido = models.CharField(blank=True, null=True)
    texto = models.CharField(blank=True, null=True)
    funcion = models.CharField(db_column='Funcion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Detreportes'


class DatasetDifcobros(models.Model):
    tipo = models.IntegerField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    monto = models.DecimalField(db_column='Monto', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    iva = models.DecimalField(db_column='Iva', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    autofactura = models.CharField(max_length=22, blank=True, null=True)
    autocobro = models.CharField(max_length=22, blank=True, null=True)
    cambiofactura = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    cambiocobro = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    contabilizado = models.IntegerField(blank=True, null=True)
    asiento = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Difcobros'


class DatasetDifpagos(models.Model):
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    monto = models.CharField(db_column='Monto', blank=True, null=True)  # Field name made lowercase.
    iva = models.CharField(db_column='Iva', blank=True, null=True)  # Field name made lowercase.
    autofactura = models.CharField(blank=True, null=True)
    autocobro = models.CharField(blank=True, null=True)
    cambiofactura = models.CharField(blank=True, null=True)
    cambiocobro = models.CharField(blank=True, null=True)
    contabilizado = models.CharField(blank=True, null=True)
    asiento = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Difpagos'


class DatasetDolar(models.Model):
    ufecha = models.CharField(max_length=19, blank=True, null=True)
    uvalor = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    umoneda = models.IntegerField(blank=True, null=True)
    upizarra = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    paridad = models.CharField(db_column='Paridad', max_length=11, blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=3, blank=True, null=True)  # Field name made lowercase.
    utcea = models.CharField(db_column='uTCEA', max_length=6, blank=True, null=True)  # Field name made lowercase.
    utcem = models.CharField(db_column='uTCEM', max_length=6, blank=True, null=True)  # Field name made lowercase.
    utcet = models.CharField(db_column='uTCET', max_length=6, blank=True, null=True)  # Field name made lowercase.
    utcia = models.CharField(db_column='uTCIA', max_length=6, blank=True, null=True)  # Field name made lowercase.
    utcim = models.CharField(db_column='uTCIM', max_length=6, blank=True, null=True)  # Field name made lowercase.
    utcit = models.CharField(db_column='uTCIT', max_length=6, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Dolar'


class DatasetEjercicio(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    comienzo = models.CharField(max_length=19, blank=True, null=True)
    final = models.CharField(max_length=19, blank=True, null=True)
    nombre = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Ejercicio'


class DatasetEmpresa(models.Model):
    dnombre = models.CharField(max_length=14, blank=True, null=True)
    drazonsocial = models.CharField(max_length=14, blank=True, null=True)
    ddireccion = models.CharField(max_length=20, blank=True, null=True)
    dtelefono = models.IntegerField(blank=True, null=True)
    drubro = models.CharField(max_length=15, blank=True, null=True)
    dlocalidad = models.CharField(max_length=10, blank=True, null=True)
    dfax = models.IntegerField(blank=True, null=True)
    dfactura = models.IntegerField(blank=True, null=True)
    druc = models.BigIntegerField(blank=True, null=True)
    dcpostal = models.IntegerField(blank=True, null=True)
    dseguro = models.CharField(max_length=3, blank=True, null=True)
    dprefijo = models.IntegerField(blank=True, null=True)
    dserie = models.CharField(max_length=1, blank=True, null=True)
    dfacturab = models.IntegerField(db_column='dfacturaB', blank=True, null=True)  # Field name made lowercase.
    dfacturac = models.IntegerField(db_column='dfacturaC', blank=True, null=True)  # Field name made lowercase.
    dfacturae = models.IntegerField(db_column='dfacturaE', blank=True, null=True)  # Field name made lowercase.
    drecibo = models.SmallIntegerField(blank=True, null=True)
    fachilea = models.IntegerField(db_column='fachileA', blank=True, null=True)  # Field name made lowercase.
    fachileb = models.IntegerField(db_column='fachileB', blank=True, null=True)  # Field name made lowercase.
    ncchilea = models.IntegerField(db_column='ncchileA', blank=True, null=True)  # Field name made lowercase.
    ncchileb = models.IntegerField(db_column='ncchileB', blank=True, null=True)  # Field name made lowercase.
    ndchilea = models.IntegerField(db_column='ndchileA', blank=True, null=True)  # Field name made lowercase.
    ndchileb = models.IntegerField(db_column='ndchileB', blank=True, null=True)  # Field name made lowercase.
    estacion = models.IntegerField(blank=True, null=True)
    replegal = models.CharField(max_length=3, blank=True, null=True)
    dprefijorecibo = models.IntegerField(blank=True, null=True)
    facturaelectronica = models.CharField(db_column='FacturaElectronica', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dinicioact = models.CharField(db_column='DInicioAct', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dingresosbrutos = models.CharField(db_column='DIngresosBrutos', max_length=3, blank=True, null=True)  # Field name made lowercase.
    nrosat = models.CharField(db_column='NroSAT', blank=True, null=True)  # Field name made lowercase.
    anosat = models.CharField(db_column='AnoSAT', blank=True, null=True)  # Field name made lowercase.
    motordoc = models.CharField(db_column='MotorDoc', max_length=1, blank=True, null=True)  # Field name made lowercase.
    auditoria = models.CharField(db_column='Auditoria', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nrosatnc = models.CharField(db_column='NroSatNC', blank=True, null=True)  # Field name made lowercase.
    anosatnc = models.CharField(db_column='AnoSatNC', blank=True, null=True)  # Field name made lowercase.
    keydosificacion = models.CharField(db_column='KeyDosificacion', max_length=3, blank=True, null=True)  # Field name made lowercase.
    noautorizacion = models.CharField(db_column='NoAutorizacion', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fechalimiteemision = models.CharField(db_column='FechaLimiteEmision', max_length=19, blank=True, null=True)  # Field name made lowercase.
    dirfe = models.CharField(db_column='DirFE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    nores = models.IntegerField(db_column='NoRes', blank=True, null=True)  # Field name made lowercase.
    fecres = models.CharField(db_column='FecRes', max_length=19, blank=True, null=True)  # Field name made lowercase.
    sc = models.CharField(db_column='SC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    factureoffice = models.CharField(db_column='FactureOffice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dirfelibros = models.CharField(db_column='DirFELibros', max_length=3, blank=True, null=True)  # Field name made lowercase.
    acteco = models.IntegerField(db_column='Acteco', blank=True, null=True)  # Field name made lowercase.
    actecoa = models.IntegerField(db_column='ActecoA', blank=True, null=True)  # Field name made lowercase.
    enviaordencomprafe = models.CharField(db_column='EnviaOrdenCompraFE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dnombrechino = models.CharField(db_column='dNombreChino', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Empresa'


class DatasetFactudif(models.Model):
    znumero = models.IntegerField(blank=True, null=True)
    zmoneda = models.IntegerField(blank=True, null=True)
    zcliente = models.SmallIntegerField(blank=True, null=True)
    ztipo = models.IntegerField(blank=True, null=True)
    zitem = models.SmallIntegerField(blank=True, null=True)
    zmonto = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    ziva = models.IntegerField(blank=True, null=True)
    zrefer = models.CharField(max_length=10, blank=True, null=True)
    zcarrier = models.CharField(max_length=30, blank=True, null=True)
    zmaster = models.CharField(max_length=24, blank=True, null=True)
    zdate = models.CharField(max_length=29, blank=True, null=True)
    zhouse = models.CharField(max_length=23, blank=True, null=True)
    zposicion = models.CharField(max_length=15, blank=True, null=True)
    zkilos = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    zbultos = models.IntegerField(blank=True, null=True)
    zvolumen = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    zorigen = models.CharField(max_length=23, blank=True, null=True)
    zdestino = models.CharField(max_length=22, blank=True, null=True)
    zdetalle = models.CharField(max_length=155, blank=True, null=True)
    ztransporte = models.CharField(max_length=1, blank=True, null=True)
    zclase = models.CharField(max_length=2, blank=True, null=True)
    zllegasale = models.CharField(max_length=19, blank=True, null=True)
    zobs1 = models.CharField(max_length=38, blank=True, null=True)
    zobs2 = models.CharField(max_length=63, blank=True, null=True)
    zobs3 = models.CharField(max_length=8, blank=True, null=True)
    zobs4 = models.CharField(max_length=8, blank=True, null=True)
    zobs5 = models.CharField(max_length=3, blank=True, null=True)
    zcommodity = models.CharField(max_length=39, blank=True, null=True)
    zembarcador = models.CharField(max_length=50, blank=True, null=True)
    zconsignatario = models.CharField(max_length=50, blank=True, null=True)
    zmonedaorigen = models.IntegerField(blank=True, null=True)
    zarbitraje = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    zorden = models.CharField(max_length=50, blank=True, null=True)
    zvalororiginal = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    zseguimiento = models.CharField(max_length=5, blank=True, null=True)
    zagente = models.CharField(max_length=50, blank=True, null=True)
    zcontrolado = models.CharField(max_length=1, blank=True, null=True)
    zusuario = models.CharField(max_length=3, blank=True, null=True)
    zfechagen = models.CharField(max_length=19, blank=True, null=True)
    zaplicable = models.CharField(db_column='zAplicable', max_length=7, blank=True, null=True)  # Field name made lowercase.
    zvendedor = models.CharField(db_column='zVendedor', max_length=2, blank=True, null=True)  # Field name made lowercase.
    zwr = models.CharField(db_column='zWR', max_length=13, blank=True, null=True)  # Field name made lowercase.
    znotas = models.CharField(db_column='zNotas', max_length=3, blank=True, null=True)  # Field name made lowercase.
    zcambiousdpactado = models.CharField(db_column='zCambioUSDPactado', max_length=6, blank=True, null=True)  # Field name made lowercase.
    zpagoflete = models.CharField(db_column='zPagoFlete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    zterminos = models.CharField(db_column='zTerminos', max_length=3, blank=True, null=True)  # Field name made lowercase.
    zfacturado = models.CharField(db_column='zFacturado', max_length=1, blank=True, null=True)  # Field name made lowercase.
    zop = models.CharField(db_column='zOP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nrofolio = models.CharField(db_column='NroFolio', blank=True, null=True)  # Field name made lowercase.
    dtefechaorden = models.CharField(db_column='DteFechaOrden', blank=True, null=True)  # Field name made lowercase.
    srazonreforden = models.CharField(db_column='sRazonRefOrden', blank=True, null=True)  # Field name made lowercase.
    zfechafacturado = models.CharField(db_column='zFechaFacturado', max_length=19, blank=True, null=True)  # Field name made lowercase.
    zboletafactura = models.CharField(db_column='zBoletaFactura', max_length=20, blank=True, null=True)  # Field name made lowercase.
    zautogenenvase = models.CharField(db_column='zAutogenEnvase', blank=True, null=True)  # Field name made lowercase.
    zfechaaprobada = models.CharField(db_column='zFechaAprobada', blank=True, null=True)  # Field name made lowercase.
    area = models.CharField(db_column='Area', blank=True, null=True)  # Field name made lowercase.
    jurisdiccion = models.CharField(db_column='Jurisdiccion', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Factudif'


class DatasetFamilias(models.Model):
    codigo = models.CharField(blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Familias'


class DatasetFedetalle(models.Model):
    encid = models.CharField(db_column='EncID', blank=True, null=True)  # Field name made lowercase.
    nrolindet = models.CharField(db_column='NroLinDet', blank=True, null=True)  # Field name made lowercase.
    tpocodigo = models.CharField(db_column='TpoCodigo', blank=True, null=True)  # Field name made lowercase.
    vlrcodigo = models.CharField(db_column='VlrCodigo', blank=True, null=True)  # Field name made lowercase.
    indexe = models.CharField(db_column='IndExe', blank=True, null=True)  # Field name made lowercase.
    nmbitem = models.CharField(db_column='NmbItem', blank=True, null=True)  # Field name made lowercase.
    prcotrmon = models.CharField(db_column='PrcOtrMon', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    fctconv = models.CharField(db_column='FctConv', blank=True, null=True)  # Field name made lowercase.
    montoitem = models.CharField(db_column='MontoItem', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.FeDetalle'


class DatasetFeencabezado(models.Model):
    encid = models.CharField(db_column='EncID', blank=True, null=True)  # Field name made lowercase.
    tipodte = models.CharField(db_column='TipoDTE', blank=True, null=True)  # Field name made lowercase.
    folio = models.CharField(db_column='Folio', blank=True, null=True)  # Field name made lowercase.
    fchemis = models.CharField(db_column='FchEmis', blank=True, null=True)  # Field name made lowercase.
    fchvto = models.CharField(db_column='FchVto', blank=True, null=True)  # Field name made lowercase.
    rutrecep = models.CharField(db_column='RUTRecep', blank=True, null=True)  # Field name made lowercase.
    rznsocrecep = models.CharField(db_column='RznSocRecep', blank=True, null=True)  # Field name made lowercase.
    girorecep = models.CharField(db_column='GiroRecep', blank=True, null=True)  # Field name made lowercase.
    dirrecep = models.CharField(db_column='DirRecep', blank=True, null=True)  # Field name made lowercase.
    cmnarecep = models.CharField(db_column='CmnaRecep', blank=True, null=True)  # Field name made lowercase.
    ciudadrecep = models.CharField(db_column='CiudadRecep', blank=True, null=True)  # Field name made lowercase.
    mntneto = models.CharField(db_column='MntNeto', blank=True, null=True)  # Field name made lowercase.
    mntexe = models.CharField(db_column='MntExe', blank=True, null=True)  # Field name made lowercase.
    tasaiva = models.CharField(db_column='TasaIVA', blank=True, null=True)  # Field name made lowercase.
    iva = models.CharField(db_column='IVA', blank=True, null=True)  # Field name made lowercase.
    mnttotal = models.CharField(db_column='MntTotal', blank=True, null=True)  # Field name made lowercase.
    docstatus = models.CharField(db_column='DocStatus', blank=True, null=True)  # Field name made lowercase.
    servicereference = models.CharField(db_column='ServiceReference', blank=True, null=True)  # Field name made lowercase.
    scautogenreference = models.CharField(db_column='SCAutogenReference', blank=True, null=True)  # Field name made lowercase.
    formatpdf = models.CharField(db_column='FormatPDF', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.FeEncabezado'


class DatasetFeimpresiondetalles(models.Model):
    encid = models.CharField(db_column='EncID', blank=True, null=True)  # Field name made lowercase.
    personnrolindet = models.CharField(db_column='PersonNroLinDet', blank=True, null=True)  # Field name made lowercase.
    detpersonafn_01 = models.CharField(db_column='DetPersonAFN_01', blank=True, null=True)  # Field name made lowercase.
    detpersonafn_02 = models.CharField(db_column='DetPersonAFN_02', blank=True, null=True)  # Field name made lowercase.
    detpersonafn_03 = models.CharField(db_column='DetPersonAFN_03', blank=True, null=True)  # Field name made lowercase.
    detpersonafn_04 = models.CharField(db_column='DetPersonAFN_04', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.FeImpresionDetalles'


class DatasetFepersonalizados(models.Model):
    encid = models.CharField(db_column='EncID', blank=True, null=True)  # Field name made lowercase.
    dteid = models.CharField(db_column='DteID', blank=True, null=True)  # Field name made lowercase.
    refdocorden = models.CharField(db_column='RefDocOrden', blank=True, null=True)  # Field name made lowercase.
    refdocblawb = models.CharField(db_column='REfDocBLAWB', blank=True, null=True)  # Field name made lowercase.
    refdocnave = models.CharField(db_column='RefDocNave', blank=True, null=True)  # Field name made lowercase.
    refdocpos = models.CharField(db_column='RefDocPos', blank=True, null=True)  # Field name made lowercase.
    refdocbultos = models.CharField(db_column='RefDocBultos', blank=True, null=True)  # Field name made lowercase.
    refdockilos = models.CharField(db_column='RefDocKilos', blank=True, null=True)  # Field name made lowercase.
    refdocremitente = models.CharField(db_column='RefDocRemitente', blank=True, null=True)  # Field name made lowercase.
    refdocconsignee = models.CharField(db_column='RefDocConsignee', blank=True, null=True)  # Field name made lowercase.
    refdocorigen = models.CharField(db_column='RefDocOrigen', blank=True, null=True)  # Field name made lowercase.
    refdocdestino = models.CharField(db_column='RefDocDestino', blank=True, null=True)  # Field name made lowercase.
    obsmdadoc = models.CharField(db_column='ObsMdaDoc', blank=True, null=True)  # Field name made lowercase.
    obstc = models.CharField(db_column='ObsTC', blank=True, null=True)  # Field name made lowercase.
    obsnumlts = models.CharField(db_column='ObsNumLts', blank=True, null=True)  # Field name made lowercase.
    telrecep = models.CharField(db_column='TelRecep', blank=True, null=True)  # Field name made lowercase.
    faxrecep = models.CharField(db_column='FaxRecep', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    obsln1 = models.CharField(db_column='ObsLn1', blank=True, null=True)  # Field name made lowercase.
    obsln2 = models.CharField(db_column='ObsLn2', blank=True, null=True)  # Field name made lowercase.
    obsln3 = models.CharField(db_column='ObsLn3', blank=True, null=True)  # Field name made lowercase.
    obsln4 = models.CharField(db_column='ObsLn4', blank=True, null=True)  # Field name made lowercase.
    obsln5 = models.CharField(db_column='ObsLn5', blank=True, null=True)  # Field name made lowercase.
    condpago = models.CharField(db_column='CondPago', blank=True, null=True)  # Field name made lowercase.
    att = models.CharField(db_column='Att', blank=True, null=True)  # Field name made lowercase.
    tototramoneda = models.CharField(db_column='TotOtraMoneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.FePersonalizados'


class DatasetFeqbli(models.Model):
    encid = models.CharField(db_column='EncID', blank=True, null=True)  # Field name made lowercase.
    ordencliente = models.CharField(db_column='OrdenCliente', blank=True, null=True)  # Field name made lowercase.
    tpodocref = models.CharField(db_column='TpoDocRef', blank=True, null=True)  # Field name made lowercase.
    servicioid = models.CharField(db_column='ServicioID', blank=True, null=True)  # Field name made lowercase.
    qbliitem = models.CharField(db_column='QBLiItem', blank=True, null=True)  # Field name made lowercase.
    fchorden = models.CharField(db_column='FchOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.FeQBLi'


class DatasetFereferencia(models.Model):
    encid = models.CharField(db_column='EncID', blank=True, null=True)  # Field name made lowercase.
    nrolinref = models.CharField(db_column='NroLinRef', blank=True, null=True)  # Field name made lowercase.
    tpodocref = models.CharField(db_column='TpoDocRef', blank=True, null=True)  # Field name made lowercase.
    folioref = models.CharField(db_column='FolioRef', blank=True, null=True)  # Field name made lowercase.
    fchref = models.CharField(db_column='FchRef', blank=True, null=True)  # Field name made lowercase.
    codref = models.CharField(db_column='CodRef', blank=True, null=True)  # Field name made lowercase.
    razonref = models.CharField(db_column='RazonRef', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.FeReferencia'


class DatasetFeresultado(models.Model):
    encid = models.CharField(db_column='EncID', blank=True, null=True)  # Field name made lowercase.
    tpodte = models.CharField(db_column='TpoDTE', blank=True, null=True)  # Field name made lowercase.
    wsresult = models.CharField(db_column='WSResult', blank=True, null=True)  # Field name made lowercase.
    wsidstatus = models.CharField(db_column='WSIdStatus', blank=True, null=True)  # Field name made lowercase.
    wsstatus = models.CharField(db_column='WSStatus', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.FeResultado'


class DatasetFetipos(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.FeTipos'


class DatasetFechacorte(models.Model):
    fecha = models.CharField(max_length=19, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    fechahasta = models.CharField(db_column='FechaHasta', max_length=19, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Fechacorte'


class DatasetFolioschile(models.Model):
    serie = models.CharField(db_column='Serie', blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.FoliosChile'


class DatasetFoliosdominicana(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.FoliosDominicana'


class DatasetGruposactivofijo(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    cuenta = models.CharField(db_column='Cuenta', blank=True, null=True)  # Field name made lowercase.
    porcentaje = models.CharField(db_column='Porcentaje', blank=True, null=True)  # Field name made lowercase.
    porcentajeniif = models.CharField(db_column='PorcentajeNIIF', blank=True, null=True)  # Field name made lowercase.
    anios = models.CharField(db_column='Anios', blank=True, null=True)  # Field name made lowercase.
    aniosniif = models.CharField(db_column='AniosNIIF', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.GruposActivoFijo'


class DatasetGuiadespacho(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    boleta = models.CharField(db_column='Boleta', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    importador = models.CharField(db_column='Importador', blank=True, null=True)  # Field name made lowercase.
    ruc = models.CharField(db_column='Ruc', blank=True, null=True)  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', blank=True, null=True)  # Field name made lowercase.
    declaracion = models.CharField(db_column='Declaracion', blank=True, null=True)  # Field name made lowercase.
    fechadeclaracion = models.CharField(db_column='FechaDeclaracion', blank=True, null=True)  # Field name made lowercase.
    aduana = models.CharField(db_column='Aduana', blank=True, null=True)  # Field name made lowercase.
    despacho = models.CharField(db_column='Despacho', blank=True, null=True)  # Field name made lowercase.
    transportador = models.CharField(db_column='Transportador', blank=True, null=True)  # Field name made lowercase.
    vehiculo = models.CharField(db_column='Vehiculo', blank=True, null=True)  # Field name made lowercase.
    patente = models.CharField(db_column='Patente', blank=True, null=True)  # Field name made lowercase.
    despachonum = models.CharField(db_column='DespachoNum', blank=True, null=True)  # Field name made lowercase.
    ref = models.CharField(db_column='Ref', blank=True, null=True)  # Field name made lowercase.
    ubicacion = models.CharField(db_column='Ubicacion', blank=True, null=True)  # Field name made lowercase.
    vaport = models.CharField(db_column='Vaport', blank=True, null=True)  # Field name made lowercase.
    observaciones = models.CharField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    choferruc = models.CharField(db_column='ChoferRUC', blank=True, null=True)  # Field name made lowercase.
    chofernombre = models.CharField(db_column='ChoferNombre', blank=True, null=True)  # Field name made lowercase.
    ciudaddestino = models.CharField(db_column='CiudadDestino', blank=True, null=True)  # Field name made lowercase.
    direcciondestino = models.CharField(db_column='DireccionDestino', blank=True, null=True)  # Field name made lowercase.
    comunadestino = models.CharField(db_column='ComunaDestino', blank=True, null=True)  # Field name made lowercase.
    vapor = models.CharField(db_column='Vapor', blank=True, null=True)  # Field name made lowercase.
    facturable = models.CharField(db_column='Facturable', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.GuiaDespacho'


class DatasetGuiadespachodetalle(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', blank=True, null=True)  # Field name made lowercase.
    embarque = models.CharField(db_column='Embarque', blank=True, null=True)  # Field name made lowercase.
    marca = models.CharField(db_column='Marca', blank=True, null=True)  # Field name made lowercase.
    cantidad = models.CharField(db_column='Cantidad', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    mercaderia = models.CharField(db_column='Mercaderia', blank=True, null=True)  # Field name made lowercase.
    peso = models.CharField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    cif = models.CharField(db_column='CIF', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.GuiaDespachoDetalle'


class DatasetHistoria(models.Model):
    htipo = models.IntegerField(blank=True, null=True)
    hboleta = models.CharField(max_length=20, blank=True, null=True)
    hfechamov = models.CharField(max_length=19, blank=True, null=True)
    hcodigo = models.SmallIntegerField(blank=True, null=True)
    hiva = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    hprecio = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    hmoneda = models.IntegerField(blank=True, null=True)
    hautogen = models.CharField(max_length=39, blank=True, null=True)
    hcambio = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    hserie = models.CharField(max_length=1, blank=True, null=True)
    hprefijo = models.SmallIntegerField(blank=True, null=True)
    hembarque = models.CharField(max_length=12, blank=True, null=True)
    hposicion = models.CharField(max_length=15, blank=True, null=True)
    heditado = models.CharField(max_length=72, blank=True, null=True)
    harea = models.IntegerField(blank=True, null=True)
    hcantidad = models.CharField(blank=True, null=True)
    htipogasto = models.CharField(db_column='Htipogasto', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hpago = models.CharField(db_column='Hpago', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hmontooriginal = models.CharField(db_column='hMontoOriginal', max_length=11, blank=True, null=True)  # Field name made lowercase.
    hmonedaoriginal = models.CharField(db_column='hMonedaOriginal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hparidad = models.DecimalField(db_column='hParidad', max_digits=7, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    hautogenlink = models.CharField(db_column='HAutogenLink', max_length=3, blank=True, null=True)  # Field name made lowercase.
    hpinformar = models.CharField(db_column='HPinformar', max_length=11, blank=True, null=True)  # Field name made lowercase.
    hnotas = models.CharField(db_column='HNotas', max_length=42, blank=True, null=True)  # Field name made lowercase.
    harbitrajeoriginal = models.CharField(db_column='hArbitrajeOriginal', max_length=7, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    hautogenenvase = models.CharField(db_column='hAutogenEnvase', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Historia'


class DatasetHistoriaimpbrasil(models.Model):
    autogen = models.CharField(db_column='Autogen', blank=True, null=True)  # Field name made lowercase.
    cliente = models.CharField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    porcentaje = models.CharField(db_column='Porcentaje', blank=True, null=True)  # Field name made lowercase.
    monto = models.CharField(db_column='Monto', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.HistoriaImpBrasil'


class DatasetImpucompras(models.Model):
    autogen = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True)
    serie = models.CharField(blank=True, null=True)
    prefijo = models.CharField(blank=True, null=True)
    numero = models.CharField(blank=True, null=True)
    cliente = models.SmallIntegerField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    autofac = models.CharField(max_length=39, blank=True, null=True)
    parteiva = models.CharField(db_column='ParteIVA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    montorg = models.CharField(db_column='MontoRG', blank=True, null=True)  # Field name made lowercase.
    montoriva = models.CharField(db_column='MontoRIVA', blank=True, null=True)  # Field name made lowercase.
    montorib = models.CharField(db_column='MontoRIB', blank=True, null=True)  # Field name made lowercase.
    montorsuss = models.CharField(db_column='MontoRSUSS', blank=True, null=True)  # Field name made lowercase.
    montootros = models.CharField(db_column='MontoOtros', blank=True, null=True)  # Field name made lowercase.
    porcentajerg = models.CharField(db_column='PorcentajeRG', blank=True, null=True)  # Field name made lowercase.
    porcentajeriva = models.CharField(db_column='PorcentajeRIVA', blank=True, null=True)  # Field name made lowercase.
    porcentajerib = models.CharField(db_column='PorcentajeRIB', blank=True, null=True)  # Field name made lowercase.
    porcentajersuss = models.CharField(db_column='PorcentajeRSUSS', blank=True, null=True)  # Field name made lowercase.
    porcentajeotros = models.CharField(db_column='PorcentajeOtros', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Impucompras'


class DatasetImpuestosbrasil(models.Model):
    id = models.CharField(blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)
    porcentaje = models.CharField(blank=True, null=True)
    cuenta = models.CharField(blank=True, null=True)
    cuenta2 = models.CharField(db_column='Cuenta2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ImpuestosBrasil'


class DatasetImpuordenes(models.Model):
    orden = models.SmallIntegerField(db_column='Orden', blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(blank=True, null=True)
    cliente = models.SmallIntegerField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    autofac = models.CharField(max_length=39, blank=True, null=True)
    prefijo = models.CharField(blank=True, null=True)
    serie = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Impuordenes'


class DatasetImpuvtas(models.Model):
    autogen = models.CharField(max_length=28, blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True)
    serie = models.CharField(blank=True, null=True)
    prefijo = models.CharField(blank=True, null=True)
    numero = models.CharField(blank=True, null=True)
    cliente = models.SmallIntegerField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    autofac = models.CharField(max_length=37, blank=True, null=True)
    parteiva = models.CharField(db_column='ParteIVA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    montorg = models.CharField(db_column='MontoRG', max_length=6, blank=True, null=True)  # Field name made lowercase.
    montoriva = models.CharField(db_column='MontoRIVA', max_length=6, blank=True, null=True)  # Field name made lowercase.
    montorib = models.CharField(db_column='MontoRIB', max_length=6, blank=True, null=True)  # Field name made lowercase.
    montorsuss = models.CharField(db_column='MontoRSUSS', max_length=6, blank=True, null=True)  # Field name made lowercase.
    montootros = models.CharField(db_column='MontoOtros', max_length=6, blank=True, null=True)  # Field name made lowercase.
    porcentajerg = models.CharField(db_column='PorcentajeRG', max_length=3, blank=True, null=True)  # Field name made lowercase.
    porcentajeriva = models.CharField(db_column='PorcentajeRIVA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    porcentajerib = models.CharField(db_column='PorcentajeRIB', max_length=3, blank=True, null=True)  # Field name made lowercase.
    porcentajersuss = models.CharField(db_column='PorcentajeRSUSS', max_length=3, blank=True, null=True)  # Field name made lowercase.
    porcentajeotros = models.CharField(db_column='PorcentajeOtros', max_length=3, blank=True, null=True)  # Field name made lowercase.
    anticipo = models.CharField(db_column='Anticipo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechaimpu = models.CharField(db_column='FechaImpu', max_length=19, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Impuvtas'


class DatasetInfofactura(models.Model):
    autogenerado = models.CharField(db_column='Autogenerado', max_length=26, blank=True, null=True)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=8, blank=True, null=True)  # Field name made lowercase.
    seguimiento = models.IntegerField(db_column='Seguimiento', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', max_length=20, blank=True, null=True)  # Field name made lowercase.
    vuelo = models.CharField(db_column='Vuelo', max_length=29, blank=True, null=True)  # Field name made lowercase.
    master = models.CharField(db_column='Master', max_length=20, blank=True, null=True)  # Field name made lowercase.
    house = models.CharField(db_column='House', max_length=42, blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=10, blank=True, null=True)  # Field name made lowercase.
    commodity = models.CharField(db_column='Commodity', max_length=30, blank=True, null=True)  # Field name made lowercase.
    kilos = models.DecimalField(db_column='Kilos', max_digits=9, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    volumen = models.DecimalField(db_column='Volumen', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    bultos = models.IntegerField(db_column='Bultos', blank=True, null=True)  # Field name made lowercase.
    ordencliente = models.CharField(db_column='OrdenCliente', max_length=50, blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=28, blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=23, blank=True, null=True)  # Field name made lowercase.
    consigna = models.CharField(db_column='Consigna', max_length=50, blank=True, null=True)  # Field name made lowercase.
    embarca = models.CharField(db_column='Embarca', max_length=50, blank=True, null=True)  # Field name made lowercase.
    agente = models.CharField(db_column='Agente', max_length=50, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=16, blank=True, null=True)  # Field name made lowercase.
    wr = models.CharField(db_column='WR', max_length=13, blank=True, null=True)  # Field name made lowercase.
    terminos = models.CharField(db_column='Terminos', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pagoflete = models.CharField(db_column='PagoFlete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tipoembarque = models.CharField(db_column='TipoEmbarque', max_length=1, blank=True, null=True)  # Field name made lowercase.
    etd = models.CharField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.CharField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.InfoFactura'


class DatasetIva(models.Model):
    xporcentaje = models.CharField(max_length=5, blank=True, null=True)
    xctavta = models.IntegerField(blank=True, null=True)
    xctacom = models.IntegerField(blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)
    xfechavigencia = models.CharField(db_column='xFechaVigencia', max_length=19, blank=True, null=True)  # Field name made lowercase.
    xporcentajeant = models.CharField(db_column='xPorcentajeAnt', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Iva'


class DatasetJurisdicciones(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    codigoexterno = models.CharField(db_column='CodigoExterno', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Jurisdicciones'


class DatasetMensajes(models.Model):
    autogenerado = models.CharField(max_length=26, blank=True, null=True)
    texto1 = models.CharField(max_length=93, blank=True, null=True)
    texto2 = models.CharField(max_length=63, blank=True, null=True)
    texto3 = models.CharField(max_length=52, blank=True, null=True)
    texto4 = models.CharField(max_length=52, blank=True, null=True)
    texto5 = models.CharField(max_length=47, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Mensajes'


class DatasetMensajesfactura(models.Model):
    codigo = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=14, blank=True, null=True)
    texto1 = models.CharField(max_length=54, blank=True, null=True)
    texto2 = models.CharField(max_length=3, blank=True, null=True)
    texto3 = models.CharField(max_length=3, blank=True, null=True)
    texto4 = models.CharField(max_length=3, blank=True, null=True)
    texto5 = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.MensajesFactura'


class DatasetMovims(models.Model):
    mtipo = models.IntegerField(blank=True, null=True)
    mfechamov = models.CharField(max_length=19, blank=True, null=True)
    mboleta = models.CharField(max_length=20, blank=True, null=True)
    mmonto = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    miva = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    mtotal = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    msobretasa = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    msaldo = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    mvtomov = models.CharField(max_length=19, blank=True, null=True)
    mmoneda = models.IntegerField(blank=True, null=True)
    mvendedor = models.IntegerField(blank=True, null=True)
    mcobrador = models.CharField(blank=True, null=True)
    mdetalle = models.CharField(max_length=200, blank=True, null=True)
    mcliente = models.SmallIntegerField(blank=True, null=True)
    mnombre = models.CharField(max_length=50, blank=True, null=True)
    mdireccion = models.CharField(blank=True, null=True)
    mcambio = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    mnombremov = models.CharField(max_length=11, blank=True, null=True)
    mautogen = models.CharField(max_length=39, blank=True, null=True)
    mseccion = models.IntegerField(blank=True, null=True)
    mserie = models.CharField(max_length=1, blank=True, null=True)
    mprefijo = models.SmallIntegerField(blank=True, null=True)
    mactivo = models.CharField(max_length=1, blank=True, null=True)
    mposicion = models.CharField(max_length=11, blank=True, null=True)
    mmesimpu = models.IntegerField(blank=True, null=True)
    manoimpu = models.SmallIntegerField(blank=True, null=True)
    mmonedaoriginal = models.CharField(max_length=1, blank=True, null=True)
    marbitraje = models.CharField(max_length=10, blank=True, null=True)
    mmontooriginal = models.CharField(max_length=11, blank=True, null=True)
    mctaorden = models.CharField(max_length=1, blank=True, null=True)
    mcliorden = models.CharField(max_length=1, blank=True, null=True)
    mvoucher = models.CharField(max_length=1, blank=True, null=True)
    mruc = models.CharField(max_length=24, blank=True, null=True)
    mimpreso = models.CharField(max_length=1, blank=True, null=True)
    mfechadoc = models.CharField(db_column='mFechaDoc', max_length=19, blank=True, null=True)  # Field name made lowercase.
    minialta = models.CharField(db_column='mIniAlta', max_length=3, blank=True, null=True)  # Field name made lowercase.
    miniprint = models.CharField(db_column='mIniPrint', max_length=3, blank=True, null=True)  # Field name made lowercase.
    mparidad = models.CharField(db_column='mParidad', max_length=8, blank=True, null=True)  # Field name made lowercase.
    msucursal = models.CharField(db_column='mSucursal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    electronica = models.CharField(db_column='Electronica', blank=True, null=True)  # Field name made lowercase.
    mnropapel = models.CharField(db_column='mNroPapel', max_length=1, blank=True, null=True)  # Field name made lowercase.
    midfiscal = models.CharField(db_column='mIdFiscal', max_length=3, blank=True, null=True)  # Field name made lowercase.
    liquidada = models.CharField(db_column='Liquidada', blank=True, null=True)  # Field name made lowercase.
    mdetallepagada = models.CharField(db_column='mDetallePagada', blank=True, null=True)  # Field name made lowercase.
    maprobada = models.CharField(db_column='mAprobada', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tccorreccion = models.CharField(db_column='TcCorreccion', blank=True, null=True)  # Field name made lowercase.
    moncorreccion = models.CharField(db_column='MonCorreccion', blank=True, null=True)  # Field name made lowercase.
    codigocontrol = models.CharField(db_column='CodigoControl', blank=True, null=True)  # Field name made lowercase.
    cainro = models.CharField(db_column='CAINro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    caivto = models.CharField(db_column='CaiVto', max_length=19, blank=True, null=True)  # Field name made lowercase.
    mnombre2 = models.CharField(db_column='mNombre2', max_length=25, blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ponumber = models.CharField(db_column='PONumber', blank=True, null=True)  # Field name made lowercase.
    cae = models.CharField(db_column='CAE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechavtocae = models.CharField(db_column='FechaVtoCAE', blank=True, null=True)  # Field name made lowercase.
    fleteinternacional = models.CharField(db_column='FleteInternacional', max_length=2, blank=True, null=True)  # Field name made lowercase.
    lugarprestacionservicio = models.CharField(db_column='LugarPrestacionServicio', max_length=5, blank=True, null=True)  # Field name made lowercase.
    caimonto = models.CharField(db_column='CaiMonto', max_length=6, blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tipocomprobante = models.CharField(db_column='TipoComprobante', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tiposustento = models.CharField(db_column='TipoSustento', max_length=1, blank=True, null=True)  # Field name made lowercase.
    foliofeactualizado = models.CharField(db_column='FolioFEActualizado', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mcodref = models.CharField(db_column='mCodRef', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mrazonref = models.CharField(db_column='mRazonRef', max_length=39, blank=True, null=True)  # Field name made lowercase.
    noautorizacion = models.CharField(db_column='NoAutorizacion', blank=True, null=True)  # Field name made lowercase.
    fechalimiteemision = models.CharField(db_column='FechaLimiteEmision', max_length=19, blank=True, null=True)  # Field name made lowercase.
    ivanorecuperable = models.CharField(db_column='IVANoRecuperable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    formapago = models.CharField(db_column='FormaPago', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fe_uuid = models.CharField(db_column='FE_UUID', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fe_idcontrol = models.CharField(db_column='FE_IDControl', blank=True, null=True)  # Field name made lowercase.
    recuperodegastos = models.CharField(db_column='RecuperodeGastos', max_length=2, blank=True, null=True)  # Field name made lowercase.
    jurisdiccion = models.CharField(db_column='Jurisdiccion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    eticket = models.CharField(db_column='eTicket', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Movims'


class DatasetNiveles(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=10, blank=True, null=True)
    capitulo = models.CharField(max_length=32, blank=True, null=True)
    capituloingles = models.CharField(db_column='CapituloIngles', max_length=3, blank=True, null=True)  # Field name made lowercase.
    alternativo = models.CharField(db_column='Alternativo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Niveles'


class DatasetNivelesniif(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    capitulo = models.CharField(db_column='Capitulo', blank=True, null=True)  # Field name made lowercase.
    capituloingles = models.CharField(db_column='CapituloIngles', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.NivelesNIIF'


class DatasetNotas(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    notas = models.CharField(max_length=67, blank=True, null=True)
    asunto = models.CharField(max_length=18, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Notas'


class DatasetNotasfiscales(models.Model):
    sucursal = models.CharField(db_column='Sucursal', blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    cliente = models.CharField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.
    neto = models.CharField(db_column='Neto', blank=True, null=True)  # Field name made lowercase.
    iss = models.CharField(db_column='ISS', blank=True, null=True)  # Field name made lowercase.
    total = models.CharField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    condicion = models.CharField(db_column='Condicion', blank=True, null=True)  # Field name made lowercase.
    alicuota = models.CharField(db_column='Alicuota', blank=True, null=True)  # Field name made lowercase.
    inicial = models.CharField(db_column='Inicial', blank=True, null=True)  # Field name made lowercase.
    activa = models.CharField(db_column='Activa', blank=True, null=True)  # Field name made lowercase.
    fechaservicio = models.CharField(db_column='FechaServicio', blank=True, null=True)  # Field name made lowercase.
    vto = models.CharField(db_column='VTO', blank=True, null=True)  # Field name made lowercase.
    duplicata = models.CharField(db_column='Duplicata', blank=True, null=True)  # Field name made lowercase.
    procesada = models.CharField(db_column='Procesada', blank=True, null=True)  # Field name made lowercase.
    aplicable = models.CharField(db_column='Aplicable', blank=True, null=True)  # Field name made lowercase.
    asiento = models.CharField(db_column='Asiento', blank=True, null=True)  # Field name made lowercase.
    detalle1 = models.CharField(db_column='Detalle1', blank=True, null=True)  # Field name made lowercase.
    detalle2 = models.CharField(db_column='Detalle2', blank=True, null=True)  # Field name made lowercase.
    detalle3 = models.CharField(db_column='Detalle3', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.NotasFiscales'


class DatasetObservacionescae(models.Model):
    autogenerado = models.CharField(db_column='Autogenerado', blank=True, null=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.ObservacionesCAE'


class DatasetOrdenes(models.Model):
    mboleta = models.SmallIntegerField(blank=True, null=True)
    mfechamov = models.CharField(max_length=19, blank=True, null=True)
    mmonto = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    mmoneda = models.IntegerField(blank=True, null=True)
    mdetalle = models.CharField(max_length=200, blank=True, null=True)
    mcliente = models.SmallIntegerField(blank=True, null=True)
    mnombre = models.CharField(max_length=39, blank=True, null=True)
    mactiva = models.CharField(max_length=1, blank=True, null=True)
    mcaja = models.IntegerField(blank=True, null=True)
    masiento = models.CharField(max_length=15, blank=True, null=True)
    monedaefec = models.IntegerField(blank=True, null=True)
    montoefec = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    mautogenmovims = models.CharField(db_column='mAutogenMovims', max_length=29, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Ordenes'


class DatasetPlan(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Plan'


class DatasetPlan8(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=14, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Plan8'


class DatasetPlanniif(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.PlanNIIF'


class DatasetPosiciones(models.Model):
    posicion = models.CharField(blank=True, null=True)
    detalle = models.CharField(blank=True, null=True)
    observaciones = models.CharField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    fecha = models.CharField(blank=True, null=True)
    alternativo = models.CharField(db_column='Alternativo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Posiciones'


class DatasetRelacionniif(models.Model):
    xcodigoniif = models.CharField(db_column='xCodigoNIIF', blank=True, null=True)  # Field name made lowercase.
    xcodigocuenta = models.CharField(db_column='xCodigoCuenta', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.RelacionNIIF'


class DatasetResguardos(models.Model):
    rautogen = models.CharField(db_column='rAutogen', blank=True, null=True)  # Field name made lowercase.
    rcliente = models.CharField(db_column='rCliente', blank=True, null=True)  # Field name made lowercase.
    rserie = models.CharField(db_column='rSerie', blank=True, null=True)  # Field name made lowercase.
    rnumero = models.CharField(db_column='rNumero', blank=True, null=True)  # Field name made lowercase.
    rmoneda = models.CharField(db_column='rMoneda', blank=True, null=True)  # Field name made lowercase.
    robs = models.CharField(db_column='rObs', blank=True, null=True)  # Field name made lowercase.
    rfecha = models.CharField(db_column='rFecha', blank=True, null=True)  # Field name made lowercase.
    rvto = models.CharField(db_column='rVto', blank=True, null=True)  # Field name made lowercase.
    raceptado = models.CharField(db_column='rAceptado', blank=True, null=True)  # Field name made lowercase.
    rtipocambio = models.CharField(db_column='rTipoCambio', blank=True, null=True)  # Field name made lowercase.
    rtotal = models.CharField(db_column='rTotal', blank=True, null=True)  # Field name made lowercase.
    rescontingencia = models.CharField(db_column='rEsContingencia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Resguardos'


class DatasetRetencionesiibb(models.Model):
    autogenerado = models.CharField(db_column='Autogenerado', blank=True, null=True)  # Field name made lowercase.
    prefijo = models.CharField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    documento = models.CharField(db_column='Documento', blank=True, null=True)  # Field name made lowercase.
    neto = models.CharField(db_column='Neto', blank=True, null=True)  # Field name made lowercase.
    alicuota = models.CharField(db_column='Alicuota', blank=True, null=True)  # Field name made lowercase.
    retenido = models.CharField(db_column='Retenido', blank=True, null=True)  # Field name made lowercase.
    enviado = models.CharField(db_column='Enviado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.RetencionesIIBB'


class DatasetSeccion(models.Model):
    zcod = models.CharField(blank=True, null=True)
    znomsec = models.CharField(blank=True, null=True)
    zobserv = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.Seccion'


class DatasetSped(models.Model):
    id = models.CharField(blank=True, null=True)
    inscricaocadastro = models.CharField(db_column='InscricaoCadastro', blank=True, null=True)  # Field name made lowercase.
    codigocadastral = models.CharField(db_column='CodigoCadastral', blank=True, null=True)  # Field name made lowercase.
    uf = models.CharField(db_column='UF', blank=True, null=True)  # Field name made lowercase.
    nire = models.CharField(db_column='Nire', blank=True, null=True)  # Field name made lowercase.
    numordenactual = models.CharField(db_column='NumOrdenActual', blank=True, null=True)  # Field name made lowercase.
    naturezalibro = models.CharField(db_column='NaturezaLibro', blank=True, null=True)  # Field name made lowercase.
    dteconstitutivos = models.CharField(db_column='dteConstitutivos', blank=True, null=True)  # Field name made lowercase.
    dteconvercion = models.CharField(db_column='dteConvercion', blank=True, null=True)  # Field name made lowercase.
    respnome = models.CharField(db_column='RespNome', blank=True, null=True)  # Field name made lowercase.
    cpf = models.CharField(db_column='CPF', blank=True, null=True)  # Field name made lowercase.
    respcategoria = models.CharField(db_column='RespCategoria', blank=True, null=True)  # Field name made lowercase.
    municipio = models.CharField(db_column='Municipio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Sped'


class DatasetSustentos(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Sustentos'


class DatasetTipocliretencion(models.Model):
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    cuenta = models.CharField(db_column='Cuenta', blank=True, null=True)  # Field name made lowercase.
    aplica = models.CharField(db_column='Aplica', blank=True, null=True)  # Field name made lowercase.
    comentario = models.CharField(db_column='Comentario', blank=True, null=True)  # Field name made lowercase.
    porcentaje = models.CharField(db_column='Porcentaje', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.TipoCliRetencion'


class DatasetTipocli(models.Model):
    dcodigo = models.CharField(blank=True, null=True)
    dnomtip = models.CharField(blank=True, null=True)
    dtipofac = models.CharField(blank=True, null=True)
    dsobretasa = models.CharField(blank=True, null=True)
    dpuntoventa = models.CharField(db_column='dPuntoVenta', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.Tipocli'


class DatasetTiposcompproveedor(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    establecimiento = models.CharField(db_column='Establecimiento', blank=True, null=True)  # Field name made lowercase.
    serie = models.CharField(db_column='Serie', blank=True, null=True)  # Field name made lowercase.
    numerodesde = models.CharField(db_column='NumeroDesde', blank=True, null=True)  # Field name made lowercase.
    numerohasta = models.CharField(db_column='NumeroHasta', blank=True, null=True)  # Field name made lowercase.
    autorizacion = models.CharField(db_column='Autorizacion', blank=True, null=True)  # Field name made lowercase.
    emision = models.CharField(db_column='Emision', blank=True, null=True)  # Field name made lowercase.
    vencimiento = models.CharField(db_column='Vencimiento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.TiposCompProveedor'


class DatasetTiposcompretencion(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    establecimiento = models.CharField(db_column='Establecimiento', blank=True, null=True)  # Field name made lowercase.
    serie = models.CharField(db_column='Serie', blank=True, null=True)  # Field name made lowercase.
    numerodesde = models.CharField(db_column='NumeroDesde', blank=True, null=True)  # Field name made lowercase.
    numerohasta = models.CharField(db_column='NumeroHasta', blank=True, null=True)  # Field name made lowercase.
    autorizacion = models.CharField(db_column='Autorizacion', blank=True, null=True)  # Field name made lowercase.
    emision = models.CharField(db_column='Emision', blank=True, null=True)  # Field name made lowercase.
    vencimiento = models.CharField(db_column='Vencimiento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.TiposCompRetencion'


class DatasetTiposcomprobantesustentos(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    idtc = models.CharField(db_column='IDTC', blank=True, null=True)  # Field name made lowercase.
    idsustento = models.CharField(db_column='IDSustento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.TiposComprobanteSustentos'


class DatasetTiposcomprobantes(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    secuencia = models.CharField(db_column='Secuencia', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    comportamiento = models.CharField(db_column='Comportamiento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.TiposComprobantes'


class DatasetTiposrenta(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dataset.TiposRenta'


class DatasetDtproperties(models.Model):
    id = models.CharField(blank=True, null=True)
    objectid = models.CharField(blank=True, null=True)
    property = models.CharField(blank=True, null=True)
    value = models.CharField(blank=True, null=True)
    lvalue = models.CharField(blank=True, null=True)
    version = models.CharField(blank=True, null=True)
    uvalue = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dataset.dtproperties'


class ExpomaritAnulados(models.Model):
    fecha = models.CharField(max_length=19, blank=True, null=True)
    detalle = models.CharField(max_length=46, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Expomarit.Anulados'


class ExpomaritAttachhijo(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=206, blank=True, null=True)
    detalle = models.CharField(max_length=22, blank=True, null=True)
    web = models.CharField(blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.AttachHijo'


class ExpomaritAttachmadre(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=56, blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.AttachMadre'


class ExpomaritBookenv(models.Model):
    numero = models.CharField(blank=True, null=True)
    marks = models.CharField(blank=True, null=True)
    packages = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    gross = models.CharField(blank=True, null=True)
    tare = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Expomarit.Bookenv'


class ExpomaritBooking(models.Model):
    numero = models.CharField(blank=True, null=True)
    empresa = models.CharField(blank=True, null=True)
    direccion = models.CharField(blank=True, null=True)
    pais = models.CharField(blank=True, null=True)
    localidad = models.CharField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True)
    comboembarca = models.CharField(blank=True, null=True)
    cliente2 = models.CharField(blank=True, null=True)
    cliente3 = models.CharField(blank=True, null=True)
    cliente4 = models.CharField(blank=True, null=True)
    comboconsig = models.CharField(blank=True, null=True)
    direcconsigna = models.CharField(blank=True, null=True)
    localconsigna = models.CharField(blank=True, null=True)
    teleconsigna = models.CharField(blank=True, null=True)
    otralinea = models.CharField(blank=True, null=True)
    nrobooking = models.CharField(blank=True, null=True)
    dia = models.CharField(blank=True, null=True)
    salede = models.CharField(blank=True, null=True)
    loading = models.CharField(blank=True, null=True)
    discharge = models.CharField(blank=True, null=True)
    delivery = models.CharField(blank=True, null=True)
    vapor = models.CharField(blank=True, null=True)
    etapod = models.CharField(blank=True, null=True)
    etapol = models.CharField(blank=True, null=True)
    viaje = models.CharField(blank=True, null=True)
    payable = models.CharField(blank=True, null=True)
    combotransport = models.CharField(blank=True, null=True)
    comboproduc = models.CharField(blank=True, null=True)
    bultos = models.CharField(blank=True, null=True)
    pesobruto = models.CharField(blank=True, null=True)
    net = models.CharField(blank=True, null=True)
    sold = models.CharField(blank=True, null=True)
    profit = models.CharField(blank=True, null=True)
    remarks = models.CharField(blank=True, null=True)
    giro = models.CharField(blank=True, null=True)
    despachante = models.CharField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)
    terminal = models.CharField(blank=True, null=True)
    direccterminal = models.CharField(blank=True, null=True)
    telterminal = models.CharField(blank=True, null=True)
    contactoterminal = models.CharField(db_column='ContactoTerminal', blank=True, null=True)  # Field name made lowercase.
    bandera = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Expomarit.Booking'


class ExpomaritCargaaerea(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    medidas = models.CharField(max_length=17, blank=True, null=True)
    tipo = models.CharField(max_length=9, blank=True, null=True)
    fechaembarque = models.CharField(max_length=19, blank=True, null=True)
    cbm = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    mercaderia = models.CharField(max_length=79, blank=True, null=True)
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    marcas = models.CharField(db_column='Marcas', max_length=3, blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', blank=True, null=True)  # Field name made lowercase.
    sobredimensionada = models.CharField(db_column='Sobredimensionada', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.Cargaaerea'


class ExpomaritClavenrohouse(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    embarque = models.CharField(db_column='Embarque', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.ClaveNroHouse'


class ExpomaritClaveposicion(models.Model):
    posicion = models.CharField(max_length=10, blank=True, null=True)
    numeroorden = models.IntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.Claveposicion'


class ExpomaritConexreserva(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    vapor = models.CharField(max_length=16, blank=True, null=True)
    salida = models.CharField(max_length=19, blank=True, null=True)
    llegada = models.CharField(max_length=19, blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(max_length=9, blank=True, null=True)
    modo = models.CharField(max_length=8, blank=True, null=True)
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    horaorigen = models.CharField(db_column='HoraOrigen', blank=True, null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.Conexreserva'


class ExpomaritEmbarqueaereo(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    cliente = models.SmallIntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    despachante = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    consolidado = models.IntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=15, blank=True, null=True)
    operacion = models.CharField(max_length=23, blank=True, null=True)
    aduana = models.CharField(max_length=3, blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    pago = models.CharField(blank=True, null=True)
    awb = models.CharField(max_length=20, blank=True, null=True)
    hawb = models.CharField(max_length=19, blank=True, null=True)
    transportista = models.SmallIntegerField(blank=True, null=True)
    valortransporte = models.CharField(blank=True, null=True)
    valoraduana = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    fechaembarque = models.CharField(max_length=19, blank=True, null=True)
    fecharetiro = models.CharField(max_length=19, blank=True, null=True)
    pagoflete = models.CharField(max_length=1, blank=True, null=True)
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    valorseguro = models.CharField(blank=True, null=True)
    tarifaventa = models.CharField(blank=True, null=True)
    tarifacompra = models.CharField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    volumencubico = models.CharField(blank=True, null=True)
    cotizacion = models.SmallIntegerField(blank=True, null=True)
    cotitransp = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    transdestino = models.SmallIntegerField(blank=True, null=True)
    facturado = models.CharField(max_length=1, blank=True, null=True)
    profitage = models.CharField(blank=True, null=True)
    embarcador = models.SmallIntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    notificar = models.SmallIntegerField(db_column='Notificar', blank=True, null=True)  # Field name made lowercase.
    vaporcli = models.CharField(db_column='Vaporcli', blank=True, null=True)  # Field name made lowercase.
    vaporcli2 = models.CharField(db_column='Vaporcli2', blank=True, null=True)  # Field name made lowercase.
    vapor = models.CharField(db_column='Vapor', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tipovend = models.CharField(db_column='Tipovend', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendedor = models.IntegerField(db_column='Vendedor', blank=True, null=True)  # Field name made lowercase.
    comivend = models.DecimalField(db_column='Comivend', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    aplicaprofit = models.SmallIntegerField(db_column='Aplicaprofit', blank=True, null=True)  # Field name made lowercase.
    nroreferedi = models.CharField(blank=True, null=True)
    ordencliente = models.CharField(max_length=38, blank=True, null=True)
    armador = models.CharField(blank=True, null=True)
    viaje = models.CharField(max_length=9, blank=True, null=True)
    propia = models.IntegerField(blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    trafico = models.IntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    hawbtext = models.CharField(db_column='HawbText', max_length=6, blank=True, null=True)  # Field name made lowercase.
    booking = models.CharField(max_length=13, blank=True, null=True)
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=3, blank=True, null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=3, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=7, blank=True, null=True)  # Field name made lowercase.
    proyecto = models.IntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=8, blank=True, null=True)  # Field name made lowercase.
    depcontenedoringreso = models.IntegerField(db_column='DepContenedorIngreso', blank=True, null=True)  # Field name made lowercase.
    depcontenedorvacios = models.IntegerField(db_column='DepContenedorVacios', blank=True, null=True)  # Field name made lowercase.
    agenteportuario = models.IntegerField(db_column='AgentePortuario', blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=3, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    deadborrador = models.CharField(db_column='DeadBorrador', max_length=19, blank=True, null=True)  # Field name made lowercase.
    deaddocumentos = models.CharField(db_column='DeadDocumentos', max_length=19, blank=True, null=True)  # Field name made lowercase.
    deadentrega = models.CharField(db_column='DeadEntrega', max_length=19, blank=True, null=True)  # Field name made lowercase.
    deadliberacion = models.CharField(db_column='DeadLiberacion', max_length=19, blank=True, null=True)  # Field name made lowercase.
    retiravacio = models.CharField(db_column='RetiraVacio', max_length=19, blank=True, null=True)  # Field name made lowercase.
    retiralleno = models.CharField(db_column='RetiraLleno', max_length=19, blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=15, blank=True, null=True)  # Field name made lowercase.
    imprimiobl = models.CharField(db_column='ImprimioBL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hblcorp = models.IntegerField(db_column='HBLCorp', blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)  # Field name made lowercase.
    datosnotificante = models.CharField(db_column='DatosNotificante', max_length=3, blank=True, null=True)  # Field name made lowercase.
    contactoemergencia = models.CharField(db_column='ContactoEmergencia', max_length=3, blank=True, null=True)  # Field name made lowercase.
    numerocomunicacion = models.CharField(db_column='NumeroComunicacion', max_length=3, blank=True, null=True)  # Field name made lowercase.
    agecompras = models.SmallIntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.SmallIntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    fechaentrega = models.CharField(db_column='FechaEntrega', max_length=19, blank=True, null=True)  # Field name made lowercase.
    aquienentrega = models.CharField(db_column='aQuienEntrega', max_length=7, blank=True, null=True)  # Field name made lowercase.
    actividad = models.IntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    salidasim = models.CharField(db_column='SalidaSIM', max_length=19, blank=True, null=True)  # Field name made lowercase.
    presentasim = models.CharField(db_column='PresentaSIM', max_length=19, blank=True, null=True)  # Field name made lowercase.
    cierresim = models.CharField(db_column='CierreSIM', max_length=19, blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    imprimioorig = models.CharField(db_column='ImprimioOrig', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enviointtrabk = models.CharField(db_column='EnvioInttraBK', blank=True, null=True)  # Field name made lowercase.
    enviointtrasi = models.CharField(db_column='EnvioInttraSI', blank=True, null=True)  # Field name made lowercase.
    maerskbk = models.CharField(db_column='MaerskBK', blank=True, null=True)  # Field name made lowercase.
    maersksi = models.CharField(db_column='MaerskSI', blank=True, null=True)  # Field name made lowercase.
    tipobl = models.CharField(db_column='TipoBL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechacutoff = models.CharField(db_column='FechaCutOff', max_length=19, blank=True, null=True)  # Field name made lowercase.
    horacutoff = models.CharField(db_column='HoraCutOff', blank=True, null=True)  # Field name made lowercase.
    fecharetiromercaderia = models.CharField(db_column='FechaRetiroMercaderia', max_length=19, blank=True, null=True)  # Field name made lowercase.
    fechainiciostacking = models.CharField(db_column='FechaInicioStacking', max_length=19, blank=True, null=True)  # Field name made lowercase.
    horainiciostacking = models.CharField(db_column='HoraInicioStacking', blank=True, null=True)  # Field name made lowercase.
    fechafinstacking = models.CharField(db_column='FechaFinStacking', max_length=19, blank=True, null=True)  # Field name made lowercase.
    horafinstacking = models.CharField(db_column='HoraFinStacking', blank=True, null=True)  # Field name made lowercase.
    emisionbl = models.CharField(db_column='EmisionBL', max_length=19, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=3, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=24, blank=True, null=True)  # Field name made lowercase.
    envioeasipassbk = models.CharField(db_column='EnvioEASIPASSBK', blank=True, null=True)  # Field name made lowercase.
    envioeasipasssi = models.CharField(db_column='EnvioEASIPASSSI', blank=True, null=True)  # Field name made lowercase.
    demora = models.IntegerField(db_column='Demora', blank=True, null=True)  # Field name made lowercase.
    valordemoravta = models.DecimalField(db_column='ValorDemoraVTA', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    truckerarrivaltime = models.CharField(db_column='TruckerArrivalTime', blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FechaIngreso', max_length=19, blank=True, null=True)  # Field name made lowercase.
    fechacutoffvgm = models.CharField(db_column='FechaCutOffVGM', max_length=19, blank=True, null=True)  # Field name made lowercase.
    horacutoffvgm = models.CharField(db_column='HoraCutOffVGM', blank=True, null=True)  # Field name made lowercase.
    emitebloriginal = models.CharField(db_column='EmiteBLOriginal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', blank=True, null=True)  # Field name made lowercase.
    etd = models.CharField(db_column='ETD', max_length=19, blank=True, null=True)  # Field name made lowercase.
    eta = models.CharField(db_column='ETA', max_length=19, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.Embarqueaereo'


class ExpomaritEntregadoc(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    entreguese = models.CharField(db_column='Entreguese', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nombreentrega = models.CharField(db_column='NombreEntrega', max_length=44, blank=True, null=True)  # Field name made lowercase.
    direccionentrega = models.CharField(db_column='DireccionEntrega', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ciudadentrega = models.CharField(db_column='CiudadEntrega', max_length=10, blank=True, null=True)  # Field name made lowercase.
    telefonoentrega = models.CharField(db_column='TelefonoEntrega', max_length=27, blank=True, null=True)  # Field name made lowercase.
    original = models.CharField(db_column='Original', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lista = models.CharField(db_column='Lista', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certorigen = models.CharField(db_column='CertOrigen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    declara = models.CharField(db_column='Declara', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certflete = models.CharField(db_column='CertFlete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cerseguro = models.CharField(db_column='CerSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    copiahbl = models.CharField(db_column='CopiaHBL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    otros = models.CharField(db_column='Otros', max_length=1, blank=True, null=True)  # Field name made lowercase.
    detotros = models.CharField(db_column='DetOtros', max_length=43, blank=True, null=True)  # Field name made lowercase.
    detotros2 = models.CharField(db_column='DetOtros2', max_length=32, blank=True, null=True)  # Field name made lowercase.
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
    remarks = models.CharField(db_column='Remarks', max_length=51, blank=True, null=True)  # Field name made lowercase.
    remarks2 = models.CharField(db_column='Remarks2', max_length=34, blank=True, null=True)  # Field name made lowercase.
    facturacom = models.CharField(db_column='FacturaCom', max_length=24, blank=True, null=True)  # Field name made lowercase.
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', blank=True, null=True)  # Field name made lowercase.
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', blank=True, null=True)  # Field name made lowercase.
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crtnumero = models.CharField(db_column='CRTNumero', blank=True, null=True)  # Field name made lowercase.
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', blank=True, null=True)  # Field name made lowercase.
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    micdtanumero = models.CharField(db_column='MicDtaNumero', blank=True, null=True)  # Field name made lowercase.
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    papeletanumero = models.CharField(db_column='PapeletaNumero', blank=True, null=True)  # Field name made lowercase.
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True, null=True)  # Field name made lowercase.
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', blank=True, null=True)  # Field name made lowercase.
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', blank=True, null=True)  # Field name made lowercase.
    certorigennumero = models.CharField(db_column='CertOrigenNumero', blank=True, null=True)  # Field name made lowercase.
    certseguronumero = models.CharField(db_column='CertSeguroNumero', blank=True, null=True)  # Field name made lowercase.
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', blank=True, null=True)  # Field name made lowercase.
    detotros3 = models.CharField(db_column='DetOtros3', blank=True, null=True)  # Field name made lowercase.
    detotros4 = models.CharField(db_column='DetOtros4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.EntregaDoc'


class ExpomaritEnvases(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=3, blank=True, null=True)
    tipo = models.CharField(max_length=14, blank=True, null=True)
    movimiento = models.CharField(max_length=7, blank=True, null=True)
    terminos = models.CharField(max_length=4, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    marcas = models.CharField(max_length=46, blank=True, null=True)
    precinto = models.CharField(max_length=13, blank=True, null=True)
    tara = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    envase = models.CharField(db_column='Envase', max_length=9, blank=True, null=True)  # Field name made lowercase.
    bultos = models.IntegerField(blank=True, null=True)
    peso = models.DecimalField(db_column='Peso', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(max_length=13, blank=True, null=True)
    volumen = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    temperatura = models.DecimalField(db_column='Temperatura', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ventilacion = models.CharField(db_column='Ventilacion', blank=True, null=True)  # Field name made lowercase.
    genset = models.CharField(db_column='GenSet', max_length=1, blank=True, null=True)  # Field name made lowercase.
    atmosferacontrolada = models.CharField(db_column='AtmosferaControlada', max_length=1, blank=True, null=True)  # Field name made lowercase.
    consolidacion = models.IntegerField(db_column='Consolidacion', blank=True, null=True)  # Field name made lowercase.
    tipoventilacion = models.CharField(db_column='TipoVentilacion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pesovgm = models.CharField(db_column='PesoVGM', max_length=3, blank=True, null=True)  # Field name made lowercase.
    humedad = models.CharField(db_column='Humedad', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.Envases'


class ExpomaritFaxes(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.Faxes'


class ExpomaritFisico(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=40, blank=True, null=True)  # Field name made lowercase.
    marcas = models.CharField(db_column='Marcas', max_length=13, blank=True, null=True)  # Field name made lowercase.
    precinto = models.CharField(db_column='Precinto', max_length=12, blank=True, null=True)  # Field name made lowercase.
    tara = models.IntegerField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    peso = models.DecimalField(db_column='Peso', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    detalle2 = models.CharField(blank=True, null=True)
    cliente = models.IntegerField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.Fisico'


class ExpomaritGastoshijos(models.Model):
    cliente = models.CharField(blank=True, null=True)
    codigo = models.CharField(blank=True, null=True)
    precio = models.CharField(blank=True, null=True)
    tipogasto = models.CharField(blank=True, null=True)
    modo = models.CharField(blank=True, null=True)
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.CharField(db_column='Costo', blank=True, null=True)  # Field name made lowercase.
    statushijos = models.CharField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    movimiento = models.CharField(db_column='Movimiento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.Gastoshijos'


class ExpomaritGuiasgrabadas(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    empresa = models.CharField(blank=True, null=True)
    direccion = models.CharField(blank=True, null=True)
    pais = models.CharField(blank=True, null=True)
    localidad = models.CharField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True)
    cliente1 = models.CharField(max_length=25, blank=True, null=True)
    cliente2 = models.CharField(max_length=38, blank=True, null=True)
    cliente3 = models.CharField(max_length=29, blank=True, null=True)
    cliente4 = models.CharField(max_length=50, blank=True, null=True)
    consigna = models.CharField(max_length=37, blank=True, null=True)
    direcconsigna = models.CharField(max_length=45, blank=True, null=True)
    localconsigna = models.CharField(max_length=34, blank=True, null=True)
    teleconsigna = models.CharField(max_length=25, blank=True, null=True)
    otralinea = models.CharField(blank=True, null=True)
    notif = models.CharField(max_length=37, blank=True, null=True)
    dirnotif = models.CharField(max_length=45, blank=True, null=True)
    otralinea2 = models.CharField(max_length=34, blank=True, null=True)
    telnotif = models.CharField(max_length=25, blank=True, null=True)
    tipoflete = models.CharField(max_length=15, blank=True, null=True)
    position = models.CharField(max_length=15, blank=True, null=True)
    salede = models.CharField(max_length=10, blank=True, null=True)
    vapor = models.CharField(max_length=17, blank=True, null=True)
    viaje = models.CharField(max_length=5, blank=True, null=True)
    loading = models.CharField(max_length=10, blank=True, null=True)
    discharge = models.CharField(max_length=25, blank=True, null=True)
    delivery = models.CharField(max_length=25, blank=True, null=True)
    transterms = models.CharField(max_length=4, blank=True, null=True)
    simbolo = models.CharField(max_length=3, blank=True, null=True)
    condentrega = models.CharField(max_length=3, blank=True, null=True)
    tipomov = models.CharField(max_length=7, blank=True, null=True)
    carriage = models.CharField(blank=True, null=True)
    custom = models.CharField(blank=True, null=True)
    valseguro = models.CharField(blank=True, null=True)
    goods = models.CharField(blank=True, null=True)
    free1 = models.CharField(blank=True, null=True)
    free2 = models.CharField(blank=True, null=True)
    free3 = models.CharField(blank=True, null=True)
    signature = models.CharField(max_length=42, blank=True, null=True)
    signature2 = models.CharField(max_length=46, blank=True, null=True)
    signature3 = models.CharField(max_length=29, blank=True, null=True)
    nbls = models.IntegerField(blank=True, null=True)
    payable = models.CharField(max_length=15, blank=True, null=True)
    board = models.CharField(max_length=10, blank=True, null=True)
    clean = models.CharField(max_length=14, blank=True, null=True)
    fechaemi = models.CharField(max_length=10, blank=True, null=True)
    restotext = models.CharField(max_length=10, blank=True, null=True)
    portext = models.CharField(max_length=14, blank=True, null=True)
    vadeclared = models.IntegerField(blank=True, null=True)
    cliente5 = models.CharField(max_length=41, blank=True, null=True)
    otranotif = models.CharField(blank=True, null=True)
    signature4 = models.CharField(blank=True, null=True)
    signature5 = models.CharField(max_length=9, blank=True, null=True)
    booking = models.CharField(blank=True, null=True)
    position2 = models.CharField(max_length=9, blank=True, null=True)
    origin = models.CharField(db_column='Origin', max_length=7, blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', max_length=6, blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=3, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    awb = models.CharField(db_column='AWB', max_length=16, blank=True, null=True)  # Field name made lowercase.
    hawb = models.CharField(db_column='HAWB', max_length=11, blank=True, null=True)  # Field name made lowercase.
    totalkilos = models.DecimalField(db_column='TotalKilos', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    totalpaquetes = models.IntegerField(db_column='TotalPaquetes', blank=True, null=True)  # Field name made lowercase.
    tipodocumento = models.CharField(db_column='TipoDocumento', max_length=1, blank=True, null=True)  # Field name made lowercase.
    consolidado = models.IntegerField(db_column='Consolidado', blank=True, null=True)  # Field name made lowercase.
    mensaje1 = models.IntegerField(db_column='Mensaje1', blank=True, null=True)  # Field name made lowercase.
    mensaje2 = models.IntegerField(db_column='Mensaje2', blank=True, null=True)  # Field name made lowercase.
    label6 = models.CharField(db_column='Label6', max_length=18, blank=True, null=True)  # Field name made lowercase.
    texto = models.CharField(db_column='Texto', blank=True, null=True)  # Field name made lowercase.
    consigna6 = models.CharField(db_column='Consigna6', blank=True, null=True)  # Field name made lowercase.
    consigna7 = models.CharField(db_column='Consigna7', blank=True, null=True)  # Field name made lowercase.
    consigna8 = models.CharField(db_column='Consigna8', blank=True, null=True)  # Field name made lowercase.
    precarriage = models.CharField(db_column='PreCarriage', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.GuiasGrabadas'


class ExpomaritGuiasgrabadas2(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    marks = models.CharField(max_length=12, blank=True, null=True)
    packages = models.CharField(max_length=2, blank=True, null=True)
    description = models.CharField(max_length=36, blank=True, null=True)
    gross = models.CharField(max_length=8, blank=True, null=True)
    tare = models.CharField(max_length=7, blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)
    tara2 = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Expomarit.GuiasGrabadas2'


class ExpomaritGuiasgrabadas3(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    servicio = models.CharField(db_column='Servicio', blank=True, null=True)  # Field name made lowercase.
    prepaid = models.CharField(db_column='Prepaid', blank=True, null=True)  # Field name made lowercase.
    collect = models.CharField(db_column='Collect', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.GuiasGrabadas3'


class ExpomaritMadresgrabadas(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    empresa = models.CharField(blank=True, null=True)
    direccion = models.CharField(blank=True, null=True)
    pais = models.CharField(blank=True, null=True)
    localidad = models.CharField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True)
    cliente1 = models.CharField(max_length=14, blank=True, null=True)
    cliente2 = models.CharField(max_length=20, blank=True, null=True)
    cliente3 = models.CharField(max_length=20, blank=True, null=True)
    cliente4 = models.CharField(max_length=37, blank=True, null=True)
    consigna = models.CharField(max_length=22, blank=True, null=True)
    direcconsigna = models.CharField(max_length=29, blank=True, null=True)
    localconsigna = models.CharField(max_length=25, blank=True, null=True)
    teleconsigna = models.CharField(max_length=19, blank=True, null=True)
    otralinea = models.CharField(blank=True, null=True)
    notif = models.CharField(max_length=22, blank=True, null=True)
    dirnotif = models.CharField(max_length=29, blank=True, null=True)
    otralinea2 = models.CharField(max_length=25, blank=True, null=True)
    telnotif = models.CharField(max_length=9, blank=True, null=True)
    tipoflete = models.CharField(max_length=15, blank=True, null=True)
    position = models.CharField(blank=True, null=True)
    salede = models.CharField(max_length=10, blank=True, null=True)
    vapor = models.CharField(max_length=15, blank=True, null=True)
    viaje = models.CharField(max_length=5, blank=True, null=True)
    loading = models.CharField(max_length=10, blank=True, null=True)
    discharge = models.CharField(max_length=10, blank=True, null=True)
    delivery = models.CharField(max_length=10, blank=True, null=True)
    transterms = models.CharField(blank=True, null=True)
    simbolo = models.CharField(max_length=3, blank=True, null=True)
    condentrega = models.CharField(blank=True, null=True)
    tipomov = models.CharField(blank=True, null=True)
    carriage = models.CharField(blank=True, null=True)
    custom = models.CharField(blank=True, null=True)
    valseguro = models.CharField(blank=True, null=True)
    goods = models.CharField(blank=True, null=True)
    free1 = models.CharField(blank=True, null=True)
    free2 = models.CharField(blank=True, null=True)
    free3 = models.CharField(blank=True, null=True)
    signature = models.CharField(blank=True, null=True)
    signature2 = models.CharField(blank=True, null=True)
    signature3 = models.CharField(blank=True, null=True)
    nbls = models.IntegerField(blank=True, null=True)
    payable = models.CharField(max_length=10, blank=True, null=True)
    board = models.CharField(max_length=10, blank=True, null=True)
    clean = models.CharField(max_length=14, blank=True, null=True)
    fechaemi = models.CharField(max_length=10, blank=True, null=True)
    restotext = models.CharField(max_length=10, blank=True, null=True)
    portext = models.CharField(blank=True, null=True)
    vadeclared = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Expomarit.Madresgrabadas'


class ExpomaritMadresgrabadas2(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    marks = models.CharField(max_length=12, blank=True, null=True)
    packages = models.CharField(max_length=1, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    gross = models.CharField(max_length=6, blank=True, null=True)
    tare = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Expomarit.Madresgrabadas2'


class ExpomaritReservas(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    transportista = models.SmallIntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    kilos = models.CharField(db_column='Kilos', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    awb = models.CharField(max_length=20, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    moneda = models.IntegerField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=3, blank=True, null=True)  # Field name made lowercase.
    volumen = models.CharField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    aduana = models.CharField(max_length=3, blank=True, null=True)
    profitage = models.CharField(max_length=6, blank=True, null=True)
    tarifapl = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=20, blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=9, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=15, blank=True, null=True)  # Field name made lowercase.
    envioedi = models.CharField(max_length=1, blank=True, null=True)
    nroreferedi = models.CharField(blank=True, null=True)
    ciep = models.CharField(max_length=3, blank=True, null=True)
    armador = models.SmallIntegerField(blank=True, null=True)
    operacion = models.CharField(max_length=23, blank=True, null=True)
    plfacturado = models.CharField(max_length=1, blank=True, null=True)
    trafico = models.IntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=8, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=3, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', blank=True, null=True)  # Field name made lowercase.
    enviointtrabk = models.CharField(db_column='EnvioInttraBK', blank=True, null=True)  # Field name made lowercase.
    enviointtrasi = models.CharField(db_column='EnvioInttraSI', blank=True, null=True)  # Field name made lowercase.
    maerskbk = models.CharField(db_column='MaerskBK', blank=True, null=True)  # Field name made lowercase.
    maersksi = models.CharField(db_column='MaerskSI', blank=True, null=True)  # Field name made lowercase.
    embarcador = models.CharField(db_column='Embarcador', max_length=2, blank=True, null=True)  # Field name made lowercase.
    esagente = models.CharField(db_column='esAgente', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=3, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=14, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FechaIngreso', max_length=19, blank=True, null=True)  # Field name made lowercase.
    tipobl = models.CharField(db_column='TipoBL', max_length=2, blank=True, null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', blank=True, null=True)  # Field name made lowercase.
    deposito = models.IntegerField(db_column='Deposito', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.Reservas'


class ExpomaritServireserva(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    costo = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=34, blank=True, null=True)
    tipogasto = models.CharField(max_length=13, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    descripcion = models.CharField(max_length=3, blank=True, null=True)
    precio = models.CharField(blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=15, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.Servireserva'


class ExpomaritTraceop(models.Model):
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=11, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=109, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=8, blank=True, null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.TraceOP'


class ExpomaritConexaerea(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=4, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=22, blank=True, null=True)  # Field name made lowercase.
    salida = models.CharField(max_length=19, blank=True, null=True)
    llegada = models.CharField(max_length=19, blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(max_length=8, blank=True, null=True)
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    horaorigen = models.CharField(db_column='HoraOrigen', blank=True, null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.conexaerea'


class ExpomaritServiceaereo(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=30, blank=True, null=True)
    tipogasto = models.CharField(max_length=13, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    descripcion = models.CharField(max_length=3, blank=True, null=True)
    pinformar = models.CharField(max_length=10, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=21, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expomarit.serviceaereo'


class ExportAnulados(models.Model):
    fecha = models.CharField(max_length=19, blank=True, null=True)
    detalle = models.CharField(max_length=47, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Export.Anulados'


class ExportAttachhijo(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=111, blank=True, null=True)
    detalle = models.CharField(max_length=22, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.AttachHijo'


class ExportAttachmadre(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=61, blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.AttachMadre'


class ExportCargaaerea(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.SmallIntegerField(blank=True, null=True)
    bruto = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    medidas = models.CharField(max_length=18, blank=True, null=True)
    tipo = models.CharField(max_length=8, blank=True, null=True)
    fechaembarque = models.CharField(max_length=19, blank=True, null=True)
    tarifa = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    aplicable = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    unidad = models.CharField(db_column='Unidad', blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', blank=True, null=True)  # Field name made lowercase.
    tara = models.CharField(db_column='Tara', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.Cargaaerea'


class ExportClavehawb(models.Model):
    hawb = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Export.ClaveHawb'


class ExportClaveguia(models.Model):
    awb = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Export.Claveguia'


class ExportClaveposicion(models.Model):
    posicion = models.CharField(max_length=10, blank=True, null=True)
    numeroorden = models.IntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.Claveposicion'


class ExportConexreserva(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    vuelo = models.CharField(max_length=8, blank=True, null=True)
    salida = models.CharField(max_length=19, blank=True, null=True)
    llegada = models.CharField(max_length=19, blank=True, null=True)
    ciavuelo = models.CharField(max_length=2, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    horaorigen = models.CharField(db_column='HoraOrigen', blank=True, null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.Conexreserva'


class ExportEmbarqueaereo(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    cliente = models.SmallIntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    notificante = models.SmallIntegerField(blank=True, null=True)
    despachante = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    consolidado = models.IntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=15, blank=True, null=True)
    operacion = models.CharField(max_length=11, blank=True, null=True)
    aduana = models.CharField(max_length=3, blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    pago = models.CharField(blank=True, null=True)
    awb = models.CharField(max_length=12, blank=True, null=True)
    hawb = models.CharField(max_length=12, blank=True, null=True)
    transportista = models.SmallIntegerField(blank=True, null=True)
    valortransporte = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    valoraduana = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    fechaembarque = models.CharField(max_length=19, blank=True, null=True)
    fecharetiro = models.CharField(max_length=19, blank=True, null=True)
    pagoflete = models.CharField(max_length=1, blank=True, null=True)
    marcas = models.CharField(max_length=26, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=126, blank=True, null=True)  # Field name made lowercase.
    valorseguro = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    tomopeso = models.IntegerField(blank=True, null=True)
    aplicable = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    tarifaventa = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    tarifacompra = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    volumencubico = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    cotizacion = models.IntegerField(blank=True, null=True)
    cotitransp = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    aplitransp = models.DecimalField(max_digits=23, decimal_places=17, blank=True, null=True)
    facturado = models.CharField(max_length=1, blank=True, null=True)
    profitage = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    tarifafija = models.CharField(max_length=1, blank=True, null=True)
    tipobonifcli = models.CharField(max_length=1, blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    over = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    tipoover = models.CharField(max_length=1, blank=True, null=True)
    comision = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    tipovend = models.CharField(db_column='Tipovend', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendedor = models.IntegerField(blank=True, null=True)
    comivend = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    reporteada = models.IntegerField(blank=True, null=True)
    nroreferedi = models.IntegerField(blank=True, null=True)
    impresiones = models.IntegerField(blank=True, null=True)
    ordencliente = models.CharField(max_length=26, blank=True, null=True)
    propia = models.IntegerField(blank=True, null=True)
    embarcador = models.SmallIntegerField(blank=True, null=True)
    vaporcli = models.CharField(blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    trafico = models.IntegerField(blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    agente = models.SmallIntegerField(db_column='Agente', blank=True, null=True)  # Field name made lowercase.
    tarifaprofit = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    hawbtext = models.CharField(db_column='HawbText', max_length=3, blank=True, null=True)  # Field name made lowercase.
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=3, blank=True, null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=3, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=3, blank=True, null=True)  # Field name made lowercase.
    mercaderia = models.CharField(db_column='Mercaderia', max_length=204, blank=True, null=True)  # Field name made lowercase.
    proyecto = models.IntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    datosnotificante = models.CharField(db_column='DatosNotificante', max_length=3, blank=True, null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=26, blank=True, null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=8, blank=True, null=True)  # Field name made lowercase.
    arbitrajecass = models.DecimalField(db_column='ArbitrajeCASS', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=13, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', blank=True, null=True)  # Field name made lowercase.
    servicelevel = models.CharField(blank=True, null=True)
    serviceleveltype = models.CharField(blank=True, null=True)
    stthawb = models.CharField(blank=True, null=True)
    sttawb = models.CharField(blank=True, null=True)
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    fechaentrega = models.CharField(db_column='FechaEntrega', max_length=19, blank=True, null=True)  # Field name made lowercase.
    aquienentrega = models.CharField(db_column='aQuienEntrega', max_length=3, blank=True, null=True)  # Field name made lowercase.
    actividad = models.IntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    deposito = models.IntegerField(db_column='Deposito', blank=True, null=True)  # Field name made lowercase.
    autogenfletecpa = models.CharField(db_column='AutogenFleteCPA', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    envioiata = models.CharField(db_column='EnvioIATA', blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FechaIngreso', max_length=19, blank=True, null=True)  # Field name made lowercase.
    documentos = models.CharField(db_column='Documentos', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=3, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=3, blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', blank=True, null=True)  # Field name made lowercase.
    etd = models.CharField(db_column='ETD', max_length=19, blank=True, null=True)  # Field name made lowercase.
    eta = models.CharField(db_column='ETA', max_length=19, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.Embarqueaereo'


class ExportEntregadoc(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    entreguese = models.CharField(db_column='Entreguese', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nombreentrega = models.CharField(db_column='NombreEntrega', max_length=38, blank=True, null=True)  # Field name made lowercase.
    direccionentrega = models.CharField(db_column='DireccionEntrega', max_length=47, blank=True, null=True)  # Field name made lowercase.
    ciudadentrega = models.CharField(db_column='CiudadEntrega', max_length=10, blank=True, null=True)  # Field name made lowercase.
    telefonoentrega = models.CharField(db_column='TelefonoEntrega', max_length=12, blank=True, null=True)  # Field name made lowercase.
    original = models.CharField(db_column='Original', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lista = models.CharField(db_column='Lista', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certorigen = models.CharField(db_column='CertOrigen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    declara = models.CharField(db_column='Declara', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certflete = models.CharField(db_column='CertFlete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cerseguro = models.CharField(db_column='CerSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    copiahbl = models.CharField(db_column='CopiaHBL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    otros = models.CharField(db_column='Otros', max_length=1, blank=True, null=True)  # Field name made lowercase.
    detotros = models.CharField(db_column='DetOtros', max_length=18, blank=True, null=True)  # Field name made lowercase.
    detotros2 = models.CharField(db_column='DetOtros2', blank=True, null=True)  # Field name made lowercase.
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
    remarks = models.CharField(db_column='Remarks', blank=True, null=True)  # Field name made lowercase.
    remarks2 = models.CharField(db_column='Remarks2', blank=True, null=True)  # Field name made lowercase.
    facturacom = models.CharField(db_column='FacturaCom', blank=True, null=True)  # Field name made lowercase.
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', blank=True, null=True)  # Field name made lowercase.
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', blank=True, null=True)  # Field name made lowercase.
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crtnumero = models.CharField(db_column='CRTNumero', blank=True, null=True)  # Field name made lowercase.
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', blank=True, null=True)  # Field name made lowercase.
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    micdtanumero = models.CharField(db_column='MicDtaNumero', blank=True, null=True)  # Field name made lowercase.
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    papeletanumero = models.CharField(db_column='PapeletaNumero', blank=True, null=True)  # Field name made lowercase.
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True, null=True)  # Field name made lowercase.
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', blank=True, null=True)  # Field name made lowercase.
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', blank=True, null=True)  # Field name made lowercase.
    certorigennumero = models.CharField(db_column='CertOrigenNumero', blank=True, null=True)  # Field name made lowercase.
    certseguronumero = models.CharField(db_column='CertSeguroNumero', blank=True, null=True)  # Field name made lowercase.
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', blank=True, null=True)  # Field name made lowercase.
    detotros3 = models.CharField(db_column='DetOtros3', blank=True, null=True)  # Field name made lowercase.
    detotros4 = models.CharField(db_column='DetOtros4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.EntregaDoc'


class ExportFaxes(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.CharField(max_length=193, blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)
    status = models.CharField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.Faxes'


class ExportGastoshijos(models.Model):
    cliente = models.CharField(blank=True, null=True)
    codigo = models.CharField(blank=True, null=True)
    precio = models.CharField(blank=True, null=True)
    tipogasto = models.CharField(blank=True, null=True)
    modo = models.CharField(blank=True, null=True)
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.CharField(db_column='Costo', blank=True, null=True)  # Field name made lowercase.
    statushijos = models.CharField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.Gastoshijos'


class ExportGuiasgrabadas(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    empresa = models.CharField(max_length=22, blank=True, null=True)
    direccion = models.CharField(max_length=38, blank=True, null=True)
    pais = models.CharField(max_length=7, blank=True, null=True)
    localidad = models.CharField(max_length=22, blank=True, null=True)
    telefono = models.CharField(max_length=44, blank=True, null=True)
    cliente1 = models.CharField(max_length=45, blank=True, null=True)
    cliente2 = models.CharField(max_length=45, blank=True, null=True)
    cliente3 = models.CharField(max_length=45, blank=True, null=True)
    cliente4 = models.CharField(max_length=45, blank=True, null=True)
    consigna = models.CharField(max_length=45, blank=True, null=True)
    direcconsigna = models.CharField(max_length=45, blank=True, null=True)
    localconsigna = models.CharField(max_length=45, blank=True, null=True)
    teleconsigna = models.CharField(max_length=45, blank=True, null=True)
    otralinea = models.CharField(max_length=45, blank=True, null=True)
    empresa2 = models.CharField(max_length=21, blank=True, null=True)
    otracarrier = models.CharField(max_length=27, blank=True, null=True)
    localidad2 = models.CharField(max_length=27, blank=True, null=True)
    otrosdeagente = models.CharField(max_length=35, blank=True, null=True)
    iata = models.CharField(max_length=10, blank=True, null=True)
    salede = models.CharField(max_length=10, blank=True, null=True)
    cadenaaerea = models.CharField(max_length=20, blank=True, null=True)
    tipoflete = models.CharField(max_length=15, blank=True, null=True)
    numerolc = models.CharField(blank=True, null=True)
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
    simbolo = models.CharField(max_length=3, blank=True, null=True)
    carriage = models.CharField(max_length=3, blank=True, null=True)
    custom = models.CharField(max_length=3, blank=True, null=True)
    nombredestino = models.CharField(max_length=22, blank=True, null=True)
    vuelo1 = models.CharField(max_length=15, blank=True, null=True)
    vuelo2 = models.CharField(max_length=14, blank=True, null=True)
    vuelo3 = models.CharField(max_length=15, blank=True, null=True)
    vuelo4 = models.CharField(max_length=13, blank=True, null=True)
    valseguro = models.CharField(max_length=3, blank=True, null=True)
    cliente5 = models.CharField(db_column='Cliente5', max_length=44, blank=True, null=True)  # Field name made lowercase.
    consigna6 = models.CharField(db_column='Consigna6', max_length=44, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.GuiasGrabadas'


class ExportGuiasgrabadas2(models.Model):
    marcas = models.CharField(max_length=76, blank=True, null=True)
    otraline = models.CharField(max_length=80, blank=True, null=True)
    attached = models.CharField(max_length=64, blank=True, null=True)
    nature1 = models.CharField(max_length=18, blank=True, null=True)
    nature2 = models.CharField(max_length=25, blank=True, null=True)
    nature3 = models.CharField(max_length=25, blank=True, null=True)
    nature4 = models.CharField(max_length=25, blank=True, null=True)
    nature5 = models.CharField(max_length=25, blank=True, null=True)
    nature6 = models.CharField(max_length=25, blank=True, null=True)
    nature7 = models.CharField(max_length=24, blank=True, null=True)
    nature8 = models.CharField(max_length=25, blank=True, null=True)
    nature9 = models.CharField(max_length=25, blank=True, null=True)
    free1 = models.CharField(max_length=59, blank=True, null=True)
    free2 = models.CharField(max_length=57, blank=True, null=True)
    free3 = models.CharField(max_length=60, blank=True, null=True)
    free4 = models.CharField(max_length=55, blank=True, null=True)
    free5 = models.CharField(max_length=60, blank=True, null=True)
    other1 = models.CharField(max_length=50, blank=True, null=True)
    other2 = models.CharField(max_length=49, blank=True, null=True)
    other3 = models.CharField(max_length=36, blank=True, null=True)
    signature = models.CharField(max_length=45, blank=True, null=True)
    fechaemi = models.CharField(max_length=10, blank=True, null=True)
    restotext = models.CharField(max_length=10, blank=True, null=True)
    portext = models.CharField(max_length=20, blank=True, null=True)
    numero = models.SmallIntegerField(blank=True, null=True)
    nature10 = models.CharField(max_length=25, blank=True, null=True)
    nature11 = models.CharField(max_length=25, blank=True, null=True)
    nature12 = models.CharField(max_length=25, blank=True, null=True)
    gastosconiva = models.IntegerField(blank=True, null=True)
    nature13 = models.CharField(db_column='Nature13', max_length=24, blank=True, null=True)  # Field name made lowercase.
    nature14 = models.CharField(db_column='Nature14', max_length=24, blank=True, null=True)  # Field name made lowercase.
    nature15 = models.CharField(db_column='Nature15', max_length=24, blank=True, null=True)  # Field name made lowercase.
    nature16 = models.CharField(db_column='Nature16', max_length=24, blank=True, null=True)  # Field name made lowercase.
    nature17 = models.CharField(db_column='Nature17', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nature18 = models.CharField(db_column='Nature18', blank=True, null=True)  # Field name made lowercase.
    nature19 = models.CharField(db_column='Nature19', blank=True, null=True)  # Field name made lowercase.
    asagent = models.CharField(db_column='AsAgent', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ofthecarrier = models.CharField(db_column='OfTheCarrier', max_length=65, blank=True, null=True)  # Field name made lowercase.
    chargesatdestination = models.CharField(db_column='ChargesAtDestination', max_length=6, blank=True, null=True)  # Field name made lowercase.
    totalcollectcharges = models.CharField(db_column='TotalCollectCharges', max_length=6, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.GuiasGrabadas2'


class ExportGuiasgrabadas3(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    piezas = models.SmallIntegerField(db_column='Piezas', blank=True, null=True)  # Field name made lowercase.
    piezas2 = models.CharField(db_column='Piezas2', max_length=2, blank=True, null=True)  # Field name made lowercase.
    piezas3 = models.CharField(db_column='Piezas3', max_length=2, blank=True, null=True)  # Field name made lowercase.
    piezas4 = models.CharField(db_column='Piezas4', max_length=1, blank=True, null=True)  # Field name made lowercase.
    piezas5 = models.CharField(db_column='Piezas5', max_length=2, blank=True, null=True)  # Field name made lowercase.
    totpiezas = models.CharField(db_column='TotPiezas', max_length=3, blank=True, null=True)  # Field name made lowercase.
    gross = models.DecimalField(db_column='Gross', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    otrogross = models.CharField(db_column='OtroGross', max_length=7, blank=True, null=True)  # Field name made lowercase.
    otrogross2 = models.CharField(db_column='OtroGross2', max_length=6, blank=True, null=True)  # Field name made lowercase.
    otrogross3 = models.CharField(db_column='OtroGross3', max_length=6, blank=True, null=True)  # Field name made lowercase.
    otrogross4 = models.CharField(db_column='OtroGross4', max_length=6, blank=True, null=True)  # Field name made lowercase.
    totgross = models.CharField(db_column='TotGross', max_length=7, blank=True, null=True)  # Field name made lowercase.
    k = models.CharField(db_column='K', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k2 = models.CharField(db_column='K2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k3 = models.CharField(db_column='K3', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k4 = models.CharField(db_column='K4', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k5 = models.CharField(db_column='K5', max_length=1, blank=True, null=True)  # Field name made lowercase.
    r = models.CharField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    r2 = models.CharField(db_column='R2', blank=True, null=True)  # Field name made lowercase.
    r3 = models.CharField(db_column='R3', blank=True, null=True)  # Field name made lowercase.
    r4 = models.CharField(db_column='R4', blank=True, null=True)  # Field name made lowercase.
    r5 = models.CharField(db_column='R5', blank=True, null=True)  # Field name made lowercase.
    commodity = models.CharField(db_column='Commodity', blank=True, null=True)  # Field name made lowercase.
    comm2 = models.CharField(db_column='Comm2', blank=True, null=True)  # Field name made lowercase.
    comm3 = models.CharField(db_column='Comm3', blank=True, null=True)  # Field name made lowercase.
    comm4 = models.CharField(db_column='Comm4', blank=True, null=True)  # Field name made lowercase.
    comm5 = models.CharField(db_column='Comm5', blank=True, null=True)  # Field name made lowercase.
    chw = models.CharField(db_column='Chw', max_length=7, blank=True, null=True)  # Field name made lowercase.
    asvol = models.CharField(db_column='AsVol', max_length=6, blank=True, null=True)  # Field name made lowercase.
    chw3 = models.CharField(db_column='Chw3', blank=True, null=True)  # Field name made lowercase.
    chw4 = models.CharField(db_column='Chw4', blank=True, null=True)  # Field name made lowercase.
    chw5 = models.CharField(db_column='Chw5', blank=True, null=True)  # Field name made lowercase.
    rate = models.CharField(db_column='Rate', max_length=7, blank=True, null=True)  # Field name made lowercase.
    rate2 = models.CharField(db_column='Rate2', blank=True, null=True)  # Field name made lowercase.
    rate3 = models.CharField(db_column='Rate3', blank=True, null=True)  # Field name made lowercase.
    rate4 = models.CharField(db_column='Rate4', blank=True, null=True)  # Field name made lowercase.
    rate5 = models.CharField(db_column='Rate5', blank=True, null=True)  # Field name made lowercase.
    total = models.CharField(db_column='Total', max_length=9, blank=True, null=True)  # Field name made lowercase.
    total2 = models.CharField(db_column='Total2', blank=True, null=True)  # Field name made lowercase.
    total3 = models.CharField(db_column='Total3', blank=True, null=True)  # Field name made lowercase.
    total4 = models.CharField(db_column='Total4', blank=True, null=True)  # Field name made lowercase.
    total5 = models.CharField(db_column='Total5', blank=True, null=True)  # Field name made lowercase.
    totalfinal = models.CharField(db_column='TotalFinal', max_length=9, blank=True, null=True)  # Field name made lowercase.
    totalpp = models.CharField(db_column='TotalPP', max_length=9, blank=True, null=True)  # Field name made lowercase.
    totalcc = models.CharField(db_column='TotalCC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    valpp = models.CharField(db_column='ValPP', max_length=9, blank=True, null=True)  # Field name made lowercase.
    valcc = models.CharField(db_column='ValCC', blank=True, null=True)  # Field name made lowercase.
    taxpp = models.CharField(db_column='TaxPP', blank=True, null=True)  # Field name made lowercase.
    taxcc = models.CharField(db_column='TaxCC', blank=True, null=True)  # Field name made lowercase.
    dapp = models.CharField(db_column='DaPP', max_length=9, blank=True, null=True)  # Field name made lowercase.
    dacc = models.CharField(db_column='DaCC', max_length=9, blank=True, null=True)  # Field name made lowercase.
    dcpp = models.CharField(db_column='DcPP', max_length=9, blank=True, null=True)  # Field name made lowercase.
    dccc = models.CharField(db_column='DcCC', max_length=9, blank=True, null=True)  # Field name made lowercase.
    totalprepaid = models.CharField(db_column='TotalPrepaid', max_length=9, blank=True, null=True)  # Field name made lowercase.
    totalcollect = models.CharField(db_column='TotalCollect', max_length=9, blank=True, null=True)  # Field name made lowercase.
    totalpprate = models.CharField(db_column='TotalPPRate', blank=True, null=True)  # Field name made lowercase.
    totalccrate = models.CharField(db_column='TotalCCRate', blank=True, null=True)  # Field name made lowercase.
    cass = models.CharField(db_column='Cass', max_length=3, blank=True, null=True)  # Field name made lowercase.
    chgscode = models.CharField(db_column='ChgsCode', max_length=2, blank=True, null=True)  # Field name made lowercase.
    wtval = models.CharField(db_column='WtVal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(db_column='Other', max_length=1, blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', max_length=50, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=15, blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    carrierfinal = models.CharField(db_column='CarrierFinal', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.GuiasGrabadas3'


class ExportMadresgrabadas(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    empresa = models.CharField(max_length=35, blank=True, null=True)
    direccion = models.CharField(max_length=38, blank=True, null=True)
    pais = models.CharField(max_length=7, blank=True, null=True)
    localidad = models.CharField(max_length=22, blank=True, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    cliente1 = models.CharField(max_length=15, blank=True, null=True)
    cliente2 = models.CharField(max_length=20, blank=True, null=True)
    cliente3 = models.CharField(max_length=45, blank=True, null=True)
    cliente4 = models.CharField(max_length=18, blank=True, null=True)
    consigna = models.CharField(max_length=45, blank=True, null=True)
    direcconsigna = models.CharField(max_length=45, blank=True, null=True)
    localconsigna = models.CharField(max_length=45, blank=True, null=True)
    teleconsigna = models.CharField(max_length=44, blank=True, null=True)
    otralinea = models.CharField(max_length=44, blank=True, null=True)
    empresa2 = models.CharField(max_length=21, blank=True, null=True)
    otracarrier = models.CharField(max_length=32, blank=True, null=True)
    localidad2 = models.CharField(max_length=27, blank=True, null=True)
    otrosdeagente = models.CharField(max_length=18, blank=True, null=True)
    iata = models.CharField(max_length=10, blank=True, null=True)
    salede = models.CharField(max_length=10, blank=True, null=True)
    cadenaaerea = models.CharField(max_length=20, blank=True, null=True)
    tipoflete = models.CharField(max_length=15, blank=True, null=True)
    notif = models.CharField(max_length=45, blank=True, null=True)
    dirnotif = models.CharField(max_length=45, blank=True, null=True)
    otralinea2 = models.CharField(max_length=45, blank=True, null=True)
    telnotif = models.CharField(max_length=45, blank=True, null=True)
    otralinea3 = models.CharField(max_length=44, blank=True, null=True)
    otralinea4 = models.CharField(max_length=43, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    idtransport = models.CharField(max_length=2, blank=True, null=True)
    to1 = models.CharField(max_length=3, blank=True, null=True)
    by1 = models.CharField(max_length=2, blank=True, null=True)
    to2 = models.CharField(max_length=3, blank=True, null=True)
    by2 = models.CharField(max_length=2, blank=True, null=True)
    simbolo = models.CharField(max_length=3, blank=True, null=True)
    carriage = models.CharField(max_length=3, blank=True, null=True)
    custom = models.CharField(max_length=3, blank=True, null=True)
    nombredestino = models.CharField(max_length=22, blank=True, null=True)
    vuelo1 = models.CharField(max_length=15, blank=True, null=True)
    vuelo2 = models.CharField(max_length=14, blank=True, null=True)
    vuelo3 = models.CharField(max_length=14, blank=True, null=True)
    vuelo4 = models.CharField(max_length=13, blank=True, null=True)
    valseguro = models.CharField(max_length=3, blank=True, null=True)
    marcas = models.CharField(max_length=73, blank=True, null=True)
    otraline = models.CharField(max_length=75, blank=True, null=True)
    attached = models.CharField(max_length=61, blank=True, null=True)
    nature2 = models.CharField(max_length=20, blank=True, null=True)
    nature3 = models.CharField(max_length=23, blank=True, null=True)
    houses = models.CharField(max_length=27, blank=True, null=True)
    houses2 = models.CharField(max_length=28, blank=True, null=True)
    houses3 = models.CharField(max_length=26, blank=True, null=True)
    free1 = models.CharField(max_length=38, blank=True, null=True)
    free2 = models.CharField(max_length=37, blank=True, null=True)
    free3 = models.CharField(max_length=41, blank=True, null=True)
    free4 = models.CharField(max_length=39, blank=True, null=True)
    free5 = models.CharField(blank=True, null=True)
    other1 = models.CharField(max_length=33, blank=True, null=True)
    other2 = models.CharField(max_length=48, blank=True, null=True)
    other3 = models.CharField(max_length=13, blank=True, null=True)
    signature = models.CharField(max_length=14, blank=True, null=True)
    fechaemi = models.CharField(max_length=10, blank=True, null=True)
    restotext = models.CharField(max_length=10, blank=True, null=True)
    portext = models.CharField(max_length=21, blank=True, null=True)
    houses4 = models.CharField(db_column='Houses4', max_length=24, blank=True, null=True)  # Field name made lowercase.
    houses5 = models.CharField(db_column='Houses5', blank=True, null=True)  # Field name made lowercase.
    houses6 = models.CharField(db_column='Houses6', blank=True, null=True)  # Field name made lowercase.
    asagent = models.CharField(db_column='AsAgent', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ofthecarrier = models.CharField(db_column='OfTheCarrier', max_length=45, blank=True, null=True)  # Field name made lowercase.
    gastosconiva = models.IntegerField(db_column='GastosConIVA', blank=True, null=True)  # Field name made lowercase.
    houses7 = models.CharField(db_column='Houses7', blank=True, null=True)  # Field name made lowercase.
    houses8 = models.CharField(db_column='Houses8', blank=True, null=True)  # Field name made lowercase.
    houses9 = models.CharField(db_column='Houses9', blank=True, null=True)  # Field name made lowercase.
    houses10 = models.CharField(db_column='Houses10', blank=True, null=True)  # Field name made lowercase.
    houses11 = models.CharField(db_column='Houses11', blank=True, null=True)  # Field name made lowercase.
    houses12 = models.CharField(db_column='Houses12', blank=True, null=True)  # Field name made lowercase.
    houses13 = models.CharField(db_column='Houses13', blank=True, null=True)  # Field name made lowercase.
    houses14 = models.CharField(db_column='Houses14', blank=True, null=True)  # Field name made lowercase.
    houses15 = models.CharField(db_column='Houses15', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.MadresGrabadas'


class ExportMadresgrabadas3(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    piezas = models.SmallIntegerField(db_column='Piezas', blank=True, null=True)  # Field name made lowercase.
    piezas2 = models.CharField(db_column='Piezas2', blank=True, null=True)  # Field name made lowercase.
    piezas3 = models.CharField(db_column='Piezas3', blank=True, null=True)  # Field name made lowercase.
    piezas4 = models.CharField(db_column='Piezas4', blank=True, null=True)  # Field name made lowercase.
    piezas5 = models.CharField(db_column='Piezas5', blank=True, null=True)  # Field name made lowercase.
    totpiezas = models.SmallIntegerField(db_column='TotPiezas', blank=True, null=True)  # Field name made lowercase.
    gross = models.DecimalField(db_column='Gross', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    otrogross = models.CharField(db_column='OtroGross', blank=True, null=True)  # Field name made lowercase.
    otrogross2 = models.CharField(db_column='OtroGross2', blank=True, null=True)  # Field name made lowercase.
    otrogross3 = models.CharField(db_column='OtroGross3', blank=True, null=True)  # Field name made lowercase.
    otrogross4 = models.CharField(db_column='OtroGross4', blank=True, null=True)  # Field name made lowercase.
    totgross = models.DecimalField(db_column='TotGross', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    k = models.CharField(db_column='K', max_length=1, blank=True, null=True)  # Field name made lowercase.
    k2 = models.CharField(db_column='K2', blank=True, null=True)  # Field name made lowercase.
    k3 = models.CharField(db_column='K3', blank=True, null=True)  # Field name made lowercase.
    k4 = models.CharField(db_column='K4', blank=True, null=True)  # Field name made lowercase.
    k5 = models.CharField(db_column='K5', blank=True, null=True)  # Field name made lowercase.
    r = models.CharField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    r2 = models.CharField(db_column='R2', blank=True, null=True)  # Field name made lowercase.
    r3 = models.CharField(db_column='R3', blank=True, null=True)  # Field name made lowercase.
    r4 = models.CharField(db_column='R4', blank=True, null=True)  # Field name made lowercase.
    r5 = models.CharField(db_column='R5', blank=True, null=True)  # Field name made lowercase.
    commodity = models.CharField(db_column='Commodity', blank=True, null=True)  # Field name made lowercase.
    comm2 = models.CharField(db_column='Comm2', blank=True, null=True)  # Field name made lowercase.
    comm3 = models.CharField(db_column='Comm3', blank=True, null=True)  # Field name made lowercase.
    comm4 = models.CharField(db_column='Comm4', blank=True, null=True)  # Field name made lowercase.
    comm5 = models.CharField(db_column='Comm5', blank=True, null=True)  # Field name made lowercase.
    chw = models.CharField(db_column='Chw', max_length=7, blank=True, null=True)  # Field name made lowercase.
    asvol = models.CharField(db_column='AsVol', max_length=6, blank=True, null=True)  # Field name made lowercase.
    chw3 = models.CharField(db_column='Chw3', blank=True, null=True)  # Field name made lowercase.
    chw4 = models.CharField(db_column='Chw4', blank=True, null=True)  # Field name made lowercase.
    chw5 = models.CharField(db_column='Chw5', blank=True, null=True)  # Field name made lowercase.
    rate = models.CharField(db_column='Rate', max_length=7, blank=True, null=True)  # Field name made lowercase.
    rate2 = models.CharField(db_column='Rate2', blank=True, null=True)  # Field name made lowercase.
    rate3 = models.CharField(db_column='Rate3', blank=True, null=True)  # Field name made lowercase.
    rate4 = models.CharField(db_column='Rate4', blank=True, null=True)  # Field name made lowercase.
    rate5 = models.CharField(db_column='Rate5', blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    total2 = models.CharField(db_column='Total2', blank=True, null=True)  # Field name made lowercase.
    total3 = models.CharField(db_column='Total3', blank=True, null=True)  # Field name made lowercase.
    total4 = models.CharField(db_column='Total4', blank=True, null=True)  # Field name made lowercase.
    total5 = models.CharField(db_column='Total5', blank=True, null=True)  # Field name made lowercase.
    totalfinal = models.DecimalField(db_column='TotalFinal', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    totalpp = models.CharField(db_column='TotalPP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    totalcc = models.CharField(db_column='TotalCC', max_length=6, blank=True, null=True)  # Field name made lowercase.
    valpp = models.CharField(db_column='ValPP', blank=True, null=True)  # Field name made lowercase.
    valcc = models.CharField(db_column='ValCC', blank=True, null=True)  # Field name made lowercase.
    taxpp = models.CharField(db_column='TaxPP', blank=True, null=True)  # Field name made lowercase.
    taxcc = models.CharField(db_column='TaxCC', blank=True, null=True)  # Field name made lowercase.
    dapp = models.CharField(db_column='DaPP', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dacc = models.CharField(db_column='DaCC', max_length=7, blank=True, null=True)  # Field name made lowercase.
    dcpp = models.CharField(db_column='DcPP', max_length=7, blank=True, null=True)  # Field name made lowercase.
    dccc = models.CharField(db_column='DcCC', max_length=6, blank=True, null=True)  # Field name made lowercase.
    totalprepaid = models.CharField(db_column='TotalPrepaid', max_length=8, blank=True, null=True)  # Field name made lowercase.
    totalcollect = models.CharField(db_column='TotalCollect', max_length=7, blank=True, null=True)  # Field name made lowercase.
    totalpprate = models.CharField(db_column='TotalPPRate', blank=True, null=True)  # Field name made lowercase.
    totalccrate = models.CharField(db_column='TotalCCRate', blank=True, null=True)  # Field name made lowercase.
    cass = models.CharField(db_column='Cass', max_length=9, blank=True, null=True)  # Field name made lowercase.
    chgscode = models.CharField(db_column='ChgsCode', max_length=2, blank=True, null=True)  # Field name made lowercase.
    wtval = models.CharField(db_column='WtVal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(db_column='Other', max_length=1, blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', max_length=50, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=15, blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=3, blank=True, null=True)  # Field name made lowercase.
    carrierfinal = models.CharField(db_column='CarrierFinal', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.MadresGrabadas3'


class ExportReservas(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    transportista = models.SmallIntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    vuelo = models.CharField(db_column='Vuelo', blank=True, null=True)  # Field name made lowercase.
    kilos = models.DecimalField(db_column='Kilos', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    awb = models.CharField(max_length=12, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    moneda = models.IntegerField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    tarifaawb = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=3, blank=True, null=True)  # Field name made lowercase.
    volumen = models.DecimalField(db_column='Volumen', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    tomopeso = models.IntegerField(blank=True, null=True)
    aplicable = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    aduana = models.CharField(max_length=3, blank=True, null=True)
    tarifapl = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    profitage = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    plfacturado = models.CharField(max_length=1, blank=True, null=True)
    tipoover = models.CharField(db_column='Tipoover', max_length=1, blank=True, null=True)  # Field name made lowercase.
    over = models.DecimalField(db_column='Over', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    comision = models.DecimalField(db_column='Comision', max_digits=3, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(max_length=15, blank=True, null=True)
    envioedi = models.CharField(max_length=1, blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    reporteada = models.IntegerField(blank=True, null=True)
    nroreferedi = models.IntegerField(blank=True, null=True)
    impresiones = models.IntegerField(blank=True, null=True)
    operacion = models.CharField(max_length=11, blank=True, null=True)
    trafico = models.IntegerField(blank=True, null=True)
    tarifafija = models.CharField(max_length=1, blank=True, null=True)
    fechareport = models.CharField(max_length=19, blank=True, null=True)
    manifiesto = models.CharField(max_length=9, blank=True, null=True)
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=10, blank=True, null=True)  # Field name made lowercase.
    arbitrajecass = models.DecimalField(db_column='ArbitrajeCASS', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', blank=True, null=True)  # Field name made lowercase.
    sttawb = models.CharField(blank=True, null=True)
    autogenfletecpa = models.CharField(db_column='AutogenFleteCPA', blank=True, null=True)  # Field name made lowercase.
    envioiata = models.CharField(db_column='EnvioIATA', blank=True, null=True)  # Field name made lowercase.
    embarcador = models.CharField(db_column='Embarcador', max_length=1, blank=True, null=True)  # Field name made lowercase.
    esagente = models.CharField(db_column='esAgente', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FechaIngreso', max_length=19, blank=True, null=True)  # Field name made lowercase.
    documentos = models.CharField(db_column='Documentos', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', blank=True, null=True)  # Field name made lowercase.
    deposito = models.IntegerField(db_column='Deposito', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.Reservas'


class ExportServireserva(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    costo = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=35, blank=True, null=True)
    tipogasto = models.CharField(max_length=13, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    descripcion = models.CharField(max_length=3, blank=True, null=True)
    precio = models.CharField(blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=16, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.Servireserva'


class ExportTraceop(models.Model):
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=11, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=114, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=8, blank=True, null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.TraceOP'


class ExportConexaerea(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    vuelo = models.CharField(max_length=8, blank=True, null=True)
    salida = models.CharField(max_length=19, blank=True, null=True)
    llegada = models.CharField(max_length=19, blank=True, null=True)
    ciavuelo = models.CharField(max_length=5, blank=True, null=True)
    viaje = models.CharField(max_length=8, blank=True, null=True)
    modo = models.CharField(max_length=5, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    horaorigen = models.CharField(db_column='HoraOrigen', blank=True, null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.conexaerea'


class ExportServiceaereo(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=35, blank=True, null=True)
    tipogasto = models.CharField(max_length=13, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    descripcion = models.CharField(max_length=3, blank=True, null=True)
    pinformar = models.CharField(max_length=10, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=5, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Export.serviceaereo'


class ExpoterraAnulados(models.Model):
    fecha = models.CharField(max_length=19, blank=True, null=True)
    detalle = models.CharField(max_length=34, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Expoterra.Anulados'


class ExpoterraAttachhijo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=64, blank=True, null=True)
    detalle = models.CharField(max_length=15, blank=True, null=True)
    web = models.CharField(blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.AttachHijo'


class ExpoterraAttachmadre(models.Model):
    numero = models.CharField(blank=True, null=True)
    archivo = models.CharField(blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.AttachMadre'


class ExpoterraCargaaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.SmallIntegerField(blank=True, null=True)
    bruto = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    medidas = models.CharField(max_length=3, blank=True, null=True)
    tipo = models.CharField(max_length=8, blank=True, null=True)
    fechaembarque = models.CharField(max_length=19, blank=True, null=True)
    cbm = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    mercaderia = models.CharField(max_length=41, blank=True, null=True)
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.Cargaaerea'


class ExpoterraClaveposicion(models.Model):
    posicion = models.CharField(max_length=10, blank=True, null=True)
    numeroorden = models.IntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.ClavePosicion'


class ExpoterraConexreserva(models.Model):
    numero = models.CharField(blank=True, null=True)
    origen = models.CharField(blank=True, null=True)
    destino = models.CharField(blank=True, null=True)
    salida = models.CharField(blank=True, null=True)
    llegada = models.CharField(blank=True, null=True)
    cia = models.CharField(blank=True, null=True)
    modo = models.CharField(blank=True, null=True)
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.Conexreserva'


class ExpoterraDeclaracion(models.Model):
    numero = models.CharField(blank=True, null=True)
    ncorr = models.CharField(db_column='Ncorr', blank=True, null=True)  # Field name made lowercase.
    nintdespacho = models.CharField(db_column='NintDespacho', blank=True, null=True)  # Field name made lowercase.
    codfisc = models.CharField(db_column='CodFisc', blank=True, null=True)  # Field name made lowercase.
    coddeclaracion = models.CharField(db_column='CodDeclaracion', blank=True, null=True)  # Field name made lowercase.
    nomdeclaracion = models.CharField(db_column='NomDeclaracion', blank=True, null=True)  # Field name made lowercase.
    aduana = models.CharField(db_column='Aduana', blank=True, null=True)  # Field name made lowercase.
    codaduana = models.CharField(db_column='CodAduana', blank=True, null=True)  # Field name made lowercase.
    regimen = models.CharField(db_column='Regimen', blank=True, null=True)  # Field name made lowercase.
    codregimen = models.CharField(db_column='CodRegimen', blank=True, null=True)  # Field name made lowercase.
    tipotramite = models.CharField(db_column='TipoTramite', blank=True, null=True)  # Field name made lowercase.
    codtramite = models.CharField(db_column='CodTramite', blank=True, null=True)  # Field name made lowercase.
    aduana2 = models.CharField(db_column='Aduana2', blank=True, null=True)  # Field name made lowercase.
    codaduana2 = models.CharField(db_column='CodAduana2', blank=True, null=True)  # Field name made lowercase.
    numero2 = models.CharField(db_column='Numero2', blank=True, null=True)  # Field name made lowercase.
    despachador = models.CharField(db_column='Despachador', blank=True, null=True)  # Field name made lowercase.
    coddespachador = models.CharField(db_column='CodDespachador', blank=True, null=True)  # Field name made lowercase.
    numerodeclaracion = models.CharField(db_column='NumeroDeclaracion', blank=True, null=True)  # Field name made lowercase.
    fechadeclaracion = models.CharField(db_column='FechaDeclaracion', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    consignatario = models.CharField(db_column='Consignatario', blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', blank=True, null=True)  # Field name made lowercase.
    almacenista = models.CharField(db_column='Almacenista', blank=True, null=True)  # Field name made lowercase.
    codalmacenista = models.CharField(db_column='CodAlmacenista', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    codtipo = models.CharField(db_column='CodTipo', blank=True, null=True)  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', blank=True, null=True)  # Field name made lowercase.
    rut = models.CharField(db_column='Rut', blank=True, null=True)  # Field name made lowercase.
    fecharecepcion = models.CharField(db_column='FechaRecepcion', blank=True, null=True)  # Field name made lowercase.
    consignante = models.CharField(db_column='Consignante', blank=True, null=True)  # Field name made lowercase.
    ubicacion = models.CharField(db_column='Ubicacion', blank=True, null=True)  # Field name made lowercase.
    aduanadestino = models.CharField(db_column='AduanaDestino', blank=True, null=True)  # Field name made lowercase.
    codaduanadestino = models.CharField(db_column='CodAduanaDestino', blank=True, null=True)  # Field name made lowercase.
    ubicacion2 = models.CharField(db_column='Ubicacion2', blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', blank=True, null=True)  # Field name made lowercase.
    codpaisdestino = models.CharField(db_column='CodPaisDestino', blank=True, null=True)  # Field name made lowercase.
    paisorigen = models.CharField(db_column='PaisOrigen', blank=True, null=True)  # Field name made lowercase.
    codpaisorigen = models.CharField(db_column='CodPaisOrigen', blank=True, null=True)  # Field name made lowercase.
    viatransporte = models.CharField(db_column='ViaTransporte', blank=True, null=True)  # Field name made lowercase.
    codviatransporte = models.CharField(db_column='CodViaTransporte', blank=True, null=True)  # Field name made lowercase.
    paisorigen2 = models.CharField(db_column='PaisOrigen2', blank=True, null=True)  # Field name made lowercase.
    codpaisorigen2 = models.CharField(db_column='CodPaisOrigen2', blank=True, null=True)  # Field name made lowercase.
    garantia = models.CharField(db_column='Garantia', blank=True, null=True)  # Field name made lowercase.
    texto1 = models.CharField(db_column='Texto1', blank=True, null=True)  # Field name made lowercase.
    paisorigen3 = models.CharField(db_column='PaisOrigen3', blank=True, null=True)  # Field name made lowercase.
    codpaisorigen3 = models.CharField(db_column='CodPaisOrigen3', blank=True, null=True)  # Field name made lowercase.
    garantia2 = models.CharField(db_column='Garantia2', blank=True, null=True)  # Field name made lowercase.
    texto2 = models.CharField(db_column='Texto2', blank=True, null=True)  # Field name made lowercase.
    texto3 = models.CharField(db_column='Texto3', blank=True, null=True)  # Field name made lowercase.
    puertoembarque = models.CharField(db_column='PuertoEmbarque', blank=True, null=True)  # Field name made lowercase.
    codpuertoembarque = models.CharField(db_column='CodPuertoEmbarque', blank=True, null=True)  # Field name made lowercase.
    puertodesembarque = models.CharField(db_column='PuertoDesembarque', blank=True, null=True)  # Field name made lowercase.
    codpuertodesembarque = models.CharField(db_column='CodPuertoDesembarque', blank=True, null=True)  # Field name made lowercase.
    valorfob = models.CharField(db_column='ValorFob', blank=True, null=True)  # Field name made lowercase.
    viatransporte2 = models.CharField(db_column='ViaTransporte2', blank=True, null=True)  # Field name made lowercase.
    codviatransporte2 = models.CharField(db_column='CodViaTransporte2', blank=True, null=True)  # Field name made lowercase.
    flete = models.CharField(db_column='Flete', blank=True, null=True)  # Field name made lowercase.
    codflete = models.CharField(db_column='CodFlete', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.Declaracion'


class ExpoterraDeclaracion2(models.Model):
    numero = models.CharField(blank=True, null=True)
    conocembarque = models.CharField(db_column='ConocEmbarque', blank=True, null=True)  # Field name made lowercase.
    fechaemision = models.CharField(db_column='FechaEmision', blank=True, null=True)  # Field name made lowercase.
    emisor = models.CharField(db_column='Emisor', blank=True, null=True)  # Field name made lowercase.
    seguro = models.CharField(db_column='Seguro', blank=True, null=True)  # Field name made lowercase.
    codseguro = models.CharField(db_column='CodSeguro', blank=True, null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', blank=True, null=True)  # Field name made lowercase.
    valorcif = models.CharField(db_column='ValorCif', blank=True, null=True)  # Field name made lowercase.
    texto4 = models.CharField(db_column='Texto4', blank=True, null=True)  # Field name made lowercase.
    texto5 = models.CharField(db_column='Texto5', blank=True, null=True)  # Field name made lowercase.
    texto6 = models.CharField(db_column='Texto6', blank=True, null=True)  # Field name made lowercase.
    texto7 = models.CharField(db_column='Texto7', blank=True, null=True)  # Field name made lowercase.
    infref = models.CharField(db_column='InfRef', blank=True, null=True)  # Field name made lowercase.
    idbultos = models.CharField(db_column='IdBultos', blank=True, null=True)  # Field name made lowercase.
    cantbultos = models.CharField(db_column='CantBultos', blank=True, null=True)  # Field name made lowercase.
    codbultos = models.CharField(db_column='CodBultos', blank=True, null=True)  # Field name made lowercase.
    infref2 = models.CharField(db_column='InfRef2', blank=True, null=True)  # Field name made lowercase.
    idbultos2 = models.CharField(db_column='IdBultos2', blank=True, null=True)  # Field name made lowercase.
    cantbultos2 = models.CharField(db_column='CantBultos2', blank=True, null=True)  # Field name made lowercase.
    codbultos2 = models.CharField(db_column='CodBultos2', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    idbultos3 = models.CharField(db_column='IdBultos3', blank=True, null=True)  # Field name made lowercase.
    cantbultos3 = models.CharField(db_column='CantBultos3', blank=True, null=True)  # Field name made lowercase.
    codbultos3 = models.CharField(db_column='CodBultos3', blank=True, null=True)  # Field name made lowercase.
    variedad = models.CharField(db_column='Variedad', blank=True, null=True)  # Field name made lowercase.
    idbultos4 = models.CharField(db_column='IdBultos4', blank=True, null=True)  # Field name made lowercase.
    cantbultos4 = models.CharField(db_column='CantBultos4', blank=True, null=True)  # Field name made lowercase.
    codbultos4 = models.CharField(db_column='CodBultos4', blank=True, null=True)  # Field name made lowercase.
    marca = models.CharField(db_column='Marca', blank=True, null=True)  # Field name made lowercase.
    idbultos5 = models.CharField(db_column='IdBultos5', blank=True, null=True)  # Field name made lowercase.
    cantbultos5 = models.CharField(db_column='CantBultos5', blank=True, null=True)  # Field name made lowercase.
    codbultos5 = models.CharField(db_column='CodBultos5', blank=True, null=True)  # Field name made lowercase.
    otrosant = models.CharField(db_column='OtrosAnt', blank=True, null=True)  # Field name made lowercase.
    idbultos6 = models.CharField(db_column='IdBultos6', blank=True, null=True)  # Field name made lowercase.
    cantbultos6 = models.CharField(db_column='CantBultos6', blank=True, null=True)  # Field name made lowercase.
    codbultos6 = models.CharField(db_column='CodBultos6', blank=True, null=True)  # Field name made lowercase.
    obs = models.CharField(db_column='Obs', blank=True, null=True)  # Field name made lowercase.
    idbultos7 = models.CharField(db_column='IdBultos7', blank=True, null=True)  # Field name made lowercase.
    cantbultos7 = models.CharField(db_column='CantBultos7', blank=True, null=True)  # Field name made lowercase.
    codbultos7 = models.CharField(db_column='CodBultos7', blank=True, null=True)  # Field name made lowercase.
    obs2 = models.CharField(db_column='Obs2', blank=True, null=True)  # Field name made lowercase.
    idbultos8 = models.CharField(db_column='IdBultos8', blank=True, null=True)  # Field name made lowercase.
    cantbultos8 = models.CharField(db_column='CantBultos8', blank=True, null=True)  # Field name made lowercase.
    codbultos8 = models.CharField(db_column='CodBultos8', blank=True, null=True)  # Field name made lowercase.
    obs3 = models.CharField(db_column='Obs3', blank=True, null=True)  # Field name made lowercase.
    idbultos9 = models.CharField(db_column='IdBultos9', blank=True, null=True)  # Field name made lowercase.
    cantbultos9 = models.CharField(db_column='CantBultos9', blank=True, null=True)  # Field name made lowercase.
    codbultos9 = models.CharField(db_column='CodBultos9', blank=True, null=True)  # Field name made lowercase.
    obs4 = models.CharField(db_column='Obs4', blank=True, null=True)  # Field name made lowercase.
    idbultos10 = models.CharField(db_column='IdBultos10', blank=True, null=True)  # Field name made lowercase.
    cantbultos10 = models.CharField(db_column='CantBultos10', blank=True, null=True)  # Field name made lowercase.
    codbultos10 = models.CharField(db_column='CodBultos10', blank=True, null=True)  # Field name made lowercase.
    codnab = models.CharField(db_column='CodNab', blank=True, null=True)  # Field name made lowercase.
    esp = models.CharField(db_column='Esp', blank=True, null=True)  # Field name made lowercase.
    adval = models.CharField(db_column='AdVal', blank=True, null=True)  # Field name made lowercase.
    stasa = models.CharField(db_column='Stasa', blank=True, null=True)  # Field name made lowercase.
    idbultos11 = models.CharField(db_column='IdBultos11', blank=True, null=True)  # Field name made lowercase.
    cantbultos11 = models.CharField(db_column='CantBultos11', blank=True, null=True)  # Field name made lowercase.
    codbultos11 = models.CharField(db_column='CodBultos11', blank=True, null=True)  # Field name made lowercase.
    cantmerc = models.CharField(db_column='CantMerc', blank=True, null=True)  # Field name made lowercase.
    punit = models.CharField(db_column='Punit', blank=True, null=True)  # Field name made lowercase.
    umed = models.CharField(db_column='Umed', blank=True, null=True)  # Field name made lowercase.
    pesobruto = models.CharField(db_column='PesoBruto', blank=True, null=True)  # Field name made lowercase.
    valorcif2 = models.CharField(db_column='ValorCif2', blank=True, null=True)  # Field name made lowercase.
    totalbultos = models.CharField(db_column='TotalBultos', blank=True, null=True)  # Field name made lowercase.
    totalacumulado = models.CharField(db_column='TotalAcumulado', blank=True, null=True)  # Field name made lowercase.
    totalacumulado2 = models.CharField(db_column='TotalAcumulado2', blank=True, null=True)  # Field name made lowercase.
    totalacumulado3 = models.CharField(db_column='TotalAcumulado3', blank=True, null=True)  # Field name made lowercase.
    totalitem = models.CharField(db_column='TotalItem', blank=True, null=True)  # Field name made lowercase.
    totalhojas = models.CharField(db_column='TotalHojas', blank=True, null=True)  # Field name made lowercase.
    totalfinal = models.CharField(db_column='TotalFinal', blank=True, null=True)  # Field name made lowercase.
    totalfinal2 = models.CharField(db_column='TotalFinal2', blank=True, null=True)  # Field name made lowercase.
    totalfinal3 = models.CharField(db_column='TotalFinal3', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.Declaracion2'


class ExpoterraEmbarqueaereo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    cliente = models.SmallIntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    despachante = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    localint = models.CharField(max_length=13, blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    consolidado = models.IntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=15, blank=True, null=True)
    operacion = models.CharField(max_length=11, blank=True, null=True)
    aduana = models.CharField(max_length=3, blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    pago = models.CharField(blank=True, null=True)
    awb = models.CharField(max_length=13, blank=True, null=True)
    hawb = models.CharField(max_length=3, blank=True, null=True)
    transportista = models.SmallIntegerField(blank=True, null=True)
    valortransporte = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    valoraduana = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    fechaembarque = models.CharField(max_length=19, blank=True, null=True)
    fecharetiro = models.CharField(max_length=19, blank=True, null=True)
    pagoflete = models.CharField(max_length=1, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=15, blank=True, null=True)  # Field name made lowercase.
    valorseguro = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    tarifaventa = models.CharField(blank=True, null=True)
    tarifacompra = models.CharField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    volumencubico = models.CharField(blank=True, null=True)
    cotizacion = models.IntegerField(blank=True, null=True)
    cotitransp = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    transdestino = models.SmallIntegerField(blank=True, null=True)
    notifcliente = models.CharField(max_length=19, blank=True, null=True)
    aquien = models.CharField(max_length=3, blank=True, null=True)
    transfcliente = models.CharField(max_length=19, blank=True, null=True)
    notifagente = models.CharField(max_length=19, blank=True, null=True)
    observadoc = models.CharField(max_length=3, blank=True, null=True)
    completo = models.CharField(max_length=1, blank=True, null=True)
    observado = models.CharField(max_length=1, blank=True, null=True)
    detcompleto = models.CharField(max_length=3, blank=True, null=True)
    detobservado = models.CharField(max_length=3, blank=True, null=True)
    facturado = models.CharField(max_length=1, blank=True, null=True)
    profitage = models.CharField(blank=True, null=True)
    embarcador = models.SmallIntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    notificar = models.SmallIntegerField(db_column='Notificar', blank=True, null=True)  # Field name made lowercase.
    vaporcli = models.CharField(db_column='Vaporcli', blank=True, null=True)  # Field name made lowercase.
    vaporcli2 = models.CharField(db_column='Vaporcli2', blank=True, null=True)  # Field name made lowercase.
    terminal = models.IntegerField(blank=True, null=True)
    terminal2 = models.IntegerField(blank=True, null=True)
    tipovend = models.CharField(db_column='Tipovend', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendedor = models.IntegerField(db_column='Vendedor', blank=True, null=True)  # Field name made lowercase.
    comivend = models.DecimalField(db_column='Comivend', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    aplicaprofit = models.IntegerField(db_column='Aplicaprofit', blank=True, null=True)  # Field name made lowercase.
    aduanasalida = models.CharField(max_length=3, blank=True, null=True)
    aduanallegada = models.CharField(max_length=3, blank=True, null=True)
    documanexo = models.CharField(max_length=3, blank=True, null=True)
    matriculas = models.CharField(max_length=3, blank=True, null=True)
    registros = models.CharField(max_length=3, blank=True, null=True)
    precintos = models.CharField(max_length=3, blank=True, null=True)
    advalvta = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    advalcto = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    nroreferedi = models.CharField(blank=True, null=True)
    ordencliente = models.CharField(db_column='OrdenCliente', max_length=17, blank=True, null=True)  # Field name made lowercase.
    propia = models.IntegerField(blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    trafico = models.IntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    vapor = models.CharField(max_length=3, blank=True, null=True)
    conocimiento = models.CharField(max_length=3, blank=True, null=True)
    origenawb = models.CharField(max_length=3, blank=True, null=True)
    destinoawb = models.CharField(max_length=3, blank=True, null=True)
    salidaawb = models.CharField(max_length=19, blank=True, null=True)
    llegadaawb = models.CharField(max_length=19, blank=True, null=True)
    viaje = models.CharField(max_length=3, blank=True, null=True)
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=3, blank=True, null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=3, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=3, blank=True, null=True)  # Field name made lowercase.
    proyecto = models.IntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', blank=True, null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=3, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    despafrontera = models.IntegerField(db_column='DespaFrontera', blank=True, null=True)  # Field name made lowercase.
    sociotransfer = models.IntegerField(db_column='SocioTransfer', blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=3, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)  # Field name made lowercase.
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    fechaentrega = models.CharField(db_column='FechaEntrega', max_length=19, blank=True, null=True)  # Field name made lowercase.
    aquienentrega = models.CharField(db_column='aQuienEntrega', max_length=3, blank=True, null=True)  # Field name made lowercase.
    actividad = models.IntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', blank=True, null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', blank=True, null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', blank=True, null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', blank=True, null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', blank=True, null=True)  # Field name made lowercase.
    booking = models.CharField(db_column='Booking', max_length=3, blank=True, null=True)  # Field name made lowercase.
    diasalmacenaje = models.IntegerField(db_column='DiasAlmacenaje', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FechaIngreso', max_length=19, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=3, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=3, blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', blank=True, null=True)  # Field name made lowercase.
    etd = models.CharField(db_column='ETD', max_length=19, blank=True, null=True)  # Field name made lowercase.
    eta = models.CharField(db_column='ETA', max_length=19, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.Embarqueaereo'


class ExpoterraEntregadoc(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    entreguese = models.CharField(db_column='Entreguese', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nombreentrega = models.CharField(db_column='NombreEntrega', max_length=21, blank=True, null=True)  # Field name made lowercase.
    direccionentrega = models.CharField(db_column='DireccionEntrega', max_length=19, blank=True, null=True)  # Field name made lowercase.
    ciudadentrega = models.CharField(db_column='CiudadEntrega', max_length=3, blank=True, null=True)  # Field name made lowercase.
    telefonoentrega = models.CharField(db_column='TelefonoEntrega', max_length=3, blank=True, null=True)  # Field name made lowercase.
    original = models.CharField(db_column='Original', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lista = models.CharField(db_column='Lista', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certorigen = models.CharField(db_column='CertOrigen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    declara = models.CharField(db_column='Declara', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certflete = models.CharField(db_column='CertFlete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cerseguro = models.CharField(db_column='CerSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    copiahbl = models.CharField(db_column='CopiaHBL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    otros = models.CharField(db_column='Otros', max_length=1, blank=True, null=True)  # Field name made lowercase.
    detotros = models.CharField(db_column='DetOtros', blank=True, null=True)  # Field name made lowercase.
    detotros2 = models.CharField(db_column='DetOtros2', blank=True, null=True)  # Field name made lowercase.
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
    remarks = models.CharField(db_column='Remarks', blank=True, null=True)  # Field name made lowercase.
    remarks2 = models.CharField(db_column='Remarks2', blank=True, null=True)  # Field name made lowercase.
    facturacom = models.CharField(db_column='FacturaCom', blank=True, null=True)  # Field name made lowercase.
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', blank=True, null=True)  # Field name made lowercase.
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', blank=True, null=True)  # Field name made lowercase.
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crtnumero = models.CharField(db_column='CRTNumero', blank=True, null=True)  # Field name made lowercase.
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', blank=True, null=True)  # Field name made lowercase.
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    micdtanumero = models.CharField(db_column='MicDtaNumero', blank=True, null=True)  # Field name made lowercase.
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    papeletanumero = models.CharField(db_column='PapeletaNumero', blank=True, null=True)  # Field name made lowercase.
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True, null=True)  # Field name made lowercase.
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', blank=True, null=True)  # Field name made lowercase.
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', blank=True, null=True)  # Field name made lowercase.
    certorigennumero = models.CharField(db_column='CertOrigenNumero', blank=True, null=True)  # Field name made lowercase.
    certseguronumero = models.CharField(db_column='CertSeguroNumero', blank=True, null=True)  # Field name made lowercase.
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', blank=True, null=True)  # Field name made lowercase.
    detotros3 = models.CharField(db_column='DetOtros3', blank=True, null=True)  # Field name made lowercase.
    detotros4 = models.CharField(db_column='DetOtros4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.EntregaDoc'


class ExpoterraEnvases(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=13, blank=True, null=True)
    tipo = models.CharField(max_length=14, blank=True, null=True)
    movimiento = models.CharField(max_length=17, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    precio = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    marcas = models.CharField(max_length=3, blank=True, null=True)
    volumen = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    tara = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    envase = models.CharField(db_column='Envase', max_length=8, blank=True, null=True)  # Field name made lowercase.
    bultos = models.IntegerField(blank=True, null=True)
    peso = models.DecimalField(db_column='Peso', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    profit = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    temperatura = models.DecimalField(db_column='Temperatura', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    condespeciales = models.CharField(db_column='CondEspeciales', blank=True, null=True)  # Field name made lowercase.
    nomchofer = models.CharField(db_column='NomChofer', blank=True, null=True)  # Field name made lowercase.
    telchofer = models.CharField(db_column='TelChofer', blank=True, null=True)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    horacitacion = models.CharField(db_column='HoraCitacion', blank=True, null=True)  # Field name made lowercase.
    horallegada = models.CharField(db_column='HoraLlegada', blank=True, null=True)  # Field name made lowercase.
    depositoretiro = models.IntegerField(db_column='DepositoRetiro', blank=True, null=True)  # Field name made lowercase.
    depositodev = models.IntegerField(db_column='DepositoDev', blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.IntegerField(db_column='Cotizacion', blank=True, null=True)  # Field name made lowercase.
    direccionentrega = models.IntegerField(db_column='DireccionEntrega', blank=True, null=True)  # Field name made lowercase.
    rucchofer = models.CharField(db_column='RucChofer', blank=True, null=True)  # Field name made lowercase.
    fechallegadaplanta = models.CharField(db_column='FechaLlegadaPlanta', max_length=19, blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=12, blank=True, null=True)  # Field name made lowercase.
    precinto = models.CharField(db_column='Precinto', max_length=3, blank=True, null=True)  # Field name made lowercase.
    autogenenvase = models.CharField(db_column='AutogenEnvase', blank=True, null=True)  # Field name made lowercase.
    fechacitacion = models.CharField(db_column='FechaCitacion', max_length=19, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.Envases'


class ExpoterraFaxes(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.CharField(max_length=112, blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.Faxes'


class ExpoterraFisico(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', blank=True, null=True)  # Field name made lowercase.
    volumen = models.CharField(blank=True, null=True)
    tara = models.CharField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.
    precio = models.CharField(db_column='Precio', blank=True, null=True)  # Field name made lowercase.
    costo = models.CharField(db_column='Costo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.Fisico'


class ExpoterraGastoshijos(models.Model):
    codigo = models.CharField(blank=True, null=True)
    precio = models.CharField(blank=True, null=True)
    tipogasto = models.CharField(blank=True, null=True)
    modo = models.CharField(blank=True, null=True)
    cliente = models.CharField(blank=True, null=True)
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.CharField(db_column='Costo', blank=True, null=True)  # Field name made lowercase.
    statushijos = models.CharField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.GastosHijos'


class ExpoterraGuiasgrabadas(models.Model):
    numero = models.CharField(blank=True, null=True)
    empresa = models.CharField(blank=True, null=True)
    direccion = models.CharField(blank=True, null=True)
    pais = models.CharField(blank=True, null=True)
    localidad = models.CharField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True)
    cliente1 = models.CharField(blank=True, null=True)
    cliente2 = models.CharField(blank=True, null=True)
    cliente3 = models.CharField(blank=True, null=True)
    cliente4 = models.CharField(blank=True, null=True)
    destina = models.CharField(blank=True, null=True)
    direcdestina = models.CharField(blank=True, null=True)
    localdestina = models.CharField(blank=True, null=True)
    teledestina = models.CharField(blank=True, null=True)
    consigna = models.CharField(blank=True, null=True)
    direcconsigna = models.CharField(blank=True, null=True)
    localconsigna = models.CharField(blank=True, null=True)
    teleconsigna = models.CharField(blank=True, null=True)
    notif = models.CharField(blank=True, null=True)
    dirnotif = models.CharField(blank=True, null=True)
    otralinea2 = models.CharField(blank=True, null=True)
    telnotif = models.CharField(blank=True, null=True)
    salede = models.CharField(blank=True, null=True)
    loading = models.CharField(blank=True, null=True)
    discharge = models.CharField(blank=True, null=True)
    porte1 = models.CharField(blank=True, null=True)
    porte2 = models.CharField(blank=True, null=True)
    porte3 = models.CharField(blank=True, null=True)
    declaravalor = models.CharField(blank=True, null=True)
    documanexo1 = models.CharField(blank=True, null=True)
    documanexo2 = models.CharField(blank=True, null=True)
    documanexo3 = models.CharField(blank=True, null=True)
    documanexo4 = models.CharField(blank=True, null=True)
    aduana1 = models.CharField(blank=True, null=True)
    aduana2 = models.CharField(blank=True, null=True)
    aduana3 = models.CharField(blank=True, null=True)
    aduana4 = models.CharField(blank=True, null=True)
    aduana5 = models.CharField(blank=True, null=True)
    declara1 = models.CharField(blank=True, null=True)
    declara2 = models.CharField(blank=True, null=True)
    declara3 = models.CharField(blank=True, null=True)
    declara4 = models.CharField(blank=True, null=True)
    declara5 = models.CharField(blank=True, null=True)
    destina1 = models.CharField(blank=True, null=True)
    destina2 = models.CharField(blank=True, null=True)
    destina3 = models.CharField(blank=True, null=True)
    fleteexterno = models.CharField(blank=True, null=True)
    reembolso = models.CharField(blank=True, null=True)
    remite1 = models.CharField(blank=True, null=True)
    remite2 = models.CharField(blank=True, null=True)
    remite3 = models.CharField(blank=True, null=True)
    signature = models.CharField(blank=True, null=True)
    signature2 = models.CharField(blank=True, null=True)
    fechaemi = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Expoterra.GuiasGrabadas'


class ExpoterraGuiasgrabadas2(models.Model):
    numero = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Expoterra.GuiasGrabadas2'


class ExpoterraReservas(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    transportista = models.SmallIntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    kilos = models.CharField(db_column='Kilos', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    awb = models.CharField(max_length=12, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    moneda = models.IntegerField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=3, blank=True, null=True)  # Field name made lowercase.
    volumen = models.CharField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    aduana = models.CharField(max_length=3, blank=True, null=True)
    preaviso = models.CharField(max_length=1, blank=True, null=True)
    notirecibo = models.CharField(max_length=19, blank=True, null=True)
    porquien = models.CharField(max_length=3, blank=True, null=True)
    completo = models.CharField(max_length=1, blank=True, null=True)
    observado = models.CharField(max_length=1, blank=True, null=True)
    detcompleto = models.CharField(max_length=3, blank=True, null=True)
    detobservado = models.CharField(max_length=3, blank=True, null=True)
    observadoc = models.CharField(max_length=3, blank=True, null=True)
    profitage = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    tarifapl = models.CharField(blank=True, null=True)
    posicion = models.CharField(db_column='Posicion', max_length=15, blank=True, null=True)  # Field name made lowercase.
    envioedi = models.CharField(max_length=1, blank=True, null=True)
    aduanallegada = models.CharField(max_length=3, blank=True, null=True)
    aduanasalida = models.CharField(max_length=3, blank=True, null=True)
    matriculas = models.CharField(max_length=3, blank=True, null=True)
    precintos = models.CharField(max_length=3, blank=True, null=True)
    registros = models.CharField(max_length=3, blank=True, null=True)
    documanexo = models.CharField(max_length=3, blank=True, null=True)
    terminal = models.IntegerField(blank=True, null=True)
    terminal2 = models.IntegerField(blank=True, null=True)
    nroreferedi = models.CharField(blank=True, null=True)
    operacion = models.CharField(max_length=11, blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    trafico = models.IntegerField(blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=3, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FechaIngreso', max_length=19, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', blank=True, null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.Reservas'


class ExpoterraServireserva(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    costo = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=24, blank=True, null=True)
    tipogasto = models.CharField(max_length=11, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    secomparte = models.CharField(blank=True, null=True)
    repartir = models.CharField(blank=True, null=True)
    pinformar = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    descripcion = models.CharField(max_length=3, blank=True, null=True)
    precio = models.CharField(blank=True, null=True)
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.Servireserva'


class ExpoterraTraceop(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=102, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=8, blank=True, null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.TraceOP'


class ExpoterraConexaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    salida = models.CharField(max_length=19, blank=True, null=True)
    llegada = models.CharField(max_length=19, blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=9, blank=True, null=True)
    viaje = models.CharField(max_length=3, blank=True, null=True)
    vuelo = models.CharField(max_length=14, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    embarcador = models.SmallIntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    consignatario = models.SmallIntegerField(db_column='Consignatario', blank=True, null=True)  # Field name made lowercase.
    transportista = models.SmallIntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    horasalida = models.CharField(db_column='HoraSalida', blank=True, null=True)  # Field name made lowercase.
    horallegada = models.CharField(db_column='HoraLlegada', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.conexaerea'


class ExpoterraServiceaereo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=32, blank=True, null=True)
    tipogasto = models.CharField(max_length=13, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    notomaprofit = models.IntegerField(db_column='Notomaprofit', blank=True, null=True)  # Field name made lowercase.
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    descripcion = models.CharField(max_length=3, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=3, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    autogenenvase = models.CharField(db_column='AutogenEnvase', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Expoterra.serviceaereo'


class ImpomaritAnulados(models.Model):
    fecha = models.CharField(max_length=19, blank=True, null=True)
    detalle = models.CharField(max_length=47, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Impomarit.Anulados'


class ImpomaritAttachhijo(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=188, blank=True, null=True)
    detalle = models.CharField(max_length=22, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.AttachHijo'


class ImpomaritAttachmadre(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=82, blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.AttachMadre'


class ImpomaritCargaaerea(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    medidas = models.CharField(max_length=29, blank=True, null=True)
    tipo = models.CharField(max_length=13, blank=True, null=True)
    fechaembarque = models.CharField(max_length=19, blank=True, null=True)
    cbm = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    mercaderia = models.CharField(max_length=64, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.Cargaaerea'


class ImpomaritClavenrohouse(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    embarque = models.CharField(db_column='Embarque', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.ClaveNroHouse'


class ImpomaritClaveposicion(models.Model):
    posicion = models.CharField(max_length=10, blank=True, null=True)
    numeroorden = models.IntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.Claveposicion'


class ImpomaritConexreserva(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    vapor = models.CharField(max_length=22, blank=True, null=True)
    salida = models.CharField(max_length=19, blank=True, null=True)
    llegada = models.CharField(max_length=19, blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(max_length=9, blank=True, null=True)
    modo = models.CharField(max_length=8, blank=True, null=True)
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    horaorigen = models.CharField(db_column='HoraOrigen', blank=True, null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.Conexreserva'


class ImpomaritEmbarqueaereo(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    cliente = models.SmallIntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    despachante = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    consolidado = models.IntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=15, blank=True, null=True)
    operacion = models.CharField(max_length=23, blank=True, null=True)
    aduana = models.CharField(max_length=3, blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    pago = models.CharField(blank=True, null=True)
    awb = models.CharField(max_length=24, blank=True, null=True)
    hawb = models.CharField(max_length=23, blank=True, null=True)
    transportista = models.SmallIntegerField(blank=True, null=True)
    valortransporte = models.CharField(blank=True, null=True)
    valoraduana = models.CharField(max_length=11, blank=True, null=True)
    fechaembarque = models.CharField(max_length=19, blank=True, null=True)
    fecharetiro = models.CharField(max_length=19, blank=True, null=True)
    pagoflete = models.CharField(max_length=1, blank=True, null=True)
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    valorseguro = models.CharField(blank=True, null=True)
    tarifaventa = models.CharField(blank=True, null=True)
    tarifacompra = models.CharField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    volumencubico = models.CharField(blank=True, null=True)
    cotizacion = models.SmallIntegerField(blank=True, null=True)
    cotitransp = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    transdestino = models.SmallIntegerField(blank=True, null=True)
    notifcliente = models.CharField(max_length=19, blank=True, null=True)
    aquien = models.CharField(max_length=30, blank=True, null=True)
    transftransport = models.CharField(max_length=19, blank=True, null=True)
    transfcliente = models.CharField(max_length=19, blank=True, null=True)
    retirada = models.CharField(max_length=3, blank=True, null=True)
    notifagente = models.CharField(max_length=19, blank=True, null=True)
    observadoc = models.CharField(max_length=49, blank=True, null=True)
    completo = models.CharField(max_length=1, blank=True, null=True)
    observado = models.CharField(max_length=1, blank=True, null=True)
    detcompleto = models.CharField(max_length=8, blank=True, null=True)
    detobservado = models.CharField(max_length=31, blank=True, null=True)
    facturado = models.CharField(max_length=1, blank=True, null=True)
    profitage = models.CharField(max_length=6, blank=True, null=True)
    embarcador = models.SmallIntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    notificar = models.SmallIntegerField(db_column='Notificar', blank=True, null=True)  # Field name made lowercase.
    vaporcli = models.CharField(db_column='Vaporcli', blank=True, null=True)  # Field name made lowercase.
    vaporcli2 = models.CharField(db_column='Vaporcli2', blank=True, null=True)  # Field name made lowercase.
    vapor = models.CharField(db_column='Vapor', max_length=23, blank=True, null=True)  # Field name made lowercase.
    terminal = models.IntegerField(blank=True, null=True)
    tipovend = models.CharField(db_column='Tipovend', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendedor = models.IntegerField(db_column='Vendedor', blank=True, null=True)  # Field name made lowercase.
    comivend = models.DecimalField(db_column='Comivend', max_digits=3, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    aplicaprofit = models.IntegerField(db_column='Aplicaprofit', blank=True, null=True)  # Field name made lowercase.
    nroreferedi = models.CharField(blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    ordencliente = models.CharField(max_length=78, blank=True, null=True)
    desconsolida = models.CharField(max_length=32, blank=True, null=True)
    armador = models.CharField(blank=True, null=True)
    viaje = models.CharField(max_length=10, blank=True, null=True)
    propia = models.IntegerField(blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    trafico = models.IntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    fechaentrega = models.CharField(max_length=19, blank=True, null=True)
    aquienentrega = models.CharField(max_length=19, blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    originales = models.CharField(max_length=1, blank=True, null=True)
    fechalimitedemora = models.CharField(db_column='FechaLimiteDemora', max_length=19, blank=True, null=True)  # Field name made lowercase.
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=3, blank=True, null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=3, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=17, blank=True, null=True)  # Field name made lowercase.
    proyecto = models.IntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', blank=True, null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=26, blank=True, null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=11, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=3, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=3, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    tieneacta = models.CharField(db_column='TieneActa', max_length=1, blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=70, blank=True, null=True)  # Field name made lowercase.
    deaddocumentos = models.CharField(db_column='DeadDocumentos', max_length=19, blank=True, null=True)  # Field name made lowercase.
    deadentrega = models.CharField(db_column='DeadEntrega', max_length=19, blank=True, null=True)  # Field name made lowercase.
    hblcorp = models.IntegerField(db_column='HBLCorp', blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)  # Field name made lowercase.
    desconsolidadeposito = models.CharField(db_column='DesconsolidaDeposito', max_length=1, blank=True, null=True)  # Field name made lowercase.
    demora = models.IntegerField(db_column='Demora', blank=True, null=True)  # Field name made lowercase.
    valordemoravta = models.DecimalField(db_column='ValorDemoraVTA', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    enviointercomex = models.CharField(db_column='EnvioIntercomex', blank=True, null=True)  # Field name made lowercase.
    agecompras = models.SmallIntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.SmallIntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    actividad = models.IntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    arribosim = models.CharField(db_column='ArriboSIM', max_length=19, blank=True, null=True)  # Field name made lowercase.
    presentasim = models.CharField(db_column='PresentaSIM', max_length=19, blank=True, null=True)  # Field name made lowercase.
    cierresim = models.CharField(db_column='CierreSIM', max_length=19, blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', max_length=6, blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emisionbl = models.CharField(db_column='EmisionBL', max_length=19, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FechaIngreso', max_length=19, blank=True, null=True)  # Field name made lowercase.
    fechafinoperativa = models.CharField(db_column='FechaFinOperativa', max_length=19, blank=True, null=True)  # Field name made lowercase.
    horafinoperativa = models.CharField(db_column='HoraFinOperativa', blank=True, null=True)  # Field name made lowercase.
    fechadocsdisp = models.CharField(db_column='FechaDocsDisp', max_length=19, blank=True, null=True)  # Field name made lowercase.
    horadocsdisp = models.CharField(db_column='HoraDocsDisp', blank=True, null=True)  # Field name made lowercase.
    fechadocsret = models.CharField(db_column='FechaDocsRet', max_length=19, blank=True, null=True)  # Field name made lowercase.
    horadocsret = models.CharField(db_column='HoraDocsRet', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=15, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=27, blank=True, null=True)  # Field name made lowercase.
    tipobl = models.CharField(db_column='TipoBL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    emitebloriginal = models.CharField(db_column='EmiteBLOriginal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', blank=True, null=True)  # Field name made lowercase.
    etd = models.CharField(db_column='ETD', max_length=19, blank=True, null=True)  # Field name made lowercase.
    eta = models.CharField(db_column='ETA', max_length=19, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.Embarqueaereo'


class ImpomaritEntregadoc(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    entreguese = models.CharField(db_column='Entreguese', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nombreentrega = models.CharField(db_column='NombreEntrega', max_length=50, blank=True, null=True)  # Field name made lowercase.
    direccionentrega = models.CharField(db_column='DireccionEntrega', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ciudadentrega = models.CharField(db_column='CiudadEntrega', max_length=15, blank=True, null=True)  # Field name made lowercase.
    telefonoentrega = models.CharField(db_column='TelefonoEntrega', max_length=29, blank=True, null=True)  # Field name made lowercase.
    original = models.CharField(db_column='Original', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lista = models.CharField(db_column='Lista', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certorigen = models.CharField(db_column='CertOrigen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    declara = models.CharField(db_column='Declara', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certflete = models.CharField(db_column='CertFlete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cerseguro = models.CharField(db_column='CerSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    copiahbl = models.CharField(db_column='CopiaHBL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    otros = models.CharField(db_column='Otros', max_length=1, blank=True, null=True)  # Field name made lowercase.
    detotros = models.CharField(db_column='DetOtros', max_length=50, blank=True, null=True)  # Field name made lowercase.
    detotros2 = models.CharField(db_column='DetOtros2', max_length=32, blank=True, null=True)  # Field name made lowercase.
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
    remarks2 = models.CharField(db_column='Remarks2', max_length=54, blank=True, null=True)  # Field name made lowercase.
    facturacom = models.CharField(db_column='FacturaCom', max_length=28, blank=True, null=True)  # Field name made lowercase.
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', blank=True, null=True)  # Field name made lowercase.
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', blank=True, null=True)  # Field name made lowercase.
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crtnumero = models.CharField(db_column='CRTNumero', blank=True, null=True)  # Field name made lowercase.
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', blank=True, null=True)  # Field name made lowercase.
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    micdtanumero = models.CharField(db_column='MicDtaNumero', blank=True, null=True)  # Field name made lowercase.
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    papeletanumero = models.CharField(db_column='PapeletaNumero', blank=True, null=True)  # Field name made lowercase.
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True, null=True)  # Field name made lowercase.
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', blank=True, null=True)  # Field name made lowercase.
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', blank=True, null=True)  # Field name made lowercase.
    certorigennumero = models.CharField(db_column='CertOrigenNumero', blank=True, null=True)  # Field name made lowercase.
    certseguronumero = models.CharField(db_column='CertSeguroNumero', blank=True, null=True)  # Field name made lowercase.
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', blank=True, null=True)  # Field name made lowercase.
    detotros3 = models.CharField(db_column='DetOtros3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    detotros4 = models.CharField(db_column='DetOtros4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.EntregaDoc'


class ImpomaritEnvases(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=4, blank=True, null=True)
    tipo = models.CharField(max_length=14, blank=True, null=True)
    movimiento = models.CharField(max_length=10, blank=True, null=True)
    terminos = models.CharField(max_length=4, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    marcas = models.CharField(max_length=46, blank=True, null=True)
    precinto = models.CharField(max_length=27, blank=True, null=True)
    tara = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    envase = models.CharField(db_column='Envase', max_length=13, blank=True, null=True)  # Field name made lowercase.
    bultos = models.IntegerField(blank=True, null=True)
    peso = models.CharField(db_column='Peso', max_length=12, blank=True, null=True)  # Field name made lowercase.
    profit = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    nrocontenedor = models.CharField(max_length=23, blank=True, null=True)
    volumen = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    fechadevol = models.CharField(db_column='FechaDevol', max_length=19, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.Envases'


class ImpomaritFaxes(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.Faxes'


class ImpomaritFisico(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=40, blank=True, null=True)  # Field name made lowercase.
    marcas = models.CharField(db_column='Marcas', max_length=13, blank=True, null=True)  # Field name made lowercase.
    precinto = models.CharField(db_column='Precinto', max_length=18, blank=True, null=True)  # Field name made lowercase.
    tara = models.IntegerField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    imo = models.CharField(blank=True, null=True)
    eta = models.CharField(blank=True, null=True)
    ata = models.CharField(blank=True, null=True)
    carpetaras = models.CharField(blank=True, null=True)
    carpetaplus = models.CharField(blank=True, null=True)
    aco = models.CharField(blank=True, null=True)
    solicheque = models.CharField(blank=True, null=True)
    transfer = models.CharField(blank=True, null=True)
    orden = models.CharField(blank=True, null=True)
    devolucion = models.CharField(blank=True, null=True)
    retirocont = models.CharField(blank=True, null=True)
    devolcont = models.CharField(blank=True, null=True)
    dnafecha = models.CharField(blank=True, null=True)
    dnahora = models.CharField(blank=True, null=True)
    traslado = models.CharField(blank=True, null=True)
    bahia = models.CharField(blank=True, null=True)
    docdeposfecha = models.CharField(blank=True, null=True)
    docdeposhora = models.CharField(blank=True, null=True)
    entregafecha = models.CharField(blank=True, null=True)
    entregahora = models.CharField(blank=True, null=True)
    entrada = models.CharField(blank=True, null=True)
    vaciado = models.CharField(blank=True, null=True)
    deposito = models.IntegerField(blank=True, null=True)
    cliente = models.IntegerField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.Fisico'


class ImpomaritGastosmadre(models.Model):
    cliente = models.CharField(blank=True, null=True)
    codigo = models.CharField(blank=True, null=True)
    precio = models.CharField(blank=True, null=True)
    tipogasto = models.CharField(blank=True, null=True)
    modo = models.CharField(blank=True, null=True)
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    sucursal = models.CharField(db_column='Sucursal', blank=True, null=True)  # Field name made lowercase.
    unidad = models.CharField(db_column='Unidad', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    operacion = models.CharField(db_column='Operacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.GastosMadre'


class ImpomaritGastoshijos(models.Model):
    cliente = models.CharField(blank=True, null=True)
    codigo = models.CharField(blank=True, null=True)
    precio = models.CharField(blank=True, null=True)
    tipogasto = models.CharField(blank=True, null=True)
    modo = models.CharField(blank=True, null=True)
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.CharField(db_column='Costo', blank=True, null=True)  # Field name made lowercase.
    statushijos = models.CharField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    movimiento = models.CharField(db_column='Movimiento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.Gastoshijos'


class ImpomaritGuiasgrabadas(models.Model):
    numero = models.CharField(blank=True, null=True)
    empresa = models.CharField(blank=True, null=True)
    direccion = models.CharField(blank=True, null=True)
    pais = models.CharField(blank=True, null=True)
    localidad = models.CharField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True)
    cliente1 = models.CharField(blank=True, null=True)
    cliente2 = models.CharField(blank=True, null=True)
    cliente3 = models.CharField(blank=True, null=True)
    cliente4 = models.CharField(blank=True, null=True)
    consigna = models.CharField(blank=True, null=True)
    direcconsigna = models.CharField(blank=True, null=True)
    localconsigna = models.CharField(blank=True, null=True)
    teleconsigna = models.CharField(blank=True, null=True)
    otralinea = models.CharField(blank=True, null=True)
    notif = models.CharField(blank=True, null=True)
    dirnotif = models.CharField(blank=True, null=True)
    otralinea2 = models.CharField(blank=True, null=True)
    telnotif = models.CharField(blank=True, null=True)
    tipoflete = models.CharField(blank=True, null=True)
    position = models.CharField(blank=True, null=True)
    salede = models.CharField(blank=True, null=True)
    vapor = models.CharField(blank=True, null=True)
    viaje = models.CharField(blank=True, null=True)
    loading = models.CharField(blank=True, null=True)
    discharge = models.CharField(blank=True, null=True)
    delivery = models.CharField(blank=True, null=True)
    transterms = models.CharField(blank=True, null=True)
    simbolo = models.CharField(blank=True, null=True)
    condentrega = models.CharField(blank=True, null=True)
    tipomov = models.CharField(blank=True, null=True)
    carriage = models.CharField(blank=True, null=True)
    custom = models.CharField(blank=True, null=True)
    valseguro = models.CharField(blank=True, null=True)
    goods = models.CharField(blank=True, null=True)
    free1 = models.CharField(blank=True, null=True)
    free2 = models.CharField(blank=True, null=True)
    free3 = models.CharField(blank=True, null=True)
    signature = models.CharField(blank=True, null=True)
    signature2 = models.CharField(blank=True, null=True)
    signature3 = models.CharField(blank=True, null=True)
    nbls = models.CharField(blank=True, null=True)
    payable = models.CharField(blank=True, null=True)
    board = models.CharField(blank=True, null=True)
    clean = models.CharField(blank=True, null=True)
    fechaemi = models.CharField(blank=True, null=True)
    restotext = models.CharField(blank=True, null=True)
    portext = models.CharField(blank=True, null=True)
    vadeclared = models.CharField(blank=True, null=True)
    precarriage = models.CharField(db_column='PreCarriage', blank=True, null=True)  # Field name made lowercase.
    consigna6 = models.CharField(db_column='Consigna6', blank=True, null=True)  # Field name made lowercase.
    consigna7 = models.CharField(db_column='Consigna7', blank=True, null=True)  # Field name made lowercase.
    consigna8 = models.CharField(db_column='Consigna8', blank=True, null=True)  # Field name made lowercase.
    cliente5 = models.CharField(db_column='Cliente5', blank=True, null=True)  # Field name made lowercase.
    otranotif = models.CharField(db_column='Otranotif', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.GuiasGrabadas'


class ImpomaritGuiasgrabadas2(models.Model):
    numero = models.CharField(blank=True, null=True)
    marks = models.CharField(blank=True, null=True)
    packages = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    gross = models.CharField(blank=True, null=True)
    tare = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Impomarit.GuiasGrabadas2'


class ImpomaritNietos(models.Model):
    numero = models.CharField(blank=True, null=True)
    nieto = models.CharField(blank=True, null=True)
    conocimiento = models.CharField(blank=True, null=True)
    embarcador = models.CharField(blank=True, null=True)
    consignatario = models.CharField(blank=True, null=True)
    bultos = models.CharField(blank=True, null=True)
    cbm = models.CharField(blank=True, null=True)
    kilos = models.CharField(blank=True, null=True)
    marcas = models.CharField(blank=True, null=True)
    notas = models.CharField(blank=True, null=True)
    observaciones = models.CharField(blank=True, null=True)
    notificar = models.CharField(blank=True, null=True)
    peso = models.CharField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    producto = models.CharField(db_column='Producto', blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.Nietos'


class ImpomaritReservas(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    transportista = models.SmallIntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    kilos = models.CharField(db_column='Kilos', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    awb = models.CharField(max_length=24, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    moneda = models.IntegerField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    volumen = models.CharField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.SmallIntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    aduana = models.CharField(max_length=12, blank=True, null=True)
    preaviso = models.CharField(max_length=1, blank=True, null=True)
    notirecibo = models.CharField(max_length=19, blank=True, null=True)
    porquien = models.CharField(max_length=17, blank=True, null=True)
    transfrecibo = models.CharField(max_length=19, blank=True, null=True)
    completo = models.CharField(max_length=1, blank=True, null=True)
    observado = models.CharField(max_length=1, blank=True, null=True)
    detcompleto = models.CharField(max_length=3, blank=True, null=True)
    detobservado = models.CharField(max_length=3, blank=True, null=True)
    observadoc = models.CharField(max_length=47, blank=True, null=True)
    profitage = models.CharField(max_length=6, blank=True, null=True)
    tarifapl = models.CharField(blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=23, blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=15, blank=True, null=True)  # Field name made lowercase.
    envioedi = models.CharField(max_length=1, blank=True, null=True)
    nroreferedi = models.CharField(blank=True, null=True)
    ciep = models.CharField(max_length=6, blank=True, null=True)
    kilosmadre = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    bultosmadre = models.IntegerField(blank=True, null=True)
    deposito = models.IntegerField(blank=True, null=True)
    armador = models.SmallIntegerField(blank=True, null=True)
    operacion = models.CharField(max_length=23, blank=True, null=True)
    trafico = models.IntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    orden = models.CharField(blank=True, null=True)
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=11, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=3, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=3, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FechaIngreso', max_length=19, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', blank=True, null=True)  # Field name made lowercase.
    viajefluvial = models.CharField(db_column='ViajeFluvial', blank=True, null=True)  # Field name made lowercase.
    awbfluvial = models.CharField(db_column='AwbFluvial', blank=True, null=True)  # Field name made lowercase.
    prefijofluvial = models.CharField(db_column='PrefijoFluvial', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.Reservas'


class ImpomaritServireserva(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    costo = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=38, blank=True, null=True)
    tipogasto = models.CharField(max_length=17, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    descripcion = models.CharField(blank=True, null=True)
    precio = models.CharField(blank=True, null=True)
    prorrateo = models.CharField(db_column='Prorrateo', max_length=7, blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=3, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.Servireserva'


class ImpomaritTraceop(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=11, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=117, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=11, blank=True, null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.SmallIntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.TraceOP'


class ImpomaritConexaerea(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=23, blank=True, null=True)  # Field name made lowercase.
    salida = models.CharField(max_length=19, blank=True, null=True)
    llegada = models.CharField(max_length=19, blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(db_column='Viaje', max_length=9, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(max_length=9, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    horaorigen = models.CharField(db_column='HoraOrigen', blank=True, null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.conexaerea'


class ImpomaritServiceaereo(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=39, blank=True, null=True)
    tipogasto = models.CharField(max_length=13, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    pinformar = models.CharField(max_length=11, blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    descripcion = models.CharField(blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=61, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impomarit.serviceaereo'


class ImpterraAnulados(models.Model):
    fecha = models.CharField(max_length=19, blank=True, null=True)
    detalle = models.CharField(max_length=35, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Impterra.Anulados'


class ImpterraAttachhijo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=61, blank=True, null=True)
    detalle = models.CharField(max_length=23, blank=True, null=True)
    web = models.CharField(blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.AttachHijo'


class ImpterraAttachmadre(models.Model):
    numero = models.CharField(blank=True, null=True)
    archivo = models.CharField(blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.AttachMadre'


class ImpterraCargaaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.SmallIntegerField(blank=True, null=True)
    bruto = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    medidas = models.CharField(max_length=3, blank=True, null=True)
    tipo = models.CharField(max_length=7, blank=True, null=True)
    fechaembarque = models.CharField(max_length=19, blank=True, null=True)
    cbm = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    mercaderia = models.CharField(db_column='Mercaderia', max_length=9, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.Cargaaerea'


class ImpterraClaveposicion(models.Model):
    posicion = models.CharField(max_length=10, blank=True, null=True)
    numeroorden = models.IntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.ClavePosicion'


class ImpterraConexreserva(models.Model):
    numero = models.CharField(blank=True, null=True)
    origen = models.CharField(blank=True, null=True)
    destino = models.CharField(blank=True, null=True)
    salida = models.CharField(blank=True, null=True)
    llegada = models.CharField(blank=True, null=True)
    cia = models.CharField(blank=True, null=True)
    modo = models.CharField(blank=True, null=True)
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.Conexreserva'


class ImpterraEmbarqueaereo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    cliente = models.SmallIntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    despachante = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    localint = models.CharField(max_length=13, blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    consolidado = models.IntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=15, blank=True, null=True)
    operacion = models.CharField(max_length=11, blank=True, null=True)
    aduana = models.CharField(max_length=3, blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    pago = models.CharField(blank=True, null=True)
    awb = models.CharField(max_length=15, blank=True, null=True)
    hawb = models.CharField(max_length=1, blank=True, null=True)
    transportista = models.SmallIntegerField(blank=True, null=True)
    valortransporte = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    valoraduana = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    fechaembarque = models.CharField(max_length=19, blank=True, null=True)
    fecharetiro = models.CharField(max_length=19, blank=True, null=True)
    pagoflete = models.CharField(max_length=1, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=15, blank=True, null=True)  # Field name made lowercase.
    valorseguro = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    tarifaventa = models.CharField(blank=True, null=True)
    tarifacompra = models.CharField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    volumencubico = models.CharField(blank=True, null=True)
    cotizacion = models.IntegerField(blank=True, null=True)
    cotitransp = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    transdestino = models.SmallIntegerField(blank=True, null=True)
    notifcliente = models.CharField(max_length=19, blank=True, null=True)
    aquien = models.CharField(max_length=3, blank=True, null=True)
    transfcliente = models.CharField(max_length=19, blank=True, null=True)
    notifagente = models.CharField(max_length=19, blank=True, null=True)
    observadoc = models.CharField(max_length=3, blank=True, null=True)
    completo = models.CharField(max_length=1, blank=True, null=True)
    observado = models.CharField(max_length=1, blank=True, null=True)
    detcompleto = models.CharField(max_length=3, blank=True, null=True)
    detobservado = models.CharField(max_length=3, blank=True, null=True)
    facturado = models.CharField(max_length=1, blank=True, null=True)
    profitage = models.CharField(blank=True, null=True)
    embarcador = models.SmallIntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    notificar = models.SmallIntegerField(db_column='Notificar', blank=True, null=True)  # Field name made lowercase.
    vaporcli = models.CharField(db_column='Vaporcli', blank=True, null=True)  # Field name made lowercase.
    vaporcli2 = models.CharField(db_column='Vaporcli2', blank=True, null=True)  # Field name made lowercase.
    terminal = models.IntegerField(blank=True, null=True)
    terminal2 = models.IntegerField(blank=True, null=True)
    tipovend = models.CharField(db_column='Tipovend', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendedor = models.IntegerField(db_column='Vendedor', blank=True, null=True)  # Field name made lowercase.
    comivend = models.DecimalField(db_column='Comivend', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    aplicaprofit = models.IntegerField(db_column='Aplicaprofit', blank=True, null=True)  # Field name made lowercase.
    aduanasalida = models.CharField(max_length=3, blank=True, null=True)
    aduanallegada = models.CharField(max_length=3, blank=True, null=True)
    documanexo = models.CharField(max_length=3, blank=True, null=True)
    matriculas = models.CharField(max_length=3, blank=True, null=True)
    registros = models.CharField(max_length=3, blank=True, null=True)
    precintos = models.CharField(max_length=3, blank=True, null=True)
    advalvta = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    advalcto = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    nroreferedi = models.CharField(blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    ordencliente = models.CharField(db_column='OrdenCliente', max_length=13, blank=True, null=True)  # Field name made lowercase.
    propia = models.IntegerField(blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    trafico = models.IntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    aquienentrega = models.CharField(max_length=3, blank=True, null=True)
    fechaentrega = models.CharField(max_length=19, blank=True, null=True)
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=3, blank=True, null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=3, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=3, blank=True, null=True)  # Field name made lowercase.
    proyecto = models.IntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', blank=True, null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=5, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=3, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    despafrontera = models.IntegerField(db_column='DespaFrontera', blank=True, null=True)  # Field name made lowercase.
    sociotransfer = models.IntegerField(db_column='SocioTransfer', blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=3, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', blank=True, null=True)  # Field name made lowercase.
    enviointercomex = models.CharField(db_column='EnvioIntercomex', blank=True, null=True)  # Field name made lowercase.
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    actividad = models.IntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', blank=True, null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', blank=True, null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', blank=True, null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', blank=True, null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FechaIngreso', max_length=19, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=3, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=3, blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', blank=True, null=True)  # Field name made lowercase.
    etd = models.CharField(db_column='ETD', max_length=19, blank=True, null=True)  # Field name made lowercase.
    eta = models.CharField(db_column='ETA', max_length=19, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.Embarqueaereo'


class ImpterraEntregadoc(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    entreguese = models.CharField(db_column='Entreguese', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nombreentrega = models.CharField(db_column='NombreEntrega', max_length=25, blank=True, null=True)  # Field name made lowercase.
    direccionentrega = models.CharField(db_column='DireccionEntrega', max_length=13, blank=True, null=True)  # Field name made lowercase.
    ciudadentrega = models.CharField(db_column='CiudadEntrega', max_length=10, blank=True, null=True)  # Field name made lowercase.
    telefonoentrega = models.CharField(db_column='TelefonoEntrega', max_length=8, blank=True, null=True)  # Field name made lowercase.
    original = models.CharField(db_column='Original', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lista = models.CharField(db_column='Lista', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certorigen = models.CharField(db_column='CertOrigen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    declara = models.CharField(db_column='Declara', max_length=1, blank=True, null=True)  # Field name made lowercase.
    certflete = models.CharField(db_column='CertFlete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cerseguro = models.CharField(db_column='CerSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    copiahbl = models.CharField(db_column='CopiaHBL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    otros = models.CharField(db_column='Otros', max_length=1, blank=True, null=True)  # Field name made lowercase.
    detotros = models.CharField(db_column='DetOtros', blank=True, null=True)  # Field name made lowercase.
    detotros2 = models.CharField(db_column='DetOtros2', blank=True, null=True)  # Field name made lowercase.
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
    remarks = models.CharField(db_column='Remarks', blank=True, null=True)  # Field name made lowercase.
    remarks2 = models.CharField(db_column='Remarks2', blank=True, null=True)  # Field name made lowercase.
    facturacom = models.CharField(db_column='FacturaCom', blank=True, null=True)  # Field name made lowercase.
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', blank=True, null=True)  # Field name made lowercase.
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', blank=True, null=True)  # Field name made lowercase.
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crtnumero = models.CharField(db_column='CRTNumero', blank=True, null=True)  # Field name made lowercase.
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', blank=True, null=True)  # Field name made lowercase.
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    micdtanumero = models.CharField(db_column='MicDtaNumero', blank=True, null=True)  # Field name made lowercase.
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    papeletanumero = models.CharField(db_column='PapeletaNumero', blank=True, null=True)  # Field name made lowercase.
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True, null=True)  # Field name made lowercase.
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', blank=True, null=True)  # Field name made lowercase.
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', blank=True, null=True)  # Field name made lowercase.
    certorigennumero = models.CharField(db_column='CertOrigenNumero', blank=True, null=True)  # Field name made lowercase.
    certseguronumero = models.CharField(db_column='CertSeguroNumero', blank=True, null=True)  # Field name made lowercase.
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', blank=True, null=True)  # Field name made lowercase.
    detotros3 = models.CharField(db_column='DetOtros3', blank=True, null=True)  # Field name made lowercase.
    detotros4 = models.CharField(db_column='DetOtros4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.EntregaDoc'


class ImpterraEnvases(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=13, blank=True, null=True)
    tipo = models.CharField(max_length=3, blank=True, null=True)
    movimiento = models.CharField(max_length=9, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    marcas = models.CharField(max_length=3, blank=True, null=True)
    volumen = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    tara = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    envase = models.CharField(db_column='Envase', max_length=8, blank=True, null=True)  # Field name made lowercase.
    bultos = models.SmallIntegerField(blank=True, null=True)
    peso = models.DecimalField(db_column='Peso', max_digits=6, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    profit = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=3, blank=True, null=True)  # Field name made lowercase.
    precinto = models.CharField(db_column='Precinto', max_length=3, blank=True, null=True)  # Field name made lowercase.
    temperatura = models.CharField(db_column='Temperatura', blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', blank=True, null=True)  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', blank=True, null=True)  # Field name made lowercase.
    condespeciales = models.CharField(db_column='CondEspeciales', blank=True, null=True)  # Field name made lowercase.
    nomchofer = models.CharField(db_column='NomChofer', blank=True, null=True)  # Field name made lowercase.
    telchofer = models.CharField(db_column='TelChofer', blank=True, null=True)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    horacitacion = models.CharField(db_column='HoraCitacion', blank=True, null=True)  # Field name made lowercase.
    horallegada = models.CharField(db_column='HoraLlegada', blank=True, null=True)  # Field name made lowercase.
    depositoretiro = models.CharField(db_column='DepositoRetiro', blank=True, null=True)  # Field name made lowercase.
    depositodev = models.CharField(db_column='DepositoDev', blank=True, null=True)  # Field name made lowercase.
    direccionentrega = models.CharField(db_column='DireccionEntrega', blank=True, null=True)  # Field name made lowercase.
    rucchofer = models.CharField(db_column='RucChofer', blank=True, null=True)  # Field name made lowercase.
    fechallegadaplanta = models.CharField(db_column='FechaLlegadaPlanta', blank=True, null=True)  # Field name made lowercase.
    fechacitacion = models.CharField(db_column='FechaCitacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.Envases'


class ImpterraFaxes(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.CharField(max_length=164, blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)
    id = models.SmallIntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.Faxes'


class ImpterraFisico(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', blank=True, null=True)  # Field name made lowercase.
    volumen = models.CharField(blank=True, null=True)
    tara = models.CharField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.
    precio = models.CharField(db_column='Precio', blank=True, null=True)  # Field name made lowercase.
    costo = models.CharField(db_column='Costo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.Fisico'


class ImpterraGastoshijos(models.Model):
    codigo = models.CharField(blank=True, null=True)
    precio = models.CharField(blank=True, null=True)
    tipogasto = models.CharField(blank=True, null=True)
    modo = models.CharField(blank=True, null=True)
    cliente = models.CharField(blank=True, null=True)
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.CharField(db_column='Costo', blank=True, null=True)  # Field name made lowercase.
    statushijos = models.CharField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.GastosHijos'


class ImpterraGuiasgrabadas(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    empresa = models.CharField(blank=True, null=True)
    direccion = models.CharField(blank=True, null=True)
    pais = models.CharField(blank=True, null=True)
    localidad = models.CharField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True)
    cliente1 = models.CharField(max_length=29, blank=True, null=True)
    cliente2 = models.CharField(max_length=44, blank=True, null=True)
    cliente3 = models.CharField(max_length=3, blank=True, null=True)
    cliente4 = models.CharField(max_length=5, blank=True, null=True)
    destina = models.CharField(max_length=25, blank=True, null=True)
    direcdestina = models.CharField(max_length=13, blank=True, null=True)
    localdestina = models.CharField(max_length=20, blank=True, null=True)
    teledestina = models.CharField(max_length=27, blank=True, null=True)
    consigna = models.CharField(max_length=25, blank=True, null=True)
    direcconsigna = models.CharField(max_length=13, blank=True, null=True)
    localconsigna = models.CharField(max_length=20, blank=True, null=True)
    teleconsigna = models.CharField(max_length=27, blank=True, null=True)
    notif = models.CharField(max_length=25, blank=True, null=True)
    dirnotif = models.CharField(max_length=13, blank=True, null=True)
    otralinea2 = models.CharField(max_length=26, blank=True, null=True)
    telnotif = models.CharField(max_length=27, blank=True, null=True)
    salede = models.CharField(max_length=23, blank=True, null=True)
    loading = models.CharField(max_length=23, blank=True, null=True)
    discharge = models.CharField(max_length=18, blank=True, null=True)
    porte1 = models.CharField(max_length=9, blank=True, null=True)
    porte2 = models.CharField(blank=True, null=True)
    porte3 = models.CharField(blank=True, null=True)
    declaravalor = models.CharField(blank=True, null=True)
    documanexo1 = models.CharField(max_length=9, blank=True, null=True)
    documanexo2 = models.CharField(blank=True, null=True)
    documanexo3 = models.CharField(blank=True, null=True)
    documanexo4 = models.CharField(blank=True, null=True)
    aduana1 = models.CharField(blank=True, null=True)
    aduana2 = models.CharField(blank=True, null=True)
    aduana3 = models.CharField(blank=True, null=True)
    aduana4 = models.CharField(blank=True, null=True)
    aduana5 = models.CharField(blank=True, null=True)
    declara1 = models.CharField(max_length=25, blank=True, null=True)
    declara2 = models.CharField(blank=True, null=True)
    declara3 = models.CharField(blank=True, null=True)
    declara4 = models.CharField(blank=True, null=True)
    declara5 = models.CharField(blank=True, null=True)
    destina1 = models.CharField(blank=True, null=True)
    destina2 = models.CharField(blank=True, null=True)
    destina3 = models.CharField(blank=True, null=True)
    fleteexterno = models.CharField(blank=True, null=True)
    reembolso = models.CharField(max_length=9, blank=True, null=True)
    remite1 = models.CharField(max_length=33, blank=True, null=True)
    remite2 = models.CharField(blank=True, null=True)
    remite3 = models.CharField(blank=True, null=True)
    signature = models.CharField(blank=True, null=True)
    signature2 = models.CharField(blank=True, null=True)
    fechaemi = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Impterra.GuiasGrabadas'


class ImpterraGuiasgrabadas2(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Impterra.GuiasGrabadas2'


class ImpterraReservas(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    kilos = models.CharField(db_column='Kilos', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(blank=True, null=True)
    destino = models.CharField(blank=True, null=True)
    awb = models.CharField(blank=True, null=True)
    agente = models.CharField(blank=True, null=True)
    consignatario = models.CharField(blank=True, null=True)
    pagoflete = models.CharField(db_column='Pagoflete', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(blank=True, null=True)
    arbitraje = models.CharField(blank=True, null=True)
    tarifa = models.CharField(db_column='Tarifa', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    volumen = models.CharField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.CharField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    aduana = models.CharField(blank=True, null=True)
    preaviso = models.CharField(blank=True, null=True)
    notirecibo = models.CharField(blank=True, null=True)
    porquien = models.CharField(blank=True, null=True)
    completo = models.CharField(blank=True, null=True)
    observado = models.CharField(blank=True, null=True)
    detcompleto = models.CharField(blank=True, null=True)
    detobservado = models.CharField(blank=True, null=True)
    observadoc = models.CharField(blank=True, null=True)
    profitage = models.CharField(blank=True, null=True)
    tarifapl = models.CharField(blank=True, null=True)
    posicion = models.CharField(db_column='Posicion', blank=True, null=True)  # Field name made lowercase.
    envioedi = models.CharField(blank=True, null=True)
    aduanallegada = models.CharField(blank=True, null=True)
    aduanasalida = models.CharField(blank=True, null=True)
    matriculas = models.CharField(blank=True, null=True)
    precintos = models.CharField(blank=True, null=True)
    registros = models.CharField(blank=True, null=True)
    documanexo = models.CharField(blank=True, null=True)
    terminal = models.CharField(blank=True, null=True)
    terminal2 = models.CharField(blank=True, null=True)
    nroreferedi = models.CharField(blank=True, null=True)
    kilosmadre = models.CharField(blank=True, null=True)
    bultosmadre = models.CharField(blank=True, null=True)
    operacion = models.CharField(blank=True, null=True)
    trafico = models.CharField(blank=True, null=True)
    iniciales = models.CharField(blank=True, null=True)
    exportado = models.CharField(blank=True, null=True)
    unidadpeso = models.CharField(db_column='UnidadPeso', blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.CharField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', blank=True, null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.Reservas'


class ImpterraServireserva(models.Model):
    numero = models.CharField(blank=True, null=True)
    servicio = models.CharField(blank=True, null=True)
    moneda = models.CharField(blank=True, null=True)
    modo = models.CharField(blank=True, null=True)
    costo = models.CharField(blank=True, null=True)
    detalle = models.CharField(blank=True, null=True)
    tipogasto = models.CharField(blank=True, null=True)
    arbitraje = models.CharField(blank=True, null=True)
    notomaprofit = models.CharField(blank=True, null=True)
    repartir = models.CharField(blank=True, null=True)
    pinformar = models.CharField(blank=True, null=True)
    descripcion = models.CharField(blank=True, null=True)
    precio = models.CharField(blank=True, null=True)
    prorrateo = models.CharField(db_column='Prorrateo', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.Servireserva'


class ImpterraTraceop(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=11, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=110, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=11, blank=True, null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.TraceOP'


class ImpterraConexaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    destino = models.CharField(max_length=3, blank=True, null=True)
    salida = models.CharField(max_length=19, blank=True, null=True)
    llegada = models.CharField(max_length=19, blank=True, null=True)
    cia = models.CharField(max_length=24, blank=True, null=True)
    modo = models.CharField(max_length=9, blank=True, null=True)
    viaje = models.CharField(max_length=3, blank=True, null=True)
    vuelo = models.CharField(max_length=14, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    embarcador = models.SmallIntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    consignatario = models.SmallIntegerField(db_column='Consignatario', blank=True, null=True)  # Field name made lowercase.
    transportista = models.SmallIntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    horasalida = models.CharField(db_column='HoraSalida', blank=True, null=True)  # Field name made lowercase.
    horallegada = models.CharField(db_column='HoraLlegada', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.conexaerea'


class ImpterraServiceaereo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=36, blank=True, null=True)
    tipogasto = models.CharField(max_length=13, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    descripcion = models.CharField(max_length=3, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=3, blank=True, null=True)  # Field name made lowercase.
    empresa = models.IntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True, null=True)  # Field name made lowercase.
    socio = models.CharField(db_column='Socio', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Impterra.serviceaereo'


class SeguirAttachhijo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=206, blank=True, null=True)
    detalle = models.CharField(max_length=23, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.AttachHijo'


class SeguirAttachhijopo(models.Model):
    numero = models.CharField(blank=True, null=True)
    archivo = models.CharField(blank=True, null=True)
    detalle = models.CharField(blank=True, null=True)
    web = models.CharField(blank=True, null=True)
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.AttachHijoPO'


class SeguirBl(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', blank=True, null=True)  # Field name made lowercase.
    cliente1 = models.CharField(db_column='Cliente1', blank=True, null=True)  # Field name made lowercase.
    cliente2 = models.CharField(db_column='Cliente2', blank=True, null=True)  # Field name made lowercase.
    cliente3 = models.CharField(db_column='Cliente3', blank=True, null=True)  # Field name made lowercase.
    cliente4 = models.CharField(db_column='Cliente4', blank=True, null=True)  # Field name made lowercase.
    consigna = models.CharField(db_column='Consigna', blank=True, null=True)  # Field name made lowercase.
    direcconsigna = models.CharField(db_column='DirecConsigna', blank=True, null=True)  # Field name made lowercase.
    localconsigna = models.CharField(db_column='LocalConsigna', blank=True, null=True)  # Field name made lowercase.
    teleconsigna = models.CharField(db_column='TeleConsigna', blank=True, null=True)  # Field name made lowercase.
    otralinea = models.CharField(db_column='Otralinea', blank=True, null=True)  # Field name made lowercase.
    notif = models.CharField(db_column='Notif', blank=True, null=True)  # Field name made lowercase.
    dirnotif = models.CharField(db_column='DirNotif', blank=True, null=True)  # Field name made lowercase.
    otralinea2 = models.CharField(db_column='Otralinea2', blank=True, null=True)  # Field name made lowercase.
    telnotif = models.CharField(db_column='TelNotif', blank=True, null=True)  # Field name made lowercase.
    tipoflete = models.CharField(db_column='TipoFlete', blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(db_column='Position', blank=True, null=True)  # Field name made lowercase.
    salede = models.CharField(db_column='Salede', blank=True, null=True)  # Field name made lowercase.
    vapor = models.CharField(db_column='Vapor', blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', blank=True, null=True)  # Field name made lowercase.
    delivery = models.CharField(db_column='Delivery', blank=True, null=True)  # Field name made lowercase.
    transterms = models.CharField(db_column='TransTerms', blank=True, null=True)  # Field name made lowercase.
    simbolo = models.CharField(db_column='Simbolo', blank=True, null=True)  # Field name made lowercase.
    condentrega = models.CharField(db_column='CondEntrega', blank=True, null=True)  # Field name made lowercase.
    tipomov = models.CharField(db_column='TipoMov', blank=True, null=True)  # Field name made lowercase.
    carriage = models.CharField(db_column='Carriage', blank=True, null=True)  # Field name made lowercase.
    custom = models.CharField(db_column='Custom', blank=True, null=True)  # Field name made lowercase.
    valseguro = models.CharField(db_column='ValSeguro', blank=True, null=True)  # Field name made lowercase.
    goods = models.CharField(db_column='Goods', blank=True, null=True)  # Field name made lowercase.
    free1 = models.CharField(db_column='Free1', blank=True, null=True)  # Field name made lowercase.
    free2 = models.CharField(db_column='Free2', blank=True, null=True)  # Field name made lowercase.
    free3 = models.CharField(db_column='Free3', blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', blank=True, null=True)  # Field name made lowercase.
    signature2 = models.CharField(db_column='Signature2', blank=True, null=True)  # Field name made lowercase.
    signature3 = models.CharField(db_column='Signature3', blank=True, null=True)  # Field name made lowercase.
    nbls = models.CharField(db_column='Nbls', blank=True, null=True)  # Field name made lowercase.
    payable = models.CharField(db_column='Payable', blank=True, null=True)  # Field name made lowercase.
    board = models.CharField(db_column='Board', blank=True, null=True)  # Field name made lowercase.
    clean = models.CharField(db_column='Clean', blank=True, null=True)  # Field name made lowercase.
    fechaemi = models.CharField(db_column='FechaEmi', blank=True, null=True)  # Field name made lowercase.
    restotext = models.CharField(db_column='RestoText', blank=True, null=True)  # Field name made lowercase.
    portext = models.CharField(db_column='PorText', blank=True, null=True)  # Field name made lowercase.
    vadeclared = models.CharField(db_column='VaDeclared', blank=True, null=True)  # Field name made lowercase.
    cliente5 = models.CharField(db_column='Cliente5', blank=True, null=True)  # Field name made lowercase.
    otranotif = models.CharField(db_column='OtraNotif', blank=True, null=True)  # Field name made lowercase.
    signature4 = models.CharField(db_column='Signature4', blank=True, null=True)  # Field name made lowercase.
    signature5 = models.CharField(db_column='Signature5', blank=True, null=True)  # Field name made lowercase.
    booking = models.CharField(db_column='Booking', blank=True, null=True)  # Field name made lowercase.
    position2 = models.CharField(db_column='Position2', blank=True, null=True)  # Field name made lowercase.
    origin = models.CharField(db_column='Origin', blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', blank=True, null=True)  # Field name made lowercase.
    awb = models.CharField(db_column='AWB', blank=True, null=True)  # Field name made lowercase.
    hawb = models.CharField(db_column='HAWB', blank=True, null=True)  # Field name made lowercase.
    totalkilos = models.CharField(db_column='TotalKilos', blank=True, null=True)  # Field name made lowercase.
    totalpaquetes = models.CharField(db_column='TotalPaquetes', blank=True, null=True)  # Field name made lowercase.
    tipodocumento = models.CharField(db_column='TipoDocumento', blank=True, null=True)  # Field name made lowercase.
    consolidado = models.CharField(db_column='Consolidado', blank=True, null=True)  # Field name made lowercase.
    mensaje1 = models.CharField(db_column='Mensaje1', blank=True, null=True)  # Field name made lowercase.
    mensaje2 = models.CharField(db_column='Mensaje2', blank=True, null=True)  # Field name made lowercase.
    label6 = models.CharField(db_column='Label6', blank=True, null=True)  # Field name made lowercase.
    texto = models.CharField(db_column='Texto', blank=True, null=True)  # Field name made lowercase.
    consigna6 = models.CharField(db_column='Consigna6', blank=True, null=True)  # Field name made lowercase.
    consigna7 = models.CharField(db_column='Consigna7', blank=True, null=True)  # Field name made lowercase.
    consigna8 = models.CharField(db_column='Consigna8', blank=True, null=True)  # Field name made lowercase.
    precarriage = models.CharField(db_column='PreCarriage', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.BL'


class SeguirBl2(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    marks = models.CharField(db_column='Marks', blank=True, null=True)  # Field name made lowercase.
    packages = models.CharField(db_column='Packages', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    gross = models.CharField(db_column='Gross', blank=True, null=True)  # Field name made lowercase.
    tare = models.CharField(db_column='Tare', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.BL2'


class SeguirBl3(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    servicio = models.CharField(db_column='Servicio', blank=True, null=True)  # Field name made lowercase.
    prepaid = models.CharField(db_column='Prepaid', blank=True, null=True)  # Field name made lowercase.
    collect = models.CharField(db_column='Collect', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.BL3'


class SeguirBookenv(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    marks = models.CharField(max_length=21, blank=True, null=True)
    packages = models.CharField(max_length=3, blank=True, null=True)
    description = models.CharField(max_length=34, blank=True, null=True)
    gross = models.CharField(max_length=5, blank=True, null=True)
    tare = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Seguir.Bookenv'


class SeguirBooking(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    empresa = models.CharField(max_length=14, blank=True, null=True)
    direccion = models.CharField(max_length=20, blank=True, null=True)
    pais = models.CharField(blank=True, null=True)
    localidad = models.CharField(max_length=10, blank=True, null=True)
    telefono = models.CharField(max_length=41, blank=True, null=True)
    comboembarca = models.SmallIntegerField(blank=True, null=True)
    cliente2 = models.CharField(max_length=45, blank=True, null=True)
    cliente3 = models.CharField(max_length=28, blank=True, null=True)
    cliente4 = models.CharField(max_length=45, blank=True, null=True)
    comboconsig = models.SmallIntegerField(blank=True, null=True)
    direcconsigna = models.CharField(max_length=43, blank=True, null=True)
    localconsigna = models.CharField(max_length=20, blank=True, null=True)
    teleconsigna = models.CharField(max_length=44, blank=True, null=True)
    otralinea = models.CharField(blank=True, null=True)
    nrobooking = models.SmallIntegerField(blank=True, null=True)
    dia = models.CharField(max_length=19, blank=True, null=True)
    salede = models.CharField(max_length=15, blank=True, null=True)
    loading = models.CharField(max_length=15, blank=True, null=True)
    discharge = models.CharField(max_length=10, blank=True, null=True)
    delivery = models.CharField(max_length=10, blank=True, null=True)
    vapor = models.CharField(max_length=20, blank=True, null=True)
    etapod = models.CharField(max_length=19, blank=True, null=True)
    etapol = models.CharField(max_length=19, blank=True, null=True)
    viaje = models.CharField(max_length=5, blank=True, null=True)
    payable = models.CharField(max_length=15, blank=True, null=True)
    combotransport = models.SmallIntegerField(blank=True, null=True)
    comboproduc = models.SmallIntegerField(blank=True, null=True)
    bultos = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    pesobruto = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    net = models.CharField(blank=True, null=True)
    sold = models.CharField(max_length=21, blank=True, null=True)
    profit = models.CharField(max_length=32, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    giro = models.CharField(blank=True, null=True)
    despachante = models.CharField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)
    terminal = models.CharField(max_length=10, blank=True, null=True)
    direccterminal = models.CharField(blank=True, null=True)
    telterminal = models.CharField(blank=True, null=True)
    contactoterminal = models.CharField(db_column='ContactoTerminal', blank=True, null=True)  # Field name made lowercase.
    bandera = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Seguir.Booking'


class SeguirBooking2(models.Model):
    numero = models.CharField(blank=True, null=True)
    empresa = models.CharField(blank=True, null=True)
    direccion = models.CharField(blank=True, null=True)
    pais = models.CharField(blank=True, null=True)
    localidad = models.CharField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True)
    comboembarca = models.CharField(blank=True, null=True)
    cliente2 = models.CharField(blank=True, null=True)
    cliente3 = models.CharField(blank=True, null=True)
    cliente4 = models.CharField(blank=True, null=True)
    comboconsig = models.CharField(blank=True, null=True)
    direcconsigna = models.CharField(blank=True, null=True)
    localconsigna = models.CharField(blank=True, null=True)
    teleconsigna = models.CharField(blank=True, null=True)
    otralinea = models.CharField(blank=True, null=True)
    nrobooking = models.CharField(blank=True, null=True)
    dia = models.CharField(blank=True, null=True)
    salede = models.CharField(blank=True, null=True)
    loading = models.CharField(blank=True, null=True)
    discharge = models.CharField(blank=True, null=True)
    delivery = models.CharField(blank=True, null=True)
    vapor = models.CharField(blank=True, null=True)
    etapod = models.CharField(blank=True, null=True)
    etapol = models.CharField(blank=True, null=True)
    viaje = models.CharField(blank=True, null=True)
    payable = models.CharField(blank=True, null=True)
    tipomov = models.CharField(blank=True, null=True)
    combotransport = models.CharField(blank=True, null=True)
    comboproduc = models.CharField(blank=True, null=True)
    bultos = models.CharField(blank=True, null=True)
    pesobruto = models.CharField(blank=True, null=True)
    combounidad = models.CharField(blank=True, null=True)
    combotipo = models.CharField(blank=True, null=True)
    cantidad = models.CharField(blank=True, null=True)
    net = models.CharField(blank=True, null=True)
    sold = models.CharField(blank=True, null=True)
    profit = models.CharField(blank=True, null=True)
    remarks = models.CharField(blank=True, null=True)
    vaporcli2 = models.CharField(blank=True, null=True)
    vaporcli = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Seguir.Booking2'


class SeguirCrt(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', blank=True, null=True)  # Field name made lowercase.
    cliente1 = models.CharField(db_column='Cliente1', blank=True, null=True)  # Field name made lowercase.
    cliente2 = models.CharField(db_column='Cliente2', blank=True, null=True)  # Field name made lowercase.
    cliente3 = models.CharField(db_column='Cliente3', blank=True, null=True)  # Field name made lowercase.
    cliente4 = models.CharField(db_column='Cliente4', blank=True, null=True)  # Field name made lowercase.
    destina = models.CharField(db_column='Destina', blank=True, null=True)  # Field name made lowercase.
    direcdestina = models.CharField(db_column='DirecDestina', blank=True, null=True)  # Field name made lowercase.
    localdestina = models.CharField(db_column='LocalDestina', blank=True, null=True)  # Field name made lowercase.
    teledestina = models.CharField(db_column='TeleDestina', blank=True, null=True)  # Field name made lowercase.
    consigna = models.CharField(db_column='Consigna', blank=True, null=True)  # Field name made lowercase.
    direcconsigna = models.CharField(db_column='DirecConsigna', blank=True, null=True)  # Field name made lowercase.
    localconsigna = models.CharField(db_column='LocalConsigna', blank=True, null=True)  # Field name made lowercase.
    teleconsigna = models.CharField(db_column='TeleConsigna', blank=True, null=True)  # Field name made lowercase.
    notif = models.CharField(db_column='Notif', blank=True, null=True)  # Field name made lowercase.
    dirnotif = models.CharField(db_column='DirNotif', blank=True, null=True)  # Field name made lowercase.
    otralinea2 = models.CharField(db_column='Otralinea2', blank=True, null=True)  # Field name made lowercase.
    telnotif = models.CharField(db_column='TelNotif', blank=True, null=True)  # Field name made lowercase.
    salede = models.CharField(db_column='Salede', blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', blank=True, null=True)  # Field name made lowercase.
    porte1 = models.CharField(db_column='Porte1', blank=True, null=True)  # Field name made lowercase.
    porte2 = models.CharField(db_column='Porte2', blank=True, null=True)  # Field name made lowercase.
    porte3 = models.CharField(db_column='Porte3', blank=True, null=True)  # Field name made lowercase.
    declaravalor = models.CharField(db_column='DeclaraValor', blank=True, null=True)  # Field name made lowercase.
    documanexo1 = models.CharField(db_column='DocumAnexo1', blank=True, null=True)  # Field name made lowercase.
    documanexo2 = models.CharField(db_column='DocumAnexo2', blank=True, null=True)  # Field name made lowercase.
    documanexo3 = models.CharField(db_column='DocumAnexo3', blank=True, null=True)  # Field name made lowercase.
    documanexo4 = models.CharField(db_column='DocumAnexo4', blank=True, null=True)  # Field name made lowercase.
    aduana1 = models.CharField(db_column='Aduana1', blank=True, null=True)  # Field name made lowercase.
    aduana2 = models.CharField(db_column='Aduana2', blank=True, null=True)  # Field name made lowercase.
    aduana3 = models.CharField(db_column='Aduana3', blank=True, null=True)  # Field name made lowercase.
    aduana4 = models.CharField(db_column='Aduana4', blank=True, null=True)  # Field name made lowercase.
    aduana5 = models.CharField(db_column='Aduana5', blank=True, null=True)  # Field name made lowercase.
    declara1 = models.CharField(db_column='Declara1', blank=True, null=True)  # Field name made lowercase.
    declara2 = models.CharField(db_column='Declara2', blank=True, null=True)  # Field name made lowercase.
    declara3 = models.CharField(db_column='Declara3', blank=True, null=True)  # Field name made lowercase.
    declara4 = models.CharField(db_column='Declara4', blank=True, null=True)  # Field name made lowercase.
    declara5 = models.CharField(db_column='Declara5', blank=True, null=True)  # Field name made lowercase.
    destina1 = models.CharField(db_column='Destina1', blank=True, null=True)  # Field name made lowercase.
    destina2 = models.CharField(db_column='Destina2', blank=True, null=True)  # Field name made lowercase.
    destina3 = models.CharField(db_column='Destina3', blank=True, null=True)  # Field name made lowercase.
    fleteexterno = models.CharField(db_column='FleteExterno', blank=True, null=True)  # Field name made lowercase.
    reembolso = models.CharField(db_column='Reembolso', blank=True, null=True)  # Field name made lowercase.
    remite1 = models.CharField(db_column='Remite1', blank=True, null=True)  # Field name made lowercase.
    remite2 = models.CharField(db_column='Remite2', blank=True, null=True)  # Field name made lowercase.
    remite3 = models.CharField(db_column='Remite3', blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', blank=True, null=True)  # Field name made lowercase.
    signature2 = models.CharField(db_column='Signature2', blank=True, null=True)  # Field name made lowercase.
    fechaemi = models.CharField(db_column='FechaEmi', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.CRT'


class SeguirCrt2(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.CRT2'


class SeguirCabezalocc(models.Model):
    numero = models.CharField(blank=True, null=True)
    orden = models.CharField(blank=True, null=True)
    fecha = models.CharField(blank=True, null=True)
    cliente = models.CharField(blank=True, null=True)
    proveedor = models.CharField(blank=True, null=True)
    vaporcli2 = models.CharField(blank=True, null=True)
    origen = models.CharField(blank=True, null=True)
    destino = models.CharField(blank=True, null=True)
    despachante = models.CharField(blank=True, null=True)
    terminos = models.CharField(blank=True, null=True)
    iniciales = models.CharField(blank=True, null=True)
    notas = models.CharField(blank=True, null=True)
    valor = models.CharField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    estimadorecepcion = models.CharField(blank=True, null=True)
    recepcion = models.CharField(blank=True, null=True)
    recepcionado = models.CharField(blank=True, null=True)
    lugar = models.CharField(blank=True, null=True)
    embarcado = models.CharField(blank=True, null=True)
    periodo = models.CharField(blank=True, null=True)
    agevtas = models.CharField(blank=True, null=True)
    agecomp = models.CharField(blank=True, null=True)
    centro = models.CharField(blank=True, null=True)
    refproveedor = models.CharField(blank=True, null=True)
    moneda = models.CharField(blank=True, null=True)
    comienzo = models.CharField(blank=True, null=True)
    formapago = models.CharField(blank=True, null=True)
    expedir = models.CharField(db_column='Expedir', blank=True, null=True)  # Field name made lowercase.
    proyecto = models.CharField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    consignatario = models.CharField(db_column='Consignatario', blank=True, null=True)  # Field name made lowercase.
    cartaaprobacion = models.CharField(db_column='CartaAprobacion', blank=True, null=True)  # Field name made lowercase.
    ultimocomienzoembarque = models.CharField(db_column='UltimoComienzoEmbarque', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.Cabezalocc'


class SeguirCargaaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    medidas = models.CharField(max_length=29, blank=True, null=True)
    tipo = models.CharField(max_length=13, blank=True, null=True)
    cbm = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    mercaderia = models.CharField(db_column='Mercaderia', max_length=79, blank=True, null=True)  # Field name made lowercase.
    marcas = models.CharField(db_column='Marcas', blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', blank=True, null=True)  # Field name made lowercase.
    materialreceipt = models.CharField(db_column='MaterialReceipt', max_length=21, blank=True, null=True)  # Field name made lowercase.
    sobredimensionada = models.CharField(db_column='Sobredimensionada', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.Cargaaerea'


class SeguirCargaaereaaduana(models.Model):
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    producto = models.CharField(db_column='Producto', blank=True, null=True)  # Field name made lowercase.
    bultos = models.CharField(db_column='Bultos', blank=True, null=True)  # Field name made lowercase.
    bruto = models.CharField(db_column='Bruto', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', blank=True, null=True)  # Field name made lowercase.
    fechamanifiesto = models.CharField(db_column='FechaManifiesto', blank=True, null=True)  # Field name made lowercase.
    enviado = models.CharField(db_column='Enviado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.CargaaereaAduana'


class SeguirClaveguia(models.Model):
    awb = models.CharField(db_column='AWB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.ClaveGuia'


class SeguirClavehawb(models.Model):
    hawb = models.CharField(db_column='HAWB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.ClaveHawb'


class SeguirClaveposicion(models.Model):
    posicion = models.CharField(db_column='Posicion', blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.ClavePosicion'


class SeguirConexreserva(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    vapor = models.CharField(db_column='Vapor', blank=True, null=True)  # Field name made lowercase.
    salida = models.CharField(db_column='Salida', blank=True, null=True)  # Field name made lowercase.
    llegada = models.CharField(db_column='Llegada', blank=True, null=True)  # Field name made lowercase.
    cia = models.CharField(db_column='Cia', blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.ConexReserva'


class SeguirCronologia(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    cantrecibida = models.CharField(db_column='CantRecibida', blank=True, null=True)  # Field name made lowercase.
    cantembarcado = models.CharField(db_column='CantEmbarcado', blank=True, null=True)  # Field name made lowercase.
    cantroto = models.CharField(db_column='CantRoto', blank=True, null=True)  # Field name made lowercase.
    cantperdido = models.CharField(db_column='CantPerdido', blank=True, null=True)  # Field name made lowercase.
    inspeccionadopor = models.CharField(db_column='InspeccionadoPor', blank=True, null=True)  # Field name made lowercase.
    recibidopor = models.CharField(db_column='RecibidoPor', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    trucknbr = models.CharField(db_column='TruckNbr', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.Cronologia'


class SeguirDetalleocc(models.Model):
    numero = models.CharField(blank=True, null=True)
    codigo = models.CharField(blank=True, null=True)
    descripcion = models.CharField(blank=True, null=True)
    cantidad = models.CharField(blank=True, null=True)
    costounit = models.CharField(blank=True, null=True)
    pesounit = models.CharField(blank=True, null=True)
    contrato = models.CharField(blank=True, null=True)
    estilo = models.CharField(blank=True, null=True)
    seccion = models.CharField(blank=True, null=True)
    unidad = models.CharField(blank=True, null=True)
    talla = models.CharField(blank=True, null=True)
    color = models.CharField(blank=True, null=True)
    sku = models.CharField(blank=True, null=True)
    descripcion2 = models.CharField(db_column='Descripcion2', blank=True, null=True)  # Field name made lowercase.
    cantidadbkd = models.CharField(db_column='CantidadBKD', blank=True, null=True)  # Field name made lowercase.
    volumen = models.CharField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    bultos = models.CharField(db_column='Bultos', blank=True, null=True)  # Field name made lowercase.
    cantidadpre = models.CharField(db_column='CantidadPRE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.Detalleocc'


class SeguirEntregadoc(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    entreguese = models.CharField(db_column='Entreguese', blank=True, null=True)  # Field name made lowercase.
    nombreentrega = models.CharField(db_column='NombreEntrega', blank=True, null=True)  # Field name made lowercase.
    direccionentrega = models.CharField(db_column='DireccionEntrega', blank=True, null=True)  # Field name made lowercase.
    ciudadentrega = models.CharField(db_column='CiudadEntrega', blank=True, null=True)  # Field name made lowercase.
    telefonoentrega = models.CharField(db_column='TelefonoEntrega', blank=True, null=True)  # Field name made lowercase.
    original = models.CharField(db_column='Original', blank=True, null=True)  # Field name made lowercase.
    lista = models.CharField(db_column='Lista', blank=True, null=True)  # Field name made lowercase.
    certorigen = models.CharField(db_column='CertOrigen', blank=True, null=True)  # Field name made lowercase.
    declara = models.CharField(db_column='Declara', blank=True, null=True)  # Field name made lowercase.
    certflete = models.CharField(db_column='CertFlete', blank=True, null=True)  # Field name made lowercase.
    cerseguro = models.CharField(db_column='CerSeguro', blank=True, null=True)  # Field name made lowercase.
    copiahbl = models.CharField(db_column='CopiaHBL', blank=True, null=True)  # Field name made lowercase.
    otros = models.CharField(db_column='Otros', blank=True, null=True)  # Field name made lowercase.
    detotros = models.CharField(db_column='DetOtros', blank=True, null=True)  # Field name made lowercase.
    detotros2 = models.CharField(db_column='DetOtros2', blank=True, null=True)  # Field name made lowercase.
    ordendep = models.CharField(db_column='OrdenDep', blank=True, null=True)  # Field name made lowercase.
    certgastos = models.CharField(db_column='CertGastos', blank=True, null=True)  # Field name made lowercase.
    libre = models.CharField(db_column='Libre', blank=True, null=True)  # Field name made lowercase.
    eur1 = models.CharField(db_column='Eur1', blank=True, null=True)  # Field name made lowercase.
    factura = models.CharField(db_column='Factura', blank=True, null=True)  # Field name made lowercase.
    nuestra = models.CharField(db_column='Nuestra', blank=True, null=True)  # Field name made lowercase.
    certcalidad = models.CharField(db_column='CertCalidad', blank=True, null=True)  # Field name made lowercase.
    cumplido = models.CharField(db_column='Cumplido', blank=True, null=True)  # Field name made lowercase.
    transfer = models.CharField(db_column='Transfer', blank=True, null=True)  # Field name made lowercase.
    certpeligroso = models.CharField(db_column='CertPeligroso', blank=True, null=True)  # Field name made lowercase.
    imprimecom = models.CharField(db_column='ImprimeCom', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', blank=True, null=True)  # Field name made lowercase.
    remarks2 = models.CharField(db_column='Remarks2', blank=True, null=True)  # Field name made lowercase.
    facturacom = models.CharField(db_column='FacturaCom', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.EntregaDoc'


class SeguirEntregaorden(models.Model):
    numero = models.CharField(blank=True, null=True)
    orden = models.CharField(blank=True, null=True)
    codigo = models.CharField(blank=True, null=True)
    descripcion = models.CharField(blank=True, null=True)
    cantidad = models.CharField(blank=True, null=True)
    entrega = models.CharField(blank=True, null=True)
    entregareal = models.CharField(blank=True, null=True)
    unidad = models.CharField(blank=True, null=True)
    arribo = models.CharField(blank=True, null=True)
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    materialreceipt = models.CharField(db_column='MaterialReceipt', blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.EntregaOrden'


class SeguirEntregasocc(models.Model):
    numero = models.CharField(blank=True, null=True)
    codigo = models.CharField(blank=True, null=True)
    cantidad = models.CharField(blank=True, null=True)
    entrega = models.CharField(blank=True, null=True)
    arribo = models.CharField(blank=True, null=True)
    embarcar = models.CharField(db_column='Embarcar', blank=True, null=True)  # Field name made lowercase.
    materialreceipt = models.CharField(db_column='MaterialReceipt', blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', blank=True, null=True)  # Field name made lowercase.
    etd = models.CharField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    boxempacado = models.CharField(db_column='BoxEmpacado', blank=True, null=True)  # Field name made lowercase.
    boxmedidas = models.CharField(db_column='BoxMedidas', blank=True, null=True)  # Field name made lowercase.
    boxpeso = models.CharField(db_column='BoxPeso', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.Entregasocc'


class SeguirEnvases(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=13, blank=True, null=True)
    tipo = models.CharField(max_length=14, blank=True, null=True)
    movimiento = models.CharField(max_length=17, blank=True, null=True)
    terminos = models.CharField(max_length=4, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    marcas = models.CharField(max_length=46, blank=True, null=True)
    precinto = models.CharField(max_length=27, blank=True, null=True)
    tara = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    envase = models.CharField(db_column='Envase', max_length=13, blank=True, null=True)  # Field name made lowercase.
    bultos = models.IntegerField(blank=True, null=True)
    peso = models.DecimalField(db_column='Peso', max_digits=9, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    profit = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    nrocontenedor = models.CharField(max_length=13, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    volumen = models.DecimalField(db_column='Volumen', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    temperatura = models.DecimalField(db_column='Temperatura', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', max_length=1, blank=True, null=True)  # Field name made lowercase.
    condespeciales = models.CharField(db_column='CondEspeciales', blank=True, null=True)  # Field name made lowercase.
    nomchofer = models.CharField(db_column='NomChofer', blank=True, null=True)  # Field name made lowercase.
    telchofer = models.CharField(db_column='TelChofer', blank=True, null=True)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', max_length=1, blank=True, null=True)  # Field name made lowercase.
    horacitacion = models.CharField(db_column='HoraCitacion', blank=True, null=True)  # Field name made lowercase.
    horallegada = models.CharField(db_column='HoraLlegada', blank=True, null=True)  # Field name made lowercase.
    depositoretiro = models.CharField(db_column='DepositoRetiro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    depositodev = models.CharField(db_column='DepositoDev', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.CharField(db_column='Cotizacion', blank=True, null=True)  # Field name made lowercase.
    rucchofer = models.CharField(db_column='RucChofer', blank=True, null=True)  # Field name made lowercase.
    fechallegadaplanta = models.CharField(db_column='FechaLlegadaPlanta', max_length=19, blank=True, null=True)  # Field name made lowercase.
    direccionentrega = models.IntegerField(db_column='DireccionEntrega', blank=True, null=True)  # Field name made lowercase.
    fechacitacion = models.CharField(db_column='FechaCitacion', max_length=19, blank=True, null=True)  # Field name made lowercase.
    ventilacion = models.CharField(db_column='Ventilacion', blank=True, null=True)  # Field name made lowercase.
    genset = models.CharField(db_column='GenSet', max_length=1, blank=True, null=True)  # Field name made lowercase.
    atmosferacontrolada = models.CharField(db_column='AtmosferaControlada', max_length=1, blank=True, null=True)  # Field name made lowercase.
    consolidacion = models.IntegerField(db_column='Consolidacion', blank=True, null=True)  # Field name made lowercase.
    tipoventilacion = models.CharField(db_column='TipoVentilacion', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pesovgm = models.CharField(db_column='PesoVGM', blank=True, null=True)  # Field name made lowercase.
    humedad = models.CharField(db_column='Humedad', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.Envases'


class SeguirFaxes(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.Faxes'


class SeguirFaxesoc(models.Model):
    numero = models.CharField(blank=True, null=True)
    fecha = models.CharField(blank=True, null=True)
    notas = models.CharField(blank=True, null=True)
    asunto = models.CharField(blank=True, null=True)
    tipo = models.CharField(blank=True, null=True)
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.FaxesOC'


class SeguirFisico(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', blank=True, null=True)  # Field name made lowercase.
    marcas = models.CharField(db_column='Marcas', blank=True, null=True)  # Field name made lowercase.
    precinto = models.CharField(db_column='Precinto', blank=True, null=True)  # Field name made lowercase.
    tara = models.CharField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.
    precio = models.CharField(db_column='Precio', blank=True, null=True)  # Field name made lowercase.
    costo = models.CharField(db_column='Costo', blank=True, null=True)  # Field name made lowercase.
    peso = models.CharField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    deposito = models.CharField(db_column='Deposito', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.Fisico'


class SeguirGastoshijos(models.Model):
    cliente = models.CharField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    precio = models.CharField(db_column='Precio', blank=True, null=True)  # Field name made lowercase.
    costo = models.CharField(db_column='Costo', blank=True, null=True)  # Field name made lowercase.
    tipogasto = models.CharField(db_column='TipoGasto', blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.GastosHijos'


class SeguirGuiasgrabadas(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', blank=True, null=True)  # Field name made lowercase.
    cliente1 = models.CharField(db_column='Cliente1', blank=True, null=True)  # Field name made lowercase.
    cliente2 = models.CharField(db_column='Cliente2', blank=True, null=True)  # Field name made lowercase.
    cliente3 = models.CharField(db_column='Cliente3', blank=True, null=True)  # Field name made lowercase.
    cliente4 = models.CharField(db_column='Cliente4', blank=True, null=True)  # Field name made lowercase.
    consigna = models.CharField(db_column='Consigna', blank=True, null=True)  # Field name made lowercase.
    direcconsigna = models.CharField(db_column='DirecConsigna', blank=True, null=True)  # Field name made lowercase.
    localconsigna = models.CharField(db_column='LocalConsigna', blank=True, null=True)  # Field name made lowercase.
    teleconsigna = models.CharField(db_column='TeleConsigna', blank=True, null=True)  # Field name made lowercase.
    otralinea = models.CharField(db_column='Otralinea', blank=True, null=True)  # Field name made lowercase.
    empresa2 = models.CharField(db_column='Empresa2', blank=True, null=True)  # Field name made lowercase.
    otracarrier = models.CharField(db_column='OtraCarrier', blank=True, null=True)  # Field name made lowercase.
    localidad2 = models.CharField(db_column='Localidad2', blank=True, null=True)  # Field name made lowercase.
    otrosdeagente = models.CharField(db_column='OtrosdeAgente', blank=True, null=True)  # Field name made lowercase.
    iata = models.CharField(db_column='Iata', blank=True, null=True)  # Field name made lowercase.
    salede = models.CharField(db_column='Salede', blank=True, null=True)  # Field name made lowercase.
    cadenaaerea = models.CharField(db_column='CadenaAerea', blank=True, null=True)  # Field name made lowercase.
    tipoflete = models.CharField(db_column='TipoFlete', blank=True, null=True)  # Field name made lowercase.
    numerolc = models.CharField(db_column='Numerolc', blank=True, null=True)  # Field name made lowercase.
    notif = models.CharField(db_column='Notif', blank=True, null=True)  # Field name made lowercase.
    dirnotif = models.CharField(db_column='DirNotif', blank=True, null=True)  # Field name made lowercase.
    otralinea2 = models.CharField(db_column='Otralinea2', blank=True, null=True)  # Field name made lowercase.
    telnotif = models.CharField(db_column='TelNotif', blank=True, null=True)  # Field name made lowercase.
    otralinea3 = models.CharField(db_column='Otralinea3', blank=True, null=True)  # Field name made lowercase.
    otralinea4 = models.CharField(db_column='Otralinea4', blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    idtransport = models.CharField(db_column='Idtransport', blank=True, null=True)  # Field name made lowercase.
    to1 = models.CharField(db_column='To1', blank=True, null=True)  # Field name made lowercase.
    by1 = models.CharField(db_column='By1', blank=True, null=True)  # Field name made lowercase.
    to2 = models.CharField(db_column='To2', blank=True, null=True)  # Field name made lowercase.
    by2 = models.CharField(db_column='By2', blank=True, null=True)  # Field name made lowercase.
    simbolo = models.CharField(db_column='Simbolo', blank=True, null=True)  # Field name made lowercase.
    carriage = models.CharField(db_column='Carriage', blank=True, null=True)  # Field name made lowercase.
    custom = models.CharField(db_column='Custom', blank=True, null=True)  # Field name made lowercase.
    nombredestino = models.CharField(db_column='NombreDestino', blank=True, null=True)  # Field name made lowercase.
    vuelo1 = models.CharField(db_column='Vuelo1', blank=True, null=True)  # Field name made lowercase.
    vuelo2 = models.CharField(db_column='Vuelo2', blank=True, null=True)  # Field name made lowercase.
    vuelo3 = models.CharField(db_column='Vuelo3', blank=True, null=True)  # Field name made lowercase.
    vuelo4 = models.CharField(db_column='Vuelo4', blank=True, null=True)  # Field name made lowercase.
    valseguro = models.CharField(db_column='ValSeguro', blank=True, null=True)  # Field name made lowercase.
    cliente5 = models.CharField(db_column='Cliente5', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.GuiasGrabadas'


class SeguirGuiasgrabadas2(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    marcas = models.CharField(db_column='Marcas', blank=True, null=True)  # Field name made lowercase.
    otraline = models.CharField(db_column='Otraline', blank=True, null=True)  # Field name made lowercase.
    attached = models.CharField(db_column='Attached', blank=True, null=True)  # Field name made lowercase.
    nature1 = models.CharField(db_column='Nature1', blank=True, null=True)  # Field name made lowercase.
    nature2 = models.CharField(db_column='Nature2', blank=True, null=True)  # Field name made lowercase.
    nature3 = models.CharField(db_column='Nature3', blank=True, null=True)  # Field name made lowercase.
    nature4 = models.CharField(db_column='Nature4', blank=True, null=True)  # Field name made lowercase.
    nature5 = models.CharField(db_column='Nature5', blank=True, null=True)  # Field name made lowercase.
    nature6 = models.CharField(db_column='Nature6', blank=True, null=True)  # Field name made lowercase.
    nature7 = models.CharField(db_column='Nature7', blank=True, null=True)  # Field name made lowercase.
    nature8 = models.CharField(db_column='Nature8', blank=True, null=True)  # Field name made lowercase.
    nature9 = models.CharField(db_column='Nature9', blank=True, null=True)  # Field name made lowercase.
    nature10 = models.CharField(db_column='Nature10', blank=True, null=True)  # Field name made lowercase.
    nature11 = models.CharField(db_column='Nature11', blank=True, null=True)  # Field name made lowercase.
    nature12 = models.CharField(db_column='Nature12', blank=True, null=True)  # Field name made lowercase.
    free1 = models.CharField(db_column='Free1', blank=True, null=True)  # Field name made lowercase.
    free2 = models.CharField(db_column='Free2', blank=True, null=True)  # Field name made lowercase.
    free3 = models.CharField(db_column='Free3', blank=True, null=True)  # Field name made lowercase.
    free4 = models.CharField(db_column='Free4', blank=True, null=True)  # Field name made lowercase.
    free5 = models.CharField(db_column='Free5', blank=True, null=True)  # Field name made lowercase.
    other1 = models.CharField(db_column='Other1', blank=True, null=True)  # Field name made lowercase.
    other2 = models.CharField(db_column='Other2', blank=True, null=True)  # Field name made lowercase.
    other3 = models.CharField(db_column='Other3', blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', blank=True, null=True)  # Field name made lowercase.
    fechaemi = models.CharField(db_column='Fechaemi', blank=True, null=True)  # Field name made lowercase.
    restotext = models.CharField(db_column='Restotext', blank=True, null=True)  # Field name made lowercase.
    portext = models.CharField(db_column='Portext', blank=True, null=True)  # Field name made lowercase.
    gastosconiva = models.CharField(db_column='GastosconIva', blank=True, null=True)  # Field name made lowercase.
    nature13 = models.CharField(db_column='Nature13', blank=True, null=True)  # Field name made lowercase.
    nature14 = models.CharField(db_column='Nature14', blank=True, null=True)  # Field name made lowercase.
    nature15 = models.CharField(db_column='Nature15', blank=True, null=True)  # Field name made lowercase.
    nature16 = models.CharField(db_column='Nature16', blank=True, null=True)  # Field name made lowercase.
    nature17 = models.CharField(db_column='Nature17', blank=True, null=True)  # Field name made lowercase.
    nature18 = models.CharField(db_column='Nature18', blank=True, null=True)  # Field name made lowercase.
    nature19 = models.CharField(db_column='Nature19', blank=True, null=True)  # Field name made lowercase.
    asagent = models.CharField(db_column='AsAgent', blank=True, null=True)  # Field name made lowercase.
    ofthecarrier = models.CharField(db_column='OfTheCarrier', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.GuiasGrabadas2'


class SeguirGuiasgrabadas3(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    piezas = models.CharField(db_column='Piezas', blank=True, null=True)  # Field name made lowercase.
    piezas2 = models.CharField(db_column='Piezas2', blank=True, null=True)  # Field name made lowercase.
    piezas3 = models.CharField(db_column='Piezas3', blank=True, null=True)  # Field name made lowercase.
    piezas4 = models.CharField(db_column='Piezas4', blank=True, null=True)  # Field name made lowercase.
    piezas5 = models.CharField(db_column='Piezas5', blank=True, null=True)  # Field name made lowercase.
    totpiezas = models.CharField(db_column='TotPiezas', blank=True, null=True)  # Field name made lowercase.
    gross = models.CharField(db_column='Gross', blank=True, null=True)  # Field name made lowercase.
    otrogross = models.CharField(db_column='OtroGross', blank=True, null=True)  # Field name made lowercase.
    otrogross2 = models.CharField(db_column='OtroGross2', blank=True, null=True)  # Field name made lowercase.
    otrogross3 = models.CharField(db_column='OtroGross3', blank=True, null=True)  # Field name made lowercase.
    otrogross4 = models.CharField(db_column='OtroGross4', blank=True, null=True)  # Field name made lowercase.
    totgross = models.CharField(db_column='TotGross', blank=True, null=True)  # Field name made lowercase.
    k = models.CharField(db_column='K', blank=True, null=True)  # Field name made lowercase.
    k2 = models.CharField(db_column='K2', blank=True, null=True)  # Field name made lowercase.
    k3 = models.CharField(db_column='K3', blank=True, null=True)  # Field name made lowercase.
    k4 = models.CharField(db_column='K4', blank=True, null=True)  # Field name made lowercase.
    k5 = models.CharField(db_column='K5', blank=True, null=True)  # Field name made lowercase.
    r = models.CharField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    r2 = models.CharField(db_column='R2', blank=True, null=True)  # Field name made lowercase.
    r3 = models.CharField(db_column='R3', blank=True, null=True)  # Field name made lowercase.
    r4 = models.CharField(db_column='R4', blank=True, null=True)  # Field name made lowercase.
    r5 = models.CharField(db_column='R5', blank=True, null=True)  # Field name made lowercase.
    commodity = models.CharField(db_column='Commodity', blank=True, null=True)  # Field name made lowercase.
    comm2 = models.CharField(db_column='Comm2', blank=True, null=True)  # Field name made lowercase.
    comm3 = models.CharField(db_column='Comm3', blank=True, null=True)  # Field name made lowercase.
    comm4 = models.CharField(db_column='Comm4', blank=True, null=True)  # Field name made lowercase.
    comm5 = models.CharField(db_column='Comm5', blank=True, null=True)  # Field name made lowercase.
    chw = models.CharField(db_column='Chw', blank=True, null=True)  # Field name made lowercase.
    asvol = models.CharField(db_column='AsVol', blank=True, null=True)  # Field name made lowercase.
    chw3 = models.CharField(db_column='Chw3', blank=True, null=True)  # Field name made lowercase.
    chw4 = models.CharField(db_column='Chw4', blank=True, null=True)  # Field name made lowercase.
    chw5 = models.CharField(db_column='Chw5', blank=True, null=True)  # Field name made lowercase.
    rate = models.CharField(db_column='Rate', blank=True, null=True)  # Field name made lowercase.
    rate2 = models.CharField(db_column='Rate2', blank=True, null=True)  # Field name made lowercase.
    rate3 = models.CharField(db_column='Rate3', blank=True, null=True)  # Field name made lowercase.
    rate4 = models.CharField(db_column='Rate4', blank=True, null=True)  # Field name made lowercase.
    rate5 = models.CharField(db_column='Rate5', blank=True, null=True)  # Field name made lowercase.
    total = models.CharField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    total2 = models.CharField(db_column='Total2', blank=True, null=True)  # Field name made lowercase.
    total3 = models.CharField(db_column='Total3', blank=True, null=True)  # Field name made lowercase.
    total4 = models.CharField(db_column='Total4', blank=True, null=True)  # Field name made lowercase.
    total5 = models.CharField(db_column='Total5', blank=True, null=True)  # Field name made lowercase.
    totalfinal = models.CharField(db_column='TotalFinal', blank=True, null=True)  # Field name made lowercase.
    totalpp = models.CharField(db_column='TotalPP', blank=True, null=True)  # Field name made lowercase.
    totalcc = models.CharField(db_column='TotalCC', blank=True, null=True)  # Field name made lowercase.
    valpp = models.CharField(db_column='ValPP', blank=True, null=True)  # Field name made lowercase.
    valcc = models.CharField(db_column='ValCC', blank=True, null=True)  # Field name made lowercase.
    taxpp = models.CharField(db_column='TaxPP', blank=True, null=True)  # Field name made lowercase.
    taxcc = models.CharField(db_column='TaxCC', blank=True, null=True)  # Field name made lowercase.
    dapp = models.CharField(db_column='DaPP', blank=True, null=True)  # Field name made lowercase.
    dacc = models.CharField(db_column='DaCC', blank=True, null=True)  # Field name made lowercase.
    dcpp = models.CharField(db_column='DcPP', blank=True, null=True)  # Field name made lowercase.
    dccc = models.CharField(db_column='DcCC', blank=True, null=True)  # Field name made lowercase.
    totalprepaid = models.CharField(db_column='TotalPrepaid', blank=True, null=True)  # Field name made lowercase.
    totalcollect = models.CharField(db_column='TotalCollect', blank=True, null=True)  # Field name made lowercase.
    totalpprate = models.CharField(db_column='TotalPPRate', blank=True, null=True)  # Field name made lowercase.
    totalccrate = models.CharField(db_column='TotalCCRate', blank=True, null=True)  # Field name made lowercase.
    cass = models.CharField(db_column='Cass', blank=True, null=True)  # Field name made lowercase.
    chgscode = models.CharField(db_column='ChgsCode', blank=True, null=True)  # Field name made lowercase.
    wtval = models.CharField(db_column='WtVal', blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(db_column='Other', blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', blank=True, null=True)  # Field name made lowercase.
    carrierfinal = models.CharField(db_column='CarrierFinal', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.GuiasGrabadas3'


class SeguirMbl(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', blank=True, null=True)  # Field name made lowercase.
    cliente1 = models.CharField(db_column='Cliente1', blank=True, null=True)  # Field name made lowercase.
    cliente2 = models.CharField(db_column='Cliente2', blank=True, null=True)  # Field name made lowercase.
    cliente3 = models.CharField(db_column='Cliente3', blank=True, null=True)  # Field name made lowercase.
    cliente4 = models.CharField(db_column='Cliente4', blank=True, null=True)  # Field name made lowercase.
    consigna = models.CharField(db_column='Consigna', blank=True, null=True)  # Field name made lowercase.
    direcconsigna = models.CharField(db_column='DirecConsigna', blank=True, null=True)  # Field name made lowercase.
    localconsigna = models.CharField(db_column='LocalConsigna', blank=True, null=True)  # Field name made lowercase.
    teleconsigna = models.CharField(db_column='TeleConsigna', blank=True, null=True)  # Field name made lowercase.
    otralinea = models.CharField(db_column='Otralinea', blank=True, null=True)  # Field name made lowercase.
    notif = models.CharField(db_column='Notif', blank=True, null=True)  # Field name made lowercase.
    dirnotif = models.CharField(db_column='DirNotif', blank=True, null=True)  # Field name made lowercase.
    otralinea2 = models.CharField(db_column='Otralinea2', blank=True, null=True)  # Field name made lowercase.
    telnotif = models.CharField(db_column='TelNotif', blank=True, null=True)  # Field name made lowercase.
    tipoflete = models.CharField(db_column='TipoFlete', blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(db_column='Position', blank=True, null=True)  # Field name made lowercase.
    salede = models.CharField(db_column='Salede', blank=True, null=True)  # Field name made lowercase.
    vapor = models.CharField(db_column='Vapor', blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', blank=True, null=True)  # Field name made lowercase.
    delivery = models.CharField(db_column='Delivery', blank=True, null=True)  # Field name made lowercase.
    transterms = models.CharField(db_column='TransTerms', blank=True, null=True)  # Field name made lowercase.
    simbolo = models.CharField(db_column='Simbolo', blank=True, null=True)  # Field name made lowercase.
    condentrega = models.CharField(db_column='CondEntrega', blank=True, null=True)  # Field name made lowercase.
    tipomov = models.CharField(db_column='TipoMov', blank=True, null=True)  # Field name made lowercase.
    carriage = models.CharField(db_column='Carriage', blank=True, null=True)  # Field name made lowercase.
    custom = models.CharField(db_column='Custom', blank=True, null=True)  # Field name made lowercase.
    valseguro = models.CharField(db_column='ValSeguro', blank=True, null=True)  # Field name made lowercase.
    goods = models.CharField(db_column='Goods', blank=True, null=True)  # Field name made lowercase.
    free1 = models.CharField(db_column='Free1', blank=True, null=True)  # Field name made lowercase.
    free2 = models.CharField(db_column='Free2', blank=True, null=True)  # Field name made lowercase.
    free3 = models.CharField(db_column='Free3', blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', blank=True, null=True)  # Field name made lowercase.
    signature2 = models.CharField(db_column='Signature2', blank=True, null=True)  # Field name made lowercase.
    signature3 = models.CharField(db_column='Signature3', blank=True, null=True)  # Field name made lowercase.
    nbls = models.CharField(db_column='Nbls', blank=True, null=True)  # Field name made lowercase.
    payable = models.CharField(db_column='Payable', blank=True, null=True)  # Field name made lowercase.
    board = models.CharField(db_column='Board', blank=True, null=True)  # Field name made lowercase.
    clean = models.CharField(db_column='Clean', blank=True, null=True)  # Field name made lowercase.
    fechaemi = models.CharField(db_column='FechaEmi', blank=True, null=True)  # Field name made lowercase.
    restotext = models.CharField(db_column='RestoText', blank=True, null=True)  # Field name made lowercase.
    vadeclared = models.CharField(db_column='VaDeclared', blank=True, null=True)  # Field name made lowercase.
    portext = models.CharField(db_column='PorText', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.MBL'


class SeguirMbl2(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    marks = models.CharField(db_column='Marks', blank=True, null=True)  # Field name made lowercase.
    packages = models.CharField(db_column='Packages', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    gross = models.CharField(db_column='Gross', blank=True, null=True)  # Field name made lowercase.
    tare = models.CharField(db_column='Tare', blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.MBL2'


class SeguirMadresgrabadas(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    empresa = models.CharField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', blank=True, null=True)  # Field name made lowercase.
    localidad = models.CharField(db_column='Localidad', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', blank=True, null=True)  # Field name made lowercase.
    cliente1 = models.CharField(db_column='Cliente1', blank=True, null=True)  # Field name made lowercase.
    cliente2 = models.CharField(db_column='Cliente2', blank=True, null=True)  # Field name made lowercase.
    cliente3 = models.CharField(db_column='Cliente3', blank=True, null=True)  # Field name made lowercase.
    cliente4 = models.CharField(db_column='Cliente4', blank=True, null=True)  # Field name made lowercase.
    consigna = models.CharField(db_column='Consigna', blank=True, null=True)  # Field name made lowercase.
    direcconsigna = models.CharField(db_column='DirecConsigna', blank=True, null=True)  # Field name made lowercase.
    localconsigna = models.CharField(db_column='LocalConsigna', blank=True, null=True)  # Field name made lowercase.
    teleconsigna = models.CharField(db_column='TeleConsigna', blank=True, null=True)  # Field name made lowercase.
    otralinea = models.CharField(db_column='Otralinea', blank=True, null=True)  # Field name made lowercase.
    empresa2 = models.CharField(db_column='Empresa2', blank=True, null=True)  # Field name made lowercase.
    otracarrier = models.CharField(db_column='OtraCarrier', blank=True, null=True)  # Field name made lowercase.
    localidad2 = models.CharField(db_column='Localidad2', blank=True, null=True)  # Field name made lowercase.
    otrosdeagente = models.CharField(db_column='OtrosdeAgente', blank=True, null=True)  # Field name made lowercase.
    iata = models.CharField(db_column='Iata', blank=True, null=True)  # Field name made lowercase.
    salede = models.CharField(db_column='Salede', blank=True, null=True)  # Field name made lowercase.
    cadenaaerea = models.CharField(db_column='CadenaAerea', blank=True, null=True)  # Field name made lowercase.
    tipoflete = models.CharField(db_column='TipoFlete', blank=True, null=True)  # Field name made lowercase.
    notif = models.CharField(db_column='Notif', blank=True, null=True)  # Field name made lowercase.
    dirnotif = models.CharField(db_column='DirNotif', blank=True, null=True)  # Field name made lowercase.
    otralinea2 = models.CharField(db_column='Otralinea2', blank=True, null=True)  # Field name made lowercase.
    telnotif = models.CharField(db_column='TelNotif', blank=True, null=True)  # Field name made lowercase.
    otralinea3 = models.CharField(db_column='Otralinea3', blank=True, null=True)  # Field name made lowercase.
    otralinea4 = models.CharField(db_column='Otralinea4', blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', blank=True, null=True)  # Field name made lowercase.
    idtransport = models.CharField(db_column='Idtransport', blank=True, null=True)  # Field name made lowercase.
    to1 = models.CharField(db_column='To1', blank=True, null=True)  # Field name made lowercase.
    by1 = models.CharField(db_column='By1', blank=True, null=True)  # Field name made lowercase.
    to2 = models.CharField(db_column='To2', blank=True, null=True)  # Field name made lowercase.
    by2 = models.CharField(db_column='By2', blank=True, null=True)  # Field name made lowercase.
    simbolo = models.CharField(db_column='Simbolo', blank=True, null=True)  # Field name made lowercase.
    carriage = models.CharField(db_column='Carriage', blank=True, null=True)  # Field name made lowercase.
    custom = models.CharField(db_column='Custom', blank=True, null=True)  # Field name made lowercase.
    nombredestino = models.CharField(db_column='NombreDestino', blank=True, null=True)  # Field name made lowercase.
    vuelo1 = models.CharField(db_column='Vuelo1', blank=True, null=True)  # Field name made lowercase.
    vuelo2 = models.CharField(db_column='Vuelo2', blank=True, null=True)  # Field name made lowercase.
    vuelo3 = models.CharField(db_column='Vuelo3', blank=True, null=True)  # Field name made lowercase.
    vuelo4 = models.CharField(db_column='Vuelo4', blank=True, null=True)  # Field name made lowercase.
    valseguro = models.CharField(db_column='ValSeguro', blank=True, null=True)  # Field name made lowercase.
    marcas = models.CharField(db_column='Marcas', blank=True, null=True)  # Field name made lowercase.
    otraline = models.CharField(db_column='Otraline', blank=True, null=True)  # Field name made lowercase.
    attached = models.CharField(db_column='Attached', blank=True, null=True)  # Field name made lowercase.
    nature2 = models.CharField(db_column='Nature2', blank=True, null=True)  # Field name made lowercase.
    nature3 = models.CharField(db_column='Nature3', blank=True, null=True)  # Field name made lowercase.
    houses = models.CharField(db_column='Houses', blank=True, null=True)  # Field name made lowercase.
    houses2 = models.CharField(db_column='Houses2', blank=True, null=True)  # Field name made lowercase.
    houses3 = models.CharField(db_column='Houses3', blank=True, null=True)  # Field name made lowercase.
    free1 = models.CharField(db_column='Free1', blank=True, null=True)  # Field name made lowercase.
    free2 = models.CharField(db_column='Free2', blank=True, null=True)  # Field name made lowercase.
    free3 = models.CharField(db_column='Free3', blank=True, null=True)  # Field name made lowercase.
    free4 = models.CharField(db_column='Free4', blank=True, null=True)  # Field name made lowercase.
    free5 = models.CharField(db_column='Free5', blank=True, null=True)  # Field name made lowercase.
    other1 = models.CharField(db_column='Other1', blank=True, null=True)  # Field name made lowercase.
    other2 = models.CharField(db_column='Other2', blank=True, null=True)  # Field name made lowercase.
    other3 = models.CharField(db_column='Other3', blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', blank=True, null=True)  # Field name made lowercase.
    fechaemi = models.CharField(db_column='Fechaemi', blank=True, null=True)  # Field name made lowercase.
    restotext = models.CharField(db_column='RestoText', blank=True, null=True)  # Field name made lowercase.
    portext = models.CharField(db_column='PorText', blank=True, null=True)  # Field name made lowercase.
    houses4 = models.CharField(db_column='Houses4', blank=True, null=True)  # Field name made lowercase.
    houses5 = models.CharField(db_column='Houses5', blank=True, null=True)  # Field name made lowercase.
    houses6 = models.CharField(db_column='Houses6', blank=True, null=True)  # Field name made lowercase.
    asagent = models.CharField(db_column='AsAgent', blank=True, null=True)  # Field name made lowercase.
    ofthecarrier = models.CharField(db_column='OfTheCarrier', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.MadresGrabadas'


class SeguirMadresgrabadas3(models.Model):
    numero = models.CharField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    piezas = models.CharField(db_column='Piezas', blank=True, null=True)  # Field name made lowercase.
    piezas2 = models.CharField(db_column='Piezas2', blank=True, null=True)  # Field name made lowercase.
    piezas3 = models.CharField(db_column='Piezas3', blank=True, null=True)  # Field name made lowercase.
    piezas4 = models.CharField(db_column='Piezas4', blank=True, null=True)  # Field name made lowercase.
    piezas5 = models.CharField(db_column='Piezas5', blank=True, null=True)  # Field name made lowercase.
    totpiezas = models.CharField(db_column='TotPiezas', blank=True, null=True)  # Field name made lowercase.
    gross = models.CharField(db_column='Gross', blank=True, null=True)  # Field name made lowercase.
    otrogross = models.CharField(db_column='OtroGross', blank=True, null=True)  # Field name made lowercase.
    otrogross2 = models.CharField(db_column='OtroGross2', blank=True, null=True)  # Field name made lowercase.
    otrogross3 = models.CharField(db_column='OtroGross3', blank=True, null=True)  # Field name made lowercase.
    otrogross4 = models.CharField(db_column='OtroGross4', blank=True, null=True)  # Field name made lowercase.
    totgross = models.CharField(db_column='TotGross', blank=True, null=True)  # Field name made lowercase.
    k = models.CharField(db_column='K', blank=True, null=True)  # Field name made lowercase.
    k2 = models.CharField(db_column='K2', blank=True, null=True)  # Field name made lowercase.
    k3 = models.CharField(db_column='K3', blank=True, null=True)  # Field name made lowercase.
    k4 = models.CharField(db_column='K4', blank=True, null=True)  # Field name made lowercase.
    k5 = models.CharField(db_column='K5', blank=True, null=True)  # Field name made lowercase.
    r = models.CharField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    r2 = models.CharField(db_column='R2', blank=True, null=True)  # Field name made lowercase.
    r3 = models.CharField(db_column='R3', blank=True, null=True)  # Field name made lowercase.
    r4 = models.CharField(db_column='R4', blank=True, null=True)  # Field name made lowercase.
    r5 = models.CharField(db_column='R5', blank=True, null=True)  # Field name made lowercase.
    commodity = models.CharField(db_column='Commodity', blank=True, null=True)  # Field name made lowercase.
    comm2 = models.CharField(db_column='Comm2', blank=True, null=True)  # Field name made lowercase.
    comm3 = models.CharField(db_column='Comm3', blank=True, null=True)  # Field name made lowercase.
    comm4 = models.CharField(db_column='Comm4', blank=True, null=True)  # Field name made lowercase.
    comm5 = models.CharField(db_column='Comm5', blank=True, null=True)  # Field name made lowercase.
    chw = models.CharField(db_column='Chw', blank=True, null=True)  # Field name made lowercase.
    asvol = models.CharField(db_column='AsVol', blank=True, null=True)  # Field name made lowercase.
    chw3 = models.CharField(db_column='Chw3', blank=True, null=True)  # Field name made lowercase.
    chw4 = models.CharField(db_column='Chw4', blank=True, null=True)  # Field name made lowercase.
    chw5 = models.CharField(db_column='Chw5', blank=True, null=True)  # Field name made lowercase.
    rate = models.CharField(db_column='Rate', blank=True, null=True)  # Field name made lowercase.
    rate2 = models.CharField(db_column='Rate2', blank=True, null=True)  # Field name made lowercase.
    rate3 = models.CharField(db_column='Rate3', blank=True, null=True)  # Field name made lowercase.
    rate4 = models.CharField(db_column='Rate4', blank=True, null=True)  # Field name made lowercase.
    rate5 = models.CharField(db_column='Rate5', blank=True, null=True)  # Field name made lowercase.
    total = models.CharField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    total2 = models.CharField(db_column='Total2', blank=True, null=True)  # Field name made lowercase.
    total3 = models.CharField(db_column='Total3', blank=True, null=True)  # Field name made lowercase.
    total4 = models.CharField(db_column='Total4', blank=True, null=True)  # Field name made lowercase.
    total5 = models.CharField(db_column='Total5', blank=True, null=True)  # Field name made lowercase.
    totalfinal = models.CharField(db_column='TotalFinal', blank=True, null=True)  # Field name made lowercase.
    totalpp = models.CharField(db_column='TotalPP', blank=True, null=True)  # Field name made lowercase.
    totalcc = models.CharField(db_column='TotalCC', blank=True, null=True)  # Field name made lowercase.
    valpp = models.CharField(db_column='ValPP', blank=True, null=True)  # Field name made lowercase.
    valcc = models.CharField(db_column='ValCC', blank=True, null=True)  # Field name made lowercase.
    taxpp = models.CharField(db_column='TaxPP', blank=True, null=True)  # Field name made lowercase.
    taxcc = models.CharField(db_column='TaxCC', blank=True, null=True)  # Field name made lowercase.
    dapp = models.CharField(db_column='DaPP', blank=True, null=True)  # Field name made lowercase.
    dacc = models.CharField(db_column='DaCC', blank=True, null=True)  # Field name made lowercase.
    dcpp = models.CharField(db_column='DcPP', blank=True, null=True)  # Field name made lowercase.
    dccc = models.CharField(db_column='DcCC', blank=True, null=True)  # Field name made lowercase.
    totalprepaid = models.CharField(db_column='TotalPrepaid', blank=True, null=True)  # Field name made lowercase.
    totalcollect = models.CharField(db_column='TotalCollect', blank=True, null=True)  # Field name made lowercase.
    totalpprate = models.CharField(db_column='TotalPPRate', blank=True, null=True)  # Field name made lowercase.
    totalccrate = models.CharField(db_column='TotalCCRate', blank=True, null=True)  # Field name made lowercase.
    cass = models.CharField(db_column='Cass', blank=True, null=True)  # Field name made lowercase.
    chgscode = models.CharField(db_column='ChgsCode', blank=True, null=True)  # Field name made lowercase.
    wtval = models.CharField(db_column='WtVal', blank=True, null=True)  # Field name made lowercase.
    other = models.CharField(db_column='Other', blank=True, null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', blank=True, null=True)  # Field name made lowercase.
    carrierfinal = models.CharField(db_column='CarrierFinal', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.MadresGrabadas3'


class SeguirReservas(models.Model):
    numero = models.CharField(blank=True, null=True)
    transportista = models.CharField(blank=True, null=True)
    armador = models.CharField(blank=True, null=True)
    agente = models.CharField(blank=True, null=True)
    fecha = models.CharField(blank=True, null=True)
    origen = models.CharField(blank=True, null=True)
    destino = models.CharField(blank=True, null=True)
    awb = models.CharField(blank=True, null=True)
    cotizacion = models.CharField(blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    vapor = models.CharField(blank=True, null=True)
    viaje = models.CharField(blank=True, null=True)
    aplicable = models.CharField(blank=True, null=True)
    iniciales = models.CharField(blank=True, null=True)
    modo = models.CharField(blank=True, null=True)
    embarque = models.CharField(blank=True, null=True)
    editado = models.CharField(db_column='Editado', blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', blank=True, null=True)  # Field name made lowercase.
    pagoflete = models.CharField(db_column='PagoFlete', blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    arbitraje = models.CharField(db_column='Arbitraje', blank=True, null=True)  # Field name made lowercase.
    tomopeso = models.CharField(db_column='TomoPeso', blank=True, null=True)  # Field name made lowercase.
    tarifaawb = models.CharField(db_column='TarifaAWB', blank=True, null=True)  # Field name made lowercase.
    kilos = models.CharField(db_column='Kilos', blank=True, null=True)  # Field name made lowercase.
    volumen = models.CharField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    tarifafija = models.CharField(db_column='TarifaFija', blank=True, null=True)  # Field name made lowercase.
    tarifa = models.CharField(db_column='Tarifa', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.Reservas'


class SeguirSeguimiento(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    cliente = models.SmallIntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    embarcador = models.SmallIntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    vaporcli = models.CharField(db_column='Vaporcli', blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(max_length=16, blank=True, null=True)
    fecha = models.CharField(max_length=19, blank=True, null=True)
    vencimiento = models.CharField(max_length=19, blank=True, null=True)
    embarque = models.SmallIntegerField(blank=True, null=True)
    vapor = models.CharField(max_length=23, blank=True, null=True)
    awb = models.CharField(max_length=24, blank=True, null=True)
    hawb = models.CharField(max_length=23, blank=True, null=True)
    volumen = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True)
    tarifaventa = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    tarifacompra = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    pago = models.CharField(max_length=7, blank=True, null=True)
    refcliente = models.CharField(max_length=78, blank=True, null=True)
    transportista = models.SmallIntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=15, blank=True, null=True)
    cotizacion = models.SmallIntegerField(blank=True, null=True)
    cotizacion1 = models.SmallIntegerField(blank=True, null=True)
    vaporcli2 = models.CharField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    vendedor = models.IntegerField(blank=True, null=True)
    despachante = models.SmallIntegerField(blank=True, null=True)
    agecompras = models.SmallIntegerField(blank=True, null=True)
    ageventas = models.SmallIntegerField(blank=True, null=True)
    deposito = models.IntegerField(blank=True, null=True)
    recepcion = models.CharField(max_length=19, blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    nrodespacho = models.CharField(max_length=11, blank=True, null=True)
    aduana = models.CharField(max_length=3, blank=True, null=True)
    fecacepta = models.CharField(max_length=19, blank=True, null=True)
    fecentrega = models.CharField(max_length=19, blank=True, null=True)
    fecretiro = models.CharField(max_length=19, blank=True, null=True)
    totalgiro = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    nroguiadesp = models.IntegerField(blank=True, null=True)
    aplicable = models.CharField(max_length=9, blank=True, null=True)
    refproveedor = models.CharField(max_length=76, blank=True, null=True)
    estimadorecepcion = models.CharField(max_length=19, blank=True, null=True)
    eta = models.CharField(max_length=19, blank=True, null=True)
    etd = models.CharField(max_length=19, blank=True, null=True)
    recepcionado = models.CharField(max_length=1, blank=True, null=True)
    lugar = models.CharField(max_length=11, blank=True, null=True)
    fecaduana = models.CharField(db_column='Fecaduana', max_length=19, blank=True, null=True)  # Field name made lowercase.
    fecdocage = models.CharField(db_column='Fecdocage', max_length=19, blank=True, null=True)  # Field name made lowercase.
    fecrecdoc = models.CharField(max_length=19, blank=True, null=True)
    fecemision = models.CharField(max_length=19, blank=True, null=True)
    fecseguro = models.CharField(max_length=19, blank=True, null=True)
    nroseguro = models.CharField(max_length=3, blank=True, null=True)
    valor = models.CharField(max_length=9, blank=True, null=True)
    manifiesto = models.CharField(max_length=3, blank=True, null=True)
    ubicacion = models.CharField(max_length=18, blank=True, null=True)
    fecpagoder = models.CharField(max_length=19, blank=True, null=True)
    tarifafija = models.CharField(max_length=1, blank=True, null=True)
    tomopeso = models.IntegerField(blank=True, null=True)
    fecpresdi = models.CharField(max_length=19, blank=True, null=True)
    prima = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    centro = models.CharField(max_length=9, blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    transportelocal = models.IntegerField(blank=True, null=True)
    estimadopup = models.CharField(max_length=19, blank=True, null=True)
    realpup = models.CharField(max_length=19, blank=True, null=True)
    estimadodelivery = models.CharField(max_length=19, blank=True, null=True)
    realdelivery = models.CharField(max_length=19, blank=True, null=True)
    referencialocal = models.CharField(max_length=3, blank=True, null=True)
    modolocal = models.CharField(max_length=8, blank=True, null=True)
    fecguiadesp = models.CharField(max_length=19, blank=True, null=True)
    tarifaprofit = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    armador = models.SmallIntegerField(blank=True, null=True)
    notificar = models.SmallIntegerField(db_column='Notificar', blank=True, null=True)  # Field name made lowercase.
    fechaonhand = models.CharField(db_column='FechaOnHand', max_length=19, blank=True, null=True)  # Field name made lowercase.
    booking = models.CharField(max_length=29, blank=True, null=True)
    propia = models.IntegerField(db_column='Propia', blank=True, null=True)  # Field name made lowercase.
    trafico = models.IntegerField(db_column='Trafico', blank=True, null=True)  # Field name made lowercase.
    proyecto = models.IntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    modificado = models.CharField(db_column='Modificado', max_length=1, blank=True, null=True)  # Field name made lowercase.
    depcontenedoringreso = models.IntegerField(db_column='DepContenedorIngreso', blank=True, null=True)  # Field name made lowercase.
    depcontenedorvacios = models.IntegerField(db_column='DepContenedorVacios', blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=3, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True, null=True)  # Field name made lowercase.
    deadborrador = models.CharField(db_column='DeadBorrador', max_length=19, blank=True, null=True)  # Field name made lowercase.
    deaddocumentos = models.CharField(db_column='DeadDocumentos', max_length=19, blank=True, null=True)  # Field name made lowercase.
    deadentrega = models.CharField(db_column='DeadEntrega', max_length=19, blank=True, null=True)  # Field name made lowercase.
    deadliberacion = models.CharField(db_column='DeadLiberacion', max_length=19, blank=True, null=True)  # Field name made lowercase.
    retiravacio = models.CharField(db_column='RetiraVacio', max_length=19, blank=True, null=True)  # Field name made lowercase.
    retiralleno = models.CharField(db_column='RetiraLleno', max_length=19, blank=True, null=True)  # Field name made lowercase.
    arriboreal = models.CharField(db_column='ArriboReal', max_length=19, blank=True, null=True)  # Field name made lowercase.
    pagoenfirme = models.CharField(db_column='PagoenFirme', max_length=19, blank=True, null=True)  # Field name made lowercase.
    recepcionprealert = models.CharField(db_column='RecepcionPrealert', max_length=19, blank=True, null=True)  # Field name made lowercase.
    bltipo = models.CharField(db_column='BLTipo', max_length=16, blank=True, null=True)  # Field name made lowercase.
    credito = models.CharField(db_column='Credito', max_length=3, blank=True, null=True)  # Field name made lowercase.
    revalidacion = models.CharField(db_column='Revalidacion', max_length=19, blank=True, null=True)  # Field name made lowercase.
    almacenajelibrehasta = models.CharField(db_column='AlmacenajeLibreHasta', max_length=19, blank=True, null=True)  # Field name made lowercase.
    demoraslibrehasta = models.CharField(db_column='DemorasLibreHasta', max_length=19, blank=True, null=True)  # Field name made lowercase.
    entregavacio = models.CharField(db_column='EntregaVacio', max_length=19, blank=True, null=True)  # Field name made lowercase.
    tipobonifcli = models.CharField(db_column='TipoBonifCli', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bonifcli = models.DecimalField(db_column='BonifCli', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    originales = models.CharField(db_column='Originales', max_length=1, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=11, blank=True, null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=17, blank=True, null=True)  # Field name made lowercase.
    consolidado = models.CharField(db_column='Consolidado', blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)  # Field name made lowercase.
    hawbtext = models.CharField(db_column='HawbText', max_length=3, blank=True, null=True)  # Field name made lowercase.
    demora = models.IntegerField(db_column='Demora', blank=True, null=True)  # Field name made lowercase.
    valordemoravta = models.CharField(db_column='ValorDemoraVTA', max_length=6, blank=True, null=True)  # Field name made lowercase.
    valordemoracpa = models.CharField(db_column='ValorDemoraCPA', max_length=6, blank=True, null=True)  # Field name made lowercase.
    rotulosincorrectos = models.CharField(db_column='RotulosIncorrectos', max_length=1, blank=True, null=True)  # Field name made lowercase.
    actividad = models.IntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    entregadoa = models.CharField(db_column='EntregadoA', blank=True, null=True)  # Field name made lowercase.
    loadingdate = models.CharField(db_column='LoadingDate', max_length=19, blank=True, null=True)  # Field name made lowercase.
    diasalmacenaje = models.IntegerField(db_column='DiasAlmacenaje', blank=True, null=True)  # Field name made lowercase.
    muestroflete = models.DecimalField(db_column='MuestroFlete', max_digits=8, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    operacion = models.CharField(db_column='Operacion', max_length=23, blank=True, null=True)  # Field name made lowercase.
    enviointtrabk = models.CharField(db_column='EnvioInttraBK', blank=True, null=True)  # Field name made lowercase.
    enviointtrasi = models.CharField(db_column='EnvioInttraSI', blank=True, null=True)  # Field name made lowercase.
    maerskbk = models.CharField(db_column='MaerskBK', blank=True, null=True)  # Field name made lowercase.
    maersksi = models.CharField(db_column='MaerskSI', blank=True, null=True)  # Field name made lowercase.
    wwanumerobooking = models.CharField(db_column='WWANumeroBooking', blank=True, null=True)  # Field name made lowercase.
    envioeasipassbk = models.CharField(db_column='EnvioEASIPASSBK', blank=True, null=True)  # Field name made lowercase.
    envioeasipasssi = models.CharField(db_column='EnvioEASIPASSSI', blank=True, null=True)  # Field name made lowercase.
    fechastacking = models.CharField(db_column='FechaStacking', max_length=19, blank=True, null=True)  # Field name made lowercase.
    horastacking = models.CharField(db_column='HoraStacking', blank=True, null=True)  # Field name made lowercase.
    fechafinstacking = models.CharField(db_column='FechaFinStacking', max_length=19, blank=True, null=True)  # Field name made lowercase.
    horafinstacking = models.CharField(db_column='HoraFinStacking', blank=True, null=True)  # Field name made lowercase.
    fechacutoff = models.CharField(db_column='FechaCutOff', max_length=19, blank=True, null=True)  # Field name made lowercase.
    horacutoff = models.CharField(db_column='HoraCutOff', blank=True, null=True)  # Field name made lowercase.
    tieneseguro = models.CharField(db_column='TieneSeguro', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=3, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=27, blank=True, null=True)  # Field name made lowercase.
    fechacutoffvgm = models.CharField(db_column='FechaCutOffVGM', max_length=19, blank=True, null=True)  # Field name made lowercase.
    horacutoffvgm = models.CharField(db_column='HoraCutOffVGM', blank=True, null=True)  # Field name made lowercase.
    nroreferedi = models.CharField(db_column='NroReferEDI', blank=True, null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', blank=True, null=True)  # Field name made lowercase.
    deaddocumentoshora = models.CharField(db_column='DeadDocumentosHora', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.Seguimiento'


class SeguirServireserva(models.Model):
    numero = models.CharField(blank=True, null=True)
    servicio = models.CharField(blank=True, null=True)
    moneda = models.CharField(blank=True, null=True)
    modo = models.CharField(blank=True, null=True)
    costo = models.CharField(blank=True, null=True)
    detalle = models.CharField(blank=True, null=True)
    tipogasto = models.CharField(blank=True, null=True)
    arbitraje = models.CharField(blank=True, null=True)
    notomaprofit = models.CharField(blank=True, null=True)
    repartir = models.CharField(blank=True, null=True)
    pinformar = models.CharField(blank=True, null=True)
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.Servireserva'


class SeguirTraceop(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=19, blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=11, blank=True, null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=123, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=9, blank=True, null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.TraceOP'


class SeguirConexaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=23, blank=True, null=True)  # Field name made lowercase.
    salida = models.CharField(max_length=19, blank=True, null=True)
    llegada = models.CharField(max_length=19, blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(max_length=9, blank=True, null=True)
    accion = models.CharField(db_column='Accion', max_length=7, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.conexaerea'


class SeguirServiceaereo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.IntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=89, blank=True, null=True)
    tipogasto = models.CharField(max_length=13, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    pinformar = models.DecimalField(max_digits=9, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    socio = models.SmallIntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Seguir.serviceaereo'
