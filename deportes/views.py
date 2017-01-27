from models import Deporte
from django.shortcuts import render_to_response
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from usuarios.models import Persona

###############################ABM DEPORTES##############################################
class ListarDeportes(ListView):
    model = Deporte
    context_object_name = 'deportes'

class DetallesDeportes(DetailView):
    model = Deporte
    context_object_name = 'deportes'

class CrearDeportes(CreateView):
    model = Deporte

class ActualizarDeportes(UpdateView):
    model = Deporte

class EliminarDeportes(DeleteView):
    model = Deporte
    context_object_name = 'deportes'
    success_url = reverse_lazy('listar-deporte')

##########################################################################################
def ver_deportes_personas(request):
    template = "ver_deportes_personas.html"    
    ctx = {
        'deportes': Persona.objects.get(id=request.user.id).lista_deporte.all(),
        'usuario': request.user.username
    }
    return render_to_response(template, ctx)

def listar_deportes(request):
    template = "lista_deportes.html"
    ctx = {
        'deportes': Deporte.objects.all()
    }
    return render_to_response(template, ctx)