# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Proveedor(models.Model):
	class Meta:
		verbose_name = 'proveedor'
		verbose_name_plural = 'proveedores'

	razon_social = models.CharField(max_length=100, verbose_name="Nombre o razón social")
	ruc = models.CharField(max_length=20, null=True, blank=True, verbose_name="RUC")
	direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name="dirección")
	telefono = models.CharField(max_length=50, null=True, blank=True, verbose_name="teléfono")
	email = models.CharField(max_length=100, null=True, blank=True, verbose_name="e-mail")
	observaciones = models.TextField(max_length=500, null=True, blank=True,)

	def __unicode__(self):
		return self.razon_social

