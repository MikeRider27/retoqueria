from django.conf.urls import patterns, include, url
from funcionarios.autocomplete import *
from funcionarios.views import *

urlpatterns = [
    url(
        'funcionarioautocomplete/$',
        FuncionarioAutocomplete.as_view(),
        name='funcionario-autocomplete',
    ),
    url(
       r'^liquidacion/$',
       (LiquidacionListView.as_view()),
       name='liquidacion_lis'
    ),
    url(r'^funcionario/(?P<pk>\d+)/detail/$', FuncionarioDetailView.as_view(), name='funcionario_det'),
    url(r'^funcionario/$', FuncionarioListView.as_view(), name='funcionario_lis'),
    url(r'^$', funcionarios_presentacion),
]
