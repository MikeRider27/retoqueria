# -*- coding: utf-8 -*-

from django.db import models

TIPO_DE_SERVICIO = (
    ("modista", 'Modista'),
    ("costura", 'Costurera'),
)


class CategoriaDeServicio(models.Model):
    class Meta:
        verbose_name = "categoria de servicio"
        verbose_name_plural = "categorias de servicio"

    codigo = models.IntegerField(default=0)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s - %s' % (self.codigo, unicode(self.nombre))


class Tela(models.Model):
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.nombre)


class Servicio(models.Model):
    categoria = models.ForeignKey(CategoriaDeServicio)
    codigo = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=100)
    duracion = models.IntegerField(verbose_name="duracion (en minutos)", default=0)
    es_plantilla = models.BooleanField(default=True)
    servicio_padre = models.ForeignKey('self', null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_DE_SERVICIO, default="modista")

    def __unicode__(self):
        return unicode(self.descripcion)

    def get_materiales(self):
        return DetalleDeServicioMaterial.objects.filter(servicio_id=self.id)


class DetalleDeServicioTela(models.Model):
    servicio = models.ForeignKey(Servicio)
    tela = models.ForeignKey(Tela)
    precio = models.DecimalField(max_digits=15, decimal_places=2)


class DetalleDeServicioMaterial(models.Model):
    servicio = models.ForeignKey(Servicio)
    material = models.ForeignKey("materiales.Material")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2)
