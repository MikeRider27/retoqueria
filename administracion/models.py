from django.db import models
from datetime import datetime

from administracion.constants import TipoFlujoCaja


class CategoriaFlujoCaja(models.Model):
    nombre = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(choices=TipoFlujoCaja.TIPOS, max_length=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class FlujoCaja(models.Model):
    categoria = models.ForeignKey(CategoriaFlujoCaja, null=True)
    sesion = models.ForeignKey('ventas.Sesion', null=True)
    tipo = models.CharField(choices=TipoFlujoCaja.TIPOS,max_length=5)
    motivo = models.CharField(max_length=200, null=True, blank=True)
    monto = models.DecimalField(decimal_places=2, max_digits=14)
    fecha = models.DateTimeField(default=datetime.now)
    forma_pago = models.ForeignKey('ventas.FormaPago', null=True, verbose_name='Forma de Pago')
    venta = models.ForeignKey('ventas.Venta', null=True)

    def __str__(self):
        return str(self.fecha.strftime('%d/%m/%Y - %H:%m'))




class RetiroDinero(FlujoCaja):
    class Meta:
        proxy = True
        verbose_name = "Retiro de Dinero"
        verbose_name_plural = "Retiros de Dinero"


class IngresoDinero(FlujoCaja):
    class Meta:
        proxy = True
        verbose_name = "Ingreso de Dinero"
        verbose_name_plural = "Ingresos de Dinero"
