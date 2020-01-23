from dal import autocomplete
from django.db.models import Q
from proveedores.models import *

class ProveedorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Proveedor.objects.none()

        qs = Proveedor.objects.all()

        if self.q:
            qs = qs.filter( Q(razon_social__icontains=self.q) | Q(ruc__istartswith=self.q) )

        return qs