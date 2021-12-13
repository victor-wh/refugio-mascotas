from django.conf.urls import url, include
from mascota.views import index, mascota_view, mascota_list, mascota_edit, mascota_delete, \
    MascotaList, MascotaCreate, MascotaUpdate, MascotaDelete, VacunaList, VacunaCreate, VacunaUpdate, \
    VacunaDelete, vacuna_view, vacuna_list, vacuna_edit, vacuna_delete

urlpatterns = [
    url(r'^nuevofuncion/$', mascota_view, name="mascota_crearfuncion"),
    url(r'nuevoclase/', MascotaCreate.as_view(), name="mascota_crearclase"),
    url(r'listarclase/', MascotaList.as_view(), name="mascota_listarclase"), #basado en clases
    url(r'listarfuncion/', mascota_list, name="mascota_listarfuncion"), #basado en funciones
    url(r'editarfuncion/(?P<id_mascota>\d+)/', mascota_edit, name="mascota_editarfuncion"),
    url(r'editarclase/(?P<pk>\d+)/', MascotaUpdate.as_view(), name="mascota_editarclase"), #vistas genericas automm pide pk
    url(r'eliminarfuncion/(?P<id_mascota>\d+)/', mascota_delete, name="mascota_eliminarfuncion"),
    url(r'eliminarclase/(?P<pk>\d+)/', MascotaDelete.as_view(), name="mascota_eliminarclase"),
    url(r'vacuna/nuevavclase/', VacunaCreate.as_view(), name="vacuna_crearclase"),
    url(r'vacuna/listarvclase/', VacunaList.as_view(), name="vacuna_listarclase"),
    url(r'vacuna/editarvclase/(?P<pk>\d+)/', VacunaUpdate.as_view(), name="vacuna_editarclase"),
    url(r'vacuna/eliminarvclase/(?P<pk>\d+)/', VacunaDelete.as_view(), name="vacuna_eliminarclase"),
    url(r'vacuna/nuevavfuncion/', vacuna_view, name="vacuna_crearfuncion"),
    url(r'vacuna/listarvfuncion/', vacuna_list, name="vacuna_listarfuncion"),
    url(r'vacuna/editarvfuncion/(?P<id_vacuna>\d+)/', vacuna_edit, name="vacuna_editarfuncion"),
    url(r'vacuna/eliminarvfuncion/(?P<id_vacuna>\d+)/', vacuna_delete, name="vacuna_eliminarfuncion"),
    url(r'^$', MascotaList.as_view(), name="index"),
    #url(r'', index, name="index"),
]