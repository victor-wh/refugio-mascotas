from django.conf.urls import url
from adopcion.views import index_adopcion, SolicitudList, SolicitudCreate, SolicitudUpdate, \
    SolicitudDelete, solicitud_list, solicitud_delete, solicitud_view, solicitud_edit, PersonaList, \
    PersonaDelete, PersonaDetail, persona_detail, persona_list, persona_delete

urlpatterns = [
    url(r'solicitud/crearclase/', SolicitudCreate.as_view(), name='solicitud_crearclase'),
    url(r'solicitud/crearfuncion/', solicitud_view, name='solicitud_crearfuncion'),
    url(r'solicitud/listarclase/', SolicitudList.as_view(), name='solicitud_listarclase'),
    url(r'solicitud/listarfuncion/', solicitud_list, name='solicitud_listarfuncion'),
    url(r'solicitud/editarclase/(?P<pk>\d+)/', SolicitudUpdate.as_view(), name='solicitud_editarclase'),
    url(r'solicitud/editarfuncion/(?P<id_solicitud>\d+)/', solicitud_edit, name='solicitud_editarfuncion'),
    url(r'solicitud/eliminarclase/(?P<pk>\d+)/', SolicitudDelete.as_view(), name='solicitud_eliminarclase'),
    url(r'solicitud/eliminarfuncion/(?P<id_solicitud>\d+)/', solicitud_delete, name='solicitud_eliminarfuncion'),
    url(r'personas/listarpclase/', PersonaList.as_view(), name='persona_listarclase'),
    url(r'personas/listarpfuncion/', persona_list, name='persona_listarfuncion'),
    url(r'personas/eliminarfuncion/(?P<id_persona>\d+)/', persona_delete, name='persona_eliminarfuncion'),
    url(r'personas/eliminarclase/(?P<pk>\d+)/', PersonaDelete.as_view(), name='persona_eliminarclase'),
    url(r'persona/datalleclase/(?P<pk>\d+)/', PersonaDetail.as_view(), name='persona_detailclase'),
    url(r'persona/datallefuncion/(?P<id_persona>\d+)/', persona_detail, name='persona_detailfuncion'),
    url(r'^$', SolicitudList.as_view(), name='index'),
    #url(r'', index_adopcion),
]