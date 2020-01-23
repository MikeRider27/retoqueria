# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import  HttpResponseRedirect
from django.core.urlresolvers import reverse

from administracion.constants import TipoFlujoCaja
from administracion.models import CategoriaFlujoCaja, RetiroDinero, IngresoDinero
from retoqueria.globales import separar
from ventas.servicios import get_sesion_abierta


@admin.register(CategoriaFlujoCaja)
class CategoriaFlujoCajaAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ['nombre', 'tipo', 'activo']
    list_filter = ['tipo', 'activo']
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False


class FlujoCajaAdmin(admin.ModelAdmin):
    readonly_fields = ['fecha']
    list_display = ['fecha', 'sesion_', '_monto', 'motivo']
    fields = [
        'categoria',
        'motivo',
        'monto',
        'fecha'
        'forma_pago'
    ]
    actions = None

    def sesion_(self, obj):

        return mark_safe(obj.sesion or '')
    sesion_.short_description = u'Sesión'

    def _monto(self, obj):
        return str(separar(int(round(obj.monto)))) +' Gs.'

    def add_view(self, request, form_url='', extra_context=None):
        self.readonly_fields = ['fecha']
        self.fields = [
            'categoria',
            'motivo',
            'monto',
            'fecha',
            'forma_pago'
            ]
        return super(FlujoCajaAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def get_form(self, request, obj=None, **kwargs):
        form = super(FlujoCajaAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fields = [
            'categoria',
            'motivo',
            'monto',
            'fecha',
            'sesion'
        ]
        self.readonly_fields = self.fields

        return super(FlujoCajaAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        return super(FlujoCajaAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        form = getattr(self,'advanced_search_form',None)
        qs = super(FlujoCajaAdmin, self).get_queryset(request)
        if form:
            if form.cleaned_data.get('motivo', ''):
                qs = qs.filter(motivo__icontains=form.cleaned_data['motivo'])
            if form.cleaned_data.get('caja', ''):
                qs = qs.filter(sesion__caja_id=form.cleaned_data['caja'].pk)
            if form.cleaned_data.get('desde', ''):
                qs = qs.filter(fecha__gte=form.cleaned_data['desde'])
            if form.cleaned_data.get('hasta', ''):
                qs = qs.filter(fecha__lte=form.cleaned_data['hasta'])
        return qs

    other_search_fields = {}

    # standard search

    def lookup_allowed(self, lookup, *args, **kwargs):
        if lookup in self.advanced_search_form.fields.keys():
            return True
        return super(FlujoCajaAdmin, self).lookup_allowed(lookup, *args, **kwargs)


@admin.register(RetiroDinero)
class RetiroDineroAdmin(FlujoCajaAdmin):
    #form = RetiroDineroForm

    def add_view(self, request, form_url='', extra_context=None):
        if not get_sesion_abierta(request.user):
            self.message_user(request, mark_safe(
                u'Debe realizar una <strong>"Apertura de Caja"</strong> para realizar esta acción'))
            return HttpResponseRedirect(reverse('admin:administracion_retirodinero_changelist'))
        return super(RetiroDineroAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def get_queryset(self, request):
        return super(RetiroDineroAdmin, self).get_queryset(request).filter(tipo=TipoFlujoCaja.EGRESO)

    def save_model(self, request, obj, form, change):
        obj.sesion = get_sesion_abierta(request.user)
        obj.tipo = TipoFlujoCaja.EGRESO
        res = super(RetiroDineroAdmin, self).save_model(request, obj, form, change)
        obj.sesion.caja.disponible -= obj.monto
        obj.sesion.caja.save()
        return res


@admin.register(IngresoDinero)
class IngresoDineroAdmin(FlujoCajaAdmin):
    #form = IngresoDineroForm

    def add_view(self, request, form_url='', extra_context=None):
        if not get_sesion_abierta(request.user):
            self.message_user(request, mark_safe(u'Debe realizar una <strong>"Apertura de Caja"</strong> para realizar esta acción'))
            return HttpResponseRedirect(reverse('admin:administracion_ingresodinero_changelist'))
        return super(IngresoDineroAdmin, self).add_view(request,
                                                    form_url=form_url,
                                                    extra_context=extra_context)

    def get_queryset(self, request):
        return super(IngresoDineroAdmin, self).get_queryset(request).filter(tipo=TipoFlujoCaja.INGRESO)

    def save_model(self, request, obj, form, change):
        obj.sesion = get_sesion_abierta(request.user)
        obj.tipo = TipoFlujoCaja.INGRESO
        res = super(IngresoDineroAdmin, self).save_model(request, obj, form, change)
        obj.sesion.caja.disponible += obj.monto
        obj.sesion.caja.save()
        return res