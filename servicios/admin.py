from django.contrib import admin
from django.contrib.admin.decorators import register
from servicios.models import *
from servicios.forms import *

from django.http import HttpResponseRedirect


@register(CategoriaDeServicio)
class CategoriaDeServicioAdmin(admin.ModelAdmin):
	pass

@register(Tela)
class TelaAdmin(admin.ModelAdmin):
	pass


class DetalleDeServicioTelaInline(admin.TabularInline):
	model = DetalleDeServicioTela
	form = DetalleDeServicioTelaForm
	extra = 4


class DetalleDeServicioMaterialInline(admin.TabularInline):
	model = DetalleDeServicioMaterial
	form = DetalleDeServicioMaterialForm
	extra = 4


@register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
	class Media:
		js = ('servicio.js',)

	form = ServicioForm
	inlines = (DetalleDeServicioTelaInline, DetalleDeServicioMaterialInline)

	# si servicioid se pasa por get inicializamos el formulario cabecera
	def get_changeform_initial_data(self, request):
		initial = super(ServicioAdmin, self).get_changeform_initial_data(request)
		if 'servicioid' in request.GET:
			servicioid = request.GET['servicioid']
			servicio = Servicio.objects.get(pk=servicioid)
			initial['categoria'] = servicio.categoria
			initial['codigo'] = servicio.codigo
			initial['descripcion'] = servicio.descripcion
			initial['tipo'] = servicio.tipo
			initial['es_plantilla'] = False
			initial['servicio_padre'] = servicio

		return initial


