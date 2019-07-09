from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#class Proveedor(AbstractUser):
#	foto = models.ImageField(upload_to='media/images', default="default.png")
#	AUTH_USER_MODEL = "accounts.Proveedor"
#
#	class Meta:
#		verbose_name = "Proveedor"
#		verbose_name_plural = "Proveedores"
#
#	def __unicode__(self):
#		return self.username