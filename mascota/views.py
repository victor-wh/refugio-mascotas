import requests
import json

from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from mascota.forms import MascotaForm, VacunaForm
from mascota.models import Mascota, Vacuna

from django.views.decorators.csrf import csrf_protect


# Create your views here.
def index(request):
    #return HttpResponse("Index")
    return render(request,"mascota/index.html")


def mascota_view(request):
    local_domain = settings.LOCAL_DOMAIN  # localhost:8000
    form = MascotaForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        url = 'http://{0}{1}'.format(local_domain, reverse("api_mascota_list_v2"))
        response = requests.post(url=url, cookies=request.COOKIES, data=request.POST)
        return redirect('mascota_listarfuncion')
    else:
        form = MascotaForm()
    return render(request, 'mascota/mascota_form.html', {'form': form})


def mascota_list(request):
    local_domain = settings.LOCAL_DOMAIN  # localhost:8000
    url = 'http://{0}{1}'.format(local_domain, reverse("api_mascota_list_v2"))
    response = requests.get(url=url, cookies=request.COOKIES)
    mascota = []
    if response.status_code == 200:
        mascota = response.json()
    else:
        print("NO TIENE SESSION INICIADA")
    contexto = {'mascotas': mascota}
    return render(request, 'mascota/mascota_list.html', contexto)


def mascota_edit(request, id_mascota):
    local_domain = settings.LOCAL_DOMAIN  # localhost:8000
    mascota = Mascota.objects.get(id=id_mascota)
    if request.method == 'POST':
        url = 'http://{0}{1}'.format(local_domain, reverse("api_mascota_list_v2", args=[id_mascota]))
        csrf_token = request.COOKIES.get('csrftoken')
        response = requests.put(url=url, cookies=request.COOKIES, headers={'X-CSRFToken': csrf_token}, data=request.POST)
        return redirect('mascota_listarfuncion')
    else:
        url = 'http://{0}{1}'.format(local_domain, reverse("api_mascota_list_v2", args=[id_mascota]))
        response = requests.get(url=url, cookies=request.COOKIES)
        dic_initial = json.loads(response.content)
        vacunas = [d['id'] for d in dic_initial.get('vacuna')]
        dic_initial['vacuna'] = vacunas
        dic_initial['persona'] = dic_initial.get('persona').get('id')
        form = MascotaForm(initial=dic_initial)

    return render(request, 'mascota/mascota_form.html', {'form': form})


def mascota_delete(request, id_mascota):
    mascota = Mascota.objects.get(id=id_mascota)
    if request.method == 'POST':
        local_domain = settings.LOCAL_DOMAIN  # localhost:8000
        url = 'http://{0}{1}'.format(local_domain, reverse("api_mascota_list_v2", args=[id_mascota]))
        csrf_token = request.COOKIES.get('csrftoken')
        response = requests.delete(url=url, cookies=request.COOKIES, headers={'X-CSRFToken': csrf_token})
        if response.status_code == 200:
            print("success")
        return redirect('mascota_listarfuncion')
    return render(request, 'mascota/mascota_delete.html', {'mascota':mascota})


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


class MascotaList(ListView):
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