# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuditlogLogentry(models.Model):
    object_pk = models.CharField(max_length=255)
    object_id = models.BigIntegerField(blank=True, null=True)
    object_repr = models.TextField()
    action = models.PositiveSmallIntegerField()
    changes = models.TextField()
    timestamp = models.DateTimeField()
    actor = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    remote_addr = models.CharField(max_length=39, blank=True, null=True)
    additional_data = models.JSONField(blank=True, null=True)
    serialized_data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditlog_logentry'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Activofijo(models.Model):
    codigo = models.IntegerField()
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    autogenerado = models.CharField(max_length=40, blank=True, null=True)
    grupo = models.SmallIntegerField(blank=True, null=True)
    numeroserie = models.CharField(max_length=40, blank=True, null=True)
    garantia = models.CharField(max_length=1, blank=True, null=True)
    vtogarantia = models.DateTimeField(blank=True, null=True)
    seguro = models.CharField(max_length=1, blank=True, null=True)
    aseguradora = models.IntegerField(blank=True, null=True)
    poliza = models.CharField(max_length=50, blank=True, null=True)
    ubicacion = models.CharField(max_length=50, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)
    fechabaja = models.DateTimeField(blank=True, null=True)
    destinofinal = models.CharField(max_length=100, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    monedavalorminimo = models.SmallIntegerField(blank=True, null=True)
    valorminimo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    anosdepreciacion = models.SmallIntegerField(blank=True, null=True)
    porcentaje = models.FloatField(blank=True, null=True)
    anosdepreciacionniif = models.SmallIntegerField(blank=True, null=True)
    porcentajeniif = models.FloatField(blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    valor = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    ctaactivo = models.IntegerField(blank=True, null=True)
    cuota = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    cuotaniif = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    modocalculo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_activofijo'


class Amortactivofijo(models.Model):
    codigo = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    asiento = models.FloatField(blank=True, null=True)
    valororiginal = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    valornuevo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    usuario = models.CharField(max_length=3, blank=True, null=True)
    niif = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_amortactivofijo'


class Areas(models.Model):
    numero = models.SmallIntegerField()
    nombre = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_areas'


class Asientos(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    cuenta = models.BigIntegerField(blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    monto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    cambio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=250, blank=True, null=True)
    asiento = models.FloatField(blank=True, null=True)
    imputacion = models.SmallIntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    documento = models.CharField(max_length=50, blank=True, null=True)
    vto = models.DateTimeField(blank=True, null=True)
    pasado = models.SmallIntegerField(blank=True, null=True)
    autogenerado = models.CharField(max_length=40, blank=True, null=True)
    cliente = models.IntegerField(blank=True, null=True)
    banco = models.CharField(max_length=50, blank=True, null=True)
    centro = models.CharField(max_length=3, blank=True, null=True)
    mov = models.FloatField(blank=True, null=True)
    mesimpu = models.SmallIntegerField(blank=True, null=True)
    anoimpu = models.SmallIntegerField(blank=True, null=True)
    conciliado = models.CharField(max_length=1, blank=True, null=True)
    estacion = models.SmallIntegerField(blank=True, null=True)
    posicion = models.CharField(max_length=20, blank=True, null=True)
    enviado = models.CharField(max_length=1, blank=True, null=True)
    clearing = models.DateTimeField(blank=True, null=True)
    voucher = models.IntegerField(blank=True, null=True)
    revertir = models.CharField(max_length=1, blank=True, null=True)
    fecrevertir = models.DateTimeField(blank=True, null=True)
    area = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    paridad = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    numeroenvio = models.IntegerField(blank=True, null=True)
    vinculo = models.FloatField(blank=True, null=True)
    sociocom = models.IntegerField(blank=True, null=True)
    monedaorigen = models.SmallIntegerField(blank=True, null=True)
    tccorreccion = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    parcorreccion = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    modo = models.CharField(max_length=15, blank=True, null=True)
    fechaemision = models.DateTimeField(blank=True, null=True)
    fechavencimiento = models.DateTimeField(blank=True, null=True)
    nrocomprobante = models.CharField(max_length=20, blank=True, null=True)
    desretencion = models.CharField(max_length=50, blank=True, null=True)
    baseimponible = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    control = models.CharField(max_length=1, blank=True, null=True)
    base = models.FloatField(blank=True, null=True)
    jurisdiccion = models.SmallIntegerField(blank=True, null=True)
    nroserv = models.SmallIntegerField(blank=True, null=True)
    fechacheque = models.DateTimeField(blank=True, null=True)
    bancooridest = models.SmallIntegerField(blank=True, null=True)
    cuentaoridest = models.CharField(max_length=30, blank=True, null=True)
    linkretencion = models.CharField(max_length=40, blank=True, null=True)
    foliofiscal = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_asientos'

    def get_id(self):
        asiento=Asientos.objects.last()
        return int(asiento.id+1)


class Asociadosresg(models.Model):
    rautogen = models.CharField(max_length=40, blank=True, null=True)
    rautogenasociado = models.CharField(max_length=40, blank=True, null=True)
    rformret = models.CharField(max_length=10, blank=True, null=True)
    rcodret = models.CharField(max_length=10, blank=True, null=True)
    rdescripcionret = models.CharField(max_length=100, blank=True, null=True)
    rtasa = models.FloatField(blank=True, null=True)
    rmoneda = models.IntegerField(blank=True, null=True)
    rvalor = models.FloatField(blank=True, null=True)
    rmontosujeto = models.FloatField(blank=True, null=True)
    rtiporet = models.IntegerField(blank=True, null=True)
    rtipo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_asociadosresg'


class Attachasientos(models.Model):
    autogenerado = models.CharField(max_length=40, blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_attachasientos'


class Boleta(models.Model):
    autogenerado = models.CharField(max_length=40, blank=True, null=True)
    tipo = models.SmallIntegerField(blank=True, null=True)
    tipo2 = models.SmallIntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    vto = models.DateTimeField(blank=True, null=True)
    sucursal = models.SmallIntegerField(blank=True, null=True)
    tipofactura = models.CharField(max_length=1, blank=True, null=True)
    serie = models.CharField(max_length=1, blank=True, null=True)
    prefijo = models.IntegerField(blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    linea = models.SmallIntegerField(blank=True, null=True)
    nrocliente = models.IntegerField(blank=True, null=True)
    cliente = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    direccion2 = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=30, blank=True, null=True)
    pais = models.CharField(max_length=30, blank=True, null=True)
    telefax = models.CharField(max_length=50, blank=True, null=True)
    ruc = models.CharField(max_length=30, blank=True, null=True)
    ibruto = models.CharField(max_length=1, blank=True, null=True)
    condiciones = models.CharField(max_length=50, blank=True, null=True)
    corporativo = models.CharField(max_length=20, blank=True, null=True)
    refer = models.CharField(max_length=30, blank=True, null=True)
    carrier = models.CharField(max_length=30, blank=True, null=True)
    master = models.CharField(max_length=30, blank=True, null=True)
    house = models.CharField(max_length=50, blank=True, null=True)
    vuelo = models.CharField(max_length=30, blank=True, null=True)
    nroservicio = models.IntegerField(blank=True, null=True)
    concepto = models.CharField(max_length=100, blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    iva = models.CharField(max_length=10, blank=True, null=True)
    monto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    monedalinea = models.SmallIntegerField(blank=True, null=True)
    totiva = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    totsobre = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    total = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    anticiposcobrados = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    moneda = models.CharField(max_length=10, blank=True, null=True)
    cambio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    paridad = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    montooriginal = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    posicion = models.CharField(max_length=30, blank=True, null=True)
    monedaemba = models.SmallIntegerField(blank=True, null=True)
    tcaemba = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    kilos = models.FloatField(blank=True, null=True)
    aplicable = models.FloatField(blank=True, null=True)
    volumen = models.FloatField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    pagoflete = models.CharField(max_length=1, blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    origen = models.CharField(max_length=30, blank=True, null=True)
    destino = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    texto1 = models.CharField(max_length=100, blank=True, null=True)
    texto2 = models.CharField(max_length=100, blank=True, null=True)
    texto3 = models.CharField(max_length=100, blank=True, null=True)
    texto4 = models.CharField(max_length=100, blank=True, null=True)
    texto5 = models.CharField(max_length=100, blank=True, null=True)
    llegasale = models.DateTimeField(blank=True, null=True)
    commodity = models.CharField(max_length=50, blank=True, null=True)
    embarcador = models.CharField(max_length=50, blank=True, null=True)
    consignatario = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=50, blank=True, null=True)
    orden = models.CharField(max_length=50, blank=True, null=True)
    wr = models.CharField(max_length=100, blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    ordenbolivia = models.CharField(max_length=20, blank=True, null=True)
    nrosat = models.CharField(max_length=10, blank=True, null=True)
    anosat = models.CharField(max_length=10, blank=True, null=True)
    idfiscal = models.CharField(max_length=30, blank=True, null=True)
    tipocliente = models.CharField(max_length=50, blank=True, null=True)
    nrosatnc = models.CharField(max_length=10, blank=True, null=True)
    anosatnc = models.CharField(max_length=10, blank=True, null=True)
    cliente2 = models.CharField(max_length=50, blank=True, null=True)
    aimagen = models.CharField(max_length=1, blank=True, null=True)
    cae = models.BigIntegerField(blank=True, null=True)
    fechavtocae = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_boleta'

class Boletaretenciones(models.Model):
    autogenerado = models.CharField(max_length=40, blank=True, null=True)
    nombre = models.CharField(max_length=40, blank=True, null=True)
    monto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    autorretenedor = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_boletaretenciones'


class Cabreportes(models.Model):
    numero = models.IntegerField()
    titulo = models.CharField(max_length=50, blank=True, null=True)
    netear = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_cabreportes'


class Chequeorden(models.Model):
    cfecha = models.DateTimeField(blank=True, null=True)
    cbanco = models.BigIntegerField(blank=True, null=True)
    cnumero = models.IntegerField(blank=True, null=True)
    cvto = models.DateTimeField(blank=True, null=True)
    cmonto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    corden = models.IntegerField(blank=True, null=True)
    cmoneda = models.SmallIntegerField(blank=True, null=True)
    chequeterceros = models.CharField(max_length=1, blank=True, null=True)
    clienteterceros = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_chequeorden'


class Chequeras(models.Model):
    estado = models.SmallIntegerField(blank=True, null=True)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    sucursal = models.SmallIntegerField(blank=True, null=True)
    banco = models.BigIntegerField(blank=True, null=True)
    cheque = models.FloatField(blank=True, null=True)
    diferido = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_chequeras'


class Cheques(models.Model):
    cfecha = models.DateTimeField(blank=True, null=True)
    cbanco = models.CharField(max_length=50, blank=True, null=True)
    cnumero = models.FloatField(blank=True, null=True)
    cvto = models.DateTimeField(blank=True, null=True)
    cmonto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    cautogenerado = models.CharField(max_length=40, blank=True, null=True)
    cdetalle = models.CharField(max_length=50, blank=True, null=True)
    cmoneda = models.SmallIntegerField(blank=True, null=True)
    cestado = models.SmallIntegerField(blank=True, null=True)
    ccliente = models.IntegerField(blank=True, null=True)
    cestadobco = models.SmallIntegerField(blank=True, null=True)
    cnrodepos = models.FloatField(blank=True, null=True)
    ctipo = models.CharField(max_length=2, blank=True, null=True)
    cproveedor = models.IntegerField(blank=True, null=True)
    cpago = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_cheques'


class Clavefactura(models.Model):
    boleta = models.FloatField()
    prefijo = models.SmallIntegerField()
    tipo = models.SmallIntegerField()
    serie = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'dataset_clavefactura'


class Clavefacturab(models.Model):
    boleta = models.IntegerField()
    prefijo = models.SmallIntegerField()
    tipo = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'dataset_clavefacturab'


class Clavefacturac(models.Model):
    boleta = models.IntegerField()
    prefijo = models.SmallIntegerField()
    tipo = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'dataset_clavefacturac'


class Clavefacturad(models.Model):
    boleta = models.IntegerField()
    prefijo = models.SmallIntegerField()
    tipo = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'dataset_clavefacturad'


class Clavefacturae(models.Model):
    boleta = models.IntegerField()
    prefijo = models.SmallIntegerField()
    tipo = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'dataset_clavefacturae'


class Clavefacturaf(models.Model):
    boleta = models.FloatField()
    prefijo = models.SmallIntegerField()
    tipo = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'dataset_clavefacturaf'


class Clavefacturag(models.Model):
    boleta = models.FloatField()
    prefijo = models.SmallIntegerField()
    tipo = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'dataset_clavefacturag'


class Clavefacturah(models.Model):
    boleta = models.FloatField()
    prefijo = models.SmallIntegerField()
    tipo = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'dataset_clavefacturah'


class Claveiibb(models.Model):
    boleta = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dataset_claveiibb'


class Claveorden(models.Model):
    boleta = models.FloatField()

    class Meta:
        managed = False
        db_table = 'dataset_claveorden'


class Clavepreventa(models.Model):
    numero = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dataset_clavepreventa'


class Claverecibo(models.Model):
    boleta = models.FloatField()
    prefijo = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'dataset_claverecibo'


class Claverecibom(models.Model):
    boleta = models.FloatField()

    class Meta:
        managed = False
        db_table = 'dataset_claverecibom'


class Clavevoucher(models.Model):
    voucher = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dataset_clavevoucher'


class Codigocontrol(models.Model):
    keydosificacion = models.CharField(max_length=255, blank=True, null=True)
    codautorizacion = models.CharField(max_length=255, blank=True, null=True)
    fechainicio = models.DateTimeField(blank=True, null=True)
    fechalimite = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_codigocontrol'


class Codigossunat(models.Model):
    numero = models.SmallIntegerField()
    codigo = models.SmallIntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    signo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_codigossunat'


class Concilio(models.Model):
    banco = models.IntegerField(blank=True, null=True)
    documento = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=3, blank=True, null=True)
    monto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_concilio'


class Config(models.Model):
    ktema = models.CharField(max_length=70, blank=True, null=True)
    kdato = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_config'


class Contacompra(models.Model):
    contador = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_contacompra'


class Cuentas(models.Model):
    xcodigo = models.BigIntegerField()
    xnombre = models.CharField(max_length=50, blank=True, null=True)
    xtipo = models.SmallIntegerField(blank=True, null=True)
    xobservaciones = models.TextField(blank=True, null=True)
    xgrupo = models.CharField(max_length=20, blank=True, null=True)
    xmoneda = models.SmallIntegerField(blank=True, null=True)
    xcalculadifpesos = models.CharField(max_length=1, blank=True, null=True)
    xcalculadifdolar = models.CharField(max_length=1, blank=True, null=True)
    xnivel1 = models.CharField(max_length=40, blank=True, null=True)
    presupuesto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    objetivo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    sobregiro = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    alternativo = models.CharField(max_length=30, blank=True, null=True)
    ordinal = models.SmallIntegerField(blank=True, null=True)
    inflacion = models.CharField(max_length=1, blank=True, null=True)
    nombreingles = models.CharField(max_length=50, blank=True, null=True)
    codificada = models.CharField(max_length=1, blank=True, null=True)
    bloqueodirecto = models.CharField(max_length=1, blank=True, null=True)
    manejasocioscom = models.CharField(max_length=1, blank=True, null=True)
    vincular = models.CharField(max_length=1, blank=True, null=True)
    activo = models.CharField(max_length=1, blank=True, null=True)
    brctaref = models.CharField(max_length=150, blank=True, null=True)
    compsaldo = models.CharField(max_length=1, blank=True, null=True)
    xbanco = models.SmallIntegerField(blank=True, null=True)
    xcuentabanco = models.CharField(max_length=30, blank=True, null=True)
    activofijo = models.CharField(max_length=1, blank=True, null=True)
    cuentaniif = models.BigIntegerField(blank=True, null=True)
    aperturaporsocio = models.CharField(max_length=1, blank=True, null=True)
    aplicacierreterceros = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_cuentas'


class Cuentasniif(models.Model):
    xcodigo = models.BigIntegerField()
    xnombre = models.CharField(max_length=50, blank=True, null=True)
    nombreingles = models.CharField(max_length=50, blank=True, null=True)
    xgrupo = models.CharField(max_length=20, blank=True, null=True)
    xnivel1 = models.CharField(max_length=40, blank=True, null=True)
    xobservaciones = models.TextField(blank=True, null=True)
    codificada = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_cuentasniif'


class Cuentasocios(models.Model):
    cuenta = models.BigIntegerField(blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    socio = models.CharField(max_length=1, blank=True, null=True)
    exterior = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_cuentasocios'


class Detallenotasfiscales(models.Model):
    sucursal = models.IntegerField(blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    servicio = models.IntegerField(blank=True, null=True)
    tributa = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_detallenotasfiscales'


class Detreportes(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fila = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=3, blank=True, null=True)
    contenido = models.BigIntegerField(blank=True, null=True)
    texto = models.CharField(max_length=200, blank=True, null=True)
    funcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_detreportes'


class Difcobros(models.Model):
    tipo = models.SmallIntegerField(blank=True, null=True)
    monto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    iva = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    autofactura = models.CharField(max_length=40, blank=True, null=True)
    autocobro = models.CharField(max_length=40, blank=True, null=True)
    cambiofactura = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    cambiocobro = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    contabilizado = models.IntegerField()
    asiento = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_difcobros'


class Difpagos(models.Model):
    tipo = models.SmallIntegerField(blank=True, null=True)
    monto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    iva = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    autofactura = models.CharField(max_length=40, blank=True, null=True)
    autocobro = models.CharField(max_length=40, blank=True, null=True)
    cambiofactura = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    cambiocobro = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    contabilizado = models.IntegerField()
    asiento = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_difpagos'


class Dolar(models.Model):
    ufecha = models.DateTimeField(blank=True, null=True)
    uvalor = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    umoneda = models.SmallIntegerField(blank=True, null=True)
    upizarra = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    paridad = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    usuario = models.CharField(max_length=3, blank=True, null=True)
    utcea = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    utcem = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    utcet = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    utcia = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    utcim = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    utcit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_dolar'


class Dtproperties(models.Model):
    objectid = models.IntegerField(blank=True, null=True)
    property = models.CharField(max_length=64)
    value = models.CharField(max_length=255, blank=True, null=True)
    lvalue = models.TextField(blank=True, null=True)
    version = models.IntegerField()
    uvalue = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_dtproperties'


class Ejercicio(models.Model):
    numero = models.SmallIntegerField()
    comienzo = models.DateTimeField(blank=True, null=True)
    final = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_ejercicio'


class Empresa(models.Model):
    dnombre = models.CharField(max_length=100, blank=True, null=True)
    drazonsocial = models.CharField(max_length=100, blank=True, null=True)
    ddireccion = models.CharField(max_length=100, blank=True, null=True)
    dtelefono = models.CharField(max_length=30, blank=True, null=True)
    drubro = models.CharField(max_length=200, blank=True, null=True)
    dlocalidad = models.CharField(max_length=30, blank=True, null=True)
    dfax = models.CharField(max_length=30, blank=True, null=True)
    dfactura = models.IntegerField(blank=True, null=True)
    druc = models.CharField(max_length=20, blank=True, null=True)
    dcpostal = models.CharField(max_length=20, blank=True, null=True)
    dseguro = models.CharField(max_length=20, blank=True, null=True)
    dprefijo = models.SmallIntegerField(blank=True, null=True)
    dserie = models.CharField(max_length=1, blank=True, null=True)
    dfacturab = models.IntegerField(blank=True, null=True)
    dfacturac = models.IntegerField(blank=True, null=True)
    dfacturae = models.IntegerField(blank=True, null=True)
    drecibo = models.IntegerField(blank=True, null=True)
    fachilea = models.IntegerField(blank=True, null=True)
    fachileb = models.IntegerField(blank=True, null=True)
    ncchilea = models.IntegerField(blank=True, null=True)
    ncchileb = models.IntegerField(blank=True, null=True)
    ndchilea = models.IntegerField(blank=True, null=True)
    ndchileb = models.IntegerField(blank=True, null=True)
    estacion = models.SmallIntegerField(blank=True, null=True)
    replegal = models.CharField(max_length=50, blank=True, null=True)
    dprefijorecibo = models.SmallIntegerField(blank=True, null=True)
    facturaelectronica = models.CharField(max_length=1, blank=True, null=True)
    dinicioact = models.CharField(max_length=10, blank=True, null=True)
    dingresosbrutos = models.CharField(max_length=20, blank=True, null=True)
    nrosat = models.CharField(max_length=10, blank=True, null=True)
    anosat = models.CharField(max_length=10, blank=True, null=True)
    motordoc = models.CharField(max_length=1, blank=True, null=True)
    auditoria = models.CharField(max_length=1, blank=True, null=True)
    nrosatnc = models.CharField(max_length=10, blank=True, null=True)
    anosatnc = models.CharField(max_length=10, blank=True, null=True)
    keydosificacion = models.CharField(max_length=255, blank=True, null=True)
    noautorizacion = models.CharField(max_length=255, blank=True, null=True)
    fechalimiteemision = models.DateTimeField(blank=True, null=True)
    dirfe = models.CharField(max_length=200, blank=True, null=True)
    nores = models.IntegerField(blank=True, null=True)
    fecres = models.DateTimeField(blank=True, null=True)
    sc = models.CharField(max_length=1, blank=True, null=True)
    factureoffice = models.CharField(max_length=1, blank=True, null=True)
    dirfelibros = models.CharField(max_length=200, blank=True, null=True)
    acteco = models.CharField(max_length=50, blank=True, null=True)
    actecoa = models.CharField(max_length=50, blank=True, null=True)
    enviaordencomprafe = models.CharField(max_length=1, blank=True, null=True)
    dnombrechino = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_empresa'


class Factudif(models.Model):
    znumero = models.IntegerField(blank=True, null=True)
    zmoneda = models.SmallIntegerField(blank=True, null=True)
    zcliente = models.IntegerField(blank=True, null=True)
    ztipo = models.SmallIntegerField(blank=True, null=True)
    zitem = models.SmallIntegerField(blank=True, null=True)
    zmonto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    ziva = models.SmallIntegerField(blank=True, null=True)
    zrefer = models.CharField(max_length=10, blank=True, null=True)
    zcarrier = models.CharField(max_length=30, blank=True, null=True)
    zmaster = models.CharField(max_length=40, blank=True, null=True)
    zdate = models.CharField(max_length=30, blank=True, null=True)
    zhouse = models.CharField(max_length=50, blank=True, null=True)
    zposicion = models.CharField(max_length=20, blank=True, null=True)
    zkilos = models.FloatField(blank=True, null=True)
    zbultos = models.IntegerField(blank=True, null=True)
    zvolumen = models.FloatField(blank=True, null=True)
    zorigen = models.CharField(max_length=50, blank=True, null=True)
    zdestino = models.CharField(max_length=50, blank=True, null=True)
    zdetalle = models.CharField(max_length=200, blank=True, null=True)
    ztransporte = models.CharField(max_length=1, blank=True, null=True)
    zclase = models.CharField(max_length=2, blank=True, null=True)
    zllegasale = models.DateTimeField(blank=True, null=True)
    zobs1 = models.CharField(max_length=100, blank=True, null=True)
    zobs2 = models.CharField(max_length=100, blank=True, null=True)
    zobs3 = models.CharField(max_length=100, blank=True, null=True)
    zobs4 = models.CharField(max_length=100, blank=True, null=True)
    zobs5 = models.CharField(max_length=100, blank=True, null=True)
    zcommodity = models.CharField(max_length=50, blank=True, null=True)
    zembarcador = models.CharField(max_length=50, blank=True, null=True)
    zconsignatario = models.CharField(max_length=50, blank=True, null=True)
    zmonedaorigen = models.SmallIntegerField(blank=True, null=True)
    zarbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    zorden = models.CharField(max_length=50, blank=True, null=True)
    zvalororiginal = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    zseguimiento = models.IntegerField(blank=True, null=True)
    zagente = models.CharField(max_length=50, blank=True, null=True)
    zcontrolado = models.CharField(max_length=1, blank=True, null=True)
    zusuario = models.CharField(max_length=3, blank=True, null=True)
    zfechagen = models.DateTimeField(blank=True, null=True)
    zaplicable = models.FloatField(blank=True, null=True)
    zvendedor = models.SmallIntegerField(blank=True, null=True)
    zwr = models.CharField(max_length=100, blank=True, null=True)
    znotas = models.CharField(max_length=100, blank=True, null=True)
    zcambiousdpactado = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    zpagoflete = models.CharField(max_length=1, blank=True, null=True)
    zterminos = models.CharField(max_length=3, blank=True, null=True)
    zfacturado = models.CharField(max_length=1, blank=True, null=True)
    zop = models.CharField(max_length=1, blank=True, null=True)
    nrofolio = models.IntegerField(blank=True, null=True)
    dtefechaorden = models.DateTimeField(blank=True, null=True)
    srazonreforden = models.CharField(max_length=50, blank=True, null=True)
    zfechafacturado = models.DateTimeField(blank=True, null=True)
    zboletafactura = models.CharField(max_length=20, blank=True, null=True)
    zautogenenvase = models.CharField(max_length=50, blank=True, null=True)
    zfechaaprobada = models.DateTimeField(blank=True, null=True)
    area = models.SmallIntegerField(blank=True, null=True)
    jurisdiccion = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_factudif'


class Familias(models.Model):
    codigo = models.SmallIntegerField()
    nombre = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_familias'


class Fechacorte(models.Model):
    fecha = models.DateTimeField()
    fechahasta = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_fechacorte'


class Fedetalle(models.Model):
    encid = models.IntegerField(blank=True, null=True)
    nrolindet = models.SmallIntegerField(blank=True, null=True)
    tpocodigo = models.CharField(max_length=4, blank=True, null=True)
    vlrcodigo = models.CharField(max_length=5, blank=True, null=True)
    indexe = models.SmallIntegerField(blank=True, null=True)
    nmbitem = models.CharField(max_length=250, blank=True, null=True)
    prcotrmon = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    moneda = models.CharField(max_length=3, blank=True, null=True)
    fctconv = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    montoitem = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_fedetalle'


class Feencabezado(models.Model):
    tipodte = models.IntegerField(blank=True, null=True)
    folio = models.CharField(max_length=7, blank=True, null=True)
    fchemis = models.CharField(max_length=10, blank=True, null=True)
    fchvto = models.CharField(max_length=10, blank=True, null=True)
    rutrecep = models.CharField(max_length=30, blank=True, null=True)
    rznsocrecep = models.CharField(max_length=100, blank=True, null=True)
    girorecep = models.CharField(max_length=100, blank=True, null=True)
    dirrecep = models.CharField(max_length=200, blank=True, null=True)
    cmnarecep = models.CharField(max_length=50, blank=True, null=True)
    ciudadrecep = models.CharField(max_length=50, blank=True, null=True)
    mntneto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    mntexe = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tasaiva = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    iva = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    mnttotal = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    docstatus = models.SmallIntegerField(blank=True, null=True)
    servicereference = models.CharField(max_length=80, blank=True, null=True)
    scautogenreference = models.CharField(max_length=40, blank=True, null=True)
    formatpdf = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_feencabezado'


class Feimpresiondetalles(models.Model):
    encid = models.IntegerField(blank=True, null=True)
    personnrolindet = models.SmallIntegerField(blank=True, null=True)
    detpersonafn_01 = models.CharField(max_length=80, blank=True, null=True)
    detpersonafn_02 = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detpersonafn_03 = models.CharField(max_length=3, blank=True, null=True)
    detpersonafn_04 = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_feimpresiondetalles'


class Fepersonalizados(models.Model):
    encid = models.IntegerField(blank=True, null=True)
    dteid = models.IntegerField(blank=True, null=True)
    refdocorden = models.CharField(max_length=50, blank=True, null=True)
    refdocblawb = models.CharField(max_length=50, blank=True, null=True)
    refdocnave = models.CharField(max_length=50, blank=True, null=True)
    refdocpos = models.CharField(max_length=20, blank=True, null=True)
    refdocbultos = models.SmallIntegerField(blank=True, null=True)
    refdockilos = models.FloatField(blank=True, null=True)
    refdocremitente = models.CharField(max_length=50, blank=True, null=True)
    refdocconsignee = models.CharField(max_length=50, blank=True, null=True)
    refdocorigen = models.CharField(max_length=50, blank=True, null=True)
    refdocdestino = models.CharField(max_length=50, blank=True, null=True)
    obsmdadoc = models.CharField(max_length=50, blank=True, null=True)
    obstc = models.FloatField(blank=True, null=True)
    obsnumlts = models.CharField(max_length=255, blank=True, null=True)
    telrecep = models.CharField(max_length=50, blank=True, null=True)
    faxrecep = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    obsln1 = models.CharField(max_length=150, blank=True, null=True)
    obsln2 = models.CharField(max_length=150, blank=True, null=True)
    obsln3 = models.CharField(max_length=150, blank=True, null=True)
    obsln4 = models.CharField(max_length=150, blank=True, null=True)
    obsln5 = models.CharField(max_length=150, blank=True, null=True)
    condpago = models.CharField(max_length=25, blank=True, null=True)
    att = models.CharField(max_length=45, blank=True, null=True)
    tototramoneda = models.FloatField(blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_fepersonalizados'


class Feqbli(models.Model):
    encid = models.IntegerField(blank=True, null=True)
    ordencliente = models.CharField(max_length=80, blank=True, null=True)
    tpodocref = models.CharField(max_length=10, blank=True, null=True)
    servicioid = models.IntegerField(blank=True, null=True)
    qbliitem = models.CharField(max_length=100, blank=True, null=True)
    fchorden = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_feqbli'


class Fereferencia(models.Model):
    encid = models.IntegerField(blank=True, null=True)
    nrolinref = models.SmallIntegerField(blank=True, null=True)
    tpodocref = models.CharField(max_length=3, blank=True, null=True)
    folioref = models.CharField(max_length=30, blank=True, null=True)
    fchref = models.CharField(max_length=15, blank=True, null=True)
    codref = models.CharField(max_length=10, blank=True, null=True)
    razonref = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_fereferencia'


class Feresultado(models.Model):
    encid = models.IntegerField(blank=True, null=True)
    tpodte = models.IntegerField(blank=True, null=True)
    wsresult = models.TextField(blank=True, null=True)
    wsidstatus = models.IntegerField(blank=True, null=True)
    wsstatus = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_feresultado'


class Fetipos(models.Model):
    codigo = models.SmallIntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_fetipos'


class Folioschile(models.Model):
    serie = models.CharField(max_length=1, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_folioschile'


class Foliosdominicana(models.Model):
    codigo = models.SmallIntegerField(blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_foliosdominicana'


class Gruposactivofijo(models.Model):
    codigo = models.SmallIntegerField()
    nombre = models.CharField(max_length=50, blank=True, null=True)
    cuenta = models.IntegerField(blank=True, null=True)
    porcentaje = models.FloatField(blank=True, null=True)
    porcentajeniif = models.FloatField(blank=True, null=True)
    anios = models.SmallIntegerField(blank=True, null=True)
    aniosniif = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_gruposactivofijo'


class Guiadespacho(models.Model):
    boleta = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    importador = models.IntegerField(blank=True, null=True)
    ruc = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=5, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    declaracion = models.CharField(max_length=50, blank=True, null=True)
    fechadeclaracion = models.DateTimeField(blank=True, null=True)
    aduana = models.CharField(max_length=50, blank=True, null=True)
    despacho = models.CharField(max_length=1, blank=True, null=True)
    transportador = models.IntegerField(blank=True, null=True)
    vehiculo = models.CharField(max_length=50, blank=True, null=True)
    patente = models.CharField(max_length=50, blank=True, null=True)
    despachonum = models.CharField(max_length=50, blank=True, null=True)
    ref = models.CharField(max_length=50, blank=True, null=True)
    ubicacion = models.CharField(max_length=150, blank=True, null=True)
    vaport = models.CharField(max_length=80, blank=True, null=True)
    observaciones = models.CharField(max_length=300, blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    choferruc = models.CharField(max_length=30, blank=True, null=True)
    chofernombre = models.CharField(max_length=50, blank=True, null=True)
    ciudaddestino = models.CharField(max_length=5, blank=True, null=True)
    direcciondestino = models.CharField(max_length=50, blank=True, null=True)
    comunadestino = models.CharField(max_length=30, blank=True, null=True)
    vapor = models.CharField(max_length=50, blank=True, null=True)
    facturable = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_guiadespacho'


class Guiadespachodetalle(models.Model):
    modo = models.CharField(max_length=2, blank=True, null=True)
    embarque = models.IntegerField(blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    tipo = models.CharField(max_length=30, blank=True, null=True)
    mercaderia = models.CharField(max_length=80, blank=True, null=True)
    peso = models.FloatField(blank=True, null=True)
    cif = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_guiadespachodetalle'


class Historia(models.Model):
    htipo = models.SmallIntegerField(blank=True, null=True)
    hboleta = models.CharField(max_length=20, blank=True, null=True)
    hfechamov = models.DateTimeField(blank=True, null=True)
    hcodigo = models.SmallIntegerField(blank=True, null=True)
    hiva = models.FloatField(blank=True, null=True)
    hprecio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    hmoneda = models.SmallIntegerField(blank=True, null=True)
    hautogen = models.CharField(max_length=40, blank=True, null=True)
    hcambio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    hserie = models.CharField(max_length=1, blank=True, null=True)
    hprefijo = models.CharField(max_length=10, blank=True, null=True)
    hembarque = models.CharField(max_length=15, blank=True, null=True)
    hposicion = models.CharField(max_length=20, blank=True, null=True)
    heditado = models.CharField(max_length=100, blank=True, null=True)
    harea = models.SmallIntegerField(blank=True, null=True)
    hcantidad = models.FloatField(blank=True, null=True)
    htipogasto = models.CharField(max_length=30, blank=True, null=True)
    hpago = models.CharField(max_length=1, blank=True, null=True)
    hmontooriginal = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    hmonedaoriginal = models.SmallIntegerField(blank=True, null=True)
    hparidad = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    hautogenlink = models.CharField(max_length=40, blank=True, null=True)
    hpinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    hnotas = models.CharField(max_length=100, blank=True, null=True)
    harbitrajeoriginal = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    hautogenenvase = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_historia'


class Historiaimpbrasil(models.Model):
    autogen = models.CharField(max_length=40, blank=True, null=True)
    cliente = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    porcentaje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    monto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_historiaimpbrasil'


class Impucompras(models.Model):
    autogen = models.CharField(max_length=40, blank=True, null=True)
    tipo = models.SmallIntegerField(blank=True, null=True)
    serie = models.CharField(max_length=1, blank=True, null=True)
    prefijo = models.SmallIntegerField(blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    cliente = models.IntegerField(blank=True, null=True)
    monto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    autofac = models.CharField(max_length=40, blank=True, null=True)
    parteiva = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    montorg = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    montoriva = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    montorib = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    montorsuss = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    montootros = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    porcentajerg = models.FloatField(blank=True, null=True)
    porcentajeriva = models.FloatField(blank=True, null=True)
    porcentajerib = models.FloatField(blank=True, null=True)
    porcentajersuss = models.FloatField(blank=True, null=True)
    porcentajeotros = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_impucompras'


class Impuestosbrasil(models.Model):
    nombre = models.CharField(max_length=20, blank=True, null=True)
    porcentaje = models.FloatField(blank=True, null=True)
    cuenta = models.BigIntegerField(blank=True, null=True)
    cuenta2 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_impuestosbrasil'


class Impuordenes(models.Model):
    orden = models.IntegerField(blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    cliente = models.IntegerField(blank=True, null=True)
    monto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    autofac = models.CharField(max_length=40, blank=True, null=True)
    prefijo = models.SmallIntegerField(blank=True, null=True)
    serie = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_impuordenes'


class Impuvtas(models.Model):
    autogen = models.CharField(max_length=40, blank=True, null=True)
    tipo = models.SmallIntegerField(blank=True, null=True)
    serie = models.CharField(max_length=1, blank=True, null=True)
    prefijo = models.SmallIntegerField(blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    cliente = models.IntegerField(blank=True, null=True)
    monto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    autofac = models.CharField(max_length=40, blank=True, null=True)
    parteiva = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    montorg = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    montoriva = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    montorib = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    montorsuss = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    montootros = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    porcentajerg = models.FloatField(blank=True, null=True)
    porcentajeriva = models.FloatField(blank=True, null=True)
    porcentajerib = models.FloatField(blank=True, null=True)
    porcentajersuss = models.FloatField(blank=True, null=True)
    porcentajeotros = models.FloatField(blank=True, null=True)
    anticipo = models.CharField(max_length=1, blank=True, null=True)
    fechaimpu = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_impuvtas'


class Infofactura(models.Model):
    autogenerado = models.CharField(max_length=40, blank=True, null=True)
    referencia = models.CharField(max_length=10, blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    transportista = models.CharField(max_length=20, blank=True, null=True)
    vuelo = models.CharField(max_length=30, blank=True, null=True)
    master = models.CharField(max_length=20, blank=True, null=True)
    house = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.CharField(max_length=10, blank=True, null=True)
    commodity = models.CharField(max_length=50, blank=True, null=True)
    kilos = models.FloatField(blank=True, null=True)
    volumen = models.FloatField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    ordencliente = models.CharField(max_length=50, blank=True, null=True)
    origen = models.CharField(max_length=30, blank=True, null=True)
    destino = models.CharField(max_length=30, blank=True, null=True)
    consigna = models.CharField(max_length=50, blank=True, null=True)
    embarca = models.CharField(max_length=50, blank=True, null=True)
    agente = models.CharField(max_length=50, blank=True, null=True)
    posicion = models.CharField(max_length=20, blank=True, null=True)
    wr = models.CharField(max_length=100, blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    pagoflete = models.CharField(max_length=1, blank=True, null=True)
    tipoembarque = models.CharField(max_length=1, blank=True, null=True)
    etd = models.DateTimeField(blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_infofactura'

    def get_id(self):
        lista=Infofactura.objects.last()
        return int(lista.id+1)


class Iva(models.Model):
    xporcentaje = models.CharField(max_length=8, blank=True, null=True)
    xctavta = models.BigIntegerField(blank=True, null=True)
    xctacom = models.BigIntegerField(blank=True, null=True)
    xfechavigencia = models.DateTimeField(blank=True, null=True)
    xporcentajeant = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_iva'


class Mensajes(models.Model):
    autogenerado = models.CharField(max_length=30)
    texto1 = models.CharField(max_length=100, blank=True, null=True)
    texto2 = models.CharField(max_length=100, blank=True, null=True)
    texto3 = models.CharField(max_length=100, blank=True, null=True)
    texto4 = models.CharField(max_length=100, blank=True, null=True)
    texto5 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_mensajes'


class Mensajesfactura(models.Model):
    codigo = models.SmallIntegerField()
    nombre = models.CharField(max_length=30, blank=True, null=True)
    texto1 = models.CharField(max_length=100, blank=True, null=True)
    texto2 = models.CharField(max_length=100, blank=True, null=True)
    texto3 = models.CharField(max_length=100, blank=True, null=True)
    texto4 = models.CharField(max_length=100, blank=True, null=True)
    texto5 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_mensajesfactura'


class Movims(models.Model):
    mtipo = models.SmallIntegerField(blank=True, null=True)
    mfechamov = models.DateTimeField(blank=True, null=True)
    mboleta = models.CharField(max_length=20, blank=True, null=True)
    mmonto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    miva = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    mtotal = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    msobretasa = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    msaldo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    mvtomov = models.DateTimeField(blank=True, null=True)
    mmoneda = models.SmallIntegerField(blank=True, null=True)
    mvendedor = models.SmallIntegerField(blank=True, null=True)
    mcobrador = models.SmallIntegerField(blank=True, null=True)
    mdetalle = models.CharField(max_length=200, blank=True, null=True)
    mcliente = models.IntegerField(blank=True, null=True)
    mnombre = models.CharField(max_length=50, blank=True, null=True)
    mdireccion = models.CharField(max_length=40, blank=True, null=True)
    mcambio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    mnombremov = models.CharField(max_length=20, blank=True, null=True)
    mautogen = models.CharField(max_length=40, blank=True, null=True)
    mseccion = models.SmallIntegerField(blank=True, null=True)
    mserie = models.CharField(max_length=1, blank=True, null=True)
    mprefijo = models.CharField(max_length=10, blank=True, null=True)
    mactivo = models.CharField(max_length=1, blank=True, null=True)
    mposicion = models.CharField(max_length=20, blank=True, null=True)
    mmesimpu = models.SmallIntegerField(blank=True, null=True)
    manoimpu = models.SmallIntegerField(blank=True, null=True)
    mmonedaoriginal = models.SmallIntegerField(blank=True, null=True)
    marbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    mmontooriginal = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    mctaorden = models.CharField(max_length=1, blank=True, null=True)
    mcliorden = models.IntegerField(blank=True, null=True)
    mvoucher = models.IntegerField(blank=True, null=True)
    mruc = models.CharField(max_length=30, blank=True, null=True)
    mimpreso = models.CharField(max_length=1, blank=True, null=True)
    mfechadoc = models.DateTimeField(blank=True, null=True)
    minialta = models.CharField(max_length=3, blank=True, null=True)
    miniprint = models.CharField(max_length=3, blank=True, null=True)
    mparidad = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    msucursal = models.SmallIntegerField(blank=True, null=True)
    electronica = models.CharField(max_length=1, blank=True, null=True)
    mnropapel = models.IntegerField(blank=True, null=True)
    midfiscal = models.CharField(max_length=30, blank=True, null=True)
    liquidada = models.CharField(max_length=1, blank=True, null=True)
    mdetallepagada = models.CharField(max_length=100, blank=True, null=True)
    maprobada = models.CharField(max_length=1, blank=True, null=True)
    tccorreccion = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    moncorreccion = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    codigocontrol = models.CharField(max_length=50, blank=True, null=True)
    cainro = models.CharField(max_length=50, blank=True, null=True)
    caivto = models.DateTimeField(blank=True, null=True)
    mnombre2 = models.CharField(max_length=50, blank=True, null=True)
    numentregafemsa = models.CharField(max_length=50, blank=True, null=True)
    numproveedorfemsa = models.CharField(max_length=50, blank=True, null=True)
    remisionfemsa = models.CharField(max_length=50, blank=True, null=True)
    sociedadfemsa = models.CharField(max_length=50, blank=True, null=True)
    monedadocfemsa = models.CharField(max_length=50, blank=True, null=True)
    ponumber = models.CharField(max_length=100, blank=True, null=True)
    cae = models.CharField(max_length=50, blank=True, null=True)
    fechavtocae = models.DateTimeField(blank=True, null=True)
    fleteinternacional = models.CharField(max_length=2, blank=True, null=True)
    lugarprestacionservicio = models.CharField(max_length=5, blank=True, null=True)
    caimonto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    reembolsable = models.CharField(max_length=1, blank=True, null=True)
    tipocomprobante = models.SmallIntegerField(blank=True, null=True)
    tiposustento = models.SmallIntegerField(blank=True, null=True)
    foliofeactualizado = models.CharField(max_length=1, blank=True, null=True)
    mcodref = models.CharField(max_length=10, blank=True, null=True)
    mrazonref = models.CharField(max_length=40, blank=True, null=True)
    noautorizacion = models.CharField(max_length=255, blank=True, null=True)
    fechalimiteemision = models.DateTimeField(blank=True, null=True)
    ivanorecuperable = models.CharField(max_length=1, blank=True, null=True)
    formapago = models.SmallIntegerField(blank=True, null=True)
    fe_uuid = models.CharField(max_length=50, blank=True, null=True)
    fe_idcontrol = models.CharField(max_length=50, blank=True, null=True)
    recuperodegastos = models.CharField(max_length=2, blank=True, null=True)
    jurisdiccion = models.SmallIntegerField(blank=True, null=True)
    eticket = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_movims'

    def get_id(self):
        mov=Movims.objects.last()
        return int(mov.id+1)

class Niveles(models.Model):
    numero = models.BigIntegerField()
    tipo = models.CharField(max_length=10, blank=True, null=True)
    capitulo = models.CharField(max_length=40, blank=True, null=True)
    capituloingles = models.CharField(max_length=40, blank=True, null=True)
    alternativo = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_niveles'


class Nivelesniif(models.Model):
    numero = models.BigIntegerField()
    tipo = models.CharField(max_length=10, blank=True, null=True)
    capitulo = models.CharField(max_length=40, blank=True, null=True)
    capituloingles = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_nivelesniif'


class Notas(models.Model):
    numero = models.IntegerField()
    fecha = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_notas'


class Notasfiscales(models.Model):
    sucursal = models.IntegerField(blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    cliente = models.IntegerField(blank=True, null=True)
    neto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    iss = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    total = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    condicion = models.CharField(max_length=50, blank=True, null=True)
    alicuota = models.FloatField(blank=True, null=True)
    inicial = models.CharField(max_length=3, blank=True, null=True)
    activa = models.CharField(max_length=1, blank=True, null=True)
    fechaservicio = models.DateTimeField(blank=True, null=True)
    vto = models.DateTimeField(blank=True, null=True)
    duplicata = models.CharField(max_length=10, blank=True, null=True)
    procesada = models.CharField(max_length=1, blank=True, null=True)
    aplicable = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    asiento = models.FloatField(blank=True, null=True)
    detalle1 = models.CharField(max_length=50, blank=True, null=True)
    detalle2 = models.CharField(max_length=50, blank=True, null=True)
    detalle3 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_notasfiscales'


class Observacionescae(models.Model):
    autogenerado = models.CharField(max_length=40, blank=True, null=True)
    codigo = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_observacionescae'


class Ordenes(models.Model):
    mboleta = models.IntegerField()
    mfechamov = models.DateTimeField(blank=True, null=True)
    mmonto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    mmoneda = models.SmallIntegerField(blank=True, null=True)
    mdetalle = models.CharField(max_length=200, blank=True, null=True)
    mcliente = models.IntegerField(blank=True, null=True)
    mnombre = models.CharField(max_length=40, blank=True, null=True)
    mactiva = models.CharField(max_length=1, blank=True, null=True)
    mcaja = models.BigIntegerField(blank=True, null=True)
    masiento = models.CharField(max_length=30, blank=True, null=True)
    monedaefec = models.SmallIntegerField(blank=True, null=True)
    montoefec = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    mautogenmovims = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_ordenes'


class Plan(models.Model):
    numero = models.SmallIntegerField()
    nombre = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_plan'


class Plan8(models.Model):
    numero = models.SmallIntegerField()
    nombre = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_plan8'


class Planniif(models.Model):
    numero = models.SmallIntegerField()
    nombre = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_planniif'


class Posiciones(models.Model):
    posicion = models.CharField(max_length=20)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    alternativo = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_posiciones'


class Relacionniif(models.Model):
    xcodigoniif = models.BigIntegerField(blank=True, null=True)
    xcodigocuenta = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_relacionniif'


class Resguardos(models.Model):
    rautogen = models.CharField(max_length=40, blank=True, null=True)
    rcliente = models.IntegerField(blank=True, null=True)
    rserie = models.CharField(max_length=1, blank=True, null=True)
    rnumero = models.CharField(max_length=20, blank=True, null=True)
    rmoneda = models.IntegerField(blank=True, null=True)
    robs = models.CharField(max_length=100, blank=True, null=True)
    rfecha = models.DateTimeField(blank=True, null=True)
    rvto = models.DateTimeField(blank=True, null=True)
    raceptado = models.IntegerField(blank=True, null=True)
    rtipocambio = models.FloatField(blank=True, null=True)
    rtotal = models.FloatField(blank=True, null=True)
    rescontingencia = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_resguardos'


class Retencionesiibb(models.Model):
    autogenerado = models.CharField(max_length=40, blank=True, null=True)
    prefijo = models.IntegerField(blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    documento = models.CharField(max_length=40, blank=True, null=True)
    neto = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    alicuota = models.FloatField(blank=True, null=True)
    retenido = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    enviado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_retencionesiibb'


class Seccion(models.Model):
    zcod = models.SmallIntegerField()
    znomsec = models.CharField(max_length=50, blank=True, null=True)
    zobserv = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_seccion'


class Sped(models.Model):
    inscricaocadastro = models.CharField(max_length=10, blank=True, null=True)
    codigocadastral = models.CharField(max_length=30, blank=True, null=True)
    uf = models.CharField(max_length=5, blank=True, null=True)
    nire = models.CharField(max_length=25, blank=True, null=True)
    numordenactual = models.IntegerField(blank=True, null=True)
    naturezalibro = models.CharField(max_length=150, blank=True, null=True)
    dteconstitutivos = models.DateTimeField(blank=True, null=True)
    dteconvercion = models.DateTimeField(blank=True, null=True)
    respnome = models.CharField(max_length=100, blank=True, null=True)
    cpf = models.CharField(max_length=50, blank=True, null=True)
    respcategoria = models.CharField(max_length=50, blank=True, null=True)
    municipio = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_sped'


class Sustentos(models.Model):
    codigo = models.CharField(max_length=20, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_sustentos'


class Tipocli(models.Model):
    dcodigo = models.SmallIntegerField()
    dnomtip = models.CharField(max_length=50, blank=True, null=True)
    dtipofac = models.CharField(max_length=1, blank=True, null=True)
    dsobretasa = models.CharField(max_length=1, blank=True, null=True)
    dpuntoventa = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_tipocli'


class Tipocliretencion(models.Model):
    codigo = models.SmallIntegerField(blank=True, null=True)
    cuenta = models.BigIntegerField(blank=True, null=True)
    aplica = models.CharField(max_length=1, blank=True, null=True)
    comentario = models.CharField(max_length=50, blank=True, null=True)
    porcentaje = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_tipocliretencion'


class Tiposcompproveedor(models.Model):
    codigo = models.CharField(max_length=20, blank=True, null=True)
    establecimiento = models.CharField(max_length=20, blank=True, null=True)
    serie = models.CharField(max_length=10, blank=True, null=True)
    numerodesde = models.IntegerField(blank=True, null=True)
    numerohasta = models.IntegerField(blank=True, null=True)
    autorizacion = models.CharField(max_length=30, blank=True, null=True)
    emision = models.DateTimeField(blank=True, null=True)
    vencimiento = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_tiposcompproveedor'


class Tiposcompretencion(models.Model):
    codigo = models.CharField(max_length=20, blank=True, null=True)
    establecimiento = models.CharField(max_length=20, blank=True, null=True)
    serie = models.CharField(max_length=10, blank=True, null=True)
    numerodesde = models.IntegerField(blank=True, null=True)
    numerohasta = models.IntegerField(blank=True, null=True)
    autorizacion = models.CharField(max_length=30, blank=True, null=True)
    emision = models.DateTimeField(blank=True, null=True)
    vencimiento = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_tiposcompretencion'


class Tiposcomprobantes(models.Model):
    codigo = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    secuencia = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    comportamiento = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_tiposcomprobantes'


class Tiposcomprobantesustentos(models.Model):
    idtc = models.SmallIntegerField(blank=True, null=True)
    idsustento = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_tiposcomprobantesustentos'


class Tiposrenta(models.Model):
    codigo = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_tiposrenta'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ExpmaritAnulados(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expmarit_anulados'


class ExpmaritAttachhijo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True,
                                         null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_attachhijo'


class ExpmaritAttachmadre(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_attachmadre'


class ExpmaritBookenv(models.Model):
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
    contactoterminal = models.CharField(db_column='ContactoTerminal', max_length=30, blank=True,
                                        null=True)  # Field name made lowercase.
    bandera = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expmarit_booking'


class ExpmaritCargaaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True)
    fechaembarque = models.DateTimeField(blank=True, null=True)
    cbm = models.FloatField(blank=True, null=True)
    mercaderia = models.TextField(blank=True, null=True)
    marcas = models.CharField(db_column='Marcas', max_length=150, blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=15, blank=True,
                                     null=True)  # Field name made lowercase.
    sobredimensionada = models.CharField(db_column='Sobredimensionada', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.

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
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(max_length=15, blank=True, null=True)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True,
                                  null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_conexaerea'


class ExpmaritConexreserva(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vapor = models.CharField(max_length=30, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(max_length=10, blank=True, null=True)
    modo = models.CharField(max_length=15, blank=True, null=True)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True,
                                  null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True,
                                   null=True)  # Field name made lowercase.

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
    vaporcli2 = models.CharField(db_column='Vaporcli2', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
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
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    booking = models.CharField(max_length=30, blank=True, null=True)
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=250, blank=True,
                                       null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=250, blank=True,
                                          null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=19, decimal_places=4, blank=True,
                                           null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    depcontenedoringreso = models.SmallIntegerField(db_column='DepContenedorIngreso', blank=True,
                                                    null=True)  # Field name made lowercase.
    depcontenedorvacios = models.SmallIntegerField(db_column='DepContenedorVacios', blank=True,
                                                   null=True)  # Field name made lowercase.
    agenteportuario = models.IntegerField(db_column='AgentePortuario', blank=True,
                                          null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    deadborrador = models.DateTimeField(db_column='DeadBorrador', blank=True, null=True)  # Field name made lowercase.
    deaddocumentos = models.DateTimeField(db_column='DeadDocumentos', blank=True,
                                          null=True)  # Field name made lowercase.
    deadentrega = models.DateTimeField(db_column='DeadEntrega', blank=True, null=True)  # Field name made lowercase.
    deadliberacion = models.DateTimeField(db_column='DeadLiberacion', blank=True,
                                          null=True)  # Field name made lowercase.
    retiravacio = models.DateTimeField(db_column='RetiraVacio', blank=True, null=True)  # Field name made lowercase.
    retiralleno = models.DateTimeField(db_column='RetiraLleno', blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=250, blank=True,
                                    null=True)  # Field name made lowercase.
    imprimiobl = models.CharField(db_column='ImprimioBL', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    hblcorp = models.IntegerField(db_column='HBLCorp', blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    datosnotificante = models.CharField(db_column='DatosNotificante', max_length=250, blank=True,
                                        null=True)  # Field name made lowercase.
    contactoemergencia = models.CharField(db_column='ContactoEmergencia', max_length=100, blank=True,
                                          null=True)  # Field name made lowercase.
    numerocomunicacion = models.CharField(db_column='NumeroComunicacion', max_length=50, blank=True,
                                          null=True)  # Field name made lowercase.
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    fechaentrega = models.DateTimeField(db_column='FechaEntrega', blank=True, null=True)  # Field name made lowercase.
    aquienentrega = models.CharField(db_column='aQuienEntrega', max_length=30, blank=True,
                                     null=True)  # Field name made lowercase.
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    salidasim = models.DateTimeField(db_column='SalidaSIM', blank=True, null=True)  # Field name made lowercase.
    presentasim = models.DateTimeField(db_column='PresentaSIM', blank=True, null=True)  # Field name made lowercase.
    cierresim = models.DateTimeField(db_column='CierreSIM', blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=50, blank=True,
                                       null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=50, blank=True,
                                         null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=50, blank=True,
                                      null=True)  # Field name made lowercase.
    imprimioorig = models.CharField(db_column='ImprimioOrig', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    enviointtrabk = models.CharField(db_column='EnvioInttraBK', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    enviointtrasi = models.CharField(db_column='EnvioInttraSI', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    maerskbk = models.CharField(db_column='MaerskBK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    maersksi = models.CharField(db_column='MaerskSI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tipobl = models.CharField(db_column='TipoBL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    fechacutoff = models.DateTimeField(db_column='FechaCutOff', blank=True, null=True)  # Field name made lowercase.
    horacutoff = models.CharField(db_column='HoraCutOff', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    fecharetiromercaderia = models.DateTimeField(db_column='FechaRetiroMercaderia', blank=True,
                                                 null=True)  # Field name made lowercase.
    fechainiciostacking = models.DateTimeField(db_column='FechaInicioStacking', blank=True,
                                               null=True)  # Field name made lowercase.
    horainiciostacking = models.CharField(db_column='HoraInicioStacking', max_length=30, blank=True,
                                          null=True)  # Field name made lowercase.
    fechafinstacking = models.DateTimeField(db_column='FechaFinStacking', blank=True,
                                            null=True)  # Field name made lowercase.
    horafinstacking = models.CharField(db_column='HoraFinStacking', max_length=30, blank=True,
                                       null=True)  # Field name made lowercase.
    emisionbl = models.DateTimeField(db_column='EmisionBL', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    envioeasipassbk = models.CharField(db_column='EnvioEASIPASSBK', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    envioeasipasssi = models.CharField(db_column='EnvioEASIPASSSI', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    demora = models.SmallIntegerField(db_column='Demora', blank=True, null=True)  # Field name made lowercase.
    valordemoravta = models.DecimalField(db_column='ValorDemoraVTA', max_digits=19, decimal_places=4, blank=True,
                                         null=True)  # Field name made lowercase.
    valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=19, decimal_places=4, blank=True,
                                         null=True)  # Field name made lowercase.
    truckerarrivaltime = models.CharField(db_column='TruckerArrivalTime', max_length=30, blank=True,
                                          null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    fechacutoffvgm = models.DateTimeField(db_column='FechaCutOffVGM', blank=True,
                                          null=True)  # Field name made lowercase.
    horacutoffvgm = models.CharField(db_column='HoraCutOffVGM', max_length=30, blank=True,
                                     null=True)  # Field name made lowercase.
    emitebloriginal = models.CharField(db_column='EmiteBLOriginal', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.DateTimeField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_embarqueaereo'


class ExpmaritEntregadoc(models.Model):
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
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', max_length=40, blank=True,
                                            null=True)  # Field name made lowercase.
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', max_length=40, blank=True,
                                           null=True)  # Field name made lowercase.
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crtnumero = models.CharField(db_column='CRTNumero', max_length=40, blank=True,
                                 null=True)  # Field name made lowercase.
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', max_length=40, blank=True,
                                               null=True)  # Field name made lowercase.
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    micdtanumero = models.CharField(db_column='MicDtaNumero', max_length=40, blank=True,
                                    null=True)  # Field name made lowercase.
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    papeletanumero = models.CharField(db_column='PapeletaNumero', max_length=40, blank=True,
                                      null=True)  # Field name made lowercase.
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', max_length=40, blank=True,
                                              null=True)  # Field name made lowercase.
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', max_length=40, blank=True,
                                            null=True)  # Field name made lowercase.
    certorigennumero = models.CharField(db_column='CertOrigenNumero', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    certseguronumero = models.CharField(db_column='CertSeguroNumero', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', max_length=40, blank=True,
                                          null=True)  # Field name made lowercase.
    detotros3 = models.CharField(db_column='DetOtros3', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    detotros4 = models.CharField(db_column='DetOtros4', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_entregadoc'


class ExpmaritEnvases(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=5, blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    movimiento = models.CharField(max_length=10, blank=True, null=True)
    terminos = models.CharField(max_length=5, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    marcas = models.CharField(max_length=250, blank=True, null=True)
    precinto = models.CharField(max_length=100, blank=True, null=True)
    tara = models.FloatField(blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    envase = models.CharField(db_column='Envase', max_length=15, blank=True, null=True)  # Field name made lowercase.
    bultos = models.IntegerField(blank=True, null=True)
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(max_length=100, blank=True, null=True)
    volumen = models.FloatField(blank=True, null=True)
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    temperatura = models.FloatField(db_column='Temperatura', blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    ventilacion = models.CharField(db_column='Ventilacion', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.
    genset = models.CharField(db_column='GenSet', max_length=1, blank=True, null=True)  # Field name made lowercase.
    atmosferacontrolada = models.CharField(db_column='AtmosferaControlada', max_length=1, blank=True,
                                           null=True)  # Field name made lowercase.
    consolidacion = models.SmallIntegerField(db_column='Consolidacion', blank=True,
                                             null=True)  # Field name made lowercase.
    tipoventilacion = models.CharField(db_column='TipoVentilacion', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    pesovgm = models.FloatField(db_column='PesoVGM', blank=True, null=True)  # Field name made lowercase.
    humedad = models.SmallIntegerField(db_column='Humedad', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_envases'


class ExpmaritFaxes(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expmarit_faxes'


class ExpmaritFisico(models.Model):
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
    detalle2 = models.CharField(max_length=50, blank=True, null=True)
    cliente = models.IntegerField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_fisico'


class ExpmaritGastoshijos(models.Model):
    cliente = models.IntegerField(blank=True, null=True)
    codigo = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True,
                                null=True)  # Field name made lowercase.
    statushijos = models.SmallIntegerField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    movimiento = models.CharField(db_column='Movimiento', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_gastoshijos'


class ExpmaritGuiasgrabadas(models.Model):
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
    paisdestino = models.CharField(db_column='PaisDestino', max_length=35, blank=True,
                                   null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=3, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=3, blank=True,
                                     null=True)  # Field name made lowercase.
    awb = models.CharField(db_column='AWB', max_length=40, blank=True, null=True)  # Field name made lowercase.
    hawb = models.CharField(db_column='HAWB', max_length=50, blank=True, null=True)  # Field name made lowercase.
    totalkilos = models.FloatField(db_column='TotalKilos', blank=True, null=True)  # Field name made lowercase.
    totalpaquetes = models.IntegerField(db_column='TotalPaquetes', blank=True, null=True)  # Field name made lowercase.
    tipodocumento = models.CharField(db_column='TipoDocumento', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    consolidado = models.IntegerField(db_column='Consolidado', blank=True, null=True)  # Field name made lowercase.
    mensaje1 = models.IntegerField(db_column='Mensaje1', blank=True, null=True)  # Field name made lowercase.
    mensaje2 = models.IntegerField(db_column='Mensaje2', blank=True, null=True)  # Field name made lowercase.
    label6 = models.CharField(db_column='Label6', max_length=50, blank=True, null=True)  # Field name made lowercase.
    texto = models.TextField(db_column='Texto', blank=True, null=True)  # Field name made lowercase.
    consigna6 = models.CharField(db_column='Consigna6', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    consigna7 = models.CharField(db_column='Consigna7', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    consigna8 = models.CharField(db_column='Consigna8', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    precarriage = models.CharField(db_column='PreCarriage', max_length=35, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_guiasgrabadas'


class ExpmaritGuiasgrabadas2(models.Model):
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
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    servicio = models.CharField(db_column='Servicio', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    prepaid = models.CharField(db_column='Prepaid', max_length=10, blank=True, null=True)  # Field name made lowercase.
    collect = models.CharField(db_column='Collect', max_length=10, blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_guiasgrabadas3'


class ExpmaritMadresgrabadas(models.Model):
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
    pagoflete = models.CharField(db_column='Pagoflete', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    volumen = models.FloatField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    cotizacion = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    aduana = models.CharField(max_length=30, blank=True, null=True)
    profitage = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tarifapl = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=20, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
    envioedi = models.CharField(max_length=1, blank=True, null=True)
    nroreferedi = models.IntegerField(blank=True, null=True)
    ciep = models.CharField(max_length=15, blank=True, null=True)
    armador = models.IntegerField(blank=True, null=True)
    operacion = models.CharField(max_length=25, blank=True, null=True)
    plfacturado = models.CharField(max_length=1, blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    enviointtrabk = models.CharField(db_column='EnvioInttraBK', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    enviointtrasi = models.CharField(db_column='EnvioInttraSI', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    maerskbk = models.CharField(db_column='MaerskBK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    maersksi = models.CharField(db_column='MaerskSI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    esagente = models.CharField(db_column='esAgente', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    tipobl = models.CharField(db_column='TipoBL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    deposito = models.SmallIntegerField(db_column='Deposito', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_reservas'


class ExpmaritServiceaereo(models.Model):
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
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_serviceaereo'


class ExpmaritServireserva(models.Model):
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
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_servireserva'


class ExpmaritTraceop(models.Model):
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=250, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expmarit_traceop'


class ExportAnulados(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'export_anulados'


class ExportAttachhijo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True,
                                         null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_attachhijo'


class ExportAttachmadre(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_attachmadre'


class ExportCargaaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True)
    fechaembarque = models.DateTimeField(blank=True, null=True)
    tarifa = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    aplicable = models.FloatField(blank=True, null=True)
    unidad = models.CharField(db_column='Unidad', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    tara = models.FloatField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_cargaaerea'


class ExportClaveguia(models.Model):
    awb = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'export_claveguia'


class ExportClavehawb(models.Model):
    hawb = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'export_clavehawb'


class ExportClaveposicion(models.Model):
    posicion = models.CharField(max_length=15)
    numeroorden = models.SmallIntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_claveposicion'


class ExportConexaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vuelo = models.CharField(max_length=30, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    ciavuelo = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(max_length=10, blank=True, null=True)
    modo = models.CharField(max_length=15, blank=True, null=True)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True,
                                  null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_conexaerea'


class ExportConexreserva(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vuelo = models.CharField(max_length=30, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    ciavuelo = models.CharField(max_length=2, blank=True, null=True)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True,
                                  null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True,
                                   null=True)  # Field name made lowercase.

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
    hawbtext = models.CharField(db_column='HawbText', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=250, blank=True,
                                       null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=250, blank=True,
                                          null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    mercaderia = models.TextField(db_column='Mercaderia', blank=True, null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    datosnotificante = models.CharField(db_column='DatosNotificante', max_length=250, blank=True,
                                        null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=19, decimal_places=4, blank=True,
                                           null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    arbitrajecass = models.DecimalField(db_column='ArbitrajeCASS', max_digits=19, decimal_places=4, blank=True,
                                        null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=250, blank=True,
                                    null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    servicelevel = models.CharField(max_length=20, blank=True, null=True)
    serviceleveltype = models.CharField(max_length=20, blank=True, null=True)
    stthawb = models.CharField(max_length=30, blank=True, null=True)
    sttawb = models.CharField(max_length=30, blank=True, null=True)
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    fechaentrega = models.DateTimeField(db_column='FechaEntrega', blank=True, null=True)  # Field name made lowercase.
    aquienentrega = models.CharField(db_column='aQuienEntrega', max_length=30, blank=True,
                                     null=True)  # Field name made lowercase.
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=50, blank=True,
                                       null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=50, blank=True,
                                         null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=50, blank=True,
                                      null=True)  # Field name made lowercase.
    deposito = models.SmallIntegerField(db_column='Deposito', blank=True, null=True)  # Field name made lowercase.
    autogenfletecpa = models.CharField(db_column='AutogenFleteCPA', max_length=50, blank=True,
                                       null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    envioiata = models.CharField(db_column='EnvioIATA', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    documentos = models.CharField(db_column='Documentos', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.DateTimeField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_embarqueaereo'


class ExportEntregadoc(models.Model):
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
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', max_length=40, blank=True,
                                            null=True)  # Field name made lowercase.
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', max_length=40, blank=True,
                                           null=True)  # Field name made lowercase.
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crtnumero = models.CharField(db_column='CRTNumero', max_length=40, blank=True,
                                 null=True)  # Field name made lowercase.
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', max_length=40, blank=True,
                                               null=True)  # Field name made lowercase.
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    micdtanumero = models.CharField(db_column='MicDtaNumero', max_length=40, blank=True,
                                    null=True)  # Field name made lowercase.
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    papeletanumero = models.CharField(db_column='PapeletaNumero', max_length=40, blank=True,
                                      null=True)  # Field name made lowercase.
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', max_length=40, blank=True,
                                              null=True)  # Field name made lowercase.
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', max_length=40, blank=True,
                                            null=True)  # Field name made lowercase.
    certorigennumero = models.CharField(db_column='CertOrigenNumero', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    certseguronumero = models.CharField(db_column='CertSeguroNumero', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', max_length=40, blank=True,
                                          null=True)  # Field name made lowercase.
    detotros3 = models.CharField(db_column='DetOtros3', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    detotros4 = models.CharField(db_column='DetOtros4', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_entregadoc'


class ExportFaxes(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_faxes'


class ExportGastoshijos(models.Model):
    cliente = models.IntegerField(blank=True, null=True)
    codigo = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True,
                                null=True)  # Field name made lowercase.
    statushijos = models.SmallIntegerField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_gastoshijos'


class ExportGuiasgrabadas(models.Model):
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
    cliente5 = models.CharField(db_column='Cliente5', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    consigna6 = models.CharField(db_column='Consigna6', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_guiasgrabadas'


class ExportGuiasgrabadas2(models.Model):
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
    chargesatdestination = models.DecimalField(db_column='ChargesAtDestination', max_digits=19, decimal_places=4,
                                               blank=True, null=True)  # Field name made lowercase.
    totalcollectcharges = models.DecimalField(db_column='TotalCollectCharges', max_digits=19, decimal_places=4,
                                              blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_guiasgrabadas2'


class ExportGuiasgrabadas3(models.Model):
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

    class Meta:
        managed = False
        db_table = 'export_guiasgrabadas3'


class ExportMadresgrabadas(models.Model):
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
    ofthecarrier = models.CharField(db_column='OfTheCarrier', max_length=70, blank=True,
                                    null=True)  # Field name made lowercase.
    gastosconiva = models.SmallIntegerField(db_column='GastosConIVA', blank=True,
                                            null=True)  # Field name made lowercase.
    houses7 = models.CharField(db_column='Houses7', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses8 = models.CharField(db_column='Houses8', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses9 = models.CharField(db_column='Houses9', max_length=28, blank=True, null=True)  # Field name made lowercase.
    houses10 = models.CharField(db_column='Houses10', max_length=28, blank=True,
                                null=True)  # Field name made lowercase.
    houses11 = models.CharField(db_column='Houses11', max_length=28, blank=True,
                                null=True)  # Field name made lowercase.
    houses12 = models.CharField(db_column='Houses12', max_length=28, blank=True,
                                null=True)  # Field name made lowercase.
    houses13 = models.CharField(db_column='Houses13', max_length=28, blank=True,
                                null=True)  # Field name made lowercase.
    houses14 = models.CharField(db_column='Houses14', max_length=28, blank=True,
                                null=True)  # Field name made lowercase.
    houses15 = models.CharField(db_column='Houses15', max_length=28, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_madresgrabadas'


class ExportMadresgrabadas3(models.Model):
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
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
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
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    arbitrajecass = models.DecimalField(db_column='ArbitrajeCASS', max_digits=19, decimal_places=4, blank=True,
                                        null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    sttawb = models.CharField(max_length=30, blank=True, null=True)
    autogenfletecpa = models.CharField(db_column='AutogenFleteCPA', max_length=50, blank=True,
                                       null=True)  # Field name made lowercase.
    envioiata = models.CharField(db_column='EnvioIATA', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    esagente = models.CharField(db_column='esAgente', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    documentos = models.CharField(db_column='Documentos', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    deposito = models.SmallIntegerField(db_column='Deposito', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_reservas'


class ExportServiceaereo(models.Model):
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
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_serviceaereo'


class ExportServireserva(models.Model):
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
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_servireserva'


class ExportTraceop(models.Model):
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=250, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'export_traceop'


class ExpterraAnulados(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expterra_anulados'


class ExpterraAttachhijo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True,
                                         null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_attachhijo'


class ExpterraAttachmadre(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_attachmadre'


class ExpterraCargaaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True)
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
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=15, blank=True, null=True)
    viaje = models.CharField(max_length=10, blank=True, null=True)
    vuelo = models.CharField(max_length=30, blank=True, null=True)
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    consignatario = models.IntegerField(db_column='Consignatario', blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    horasalida = models.CharField(db_column='HoraSalida', max_length=12, blank=True,
                                  null=True)  # Field name made lowercase.
    horallegada = models.CharField(db_column='HoraLlegada', max_length=12, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_conexaerea'


class ExpterraConexreserva(models.Model):
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
    numero = models.IntegerField(blank=True, null=True)
    ncorr = models.CharField(db_column='Ncorr', max_length=13, blank=True, null=True)  # Field name made lowercase.
    nintdespacho = models.CharField(db_column='NintDespacho', max_length=11, blank=True,
                                    null=True)  # Field name made lowercase.
    codfisc = models.CharField(db_column='CodFisc', max_length=6, blank=True, null=True)  # Field name made lowercase.
    coddeclaracion = models.CharField(db_column='CodDeclaracion', max_length=2, blank=True,
                                      null=True)  # Field name made lowercase.
    nomdeclaracion = models.CharField(db_column='NomDeclaracion', max_length=15, blank=True,
                                      null=True)  # Field name made lowercase.
    aduana = models.CharField(db_column='Aduana', max_length=24, blank=True, null=True)  # Field name made lowercase.
    codaduana = models.CharField(db_column='CodAduana', max_length=3, blank=True,
                                 null=True)  # Field name made lowercase.
    regimen = models.CharField(db_column='Regimen', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codregimen = models.CharField(db_column='CodRegimen', max_length=3, blank=True,
                                  null=True)  # Field name made lowercase.
    tipotramite = models.CharField(db_column='TipoTramite', max_length=24, blank=True,
                                   null=True)  # Field name made lowercase.
    codtramite = models.CharField(db_column='CodTramite', max_length=3, blank=True,
                                  null=True)  # Field name made lowercase.
    aduana2 = models.CharField(db_column='Aduana2', max_length=12, blank=True, null=True)  # Field name made lowercase.
    codaduana2 = models.CharField(db_column='CodAduana2', max_length=3, blank=True,
                                  null=True)  # Field name made lowercase.
    numero2 = models.CharField(db_column='Numero2', max_length=26, blank=True, null=True)  # Field name made lowercase.
    despachador = models.CharField(db_column='Despachador', max_length=24, blank=True,
                                   null=True)  # Field name made lowercase.
    coddespachador = models.CharField(db_column='CodDespachador', max_length=4, blank=True,
                                      null=True)  # Field name made lowercase.
    numerodeclaracion = models.CharField(db_column='NumeroDeclaracion', max_length=12, blank=True,
                                         null=True)  # Field name made lowercase.
    fechadeclaracion = models.CharField(db_column='FechaDeclaracion', max_length=10, blank=True,
                                        null=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=26, blank=True, null=True)  # Field name made lowercase.
    consignatario = models.CharField(db_column='Consignatario', max_length=37, blank=True,
                                     null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=37, blank=True,
                                 null=True)  # Field name made lowercase.
    almacenista = models.CharField(db_column='Almacenista', max_length=12, blank=True,
                                   null=True)  # Field name made lowercase.
    codalmacenista = models.CharField(db_column='CodAlmacenista', max_length=3, blank=True,
                                      null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codtipo = models.CharField(db_column='CodTipo', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rut = models.CharField(db_column='Rut', max_length=14, blank=True, null=True)  # Field name made lowercase.
    fecharecepcion = models.CharField(db_column='FechaRecepcion', max_length=12, blank=True,
                                      null=True)  # Field name made lowercase.
    consignante = models.CharField(db_column='Consignante', max_length=37, blank=True,
                                   null=True)  # Field name made lowercase.
    ubicacion = models.CharField(db_column='Ubicacion', max_length=26, blank=True,
                                 null=True)  # Field name made lowercase.
    aduanadestino = models.CharField(db_column='AduanaDestino', max_length=16, blank=True,
                                     null=True)  # Field name made lowercase.
    codaduanadestino = models.CharField(db_column='CodAduanaDestino', max_length=3, blank=True,
                                        null=True)  # Field name made lowercase.
    ubicacion2 = models.CharField(db_column='Ubicacion2', max_length=26, blank=True,
                                  null=True)  # Field name made lowercase.
    paisdestino = models.CharField(db_column='PaisDestino', max_length=16, blank=True,
                                   null=True)  # Field name made lowercase.
    codpaisdestino = models.CharField(db_column='CodPaisDestino', max_length=3, blank=True,
                                      null=True)  # Field name made lowercase.
    paisorigen = models.CharField(db_column='PaisOrigen', max_length=24, blank=True,
                                  null=True)  # Field name made lowercase.
    codpaisorigen = models.CharField(db_column='CodPaisOrigen', max_length=3, blank=True,
                                     null=True)  # Field name made lowercase.
    viatransporte = models.CharField(db_column='ViaTransporte', max_length=20, blank=True,
                                     null=True)  # Field name made lowercase.
    codviatransporte = models.CharField(db_column='CodViaTransporte', max_length=5, blank=True,
                                        null=True)  # Field name made lowercase.
    paisorigen2 = models.CharField(db_column='PaisOrigen2', max_length=24, blank=True,
                                   null=True)  # Field name made lowercase.
    codpaisorigen2 = models.CharField(db_column='CodPaisOrigen2', max_length=3, blank=True,
                                      null=True)  # Field name made lowercase.
    garantia = models.CharField(db_column='Garantia', max_length=26, blank=True,
                                null=True)  # Field name made lowercase.
    texto1 = models.CharField(db_column='Texto1', max_length=26, blank=True, null=True)  # Field name made lowercase.
    paisorigen3 = models.CharField(db_column='PaisOrigen3', max_length=24, blank=True,
                                   null=True)  # Field name made lowercase.
    codpaisorigen3 = models.CharField(db_column='CodPaisOrigen3', max_length=3, blank=True,
                                      null=True)  # Field name made lowercase.
    garantia2 = models.CharField(db_column='Garantia2', max_length=26, blank=True,
                                 null=True)  # Field name made lowercase.
    texto2 = models.CharField(db_column='Texto2', max_length=26, blank=True, null=True)  # Field name made lowercase.
    texto3 = models.CharField(db_column='Texto3', max_length=26, blank=True, null=True)  # Field name made lowercase.
    puertoembarque = models.CharField(db_column='PuertoEmbarque', max_length=24, blank=True,
                                      null=True)  # Field name made lowercase.
    codpuertoembarque = models.CharField(db_column='CodPuertoEmbarque', max_length=3, blank=True,
                                         null=True)  # Field name made lowercase.
    puertodesembarque = models.CharField(db_column='PuertoDesembarque', max_length=24, blank=True,
                                         null=True)  # Field name made lowercase.
    codpuertodesembarque = models.CharField(db_column='CodPuertoDesembarque', max_length=3, blank=True,
                                            null=True)  # Field name made lowercase.
    valorfob = models.CharField(db_column='ValorFob', max_length=16, blank=True,
                                null=True)  # Field name made lowercase.
    viatransporte2 = models.CharField(db_column='ViaTransporte2', max_length=20, blank=True,
                                      null=True)  # Field name made lowercase.
    codviatransporte2 = models.CharField(db_column='CodViaTransporte2', max_length=5, blank=True,
                                         null=True)  # Field name made lowercase.
    flete = models.CharField(db_column='Flete', max_length=16, blank=True, null=True)  # Field name made lowercase.
    codflete = models.CharField(db_column='CodFlete', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_declaracion'


class ExpterraDeclaracion2(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    conocembarque = models.CharField(db_column='ConocEmbarque', max_length=19, blank=True,
                                     null=True)  # Field name made lowercase.
    fechaemision = models.CharField(db_column='FechaEmision', max_length=10, blank=True,
                                    null=True)  # Field name made lowercase.
    emisor = models.CharField(db_column='Emisor', max_length=7, blank=True, null=True)  # Field name made lowercase.
    seguro = models.CharField(db_column='Seguro', max_length=16, blank=True, null=True)  # Field name made lowercase.
    codseguro = models.CharField(db_column='CodSeguro', max_length=3, blank=True,
                                 null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', max_length=37, blank=True,
                                  null=True)  # Field name made lowercase.
    valorcif = models.CharField(db_column='ValorCif', max_length=16, blank=True,
                                null=True)  # Field name made lowercase.
    texto4 = models.CharField(db_column='Texto4', max_length=90, blank=True, null=True)  # Field name made lowercase.
    texto5 = models.CharField(db_column='Texto5', max_length=90, blank=True, null=True)  # Field name made lowercase.
    texto6 = models.CharField(db_column='Texto6', max_length=90, blank=True, null=True)  # Field name made lowercase.
    texto7 = models.CharField(db_column='Texto7', max_length=90, blank=True, null=True)  # Field name made lowercase.
    infref = models.CharField(db_column='InfRef', max_length=45, blank=True, null=True)  # Field name made lowercase.
    idbultos = models.CharField(db_column='IdBultos', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    cantbultos = models.CharField(db_column='CantBultos', max_length=12, blank=True,
                                  null=True)  # Field name made lowercase.
    codbultos = models.CharField(db_column='CodBultos', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    infref2 = models.CharField(db_column='InfRef2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    idbultos2 = models.CharField(db_column='IdBultos2', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    cantbultos2 = models.CharField(db_column='CantBultos2', max_length=12, blank=True,
                                   null=True)  # Field name made lowercase.
    codbultos2 = models.CharField(db_column='CodBultos2', max_length=5, blank=True,
                                  null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos3 = models.CharField(db_column='IdBultos3', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    cantbultos3 = models.CharField(db_column='CantBultos3', max_length=12, blank=True,
                                   null=True)  # Field name made lowercase.
    codbultos3 = models.CharField(db_column='CodBultos3', max_length=5, blank=True,
                                  null=True)  # Field name made lowercase.
    variedad = models.CharField(db_column='Variedad', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    idbultos4 = models.CharField(db_column='IdBultos4', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    cantbultos4 = models.CharField(db_column='CantBultos4', max_length=12, blank=True,
                                   null=True)  # Field name made lowercase.
    codbultos4 = models.CharField(db_column='CodBultos4', max_length=5, blank=True,
                                  null=True)  # Field name made lowercase.
    marca = models.CharField(db_column='Marca', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos5 = models.CharField(db_column='IdBultos5', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    cantbultos5 = models.CharField(db_column='CantBultos5', max_length=12, blank=True,
                                   null=True)  # Field name made lowercase.
    codbultos5 = models.CharField(db_column='CodBultos5', max_length=5, blank=True,
                                  null=True)  # Field name made lowercase.
    otrosant = models.CharField(db_column='OtrosAnt', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    idbultos6 = models.CharField(db_column='IdBultos6', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    cantbultos6 = models.CharField(db_column='CantBultos6', max_length=12, blank=True,
                                   null=True)  # Field name made lowercase.
    codbultos6 = models.CharField(db_column='CodBultos6', max_length=5, blank=True,
                                  null=True)  # Field name made lowercase.
    obs = models.CharField(db_column='Obs', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos7 = models.CharField(db_column='IdBultos7', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    cantbultos7 = models.CharField(db_column='CantBultos7', max_length=12, blank=True,
                                   null=True)  # Field name made lowercase.
    codbultos7 = models.CharField(db_column='CodBultos7', max_length=5, blank=True,
                                  null=True)  # Field name made lowercase.
    obs2 = models.CharField(db_column='Obs2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos8 = models.CharField(db_column='IdBultos8', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    cantbultos8 = models.CharField(db_column='CantBultos8', max_length=12, blank=True,
                                   null=True)  # Field name made lowercase.
    codbultos8 = models.CharField(db_column='CodBultos8', max_length=5, blank=True,
                                  null=True)  # Field name made lowercase.
    obs3 = models.CharField(db_column='Obs3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos9 = models.CharField(db_column='IdBultos9', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    cantbultos9 = models.CharField(db_column='CantBultos9', max_length=12, blank=True,
                                   null=True)  # Field name made lowercase.
    codbultos9 = models.CharField(db_column='CodBultos9', max_length=5, blank=True,
                                  null=True)  # Field name made lowercase.
    obs4 = models.CharField(db_column='Obs4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idbultos10 = models.CharField(db_column='IdBultos10', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    cantbultos10 = models.CharField(db_column='CantBultos10', max_length=12, blank=True,
                                    null=True)  # Field name made lowercase.
    codbultos10 = models.CharField(db_column='CodBultos10', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    codnab = models.CharField(db_column='CodNab', max_length=14, blank=True, null=True)  # Field name made lowercase.
    esp = models.CharField(db_column='Esp', max_length=8, blank=True, null=True)  # Field name made lowercase.
    adval = models.CharField(db_column='AdVal', max_length=12, blank=True, null=True)  # Field name made lowercase.
    stasa = models.CharField(db_column='Stasa', max_length=14, blank=True, null=True)  # Field name made lowercase.
    idbultos11 = models.CharField(db_column='IdBultos11', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    cantbultos11 = models.CharField(db_column='CantBultos11', max_length=12, blank=True,
                                    null=True)  # Field name made lowercase.
    codbultos11 = models.CharField(db_column='CodBultos11', max_length=5, blank=True,
                                   null=True)  # Field name made lowercase.
    cantmerc = models.CharField(db_column='CantMerc', max_length=14, blank=True,
                                null=True)  # Field name made lowercase.
    punit = models.CharField(db_column='Punit', max_length=20, blank=True, null=True)  # Field name made lowercase.
    umed = models.CharField(db_column='Umed', max_length=15, blank=True, null=True)  # Field name made lowercase.
    pesobruto = models.CharField(db_column='PesoBruto', max_length=14, blank=True,
                                 null=True)  # Field name made lowercase.
    valorcif2 = models.CharField(db_column='ValorCif2', max_length=14, blank=True,
                                 null=True)  # Field name made lowercase.
    totalbultos = models.CharField(db_column='TotalBultos', max_length=9, blank=True,
                                   null=True)  # Field name made lowercase.
    totalacumulado = models.CharField(db_column='TotalAcumulado', max_length=14, blank=True,
                                      null=True)  # Field name made lowercase.
    totalacumulado2 = models.CharField(db_column='TotalAcumulado2', max_length=14, blank=True,
                                       null=True)  # Field name made lowercase.
    totalacumulado3 = models.CharField(db_column='TotalAcumulado3', max_length=9, blank=True,
                                       null=True)  # Field name made lowercase.
    totalitem = models.CharField(db_column='TotalItem', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    totalhojas = models.CharField(db_column='TotalHojas', max_length=5, blank=True,
                                  null=True)  # Field name made lowercase.
    totalfinal = models.CharField(db_column='TotalFinal', max_length=14, blank=True,
                                  null=True)  # Field name made lowercase.
    totalfinal2 = models.CharField(db_column='TotalFinal2', max_length=14, blank=True,
                                   null=True)  # Field name made lowercase.
    totalfinal3 = models.CharField(db_column='TotalFinal3', max_length=9, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_declaracion2'


class ExpterraEmbarqueaereo(models.Model):
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
    vaporcli2 = models.CharField(db_column='Vaporcli2', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
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
    ordencliente = models.CharField(db_column='OrdenCliente', max_length=850, blank=True,
                                    null=True)  # Field name made lowercase.
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
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=250, blank=True,
                                       null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=250, blank=True,
                                          null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=19, decimal_places=4, blank=True,
                                           null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    despafrontera = models.IntegerField(db_column='DespaFrontera', blank=True, null=True)  # Field name made lowercase.
    sociotransfer = models.IntegerField(db_column='SocioTransfer', blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=250, blank=True,
                                    null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    fechaentrega = models.DateTimeField(db_column='FechaEntrega', blank=True, null=True)  # Field name made lowercase.
    aquienentrega = models.CharField(db_column='aQuienEntrega', max_length=30, blank=True,
                                     null=True)  # Field name made lowercase.
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=50, blank=True,
                                       null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=50, blank=True,
                                         null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=50, blank=True,
                                      null=True)  # Field name made lowercase.
    booking = models.CharField(db_column='Booking', max_length=30, blank=True, null=True)  # Field name made lowercase.
    diasalmacenaje = models.SmallIntegerField(db_column='DiasAlmacenaje', blank=True,
                                              null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.DateTimeField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_embarqueaereo'


class ExpterraEntregadoc(models.Model):
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
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', max_length=40, blank=True,
                                            null=True)  # Field name made lowercase.
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', max_length=40, blank=True,
                                           null=True)  # Field name made lowercase.
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crtnumero = models.CharField(db_column='CRTNumero', max_length=40, blank=True,
                                 null=True)  # Field name made lowercase.
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', max_length=40, blank=True,
                                               null=True)  # Field name made lowercase.
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    micdtanumero = models.CharField(db_column='MicDtaNumero', max_length=40, blank=True,
                                    null=True)  # Field name made lowercase.
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    papeletanumero = models.CharField(db_column='PapeletaNumero', max_length=40, blank=True,
                                      null=True)  # Field name made lowercase.
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', max_length=40, blank=True,
                                              null=True)  # Field name made lowercase.
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', max_length=40, blank=True,
                                            null=True)  # Field name made lowercase.
    certorigennumero = models.CharField(db_column='CertOrigenNumero', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    certseguronumero = models.CharField(db_column='CertSeguroNumero', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', max_length=40, blank=True,
                                          null=True)  # Field name made lowercase.
    detotros3 = models.CharField(db_column='DetOtros3', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    detotros4 = models.CharField(db_column='DetOtros4', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_entregadoc'


class ExpterraEnvases(models.Model):
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
    envase = models.CharField(db_column='Envase', max_length=15, blank=True, null=True)  # Field name made lowercase.
    bultos = models.SmallIntegerField(blank=True, null=True)
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    profit = models.FloatField(blank=True, null=True)
    temperatura = models.FloatField(db_column='Temperatura', blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
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
    direccionentrega = models.SmallIntegerField(db_column='DireccionEntrega', blank=True,
                                                null=True)  # Field name made lowercase.
    rucchofer = models.CharField(db_column='RucChofer', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    fechallegadaplanta = models.DateTimeField(db_column='FechaLlegadaPlanta', blank=True,
                                              null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=100, blank=True,
                                     null=True)  # Field name made lowercase.
    precinto = models.CharField(db_column='Precinto', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    autogenenvase = models.CharField(db_column='AutogenEnvase', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    fechacitacion = models.DateTimeField(db_column='FechaCitacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_envases'


class ExpterraFaxes(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expterra_faxes'


class ExpterraFisico(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=60, blank=True, null=True)  # Field name made lowercase.
    volumen = models.FloatField(blank=True, null=True)
    tara = models.IntegerField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_fisico'


class ExpterraGastoshijos(models.Model):
    codigo = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    cliente = models.IntegerField(blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True,
                                null=True)  # Field name made lowercase.
    statushijos = models.SmallIntegerField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_gastoshijos'


class ExpterraGuiasgrabadas(models.Model):
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
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
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
    posicion = models.CharField(db_column='Posicion', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
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
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_reservas'


class ExpterraServiceaereo(models.Model):
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
    autogenenvase = models.CharField(db_column='AutogenEnvase', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_serviceaereo'


class ExpterraServireserva(models.Model):
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
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_servireserva'


class ExpterraTraceop(models.Model):
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=250, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expterra_traceop'


class ImpmaritAnulados(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impmarit_anulados'


class ImpmaritAttachhijo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True,
                                         null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_attachhijo'


class ImpmaritAttachmadre(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_attachmadre'


class ImpmaritCargaaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True)
    fechaembarque = models.DateTimeField(blank=True, null=True)
    cbm = models.FloatField(blank=True, null=True)
    mercaderia = models.TextField(blank=True, null=True)
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=400, blank=True,
                                     null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_cargaaerea'


class ImpmaritClavenrohouse(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    embarque = models.IntegerField(db_column='Embarque', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_clavenrohouse'


class ImpmaritClaveposicion(models.Model):
    posicion = models.CharField(unique=True, max_length=15)
    numeroorden = models.SmallIntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_claveposicion'


class ImpmaritConexaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=50, blank=True, null=True)
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(max_length=15, blank=True, null=True)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True,
                                  null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_conexaerea'


class ImpmaritConexreserva(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vapor = models.CharField(max_length=30, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=50, blank=True, null=True)
    viaje = models.CharField(max_length=10, blank=True, null=True)
    modo = models.CharField(max_length=15, blank=True, null=True)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True,
                                  null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_conexreserva'


class ImpmaritEmbarqueaereo(models.Model):
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
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    notificar = models.IntegerField(db_column='Notificar', blank=True, null=True)  # Field name made lowercase.
    vaporcli = models.CharField(db_column='Vaporcli', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vaporcli2 = models.CharField(db_column='Vaporcli2', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    terminal = models.SmallIntegerField(blank=True, null=True)
    tipovend = models.CharField(db_column='Tipovend', max_length=1, blank=True, null=True)  # Field name made lowercase.
    vendedor = models.SmallIntegerField(db_column='Vendedor', blank=True, null=True)  # Field name made lowercase.
    comivend = models.FloatField(db_column='Comivend', blank=True, null=True)  # Field name made lowercase.
    aplicaprofit = models.IntegerField(db_column='Aplicaprofit', blank=True, null=True)  # Field name made lowercase.
    nroreferedi = models.IntegerField(blank=True, null=True)
    notomaprofit = models.IntegerField(blank=True, null=True)
    ordencliente = models.CharField(max_length=850, blank=True, null=True)
    desconsolida = models.CharField(max_length=60, blank=True, null=True)
    armador = models.IntegerField(blank=True, null=True)
    viaje = models.CharField(max_length=20, blank=True, null=True)
    propia = models.IntegerField(blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    fechaentrega = models.DateTimeField(blank=True, null=True)
    aquienentrega = models.CharField(max_length=30, blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    originales = models.CharField(max_length=1, blank=True, null=True)
    fechalimitedemora = models.DateTimeField(db_column='FechaLimiteDemora', blank=True,
                                             null=True)  # Field name made lowercase.
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=250, blank=True,
                                       null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=250, blank=True,
                                          null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=19, decimal_places=4, blank=True,
                                           null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    tieneacta = models.CharField(db_column='TieneActa', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=250, blank=True,
                                    null=True)  # Field name made lowercase.
    deaddocumentos = models.DateTimeField(db_column='DeadDocumentos', blank=True,
                                          null=True)  # Field name made lowercase.
    deadentrega = models.DateTimeField(db_column='DeadEntrega', blank=True, null=True)  # Field name made lowercase.
    hblcorp = models.IntegerField(db_column='HBLCorp', blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    desconsolidadeposito = models.CharField(db_column='DesconsolidaDeposito', max_length=1, blank=True,
                                            null=True)  # Field name made lowercase.
    demora = models.SmallIntegerField(db_column='Demora', blank=True, null=True)  # Field name made lowercase.
    valordemoravta = models.DecimalField(db_column='ValorDemoraVTA', max_digits=19, decimal_places=4, blank=True,
                                         null=True)  # Field name made lowercase.
    valordemoracpa = models.DecimalField(db_column='ValorDemoraCPA', max_digits=19, decimal_places=4, blank=True,
                                         null=True)  # Field name made lowercase.
    enviointercomex = models.CharField(db_column='EnvioIntercomex', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    arribosim = models.DateTimeField(db_column='ArriboSIM', blank=True, null=True)  # Field name made lowercase.
    presentasim = models.DateTimeField(db_column='PresentaSIM', blank=True, null=True)  # Field name made lowercase.
    cierresim = models.DateTimeField(db_column='CierreSIM', blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=50, blank=True,
                                       null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=50, blank=True,
                                         null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=50, blank=True,
                                      null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    emisionbl = models.DateTimeField(db_column='EmisionBL', blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    fechafinoperativa = models.DateTimeField(db_column='FechaFinOperativa', blank=True,
                                             null=True)  # Field name made lowercase.
    horafinoperativa = models.CharField(db_column='HoraFinOperativa', max_length=8, blank=True,
                                        null=True)  # Field name made lowercase.
    fechadocsdisp = models.DateTimeField(db_column='FechaDocsDisp', blank=True, null=True)  # Field name made lowercase.
    horadocsdisp = models.CharField(db_column='HoraDocsDisp', max_length=8, blank=True,
                                    null=True)  # Field name made lowercase.
    fechadocsret = models.DateTimeField(db_column='FechaDocsRet', blank=True, null=True)  # Field name made lowercase.
    horadocsret = models.CharField(db_column='HoraDocsRet', max_length=8, blank=True,
                                   null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    tipobl = models.CharField(db_column='TipoBL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    emitebloriginal = models.CharField(db_column='EmiteBLOriginal', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.DateTimeField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_embarqueaereo'


class ImpmaritEntregadoc(models.Model):
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
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', max_length=40, blank=True,
                                            null=True)  # Field name made lowercase.
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', max_length=40, blank=True,
                                           null=True)  # Field name made lowercase.
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crtnumero = models.CharField(db_column='CRTNumero', max_length=40, blank=True,
                                 null=True)  # Field name made lowercase.
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', max_length=40, blank=True,
                                               null=True)  # Field name made lowercase.
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    micdtanumero = models.CharField(db_column='MicDtaNumero', max_length=40, blank=True,
                                    null=True)  # Field name made lowercase.
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    papeletanumero = models.CharField(db_column='PapeletaNumero', max_length=40, blank=True,
                                      null=True)  # Field name made lowercase.
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', max_length=40, blank=True,
                                              null=True)  # Field name made lowercase.
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', max_length=40, blank=True,
                                            null=True)  # Field name made lowercase.
    certorigennumero = models.CharField(db_column='CertOrigenNumero', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    certseguronumero = models.CharField(db_column='CertSeguroNumero', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', max_length=40, blank=True,
                                          null=True)  # Field name made lowercase.
    detotros3 = models.CharField(db_column='DetOtros3', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    detotros4 = models.CharField(db_column='DetOtros4', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_entregadoc'


class ImpmaritEnvases(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=5, blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    movimiento = models.CharField(max_length=10, blank=True, null=True)
    terminos = models.CharField(max_length=5, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    marcas = models.CharField(max_length=200, blank=True, null=True)
    precinto = models.CharField(max_length=100, blank=True, null=True)
    tara = models.FloatField(blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    envase = models.CharField(db_column='Envase', max_length=15, blank=True, null=True)  # Field name made lowercase.
    bultos = models.IntegerField(blank=True, null=True)
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    profit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    nrocontenedor = models.CharField(max_length=100, blank=True, null=True)
    volumen = models.FloatField(blank=True, null=True)
    status = models.SmallIntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    fechadevol = models.DateTimeField(db_column='FechaDevol', blank=True, null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_envases'


class ImpmaritFaxes(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impmarit_faxes'


class ImpmaritFisico(models.Model):
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
    cliente = models.IntegerField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_fisico'


class ImpmaritGastoshijos(models.Model):
    cliente = models.IntegerField(blank=True, null=True)
    codigo = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True,
                                null=True)  # Field name made lowercase.
    statushijos = models.SmallIntegerField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    movimiento = models.CharField(db_column='Movimiento', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_gastoshijos'


class ImpmaritGastosmadre(models.Model):
    cliente = models.SmallIntegerField(blank=True, null=True)
    codigo = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=15, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sucursal = models.SmallIntegerField(db_column='Sucursal', blank=True, null=True)  # Field name made lowercase.
    unidad = models.CharField(db_column='Unidad', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    operacion = models.CharField(db_column='Operacion', max_length=25, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_gastosmadre'


class ImpmaritGuiasgrabadas(models.Model):
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
    portext = models.CharField(max_length=50, blank=True, null=True)
    vadeclared = models.IntegerField(blank=True, null=True)
    precarriage = models.CharField(db_column='PreCarriage', max_length=35, blank=True,
                                   null=True)  # Field name made lowercase.
    consigna6 = models.CharField(db_column='Consigna6', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    consigna7 = models.CharField(db_column='Consigna7', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    consigna8 = models.CharField(db_column='Consigna8', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    cliente5 = models.CharField(db_column='Cliente5', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    otranotif = models.CharField(db_column='Otranotif', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_guiasgrabadas'


class ImpmaritGuiasgrabadas2(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    marks = models.CharField(max_length=30, blank=True, null=True)
    packages = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    gross = models.CharField(max_length=30, blank=True, null=True)
    tare = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impmarit_guiasgrabadas2'


class ImpmaritNietos(models.Model):
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
    observaciones = models.TextField(blank=True, null=True)
    notificar = models.CharField(max_length=50, blank=True, null=True)
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    producto = models.CharField(db_column='Producto', max_length=150, blank=True,
                                null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_nietos'


class ImpmaritReservas(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    kilos = models.FloatField(db_column='Kilos', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    awb = models.CharField(max_length=40, blank=True, null=True)
    agente = models.IntegerField(blank=True, null=True)
    consignatario = models.IntegerField(blank=True, null=True)
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    volumen = models.FloatField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
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
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=20, blank=True, null=True)  # Field name made lowercase.
    posicion = models.CharField(db_column='Posicion', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
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
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    viajefluvial = models.CharField(db_column='ViajeFluvial', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    awbfluvial = models.CharField(db_column='AwbFluvial', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    prefijofluvial = models.CharField(db_column='PrefijoFluvial', max_length=5, blank=True,
                                      null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_reservas'


class ImpmaritServiceaereo(models.Model):
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
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_serviceaereo'


class ImpmaritServireserva(models.Model):
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
    prorrateo = models.CharField(db_column='Prorrateo', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_servireserva'


class ImpmaritTraceop(models.Model):
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=250, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impmarit_traceop'


class ImportAnulados(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'import_anulados'


class ImportAttachhijo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True,
                                         null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_attachhijo'


class ImportAttachmadre(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_attachmadre'


class ImportCargaaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True)
    fechaembarque = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'import_cargaaerea'


class ImportCargaaereaaduana(models.Model):
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
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vuelo = models.CharField(max_length=30, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    ciavuelo = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(max_length=10, blank=True, null=True)
    modo = models.CharField(max_length=15, blank=True, null=True)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True,
                                  null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_conexaerea'


class ImportConexreserva(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vuelo = models.CharField(max_length=30, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    ciavuelo = models.CharField(max_length=2, blank=True, null=True)
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True,
                                  null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True,
                                   null=True)  # Field name made lowercase.

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
    vaporcli2 = models.CharField(db_column='Vaporcli2', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
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
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=250, blank=True,
                                       null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=250, blank=True,
                                          null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    mercaderia = models.TextField(db_column='Mercaderia', blank=True, null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=19, decimal_places=4, blank=True,
                                           null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    tieneacta = models.CharField(db_column='TieneActa', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=250, blank=True,
                                    null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    enviointercomex = models.CharField(db_column='EnvioIntercomex', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=50, blank=True,
                                       null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=50, blank=True,
                                         null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=50, blank=True,
                                      null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    emisionawb = models.DateTimeField(db_column='EmisionAWB', blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    fechalibdoc = models.DateTimeField(db_column='FechaLibDoc', blank=True, null=True)  # Field name made lowercase.
    horalibdoc = models.CharField(db_column='HoraLibDoc', max_length=8, blank=True,
                                  null=True)  # Field name made lowercase.
    fechapresmanif = models.DateTimeField(db_column='FechaPresManif', blank=True,
                                          null=True)  # Field name made lowercase.
    horapresmanif = models.CharField(db_column='HoraPresManif', max_length=8, blank=True,
                                     null=True)  # Field name made lowercase.
    fechacierremanif = models.DateTimeField(db_column='FechaCierreManif', blank=True,
                                            null=True)  # Field name made lowercase.
    horacierremanif = models.CharField(db_column='HoraCierreManif', max_length=8, blank=True,
                                       null=True)  # Field name made lowercase.
    fechadesconso = models.DateTimeField(db_column='FechaDesconso', blank=True, null=True)  # Field name made lowercase.
    horadesconso = models.CharField(db_column='HoraDesconso', max_length=8, blank=True,
                                    null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.DateTimeField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_embarqueaereo'


class ImportEntregadoc(models.Model):
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
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', max_length=40, blank=True,
                                            null=True)  # Field name made lowercase.
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', max_length=40, blank=True,
                                           null=True)  # Field name made lowercase.
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crtnumero = models.CharField(db_column='CRTNumero', max_length=40, blank=True,
                                 null=True)  # Field name made lowercase.
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', max_length=40, blank=True,
                                               null=True)  # Field name made lowercase.
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    micdtanumero = models.CharField(db_column='MicDtaNumero', max_length=40, blank=True,
                                    null=True)  # Field name made lowercase.
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    papeletanumero = models.CharField(db_column='PapeletaNumero', max_length=40, blank=True,
                                      null=True)  # Field name made lowercase.
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', max_length=40, blank=True,
                                              null=True)  # Field name made lowercase.
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', max_length=40, blank=True,
                                            null=True)  # Field name made lowercase.
    certorigennumero = models.CharField(db_column='CertOrigenNumero', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    certseguronumero = models.CharField(db_column='CertSeguroNumero', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', max_length=40, blank=True,
                                          null=True)  # Field name made lowercase.
    detotros3 = models.CharField(db_column='DetOtros3', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    detotros4 = models.CharField(db_column='DetOtros4', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_entregadoc'


class ImportFaxes(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'import_faxes'


class ImportGastoshijos(models.Model):
    cliente = models.IntegerField(blank=True, null=True)
    codigo = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True,
                                null=True)  # Field name made lowercase.
    statushijos = models.SmallIntegerField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_gastoshijos'


class ImportGuiasgrabadas(models.Model):
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
    ofthecarrier = models.CharField(db_column='OfTheCarrier', max_length=70, blank=True,
                                    null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_guiasgrabadas2'


class ImportGuiasgrabadas3(models.Model):
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

    class Meta:
        managed = False
        db_table = 'import_guiasgrabadas3'


class ImportReservas(models.Model):
    numero = models.IntegerField(db_column='Numero', primary_key=True)  # Field name made lowercase.
    transportista = models.SmallIntegerField(db_column='Transportista', blank=True,
                                             null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    vuelo = models.CharField(db_column='Vuelo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    kilos = models.FloatField(db_column='Kilos', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    awb = models.CharField(max_length=20, blank=True, null=True)
    agente = models.SmallIntegerField(blank=True, null=True)
    consignatario = models.SmallIntegerField(blank=True, null=True)
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
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
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_reservas'


class ImportServiceaereo(models.Model):
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
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_serviceaereo'


class ImportServireserva(models.Model):
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
    prorrateo = models.CharField(db_column='Prorrateo', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_servireserva'


class ImportTraceop(models.Model):
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=250, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'import_traceop'


class ImpterraAnulados(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impterra_anulados'


class ImpterraAttachhijo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True,
                                         null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_attachhijo'


class ImpterraAttachmadre(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_attachmadre'


class ImpterraCargaaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True)
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
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=15, blank=True, null=True)
    viaje = models.CharField(max_length=10, blank=True, null=True)
    vuelo = models.CharField(max_length=30, blank=True, null=True)
    embarcador = models.IntegerField(db_column='Embarcador', blank=True, null=True)  # Field name made lowercase.
    consignatario = models.IntegerField(db_column='Consignatario', blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    horasalida = models.CharField(db_column='HoraSalida', max_length=12, blank=True,
                                  null=True)  # Field name made lowercase.
    horallegada = models.CharField(db_column='HoraLlegada', max_length=12, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_conexaerea'


class ImpterraConexreserva(models.Model):
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
    vaporcli2 = models.CharField(db_column='Vaporcli2', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
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
    ordencliente = models.CharField(db_column='OrdenCliente', max_length=850, blank=True,
                                    null=True)  # Field name made lowercase.
    propia = models.IntegerField(blank=True, null=True)
    seguimiento = models.IntegerField(blank=True, null=True)
    multimodal = models.CharField(max_length=1, blank=True, null=True)
    trafico = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=3, blank=True, null=True)
    exportado = models.CharField(max_length=1, blank=True, null=True)
    aquienentrega = models.CharField(max_length=30, blank=True, null=True)
    fechaentrega = models.DateTimeField(blank=True, null=True)
    datosembarcador = models.CharField(db_column='DatosEmbarcador', max_length=250, blank=True,
                                       null=True)  # Field name made lowercase.
    datosconsignatario = models.CharField(db_column='DatosConsignatario', max_length=250, blank=True,
                                          null=True)  # Field name made lowercase.
    wreceipt = models.CharField(db_column='Wreceipt', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    proyecto = models.SmallIntegerField(db_column='Proyecto', blank=True, null=True)  # Field name made lowercase.
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    autogenflete = models.CharField(db_column='AutogenFlete', max_length=50, blank=True,
                                    null=True)  # Field name made lowercase.
    cambiousdpactado = models.DecimalField(db_column='CambioUSDPactado', max_digits=19, decimal_places=4, blank=True,
                                           null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    despafrontera = models.IntegerField(db_column='DespaFrontera', blank=True, null=True)  # Field name made lowercase.
    sociotransfer = models.IntegerField(db_column='SocioTransfer', blank=True, null=True)  # Field name made lowercase.
    refproveedor = models.CharField(db_column='RefProveedor', max_length=250, blank=True,
                                    null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    enviointercomex = models.CharField(db_column='EnvioIntercomex', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    agecompras = models.IntegerField(db_column='AgeCompras', blank=True, null=True)  # Field name made lowercase.
    ageventas = models.IntegerField(db_column='AgeVentas', blank=True, null=True)  # Field name made lowercase.
    actividad = models.SmallIntegerField(db_column='Actividad', blank=True, null=True)  # Field name made lowercase.
    numentregafemsa = models.CharField(db_column='NumEntregaFEMSA', max_length=50, blank=True,
                                       null=True)  # Field name made lowercase.
    numproveedorfemsa = models.CharField(db_column='NumProveedorFEMSA', max_length=50, blank=True,
                                         null=True)  # Field name made lowercase.
    remisionfemsa = models.CharField(db_column='RemisionFEMSA', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    sociedadfemsa = models.CharField(db_column='SociedadFEMSA', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    monedadocfemsa = models.CharField(db_column='MonedaDocFEMSA', max_length=50, blank=True,
                                      null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    trackid = models.CharField(db_column='TrackID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    etd = models.DateTimeField(db_column='ETD', blank=True, null=True)  # Field name made lowercase.
    eta = models.DateTimeField(db_column='ETA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_embarqueaereo'


class ImpterraEntregadoc(models.Model):
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
    cartatemp = models.CharField(db_column='CartaTemp', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    parterecepcion = models.CharField(db_column='ParteRecepcion', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.
    parterecepcionnumero = models.CharField(db_column='ParteRecepcionNumero', max_length=40, blank=True,
                                            null=True)  # Field name made lowercase.
    facturaseguro = models.CharField(db_column='FacturaSeguro', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    facturaseguronumero = models.CharField(db_column='FacturaSeguroNumero', max_length=40, blank=True,
                                           null=True)  # Field name made lowercase.
    crt = models.CharField(db_column='CRT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    crtnumero = models.CharField(db_column='CRTNumero', max_length=40, blank=True,
                                 null=True)  # Field name made lowercase.
    facturatransporte = models.CharField(db_column='FacturaTransporte', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.
    facturatransportenumero = models.CharField(db_column='FacturaTransporteNumero', max_length=40, blank=True,
                                               null=True)  # Field name made lowercase.
    micdta = models.CharField(db_column='MicDta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    micdtanumero = models.CharField(db_column='MicDtaNumero', max_length=40, blank=True,
                                    null=True)  # Field name made lowercase.
    papeleta = models.CharField(db_column='Papeleta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    papeletanumero = models.CharField(db_column='PapeletaNumero', max_length=40, blank=True,
                                      null=True)  # Field name made lowercase.
    descdocumentaria = models.CharField(db_column='DescDocumentaria', max_length=1, blank=True,
                                        null=True)  # Field name made lowercase.
    descdocumentarianumero = models.CharField(db_column='DescDocumentariaNumero', max_length=40, blank=True,
                                              null=True)  # Field name made lowercase.
    declaracionembnumero = models.CharField(db_column='DeclaracionEmbNumero', max_length=40, blank=True,
                                            null=True)  # Field name made lowercase.
    certorigennumero = models.CharField(db_column='CertOrigenNumero', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    certseguronumero = models.CharField(db_column='CertSeguroNumero', max_length=40, blank=True,
                                        null=True)  # Field name made lowercase.
    cumpaduaneronumero = models.CharField(db_column='CumpAduaneroNumero', max_length=40, blank=True,
                                          null=True)  # Field name made lowercase.
    detotros3 = models.CharField(db_column='DetOtros3', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    detotros4 = models.CharField(db_column='DetOtros4', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_entregadoc'


class ImpterraEnvases(models.Model):
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
    envase = models.CharField(db_column='Envase', max_length=15, blank=True, null=True)  # Field name made lowercase.
    bultos = models.SmallIntegerField(blank=True, null=True)
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    profit = models.FloatField(blank=True, null=True)
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=100, blank=True,
                                     null=True)  # Field name made lowercase.
    precinto = models.CharField(db_column='Precinto', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    temperatura = models.FloatField(db_column='Temperatura', blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
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
    direccionentrega = models.SmallIntegerField(db_column='DireccionEntrega', blank=True,
                                                null=True)  # Field name made lowercase.
    rucchofer = models.CharField(db_column='RucChofer', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    fechallegadaplanta = models.DateTimeField(db_column='FechaLlegadaPlanta', blank=True,
                                              null=True)  # Field name made lowercase.
    fechacitacion = models.DateTimeField(db_column='FechaCitacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_envases'


class ImpterraFaxes(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'impterra_faxes'


class ImpterraFisico(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=60, blank=True, null=True)  # Field name made lowercase.
    volumen = models.FloatField(blank=True, null=True)
    tara = models.IntegerField(db_column='Tara', blank=True, null=True)  # Field name made lowercase.
    precio = models.DecimalField(db_column='Precio', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_fisico'


class ImpterraGastoshijos(models.Model):
    codigo = models.SmallIntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    cliente = models.IntegerField(blank=True, null=True)
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(db_column='Moneda', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True,
                                null=True)  # Field name made lowercase.
    statushijos = models.SmallIntegerField(db_column='StatusHijos', blank=True, null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_gastoshijos'


class ImpterraGuiasgrabadas(models.Model):
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
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=19, decimal_places=4, blank=True,
                                 null=True)  # Field name made lowercase.
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
    posicion = models.CharField(db_column='Posicion', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
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
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    manifiesto = models.CharField(db_column='Manifiesto', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_reservas'


class ImpterraServiceaereo(models.Model):
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
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_serviceaereo'


class ImpterraServireserva(models.Model):
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
    prorrateo = models.CharField(db_column='Prorrateo', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    empresa = models.SmallIntegerField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    reembolsable = models.CharField(db_column='Reembolsable', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_servireserva'


class ImpterraTraceop(models.Model):
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=250, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'impterra_traceop'


class LoginAccount(models.Model):
    documento = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    firma = models.CharField(max_length=100, blank=True, null=True)
    clave = models.CharField(max_length=50, blank=True, null=True)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'login_account'


class LoginCorreoenviado(models.Model):
    fecha = models.DateTimeField()
    enviado_a = models.CharField(max_length=250, db_collation='utf8mb4_general_ci')
    correo = models.CharField(max_length=100, db_collation='utf8mb4_general_ci')
    mensaje = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    estado = models.CharField(max_length=10, db_collation='utf8mb4_general_ci')
    error = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    tipo = models.CharField(max_length=50, db_collation='utf8mb4_general_ci')
    usuario = models.CharField(max_length=100, db_collation='utf8mb4_general_ci')
    emisor = models.CharField(max_length=150, blank=True, null=True)
    seguimiento = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'login_correoenviado'


class MantenimientosActividades(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_actividades'


class MantenimientosAttachsocio(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    archivo = models.CharField(db_column='Archivo', max_length=250, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=50, blank=True, null=True)  # Field name made lowercase.
    web = models.CharField(db_column='Web', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_attachsocio'


class MantenimientosBancos(models.Model):
    codigo = models.SmallIntegerField(db_column='Codigo', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True,
                                   null=True)  # Field name made lowercase.
    edi = models.CharField(db_column='EDI', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nombrechino = models.CharField(db_column='NombreChino', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    rut = models.CharField(db_column='RUT', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_bancos'


class MantenimientosBandejaefreight(models.Model):
    de = models.CharField(db_column='De', max_length=100, blank=True, null=True)  # Field name made lowercase.
    asunto = models.CharField(db_column='Asunto', max_length=300, blank=True, null=True)  # Field name made lowercase.
    mensaje = models.TextField(db_column='Mensaje', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    fechaprocesado = models.DateTimeField(db_column='FechaProcesado', blank=True,
                                          null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_bandejaefreight'


class MantenimientosBudget(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_budget'


class MantenimientosCiudades(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.CharField(unique=True, max_length=5)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    codedi = models.CharField(max_length=5, blank=True, null=True)
    codaduana = models.CharField(db_column='Codaduana', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    paises_idinternacional = models.CharField(db_column='Paises_IdInternacional', max_length=2, blank=True,
                                              null=True)  # Field name made lowercase.
    estado = models.SmallIntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    fechaactualizado = models.DateTimeField(db_column='FechaActualizado', blank=True,
                                            null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_ciudades'


class MantenimientosClaveposicionmm(models.Model):
    posicion = models.CharField(db_column='Posicion', max_length=15)  # Field name made lowercase.
    numeroorden = models.SmallIntegerField(db_column='NumeroOrden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_claveposicionmm'


class MantenimientosClicontactos(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cargo = models.CharField(db_column='Cargo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    celular = models.CharField(db_column='Celular', max_length=50, blank=True, null=True)  # Field name made lowercase.
    skype = models.CharField(db_column='Skype', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_clicontactos'


class MantenimientosClientes(models.Model):
    codigo = models.IntegerField(unique=True)
    empresa = models.CharField(max_length=50, blank=True, null=True)
    razonsocial = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=5, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.SmallIntegerField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=500, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    cpostal = models.CharField(max_length=20, blank=True, null=True)
    ruc = models.CharField(max_length=30, blank=True, null=True)
    contactos = models.TextField(blank=True, null=True)
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
    expectativa = models.TextField(blank=True, null=True)
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
    usocfdisat = models.CharField(db_column='UsoCFDISAT', max_length=3, blank=True,
                                  null=True)  # Field name made lowercase.
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
        db_table = 'mantenimientos_clientes'


class MantenimientosClifaxes(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    asunto = models.TextField(db_column='Asunto', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_clifaxes'


class MantenimientosClirelacion(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    relacionado = models.IntegerField(db_column='Relacionado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_clirelacion'


class MantenimientosClireldep(models.Model):
    idcli = models.IntegerField(db_column='IDCli', blank=True, null=True)  # Field name made lowercase.
    idrep = models.IntegerField(db_column='IDRep', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_clireldep'


class MantenimientosClitipodocumento(models.Model):
    numero = models.CharField(db_column='Numero', max_length=10, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_clitipodocumento'


class MantenimientosClitipooperacion(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    tipooperacion = models.SmallIntegerField(db_column='TipoOperacion', blank=True,
                                             null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_clitipooperacion'


class MantenimientosClitraficos(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    trafico = models.SmallIntegerField(db_column='Trafico', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_clitraficos'


class MantenimientosConfig(models.Model):
    dato = models.SmallIntegerField(blank=True, null=True)
    dato2 = models.SmallIntegerField(blank=True, null=True)
    detalle = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimientos_config'


class MantenimientosContratoscli(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    numcontrato = models.CharField(db_column='NumContrato', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=5, blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_contratoscli'


class MantenimientosDepositos(models.Model):
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
    observaciones = models.TextField(blank=True, null=True)
    contactos = models.TextField(blank=True, null=True)
    ruc = models.CharField(max_length=20, blank=True, null=True)
    aduana = models.CharField(db_column='Aduana', max_length=20, blank=True, null=True)  # Field name made lowercase.
    empresachino = models.CharField(db_column='EmpresaChino', max_length=100, blank=True,
                                    null=True)  # Field name made lowercase.
    direccionchino = models.CharField(db_column='DireccionChino', max_length=100, blank=True,
                                      null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_depositos'


class MantenimientosDireccionentregas(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_direccionentregas'


class MantenimientosDtproperties(models.Model):
    objectid = models.IntegerField(blank=True, null=True)
    property = models.CharField(max_length=64)
    value = models.CharField(max_length=255, blank=True, null=True)
    lvalue = models.TextField(blank=True, null=True)
    version = models.IntegerField()
    uvalue = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimientos_dtproperties'


class MantenimientosEdimonedas(models.Model):
    agente = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    codorigen = models.SmallIntegerField(blank=True, null=True)
    coddestino = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimientos_edimonedas'


class MantenimientosEdiproductos(models.Model):
    agente = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    codorigen = models.SmallIntegerField(blank=True, null=True)
    coddestino = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimientos_ediproductos'


class MantenimientosEdiservicios(models.Model):
    agente = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    codorigen = models.SmallIntegerField(blank=True, null=True)
    coddestino = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimientos_ediservicios'


class MantenimientosEdisocios(models.Model):
    agente = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=3, blank=True, null=True)
    codorigen = models.IntegerField(blank=True, null=True)
    coddestino = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimientos_edisocios'


class MantenimientosEmpresa(models.Model):
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
    usastock = models.IntegerField(blank=True, null=True)
    usaposicion = models.IntegerField(blank=True, null=True)
    cass = models.CharField(max_length=15, blank=True, null=True)
    pasagastos = models.IntegerField(blank=True, null=True)
    vaciudad = models.IntegerField(blank=True, null=True)
    nroata = models.CharField(max_length=15, blank=True, null=True)
    prefijohouse = models.CharField(max_length=5, blank=True, null=True)
    heredaposhijo = models.IntegerField(blank=True, null=True)
    usacontrolhawb = models.IntegerField(db_column='usacontrolHAWB', blank=True,
                                         null=True)  # Field name made lowercase.
    servidores = models.CharField(max_length=1, blank=True, null=True)
    graboimagen = models.IntegerField(blank=True, null=True)
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
    support_pms = models.IntegerField(db_column='Support_PMS', blank=True, null=True)  # Field name made lowercase.
    statementtype = models.CharField(db_column='StatementType', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    processach_ap = models.IntegerField(db_column='ProcessACH_AP', blank=True, null=True)  # Field name made lowercase.
    payersunitnumber = models.CharField(db_column='PayersUnitNumber', max_length=10, blank=True,
                                        null=True)  # Field name made lowercase.
    checkseb = models.IntegerField(db_column='CheckSEB', blank=True, null=True)  # Field name made lowercase.
    bondproducernumber = models.CharField(db_column='BondProducerNumber', max_length=10, blank=True,
                                          null=True)  # Field name made lowercase.
    checkpoa = models.IntegerField(db_column='CheckPOA', blank=True, null=True)  # Field name made lowercase.
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
    binaryattach = models.IntegerField(db_column='BinaryAttach', blank=True, null=True)  # Field name made lowercase.
    campotraficoobligatorio = models.CharField(db_column='CampoTraficoObligatorio', max_length=1, blank=True,
                                               null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_empresa'


class MantenimientosEstados(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_estados'


class MantenimientosFormapago(models.Model):
    codigo = models.SmallIntegerField(db_column='Codigo', unique=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_formapago'


class MantenimientosGrupos(models.Model):
    grupo = models.CharField(max_length=50)
    detalle = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimientos_grupos'


class MantenimientosGuias(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_guias'


class MantenimientosGuiascentro(models.Model):
    transportista = models.SmallIntegerField(db_column='Transportista', unique=True)  # Field name made lowercase.
    prefijo = models.SmallIntegerField(db_column='Prefijo', blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    estado = models.SmallIntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    refmaster = models.SmallIntegerField(db_column='RefMaster', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_guiascentro'


class MantenimientosHouses(models.Model):
    contador = models.FloatField(blank=True, null=True)
    em = models.FloatField(db_column='EM', blank=True, null=True)  # Field name made lowercase.
    et = models.FloatField(db_column='ET', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_houses'


class MantenimientosInterfaces(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    tipointerface = models.CharField(db_column='TipoInterface', max_length=1, blank=True,
                                     null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    formato = models.CharField(db_column='Formato', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cabezal = models.CharField(db_column='Cabezal', max_length=1, blank=True, null=True)  # Field name made lowercase.
    delimitador = models.CharField(db_column='Delimitador', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_interfaces'


class MantenimientosInterfacesatributos(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    nombrecampo = models.CharField(db_column='NombreCampo', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    entradato = models.CharField(db_column='EntraDato', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    saledato = models.CharField(db_column='SaleDato', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_interfacesatributos'


class MantenimientosInterfacesdetalle(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_interfacesdetalle'


class MantenimientosLlegadas(models.Model):
    vapor = models.CharField(db_column='Vapor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    llegada = models.DateTimeField(db_column='Llegada', blank=True, null=True)  # Field name made lowercase.
    transportista = models.CharField(db_column='Transportista', max_length=50, blank=True,
                                     null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_llegadas'


class MantenimientosLlegadasdetalle(models.Model):
    idllegadas = models.IntegerField(db_column='IDLlegadas')  # Field name made lowercase.
    ciudad = models.CharField(db_column='Ciudad', max_length=5, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_llegadasdetalle'


class MantenimientosMonedas(models.Model):
    codigo = models.SmallIntegerField()
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_monedas'


class MantenimientosNotificaciones(models.Model):
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
    texto = models.TextField(db_column='Texto', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    idioma = models.SmallIntegerField(db_column='Idioma', blank=True, null=True)  # Field name made lowercase.
    salida = models.CharField(db_column='Salida', max_length=1, blank=True, null=True)  # Field name made lowercase.
    enviodatoshouse = models.CharField(db_column='EnvioDatosHouse', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_notificaciones'


class MantenimientosNromensaje(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_nromensaje'


class MantenimientosOrganiza(models.Model):
    codigo = models.SmallIntegerField()
    empresa = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=3, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    cpostal = models.CharField(max_length=10, blank=True, null=True)
    contactos = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimientos_organiza'


class MantenimientosOtrosservicios(models.Model):
    codigo = models.SmallIntegerField(db_column='Codigo', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_otrosservicios'


class MantenimientosPaises(models.Model):
    nombre = models.CharField(max_length=50)
    continente = models.SmallIntegerField(blank=True, null=True)
    iata = models.SmallIntegerField(blank=True, null=True)
    idinternacional = models.CharField(max_length=5, blank=True, null=True)
    cuit = models.CharField(max_length=20, blank=True, null=True)
    cartelef = models.SmallIntegerField(blank=True, null=True)
    edi = models.CharField(db_column='EDI', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_paises'


class MantenimientosPasssocios(models.Model):
    pnombre = models.CharField(db_column='Pnombre', max_length=30, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_passsocios'


class MantenimientosPassword(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_password'


class MantenimientosPasswordhistorial(models.Model):
    pnombre = models.CharField(max_length=30, blank=True, null=True)
    pword = models.CharField(max_length=30, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_passwordhistorial'


class MantenimientosPermisosterr(models.Model):
    cliente = models.IntegerField(db_column='Cliente', blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=30, blank=True, null=True)  # Field name made lowercase.
    peroriginal = models.CharField(db_column='PerOriginal', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.
    percomplem = models.CharField(db_column='PerComplem', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    contrif = models.CharField(db_column='Contrif', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_permisosterr'


class MantenimientosPrefijos(models.Model):
    prefijo = models.CharField(max_length=2, blank=True, null=True)
    detalle = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimientos_prefijos'


class MantenimientosProductos(models.Model):
    codigo = models.SmallIntegerField()
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_productos'


class MantenimientosProvincias(models.Model):
    codigo = models.IntegerField(db_column='Codigo', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pais = models.CharField(db_column='Pais', max_length=50, blank=True, null=True)  # Field name made lowercase.
    abreviacion = models.CharField(db_column='Abreviacion', max_length=10, blank=True,
                                   null=True)  # Field name made lowercase.
    referencia = models.CharField(db_column='Referencia', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_provincias'


class MantenimientosProyectos(models.Model):
    codigo = models.SmallIntegerField(db_column='Codigo', unique=True, blank=True,
                                      null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_proyectos'


class MantenimientosRetenciones(models.Model):
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
    suma = models.IntegerField(db_column='Suma', blank=True, null=True)  # Field name made lowercase.
    basemaxima = models.FloatField(db_column='BaseMaxima', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_retenciones'


class MantenimientosServicios(models.Model):
    codigo = models.SmallIntegerField()
    nombre = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    gravado = models.SmallIntegerField(blank=True, null=True)
    tasa = models.CharField(max_length=1, blank=True, null=True)
    refparam = models.SmallIntegerField(blank=True, null=True)
    prefijo = models.CharField(max_length=10, blank=True, null=True)
    contable = models.BigIntegerField(blank=True, null=True)
    contiva = models.IntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    imputar = models.CharField(max_length=1, blank=True, null=True)
    tipogasto = models.CharField(max_length=1, blank=True, null=True)
    variable = models.IntegerField()
    tipovariable = models.CharField(max_length=1, blank=True, null=True)
    variablecada = models.FloatField(blank=True, null=True)
    redondea = models.IntegerField()
    baseminima = models.FloatField(blank=True, null=True)
    ctaorden = models.IntegerField()
    modo = models.CharField(max_length=1, blank=True, null=True)
    ibruto = models.IntegerField()
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
    ctaordeniva = models.IntegerField()
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_servicios'


class MantenimientosServrelacion(models.Model):
    codigovta = models.SmallIntegerField(db_column='CodigoVTA', blank=True, null=True)  # Field name made lowercase.
    codigocpa = models.SmallIntegerField(db_column='CodigoCPA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_servrelacion'


class MantenimientosServvariables(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_servvariables'


class MantenimientosSociosweb(models.Model):
    codigo = models.IntegerField(db_column='Codigo', blank=True, null=True)  # Field name made lowercase.
    codigoweb = models.IntegerField(db_column='CodigoWeb', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_sociosweb'


class MantenimientosStatus(models.Model):
    status = models.CharField(max_length=20, blank=True, null=True)
    costos = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimientos_status'


class MantenimientosStatussocios(models.Model):
    numero = models.SmallIntegerField(unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimientos_statussocios'


class MantenimientosSucursales(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_sucursales'


class MantenimientosSucursalesargentina(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_sucursalesargentina'


class MantenimientosSucursalesbrasil(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_sucursalesbrasil'


class MantenimientosSucursaleschile(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_sucursaleschile'


class MantenimientosSucursalesdominicana(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_sucursalesdominicana'


class MantenimientosSucursalesmexico(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_sucursalesmexico'


class MantenimientosSucursalesparaguay(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_sucursalesparaguay'


class MantenimientosSucursalesperu(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_sucursalesperu'


class MantenimientosSucursalesuruguay(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_sucursalesuruguay'


class MantenimientosSucursalesusa(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_sucursalesusa'


class MantenimientosSysregisedits(models.Model):
    numerolic = models.IntegerField(db_column='NumeroLic', unique=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    equipo = models.CharField(db_column='Equipo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    registro = models.CharField(db_column='Registro', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
    vigencia = models.DateTimeField(db_column='Vigencia', blank=True, null=True)  # Field name made lowercase.
    estado = models.SmallIntegerField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_sysregisedits'


class MantenimientosTextos(models.Model):
    deposito = models.TextField(blank=True, null=True)
    agente = models.TextField(blank=True, null=True)
    cliente = models.TextField(blank=True, null=True)
    cotizaim = models.TextField(blank=True, null=True)
    cotizaia = models.TextField(blank=True, null=True)
    cotizaem = models.TextField(blank=True, null=True)
    cotizaea = models.TextField(blank=True, null=True)
    clienteia = models.TextField(blank=True, null=True)
    clienteit = models.TextField(blank=True, null=True)
    cotizait = models.TextField(blank=True, null=True)
    cotizaet = models.TextField(blank=True, null=True)
    clienteexa = models.TextField(blank=True, null=True)
    clienteexm = models.TextField(blank=True, null=True)
    clienteext = models.TextField(blank=True, null=True)
    cotgenerica = models.TextField(blank=True, null=True)
    seguircli = models.TextField(blank=True, null=True)
    seguirclii = models.TextField(blank=True, null=True)
    seguirage = models.TextField(blank=True, null=True)
    seguiragei = models.TextField(blank=True, null=True)
    general = models.TextField(blank=True, null=True)
    booking = models.TextField(db_column='Booking', blank=True, null=True)  # Field name made lowercase.
    textoaging = models.TextField(db_column='TextoAging', blank=True, null=True)  # Field name made lowercase.
    textoestadocuenta = models.TextField(db_column='TextoEstadoCuenta', blank=True,
                                         null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_textos'


class MantenimientosTipoindustria(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=150, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_tipoindustria'


class MantenimientosTipooperacion(models.Model):
    numero = models.SmallIntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=150, blank=True, null=True)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_tipooperacion'


class MantenimientosTrace(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_trace'


class MantenimientosTraceinterface(models.Model):
    fechahora = models.DateTimeField(db_column='FechaHora', blank=True, null=True)  # Field name made lowercase.
    embarque = models.IntegerField(db_column='Embarque', blank=True, null=True)  # Field name made lowercase.
    orden = models.CharField(db_column='Orden', max_length=500, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cliente = models.CharField(db_column='Cliente', max_length=50, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=500, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_traceinterface'


class MantenimientosTrackingdetalles(models.Model):
    usuario = models.IntegerField(db_column='Usuario', blank=True, null=True)  # Field name made lowercase.
    idsociocomercial = models.IntegerField(db_column='IDSocioComercial', blank=True,
                                           null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_trackingdetalles'


class MantenimientosTrackinglogin(models.Model):
    sociocomercial = models.IntegerField(db_column='SocioComercial', blank=True,
                                         null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fechain = models.DateTimeField(db_column='FechaIN', blank=True, null=True)  # Field name made lowercase.
    fechaout = models.DateTimeField(db_column='FechaOUT', blank=True, null=True)  # Field name made lowercase.
    horain = models.CharField(db_column='HoraIN', max_length=5, blank=True, null=True)  # Field name made lowercase.
    horaout = models.CharField(db_column='HoraOUT', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_trackinglogin'


class MantenimientosTrackingterceros(models.Model):
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

    class Meta:
        managed = False
        db_table = 'mantenimientos_trackingterceros'


class MantenimientosTrackingusuarios(models.Model):
    codsociocomercial = models.IntegerField(db_column='CodSocioComercial', blank=True,
                                            null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=12, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=12, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_trackingusuarios'


class MantenimientosTraficos(models.Model):
    codigo = models.SmallIntegerField(unique=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    diasim = models.SmallIntegerField(db_column='DiasIM', blank=True, null=True)  # Field name made lowercase.
    diasia = models.SmallIntegerField(db_column='DiasIA', blank=True, null=True)  # Field name made lowercase.
    diasit = models.SmallIntegerField(db_column='DiasIT', blank=True, null=True)  # Field name made lowercase.
    diasem = models.SmallIntegerField(db_column='DiasEM', blank=True, null=True)  # Field name made lowercase.
    diasea = models.SmallIntegerField(db_column='DiasEA', blank=True, null=True)  # Field name made lowercase.
    diaset = models.SmallIntegerField(db_column='DiasET', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_traficos'


class MantenimientosVapores(models.Model):
    codigo = models.SmallIntegerField(unique=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    bandera = models.CharField(max_length=50, blank=True, null=True)
    deposito = models.SmallIntegerField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    imo = models.CharField(db_column='IMO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fechaactualizado = models.DateTimeField(db_column='FechaActualizado', blank=True,
                                            null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_vapores'


class MantenimientosVendedores(models.Model):
    codigo = models.SmallIntegerField(unique=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    cpostal = models.CharField(max_length=10, blank=True, null=True)
    ciudad = models.CharField(max_length=5, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    condiciones = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
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
        managed = False
        db_table = 'mantenimientos_vendedores'


class MantenimientosVuelos(models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    vuelo = models.CharField(db_column='Vuelo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=5, blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    horaorigen = models.CharField(db_column='HoraOrigen', max_length=8, blank=True,
                                  null=True)  # Field name made lowercase.
    horadestino = models.CharField(db_column='HoraDestino', max_length=8, blank=True,
                                   null=True)  # Field name made lowercase.
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)  # Field name made lowercase.
    lunes = models.CharField(db_column='Lunes', max_length=1, blank=True, null=True)  # Field name made lowercase.
    martes = models.CharField(db_column='Martes', max_length=1, blank=True, null=True)  # Field name made lowercase.
    miercoles = models.CharField(db_column='Miercoles', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    jueves = models.CharField(db_column='Jueves', max_length=1, blank=True, null=True)  # Field name made lowercase.
    viernes = models.CharField(db_column='Viernes', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sabado = models.CharField(db_column='Sabado', max_length=1, blank=True, null=True)  # Field name made lowercase.
    domingo = models.CharField(db_column='Domingo', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mantenimientos_vuelos'


class SeguimientosAttachhijo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    restringido = models.CharField(db_column='Restringido', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    idbinaryattach = models.IntegerField(db_column='IdBinaryAttach', blank=True,
                                         null=True)  # Field name made lowercase.
    idusuario = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seguimientos_attachhijo'


class SeguimientosAttachhijopo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    archivo = models.CharField(max_length=250, blank=True, null=True)
    detalle = models.CharField(max_length=50, blank=True, null=True)
    web = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_attachhijopo'


class SeguimientosBl(models.Model):
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
    goods = models.TextField(db_column='Goods', blank=True, null=True)  # Field name made lowercase.
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
    vadeclared = models.IntegerField(db_column='VaDeclared', blank=True, null=True)  # Field name made lowercase.
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
    consolidado = models.IntegerField(db_column='Consolidado', blank=True, null=True)  # Field name made lowercase.
    mensaje1 = models.IntegerField(db_column='Mensaje1', blank=True, null=True)  # Field name made lowercase.
    mensaje2 = models.IntegerField(db_column='Mensaje2', blank=True, null=True)  # Field name made lowercase.
    label6 = models.CharField(db_column='Label6', max_length=50, blank=True, null=True)  # Field name made lowercase.
    texto = models.TextField(db_column='Texto', blank=True, null=True)  # Field name made lowercase.
    consigna6 = models.CharField(db_column='Consigna6', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    consigna7 = models.CharField(db_column='Consigna7', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    consigna8 = models.CharField(db_column='Consigna8', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    precarriage = models.CharField(db_column='PreCarriage', max_length=35, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_bl'


class SeguimientosBl2(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    marks = models.CharField(db_column='Marks', max_length=30, blank=True, null=True)  # Field name made lowercase.
    packages = models.CharField(db_column='Packages', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    gross = models.CharField(db_column='Gross', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tare = models.CharField(db_column='Tare', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_bl2'


class SeguimientosBl3(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    servicio = models.CharField(db_column='Servicio', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    prepaid = models.CharField(db_column='Prepaid', max_length=10, blank=True, null=True)  # Field name made lowercase.
    collect = models.CharField(db_column='Collect', max_length=10, blank=True, null=True)  # Field name made lowercase.
    moneda = models.CharField(db_column='Moneda', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_bl3'


class SeguimientosBookenv(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    marks = models.CharField(max_length=30, blank=True, null=True)
    packages = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    gross = models.CharField(max_length=30, blank=True, null=True)
    tare = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seguimientos_bookenv'


class SeguimientosBooking(models.Model):
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
    contactoterminal = models.CharField(db_column='ContactoTerminal', max_length=30, blank=True,
                                        null=True)  # Field name made lowercase.
    bandera = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seguimientos_booking'


class SeguimientosBooking2(models.Model):
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
    net = models.TextField(blank=True, null=True)
    sold = models.TextField(blank=True, null=True)
    profit = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    vaporcli2 = models.IntegerField()
    vaporcli = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'seguimientos_booking2'


class SeguimientosCabezalocc(models.Model):
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
    notas = models.TextField(blank=True, null=True)
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

    class Meta:
        managed = False
        db_table = 'seguimientos_cabezalocc'


class SeguimientosCargaaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    producto = models.SmallIntegerField(blank=True, null=True)
    bultos = models.IntegerField(blank=True, null=True)
    bruto = models.FloatField(blank=True, null=True)
    medidas = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=25, blank=True, null=True)
    cbm = models.FloatField(blank=True, null=True)
    mercaderia = models.TextField(db_column='Mercaderia', blank=True, null=True)  # Field name made lowercase.
    marcas = models.CharField(db_column='Marcas', max_length=150, blank=True, null=True)  # Field name made lowercase.
    nrocontenedor = models.CharField(db_column='NroContenedor', max_length=15, blank=True,
                                     null=True)  # Field name made lowercase.
    materialreceipt = models.CharField(db_column='MaterialReceipt', max_length=30, blank=True,
                                       null=True)  # Field name made lowercase.
    sobredimensionada = models.CharField(db_column='Sobredimensionada', max_length=1, blank=True,
                                         null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_cargaaerea'


class SeguimientosCargaaereaaduana(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_cargaaereaaduana'


class SeguimientosClaveguia(models.Model):
    awb = models.CharField(db_column='AWB', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_claveguia'


class SeguimientosClavehawb(models.Model):
    hawb = models.CharField(db_column='HAWB', max_length=25)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_clavehawb'


class SeguimientosClaveposicion(models.Model):
    posicion = models.CharField(db_column='Posicion', max_length=15)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_claveposicion'


class SeguimientosConexaerea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    salida = models.DateTimeField(blank=True, null=True)
    llegada = models.DateTimeField(blank=True, null=True)
    cia = models.CharField(max_length=30, blank=True, null=True)
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(max_length=15, blank=True, null=True)
    accion = models.CharField(db_column='Accion', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_conexaerea'


class SeguimientosConexreserva(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(db_column='Origen', max_length=5, blank=True, null=True)  # Field name made lowercase.
    destino = models.CharField(db_column='Destino', max_length=5, blank=True, null=True)  # Field name made lowercase.
    vapor = models.CharField(db_column='Vapor', max_length=30, blank=True, null=True)  # Field name made lowercase.
    salida = models.DateTimeField(db_column='Salida', blank=True, null=True)  # Field name made lowercase.
    llegada = models.DateTimeField(db_column='Llegada', blank=True, null=True)  # Field name made lowercase.
    cia = models.CharField(db_column='Cia', max_length=30, blank=True, null=True)  # Field name made lowercase.
    viaje = models.CharField(db_column='Viaje', max_length=10, blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(db_column='Modo', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_conexreserva'


class SeguimientosCronologia(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_cronologia'


class SeguimientosCrt(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_crt'


class SeguimientosCrt2(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=55, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_crt2'


class SeguimientosDetalleocc(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_detalleocc'


class SeguimientosEntregadoc(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_entregadoc'


class SeguimientosEntregaorden(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_entregaorden'


class SeguimientosEntregasocc(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_entregasocc'


class SeguimientosEnvases(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=25, blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    movimiento = models.CharField(max_length=30, blank=True, null=True)
    terminos = models.CharField(max_length=5, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    marcas = models.CharField(max_length=50, blank=True, null=True)
    precinto = models.CharField(max_length=100, blank=True, null=True)
    tara = models.FloatField(blank=True, null=True)
    bonifcli = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    envase = models.CharField(db_column='Envase', max_length=15, blank=True, null=True)  # Field name made lowercase.
    bultos = models.IntegerField(blank=True, null=True)
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    profit = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    nrocontenedor = models.CharField(max_length=100, blank=True, null=True)
    volumen = models.FloatField(db_column='Volumen', blank=True, null=True)  # Field name made lowercase.
    temperatura = models.FloatField(db_column='Temperatura', blank=True, null=True)  # Field name made lowercase.
    activo = models.CharField(db_column='Activo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadtemp = models.CharField(db_column='UnidadTemp', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
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
    genset = models.CharField(db_column='GenSet', max_length=1, blank=True, null=True)  # Field name made lowercase.
    atmosferacontrolada = models.CharField(db_column='AtmosferaControlada', max_length=1, blank=True,
                                           null=True)  # Field name made lowercase.
    consolidacion = models.SmallIntegerField(db_column='Consolidacion', blank=True,
                                             null=True)  # Field name made lowercase.
    tipoventilacion = models.CharField(db_column='TipoVentilacion', max_length=1, blank=True,
                                       null=True)  # Field name made lowercase.
    pesovgm = models.FloatField(db_column='PesoVGM', blank=True, null=True)  # Field name made lowercase.
    humedad = models.SmallIntegerField(db_column='Humedad', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_envases'


class SeguimientosFaxes(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seguimientos_faxes'


class SeguimientosFaxesoc(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seguimientos_faxesoc'


class SeguimientosFisico(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_fisico'


class SeguimientosGastoshijos(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_gastoshijos'


class SeguimientosGuiasgrabadas(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_guiasgrabadas'


class SeguimientosGuiasgrabadas2(models.Model):
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
    gastosconiva = models.IntegerField(db_column='GastosconIva', blank=True, null=True)  # Field name made lowercase.
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

    class Meta:
        managed = False
        db_table = 'seguimientos_guiasgrabadas2'


class SeguimientosGuiasgrabadas3(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_guiasgrabadas3'


class SeguimientosMadresgrabadas(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_madresgrabadas'


class SeguimientosMadresgrabadas3(models.Model):
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

    class Meta:
        managed = False
        db_table = 'seguimientos_madresgrabadas3'


class SeguimientosMbl(models.Model):
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
    goods = models.TextField(db_column='Goods', blank=True, null=True)  # Field name made lowercase.
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
    vadeclared = models.IntegerField(db_column='VaDeclared', blank=True, null=True)  # Field name made lowercase.
    portext = models.CharField(db_column='PorText', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_mbl'


class SeguimientosMbl2(models.Model):
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.
    marks = models.CharField(db_column='Marks', max_length=30, blank=True, null=True)  # Field name made lowercase.
    packages = models.CharField(db_column='Packages', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    gross = models.CharField(db_column='Gross', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tare = models.CharField(db_column='Tare', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_mbl2'


class SeguimientosReservas(models.Model):
    numero = models.IntegerField()
    transportista = models.IntegerField(blank=True, null=True)
    armador = models.IntegerField(blank=True, null=True)
    agente = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    awb = models.CharField(max_length=40, blank=True, null=True)
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

    class Meta:
        managed = False
        db_table = 'seguimientos_reservas'


class SeguimientosSeguimiento(models.Model):
    numero = models.IntegerField()
    cliente = models.ForeignKey(MantenimientosClientes, models.DO_NOTHING, db_column='cliente', to_field='codigo',
                                blank=True, null=True)
    consignatario = models.ForeignKey(MantenimientosClientes, models.DO_NOTHING, db_column='consignatario',
                                      to_field='codigo', related_name='seguimientosseguimiento_consignatario_set',
                                      blank=True, null=True)
    origen = models.ForeignKey(MantenimientosCiudades, models.DO_NOTHING, db_column='origen', to_field='codigo',
                               blank=True, null=True)
    destino = models.ForeignKey(MantenimientosCiudades, models.DO_NOTHING, db_column='destino', to_field='codigo',
                                related_name='seguimientosseguimiento_destino_set', blank=True, null=True)
    terminos = models.CharField(max_length=3, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    agente = models.ForeignKey(MantenimientosClientes, models.DO_NOTHING, db_column='agente', to_field='codigo',
                               related_name='seguimientosseguimiento_agente_set', blank=True, null=True)
    embarcador = models.ForeignKey(MantenimientosClientes, models.DO_NOTHING, db_column='Embarcador', to_field='codigo',
                                   related_name='seguimientosseguimiento_embarcador_set', blank=True,
                                   null=True)  # Field name made lowercase.
    vaporcli = models.IntegerField(db_column='Vaporcli', blank=True, null=True)  # Field name made lowercase.
    modo = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    vencimiento = models.DateTimeField(blank=True, null=True)
    embarque = models.IntegerField(blank=True, null=True)
    vapor = models.CharField(max_length=30, blank=True, null=True)
    awb = models.CharField(max_length=40, blank=True, null=True)
    hawb = models.CharField(max_length=40, blank=True, null=True)
    volumen = models.FloatField(blank=True, null=True)
    tarifaventa = models.FloatField(blank=True, null=True)
    tarifacompra = models.FloatField(blank=True, null=True)
    pago = models.CharField(max_length=10, blank=True, null=True)
    refcliente = models.CharField(max_length=1024, blank=True, null=True)
    transportista = models.ForeignKey(MantenimientosClientes, models.DO_NOTHING, db_column='transportista',
                                      to_field='codigo', related_name='seguimientosseguimiento_transportista_set',
                                      blank=True, null=True)
    posicion = models.CharField(max_length=30, blank=True, null=True)
    cotizacion = models.IntegerField(blank=True, null=True)
    cotizacion1 = models.IntegerField(blank=True, null=True)
    vaporcli2 = models.CharField(max_length=1, blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    vendedor = models.ForeignKey(MantenimientosVendedores, models.DO_NOTHING, db_column='vendedor', to_field='codigo',
                                 blank=True, null=True)
    despachante = models.IntegerField(blank=True, null=True)
    agecompras = models.ForeignKey(MantenimientosClientes, models.DO_NOTHING, db_column='agecompras', to_field='codigo',
                                   related_name='seguimientosseguimiento_agecompras_set', blank=True, null=True)
    ageventas = models.ForeignKey(MantenimientosClientes, models.DO_NOTHING, db_column='ageventas', to_field='codigo',
                                  related_name='seguimientosseguimiento_ageventas_set', blank=True, null=True)
    deposito = models.ForeignKey(MantenimientosDepositos, models.DO_NOTHING, db_column='deposito', to_field='codigo',
                                 blank=True, null=True)
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
    armador = models.ForeignKey(MantenimientosClientes, models.DO_NOTHING, db_column='armador', to_field='codigo',
                                related_name='seguimientosseguimiento_armador_set', blank=True, null=True)
    notificar = models.ForeignKey(MantenimientosClientes, models.DO_NOTHING, db_column='Notificar', to_field='codigo',
                                  related_name='seguimientosseguimiento_notificar_set', blank=True,
                                  null=True)  # Field name made lowercase.
    fechaonhand = models.DateTimeField(db_column='FechaOnHand', blank=True, null=True)  # Field name made lowercase.
    booking = models.CharField(max_length=30, blank=True, null=True)
    propia = models.CharField(db_column='Propia', max_length=1, blank=True, null=True)  # Field name made lowercase.
    trafico = models.ForeignKey(MantenimientosTraficos, models.DO_NOTHING, db_column='Trafico', to_field='codigo',
                                blank=True, null=True)  # Field name made lowercase.
    proyecto = models.ForeignKey(MantenimientosProyectos, models.DO_NOTHING, db_column='Proyecto', to_field='codigo',
                                 blank=True, null=True)  # Field name made lowercase.
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
    loading = models.CharField(db_column='Loading', max_length=35, blank=True, null=True)  # Field name made lowercase.
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
    actividad = models.ForeignKey(MantenimientosActividades, models.DO_NOTHING, db_column='Actividad',
                                  to_field='numero', blank=True, null=True)  # Field name made lowercase.
    entregadoa = models.CharField(db_column='EntregadoA', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    loadingdate = models.DateTimeField(db_column='LoadingDate', blank=True, null=True)  # Field name made lowercase.
    diasalmacenaje = models.SmallIntegerField(db_column='DiasAlmacenaje', blank=True,
                                              null=True)  # Field name made lowercase.
    muestroflete = models.DecimalField(db_column='MuestroFlete', max_digits=19, decimal_places=4, blank=True,
                                       null=True)  # Field name made lowercase.
    operacion = models.CharField(db_column='Operacion', max_length=25, blank=True,
                                 null=True)  # Field name made lowercase.
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

    class Meta:
        managed = False
        db_table = 'seguimientos_seguimiento'


class SeguimientosServiceaereo(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    secomparte = models.CharField(max_length=1, blank=True, null=True)
    notomaprofit = models.IntegerField()
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.
    socio = models.IntegerField(db_column='Socio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_serviceaereo'


class SeguimientosServireserva(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    servicio = models.SmallIntegerField(blank=True, null=True)
    moneda = models.SmallIntegerField(blank=True, null=True)
    modo = models.CharField(max_length=1, blank=True, null=True)
    costo = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    detalle = models.CharField(max_length=100, blank=True, null=True)
    tipogasto = models.CharField(max_length=30, blank=True, null=True)
    arbitraje = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notomaprofit = models.IntegerField()
    repartir = models.CharField(max_length=1, blank=True, null=True)
    pinformar = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    notas = models.CharField(db_column='Notas', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_servireserva'


class SeguimientosTraceop(models.Model):
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    nomusuario = models.CharField(db_column='NomUsuario', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    modulo = models.CharField(db_column='Modulo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    detalle = models.CharField(db_column='Detalle', max_length=250, blank=True, null=True)  # Field name made lowercase.
    formulario = models.CharField(db_column='Formulario', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    clave = models.CharField(db_column='Clave', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seguimientos_traceop'


class PendienteFacturar(models.Model):
    autogenerado = models.CharField(max_length=40, blank=True, null=True)

    def save(self, *args, **kwargs):
        from administracion_contabilidad.views.facturacion import facturar_pendiente
        es_nuevo = self.pk is None  # Verifica si es una nueva instancia (sin ID asignada)

        super().save(*args, **kwargs)  # Guarda el objeto en la base de datos

        if es_nuevo:
            facturar_pendiente(self.autogenerado)
