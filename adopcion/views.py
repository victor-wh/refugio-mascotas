import requests

from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from adopcion.models import Solicitud, Persona
from adopcion.forms import SolicitudForm, PersonaForm


# Create your views here.
def index_adopcion(request):
    #return HttpResponse("soy la pagina principal de la app adopcion")
    return render(request, 'adopcion/index.html')


class SolicitudList(ListView):
    model = Solicitud
    template_name = 'adopcion/solicitud_list.html'


class SolicitudCreate(CreateView):
    model = Solicitud
    template_name = 'adopcion/solicitud_form.html'
    form_class = SolicitudForm
    second_form_class = PersonaForm
    success_url = reverse_lazy('solicitud_listarclase')

    def get_context_data(self, **kwargs):
        context = super(SolicitudCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            solicitud = form.save(commit=False)
            solicitud.persona = form2.save()
            solicitud.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))


class SolicitudUpdate(UpdateView):
    model = Solicitud
    second_model = Persona
    template_name = 'adopcion/solicitud_form.html'
    form_class = SolicitudForm
    second_form_class = PersonaForm
    success_url = reverse_lazy('adopcion:solicitud_listarclase')

    def get_context_data(self, **kwargs):
        context = super(SolicitudUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        solicitud = self.model.objects.get(id=pk)
        persona = self.second_model.objects.get(id=solicitud.persona_id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=persona)
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_solicitud = kwargs['pk']
        solicitud = self.model.objects.get(id=id_solicitud)
        persona = self.second_model.objects.get(id=solicitud.persona_id)
        form = self.form_class(request.POST, instance=solicitud)
        form2 = self.second_form_class(request.POST, instance=persona)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class SolicitudDelete(DeleteView):
    model = Solicitud
    template_name = 'adopcion/solicitud_delete.html'
    success_url = reverse_lazy('adopcion:solicitud_listarclase')


class PersonaList(ListView):
    model = Persona
    template_name = 'adopcion/persona_list.html'


class PersonaDelete(DeleteView):
    model = Persona
    template_name = 'adopcion/persona_delete.html'
    success_url = reverse_lazy('adopcion:persona_listarclase')


class PersonaDetail(DetailView):
    model = Persona
    template_name = 'adopcion/persona_detail.html'


def solicitud_list(request):
    solicitud = Solicitud.objects.all().order_by('id')
    contexto = {'solicitudes':solicitud}
    return render(request, 'adopcion/solicitud_list.html', contexto)


def persona_detail(request, id_mascota):
    local_domain = settings.LOCAL_DOMAIN  # localhost:8000
    url = 'http://{0}{1}'.format(local_domain, reverse("api_mascota_persona_list_v2", args=[id_mascota]))
    response = requests.get(url=url, cookies=request.COOKIES)
    persona = []
    if response.status_code == 200:
        persona = response.json()
    else:
        print("NO TIENE SESSION INICIADA")
    return render(request, 'adopcion/persona_detail.html', {'object': persona})


def persona_list(request):
    persona = Persona.objects.all().order_by('id')
    contexto = {'personas': persona}
    return render(request, 'adopcion/persona_list.html', contexto)


def persona_delete(request,id_persona):
    persona = Persona.objects.get(id=id_persona)
    if request.method == 'POST':
        persona.delete()
        return redirect('adopcion:persona_listarfuncion')
    return render(request, 'adopcion/persona_delete.html', {'object':persona})


def solicitud_delete(request,id_solicitud):
    solicitud = Solicitud.objects.get(id=id_solicitud)
    #persona = Persona.objects.get(id=solicitud.persona_id)
    if request.method == 'POST':
        solicitud.delete()
        #persona.delete()
        return redirect('adopcion:solicitud_listarfuncion')
    return render(request, 'adopcion/solicitud_delete.html', {'solicitud':solicitud})


def solicitud_view(request):
    form = SolicitudForm(request.POST or None)
    form2 = PersonaForm(request.POST or None)
    if request.method == 'POST':
        # form = SolicitudForm(request.POST)
        # form2 = PersonaForm(request.POST)
        if form.is_valid() and form2.is_valid():
            solicitud = form.save(commit=False)
            solicitud.persona = form2.save()
            solicitud.save()
            return redirect('adopcion:solicitud_listarfuncion')
    # else:
    #     form = SolicitudForm()
    #     form2 = PersonaForm()
    return render(request, 'adopcion/solicitud_form.html', {'form':form, 'form2': form2})


def solicitud_edit(request, id_solicitud):
    solicitud = Solicitud.objects.get(id=id_solicitud)
    persona = Persona.objects.get(id=solicitud.persona_id)
    if request.method == 'GET':
        form = SolicitudForm(instance=solicitud)
        form2 = PersonaForm(instance=persona)
    else:
        form = SolicitudForm(request.POST, instance=solicitud)
        form2 = PersonaForm(request.POST, instance=persona)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
        return redirect('adopcion:solicitud_listarfuncion')
    return render(request, 'adopcion/solicitud_form.html', {'form':form, 'form2': form2})