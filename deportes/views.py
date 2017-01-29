from models import Deporte
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loguear, logout
from django.template import Context
from usuarios.models import Alumno, Profesor, UsuarioInvitado
from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
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
    id_usuario = request.user.id
    try:
        g = Alumno.objects.get(id=id_usuario)
        extiende = 'baseAlumno.html'
    except Exception as e:
        try:
            g = Profesor.objects.get(id=id_usuario)
            extiende = 'baseProfesor.html'
        except Exception as e:
            try:
                g = UsuarioInvitado.objects.get(id=id_usuario)
                extiende = 'baseAlumno.html'
            except Exception as e:
                try:
                    extiende = 'inicio.html'
                except Exception as e:
                    if request.user.is_staff:
                        extiende = 'baseAdmin.html'
    ctx = {
        'deportes': Deporte.objects.all(), 
        'extiende': extiende,
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))


        