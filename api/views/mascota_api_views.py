# Django imports
from django.http import Http404

# Django Rest Framework
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Models
from mascota.models import Mascota

# Serializer
from api.serializers import MascotaSerializer, PersonaSerializer, VacunaSerializer


class MascotaList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """
    Lista de mascotas o crear nuevas mascotas
    """
    def get(self, request, format=None):
        """
        Lista de mascotas
        http GET http://127.0.0.1:8000/api/v2/mascotas/
        :param request:
        :param format:
        :return:
        """
        mascotas = Mascota.objects.all()
        mascotas_serializer = MascotaSerializer(mascotas, many=True)
        return Response(mascotas_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Crea una nueva mascota
        http POST http://127.0.0.1:8000/api/v2/mascotas/ nombre="Loky" sexo="masculino" edad_aproximada="3" persona=2 raza=2 fecha_rescate="2022-07-11"
        :param request:
        :param format:
        :return:
        """
        mascotas_serializer = MascotaSerializer(data=request.data)
        if mascotas_serializer.is_valid():
            mascotas_serializer.save()
            return Response(mascotas_serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(mascotas_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MascotaDetail(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """
    Consulta, actualizar o borrar una instancia de mascotas
    """
    def get_object(self, pk):
        """
        Recupera la instancia de mascota
        :param pk: id de las mascota
        :return:
        """
        try:
            return Mascota.objects.get(pk=pk)
        except Mascota.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Muestra los detalles de una mascota
        http GET http://127.0.0.1:8000/api/v2/mascotas/2/
        Mustra los detall
        :param request: request con la data de la peticion
        :param pk:
        :param format:
        :return:
        """
        mascota = self.get_object(pk)
        serializer_mascota = MascotaSerializer(mascota)
        return Response(serializer_mascota.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        """
        Actualiza los detalles de un mascota
        http PUT http://127.0.0.1:8000/api/v2/mascotas/12/ nombre="Luz noceda" fecha_rescate="2022-06-11" sexo="femenino" edad_aproximada=3
        :param request: request con la data de la peticion
        :param pk:
        :param format:
        :return:
        """
        mascota = self.get_object(pk)
        serializer_mascota = MascotaSerializer(mascota, data=request.data)
        if serializer_mascota.is_valid():
            serializer_mascota.save()
            return Response(serializer_mascota.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_mascota.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Elimina el registro de una mascota
        http DELETE http://127.0.0.1:8000/api/v2/mascotas/2/
        :param request: request con la data de la peticion
        :param pk:
        :param format:
        :return:
        """
        mascotas = self.get_object(pk)
        mascotas.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MascotaPersonaList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """
    Consulta, actualizar o borrar una instancia de mascotas
    """
    def get_object(self, pk):
        """
        Recupera la instancia de mascota
        :param pk: id de las mascota
        :return:
        """
        try:
            mascota = Mascota.objects.select_related('persona', 'raza').get(pk=pk)
            persona = mascota.persona
            return persona
        except Mascota.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Muestra los detalles de una mascota
        http GET http://127.0.0.1:8000/api/v2/mascotas/2/persona/
        Mustra los detall
        :param request: request con la data de la peticion
        :param pk: id de las mascotas
        :param format:
        :return:
        """
        persona = self.get_object(pk)
        serializer_persona = PersonaSerializer(persona)
        return Response(serializer_persona.data, status=status.HTTP_200_OK)


class MascotaVacunasList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """
    Consulta, actualizar o borrar una instancia de mascotas
    """
    def get_object(self, pk):
        """
        Recupera la instancia de mascota
        :param pk: id de las mascota
        :return:
        """
        try:
            mascota = Mascota.objects.select_related('persona', 'raza').get(pk=pk)
            vacunas = mascota.vacuna.all()
            return vacunas
        except Mascota.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Muestra los detalles de una mascota
        http GET http://127.0.0.1:8000/api/v2/mascotas/2/vacunas/
        Mustra los detall
        :param request: request con la data de la peticion
        :param pk: id de las mascotas
        :param format:
        :return:
        """
        vacunas = self.get_object(pk)
        serializer_vacuna = VacunaSerializer(vacunas, many=True)
        return Response(serializer_vacuna.data, status=status.HTTP_200_OK)
