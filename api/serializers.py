import imp
from wsgiref import validate
from rest_framework import serializers

from adopcion.models import Persona, Solicitud
from mascota.models import Mascota, Raza, Vacuna


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['id', 'nombre', 'apellidos', 'edad', 'telefono', 'email', 'domicilio']


class VacunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacuna
        fields = ['id', 'nombre']


class RazaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raza
        fields = ['id', 'nombre', 'caracteristica', 'comportamiento']


class MascotaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mascota
        fields = ['id', 'nombre', 'imagen', 'sexo', 'edad_aproximada', 'fecha_rescate', 'vacuna', 'persona', 'raza']

    def to_representation(self, instance):
        self.fields['vacuna'] = VacunaSerializer(read_only=True, many=True)
        self.fields['persona'] = PersonaSerializer(read_only=True)
        self.fields['raza'] = RazaSerializer(read_only=True)
        return super(MascotaSerializer, self).to_representation(instance)
