# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from auditlog.models import AuditlogHistoryField
from django.db import models
from django.db.models import Max



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
        asiento = Asientos.objects.last()
        return int(asiento.id + 1)


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

    def __str__(self):
        return f"{self.xcodigo} - {self.xnombre}"


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
    ui = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
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

    def get_id(self):
        lista = Factudif.objects.last()
        return int(lista.id + 1)

    def get_num(self):
        lista = Factudif.objects.last()
        return int(lista.znumero + 1)

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
    id = models.IntegerField(primary_key=True)
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
        lista = Infofactura.objects.last()
        return int(lista.id + 1)


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
        mov = Movims.objects.last()
        return int(mov.id + 1)


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
    id = models.IntegerField(primary_key=True)
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

    def get_next_mboleta(self):
        current = Ordenes.objects.aggregate(maximo=Max('mboleta'))['maximo'] or 0
        next_mboleta = current + 1

        while Ordenes.objects.filter(mboleta=next_mboleta).exists():
            next_mboleta += 1

        return next_mboleta

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



class VistaGastosPreventa(models.Model):
    numero = models.CharField(max_length=255, blank=True, null=True)
    servicio = models.CharField(max_length=255, blank=True, null=True)
    cuenta = models.CharField(max_length=255, blank=True, null=True)
    moneda = models.CharField(max_length=255, blank=True, null=True)
    modo = models.CharField(max_length=10, blank=True, null=True)
    precio = models.FloatField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    detalle = models.CharField(max_length=255, blank=True, null=True)
    tipogasto = models.CharField(max_length=255, blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    notomaprofit = models.CharField(max_length=2, blank=True, null=True)
    secomparte = models.CharField(max_length=2, blank=True, null=True)
    Notas = models.CharField(max_length=255, blank=True, null=True)
    pinformar = models.CharField(max_length=255, blank=True, null=True)
    socio = models.CharField(max_length=255, blank=True, null=True)
    id_servicio = models.CharField(max_length=255, blank=True, null=True)
    id_moneda = models.CharField(max_length=255, blank=True, null=True)
    id_socio = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=2, blank=True, null=True)
    iva = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vista_gastos_preventa'


class ListaCobranzas(models.Model):
    autogenerado = models.CharField(primary_key=True, max_length=50)
    numero = models.CharField(max_length=50, null=True, blank=True)
    nrocliente = models.CharField(max_length=50, null=True, blank=True)
    posicion = models.CharField(max_length=50, null=True, blank=True)
    detalle = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField()
    cliente = models.CharField(max_length=50, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        managed = False  # Indicates that this model represents a database view
        db_table = 'lista_cobranzas'

class VistaProveedoresygastos(models.Model):
    autogenerado = models.CharField(primary_key=True, max_length=50)
    numero = models.CharField(max_length=50, null=True, blank=True)
    prefijo = models.CharField(max_length=50, null=True, blank=True)
    serie = models.CharField(max_length=50, null=True, blank=True)
    num_completo = models.CharField(max_length=50, null=True, blank=True)
    nrocliente = models.CharField(max_length=50, null=True, blank=True)
    cliente = models.CharField(max_length=50, null=True, blank=True)
    detalle = models.TextField(null=True, blank=True)
    tipo = models.CharField(max_length=50, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_cambio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paridad = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha = models.DateTimeField(null=True, blank=True)
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    fecha_ingreso = models.DateTimeField(null=True, blank=True)
    moneda = models.CharField(max_length=50, null=True, blank=True)
    posicion = models.CharField(max_length=50, null=True, blank=True)
    nombre_moneda = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        managed = False  # Indicates that this model represents a database view
        db_table = 'vista_proveedoresypagos'

class VistaVentas(models.Model):
    autogenerado = models.CharField(primary_key=True, max_length=50)
    numero = models.CharField(max_length=50, null=True, blank=True)
    prefijo = models.CharField(max_length=50, null=True, blank=True)
    serie = models.CharField(max_length=50, null=True, blank=True)
    num_completo = models.CharField(max_length=50, null=True, blank=True)
    nrocliente = models.CharField(max_length=50, null=True, blank=True)
    cliente = models.CharField(max_length=50, null=True, blank=True)
    detalle = models.TextField(null=True, blank=True)
    tipo = models.CharField(max_length=50, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_cambio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paridad = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha = models.DateTimeField(null=True, blank=True)
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    fecha_ingreso = models.DateTimeField(null=True, blank=True)
    moneda = models.CharField(max_length=50, null=True, blank=True)
    posicion = models.CharField(max_length=50, null=True, blank=True)
    nombre_moneda = models.CharField(max_length=50, null=True, blank=True)
    cae = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        managed = False  # Indicates that this model represents a database view
        db_table = 'vista_ventas'


class VistaOrdenesPago(models.Model):
    autogenerado = models.CharField(primary_key=True, max_length=50)
    num_completo = models.CharField(max_length=50, null=True, blank=True)
    nrocliente = models.CharField(max_length=50, null=True, blank=True)
    cliente = models.CharField(max_length=50, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha = models.DateTimeField(null=True, blank=True)
    posicion = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        managed = False  # Indicates that this model represents a database view
        db_table = 'vista_ordenes_pago'

class VistaPagos(models.Model):
    autogenerado = models.CharField(primary_key=True, max_length=50)
    nrocliente = models.IntegerField()
    cliente = models.CharField( max_length=50)
    moneda = models.CharField( max_length=50)
    documento = models.CharField(max_length=50, null=True, blank=True)
    serie = models.CharField(max_length=50, null=True, blank=True)
    prefijo = models.CharField(max_length=50, null=True, blank=True)
    tipo_factura = models.TextField(null=True, blank=True)
    iva = models.CharField(max_length=50, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False  # Indicates that this model represents a database view
        db_table = 'vista_pagos'


class VPreventas(models.Model):
    id = models.AutoField(primary_key=True)
    znumero = models.CharField(max_length=255, null=True, blank=True)
    zmoneda = models.CharField(max_length=50, null=True, blank=True)
    zcliente = models.CharField(max_length=255, null=True, blank=True)
    ztipo = models.CharField(max_length=50, null=True, blank=True)
    zitem = models.CharField(max_length=255, null=True, blank=True)
    zmonto = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    ziva = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    zrefer = models.CharField(max_length=255, null=True, blank=True)
    zcarrier = models.CharField(max_length=255, null=True, blank=True)
    zmaster = models.CharField(max_length=255, null=True, blank=True)
    zdate = models.DateTimeField(null=True, blank=True)
    zhouse = models.CharField(max_length=255, null=True, blank=True)
    zposicion = models.CharField(max_length=255, null=True, blank=True)
    zkilos = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    zbultos = models.IntegerField(null=True, blank=True)
    zvolumen = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    zorigen = models.CharField(max_length=255, null=True, blank=True)
    zdestino = models.CharField(max_length=255, null=True, blank=True)
    zdetalle = models.TextField(null=True, blank=True)
    ztransporte = models.CharField(max_length=255, null=True, blank=True)
    zclase = models.CharField(max_length=50, null=True, blank=True)
    zllegasale = models.DateTimeField(null=True, blank=True)
    zobs1 = models.TextField(null=True, blank=True)
    zobs2 = models.TextField(null=True, blank=True)
    zobs3 = models.TextField(null=True, blank=True)
    zobs4 = models.TextField(null=True, blank=True)
    zobs5 = models.TextField(null=True, blank=True)
    zcommodity = models.CharField(max_length=255, null=True, blank=True)
    zembarcador = models.CharField(max_length=255, null=True, blank=True)
    zconsignatario = models.CharField(max_length=255, null=True, blank=True)
    zmonedaorigen = models.CharField(max_length=50, null=True, blank=True)
    zarbitraje = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    zorden = models.CharField(max_length=255, null=True, blank=True)
    zvalororiginal = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    zseguimiento = models.CharField(max_length=255, null=True, blank=True)
    zagente = models.CharField(max_length=255, null=True, blank=True)
    zcontrolado = models.BooleanField(default=False)
    zusuario = models.CharField(max_length=255, null=True, blank=True)
    zfechagen = models.DateTimeField(null=True, blank=True)
    zaplicable = models.BooleanField(default=False)
    zvendedor = models.CharField(max_length=255, null=True, blank=True)
    zwr = models.CharField(max_length=255, null=True, blank=True)
    znotas = models.TextField(null=True, blank=True)
    zcambiousdpactado = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    zpagoflete = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    zterminos = models.CharField(max_length=255, null=True, blank=True)
    zfacturado = models.BooleanField(default=False, null=True, blank=True)
    zop = models.CharField(max_length=255, null=True, blank=True)
    nrofolio = models.CharField(max_length=255, null=True, blank=True)
    dtefechaorden = models.DateTimeField(null=True, blank=True)
    srazonreforden = models.TextField(null=True, blank=True)
    zfechafacturado = models.DateTimeField(null=True, blank=True)
    zboletafactura = models.CharField(max_length=255, null=True, blank=True)
    zautogenenvase = models.CharField(max_length=255, null=True, blank=True)
    zfechaaprobada = models.DateTimeField(null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    jurisdiccion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'VPreventas'

class VItemsCompra(models.Model):
    concepto = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=50, null=True, blank=True)
    precio = models.CharField(max_length=50, null=True, blank=True)
    iva = models.CharField(max_length=50, null=True, blank=True)
    posicion = models.CharField(max_length=50, null=True, blank=True)
    autogenerado = models.CharField(max_length=50, null=True, blank=True)
    imputar = models.CharField(max_length=50, null=True, blank=True)
    imputacion = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'VItemsCompra'

class VItemsVenta(models.Model):
    concepto = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=50, null=True, blank=True)
    precio = models.CharField(max_length=50, null=True, blank=True)
    iva = models.CharField(max_length=50, null=True, blank=True)
    posicion = models.CharField(max_length=50, null=True, blank=True)
    autogenerado = models.CharField(max_length=50, null=True, blank=True)
    imputar = models.CharField(max_length=50, null=True, blank=True)
    imputacion = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        managed = False  # Indicates that this model represents a database view
        db_table = 'VItemsVenta'
class VistaCobranza(models.Model):
    autogenerado = models.CharField(max_length=40,primary_key=True)
    tipo = models.CharField(max_length=8, null=True, blank=True)
    emision = models.DateTimeField(null=True, blank=True)
    vencimiento = models.DateTimeField(null=True, blank=True)
    nrocliente = models.IntegerField(null=True, blank=True)
    cliente = models.CharField(max_length=50, null=True, blank=True)
    embarque = models.CharField(max_length=30, null=True, blank=True)
    total = models.DecimalField(null=True, blank=True,decimal_places=4,max_digits=4)
    moneda = models.CharField(max_length=10, null=True, blank=True)
    arbitraje = models.CharField(max_length=21, null=True, blank=True)
    paridad = models.DecimalField(null=True, blank=True, decimal_places=4,max_digits=4)
    posicion = models.CharField(max_length=30, null=True, blank=True)
    documento = models.CharField(max_length=22, null=True, blank=True)
    tipo_doc = models.CharField(max_length=20, null=True, blank=True)
    detalle = models.CharField(max_length=200, null=True, blank=True)
    source = models.CharField(max_length=8, null=True, blank=True)
    saldo = models.DecimalField(null=True, blank=True,decimal_places=4,max_digits=4)
    pago = models.DecimalField(null=True, blank=True,decimal_places=4,max_digits=4)
    class Meta:
        managed = False
        db_table = 'vista_cobranza'

class VChequesDiferidosBajar(models.Model):
    autogenerado = models.CharField(max_length=50,primary_key=True)
    fecha = models.DateField()
    vto = models.DateField(null=True, blank=True)
    documento = models.IntegerField()
    tipo = models.CharField(max_length=1)  # Por ejemplo: 'B', 'T'
    detalle = models.TextField()
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    mov = models.CharField(max_length=50, null=True, blank=True)
    cambio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    paridad = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    cuenta = models.IntegerField()
    banco = models.CharField(max_length=50)

    class Meta:
        db_table = 'VChequesDiferidosBajar'


"""
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

class MyModel(models.Model):
    history = AuditlogHistoryField()
    # Model definition goes here


auditlog.register(MyModel)

from inspect import getmembers
from auditlog.registry import auditlog
from administracion_contabilidad import models

tablas = getmembers(models)
for t in tablas:
    try:
        auditlog.register(t[1], serialize_data=True)
    except Exception as e:
        pass
"""



from auditlog.registry import auditlog

class MyModel(models.Model):
    history = AuditlogHistoryField()
    # Model definition goes here


auditlog.register(MyModel)

from inspect import getmembers
from auditlog.registry import auditlog
from administracion_contabilidad import models

tablas = getmembers(models)
for t in tablas:
    try:
        auditlog.register(t[1], serialize_data=True)
    except Exception as e:
        pass