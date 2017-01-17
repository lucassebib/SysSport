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
	return render_to_response(template,ctx , context_instance=RequestContext(request))

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
	
#def ingreso(request):
	#return render_to_response('ingreso.html')

#def base(request):
	#return render_to_response('base.html')
	
#def base2(request):
	#return render_to_response('base2.html')

#def login(request):
	#return render_to_response('login.html')



#def enviar(request):
	#return render_to_response('gracias.html')

#def formulario(request):
	#return render_to_response('registro.html')

class ListarNovedades(ListView):
    model = Novedades
    context_object_name = 'novedades'

class DetallesNovedades(DetailView):
    model = Novedades
    context_object_name = 'novedades'

class CrearNovedades(CreateView):
    model = Novedades
    

class ActualizarNovedades(UpdateView):
    model = Novedades
    

class EliminarNovedades(DeleteView):
    model = Novedades
    context_object_name = 'novedades'
    success_url = reverse_lazy('listar-novedades')





