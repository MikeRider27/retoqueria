from django.contrib import admin
from django.contrib.admin.decorators import register

from funcionarios.forms import DetalleDeLiquidacionForm, LiquidacionForm
from funcionarios.models import Funcionario, Liquidacion, DetalleDeLiquidacion, get_subtotal

from produccion.models import DetalleOrdenDeTrabajo


@register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id',)


class DetalleDeLiquidacionInline(admin.TabularInline):
    model = DetalleDeLiquidacion
    form = DetalleDeLiquidacionForm
    extra = 0


@register(Liquidacion)
class LiquidacionAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'modista']
    search_fields = ['modista', ]
    form = LiquidacionForm

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = (DetalleDeLiquidacionInline,)
        return super(LiquidacionAdmin, self).change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        modista_id = request.POST['modista']
        obj.save()
        if modista_id:
            detalles = DetalleOrdenDeTrabajo.objects.filter(orden_de_trabajo__modista_id=modista_id).exclude(orden_de_trabajo__estado=0).exclude(orden_de_trabajo__estado=1).exclude(orden_de_trabajo__estado=2).exclude(orden_de_trabajo__estado=6)
            for detalle in detalles:
                detalle.marcar_liquidado()
                detalle.save()
                if not detalle.liquidado:
                    liquidacion = obj
                    servicio = detalle
                    subtotal = get_subtotal(detalle)
                    DetalleDeLiquidacion.objects.create(liquidacion=liquidacion, servicio=servicio, subtotal=subtotal)
        return super(LiquidacionAdmin, self).save_model(request, obj, form, change)
