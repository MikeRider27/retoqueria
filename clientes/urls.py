from django.conf.urls import patterns, include, url
from clientes.autocomplete import *
from clientes.views import *


urlpatterns = [
    url(
        'clienteautocomplete/$',
        ClienteAutocomplete.as_view(),
        name='cliente-autocomplete',
    ),

    url(r'^cliente/(?P<pk>\d+)/detail/$', ClienteDetailView.as_view(), name='cliente_det'),
    url(r'^cliente/$', ClienteListView.as_view(), name='cliente_lis'),
    url(r'^$', clientes_presentacion),
]

