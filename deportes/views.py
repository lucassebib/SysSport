from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from models import Deporte, FichaMedica
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loguear, logout
from django.template import Context
from usuarios.models import Alumno, Profesor, UsuarioInvitado
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from usuarios.models import Persona
from django.http import HttpResponseRedirect
from forms import FormularioSubirFichaMedica



############################### CRUD DEPORTES ##############################################
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
    success_url = reverse_lazy('lista_deportes')

###################################### PARA TODOS ####################################################
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
                darse_de_baja = False   
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


def deporte_detalle(request, pk):
    template = "deporte_detalle.html"

    ctx = {
        'deporte': Deporte.objects.get(id=pk)
    }

    return render_to_response(template, ctx, context_instance=RequestContext(request))

######################################## PARA ALUMNOS ##################################################
@login_required
def inscripcion_deportes(request):
    template = "inscripcion_deportes.html"
    id_usuario = request.user.id
    darse_de_baja = True
    try:
        g = Alumno.objects.get(id=id_usuario)
        darse_de_baja = True
    except Exception as e:
        try:
            g = Profesor.objects.get(id=id_usuario)
            darse_de_baja = False
        except Exception as e:
            try:
                g = UsuarioInvitado.objects.get(id=id_usuario)
                darse_de_baja = False   
            except Exception as e:
                try:
                    extiende = 'inicio.html'
                    darse_de_baja = True
                except Exception as e:
                    if request.user.is_staff:
                        extiende = 'baseAdmin.html'
                        darse_de_baja = True

    ctx = {
        'deportes': Deporte.objects.all(), 
        'deportes_alumno': Persona.objects.get(id=request.user.id).lista_deporte.all(),
        'darse_de_baja': darse_de_baja,
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))

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

@login_required
def inscribir_deporte(request, pk):
    template = "inscribir_deporte.html"
    mensaje = ""

    if request.method == "POST":
        d = Deporte.objects.get(id=pk)
        p = Persona.objects.get(id=request.user.id)
        if d.apto_para == p.sexo or d.apto_para == 3: 
            p.lista_deporte.add(d)
            return HttpResponseRedirect('/ver-lista-deportes')
        else:
            mensaje = "ESTE DEPORTE ES APTO PARA: " + d.ver_aptopara()    

    ctx = {
        'mensaje': mensaje,
        'deporte': Deporte.objects.get(id=pk).nombre,
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))

######################################## PARA PROFESORES ##################################################
def subir_fichaMedicaStandar(request, pk):
    template = "profesor/subir_fichaMedicaStandar.html"
    form = FormularioSubirFichaMedica()
    deporte = Deporte.objects.get(id=pk)
    
    try:
        ficha = FichaMedica.objects.get(id=deporte.ficha_medica.id)
    except Exception as e:
        ficha = ""
    mensaje= 'no llego'
    
    if request.method == 'POST':
        form = FormularioSubirFichaMedica(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                if deporte.ficha_medica:
                    f = FichaMedica.objects.get(id=deporte.ficha_medica.id)
                    f.ficha_medica.delete(False)
                    f.ficha_medica = form.cleaned_data['ficha_medica']
                    f.descripcion = form.cleaned_data['descripcion']
                    f.save()
                    deporte.ficha_medica = f
                    deporte.save()
                    return HttpResponseRedirect('')
                else:
                    nueva_ficha = FichaMedica()
                    nueva_ficha.ficha_medica = form.cleaned_data['ficha_medica']
                    nueva_ficha.descripcion = form.cleaned_data['descripcion']
                    nueva_ficha.save()
                    deporte.ficha_medica = nueva_ficha
                    deporte.save()
                    return HttpResponseRedirect('')

            else:
                return HttpResponseRedirect('/modificar_perfil_profesor')
        else:
            return HttpResponseRedirect('/novedades')


    ctx = {
        'mensaje': mensaje,
        'form': form,
        'deporte': deporte,
        'ficha': ficha,
    }

    return render_to_response(template, ctx, context_instance=RequestContext(request))

def listar_parafichaMedica(request):
    template = "profesor/listar_parafichaMedica.html"
    deportes = Profesor.objects.get(id=request.user.id).lista_deporte.all()
    ctx = {
        'deportes': Deporte.objects.filter(id__in=deportes)     
    }

    return render_to_response(template, ctx, context_instance=RequestContext(request))




        

