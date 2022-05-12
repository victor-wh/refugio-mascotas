import requests
import json

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from mascota.forms import MascotaForm, VacunaForm, MascotaFieldForm
from mascota.models import Mascota, Vacuna

from django.views.decorators.csrf import csrf_protect

# ViewSet
from api.views.mascota_api_views import MascotaList, MascotaDetail
from api.views.mascota_generic_views import MascotaListv3, MascotaPersonaListv3
from api.views.mascota_vset_views import MascotaViewSet

# Rest Framework
from rest_framework import status


# Create your views here.
def index(request):
    #return HttpResponse("Index")
    return render(request, "mascota/index.html")


def format_mascota(mascota):
    mascota = json.loads(json.dumps(mascota))
    return mascota


def mascota_list(request, api_version):
    local_domain = settings.LOCAL_DOMAIN  # localhost:8000
    request.content_type = "application/json"
    if api_version == 'v4':
        instance = MascotaViewSet()
        mascota_instance = instance.list(request)
    elif api_version == 'v2':
        instance = MascotaList()
        mascota_instance = instance.get(request)
    else:
        instance = MascotaViewSet()
        mascota_instance = instance.list(request)
    mascota_list = mascota_instance.data
    contexto = {'mascotas': mascota_list, 'api_version': api_version}
    return render(request, 'mascota/mascota_list.html', contexto)


def mascota_view(request, api_version):
    local_domain = settings.LOCAL_DOMAIN  # localhost:8000
    form = MascotaForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        # NOTA: es necesario el form is valid? Si, es necesario, mientras mas niveles de validacion mas seguro
        # es la consolidacion de datos, puede ser agregado despues de un request.POST como un flujo normal de validacion
        request.data = request.POST
        if form.is_valid():
            if api_version == 'v4':
                instance = MascotaViewSet()
                mascota_instance = instance.create(request=request)
            elif api_version == 'v2':
                instance = MascotaList()
                mascota_instance = instance.post(request=request)
            else:
                instance = MascotaViewSet()
                mascota_instance = instance.create(request=request)

            if mascota_instance.status_code == status.HTTP_201_CREATED:
                return HttpResponseRedirect((reverse('mascota_listarfuncion', args=[api_version])))
            else:
                # En caso de errores provenientes del endpoint los agregamos manualmente al formulario
                serializers_errors = mascota_instance.data.serializer.errors
                for error in serializers_errors:
                    form.add_error(error, serializers_errors.get(error)[0].title())
    else:
        form = MascotaForm()
    return render(request, 'mascota/mascota_form.html', {'form': form, 'api_version': api_version})


def mascota_list2(request, api_version):
    instance = MascotaListv3()
    mascota_instance = instance.list(request)
    mascota_instance = mascota_instance.data
    mascota_list = []
    for mascota in mascota_instance:
        mascota = format_mascota(mascota)
        mascota_list.append(mascota)
    contexto = {'mascotas': mascota_list, 'api_version': api_version}
    return render(request, 'mascota/mascota_list.html', contexto)


def mascota_edit(request, api_version, id_mascota):
    local_domain = settings.LOCAL_DOMAIN  # localhost:8000
    mascota = Mascota.objects.get(id=id_mascota)
    if request.method == 'POST':
        request.data = request.POST
        form = MascotaForm(request.POST)
        if form.is_valid():
            if api_version == 'v4':
                instance = MascotaViewSet()
                mascota_instance = instance.update(request=request, pk=id_mascota)
            elif api_version == 'v2':
                instance = MascotaDetail()
                mascota_instance = instance.put(request=request, pk=id_mascota)
            else:
                instance = MascotaViewSet()
                mascota_instance = instance.update(request=request, pk=id_mascota)

            if mascota_instance.status_code == status.HTTP_200_OK:
                return HttpResponseRedirect((reverse('mascota_listarfuncion', args=[api_version])))
            else:
                # En caso de errores provenientes del endpoint los agregamos manualmente al formulario

                serializers_errors = mascota_instance.data.serializer.errors
                for error in serializers_errors:
                    form.add_error(error, serializers_errors.get(error)[0].title())
    else:
        if api_version == 'v4':
            instance = MascotaViewSet()
            mascota_instance = instance.retrieve(request=request, pk=id_mascota)
        elif api_version == 'v2':
            instance = MascotaDetail()
            mascota_instance = instance.get(request=request, pk=id_mascota)
        else:
            instance = MascotaViewSet()
            mascota_instance = instance.retrieve(request=request, pk=id_mascota)
        mascota_instance = mascota_instance.data
        mascota_instance = format_mascota(mascota_instance)
        mascota_instance['vacuna'] = vacunas = [d['id'] for d in mascota_instance.get('vacuna')]
        mascota_instance['persona'] = mascota_instance.get('persona').get('id')
        form = MascotaForm(initial=mascota_instance)

    return render(request, 'mascota/mascota_form.html', {'form': form, 'api_version': api_version})


def mascota_delete(request, api_version, id_mascota):
    if request.method == 'POST':
        if api_version == 'v4':
            instance = MascotaViewSet()
            mascota_instance = instance.delete(request=request, pk=id_mascota)
        elif api_version == 'v2':
            instance = MascotaDetail()
            mascota_instance = instance.delete(request=request, pk=id_mascota)
        else:
            instance = MascotaViewSet()
            mascota_instance = instance.delete(request=request, pk=id_mascota)
        if mascota_instance.status_code == status.HTTP_204_NO_CONTENT:
            return HttpResponseRedirect((reverse('mascota_listarfuncion', args=[api_version])))
        else:
            messages.warning(request, message=str(mascota_instance.text))
    else:
        if api_version == 'v4':
            instance = MascotaViewSet()
            mascota_instance = instance.retrieve(request=request, pk=id_mascota)
        elif api_version == 'v2':
            instance = MascotaDetail()
            mascota_instance = instance.get(request=request, pk=id_mascota)
        else:
            instance = MascotaViewSet()
            mascota_instance = instance.retrieve(request=request, pk=id_mascota)
        mascota_instance = mascota_instance.data
        mascota_instance = format_mascota(mascota_instance)
    return render(request, 'mascota/mascota_delete.html', {'mascota': mascota_instance, 'api_version': api_version})


def vacuna_view(request):
    form = VacunaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('vacuna_listarclase')
    else:
        form = VacunaForm()
    return render(request, 'mascota/vacuna_form.html', {'form':form})


def vacuna_list(request):
    vacuna = Vacuna.objects.all().order_by('id')
    contexto = {'vacunas':vacuna}
    return render(request, 'mascota/vacuna_list.html', contexto)


def vacuna_edit(request, id_vacuna):
    vacuna = Vacuna.objects.get(id=id_vacuna)
    if request.method == 'GET':
        form = VacunaForm(instance=vacuna)
    else:
        form = VacunaForm(request.POST, instance=vacuna)
        if form.is_valid():
            form.save()
            return redirect('vacuna_listarfuncion')
    return render(request, 'mascota/vacuna_form.html', {'form':form})


def vacuna_delete(request,id_vacuna):
    vacuna = Vacuna.objects.get(id=id_vacuna)
    if request.method == 'POST':
        vacuna.delete()
        return redirect('vacuna_listarfuncion')
    return render(request, 'mascota/vacuna_delete.html', {'vacuna':vacuna})


class MascotaList2(ListView):
    model = Mascota
    template_name = "mascota/mascota_list.html"


class MascotaCreate(CreateView):
    model = Mascota
    form_class = MascotaForm
    template_name = 'mascota/mascota_form.html'
    success_url = reverse_lazy('mascota_listarclase')


class MascotaUpdate(UpdateView):
    model = Mascota
    form_class = MascotaForm
    template_name = 'mascota/mascota_form.html'
    success_url = reverse_lazy('mascota_listarclase')


class MascotaDelete(DeleteView):
    model = Mascota
    template_name = 'mascota/mascota_delete.html'
    success_url = reverse_lazy('mascota_listarclase')


class VacunaList(ListView):
    model = Vacuna
    template_name = 'mascota/vacuna_list.html'


class VacunaUpdate(UpdateView):
    model = Vacuna
    form_class = VacunaForm
    template_name = 'mascota/vacuna_form.html'
    success_url = reverse_lazy('vacuna_listarclase')


class VacunaCreate(CreateView):
    model = Vacuna
    form_class = VacunaForm
    template_name = 'mascota/vacuna_form.html'
    success_url = reverse_lazy('vacuna_listarclase')


class VacunaDelete(DeleteView):
    model = Vacuna
    template_name = 'mascota/vacuna_delete.html'
    success_url = reverse_lazy('vacuna_listarclase')