from django.conf.urls import patterns, include, url
from materiales.autocomplete import *
from materiales.views import *

urlpatterns = [
    url(
        'unidaddemedidaautocomplete/$',
        UnidadDeMedidaAutocomplete.as_view(),
        name='unidaddemedida-autocomplete',
    ),

    url(
        'categoriadematerialautocomplete/$',
        CategoriaDeMaterialAutocomplete.as_view(),
        name='categoriadematerial-autocomplete',
    ),

    url(
        'materialautocomplete/$',
        MaterialAutocomplete.as_view(),
        name='material-autocomplete',
    ),


    url(r'^unidaddemedida/$', UnidadDeMedidaListView.as_view(), name='unidaddemedida_lis'),

    url(r'^categoriadematerial/$', CategoriaDeMaterialListView.as_view(), name='categoriadematerial_lis'),
    
    url(r'^material/$', MaterialListView.as_view(), name='material_lis'),
    url(r'^material/(?P<pk>\d+)/detail/$', MaterialDetailView.as_view(), name='material_det'),

    url(r'^$', materiales_presentacion),
]

