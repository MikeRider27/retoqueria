from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from administracion.constants import TipoFlujoCaja
from administracion.models import FlujoCaja


# Condiciones de Venta
CONTADO = 'CO'
CREDITO = 'CR'
CONDICION = (
    (CONTADO, 'CONTADO'),
    (CREDITO, 'CREDITO'),
)
PARCIAL = 'PAR'
CANCELACION = 'CAN'
CONDICION_PAGO = (
    (PARCIAL, 'PARCIAL'),
    (CANCELACION, 'CANCELACION'),
)

def get_siguiente_numero():
    from django.db import connection
    with connection.cursor() as cursor:
        try:
            cursor.execute('''SELECT MAX(id) FROM ventas_venta''')
            id = cursor.fetchone()[0]
        except:
            id = 0
        return id and (id + 1) or 1


class Caja(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    estado = models.BooleanField(choices=((True, 'Abierta'), (False, 'Cerrada')), default=False)
    disponible = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre


class FormaPago(models.Model):
    codigo = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=30, unique=True)
    nombre_comprobante = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.nombre)


class Sesion(models.Model):
    class Movimiento:
        def __init__(self, descripcion, monto, id):
            self.descripcion = descripcion
            self.monto = monto
            self.id = id

    vendedor = models.ForeignKey(User)
    caja = models.ForeignKey(Caja)
    fecha_apertura = models.DateTimeField(default=datetime.now)
    fecha_cierre = models.DateTimeField(null=True)
    saldo_apertura = models.DecimalField(decimal_places=2, max_digits=14, default=0)
    saldo_cierre = models.DecimalField(decimal_places=2, max_digits=14, default=0)

    # satanas estuvo aqui
    def agrupar(self, lista):
        values = set(map(lambda x: x.id, lista))
        newlist = []
        for x in values:
            aux = []
            for y in lista:
                if y.id == x:
                    aux.append(y)
            newlist.append(aux)
        true_list = []
        for b in newlist:
            total = 0
            for a in b:
                total += a.monto
            true_list.append(self.Movimiento(a.descripcion, total, a.id))
        return true_list

    def __unicode__(self):
        info = {
            'fecha': self.fecha_apertura.strftime('%d/%m/%Y - %H:%m'),
            'usuario' : self.vendedor.username,
            'caja' : self.caja
        }
        return mark_safe('<strong>Fecha:</strong> {fecha} hs. <strong>Usuario:</strong> {usuario}  <strong>Caja:</strong> {caja}'.format(**info))

    def ingresos(self):
        lista_ingresos = []
        for ingreso in self.flujocaja_set.filter(tipo=TipoFlujoCaja.INGRESO):
            if ingreso.forma_pago:
                lista_ingresos.append(self.Movimiento(
                    descripcion=str(ingreso.forma_pago),
                    monto=ingreso.monto,
                    id=ingreso.forma_pago.pk
                ))
        return self.agrupar(lista_ingresos)

    def egresos(self):
        lista_egresos = []
        for egreso in self.flujocaja_set.filter(tipo=TipoFlujoCaja.EGRESO):
            lista_egresos.append(self.Movimiento(
                descripcion=str(egreso.categoria),
                monto=egreso.monto,
                id=egreso.categoria.pk
            ))
        return self.agrupar(lista_egresos)

    def ingresos_egresos_apertura(self):
        obj = Sesion.objects.filter(pk__lt=self.pk)
        if obj:
            return obj.order_by('-id').first().ingresos_egresos_cierre()
        return []

    def ingresos_egresos_cierre(self):
        apertura = self.ingresos_egresos_apertura()
        egresos = []
        for egreso in self.flujocaja_set.filter(tipo=TipoFlujoCaja.EGRESO):
            if egreso.forma_pago:
                egresos.append(self.Movimiento(
                    descripcion=str(egreso.forma_pago),
                    monto=egreso.monto,
                    id=egreso.forma_pago.pk
                ))
        ingresos = self.ingresos()
        movimientos = self.agrupar(ingresos+egresos+apertura)
        for m in movimientos: m.monto = 0

        for i in apertura:
            for m in movimientos:
                if i.id == m.id:
                    m.monto += i.monto

        for i in ingresos:
            for m in movimientos:
                if i.id == m.id:
                    m.monto += i.monto

        for e in egresos:
            for m in movimientos:
                if e.id == m.id:
                    m.monto -= e.monto
        return movimientos

    def total_ingresos(self):
        total = 0
        for ingreso in self.flujocaja_set.filter(tipo=TipoFlujoCaja.INGRESO):
            total += ingreso.monto
        return int(round(total))

    def total_egresos(self):
        total = 0
        for egreso in self.flujocaja_set.filter(tipo=TipoFlujoCaja.EGRESO):
            total += egreso.monto
        return int(round(total))

    def get_saldo_apertura(self):
        total = 0
        if not self.saldo_apertura or self.saldo_apertura == 0:
            for m in self.ingresos_egresos_apertura():
                total += m.monto
            return int(round(total))
        return self.saldo_apertura

    def get_saldo_cierre(self):
        total = 0
        for m in self.ingresos_egresos_cierre():
            total += m.monto
        return int(round(total))


class MovimientoCaja(models.Model):
    caja = models.ForeignKey(Caja)
    fecha = models.DateTimeField(default=datetime.now)
    vendedor = models.ForeignKey(User)
    apertura = models.BooleanField(choices=((True, 'Apertura'), (False, 'Cierre')), verbose_name='tipo')
    efectivo = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s - %s'%(self.fecha, self.vendedor.username)


class AperturaCaja(Sesion):
    class Meta:
        proxy = True
        verbose_name = "Apertura de Caja"
        verbose_name_plural = 'Aperturas de Caja'

    def __unicode__(self):
        return '%s; %s' % (self.fecha_apertura.strftime('%d/%m/%Y - %H:%m'), self.vendedor.username)


class CierreCaja(Sesion):
    class Meta:
        proxy = True
        verbose_name = "Cierre de Caja"
        verbose_name_plural = 'Cierres de Caja'

    def __unicode__(self):
        return '%s - %s' % (self.fecha_cierre.strftime('%d/%m/%Y - %HH:%mm') if self.fecha_cierre else '', self.vendedor.username)


class Venta(models.Model):
    factura = models.CharField(max_length=50)
    cliente = models.ForeignKey("clientes.Cliente")
    fecha = models.DateField(default=date.today)
    condicion = models.CharField(choices=CONDICION, default=CONTADO, max_length=2, verbose_name='Condicion de Venta')
    anulado = models.BooleanField(default=False, editable=False)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    condicion_pago = models.CharField(choices=CONDICION_PAGO,
                                      default=CANCELACION,
                                      max_length=3,
                                      verbose_name='Condicion de Pago',
                                      null=True)
    forma_pago = models.ForeignKey(FormaPago, blank=True, null=True)
    sesion = models.ForeignKey(Sesion, null=True, blank=True, editable=False)

    def __unicode__(self):
        cadena = "FACTURA " + self.get_condicion_display() + " Nro.: " + self.factura
        return unicode(cadena)


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta)
    orden_de_trabajo = models.ForeignKey("produccion.OrdenDeTrabajo")
    precio = models.DecimalField(max_digits=15, decimal_places=2)


class MovimientoFlujoCaja(FlujoCaja):
    class Meta:
        proxy = True
        verbose_name_plural = 'Movimientos de Cajas'
        verbose_name = 'Movimiento de Caja'
