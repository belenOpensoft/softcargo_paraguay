from django.contrib.auth.models import User
from django.db import models

"""
class Account(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    documento = models.CharField(max_length=20,blank=True,null=True)
    email = models.CharField(max_length=200,blank=True,null=True)
    firma = models.FileField(upload_to='firmas',blank=True,null=True)
    clave = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.user.first_name + ' - ' + str(self.user.last_name)
"""


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    documento = models.CharField(max_length=20, blank=True, null=True)
    firma = models.FileField(upload_to='firmas', blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.user.last_name}"



class AccountEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    clave = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'email')

    def __str__(self):
        return f"{self.email} ({self.user.username})"



class CorreoEnviado(models.Model):
    choice = (
        ('ENVIADO', 'ENVIADO'),
        ('FALLIDO', 'FALLIDO'),
    )
    choice_tipo = (
        ('', ''),
        ('IM', 'IMPORT MARÍTIMO'),
        ('EM', 'EXPORT MARÍTIMO'),
        ('IA', 'IMPORT AÉREO'),
        ('EA', 'EXPORT AÉREO'),
        ('IT', 'IMPORT TERRESTRE'),
        ('ET', 'EXPORT TERRESTRE'),
        ('SG', 'SEGUIMIENTO'),
        ('AD', 'ADMINISTRACION'),
    )

    fecha = models.DateTimeField()
    enviado_a = models.CharField(max_length=500)
    correo = models.CharField(max_length=100)
    emisor = models.CharField(max_length=150,null=True,blank=True)
    seguimiento = models.CharField(max_length=150,null=True,blank=True)
    mensaje = models.TextField(null=True,blank=True)
    estado = models.CharField(max_length=10,choices=choice)
    modulo = models.CharField(max_length=10,choices=choice_tipo,default='')
    error = models.TextField(null=True,blank=True)
    tipo = models.CharField(max_length=50)
    usuario = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Correos enviados"

from auditlog.registry import auditlog
auditlog.register(CorreoEnviado)