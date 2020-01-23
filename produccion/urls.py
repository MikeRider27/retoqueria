from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required

from produccion.autocomplete import *
from produccion.ajax import *
from produccion.views import *


urlpatterns = patterns('',

                       url(
                           r'^ordendetrabajo/$',
                           permission_required('produccion.ver_ot_todos')(OrdenDeTrabajoListView.as_view()),
                           name='ordendetrabajo_lis'
                       ),

                       url(
                           r'^ordendetrabajo/pendiente/$',
                           permission_required('produccion.ver_ot_pendientes')(OrdenDeTrabajoPendienteListView.as_view()),
                           name='ordendetrabajopendiente_lis'
                       ),

                       url(
                           r'^ordendetrabajo/proceso/$',
                           permission_required('produccion.ver_ot_proceso')(OrdenDeTrabajoProcesoListView.as_view()),
                           name='ordendetrabajoproceso_lis'
                       ),

                       url(
                           r'^ordendetrabajo/produccion/$',
                           permission_required('produccion.ver_ot_produccion')(OrdenDeTrabajoProduccionListView.as_view()),
                           name='ordendetrabajoproduccion_lis'
                       ),

                       url(
                           r'^ordendetrabajo/terminado/$',
                           permission_required('produccion.ver_ot_terminados')(OrdenDeTrabajoTerminadoListView.as_view()),
                           name='ordendetrabajoterminado_lis'
                       ),

                       url(
                           r'^ordendetrabajo/revisado/$',
                           permission_required('produccion.ver_ot_revisado')(OrdenDeTrabajoRevisadoListView.as_view()),
                           name='ordendetrabajorevisado_lis'
                       ),

                       url(
                           r'^ordendetrabajo/entregado/$',
                           permission_required('produccion.ver_ot_entregado')(OrdenDeTrabajoEntregadoListView.as_view()),
                           name='ordendetrabajoentregado_lis'
                       ),
                       url(
                           r'^ordendetrabajo/entregas/$',
                           permission_required('produccion.ver_ot_entregas')(
                               OrdenDeTrabajoEntregasListView.as_view()),
                           name='ordendetrabajoentregas_lis'
                       ),
                       url(
                           r'^ordendetrabajo/calendario/$',
                           permission_required('produccion.ver_ot_entregas')(
                               CalendarioDeEntregasListView.as_view()),
                           name='calendarioentregas_lis'
                       ),

                       url(
                           r'^ordendetrabajo/rechazado/$',
                           permission_required('produccion.ver_ot_rechazado')(OrdenDeTrabajoRechazadoListView.as_view()),
                           name='ordendetrabajorechazado_lis'
                       ),

                       url(
                           r'^ordendetrabajo/(?P<pk>\d+)/detail/$',
                           OrdenDeTrabajoDetailView.as_view(),
                           name='ordendetrabajo_det'
                       ),

                       url(r'^ordendetrabajo/(?P<pk>\d+)/pasarotproceso/$', pasar_ot_proceso, name='pasar_ot_proceso'),
                       url(r'^ordendetrabajo/(?P<pk>\d+)/pasarotproduccion/$', pasar_ot_produccion, name='pasar_ot_produccion'),
                       url(r'^ordendetrabajo/(?P<pk>\d+)/pasarotterminado/$', pasar_ot_terminado, name='pasar_ot_terminado'),
                       url(r'^ordendetrabajo/(?P<pk>\d+)/pasarotrevisado/$', pasar_ot_revisado, name='pasar_ot_revisado'),
                       url(r'^ordendetrabajo/(?P<pk>\d+)/pasarotentregado/$', pasar_ot_entregado, name='pasar_ot_entregado'),
                       url(r'^ordendetrabajo/(?P<pk>\d+)/pasarotrechazado/$', pasar_ot_rechazado, name='pasar_ot_rechazado'),

                       url(r'^ordendetrabajo/(?P<pk>\d+)/retrocederotpendiente/$', retroceder_ot_pendiente, name='retroceder_ot_pendiente'),
                       url(r'^ordendetrabajo/(?P<pk>\d+)/retrocederotproceso/$', retroceder_ot_proceso, name='retroceder_ot_proceso'),
                       url(r'^ordendetrabajo/(?P<pk>\d+)/retrocederotproduccion/$', retroceder_ot_produccion, name='retroceder_ot_produccion'),
                       url(r'^ordendetrabajo/(?P<pk>\d+)/retrocederotterminado/$', retroceder_ot_terminado, name='retroceder_ot_terminado'),
                       url(r'^ordendetrabajo/(?P<pk>\d+)/retrocederotrevisado/$', retroceder_ot_revisado, name='retroceder_ot_revisado'),
                       url(r'^ordendetrabajo/(?P<pk>\d+)/retrocederotentregado/$', retroceder_ot_entregado, name='retroceder_ot_entregado'),


                       url(
                           r'^ordendetrabajo/(?P<pk>\d+)/asignarmodista/$',
                           permission_required('produccion.asignar_modista')(AsignarModistaUpdateView.as_view()),
                           name='asignar_modista'
                       ),

                       url(
                           r'^ordendetrabajo/(?P<pk>\d+)/reprogramartrabajo/$',
                           permission_required('produccion.reprogramar_dot')(ReprogramarTrabajoUpdateView.as_view()),
                           name='reprogramar_trabajo'
                       ),

                       url(
                           r'^ordendetrabajoautocomplete/$',
                           OrdenDeTrabajoAutocomplete.as_view(),
                           name='ordendetrabajo-autocomplete',
                       ),

                       url(
                           r'^ordendetrabajoventaautocomplete/$',
                           OrdenDeTrabajoVentaAutocomplete.as_view(),
                           name='ordendetrabajo_venta-autocomplete',
                       ),

                       url(
                           r'^detalleordendetrabajoautocomplete/$',
                           DetalleOrdenDeTrabajoAutocomplete.as_view(),
                           name='detalleordendetrabajo-autocomplete',
                       ),

                       url(r'^getordendetrabajo/$',get_ordendetrabajo),
                       url(r'^get_detalle_ot_duracion/$', get_detalle_ot_duracion),

                       url(r'^$', produccion_presentacion),
                       )
