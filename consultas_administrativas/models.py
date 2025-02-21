from django.db import models


class EJEMPLO(models.Model):
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