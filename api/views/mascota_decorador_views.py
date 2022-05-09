# Django imports
from django.shortcuts import render

# Django Rest Framework imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Serializers imports
from api.serializers import MascotaSerializer, PersonaSerializer, VacunaSerializer

# Models imports
from mascota.models import Mascota
from adopcion.models import Persona, Solicitud


@api_view(['GET', 'POST'])
def mascotas_list(request, format=None):
    """
    Recupera la lista de mascotas o crea nuevas mascotas
    """
    if request.method == 'GET':
        """
        Lista de mascotas
        http GET http://127.0.0.1:8000/api/v1/mascotas/
        """
        mascotas = Mascota.objects.select_related('persona', 'raza').all()
        mascotas_serializer = MascotaSerializer(mascotas, many=True)
        return Response(mascotas_serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        """
        Crea una nueva mascota
        http POST http://127.0.0.1:8000/api/v1/mascotas/ nombre="takoyaki" sexo="masculino" edad_aproximada="3" persona=1 raza=1 fecha_rescate="20  22-02-11"
        """
        mascota_serializer = MascotaSerializer(data=request.data)
        if mascota_serializer.is_valid():
            mascota_serializer.save()
            return Response(mascota_serializer.data, status=status.HTTP_201_CREATED)
        return Response(mascota_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def mascotas_detail(request, pk, format=None):
    try:
        mascota = Mascota.objects.select_related('persona', 'raza').get(pk=pk)
    except Mascota.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        """
        Muestra los detalles de un mascotas
        http GET http://127.0.0.1:8000/api/v1/mascotas/2/
        http GET http://127.0.0.1:8000/api/v1/persona/2/ -> Deberia traer todas las mascotas de esta persona
        """
        mascota = MascotaSerializer(mascota)
        return Response(mascota.data)

    elif request.method == 'PUT':
        """
        Actualiza los detalles de un mascotas
        http PUT http://127.0.0.1:8000/api/v1/mascotas/2/ nombre="king Clawthorne" "fecha_rescate": "2022-02-11" "sexo": "masculino" edad_aproximada=3
        """
        mascota = MascotaSerializer(mascota, data=request.data)
        if mascota.is_valid():
            mascota.save()
            return Response(mascota.data)
        return Response(mascota.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        """
        Elimina los detalles de un mascotas
        http DELETE http://127.0.0.1:8000/api/v1/mascotas/2/
        """
        mascota.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def persona_mascota_list(request, pk, format=None):
    """
    Recupera la persona asignada a una mascota
    """
    try:
        mascota = Mascota.objects.select_related('persona', 'raza').get(pk=pk)
        persona = mascota.persona
    except Mascota.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        """
        Lista de mascotas traidas a partir del id de una persona
        http GET http://127.0.0.1:8000/api/v1/mascotas/{id_mascota}/persona
        """
        persona = PersonaSerializer(persona)
        return Response(persona.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def vacunas_mascota_list(request, pk, format=None):
    """
    Recupera la lista de vacunas de una sola mascota
    """
    try:
        mascota = Mascota.objects.select_related('persona', 'raza').get(pk=pk)
        vacunas = mascota.vacuna.all()
    except Mascota.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        """
        Lista de mascotas traidas a partir del id de una persona
        http GET http://127.0.0.1:8000/api/v1/mascotas/{id_mascota}/persona
        """
        vacunas = VacunaSerializer(vacunas, many=True)
        return Response(vacunas.data, status=status.HTTP_200_OK)
