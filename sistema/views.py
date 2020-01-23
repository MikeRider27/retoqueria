from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from sistema.forms import *

# Create your views here.
class UsuarioCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "usuario_form.html"

    def get_success_url(self):
        return ("/admin/auth/user/" + str(self.object.id) )


def sistema_presentacion(request):
	context = RequestContext(request)
	titulo="SISTEMA"
	descripcion="."
	return render_to_response('admin/presentacion.html', {'titulo':titulo,'descripcion':descripcion}, context)
