from django.db import models


class VReporteSubdiarioVentas(models.Model):
    fecha = models.DateField(null=True, blank=True)
    tipo = models.CharField(max_length=100, null=True, blank=True)
    serie = models.CharField(max_length=100, null=True, blank=True)
    prefijo = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=100, null=True, blank=True)
    nro_cliente = models.CharField(max_length=100, null=True, blank=True)
    cliente = models.CharField(max_length=255, null=True, blank=True)
    detalle = models.CharField(max_length=500, null=True, blank=True)
    exento = models.CharField(max_length=100, null=True, blank=True)
    gravado = models.CharField(max_length=100, null=True, blank=True)
    iva = models.CharField(max_length=100, null=True, blank=True)
    total = models.CharField(max_length=100, null=True, blank=True)
    tipo_cambio = models.CharField(max_length=100, null=True, blank=True)
    paridad = models.CharField(max_length=100, null=True, blank=True)
    referencia = models.CharField(max_length=100, null=True, blank=True)
    cancelada = models.CharField(max_length=10, null=True, blank=True)

    posicion = models.CharField(max_length=100, null=True, blank=True)
    cuenta = models.CharField(max_length=100, null=True, blank=True)
    vendedor = models.CharField(max_length=255, null=True, blank=True)
    vencimiento = models.DateField(null=True, blank=True)
    cobro = models.DateField(null=True, blank=True)
    tipo_cambio_cobro = models.CharField(max_length=100, null=True, blank=True)

    moneda = models.CharField(max_length=100, null=True, blank=True)
    rut = models.CharField(max_length=100, null=True, blank=True)

    vapor = models.CharField(max_length=100, null=True, blank=True)
    viaje = models.CharField(max_length=100, null=True, blank=True)
    master = models.CharField(max_length=100, null=True, blank=True)
    house = models.CharField(max_length=100, null=True, blank=True)
    embarcador = models.CharField(max_length=255, null=True, blank=True)
    consignatario = models.CharField(max_length=255, null=True, blank=True)
    flete = models.CharField(max_length=100, null=True, blank=True)
    etd = models.DateField(null=True, blank=True)
    eta = models.DateField(null=True, blank=True)
    imputada = models.CharField(max_length=100, null=True, blank=True)

    agente = models.CharField(max_length=255, null=True, blank=True)
    origen = models.CharField(max_length=100, null=True, blank=True)
    destino = models.CharField(max_length=100, null=True, blank=True)

    operacion = models.CharField(max_length=100, null=True, blank=True)
    movimiento = models.CharField(max_length=100, null=True, blank=True)
    deposito = models.CharField(max_length=100, null=True, blank=True)
    transportista = models.CharField(max_length=255, null=True, blank=True)
    orden_cliente = models.CharField(max_length=100, null=True, blank=True)
    wr = models.CharField(max_length=100, null=True, blank=True)
    autogen_cobro = models.CharField(max_length=100, null=True, blank=True)
    autogen_factura = models.CharField(max_length=100, primary_key=True)

    class Meta:
        managed = False
        db_table = 'VReporteSubdiarioVentas'

class VCuentasCobrarBalance(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha = models.DateField(null=True, blank=True)
    codigo = models.CharField(max_length=20, db_column='codigo')
    nombre = models.CharField(max_length=200, db_column='nombre')
    moneda = models.IntegerField(db_column='moneda')
    saldo = models.DecimalField(max_digits=18, decimal_places=2, db_column='saldo')
    arbitraje = models.DecimalField(max_digits=18, decimal_places=2)
    paridad = models.DecimalField(max_digits=18, decimal_places=2 )

    class Meta:
        managed = False
        db_table = 'VCuentasCobrarBalance'

class VAntiguedadSaldos(models.Model):
    id = models.IntegerField(primary_key=True)
    nrocliente = models.IntegerField()
    moneda = models.IntegerField()
    cliente = models.CharField(max_length=255)
    fecha = models.DateField()
    vto = models.DateField()
    total = models.DecimalField(max_digits=12, decimal_places=2)
    total_pagado = models.DecimalField(max_digits=12, decimal_places=2)
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False  # Es un VIEW, no una tabla real
        db_table = 'VAntiguedadSaldos'
        verbose_name = 'Antigüedad de Saldo'
        verbose_name_plural = 'Antigüedad de Saldos'

class VReporteSubdiarioCompras(models.Model):
    fecha = models.DateField(null=True, blank=True)
    tipo = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=100, null=True, blank=True)
    nro_proveedor = models.CharField(max_length=100, null=True, blank=True)
    proveedor = models.CharField(max_length=255, null=True, blank=True)
    detalle = models.CharField(max_length=500, null=True, blank=True)
    gravado = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    exento = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    arbitraje = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    paridad = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    moneda = models.CharField(max_length=50, null=True, blank=True)
    rut = models.CharField(max_length=100, null=True, blank=True)
    prefijo = models.CharField(max_length=100, null=True, blank=True)
    serie = models.CharField(max_length=100, null=True, blank=True)
    cuenta = models.CharField(max_length=100, null=True, blank=True)
    posicion = models.CharField(max_length=100, null=True, blank=True)

    vencimiento = models.DateField(null=True, blank=True)
    pago = models.DateField(null=True, blank=True)
    tipo_cambio_pago = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    cancelada = models.CharField(max_length=10, null=True, blank=True)

    imputada = models.CharField(max_length=100, null=True, blank=True)
    autogen_factura = models.CharField(max_length=255, primary_key=True)
    autogen_pago = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'VReporteSubdiarioCompras'

class VAntiguedadSaldosCompras(models.Model):
    id = models.IntegerField(primary_key=True)
    nrocliente = models.IntegerField()
    moneda = models.IntegerField()
    cliente = models.CharField(max_length=255)
    fecha = models.DateField()
    vto = models.DateField()
    total = models.DecimalField(max_digits=12, decimal_places=2)
    total_pagado = models.DecimalField(max_digits=12, decimal_places=2)
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False  # Es un VIEW, no una tabla real
        db_table = 'VAntiguedadSaldosCompras'

