# Django imports
from django.http import Http404

# Django Rest Framework
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Models
from adopcion.models import Persona

# Serializer
from api.serializers import MascotaSerializer, PersonaSerializer, VacunaSerializer


class PersonaList(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    """
    Lista de mascotas o crear nuevas mascotas
    """
    def get(self, request, format=None):
        """
        Lista de mascotas
        http GET http://127.0.0.1:8000/api/v2/personas/
        :param request:
        :param format:
        :return:
        """
        persona = Persona.objects.all()
        persona_serializer = PersonaSerializer(persona, many=True)
        return Response(persona_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Crea una nueva mascota
        http POST http://127.0.0.1:8000/api/v2/personas/ nombre="Willow" apellidos="Park" edad=18 telefono=9983950079 email="victor.wis.p.h.ub@gmail.com" domicilio="cancun"
        :param request:
        :param format:
        :return:
        """
        persona_serializer = PersonaSerializer(data=request.data)
        if persona_serializer.is_valid():
            persona_serializer.save()
            return Response(persona_serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(persona_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonaDetail(APIView):
    """
    Consulta, actualizar o borrar una instancia de parsonas
    """
    def get_object(self, pk):
        """
        Recupera la instancia de persona
        :param pk: id de las persona
        :return:
        """
        try:
            return Persona.objects.get(pk=pk)
        except Persona.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Muestra los detalles de una persona
        http GET http://127.0.0.1:8000/api/v2/personas/2/
        :param request:
        :param pk:
        :param format:
        :return:
        """
        persona = self.get_object(pk)
        serializer_persona = PersonaSerializer(persona)
        return Response(serializer_persona.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        """
        Actualiza los detalles de un persona
        http PUT http://127.0.0.1:8000/api/v2/persona/2/ nombre="Luz noceda" fecha_rescate="2022-06-11" sexo="femenino" edad_aproximada=3
        :param request: request con la data de la peticion
        :param pk:
        :param format:
        :return:
        """
        persona = self.get_object(pk)
        serializer_persona = PersonaSerializer(persona, data=request.data)
        if serializer_persona.is_valid():
            serializer_persona.save()
            return Response(serializer_persona.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_persona.errors, status=status.HTTP_400_BAD_REQUEST)

