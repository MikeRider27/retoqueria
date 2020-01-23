from dal import autocomplete
from django.db.models import Q
from produccion.models import *
from ventas.models import *


class OrdenDeTrabajoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return OrdenDeTrabajo.objects.none()

        qs = OrdenDeTrabajo.objects.all()

        if self.q:
            qs = qs.filter(Q(id__istartswith=self.q) | Q(prenda__icontains=self.q))

        return qs.order_by('-id')


class OrdenDeTrabajoVentaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return OrdenDeTrabajo.objects.none()

        qs = OrdenDeTrabajo.objects.all()

        cliente = self.forwarded.get('cliente', None)
        if cliente:
            qs = qs.filter(cliente=cliente)  # .exclude(cliente__venta__condicion_pago=CANCELACION)
            qs = qs.exclude(detalleventa__venta__cliente=cliente, detalleventa__venta__condicion_pago=CANCELACION)
        else:
            qs = qs.none()

        if self.q:
            qs = qs.filter(Q(id__istartswith=self.q) | Q(prenda__icontains=self.q))

        return qs.order_by('-id')


class DetalleOrdenDeTrabajoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return DetalleOrdenDeTrabajo.objects.none()

        qs = DetalleOrdenDeTrabajo.objects.exclude(liquidado=True)

        if self.q:
            qs = qs.filter(orden_de_trabajo__detalleordendetrabajo=self.q)
        return qs.order_by(-id)
