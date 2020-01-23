# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db.models import Q, Sum, Count

from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from extra.globals import *

from clientes.models import *

from produccion.forms import *
from produccion.reports import *


class OrdenDeTrabajoDetailView(DetailView):
    model = OrdenDeTrabajo
    template_name = "ordendetrabajo_detail.html"

    def get_context_data(self, **kwargs):
        context = super(OrdenDeTrabajoDetailView, self).get_context_data(**kwargs)
        context['detalles'] = DetalleOrdenDeTrabajo.objects.filter(orden_de_trabajo=self.object)
        return context

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(OrdenDeTrabajoDetailView, self).dispatch(*args, **kwargs)


class OrdenDeTrabajoListView(ListView):
    model = OrdenDeTrabajo
    template_name = "ordendetrabajo_list.html"
    paginate_by = 30
    queryset = OrdenDeTrabajo.objects.all()

    def get_queryset(self):
        ordenes_de_trabajo = self.queryset

        q = self.request.GET.get('q', '')
        if q != '':
            ordenes_de_trabajo = ordenes_de_trabajo.filter(id__istartswith=q)

        cliente_id = self.request.GET.get('cliente_id', '')
        if cliente_id != '':
            ordenes_de_trabajo = ordenes_de_trabajo.filter(cliente__id=cliente_id)

        modista_id = self.request.GET.get('modista_id', '')
        if modista_id != '':
            ordenes_de_trabajo = ordenes_de_trabajo.filter(modista__id=modista_id)

        rechazadas = self.request.GET.get('rechazadas', '')
        if rechazadas != '':
            if rechazadas == 'SI':
                ordenes_de_trabajo = ordenes_de_trabajo.exclude(revision=1)
            else:
                ordenes_de_trabajo = ordenes_de_trabajo.filter(revision=1)

        estado = self.request.GET.get('estado', '')
        if estado != '':
            ordenes_de_trabajo = ordenes_de_trabajo.filter(estado=estado)

        fecha_de_ingreso_desde = self.request.GET.get('fecha_de_ingreso_desde', '')
        if fecha_de_ingreso_desde != '':
            vector = fecha_de_ingreso_desde.split("/")
            fecha = vector[2] + "-" + vector[1] + "-" + vector[0]
            ordenes_de_trabajo = ordenes_de_trabajo.filter(fecha_de_ingreso__gte=fecha)

        fecha_de_ingreso_hasta = self.request.GET.get('fecha_de_ingreso_hasta', '')
        if fecha_de_ingreso_hasta != '':
            vector = fecha_de_ingreso_hasta.split("/")
            fecha = vector[2] + "-" + vector[1] + "-" + vector[0]
            ordenes_de_trabajo = ordenes_de_trabajo.filter(fecha_de_ingreso__lte=fecha)

        fecha_de_entrega_desde = self.request.GET.get('fecha_de_entrega_desde', '')
        if fecha_de_entrega_desde != '':
            vector = fecha_de_entrega_desde.split("/")
            fecha = vector[2] + "-" + vector[1] + "-" + vector[0]
            ordenes_de_trabajo = ordenes_de_trabajo.filter(fecha_de_entrega__gte=fecha)

        fecha_de_entrega_hasta = self.request.GET.get('fecha_de_entrega_hasta', '')
        if fecha_de_entrega_hasta != '':
            vector = fecha_de_entrega_hasta.split("/")
            fecha = vector[2] + "-" + vector[1] + "-" + vector[0]
            ordenes_de_trabajo = ordenes_de_trabajo.filter(fecha_de_entrega__lte=fecha)

        return ordenes_de_trabajo.order_by('-id')

    def render_to_response(self, context, **response_kwargs):
        if 'excel' in self.request.GET.get('excel', ''):

            lista_datos = []
            datos = self.get_queryset()
            for dato in datos:
                modista = ''
                if dato.modista:
                    modista = dato.modista.nombres
                lista_datos.append([
                    dato.pk,
                    dato.revision,
                    dato.prenda,
                    dato.fecha_de_ingreso.strftime('%d-%m-%Y'),
                    dato.fecha_de_entrega.strftime('%d-%m-%Y'),
                    dato.cliente.razon_social + ' - ' + dato.cliente.telefono,
                    dato.get_estado_display(),
                    modista,
                    separador_de_miles(dato.total),
                ])

            titulos = ['OT', 'Revision', 'Prenda', 'Fecha de ingreso', 'Vencimiento', 'Cliente', 'Estado', 'Modista', 'Total', ]
            return listview_to_excel(lista_datos, 'Ordenes_De_Trabajo', titulos)

        if 'pdf_materiales' in self.request.GET.get('pdf_materiales', ''):
            lista_datos = []
            datos = self.get_queryset().order_by('id').values_list('id', flat=True)

            return reporte_lista_materiales_ot_pdf(self.request, datos)

        return super(OrdenDeTrabajoListView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrdenDeTrabajoListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['clientes'] = Cliente.objects.all()
        context['modistas'] = Funcionario.objects.exclude(activo=False)
        context['cliente_id'] = int(self.request.GET.get('cliente_id', '')) if (self.request.GET.get('cliente_id', '') != '') else ''
        context['modista_id'] = int(self.request.GET.get('modista_id', '')) if (self.request.GET.get('modista_id', '') != '') else ''
        context['fecha_de_ingreso_desde'] = self.request.GET.get('fecha_de_ingreso_desde', '')
        context['fecha_de_ingreso_hasta'] = self.request.GET.get('fecha_de_ingreso_hasta', '')
        context['fecha_de_entrega_desde'] = self.request.GET.get('fecha_de_entrega_desde', '')
        context['fecha_de_entrega_hasta'] = self.request.GET.get('fecha_de_entrega_hasta', '')
        context['lista_rechazadas'] = OrdenDeTrabajo.objects.exclude(revision=1)
        context['rechazadas'] = self.request.GET.get('rechazadas', '')
        context['estado'] = self.request.GET.get('estado', '')
        context['conteo_ots'] = self.get_queryset().count()
        context['pendientes_ots'] = self.get_queryset().filter(estado=0).count()
        context['proceso_ots'] = self.get_queryset().filter(estado=1).count()
        context['produccion_ots'] = self.get_queryset().filter(estado=2).count()
        context['terminados_ots'] = self.get_queryset().filter(estado=3).count()
        context['revisados_ots'] = self.get_queryset().filter(estado=4).count()
        context['entregados_ots'] = self.get_queryset().filter(estado=5).count()
        context['rechazados_ots'] = self.get_queryset().filter(estado=6).count()
        context['total_ots'] = self.get_queryset().aggregate(total_ots=Sum('total')).get('total_ots')
        return context


class OrdenDeTrabajoPendienteListView(OrdenDeTrabajoListView):
    template_name = "ordendetrabajopendiente_list.html"
    queryset = OrdenDeTrabajo.objects.filter(estado=OT_PENDIENTE)


class OrdenDeTrabajoProcesoListView(OrdenDeTrabajoListView):
    template_name = "ordendetrabajoproceso_list.html"
    queryset = OrdenDeTrabajo.objects.filter(estado=OT_PROCESO)


class OrdenDeTrabajoProduccionListView(OrdenDeTrabajoListView):
    template_name = "ordendetrabajoproduccion_list.html"
    queryset = OrdenDeTrabajo.objects.filter(estado=OT_PRODUCCION)


class OrdenDeTrabajoTerminadoListView(OrdenDeTrabajoListView):
    template_name = "ordendetrabajoterminado_list.html"
    queryset = OrdenDeTrabajo.objects.filter(estado=OT_TERMINADO)


class OrdenDeTrabajoRevisadoListView(OrdenDeTrabajoListView):
    template_name = "ordendetrabajorevisado_list.html"
    queryset = OrdenDeTrabajo.objects.filter(estado=OT_REVISADO)


class OrdenDeTrabajoEntregadoListView(OrdenDeTrabajoListView):
    template_name = "ordendetrabajoentregado_list.html"
    queryset = OrdenDeTrabajo.objects.filter(estado=OT_ENTREGADO)


class OrdenDeTrabajoRechazadoListView(OrdenDeTrabajoListView):
    template_name = "ordendetrabajorechazado_list.html"
    queryset = OrdenDeTrabajo.objects.filter(estado=OT_RECHAZADO)


class OrdenDeTrabajoEntregasListView(OrdenDeTrabajoListView):
    template_name = "ordendetrabajoentregas_list.html"
    queryset = OrdenDeTrabajo.objects.all()


class CalendarioDeEntregasListView(ListView):
    model = OrdenDeTrabajo
    template_name = "calendario_entregas.html"
    paginate_by = 300
    queryset = OrdenDeTrabajo.objects.values('fecha_de_entrega').distinct().annotate(ots=Count('estado')).exclude(estado=3).exclude(estado=4).exclude(estado=5)

    def get_queryset(self):
        fechas = self.queryset

        fecha_de_entrega_desde = self.request.GET.get('fecha_de_entrega_desde', '')
        if fecha_de_entrega_desde != '':
            vector = fecha_de_entrega_desde.split("/")
            fecha = vector[2] + "-" + vector[1] + "-" + vector[0]
            fechas = fechas.filter(fecha_de_entrega__gte=fecha)

        fecha_de_entrega_hasta = self.request.GET.get('fecha_de_entrega_hasta', '')
        if fecha_de_entrega_hasta != '':
            vector = fecha_de_entrega_hasta.split("/")
            fecha = vector[2] + "-" + vector[1] + "-" + vector[0]
            fechas = fechas.filter(fecha_de_entrega__lte=fecha)

        return fechas.order_by('fecha_de_entrega').reverse()

    def get_context_data(self, **kwargs):
        context = super(CalendarioDeEntregasListView, self).get_context_data(**kwargs)
        context['fecha_de_entrega_desde'] = self.request.GET.get('fecha_de_entrega_desde', '')
        context['fecha_de_entrega_hasta'] = self.request.GET.get('fecha_de_entrega_hasta', '')
        context['hoy'] = date.today()
        context['total_ots'] = self.get_queryset().aggregate(total_ots=Sum('ots')).get('total_ots')
        return context


@permission_required('produccion.pasar_ot_proceso')
def pasar_ot_proceso(request, pk):
    context = RequestContext(request)
    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

    if request.method == 'POST':
        orden_de_trabajo.estado = OT_PROCESO
        orden_de_trabajo.save()

        next = request.GET.get('next', '/admin/produccion/ordendetrabajo/')
        return redirect(next)

    mensaje = "Esta seguro que desea pasar el trabajo " + str(orden_de_trabajo.id) + " al estado en proceso?"
    return render_to_response('confirmacion.html', {'mensaje': mensaje}, context)


@permission_required('produccion.pasar_ot_produccion')
def pasar_ot_produccion(request, pk):
    context = RequestContext(request)
    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

    if request.method == 'POST':
        if orden_de_trabajo.modista:
            orden_de_trabajo.estado = OT_PRODUCCION
            orden_de_trabajo.save()

            next = request.GET.get('next', '/admin/produccion/ordendetrabajo/')
            return redirect(next)

        else:
            mensaje = "El trabajo " + str(orden_de_trabajo.id) + " no tiene modista asignada"
            return render_to_response('rechazo.html', {'mensaje': mensaje}, context)
    mensaje = "Esta seguro que desea pasar el trabajo " + str(orden_de_trabajo.id) + " al estado en produccion?"
    return render_to_response('confirmacion.html', {'mensaje': mensaje}, context)


@permission_required('produccion.pasar_ot_terminado')
def pasar_ot_terminado(request, pk):
    context = RequestContext(request)
    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

    if request.method == 'POST':
        orden_de_trabajo.estado = OT_TERMINADO
        orden_de_trabajo.save()

        next = request.GET.get('next', '/admin/produccion/ordendetrabajo/')
        return redirect(next)

    mensaje = "Esta seguro que desea pasar el trabajo " + str(orden_de_trabajo.id) + " al estado terminado?"
    return render_to_response('confirmacion.html', {'mensaje': mensaje}, context)


@permission_required('produccion.pasar_ot_revisado')
def pasar_ot_revisado(request, pk):
    context = RequestContext(request)
    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

    if request.method == 'POST':
        orden_de_trabajo.estado = OT_REVISADO
        orden_de_trabajo.save()

        next = request.GET.get('next', '/admin/produccion/ordendetrabajo/')
        return redirect(next)

    mensaje = "Esta seguro que desea pasar el trabajo " + str(orden_de_trabajo.id) + " al estado revisado?"
    return render_to_response('confirmacion.html', {'mensaje': mensaje}, context)


@permission_required('produccion.pasar_ot_entregado')
def pasar_ot_entregado(request, pk):
    context = RequestContext(request)
    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

    if request.method == 'POST':
        orden_de_trabajo.estado = OT_ENTREGADO
        orden_de_trabajo.save()

        next = request.GET.get('next', '/admin/produccion/ordendetrabajo/')
        return redirect(next)

    mensaje = "Esta seguro que desea pasar el trabajo " + str(orden_de_trabajo.id) + " al estado entregado?"
    return render_to_response('confirmacion.html', {'mensaje': mensaje}, context)


@permission_required('produccion.pasar_ot_rechazado')
def pasar_ot_rechazado(request, pk):
    context = RequestContext(request)
    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

    if request.method == 'POST':
        orden_de_trabajo.estado = OT_RECHAZADO
        orden_de_trabajo.save()

        next = request.GET.get('next', '/admin/produccion/ordendetrabajo/')
        return redirect(next)

    mensaje = "Esta seguro que desea pasar el trabajo " + str(orden_de_trabajo.id) + " al estado rechazado?"
    return render_to_response('confirmacion.html', {'mensaje': mensaje}, context)


@permission_required('produccion.retroceder_ot_pendiente')
def retroceder_ot_pendiente(request, pk):
    context = RequestContext(request)
    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

    if request.method == 'POST':
        orden_de_trabajo.estado = OT_PENDIENTE
        orden_de_trabajo.save()

        next = request.GET.get('next', '/admin/produccion/ordendetrabajo/')
        return redirect(next)

    mensaje = "Esta seguro que desea retroceder el trabajo " + str(orden_de_trabajo.id) + " al estado pendiente?"
    return render_to_response('confirmacion.html', {'mensaje': mensaje}, context)


@permission_required('produccion.retroceder_ot_proceso')
def retroceder_ot_proceso(request, pk):
    context = RequestContext(request)
    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

    if request.method == 'POST':
        orden_de_trabajo.estado = OT_PROCESO
        orden_de_trabajo.save()

        next = request.GET.get('next', '/admin/produccion/ordendetrabajo/')
        return redirect(next)

    mensaje = "Esta seguro que desea retroceder el trabajo " + str(orden_de_trabajo.id) + " al estado en proceso?"
    return render_to_response('confirmacion.html', {'mensaje': mensaje}, context)


@permission_required('produccion.retroceder_ot_produccion')
def retroceder_ot_produccion(request, pk):
    context = RequestContext(request)
    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

    if request.method == 'POST':
        orden_de_trabajo.estado = OT_PRODUCCION
        orden_de_trabajo.save()

        next = request.GET.get('next', '/admin/produccion/ordendetrabajo/')
        return redirect(next)

    mensaje = "Esta seguro que desea retroceder el trabajo " + str(orden_de_trabajo.id) + " al estado en produccion?"
    return render_to_response('confirmacion.html', {'mensaje': mensaje}, context)


@permission_required('produccion.retroceder_ot_terminado')
def retroceder_ot_terminado(request, pk):
    context = RequestContext(request)
    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

    if request.method == 'POST':
        orden_de_trabajo.estado = OT_TERMINADO
        orden_de_trabajo.save()

        next = request.GET.get('next', '/admin/produccion/ordendetrabajo/')
        return redirect(next)

    mensaje = "Esta seguro que desea retroceder el trabajo " + str(orden_de_trabajo.id) + " al estado terminado?"
    return render_to_response('confirmacion.html', {'mensaje': mensaje}, context)


@permission_required('produccion.retroceder_ot_revisado')
def retroceder_ot_revisado(request, pk):
    context = RequestContext(request)
    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

    if request.method == 'POST':
        orden_de_trabajo.estado = OT_REVISADO
        orden_de_trabajo.save()

        next = request.GET.get('next', '/admin/produccion/ordendetrabajo/')
        return redirect(next)

    mensaje = "Esta seguro que desea retroceder el trabajo " + str(orden_de_trabajo.id) + " al estado revisado?"
    return render_to_response('confirmacion.html', {'mensaje': mensaje}, context)


@permission_required('produccion.retroceder_ot_entregado')
def retroceder_ot_entregado(request, pk):
    context = RequestContext(request)
    orden_de_trabajo = OrdenDeTrabajo.objects.get(pk=pk)

    if request.method == 'POST':
        orden_de_trabajo.estado = OT_ENTREGADO
        orden_de_trabajo.save()

        next = request.GET.get('next', '/admin/produccion/ordendetrabajo/')
        return redirect(next)

    mensaje = "Esta seguro que desea retroceder el trabajo " + str(orden_de_trabajo.id) + " al estado entregado?"
    return render_to_response('confirmacion.html', {'mensaje': mensaje}, context)


class AsignarModistaUpdateView(UpdateView):
    model = OrdenDeTrabajo
    form_class = AsignarModistaForm
    template_name = 'asignar_modista_form.html'

    def get_success_url(self):
        usuario = self.request.user.id
        modista_id = self.request.POST['modista']
        pk = self.kwargs['pk']
        ot = OrdenDeTrabajo.objects.filter(id=pk).first()
        modista = Funcionario.objects.get(id=modista_id).nombres
        log_change(ot, usuario, modista)
        return self.request.GET.get('next', '/admin/produccion/ordendetrabajo/')


class ReprogramarTrabajoUpdateView(UpdateView):
    model = OrdenDeTrabajo
    form_class = ReprogramarTrabajoForm
    template_name = 'reprogramar_trabajo_form.html'

    def get_success_url(self):
        return self.request.GET.get('next', '/admin/produccion/ordendetrabajo/')


def produccion_presentacion(request):
    context = RequestContext(request)
    titulo = "PRODUCCION"
    descripcion = "."
    return render_to_response('admin/presentacion.html', {'titulo': titulo, 'descripcion': descripcion}, context)