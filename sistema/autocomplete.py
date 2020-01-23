from dal import autocomplete
from django.db.models import Q
from django.contrib.auth.models import User, Group
from sistema.models import *


class UsuarioAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return User.objects.none()

        qs = User.objects.all()

        if self.q:
            qs = qs.filter( Q(first_name__istartswith=self.q) | Q(last_name__istartswith=self.q) | Q(username__istartswith=self.q) )

        return qs


