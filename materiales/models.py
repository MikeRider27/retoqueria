# -*- coding: utf-8 -*-

from django.db import models
from django.apps import apps

class UnidadDeMedida(models.Model):
    class Meta:
        verbose_name = "unidad de medida"
        verbose_name_plural = "unidades de medida"

    nombre = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=10, blank=True, null=True, verbose_name="Símbolo")

    def __unicode__(self):
        return unicode(self.nombre)


class CategoriaDeMaterial(models.Model):
    class Meta:
        verbose_name = "categoría de materiales"
        verbose_name_plural = "categorías de materiales"

    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.nombre)

class Material(models.Model):
    class Meta:
        verbose_name_plural = "materiales"

    descripcion = models.CharField(max_length=150, verbose_name="descripción")
    unidad_de_medida = models.ForeignKey(UnidadDeMedida)
    categoria = models.ForeignKey(CategoriaDeMaterial, verbose_name="categoría")

    proveedores = models.ManyToManyField("proveedores.Proveedor", blank=True)

    stock_actual = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=False)
    stock_minimo = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __unicode__(self):
        return unicode(self.descripcion) 

    def actualizar_stock(self):
        
        cantidad = 0

        detalles_altas = apps.get_model("depositos","DetalleAlta").objects.filter(material_id = self.id)
        for detalle in detalles_altas:
            cantidad = cantidad + detalle.cantidad

        detalles_bajas = apps.get_model("depositos","DetalleBaja").objects.filter(material_id = self.id)
        for detalle in detalles_bajas:
            cantidad = cantidad - detalle.cantidad

        detalles_retiros = apps.get_model("depositos","DetalleRetiro").objects.filter(material_id = self.id)
        for detalle in detalles_retiros:
            cantidad = cantidad - detalle.cantidad

        detalles_devoluciones = apps.get_model("depositos","DetalleDevolucion").objects.filter(detalle_retiro__material__id = self.id)
        for detalle in detalles_devoluciones:
            cantidad = cantidad + detalle.cantidad

        self.stock_actual = cantidad
        self.save()
