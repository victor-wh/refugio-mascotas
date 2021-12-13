from __future__ import unicode_literals

from django.db import models
from adopcion.models import Persona


# Create your models here.
class Vacuna(models.Model):
    nombre = models.CharField(max_length=50)
    def __unicode__(self):
        return '{}'.format(self.nombre)


def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return '%s-%s-%s.%s' %(instance.persona, instance.nombre, instance.fecha_rescate, extension)

class Mascota(models.Model):
    # folio = models.CharField(max_length=10,primary_key=True)
    nombre = models.CharField(max_length=50)
    sexo = models.CharField(max_length=10)
    edad_aproximada = models.IntegerField()
    fecha_rescate = models.DateField()
    persona = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)
    vacuna = models.ManyToManyField(Vacuna, blank=True)
    imagen = models.ImageField(upload_to = upload_location, null=True, blank=True)

