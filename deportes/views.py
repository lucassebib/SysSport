from models import Deporte
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

class ListarDeportes(ListView):
    model = Deporte
    context_object_name = 'deportes'

class DetallesDeportes(DetailView):
    model = Deporte
    context_object_name = 'deportes'

class CrearDeportes(CreateView):
    model = Deporte
    #fields = ['nombre', 'fundacion', 'genero', 'origen']

class ActualizarDeportes(UpdateView):
    model = Deporte
    #fields = ['nombre', 'fundacion', 'genero', 'origen']

class EliminarDeportes(DeleteView):
    model = Deporte
    context_object_name = 'deportes'
    success_url = reverse_lazy('listar-deporte')