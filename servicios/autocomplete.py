from dal import autocomplete
from django.db.models import Q
from servicios.models import *


class CategoriaDeServicioAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return CategoriaDeServicio.objects.none()

        qs = CategoriaDeServicio.objects.all()

        if self.q:
            qs = qs.filter(nombre__icontains=self.q)

        return qs


class TelaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Tela.objects.none()

        qs = Tela.objects.filter(activo=True)

        if self.q:
            qs = qs.filter(nombre__icontains=self.q)

        return qs


class TelaItemAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        servicio = self.forwarded.get('servicio', None)

        if not self.request.user.is_authenticated() or not servicio:
            return Tela.objects.none()

        #qs = Tela.objects.filter(activo=True)
        qs = Tela.objects.filter(pk__in=[i.tela_id for i in DetalleDeServicioTela.objects.filter(servicio_id=servicio)]).exclude(activo=False)

        if self.q:
            qs = qs.filter(nombre__icontains=self.q)

        return qs


class ServicioAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Servicio.objects.none()

        qs = Servicio.objects.filter(es_plantilla=True)
        #qs = Servicio.objects.all()

        if self.q:
            qs = qs.filter(Q(descripcion__icontains=self.q) | Q(codigo__istartswith=self.q))

        return qs


class ServicioPorCategoriaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        categoria = self.forwarded.get('categoria_servicio', None)

        if not self.request.user.is_authenticated():
            return Servicio.objects.none()

        qs = Servicio.objects.filter(es_plantilla=True, categoria=categoria)
        #qs = Servicio.objects.all()

        if self.q:
            qs = qs.filter(Q(descripcion__icontains=self.q) | Q(codigo__istartswith=self.q))

        return qs
