# Django import
from django.http import Http404
from django.shortcuts import get_object_or_404

# Django rest framework
from rest_framework import viewsets, status
from rest_framework.response import Response

# Serializers imports
from api.serializers import MascotaSerializer, PersonaSerializer, VacunaSerializer

# Models imports
from mascota.models import Mascota
from adopcion.models import Persona, Solicitud


class MascotaViewSet(viewsets.ViewSet):
    """
    ViewSet para recuperar el crud de mascotas
    """

    def get_object(self, pk):
        try:
            return Mascota.objects.get(pk=pk)
        except Mascota.DoesNotExist:
            raise Http404

    def list(self, request):
        """
        Muestra la lista de mascotas
        http GET http://127.0.0.1:8000/api/v4/mascotas/
        :param request:
        :return:
        """
        queryset = Mascota.objects.all()
        serializer = MascotaSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Crea un nuevo registro en el modelo mascotas
        http POST http://127.0.0.1:8000/api/v4/mascotas/ nombre="Rainer" sexo="masculino" edad_aproximada="3" persona=2 raza=2 fecha_rescate="2022-07-11"
        :param request:
        :return:
        """
        serializer = MascotaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Muestra los detalles de una mascota
        http GET http://127.0.0.1:8000/api/v4/mascotas/1/
        :param request:
        :param pk:
        :return:
        """
        queryset = Mascota.objects.all()
        mascota = get_object_or_404(queryset, pk=pk)
        serializer = MascotaSerializer(mascota)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Actualiza los detalles de un mascota
        http PUT http://127.0.0.1:8000/api/v4/mascotas/5/ nombre="Hootie Clau" fecha_rescate="2022-08-12" sexo="masculino" edad_aproximada=5
        :param request:
        :param pk:
        :return:
        """
        queryset = self.get_object(pk)
        serializer = MascotaSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Elimina el registro de una mascota
        http DELETE http://127.0.0.1:8000/api/v4/mascotas/5/
        :param request:
        :param pk:
        :param format:
        :return:
        """
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MascotaPersonaViewSet(viewsets.ViewSet):
    """
    Recupera el dueño de una mascota
    """
    def get_object(self, pk):
        try:
            mascota = Mascota.objects.get(pk=pk)
            persona = mascota.persona
            return persona
        except Mascota.DoesNotExist:
            raise Http404

    def retrieve(self, request, pk=None):
        """
        Muestra la lista de mascotas
        http GET http://127.0.0.1:8000/api/v4/mascotas/1/persona/
        :param request:
        :return:
        """
        queryset = self.get_object(pk)
        serializer = PersonaSerializer(queryset)
        return Response(serializer.data)


class MascotaVacunasViewSet(viewsets.ViewSet):
    """
    Recuper las vacunas de una mascota
    """
    def get_object(self, pk):
        try:
            mascota = Mascota.objects.get(pk=pk)
            persona = mascota.vacuna.all()
            return persona
        except Mascota.DoesNotExist:
            raise Http404

    def retrieve(self, request, pk=None):
        """
        Muestra la lista de mascotas
        http GET http://127.0.0.1:8000/api/v4/mascotas/1/vacunas/
        :param request:
        :return:
        """
        queryset = self.get_object(pk)
        serializer = VacunaSerializer(queryset, many=True)
        return Response(serializer.data)
