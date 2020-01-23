from dal import autocomplete
from django.db.models import Q
from depositos.models import *


class RetiroAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Retiro.objects.none()

        qs = Retiro.objects.all().order_by('-id')

        if self.q:
            qs = qs.filter( Q(id__istartswith=self.q) | Q(fecha__exact=self.q) )

        return qs



class DetalleRetiroAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        retiro = self.forwarded.get('retiro', None)

        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated() or not retiro:
            return DetalleRetiro.objects.none()

        qs = DetalleRetiro.objects.filter(retiro_id=retiro).order_by('-id')

        if self.q:
            qs = qs.filter( Q(material__id__istartswith=self.q) | Q(material__descripcion__icontains=self.q) )

        return qs

