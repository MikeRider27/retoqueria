from django.contrib import admin
from django.contrib.admin.decorators import register
from depositos.models import *
from depositos.forms import *

# Register your models here.

@register(Deposito)
class DepositoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ('id',)
    search_fields = ('nombre',)


class DetalleAltaInlineAdmin(admin.TabularInline):
    model = DetalleAlta
    form = DetalleAltaForm
    extra = 3


@register(Alta)
class AltaAdmin(admin.ModelAdmin):
    form = AltaForm
    change_form_template = 'alta_form.html'
    list_display = ('fecha', 'funcionario', 'deposito',)
    ordering = ('-fecha',)
    search_fields = ('nombre',)

    inlines = [ DetalleAltaInlineAdmin, ]


class DetalleBajaInlineAdmin(admin.TabularInline):
    model = DetalleBaja
    form = DetalleBajaForm
    extra = 3


@register(Baja)
class BajaAdmin(admin.ModelAdmin):
    form = BajaForm
    change_form_template = 'baja_form.html'
    list_display = ('fecha', 'funcionario', 'deposito',)
    ordering = ('-fecha',)
    search_fields = ('nombre',)

    inlines = [ DetalleBajaInlineAdmin, ]


class DetalleRetiroInlineAdmin(admin.TabularInline):
    model = DetalleRetiro
    form = DetalleRetiroForm
    extra = 3


@register(Retiro)
class RetiroAdmin(admin.ModelAdmin):
    form = RetiroForm
    change_form_template = 'retiro_form.html'
    list_display = ('fecha', 'funcionario',)
    ordering = ('-fecha',)
    search_fields = ('nombre',)

    inlines = [ DetalleRetiroInlineAdmin, ]


class DetalleDevolucionInlineAdmin(admin.TabularInline):
    model = DetalleDevolucion
    form = DetalleDevolucionForm
    extra = 3


@register(Devolucion)
class DevolucionAdmin(admin.ModelAdmin):
    form = DevolucionForm
    change_form_template = 'devolucion_form.html'
    list_display = ('fecha', 'funcionario',)
    ordering = ('-fecha',)
    search_fields = ('nombre',)

    inlines = [ DetalleDevolucionInlineAdmin, ]




