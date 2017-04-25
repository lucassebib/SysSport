import datetime
from datetime import datetime, date, time, timedelta

from django.contrib.auth import authenticate, login as loguear, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.template import Context
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from deportes.models import Deporte
from novedades.models import Novedades, Comentario, Notificacion
from peticiones.models import Peticionesservidor
from usuarios.models import Alumno, Profesor, UsuarioInvitado, Persona, perfil_admin
from usuarios.funciones import *
from novedades.funciones import *

from forms import FormularioComentario, FormularioNovedades, FormularioNovedadesAdmin
from paginacion import Paginate



def vista_index_alumnos(request):

	template = "inicial_alumnos.html"

	return render_to_response(template, context_instance=RequestContext(request))

@login_required	
def vista_index_profesores(request):
	template = "inicial_profesores.html"	
	return render_to_response(template, context_instance=RequestContext(request))

##################################CRUD NOVEDADES########################################	

class ListarNovedades(ListView):
    model = Novedades
    context_object_name = 'novedades'

    def get_queryset(self):
    	queryset = super(ListarNovedades, self).get_queryset()
        #queryset, mensaje = buscador_novedades_por_titulo(request, queryset, mensaje)

    	return queryset.filter(autor=self.request.user.id).order_by('-fecha_publicacion')

class DetallesNovedades(DetailView):
    model = Novedades
    
class CrearNovedades(CreateView):	 
	template_name = 'novedades/novedades_form.html'
	context_object_name = 'novedades'  	
	form_class = FormularioNovedades

	def get_form_kwargs(self):
	        kwargs = super(CrearNovedades, self ).get_form_kwargs()
	        kwargs['user'] = self.request.user
	        return kwargs

	def form_valid(self, form):	
		a = form.save(commit = False)
		#a.autor = Profesor.objects.get(id = self.request.user.id)
		a.autor = self.request.user
		return super(CrearNovedades, self).form_valid(form)

class ActualizarNovedades(UpdateView):
    model = Novedades
    form_class = FormularioNovedades

    def get_form_kwargs(self):
    	kwargs = super(ActualizarNovedades, self ).get_form_kwargs()
    	kwargs['user'] = self.request.user
    	return kwargs

	def form_valid(self, form):	
		a = form.save(commit = False)
		#a.autor = Profesor.objects.get(id = self.request.user.id)
		a.autor = self.request.user
		return super(CrearNovedades, self).form_valid(form)
  
class EliminarNovedades(DeleteView):
    model = Novedades
    context_object_name = 'novedades'
    success_url = reverse_lazy('listar-novedades')


################################## NOVEDADES PARA ADMINISTRADOR ########################################
def ver_novedades_admin(request):
	template = "admin/ver_novedades_admin.html"
	consulta = Novedades.objects.all() 
	mensaje=''
	dia = ''
	mes = ''
	anio = ''

	consulta, mensaje = buscador_novedades(request, consulta, mensaje)

	ctx = {
		'novedades': consulta,
		'mensaje': mensaje,
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

def eliminar_novedad_admin(request, pk):

	template = "admin/eliminar_novedad_admin.html"
	novedad = Novedades.objects.get(id=pk)

	if request.method == 'POST' and 'boton_confirmar' in request.POST:
		novedad.delete()
		return HttpResponseRedirect(reverse('ver_novedades_admin'))
	
	ctx = {
		'novedad': novedad,
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

def editar_novedades_admin(request, pk):

	template = "admin/editar_novedad_admin.html"
	novedad = Novedades.objects.get(id=pk)
	

	form = FormularioNovedadesAdmin()
	form.initial = {
		'titulo' : novedad.titulo, 
		'contenido' : novedad.contenido,
		'fecha_publicacion' : novedad.fecha_publicacion,
		'imagen' : novedad.imagen,
		'visibilidad' : novedad.visibilidad,
		'categoria' : novedad.categoria.all(),
	}

	if request.method == "POST" and 'boton_guardar' in request.POST:
		form = FormularioNovedadesAdmin(request.POST, request.FILES)
		if form.is_valid():
			novedad.titulo = form.cleaned_data['titulo']
			novedad.contenido = form.cleaned_data['contenido']
			novedad.imagen = form.cleaned_data['imagen']
			novedad.visibilidad = form.cleaned_data['visibilidad']
			novedad.categoria = form.cleaned_data['categoria']
			novedad.save()
			return HttpResponseRedirect(reverse('ver_novedades_admin'))


	ctx = {
		'form': form,
		
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

def crear_novedad_admin(request):
	template = "admin/crear_novedad_admin.html"
	form = FormularioNovedadesAdmin()
	mensaje = request.user

	if request.method == "POST" and 'boton_confirmar' in request.POST:
		form = FormularioNovedadesAdmin(request.POST, request.FILES)
		if form.is_valid():
			titulo = form.cleaned_data['titulo']
			contenido = form.cleaned_data['contenido']
			autor = request.user
			imagen = form.cleaned_data['imagen']
			visibilidad = form.cleaned_data['visibilidad']
			categoria = form.cleaned_data['categoria']

			n = Novedades()
			n.titulo = titulo
			n.contenido = contenido
			n.autor = autor
			n.imagen = imagen
			n.visibilidad = visibilidad
			n.save()
			
			if categoria:
				for c in categoria:
					n.categoria.add(c.id)

			n.save()			
			return HttpResponseRedirect('/administrador/novedades')

	ctx = {
		'form': form,
		'mensaje': mensaje,
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

def ver_novedad_admin(request, pk):
	template = "admin/ver_novedad_admin.html"
	form = FormularioComentario()
	id_usuario = request.user.id
	novedad = Novedades.objects.get(id=pk)
	#edicion = False
	puede_editar_comentarios = True
	mensaje = ''
	extiende = 'baseAdmin.html'

	if request.method == "POST" and 'boton_agregar' in request.POST:
		form = FormularioComentario(request.POST)
		if form.is_valid():
			texto = form.cleaned_data['texto']
			autor = User.objects.get(id=request.user.id)
			comentario = Comentario(texto=texto, autor=autor.id, nombre_autor='Admin')
			comentario.save()
			novedad.lista_comentarios.add(comentario)
			novedad.save()
			#form = FormularioComentario() 

			if not autor.id == novedad.autor.id and not autor.is_staff:
				n = Notificacion()
				n.id_autor_comentario = autor.id
				n.autor_comentario = autor.obtenerNombreCompleto()
				n.notificar_a = novedad.autor
				n.novedad = novedad
				n.save()
			return HttpResponseRedirect('')
	
	if request.method == "POST" and 'boton_eliminar' in request.POST:
		mensaje = 'tendria que eliminar'
		id_comentario_eliminar = request.POST.get('boton_eliminar')
		novedad.lista_comentarios.remove(id_comentario_eliminar)
		novedad.save()
		comentario = Comentario.objects.get(id=id_comentario_eliminar)
		comentario.delete()
	 
	ctx = {
		'novedad': novedad,
		'formulario':form,
		'comentarios':novedad.lista_comentarios.all().order_by('-id'),
		'extiende': extiende,
		'puede_editar_comentarios': puede_editar_comentarios,
		'mensaje': mensaje,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))
########################################################################################################

###################################### NOVEDADES PARA TODOS ############################################	
	
def ver_novedades_visibilidadTodos(request):
	template = "novedades_visibilidad_todos.html"
	mensaje = ''
	id_usuario = obtener_id(request)

	extiende = extiende_de(id_usuario, request)
	posts = Novedades.objects.filter(visibilidad__in=[1]).order_by('-fecha_publicacion')
	posts, mensaje = buscador_novedades(request, posts, mensaje)
	
	ctx = {
		'posts': posts, 
		'extiende': extiende,
		'mensaje': mensaje,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def ver_novedades(request, pk):
	template = "ver_novedad.html"
	form = FormularioComentario()
	id_usuario = request.user.id
	novedad = Novedades.objects.get(id=pk)
	puede_editar_comentarios = False
	mensaje = ''
	
	try:
		g = Alumno.objects.get(legajo=int(request.session['user']))
		extiende = 'baseAlumno.html'
	except Exception as e:
		try:
			g = Profesor.objects.get(id=id_usuario)
			extiende = 'baseProfesor.html'
			if novedad.autor.id == id_usuario:
				puede_editar_comentarios = True
		except Exception as e:
			try:
				g = UsuarioInvitado.objects.get(id=id_usuario)
				extiende = 'baseAlumno.html'
			except Exception as e:
				if request.user.is_staff:
					extiende = 'baseAdmin.html'

	if request.method == "POST" and 'boton_agregar' in request.POST:
		form = FormularioComentario(request.POST)
		if form.is_valid():
			texto = form.cleaned_data['texto']
			autor = g.id
			try:
				nombre_completo = request.session['nombre'] + ' ' + request.session['apellido'] 
			except Exception as e:
				nombre_completo = Persona.objects.get(id=request.user.id).obtenerNombreCompleto() 
			
			comentario = Comentario(texto=texto, autor=autor, nombre_autor=nombre_completo)
			comentario.save()
			novedad.lista_comentarios.add(comentario)
			novedad.save()
			#form = FormularioComentario() 

			if not autor == novedad.autor.id and not novedad.autor.is_staff:
				n = Notificacion()
				n.id_autor_comentario = autor
				try:
					nombre_completo = request.session['nombre'] + ' ' + request.session['apellido'] 
				except Exception as e:
					nombre_completo = Persona.objects.get(id=request.user.id).obtenerNombreCompleto
				n.autor_comentario = nombre_completo
				n.notificar_a = novedad.autor
				n.novedad = novedad
				n.save()
			return HttpResponseRedirect('')
	
	if request.method == "POST" and 'boton_eliminar' in request.POST:
		mensaje = 'tendria que eliminar'
		id_comentario_eliminar = request.POST.get('boton_eliminar')
		novedad.lista_comentarios.remove(id_comentario_eliminar)
		novedad.save()
		comentario = Comentario.objects.get(id=id_comentario_eliminar)
		comentario.delete()

	#if request.method == "POST" and 'boton_editar' in request.POST:
		#mensaje='apretaste boton editar'
		#edicion = True
	
	a = perfil_admin

	#string() 
	ctx = {
		'novedad': novedad,
		'formulario':form,
		'comentarios':novedad.lista_comentarios.all().order_by('-id'),
		'extiende': extiende,
		'puede_editar_comentarios': puede_editar_comentarios,
		'mensaje': mensaje,
		'usuario': g,
		'foto_admin': a,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

################################## NOVEDADES DE PROFESORES #############################################
def novedades_profesores(request):
	template = "novedades_profesores.html"
	mensaje =''
	posts = Novedades.objects.filter(autor=request.user.id) | Novedades.objects.filter(visibilidad__in=[1,2])
	posts.order_by('fecha_publicacion')
	posts, mensaje = buscador_novedades(request, posts, mensaje)
	pag = Paginate(request, posts, 3)
	ctx = {
		'posts': pag['queryset'],
		'paginator': pag,
     	'mensaje': mensaje,
	}
	return render_to_response(template, ctx , context_instance=RequestContext(request))

################################## NOVEDADES DE ALUMNOS #############################################

def novedades_alumnos(request):
	template = "novedades_alumnos.html"	
	mensaje =''
	try:
		alumno = Persona.objects.get(id=request.user.id)
	except Exception as e:
		alumno = Alumno.objects.get(legajo=int(request.session['user']))

	posts = Novedades.objects.filter(visibilidad__in=[1,2]) | Novedades.objects.filter(visibilidad__in=[3], categoria__in=alumno.obtener_deportes())
	posts.order_by('-fecha_publicacion')
	posts, mensaje = buscador_novedades(request, posts, mensaje)
	pag = Paginate(request, posts, 3)

	deportes = alumno.obtener_deportes()
	a = perfil_admin	
	
	ctx = {
		"posts": pag['queryset'],
		"deportes": deportes,
		#'totPost': init_posts,
     	'paginator': pag,
     	'mensaje': mensaje,
     	'foto_admin': a,
	}
	return render_to_response(template, ctx , context_instance=RequestContext(request))


def ver_novedad_filtrado(request, pk):
	template = "ver_novedad_filtrado.html"	
	mensaje = ''
	try:
		alumno = Persona.objects.get(id=request.user.id)
	except Exception as e:
		alumno = Alumno.objects.get(legajo=int(request.session['user']))
	
	posts = Novedades.objects.filter(categoria__in=pk)
	deportes = alumno.obtener_deportes()

	posts, mensaje = buscador_novedades(request, posts, mensaje)

	ctx = {

		'posts': posts.order_by('-fecha_publicacion'),
		'deportes': deportes,
		'mensaje': mensaje,
	}

	return render_to_response(template, ctx ,  context_instance=RequestContext(request))










