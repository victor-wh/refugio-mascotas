from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from mascota.forms import MascotaForm, VacunaForm
from mascota.models import Mascota, Vacuna


# Create your views here.
def index(request):
    #return HttpResponse("Index")
    return render(request,"mascota/index.html")

def mascota_view(request):
    form = MascotaForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        #form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mascota:mascota_listarfuncion')
    else:
        form = MascotaForm()
    return render(request, 'mascota/mascota_form.html', {'form':form})

def mascota_list(request):
    mascota = Mascota.objects.all().order_by('id')
    contexto = {'mascotas':mascota}
    return render(request, 'mascota/mascota_list.html', contexto)

def mascota_edit(request,id_mascota):
    mascota = Mascota.objects.get(id=id_mascota)
    if request.method == 'GET':
        form = MascotaForm(instance=mascota)
    else:
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('mascota:mascota_listarfuncion')
    return render(request, 'mascota/mascota_form.html', {'form':form})

def mascota_delete(request,id_mascota):
    mascota = Mascota.objects.get(id=id_mascota)
    if request.method == 'POST':
        mascota.delete()
        return redirect('mascota:mascota_listarfuncion')
    return render(request, 'mascota/mascota_delete.html', {'mascota':mascota})

def vacuna_view(request):
    form = VacunaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('mascota:vacuna_listarclase')
    else:
        form = VacunaForm()
    return render(request, 'mascota/vacuna_form.html', {'form':form})

def vacuna_list(request):
    vacuna = Vacuna.objects.all().order_by('id')
    contexto = {'vacunas':vacuna}
    return render(request, 'mascota/vacuna_list.html', contexto)

def vacuna_edit(request,id_vacuna):
    vacuna = Vacuna.objects.get(id=id_vacuna)
    if request.method == 'GET':
        form = VacunaForm(instance=vacuna)
    else:
        form = VacunaForm(request.POST, instance=vacuna)
        if form.is_valid():
            form.save()
            return redirect('mascota:vacuna_listarfuncion')
    return render(request, 'mascota/vacuna_form.html', {'form':form})

def vacuna_delete(request,id_vacuna):
    vacuna = Vacuna.objects.get(id=id_vacuna)
    if request.method == 'POST':
        vacuna.delete()
        return redirect('mascota:vacuna_listarfuncion')
    return render(request, 'mascota/vacuna_delete.html', {'vacuna':vacuna})

class MascotaList(ListView):
    model = Mascota
    template_name = "mascota/mascota_list.html"

class MascotaCreate(CreateView):
    model = Mascota
    form_class = MascotaForm
    template_name = 'mascota/mascota_form.html'
    success_url = reverse_lazy('mascota:mascota_listarclase')

class MascotaUpdate(UpdateView):
    model = Mascota
    form_class = MascotaForm
    template_name = 'mascota/mascota_form.html'
    success_url = reverse_lazy('mascota:mascota_listarclase')

class MascotaDelete(DeleteView):
    model = Mascota
    template_name = 'mascota/mascota_delete.html'
    success_url = reverse_lazy('mascota:mascota_listarclase')

class VacunaList(ListView):
    model = Vacuna
    template_name = 'mascota/vacuna_list.html'

class VacunaUpdate(UpdateView):
    model = Vacuna
    form_class = VacunaForm
    template_name = 'mascota/vacuna_form.html'
    success_url = reverse_lazy('mascota:vacuna_listarclase')

class VacunaCreate(CreateView):
    model = Vacuna
    form_class = VacunaForm
    template_name = 'mascota/vacuna_form.html'
    success_url = reverse_lazy('mascota:vacuna_listarclase')

class VacunaDelete(DeleteView):
    model = Vacuna
    template_name = 'mascota/vacuna_delete.html'
    success_url = reverse_lazy('mascota:vacuna_listarclase')