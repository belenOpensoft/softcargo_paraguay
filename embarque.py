from django.db import models


class Reservas (models.Model):
    numero = models.IntegerField(db_column='Numero', unique=True)  # Field name made lowercase.
    transportista = models.IntegerField(db_column='Transportista', blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    kilos = models.FloatField(db_column='Kilos', blank=True, null=True)  # Field name made lowercase.
    origen = models.CharField(max_length=5, blank=True, null=True)
    destino = models.CharField(max_length=5, blank=True, null=True)
    awb = models.CharField(max_length=40, blank=True, null=True)
    agente = models.IntegerField(blank=True, null=True)
    consignatario = models.IntegerField(blank=True, null=True)
    pagoflete = models.CharField(db_column='Pagoflete', max_length=1, blank=True, null=True)  # Field name made lowercase.
    moneda = models.SmallIntegerField(blank=True, null=True)
    arbitraje = models.FloatField(blank=True, null=True)
    tarifa = models.DecimalField(db_column='Tarifa', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
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
    posicion = models.CharField(db_column='Posicion', max_length=30, blank=True, null=True)  # Field name made lowercase.
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
    unidadpeso = models.CharField(db_column='UnidadPeso', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unidadvolumen = models.CharField(db_column='UnidadVolumen', max_length=1, blank=True, null=True)  # Field name made lowercase.
    editado = models.CharField(db_column='Editado', max_length=30, blank=True, null=True)  # Field name made lowercase.
    loading = models.CharField(db_column='Loading', max_length=5, blank=True, null=True)  # Field name made lowercase.
    discharge = models.CharField(db_column='Discharge', max_length=5, blank=True, null=True)  # Field name made lowercase.
    envioaduana = models.CharField(db_column='EnvioAduana', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fechaingreso = models.DateTimeField(db_column='FechaIngreso', blank=True, null=True)  # Field name made lowercase.
    contratocli = models.CharField(db_column='ContratoCli', max_length=30, blank=True, null=True)  # Field name made lowercase.
    contratotra = models.CharField(db_column='ContratoTra', max_length=30, blank=True, null=True)  # Field name made lowercase.
    viajefluvial = models.CharField(db_column='ViajeFluvial', max_length=30, blank=True, null=True)  # Field name made lowercase.
    awbfluvial = models.CharField(db_column='AwbFluvial', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prefijofluvial = models.CharField(db_column='PrefijoFluvial', max_length=5, blank=True, null=True)  # Field name made lowercase.
