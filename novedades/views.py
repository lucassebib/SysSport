from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loguear, logout
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from novedades.models import Novedades
from usuarios.models import Alumno, Profesor, UsuarioInvitado
from deportes.models import Deporte
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

@login_required	
def vista_index_alumnos(request):
	template = "inicial_alumnos.html"	
	id_usuario = request.user.id
	alumno = Alumno.objects.get(id=id_usuario)	
	posts = Novedades.objects.filter(visibilidad__in=[1,2]) | Novedades.objects.filter(visibilidad__in=[3], categoria__in=alumno.obtener_deportes())
	ctx = {
		"posts": posts.order_by('-fecha_publicacion'),
	}
	return render_to_response(template, ctx , context_instance=RequestContext(request))

def vista_index_profesores(request):
	template = "inicial_profesores.html"	
	id_usuario = request.user.id	
	posts = Novedades.objects.filter(autor__id=id_usuario)
	ctx = {
		"posts": posts.order_by('-fecha_publicacion'),
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def vista_index_invitados(request):
	template = "inicial_invitados.html"	
	id_usuario = request.user.id
	invitado = UsuarioInvitado.objects.get(id=id_usuario)	
	posts = Novedades.objects.filter(visibilidad__in=[1,2]) | Novedades.objects.filter(visibilidad__in=[3], categoria__in=invitado.obtener_deportes())
	ctx = {
		"posts": posts.order_by('-fecha_publicacion'),
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

#@login_required	esto debe ir en cada definicion 

class ListarNovedades(ListView):
    model = Novedades
    context_object_name = 'novedades'

class DetallesNovedades(DetailView):
    model = Novedades
    
class CrearNovedades(CreateView):	 
	model = Novedades	
	context_object_name = 'novedades'  
	fields = ['titulo','contenido', 'imagen','visibilidad','categoria',]

	def form_valid(self, form):
		a = form.save(commit = False)
		profe = Profesor.objects.get(id = self.request.user.id)
		a.autor = profe
		return super(CrearNovedades, self).form_valid(form)
    
    #novedades.autor_id= 
	
class ActualizarNovedades(UpdateView):
    model = Novedades
    

class EliminarNovedades(DeleteView):
    model = Novedades
    context_object_name = 'novedades'
    success_url = reverse_lazy('listar-novedades')

def ver_novedades_visibilidadTodos(request):
	template = "novedades_visibilidad_todos.html"
	ctx = {
		'posts': Novedades.objects.filter(visibilidad__in=[1]).order_by('-fecha_publicacion'), 
	}
	return render_to_response(template, ctx)





