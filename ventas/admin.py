# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib import admin
from django.contrib.admin.decorators import register
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin.utils import quote
from django.utils.html import format_html
from django.contrib import messages
from django.utils.safestring import mark_safe

from administracion.constants import get_categoria_flujo_venta
from administracion.models import IngresoDinero
from retoqueria.globales import separar, NOMBRE_EMPRESA
from ventas.forms import DetalleVentaForm, VentaForm, MovimientoFlujoCajaForm, CierreCajaForm
from ventas.models import FormaPago, MovimientoCaja, Caja, CierreCaja, DetalleVenta, Venta, AperturaCaja, \
    get_siguiente_numero, MovimientoFlujoCaja
from ventas.servicios import get_sesion_abierta
from administracion.constants import TipoFlujoCaja


@admin.register(FormaPago)
class FormaPagoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'nombre_comprobante']

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'monto_disponible', 'estado']
    search_fields = ['nombre']
    readonly_fields = ['estado', 'disponible']
    actions = None
    list_filter = ['estado']
    fields = ['nombre', 'disponible', 'activo', 'estado']

    def monto_disponible(self, obj):
        return separar(obj.disponible)
    monto_disponible.short_description = 'Disponible'


class MovimientoAdmin(admin.ModelAdmin):
    search_fields = ['caja__nombre', 'vendedor__username']
    actions = None
    list_display_links = None


    def monto_efectivo(self, obj):
        return mark_safe('<div >'+separar(int(obj.saldo_apertura or 0))+' Gs.</div>')

    def changelist_view(self, request, extra_context=None):
        self.current_user = request.user
        return super(MovimientoAdmin, self).changelist_view(request, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.current_user = request.user
        return super(MovimientoAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.current_user = request.user
        return super(MovimientoAdmin, self).change_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)

    def modificar(self, obj):
        if self.current_user == obj.vendedor:
            opts = obj._meta
            pk_value = obj._get_pk_val()
            obj_url = reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.model_name),
                args=(quote(pk_value),),
                current_app=self.admin_site.name,
            )

            return format_html('<a href="%s">%s</a>'%(obj_url, obj.caja))

        return obj.caja

    modificar.short_description = 'Caja'
    modificar.allow_tags = False
    modificar.admin_order_field = 'caja__nombre'

    def caja_abierta(self, request):
        movimientos = MovimientoCaja.objects.filter(apertura=True,
                                                    caja__estado=True,
                                                    vendedor=request.user)
        return movimientos.exists()

    def save_model(self, request, obj, form, change):
        obj.vendedor = request.user
        return super(MovimientoAdmin,self).save_model(request, obj, form, change)

    def saldo_apertura_(self, obj):
        return separar(int(obj.saldo_apertura))


@admin.register(AperturaCaja)
class AperturaCajaAdmin(MovimientoAdmin):
    readonly_fields = ['saldo_apertura']
    fields = ['caja', 'fecha_apertura', 'saldo_apertura']
    list_display = ['modificar', 'vendedor', 'saldo_apertura_', 'fecha_apertura']

    class Media(object):
        css = {
            'all':('/static/admin/movimiento/movimiento_caja.css',)
        }
        js = (
            '/static/admin/apertura_caja/apertura_caja.js',

        )

    def save_model(self, request, obj, form, change):
        obj.caja.estado = True
        obj.caja.save()
        obj.vendedor = request.user
        obj.save()
        if not change:
            obj.saldo_apertura = obj.get_saldo_apertura()
            obj.disponible = obj.saldo_apertura
            obj.save()

    def get_queryset(self, request):
        queryset = super(AperturaCajaAdmin, self).get_queryset(request)
        return queryset

    def add_view(self, request, form_url='', extra_context=None):
        sesion = get_sesion_abierta(request.user)
        if sesion:
            self.message_user(request, "YA EXISTE UNA CAJA ABIERTA CON ESTE USUARIO.", level=messages.WARNING)
            info = self.model._meta.app_label, self.model._meta.model_name
            return HttpResponseRedirect('/admin/%s/%s/'%info)
        return super(AperturaCajaAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)


@admin.register(CierreCaja)
class CierreCajaAdmin(MovimientoAdmin):
    readonly_fields = ['caja']
    form = CierreCajaForm
    fields = ['caja', 'fecha_cierre', 'saldo_apertura', 'ingresos', 'egresos', 'saldo_cierre']
    list_display = ['modificar', 'vendedor', 'fecha_apertura',
                    'saldo_apertura_', 'fecha_cierre', 'saldo_cierre_', 'acciones']

    def acciones(self, obj):
        html = '<a href="/admin/ventas/reporte_consolidado_pdf/%s">Consolidado</a>'%obj.pk
        return  mark_safe(html)

    def saldo_cierre_(self, obj):
        return separar(int(obj.saldo_cierre)).rjust(10)

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        obj.apertura = False
        obj.caja.estado = False
        obj.efectivo = obj.caja.disponible
        obj.saldo_cierre = obj.get_saldo_cierre()
        obj.caja.estado = False
        obj.caja.save()

        return super(CierreCajaAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super(CierreCajaAdmin, self).get_queryset(request)
        return queryset.all()

    def add_view(self, request, form_url='', extra_context=None):
        if not get_sesion_abierta(request):
            self.message_user(request, "NO EXISTE UNA CAJA ABIERTA CON ESTE USUARIO", level=messages.WARNING)
            info = self.model._meta.app_label, self.model._meta.model_name
            return HttpResponseRedirect('/admin/%s/%s/' % info)

        return super(CierreCajaAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = CierreCaja.objects.get(pk=object_id)
        if obj.fecha_cierre:
            self.readonly_fields = ['caja', 'fecha_cierre']
        else:
            self.readonly_fields = ['caja']

        return super(CierreCajaAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    form = DetalleVentaForm
    extra = 5


@register(Venta)
class VentaAdmin(admin.ModelAdmin):
    change_form_template = 'venta_form.html'
    form = VentaForm
    inlines = (DetalleVentaInline,)

    def get_default_venta(self, object_id=False):
           return object_id and Venta.objects.get(pk=object_id) or Venta(id=get_siguiente_numero())

    def add_view(self, request, object_id=None, form_url='', extra_context={}, **kwargs):
        if not get_sesion_abierta(request.user):
            self.message_user(request, "NO PUEDE REALIZAR UNA VENTA SIN REALIZAR UNA APERTURA DE CAJA", level=messages.WARNING)
            info = self.model._meta.app_label, self.model._meta.model_name
            return HttpResponseRedirect('/admin/%s/%s/' % info)

        return super(VentaAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        venta = obj
        venta.save()
        venta.sesion = get_sesion_abierta(request.user)
        venta.sesion.caja.disponible += venta.total
        venta.sesion.caja.save()
        # FLUJO DE CAJA
        try:
            registro_anterior = IngresoDinero.objects.get(venta=venta)
            if registro_anterior:
                registro_anterior.delete()
        except:
            print("Registro de Ingreso de dinero asociado a venta, no encontrado.")

        IngresoDinero.objects.create(
            categoria=get_categoria_flujo_venta(),
            sesion=venta.sesion,
            tipo=TipoFlujoCaja.INGRESO,
            motivo='Venta: ' + str(obj.factura),
            monto=venta.total,
            fecha=venta.fecha,
            forma_pago=venta.forma_pago if venta.sesion else '',
            venta=obj
        )
        return super(VentaAdmin, self).save_model(request, obj, form, change)


@admin.register(MovimientoFlujoCaja)
class MovimientoFlujoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'caja', 'cliente', 'tipo', 'forma_pago', 'motivo', 'monto_movimiento']
    list_display_links = None
    actions = None
    list_filter = ['tipo', 'forma_pago']
    change_list_template = 'movimientoflujocaja.html'

    def monto_movimiento(self, obj):
        return separar(int(round(obj.monto)))
    monto_movimiento.short_description = 'Monto'

    def has_add_permission(self, request):
        return False

    def caja(self, obj):
        if obj.sesion and obj.sesion.caja:
            return str(obj.sesion.caja)
        return ''

    def cliente(self, obj):
        res = NOMBRE_EMPRESA
        if obj.tipo == TipoFlujoCaja.INGRESO:
            if obj.venta:
                 res = str(obj.venta.cliente)
        return res

    def changelist_view(self, request, extra_context=None, **kwargs):
        self.my_request_get = request.GET.copy()
        self.advanced_search_form = MovimientoFlujoCajaForm(request.GET)
        self.advanced_search_form.is_valid()
        self.other_search_fields = {}
        params = request.get_full_path().split('?')

        movimientos_queryset = self.get_queryset(self)

        total_movimientos = 0
        for movimiento in movimientos_queryset:
            total_movimientos += movimiento.monto

        extra_context = extra_context or {}
        extra_context.update({'asf': MovimientoFlujoCajaForm,
                              'monto_total': separar(int(round(total_movimientos))),
                              'my_request_get': self.my_request_get,
                              'params': '?%s' % params[1].replace('%2F', '/') if len(params) > 1 else ''
                              })
        request.GET._mutable = True

        for key in self.advanced_search_form.fields.keys():
            try:
                temp = request.GET.pop(key)
            except KeyError:
                pass
            else:
                if temp != ['']:
                    self.other_search_fields[key] = temp
        request.GET_mutable = False

        return super(MovimientoFlujoAdmin, self) \
            .changelist_view(request, extra_context=extra_context, **kwargs)

    def lookup_allowed(self, lookup, *args, **kwargs):
        if lookup in self.advanced_search_form.fields.keys():
            return True
        return super(MovimientoFlujoAdmin, self).lookup_allowed(lookup, *args, **kwargs)

    def get_queryset(self, request):
        form = self.advanced_search_form
        qs = super(MovimientoFlujoAdmin, self).get_queryset(request)
        form.is_valid()
        if form.cleaned_data.get('caja', ''):
            qs = qs.filter(sesion__caja_id=form.cleaned_data.get('caja', '').pk)
        if form.cleaned_data.get('cliente', ''):
            qs = qs.filter(venta__cliente_id=form.cleaned_data.get('cliente', '').pk)
        if form.cleaned_data.get('desde', ''):
            desde = form.cleaned_data.get('desde', '')
            desde = datetime.datetime.strptime(desde.strftime('%Y%m%d'), '%Y%m%d')
            qs = qs.filter(fecha__gte=desde)
        if form.cleaned_data.get('hasta', ''):
            hasta = form.cleaned_data.get('hasta', '')
            hasta = datetime.datetime.strptime(hasta.strftime('%Y%m%d'), '%Y%m%d')
            qs = qs.filter(fecha__lte=datetime.timedelta(hours=23, seconds=59)+hasta)
        return qs

