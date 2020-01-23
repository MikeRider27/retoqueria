from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from ventas.models import *
from clientes.models import *


class VentaDetailView(DetailView):
    model = Venta
    template_name = "venta_detail.html"

    def get_context_data(self, **kwargs):
        context = super(VentaDetailView, self).get_context_data(**kwargs)
        context['detalles'] = DetalleVenta.objects.filter(venta_id=self.object.id)
        return context


class VentaListView(ListView):
    model = Venta
    template_name = "venta_list.html"
    paginate_by = 30

    def get_queryset(self):
        ventas = Venta.objects.all()

        q = self.request.GET.get('q', '')
        if q != '':
            ventas = ventas.filter(factura=q)

        orden_de_trabajo = self.request.GET.get('orden_de_trabajo', '')
        if orden_de_trabajo != '':
            ventas = ventas.filter(pk__in=[i.venta_id for i in DetalleVenta.objects.filter(orden_de_trabajo=orden_de_trabajo) ])


        cliente_id = self.request.GET.get('cliente_id', '')
        if cliente_id != '':
            ventas = ventas.filter(cliente_id=cliente_id)


        fecha_desde = self.request.GET.get('fecha_desde', '')
        if fecha_desde != '':
            vector = fecha_desde.split("/")
            fecha = vector[2] + "-" + vector[1] + "-" + vector[0]
            ventas = ventas.filter(fecha__gte=fecha)

        fecha_hasta = self.request.GET.get('fecha_hasta', '')
        if fecha_hasta != '':
            vector = fecha_hasta.split("/")
            fecha = vector[2] + "-" + vector[1] + "-" + vector[0]
            ventas = ventas.filter(fecha__lte=fecha)

        return ventas.order_by('-factura')

    def get_context_data(self, **kwargs):
        context = super(VentaListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['clientes'] = Cliente.objects.all()
        context['cliente_id'] = int(self.request.GET.get('cliente_id', '')) if (self.request.GET.get('cliente_id', '') != '') else ''
        context['orden_de_trabajo'] = self.request.GET.get('orden_de_trabajo', '')
        context['fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        return context


def ventas_presentacion(request):
    context = RequestContext(request)
    titulo = "VENTAS"
    descripcion = "."
    return render_to_response('admin/presentacion.html', {'titulo': titulo, 'descripcion': descripcion}, context)
