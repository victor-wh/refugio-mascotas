from django.urls import path
from adopcion.views import index_adopcion, SolicitudList, SolicitudCreate, SolicitudUpdate, \
    SolicitudDelete, solicitud_list, solicitud_delete, solicitud_view, solicitud_edit, PersonaList, \
    PersonaDelete, PersonaDetail, persona_detail, persona_list, persona_delete, persona_detail2

urlpatterns = [
    path('solicitud/crearclase/', SolicitudCreate.as_view(), name='solicitud_crearclase'),
    path('solicitud/crearfuncion/', solicitud_view, name='solicitud_crearfuncion'),
    path('solicitud/listarclase/', SolicitudList.as_view(), name='solicitud_listarclase'),
    path('solicitud/listarfuncion/', solicitud_list, name='solicitud_listarfuncion'),
    path('solicitud/editarclase/<int:pk>/', SolicitudUpdate.as_view(), name='solicitud_editarclase'),
    path('solicitud/editarfuncion/<int:id_solicitud>/', solicitud_edit, name='solicitud_editarfuncion'),
    path('solicitud/eliminarclase/<int:pk>/', SolicitudDelete.as_view(), name='solicitud_eliminarclase'),
    path('solicitud/eliminarfuncion/<int:id_solicitud>/', solicitud_delete, name='solicitud_eliminarfuncion'),
    path('personas/listarpclase/', PersonaList.as_view(), name='persona_listarclase'),
    path('personas/listarpfuncion/<str:api_version>/', persona_list, name='persona_listarfuncion'),
    path('personas/eliminarfuncion/<int:id_persona>/', persona_delete, name='persona_eliminarfuncion'),
    path('personas/eliminarclase/<int:pk>/', PersonaDelete.as_view(), name='persona_eliminarclase'),
    path('persona/datalleclase/<int:pk>/', PersonaDetail.as_view(), name='persona_detailclase'),
    path('persona/datallefuncion/<str:api_version>/<int:id_mascota>/', persona_detail, name='persona_detailfuncion'),
    path('persona/datallefuncion2/<str:api_version>/<int:id_mascota>/', persona_detail2, name='persona_detailfuncion2'),
    path('', SolicitudList.as_view(), name='index'),
    #path('', index_adopcion),
]