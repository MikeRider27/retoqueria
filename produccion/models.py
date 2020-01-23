# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.db import models
from datetime import date, timedelta
from django.contrib.admin.models import LogEntry, CHANGE

from django.utils.encoding import force_unicode
from django.db.models.signals import post_save

from django.dispatch import receiver

from funcionarios.models import Funcionario, DetalleDeLiquidacion, Liquidacion

OT_PENDIENTE = 0
OT_PROCESO = 1
OT_PRODUCCION = 2
OT_TERMINADO = 3
OT_REVISADO = 4
OT_ENTREGADO = 5
OT_RECHAZADO = 6

ESTADO_OT = (
    (OT_PENDIENTE, 'Pendiente'),
    (OT_PROCESO, 'En Proceso'),
    (OT_PRODUCCION, 'En Produccion'),
    (OT_TERMINADO, 'Terminado'),
    (OT_REVISADO, 'Revisado'),
    (OT_ENTREGADO, 'Entregado'),
    (OT_RECHAZADO, 'Rechazado')
)


class OrdenDeTrabajo(models.Model):
    class Meta:
        permissions = (
            ("ver_ot_todos", "Puede ver la lista general de trabajos"),
            ("ver_ot_pendientes", "Puede ver la lista de trabajos pendientes"),
            ("ver_ot_proceso", "Puede ver la lista de trabajos en proceso"),
            ("ver_ot_produccion", "Puede ver la lista de trabajos en produccion"),
            ("ver_ot_terminados", "Puede ver la lista de trabajos terminados"),
            ("ver_ot_revisados", "Puede ver la lista de trabajos revisados"),
            ("ver_ot_entregados", "Puede ver la lista de trabajos entregados"),
            ("ver_ot_rechazados", "Puede ver la lista de trabajos rechazados"),
            ("ver_ot_entregas", "Puede ver la lista de Entregas Pendientes"),

            ("pasar_ot_proceso", "Puede pasar el trabajo al estado en proceso"),
            ("pasar_ot_produccion", "Puede pasar el trabajo al estado en produccion"),
            ("pasar_ot_terminado", "Puede pasar el trabajo al estado terminado"),
            ("pasar_ot_revisado", "Puede pasar el trabajo al estado revisado"),
            ("pasar_ot_entregado", "Puede pasar el trabajo al estado entregado"),
            ("pasar_ot_rechazado", "Puede pasar el trabajo al estado rechazado"),

            ("retroceder_ot_pendiente", "Puede retroceder el trabajo al estado pendiente"),
            ("retroceder_ot_proceso", "Puede retroceder el trabajo al estado en proceso"),
            ("retroceder_ot_produccion", "Puede retroceder el trabajo al estado en produccion"),
            ("retroceder_ot_terminado", "Puede retroceder el trabajo al estado terminado"),
            ("retroceder_ot_revisado", "Puede retroceder el trabajo al estado revisado"),
            ("retroceder_ot_entregado", "Puede retroceder el trabajo al estado entregado"),
            ("reprogramar_ot", "Puede reprogramar el trabajo rechazado"),

            ("asignar_modista", "Puede asignar una modista a la OT"),
        )

    revision = models.IntegerField(default=1, editable=False)

    fecha_de_ingreso = models.DateField(default=date.today)
    fecha_de_entrega = models.DateField(null=True)
    hora_de_entrega = models.TimeField(null=True, blank=True)
    dias_para_prueba = models.IntegerField(null=True, blank=True)
    dias_post_prueba = models.IntegerField(null=True, blank=True)
    cliente = models.ForeignKey("clientes.Cliente")
    prenda = models.CharField(max_length=300, null=True)
    estado = models.IntegerField(choices=ESTADO_OT, editable=False, default=OT_PENDIENTE)
    modista = models.ForeignKey('funcionarios.Funcionario', null=True, default=4)

    # opciones
    ninos = models.BooleanField(default=False, verbose_name="niños")
    express = models.BooleanField(default=False)
    con_forro = models.BooleanField(default=False)
    con_pedreria = models.BooleanField(default=False, verbose_name="con pedreria/encaje/lentejuela")
    gestion_de_compra = models.BooleanField(default=False)

    descuento = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __unicode__(self):
        return unicode("OT: " + str(self.id) + " - " + str(self.revision))

    def save(self, *args, **kwargs):
        if (self.pk is None) and (self.express is True):
            self.estado = OT_PRODUCCION
            self.fecha_de_entrega = date.today()
        super(OrdenDeTrabajo, self).save(*args, **kwargs)

    def get_duracion(self):
        duracion = 0
        for detalle in self.detalleordendetrabajo_set.all():
            duracion += detalle.servicio.duracion
            return duracion

    @property
    def vencida(self):
        return date.today() >= self.fecha_de_entrega


class DetalleOrdenDeTrabajo(models.Model):
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    orden_de_trabajo = models.ForeignKey(OrdenDeTrabajo)
    categoria_servicio = models.ForeignKey("servicios.CategoriaDeServicio", verbose_name="Categoria de servicio",
                                           null=True)
    servicio = models.ForeignKey("servicios.Servicio")
    tela = models.ForeignKey("servicios.Tela")
    cantidad = models.DecimalField(max_digits=4, decimal_places=2, default=1)
    precio = models.DecimalField(max_digits=15, decimal_places=2)
    observaciones = models.TextField(null=True, blank=True)
    liquidado = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s [%s]' % (str(self.servicio), str(self.tela), str(self.orden_de_trabajo))

    def marcar_liquidado(self):
        detalle = DetalleDeLiquidacion.objects.filter(servicio_id=self.id).first()

        if detalle:
            self.liquidado = True

        else:
            self.liquidado = False
        super(DetalleOrdenDeTrabajo, self).save()


def get_fecha_de_taller():
    ordenes = OrdenDeTrabajo.objects.filter(estado__in=[OT_PROCESO, OT_PENDIENTE, OT_PRODUCCION])
    buscar = True
    delta = 1
    while buscar:
        fecha_de_taller = date.today() + timedelta(days=delta)
        if int(fecha_de_taller.strftime("%w")) == 0:
            delta += 1
        else:
            ots_con_misma_fecha_de_entrega = ordenes.filter(fecha_de_entrega=fecha_de_taller).count()
            if ots_con_misma_fecha_de_entrega >= 10:
                delta += 1
            elif ots_con_misma_fecha_de_entrega < 10:
                buscar = False

    return fecha_de_taller


def log_change(object, user, modista):
    LogEntry.objects.log_action(
        user_id=user,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_unicode(object),
        action_flag=CHANGE,
        change_message='cambiada modista' + " a " + modista
    )
