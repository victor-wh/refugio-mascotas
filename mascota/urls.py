from django.urls import path, include
from mascota.views import index, mascota_view, mascota_list, mascota_edit, mascota_delete, \
    MascotaList2, MascotaCreate, MascotaUpdate, MascotaDelete, VacunaList, VacunaCreate, VacunaUpdate, \
    VacunaDelete, vacuna_view, vacuna_list, vacuna_edit, vacuna_delete, mascota_list2

urlpatterns = [
    path('nuevoclase/', MascotaCreate.as_view(), name="mascota_crearclase"),
    path('listarclase/', MascotaList2.as_view(), name="mascota_listarclase"), #basado en clases
    path('editarclase/<int:pk>/', MascotaUpdate.as_view(), name="mascota_editarclase"), #vistas genericas automm pide pk
    path('eliminarclase/<int:pk>/', MascotaDelete.as_view(), name="mascota_eliminarclase"),
    path('vacuna/nuevavclase/', VacunaCreate.as_view(), name="vacuna_crearclase"),
    path('vacuna/listarvclase/', VacunaList.as_view(), name="vacuna_listarclase"),
    path('vacuna/editarvclase/<int:pk>/', VacunaUpdate.as_view(), name="vacuna_editarclase"),
    path('vacuna/eliminarvclase/<int:pk>/', VacunaDelete.as_view(), name="vacuna_eliminarclase"),

    path('nuevofuncion/<str:api_version>/', mascota_view, name="mascota_crearfuncion"),
    path('listarfuncion/<str:api_version>/', mascota_list, name="mascota_listarfuncion"), #basado en funciones
    path('listarfuncion2/<str:api_version>/', mascota_list2, name="mascota_listarfuncion2"), #basado en funciones
    path('editarfuncion/<str:api_version>/<int:id_mascota>/', mascota_edit, name="mascota_editarfuncion"),
    path('eliminarfuncion/<str:api_version>/<int:id_mascota>/', mascota_delete, name="mascota_eliminarfuncion"),
    path('vacuna/nuevavfuncion/', vacuna_view, name="vacuna_crearfuncion"),
    path('vacuna/listarvfuncion/', vacuna_list, name="vacuna_listarfuncion"),
    path('vacuna/editarvfuncion/<int:id_vacuna>/', vacuna_edit, name="vacuna_editarfuncion"),
    path('vacuna/eliminarvfuncion/<int:id_vacuna>/', vacuna_delete, name="vacuna_eliminarfuncion"),
    #path('', MascotaList2.as_view(), name="index"),
    path('', index, name="index"),
]
