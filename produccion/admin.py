from django.contrib import admin
from django.contrib.admin.decorators import register
from produccion.forms import *
from django.http import HttpResponseRedirect


class DetalleOrdenDeTrabajoInline(admin.StackedInline):
    model = DetalleOrdenDeTrabajo
    form = DetalleOrdenDeTrabajoForm
    # formset = DetalleOTFormSet
    template = 'detalleordendetrabajo_stacked.html'

    fieldsets = (
        (None, {'fields': [('categoria_servicio', 'servicio'), ('tela', 'cantidad', 'precio'), 'observaciones']}),
    )

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


@register(OrdenDeTrabajo)
class OrdenDeTrabajoAdmin(admin.ModelAdmin):
    class Media:
        js = ('ordendetrabajo.js',)

    form = OrdenDeTrabajoForm
    inlines = (DetalleOrdenDeTrabajoInline,)

    fields = (('fecha_de_ingreso', 'fecha_de_entrega', 'hora_de_entrega'), ('dias_para_prueba', 'dias_post_prueba'),
              ('cliente', 'prenda'), ('ninos', 'express', 'con_forro', 'con_pedreria', 'gestion_de_compra'), ('descuento', 'total'))

    def response_add(self, request, obj, post_url_continue=None):
        res = super(OrdenDeTrabajoAdmin, self).response_add(request, obj, post_url_continue)

        if request.POST.has_key('_addanother') and ("next" in request.GET):
            next = request.GET['next']
            cliente = request.POST['cliente']
            return HttpResponseRedirect("/admin/produccion/ordendetrabajo/add/?next=" + next + "&cliente=" + cliente)
        elif "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            pass

        return res

    def response_change(self, request, obj):
        res = super(OrdenDeTrabajoAdmin, self).response_change(request, obj)

        if request.POST.has_key('_addanother') and ("next" in request.GET):
            cliente = request.POST['cliente']
            next = request.GET['next']
            return HttpResponseRedirect("/admin/produccion/ordendetrabajo/add/?next=" + next + "&cliente=" + cliente)
        elif "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            pass
        return res

    def response_delete(self, request, obj_display, obj_id):
        res = super(OrdenDeTrabajoAdmin, self).response_delete(request, obj_display, obj_id)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        return res

    def get_form(self, request, obj=None, **kwargs):
        form = super(OrdenDeTrabajoAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form

    def save_model(self, request, obj, form, change):
        fecha_taller = request.POST.get('fecha_taller', '')
        obj.fecha_de_taller = fecha_taller
        return super(OrdenDeTrabajoAdmin, self).save_model(request, obj, form, change)
