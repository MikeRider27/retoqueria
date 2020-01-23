from datetime import date
from django.db import models
from django.contrib.auth.models import User

from servicios.models import DetalleDeServicioTela


class Funcionario(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ruc = models.CharField(max_length=20, verbose_name="RUC/CI Nro.", null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    fecha_de_ingreso = models.DateField(null=True, blank=True)
    observaciones = models.TextField(max_length=500, null=True, blank=True)
    usuario = models.OneToOneField(User, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def get_full_name(self):
        return self.nombres + " " + self.apellidos

    def __unicode__(self):
        return unicode(self.get_full_name())


class Liquidacion(models.Model):
    class Meta:
        verbose_name = 'Liquidacion'
        verbose_name_plural = 'Liquidaciones'

    fecha = models.DateField(default=date.today)
    modista = models.ForeignKey('funcionarios.Funcionario')
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __unicode__(self):
        return unicode(str(self.modista.nombres) + " - " + str(self.fecha))

    def get_total(self):
        detalles = DetalleDeLiquidacion.objects.filter(liquidacion=self)
        total = 0
        for detalle in detalles:
            total += detalle.subtotal
        return total

    def save(self, *args, **kwargs):
        self.total = self.get_total()
        super(Liquidacion, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.total = self.get_total()
        super(Liquidacion, self).update(*args, **kwargs)


class DetalleDeLiquidacion(models.Model):
    class Meta:
        verbose_name = 'Detalle de liquidacion'
        verbose_name_plural = 'Detalle de liquidaciones'

    liquidacion = models.ForeignKey('funcionarios.Liquidacion')
    servicio = models.ForeignKey('produccion.DetalleOrdenDeTrabajo')
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        liquidacion = Liquidacion.objects.filter(id=self.liquidacion_id).first()
        liquidacion.save()
        super(DetalleDeLiquidacion, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        liquidacion = Liquidacion.objects.filter(id=self.liquidacion_id).first()
        super(DetalleDeLiquidacion, self).delete(*args, **kwargs)
        liquidacion.save()


def get_subtotal(servicio):
    detalles = DetalleDeServicioTela.objects.filter(servicio=servicio.servicio)
    subtotal = 0.0
    for detalle in detalles:
        if subtotal == 0 or detalle.precio < subtotal:
            subtotal = detalle.precio/5
    return subtotal


