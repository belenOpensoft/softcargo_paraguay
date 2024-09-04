from django.db import models

class InformeDna(models.Model):
    fecha = models.DateTimeField()
    numero = models.IntegerField()
    mensaje = models.TextField()
    respuesta = models.CharField(max_length=200)
    usuario = models.CharField(max_length=200)
