from django.shortcuts import render, render_to_response

from django.template.context import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import Q

from servicios.models import *
from extra.globals import *


class CategoriaDeServicioListView(ListView):
    model = CategoriaDeServicio
    template_name = "categoriadeservicio_list.html"
    paginate_by = 30

    def get_queryset(self):
        categoriasdeservicios = CategoriaDeServicio.objects.all()

        q = self.request.GET.get('q', '')
        if q != '':
            categoriasdeservicios = categoriasdeservicios.filter( Q(nombre__icontains=q) | Q(id__istartswith=q) )

        return categoriasdeservicios.order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super(CategoriaDeServicioListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q','')
        return context

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(CategoriaDeServicioListView, self).dispatch(*args, **kwargs)


class TelaListView(ListView):
    model = Tela
    template_name = "tela_list.html"
    paginate_by = 30

    def get_queryset(self):
        telas = Tela.objects.all()

        q = self.request.GET.get('q', '')
        if q != '':
            telas = telas.filter( Q(nombre__icontains=q) | Q(id__istartswith=q) )

        return telas.order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super(TelaListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q','')
        return context

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(TelaListView, self).dispatch(*args, **kwargs)


class ServicioListView(ListView):
    model = Servicio
    template_name = "servicio_list.html"
    paginate_by = 30

    def get_queryset(self):
        #servicios = Servicio.objects.all()
        servicios = Servicio.objects.filter(es_plantilla=True)

        q = self.request.GET.get('q', '')
        if q != '':
            servicios = servicios.filter(Q(descripcion__icontains=q) | Q(codigo__istartswith=q) )

        categoria_id=self.request.GET.get('categoria_id','')
        if categoria_id !='':
            servicios = servicios.filter(categoria_id = categoria_id)

        return servicios.order_by("descripcion")

    def get_context_data(self, **kwargs):
        context = super(ServicioListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q','')
        context['categorias'] = CategoriaDeServicio.objects.all()
        context['categoria_id'] = int(self.request.GET.get('categoria_id','')) if (self.request.GET.get('categoria_id','') != '') else ''
        return context

    def render_to_response(self, context, **response_kwargs):
        if 'excel' in self.request.GET.get('excel', ''): 

            lista_datos=[]
            datos = self.get_queryset()
            for dato in datos:
                lista_datos.append([
                    dato.categoria.nombre,
                    dato.codigo,
                    dato.descripcion,
                    dato.duracion,

                ])

            titulos=[ 
            	'Categoria',
            	'Codigo',
                'Descripcion', 
                'Duracion (en hs)', 

            ]
            return listview_to_excel(lista_datos,'Servicios',titulos)
        
        return super(ServicioListView, self).render_to_response(context, **response_kwargs)

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(ServicioListView, self).dispatch(*args, **kwargs)


class ServicioDetailView(DetailView):
    model = Servicio
    template_name = "servicio_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ServicioDetailView, self).get_context_data(**kwargs)
        context['detalle_de_servicio_tela'] = DetalleDeServicioTela.objects.filter(servicio_id=self.object.id)
        context['detalle_de_servicio_material'] = DetalleDeServicioMaterial.objects.filter(servicio_id=self.object.id)
        return context

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(ServicioDetailView, self).dispatch(*args, **kwargs)


def servicios_presentacion(request):
    context = RequestContext(request)
    titulo ="SERVICIOS"
    descripcion =".."
    return render_to_response('admin/presentacion.html', {'titulo': titulo, 'descripcion': descripcion}, context)