from django.conf.urls import patterns, include, url
from sistema.views import *
from sistema.autocomplete import *
from sistema.ajax import *

urlpatterns = [

	url('usuarioautocomplete/$', 
		UsuarioAutocomplete.as_view(), 
		name='usuario-autocomplete'
	),
    url(r'^user/add/$', UsuarioCreateView.as_view(), name='usuario_add'),

	url(r'^$', sistema_presentacion),

]

