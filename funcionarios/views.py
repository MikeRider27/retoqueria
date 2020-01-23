from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from extra.globals import listview_to_excel

from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import Q

from funcionarios.models import Funcionario, Liquidacion


class FuncionarioListView(ListView):
    model = Funcionario
    template_name = "funcionario_list.html"

    def get_queryset(self):
        funcionarios = Funcionario.objects.all()

        q = self.request.GET.get('q', '')
        if q != '':
            funcionarios = funcionarios.filter(Q(nombres__icontains=q) | Q(apellidos__icontains=q))

        return funcionarios.order_by('nombres', 'apellidos')

    def render_to_response(self, context, **response_kwargs):
        if 'excel' in self.request.GET.get('excel', ''): 

            lista_datos=[]
            datos = self.get_queryset()
            for dato in datos:
                lista_datos.append([
                    dato.get_full_name(),
                    dato.ruc,
                    dato.direccion,
                    dato.email,
                    dato.fecha_de_ingreso.strftime("%d/%m/%Y") if dato.fecha_de_ingreso != None else '',
                    dato.observaciones,
                ])

            titulos=[ 'Nombres y Apellidos', 'RUC', 'Direccion', 'Email', 'Fecha de ingreso',  'Observaciones']
            return listview_to_excel(lista_datos, 'Funcionarios', titulos)
        
        return super(FuncionarioListView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(FuncionarioListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(FuncionarioListView, self).dispatch(*args, **kwargs)


class FuncionarioDetailView(DetailView):
    model = Funcionario
    template_name = "funcionario_detail.html"


class LiquidacionListView(ListView):
    model = Liquidacion
    template_name = "liquidacion_list.html"
    paginate_by = 30
    queryset = Liquidacion.objects.all()

    def get_queryset(self):
        liquidaciones = self.queryset

        q = self.request.GET.get('q', '')
        if q != '':
            liquidaciones = liquidaciones.filter(id__istartswith=q)

        modista_id = self.request.GET.get('modista_id', '')
        if modista_id != '':
            liquidaciones = liquidaciones.filter(modista__id=modista_id)

        fecha_desde = self.request.GET.get('fecha_desde', '')
        if fecha_desde != '':
            vector = fecha_desde.split("/")
            fecha = vector[2] + "-" + vector[1] + "-" + vector[0]
            liquidaciones = liquidaciones.filter(fecha__gte=fecha)

        fecha_hasta = self.request.GET.get('fecha_hasta', '')
        if fecha_hasta != '':
            vector = fecha_hasta.split("/")
            fecha = vector[2] + "-" + vector[1] + "-" + vector[0]
            liquidaciones = liquidaciones.filter(fecha__lte=fecha)

        return liquidaciones.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(LiquidacionListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['modistas'] = Funcionario.objects.exclude(activo=False)
        context['modista_id'] = int(self.request.GET.get('modista_id', '')) if (self.request.GET.get('modista_id', '') != '') else ''
        context['fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        return context


def funcionarios_presentacion(request):
    context = RequestContext(request)
    titulo = "FUNCIONARIOS"
    descripcion = ".."
    return render_to_response('admin/presentacion.html', {'titulo': titulo, 'descripcion': descripcion}, context)

