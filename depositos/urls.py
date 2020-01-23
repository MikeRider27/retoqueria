from django.conf.urls import patterns, include, url
from depositos.autocomplete import *
from depositos.views import *
#from depositos.ajax import *


urlpatterns = [


    url(
        'detalleretiroautocomplete/$',
        DetalleRetiroAutocomplete.as_view(),
        name='detalleretiro-autocomplete',
    ),

    url(r'^deposito/$', DepositoListView.as_view(), name='deposito_lis'),
    url(r'^alta/$', AltaListView.as_view(), name='alta_lis'),
    url(r'^baja/$', BajaListView.as_view(), name='baja_lis'),
    url(r'^retiro/$', RetiroListView.as_view(), name='retiro_lis'),
    url(r'^devolucion/$', DevolucionListView.as_view(), name='devolucion_lis'),

    url(r'^alta/(?P<pk>\d+)/delete/$', AltaDeleteView.as_view(), name='alta_del'),
    url(r'^baja/(?P<pk>\d+)/delete/$', BajaDeleteView.as_view(), name='baja_del'),
    url(r'^retiro/(?P<pk>\d+)/delete/$', RetiroDeleteView.as_view(), name='retiro_del'),
    url(r'^devolucion/(?P<pk>\d+)/delete/$', DevolucionDeleteView.as_view(), name='devolucion_del'),

    url(
        'retiroautocomplete/$',
        RetiroAutocomplete.as_view(),
        name='retiro-autocomplete',
    ),


]

