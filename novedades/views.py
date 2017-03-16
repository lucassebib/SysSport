from django.contrib.auth import authenticate, login as loguear, logout
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
from usuarios.models import Alumno, Profesor, UsuarioInvitado, Persona

from forms import FormularioComentario, FormularioNovedades, FormularioNovedadesAdmin
from paginacion import Paginate

@login_required	
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
    fields = ['titulo', 'contenido', 'imagen','visibilidad', 'categoria']
  
class EliminarNovedades(DeleteView):
    model = Novedades
    context_object_name = 'novedades'
    success_url = reverse_lazy('listar-novedades')

########################################################################################################

################################## NOVEDADES PARA ADMINISTRADOR ########################################
def ver_novedades_admin(request):
	template = "admin/ver_novedades_admin.html"
	url = ''
	if request.method == 'POST' and 'boton_visualizar' in request.POST:
 		id_novedad = request.POST.get('boton_visualizar_id')
 		url = reverse('visualizar_novedad_admin', kwargs={'pk': id_novedad})
 		#string(url)
        #return HttpResponseRedirect(url)
 	#else:
 		#mensaje = 'no'

	ctx = {
		'novedades': Novedades.objects.all()
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

def editar_novedades_admin(request, pk):

	template = "admin/editar_novedad_admin.html"
	novedad = Novedades.objects.get(id=pk)
	mensaje = 'ss'

	form = FormularioNovedadesAdmin()
	form.initial = {
		'titulo' : novedad.titulo, 
		'contenido' : novedad.contenido,
		'fecha_publicacion' : novedad.fecha_publicacion,
		#'autor' : novedad.autor,
		'imagen' : novedad.imagen,
		'visibilidad' : novedad.visibilidad,
		'categoria' : novedad.categoria,
	}

 	



	ctx = {
		'form': form,
		'mensaje': mensaje,
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

def crear_novedad_admin(request):
	template = "admin/crear_novedad_admin.html"
	form = FormularioNovedadesAdmin()
	mensaje = request.user

	if request.method == "POST" and 'boton_confirmar' in request.POST:
		form = FormularioNovedadesAdmin(request.POST)
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
			return HttpResponseRedirect('/admin/novedades')

	ctx = {
		'form': form,
		'mensaje': mensaje,
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))


########################################################################################################

###################################### NOVEDADES PARA TODOS ############################################	
	
def ver_novedades_visibilidadTodos(request):
	template = "novedades_visibilidad_todos.html"
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
					extiende = 'usuario_noLogueado.html'
				except Exception as e:
					if request.user.is_staff:
						extiende = 'baseAdmin.html'

	ctx = {
		'posts': Novedades.objects.filter(visibilidad__in=[1]).order_by('-fecha_publicacion'), 
		'extiende': extiende,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def ver_novedades(request, pk):
	template = "ver_novedad.html"
	form = FormularioComentario()
	id_usuario = request.user.id
	novedad = Novedades.objects.get(id=pk)
	#edicion = False
	puede_editar_comentarios = False
	mensaje = ''
	
	try:
		g = Alumno.objects.get(id=id_usuario)
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
				try:
					extiende = 'usuario_noLogueado.html'
				except Exception as e:
					if request.user.is_staff:
						extiende = 'baseAdmin.html'

	if request.method == "POST" and 'boton_agregar' in request.POST:
		form = FormularioComentario(request.POST)
		if form.is_valid():
			texto = form.cleaned_data['texto']
			autor = Persona.objects.get(id=request.user.id)
			comentario = Comentario(texto=texto, autor=autor)
			comentario.save()
			novedad.lista_comentarios.add(comentario)
			novedad.save()
			#form = FormularioComentario() 

			if not autor.id == novedad.autor.id and not novedad.autor.is_staff:
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

	#if request.method == "POST" and 'boton_editar' in request.POST:
		#mensaje='apretaste boton editar'
		#edicion = True
	 
	ctx = {
		'novedad': novedad,
		'formulario':form,
		'comentarios':novedad.lista_comentarios.all().order_by('-id'),
		'extiende': extiende,
		'puede_editar_comentarios': puede_editar_comentarios,
		'mensaje': mensaje
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

################################## NOVEDADES DE PROFESORES #############################################
def novedades_profesores(request):
	template = "novedades_profesores.html"
	posts = Novedades.objects.filter(autor=request.user.id) | Novedades.objects.filter(visibilidad__in=[1,2])
	posts.order_by('fecha_publicacion')
	pag = Paginate(request, posts, 4)
	ctx = {
		'posts': pag['queryset'],
     	'paginator': pag,
	}
	return render_to_response(template, ctx , context_instance=RequestContext(request))

################################## NOVEDADES DE ALUMNOS #############################################
@login_required	
def novedades_alumnos(request):
	template = "novedades_alumnos.html"	
	alumno = Persona.objects.get(id=request.user.id)
	deportes = alumno.obtener_deportes()	
	
	posts = Novedades.objects.filter(visibilidad__in=[1,2]) | Novedades.objects.filter(visibilidad__in=[3], categoria__in=alumno.obtener_deportes())
	posts.order_by('-fecha_publicacion')
	pag = Paginate(request, posts, 4)
	ctx = {
		"posts": pag['queryset'],
		"deportes": deportes,
		#'totPost': init_posts,
     	'paginator': pag,
	}
	return render_to_response(template, ctx , context_instance=RequestContext(request))

@login_required
def ver_novedad_filtrado(request, pk):
	template = "ver_novedad_filtrado.html"	
	alumno = Persona.objects.get(id=request.user.id)
	posts = Novedades.objects.filter(categoria__in=pk)
	deportes = alumno.obtener_deportes()	

	ctx = {
		"posts": posts.order_by('-fecha_publicacion'),
		"deportes": deportes,
	}

	return render_to_response(template, ctx , context_instance=RequestContext(request))










