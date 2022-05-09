from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from api.views.mascota_decorador_views import mascotas_list, mascotas_detail, persona_mascota_list, vacunas_mascota_list
from api.views.mascota_api_views import MascotaList, MascotaDetail, MascotaPersonaList, MascotaVacunasList
from api.views.mascota_generic_views import MascotaListv3, MascotaDetailv3, MascotaPersonaListv3, MascotaVacunasListv3
from api.views.mascota_vset_views import MascotaViewSet, MascotaPersonaViewSet, MascotaVacunasViewSet

from api.views.persona_api_views import PersonaList

urlpatterns = [
    # =========== URLS DECORADOR (v1) ===========
    path('v1/mascotas/', mascotas_list),
    path('v1/mascotas/<int:pk>/', mascotas_detail),
    # urls persona list
    path('v1/mascotas/<int:pk>/persona/', persona_mascota_list),
    path('v1/mascotas/<int:pk>/vacunas/', vacunas_mascota_list),

    # =========== API VIEW (v2) ===========
    path('v2/mascotas/', MascotaList.as_view(), name="api_mascota_list_v2"),
    path('v2/mascotas/<int:pk>/', MascotaDetail.as_view(), name="api_mascota_list_v2"),
    # urls persona list
    path('v2/mascotas/<int:pk>/persona/', MascotaPersonaList.as_view(), name="api_mascota_persona_list_v2"),
    path('v2/mascotas/<int:pk>/vacunas/', MascotaVacunasList.as_view(), name="api_mascota_vacunas_list_v2"),

    # =========== GENERIC VIEW (v3) ===========
    path('v3/mascotas/', MascotaListv3.as_view(), name="api_mascota_list_v3"),
    path('v3/mascotas/<int:pk>/', MascotaDetailv3.as_view(), name="api_mascota_list_v3"),
    # urls persona list
    path('v3/mascotas/<int:pk>/persona/', MascotaPersonaListv3.as_view(), name="api_mascota_persona_list_v3"),
    path('v3/mascotas/<int:pk>/vacunas/', MascotaVacunasListv3.as_view(), name="api_mascota_vacunas_list_v3"),

    # =========== VIEWSET (v4) ===========
    path('v4/mascotas/', MascotaViewSet.as_view({'get': 'list', 'post': 'create'}), name="api_mascota_list_v4"),
    path('v4/mascotas/<int:pk>/', MascotaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'}),
         name="api_mascota_retrieve_v4"),
    # urls persona list
    path('v4/mascotas/<int:pk>/persona/', MascotaPersonaViewSet.as_view({'get': 'retrieve'}),
         name="api_mascota_persona_list_v4"),
    path('v4/mascotas/<int:pk>/vacunas/', MascotaVacunasViewSet.as_view({'get': 'retrieve'}),
         name="api_mascota_vacunas_list_v4"),


    # =========== Personas API VIEW (v2) ===========
    path('v2/personas/', PersonaList.as_view(), name="api_persona_list_v2"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
