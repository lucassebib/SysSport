#from django.shortcuts import render, render_to_response, RequestContext
#from django.http import HttpResponseRedirect
#from forms import FormularioCrearCancha
from models import Cancha
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

class ListarCanchas(ListView):
    model = Cancha
    context_object_name = 'canchas'

class DetallesCanchas(DetailView):
    model = Cancha
    context_object_name = 'canchas'

class CrearCanchas(CreateView):
    model = Cancha
    #fields = ['nombre', 'fundacion', 'genero', 'origen']

class ActualizarCanchas(UpdateView):
    model = Cancha
    #fields = ['nombre', 'fundacion', 'genero', 'origen']

class EliminarCanchas(DeleteView):
    model = Cancha
    context_object_name = 'canchas'
    success_url = reverse_lazy('listar-canchas')