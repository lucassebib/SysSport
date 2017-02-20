from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from models import Deporte
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loguear, logout
from django.template import Context
from usuarios.models import Alumno, Profesor, UsuarioInvitado
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from usuarios.models import Persona
from django.http import HttpResponseRedirect



###############################ABM DEPORTES##############################################
def lista_deportes(request):
    template = "lista_deportes.html"
    
    ctx = {
        'deportes': Deporte.objects.all(), 
    }
   
    return render_to_response(template, ctx, context_instance=RequestContext(request))

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
    success_url = reverse_lazy('listar-deportes')

##########################################################################################
def ver_deportes_personas(request):
    template = "ver_deportes_personas.html" 
    id_usuario = request.user.id
    darse_de_baja = True

    try:
        g = Alumno.objects.get(id=id_usuario)
        extiende = 'baseAlumno.html'
    except Exception as e:
        try:
            g = Profesor.objects.get(id=id_usuario)
            extiende = 'baseProfesor.html'
            darse_de_baja = False
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
        'deportes': Persona.objects.get(id=request.user.id).lista_deporte.all(),
        'extiende': extiende,
        'usuario': request.user.username,
        'darse_de_baja': darse_de_baja,
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))


def listar_deportes(request):
    template = "listar_deportes.html"
   
    ctx = {
        'deportes': Deporte.objects.all(), 
        
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))

#Para Alumno y Usuario Invitado
@login_required
def inscripcion_deportes(request):
    template = "inscripcion_deportes.html"
    ctx = {
        'deportes': Deporte.objects.all(), 
        'deportes_alumno': Persona.objects.get(id=request.user.id).lista_deporte.all(),
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))

#Para Alumno y Usuario Invitado
@login_required
def baja_deporte(request, pk):
    template = "baja_deporte.html"

    if request.method == "POST":
        Persona.objects.get(id=request.user.id).lista_deporte.remove(pk)
        return HttpResponseRedirect('/ver-lista-deportes')   

    ctx = {
        'deporte': Deporte.objects.get(id=pk).nombre,
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))

#Para Alumno y Usuario Invitado
@login_required
def inscribir_deporte(request, pk):
    template = "inscribir_deporte.html"

    if request.method == "POST":
        Persona.objects.get(id=request.user.id).lista_deporte.add(Deporte.objects.get(id=pk))
        return HttpResponseRedirect('/ver-lista-deportes')   

    ctx = {
        'deporte': Deporte.objects.get(id=pk).nombre,
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))




        

