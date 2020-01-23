from django.contrib import admin
from django.contrib.admin.decorators import register
from proveedores.models import Proveedor

@register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    pass


