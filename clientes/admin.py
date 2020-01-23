from django.contrib import admin
from django.contrib.admin.decorators import register
from clientes.models import Cliente

@register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    pass
