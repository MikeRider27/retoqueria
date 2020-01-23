from dal import autocomplete
from django.db.models import Q
from funcionarios.models import Funcionario


class FuncionarioAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Funcionario.objects.none()

        qs = Funcionario.objects.exclude(activo=False)

        if self.q:
            qs = qs.filter(Q(nombres__icontains=self.q) | Q(apellidos__icontains=self.q))

        return qs
