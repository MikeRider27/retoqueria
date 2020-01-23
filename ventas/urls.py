from django.conf.urls import patterns, include, url

from ventas.autocomplete import CajaAutocomplete
from ventas.reports import reporte_consolidado_pdf
from ventas.views import *


urlpatterns = [
    url(
        r'^caja-autocomplete/$',
        CajaAutocomplete.as_view(),
        name='caja-autocomplete',
    ),

    url(r'^venta/(?P<pk>\d+)/detail/$', VentaDetailView.as_view(), name='venta_det'),
    url(r'^venta/$', VentaListView.as_view(), name='venta_lis'),
    url(r'^$', ventas_presentacion),
    url(
        r'^reporte_consolidado_pdf/(?P<id>\w+)/$',
        reporte_consolidado_pdf,
        name='reporte_consolidado_pdf',
    ),
]

