from django.contrib import admin
from django.contrib.admin.decorators import register
from materiales.models import *
from materiales.forms import *


@register(UnidadDeMedida)
class UnidadDeMedidaAdmin(admin.ModelAdmin):
    pass

@register(CategoriaDeMaterial)
class CategoriaDeMaterialAdmin(admin.ModelAdmin):
    pass

@register(Material)
class MaterialAdmin(admin.ModelAdmin):
    form = MaterialForm    
    filter_horizontal = ('proveedores',)

