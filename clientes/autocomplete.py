from dal import autocomplete
from django.db.models import Q
from clientes.models import *


class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Cliente.objects.none()

        qs = Cliente.objects.all()

        if self.q:
            qs = qs.filter(Q(razon_social__icontains=self.q) | Q(ruc__istartswith=self.q) )

        return qs
