from django.shortcuts import render, render_to_response

# Create your views here.
from django.template.context import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import Q

from materiales.models import UnidadDeMedida, CategoriaDeMaterial, Material
from extra.globals import *

# Create your views here.

class UnidadDeMedidaListView(ListView):
    model = UnidadDeMedida
    template_name = "unidaddemedida_list.html"
    paginate_by = 30

    def get_queryset(self):
        unidadesdemedidas = UnidadDeMedida.objects.all()

        q = self.request.GET.get('q', '')
        if q != '':
            unidadesdemedidas = unidadesdemedidas.filter(nombre__icontains=q)

        return unidadesdemedidas.order_by("nombre")

    def get_context_data(self, **kwargs):
        context = super(UnidadDeMedidaListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q','')
        return context

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(UnidadDeMedidaListView, self).dispatch(*args, **kwargs)



class CategoriaDeMaterialListView(ListView):
    model = CategoriaDeMaterial
    template_name = "categoriadematerial_list.html"
    paginate_by = 30

    def get_queryset(self):
        categoriasdemateriales = CategoriaDeMaterial.objects.all()

        q = self.request.GET.get('q', '')
        if q != '':
            categoriasdemateriales = categoriasdemateriales.filter( Q(nombre__icontains=q) | Q(id__startswith=q) )
        return categoriasdemateriales.order_by("nombre")

    def get_context_data(self, **kwargs):
        context = super(CategoriaDeMaterialListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q','')
        return context

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(CategoriaDeMaterialListView, self).dispatch(*args, **kwargs)



class MaterialListView(ListView):
    model = Material
    template_name = "material_list.html"
    paginate_by = 30

    def get_queryset(self):
        materiales = Material.objects.all()

        q = self.request.GET.get('q', '')
        if q != '':
            materiales = materiales.filter( Q(descripcion__icontains=q) | Q(id__startswith=q) )

        categoria_id=self.request.GET.get('categoria_id','')
        if categoria_id !='':
            materiales = materiales.filter(categoria_id = categoria_id)

        return materiales.order_by("descripcion")

    def get_context_data(self, **kwargs):
        context = super(MaterialListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q','')
        context['categorias'] = CategoriaDeMaterial.objects.all()
        context['categoria_id'] = int(self.request.GET.get('categoria_id','')) if (self.request.GET.get('categoria_id','') != '') else ''
        return context

    def render_to_response(self, context, **response_kwargs):
        if 'excel' in self.request.GET.get('excel', ''): 

            lista_datos=[]
            datos = self.get_queryset()
            for dato in datos:
                lista_datos.append([
                    dato.descripcion,
                    dato.unidad_de_medida.nombre if dato.unidad_de_medida != None else '',
                    dato.categoria.nombre if dato.categoria != None else '',
                    separador_de_miles(dato.stock_actual),
                    separador_de_miles(dato.stock_minimo),

                ])

            titulos=[ 
                'Descripcion', 
                'Unidad de medida', 
                'Categoria', 
                'Stock actual',
                'Stock minimo',
            ]
            return listview_to_excel(lista_datos,'Materiales',titulos)
        
        return super(MaterialListView, self).render_to_response(context, **response_kwargs)

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(MaterialListView, self).dispatch(*args, **kwargs)

class MaterialDetailView(DetailView):
    model = Material
    template_name = "material_detail.html"

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(MaterialDetailView, self).dispatch(*args, **kwargs)

def materiales_presentacion(request):
    context = RequestContext(request)
    titulo="MATERIALES"
    descripcion=".."
    return render_to_response('admin/presentacion.html', {'titulo': titulo, 'descripcion': descripcion}, context)