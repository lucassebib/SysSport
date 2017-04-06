from django.contrib.auth import authenticate, login as loguear, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.template import Context
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from models import Deporte, FichaMedica
from entrenamiento.forms import FormularioCrearEntrenamiento
from entrenamiento.models import Entrenamiento
from usuarios.models import Alumno, Profesor, UsuarioInvitado, Persona

from deportes.funciones import *
from usuarios.funciones import *

from forms import * 

############################## DEPORTES PARA INTERNAUTAS ########################################

def deporte_detalle(request, pk):
    template = "deporte_detalle.html"
    deporte = Deporte.objects.get(id=pk)
    id_usuario = obtener_id(request)
    extiende = extiende_de(id_usuario, request)
    e = deporte.entrenamientos.all()
    try:
        profesor = Profesor.objects.get(lista_deporte__in=pk)
    except Exception as e:
        profesor= ''
    
    ctx = {
        'deporte': deporte,
        'entrenamientos': e,
        'profesor': profesor,
        'extiende': extiende,
    }

    return render_to_response(template, ctx, context_instance=RequestContext(request))

############################### CRUD DEPORTES ##############################################
#def lista_deportes(request):
    #template = "lista_deportes.html"
    
    #ctx = {
   #     'deportes': Deporte.objects.all(), 
  #  }
   
 #   return render_to_response(template, ctx, context_instance=RequestContext(request))

#class DetallesDeportes(DetailView):
 #   model = Deporte
#    context_object_name = 'deportes'

# Crear deporte admin

def crear_deporte(request):
    template = "deportes/deporte_form.html"
    form_deporte = FormularioCrearDeporte()
    #form_entrenamiento = FormularioCrearEntrenamiento()
   

    if request.method == 'POST' and 'bAceptar' in request.POST:
        form_deporte = FormularioCrearDeporte(request.POST, request.FILES)
        if form_deporte.is_valid():
          nombre = form_deporte.cleaned_data['nombre']
          genero = form_deporte.cleaned_data['apto_para']
          descripcion = form_deporte.cleaned_data['descripcion']
                  
          d = Deporte()
          d.nombre = nombre
          d.apto_para = genero
          d.descripcion = descripcion
          d.save()
          return HttpResponseRedirect(reverse('listar-deporte'))

    ctx = {
        'form_deporte': form_deporte,
       # 'form_entrenamiento': form_entrenamiento,
    }

    return render_to_response(template, ctx, context_instance=RequestContext(request))

def detalleDeporte(request):
    template = "deportes/deporte_list.html"
    consulta = Deporte.objects.all()
    mensaje =''
   
    consulta, mensaje = buscador_deportes(request, consulta, mensaje)   

    ctx = {
        'deportes': consulta,
        'mensaje': mensaje,
    }

    return render_to_response(template, ctx, context_instance=RequestContext(request))

        



def modificar_deporte(request, pk):
    template = "deportes/deporte_modificar.html"
    d = Deporte.objects.get(id=pk)
    form_deporte = FormularioCrearDeporte()

    form_deporte.initial = {
        'nombre': d.nombre,
        'descripcion': d.descripcion,
        'genero': d.apto_para,
        
    }
    
    if request.method == 'POST'and 'bModificar' in request.POST:
        form_deporte = FormularioCrearDeporte(request.POST, request.FILES)
        if form_deporte.is_valid():
            nuevo_nombre = form_deporte.cleaned_data['nombre']
            nuevo_genero = form_deporte.cleaned_data['apto_para']
            nueva_descripcion = form_deporte.cleaned_data['descripcion']

            
            d.nombre = nuevo_nombre
            d.apto_para = nuevo_genero
            d.descripcion = nueva_descripcion
            d.save()
            return HttpResponseRedirect(reverse('listar-deporte'))
    ctx = {
        'form_deporte': form_deporte,
    }

    return render_to_response(template, ctx, context_instance=RequestContext(request))

def eliminar_deporte(request, pk):
    template = "deportes/deporte_confirm_delete.html"
    d = Deporte.objects.get(id= pk)
    if request.method == 'POST' and 'bEliminar' in request.POST:
        d.delete()
        return HttpResponseRedirect(reverse('listar-deporte'))

    ctx = {
        'deportes' : d,
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))


###################################### PARA TODOS ####################################################
def ver_deportes_personas(request):
    template = "ver_deportes_personas.html" 
    id_usuario = request.user.id
    darse_de_baja = True
    editar_info = False
    mensaje = ''
    g = ''
    
    try:

        g = Alumno.objects.get(legajo=int(request.session['user']))
        extiende = 'baseAlumno.html'
    except Exception as e:
        try:
            g = Profesor.objects.get(id=id_usuario)
            extiende = 'baseProfesor.html'
            darse_de_baja = False
            editar_info = True
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
        'extiende': extiende,
        'usuario': request.user.username,
        'darse_de_baja': darse_de_baja,
        'editar_info': editar_info,
        'deportes': g.lista_deporte.all(),
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))


def listar_deportes(request):
    template = "listar_deportes.html"
    id_usuario = obtener_id(request)
    extiende = extiende_de(id_usuario, request)
    ctx = {
        'deportes': Deporte.objects.all(), 
        'extiende':extiende,
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))


######################################## PARA ALUMNOS ##################################################

def inscripcion_deportes(request):
    template = "inscripcion_deportes.html"
    id_usuario = request.user.id
    consulta = Deporte.objects.all()
    mensaje =''
   
    consulta, mensaje = buscador_deportes(request, consulta, mensaje)   

    darse_de_baja = True
    try:
        g = Alumno.objects.get(legajo=int(request.session['user']))
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
        'deportes': consulta, 
        'deportes_alumno': g.lista_deporte.all(),
        'darse_de_baja': darse_de_baja,
        'mensaje': mensaje,
       
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))


def baja_deporte(request, pk):
    template = "baja_deporte.html"

    try:
        alumno = Alumno.objects.get(legajo=int(request.session['user']))
    except Exception as e:
        alumno = Persona.objects.get(id=request.user.id)

    if request.method == "POST":
        alumno.lista_deporte.remove(pk)
        url = 'ver_deportes_personas'
        return HttpResponseRedirect(reverse(url))   

    ctx = {
        'deporte': Deporte.objects.get(id=pk).nombre,
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))


def inscribir_deporte(request, pk):
    template = "inscribir_deporte.html"
    mensaje = ""

    if request.method == "POST":
        d = Deporte.objects.get(id=pk)
        
        try:
            alumno = Alumno.objects.get(legajo=int(request.session['user']))
            sexo = request.session['sexo']
        except Exception as e:
            alumno = Persona.objects.get(id=request.user.id)
            sexo = alumno.sexo

        if d.apto_para == sexo or d.apto_para == 3: 
            alumno.lista_deporte.add(d)
            url = 'ver_deportes_personas'
            return HttpResponseRedirect(reverse(url)) 
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

def editar_info_deporte(request, pk):
    template = "profesor/editar_info_deporte.html"
    deporte = Deporte.objects.get(id=pk)
    mensaje = 'naraja'

    formulario_deporte = FormularioEditarDeporteProfesor()
    formulario_deporte.initial = {
        'descripcion' : deporte.descripcion
    }

    if request.method == 'POST' and 'boton_guardar' in request.POST:
        mensaje = 'post'
        formulario_deporte = FormularioEditarDeporteProfesor(request.POST, request.FILES)
        if formulario_deporte.is_valid():
            mensaje = 'form is valid'
            if request.FILES:
                mensaje = 'quiere cambiar foto'
                if not deporte.foto == "usuarios/deportes/fotos_deportes/none/deporte_default.png":
                    deporte.foto.delete(False)

                deporte.foto = formulario_deporte.cleaned_data['foto']
            else:
                mensaje = ''

                
            deporte.descripcion = formulario_deporte.cleaned_data['descripcion']
            deporte.save() 
            url = 'ver_deportes_personas'
            return HttpResponseRedirect(reverse(url)) 
    else:
        if request.method == 'POST' and 'boton_eliminar' in request.POST:
            id_eliminar = request.POST.get('boton_eliminar_id')
            deporte.entrenamientos.remove(id_eliminar)
            deporte.save()
            e = Entrenamiento.objects.get(id=id_eliminar)
            e.delete()



    ctx = {
        'deporte': deporte,
        'form_deporte': formulario_deporte,
        'entrenamientos': deporte.entrenamientos.all(),
        'mensaje' : mensaje,
    }

    return render_to_response(template, ctx, context_instance=RequestContext(request))

def editar_entrenamiento_deporte(request, pk):

    template = "profesor/editar_entrenamiento_deporte.html"
    mensaje = ''
    formulario_entrenamiento = FormularioCrearEntrenamiento()
    deporte = Deporte.objects.get(id=pk)

    if request.method == 'POST' and 'boton_guardar' in request.POST:
        formulario_entrenamiento = FormularioCrearEntrenamiento(request.POST)
        if formulario_entrenamiento.is_valid():
            e = Entrenamiento()
            e.dia = formulario_entrenamiento.cleaned_data['dia']
            e.horario_inicio = formulario_entrenamiento.cleaned_data['horario_inicio']
            e.horario_fin = formulario_entrenamiento.cleaned_data['horario_fin']
            e.save()
            deporte.entrenamientos.add(e)
            deporte.save()
            mensaje = 'se guardo'

            url = reverse('editar_info_deporte', kwargs={'pk': pk})
            return HttpResponseRedirect(url)
    
    ctx = {
        'form_entrenamiento': formulario_entrenamiento,
        'mensaje': mensaje,
    }

    return render_to_response(template, ctx, context_instance=RequestContext(request))

##################### ADMIN ABM  deportes ##########################################

def admin_baja_deporte(request):
    templete= "AdministracionDeportes/admin_baja_deporte.html"
    
    ctx = {
        
        
    }
    return render_to_response(templete, ctx, context_instance=RequestContext(request))


    


