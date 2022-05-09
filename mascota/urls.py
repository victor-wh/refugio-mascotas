from django.urls import path, include
from mascota.views import index, mascota_view, mascota_list, mascota_edit, mascota_delete, \
    MascotaList, MascotaCreate, MascotaUpdate, MascotaDelete, VacunaList, VacunaCreate, VacunaUpdate, \
    VacunaDelete, vacuna_view, vacuna_list, vacuna_edit, vacuna_delete

urlpatterns = [
    path('nuevofuncion/', mascota_view, name="mascota_crearfuncion"),
    path('nuevoclase/', MascotaCreate.as_view(), name="mascota_crearclase"),
    path('listarclase/', MascotaList.as_view(), name="mascota_listarclase"), #basado en clases
    path('listarfuncion/', mascota_list, name="mascota_listarfuncion"), #basado en funciones
    path('editarfuncion/<int:id_mascota>/', mascota_edit, name="mascota_editarfuncion"),
    path('editarclase/<int:pk>/', MascotaUpdate.as_view(), name="mascota_editarclase"), #vistas genericas automm pide pk
    path('eliminarfuncion/<int:id_mascota>/', mascota_delete, name="mascota_eliminarfuncion"),
    path('eliminarclase/<int:pk>/', MascotaDelete.as_view(), name="mascota_eliminarclase"),
    path('vacuna/nuevavclase/', VacunaCreate.as_view(), name="vacuna_crearclase"),
    path('vacuna/listarvclase/', VacunaList.as_view(), name="vacuna_listarclase"),
    path('vacuna/editarvclase/<int:pk>/', VacunaUpdate.as_view(), name="vacuna_editarclase"),
    path('vacuna/eliminarvclase/<int:pk>/', VacunaDelete.as_view(), name="vacuna_eliminarclase"),
    path('vacuna/nuevavfuncion/', vacuna_view, name="vacuna_crearfuncion"),
    path('vacuna/listarvfuncion/', vacuna_list, name="vacuna_listarfuncion"),
    path('vacuna/editarvfuncion/<int:id_vacuna>/', vacuna_edit, name="vacuna_editarfuncion"),
    path('vacuna/eliminarvfuncion/<int:id_vacuna>/', vacuna_delete, name="vacuna_eliminarfuncion"),
    path('', MascotaList.as_view(), name="index"),
    #url(r'', index, name="index"),
]