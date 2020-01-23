from django.conf.urls import patterns, include, url
from servicios.autocomplete import *
from servicios.views import *
from servicios.ajax import *


urlpatterns = [
    url(
        'categoriadeservicioautocomplete/$',
        CategoriaDeServicioAutocomplete.as_view(),
        name='categoriadeservicio-autocomplete',
    ),

    url(
        'telaautocomplete/$',
        TelaAutocomplete.as_view(),
        name='tela-autocomplete',
    ),

    url(
        'telaitemautocomplete/$',
        TelaItemAutocomplete.as_view(),
        name='telaitem-autocomplete',
    ),

    url(
        'servicioautocomplete/$',
        ServicioAutocomplete.as_view(),
        name='servicio-autocomplete',
    ),

    url(
        'servicio-por-categoria-autocomplete/$',
        ServicioPorCategoriaAutocomplete.as_view(),
        name='servicio-por-categoria-autocomplete',
    ),

    url('getservicio/$',get_servicio),
    url('getlistadetelasdelservicio/$',get_lista_de_telas_del_servicio),
    url('getlistadematerialesdelservicio/$', get_lista_de_materiales_del_servicio),
    url('getpreciodelservicio/$',get_precio_del_servicio),
    url(r'^get_duracion_servicio/$', get_duracion_servicio),

    url(r'^categoriadeservicio/$', CategoriaDeServicioListView.as_view(), name='categoriadeservicio_lis'),

    url(r'^tela/$', TelaListView.as_view(), name='tela_lis'),

    url(r'^servicio/(?P<pk>\d+)/detail/$', ServicioDetailView.as_view(), name='servicio_det'),
    url(r'^servicio/$', ServicioListView.as_view(), name='servicio_lis'),
    url(r'^$', servicios_presentacion),

]

