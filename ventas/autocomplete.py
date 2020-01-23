# -*- coding: utf-8 -*-

from dal import autocomplete

from ventas.models import Caja


class CajaAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Caja.objects.none()

        qs = Caja.objects.filter(activo=True)
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs
