from django.conf.urls import patterns, include, url
from proveedores.autocomplete import *
from proveedores.views import *

urlpatterns = [
    url(
        'proveedorautocomplete/$',
        ProveedorAutocomplete.as_view(),
        name='proveedor-autocomplete',
    ),

    url(r'^proveedor/(?P<pk>\d+)/detail/$', ProveedorDetailView.as_view(), name='proveedor_det'),
    url(r'^proveedor/$', ProveedorListView.as_view(), name='proveedor_lis'),
    url(r'^$', proveedores_presentacion),
]
