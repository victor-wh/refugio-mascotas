# Django imports
from django.http import Http404

# Django Rest Framework
from rest_framework import generics, status
from rest_framework.response import Response

# Models
from mascota.models import Mascota, Vacuna
from adopcion.models import Persona, Solicitud

# Serializer
from api.serializers import MascotaSerializer, PersonaSerializer, VacunaSerializer


# |------------------------------------------------|
# |         Generic class based views              |
# |------------------------------------------------|
class MascotaListv3(generics.ListCreateAPIView):
    """
    Lista de mascotas
    http GET http://127.0.0.1:8000/api/v3/mascotas/
    Crea una nueva mascota
    http POST http://127.0.0.1:8000/api/v3/mascotas/ nombre="Edalyn" sexo="femenino" edad_aproximada="3" persona=1 raza=1 fecha_rescate="2022-07-11"
    """
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer


class MascotaDetailv3(generics.RetrieveUpdateDestroyAPIView):
    """
    Muestra los detalles de una mascota
    http GET http://127.0.0.1:8000/api/v3/mascotas/16/
    Actualiza los detalles de un mascota
    http PUT http://127.0.0.1:8000/api/v3/mascotas/16/ nombre="Edalyn Clawthorne" fecha_rescate="2022-06-11" sexo="femenino" edad_aproximada=3
    Elimina el registro de una mascota
    http DELETE http://127.0.0.1:8000/api/v3/mascotas/16/
    """
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer


class MascotaPersonaListv3(generics.ListAPIView):
    """
    Lista las personas que adoptaron la mascota
    http GET http://127.0.0.1:8000/api/v3/mascotas/6/persona/
    """
    queryset = Persona.objects.all()

    def list(self, request, *args, **kwargs):
        # Recuperamos la mascota con el id que se envio
        try:
            mascota = Mascota.objects.get(**kwargs)
        except Mascota.DoesNotExist:
            raise Http404
        # Recuperamos la query
        queryset = self.get_queryset()
        # Aplicamos el filter al query de personas
        queryset = queryset.filter(id=mascota.persona.id)
        # Serializamos los datos
        serializer = PersonaSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MascotaVacunasListv3(generics.ListAPIView):
    """
    Lista las personas que adoptaron la mascota
    http GET http://127.0.0.1:8000/api/v3/mascotas/6/vacunas/
    """
    queryset = Vacuna.objects.all()

    def list(self, request, *args, **kwargs):
        # Recuperamos la mascota con el id que se envio
        try:
            mascota = Mascota.objects.get(**kwargs)
            id_vacunas = list(mascota.vacuna.all().values_list('id', flat=True))
        except Mascota.DoesNotExist:
            raise Http404
        # Recuperamos la query
        queryset = self.get_queryset()
        # Aplicamos el filter al query de personas
        queryset = queryset.filter(id__in=id_vacunas)
        # Serializamos los datos
        serializer = VacunaSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
