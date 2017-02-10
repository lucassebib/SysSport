from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loguear, logout
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from novedades.models import Novedades, Comentario
from usuarios.models import Alumno, Profesor, UsuarioInvitado, Persona
from deportes.models import Deporte
from django.db.models import Q
from django.template import Context
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from forms import FormularioComentario
@login_required	
def vista_index_alumnos(request):
	template = "inicial_alumnos.html"	
	return render_to_response(template, context_instance=RequestContext(request))
	
@login_required	
def vista_index_profesores(request):
	template = "inicial_profesores.html"	
	return render_to_response(template, context_instance=RequestContext(request))
@login_required	
def vista_index_noLogueado(request):
	template = "usuario_noLogueado.html"	
	return render_to_response(template, context_instance=RequestContext(request))

##################### Novedades de usuarios#############################################
#Novedades de alumnos
@login_required	
def novedades_alumnos(request):
	template = "novedades_alumnos.html"	
	id_usuario = request.user.id
	alumno = Alumno.objects.get(id=id_usuario)	
	posts = Novedades.objects.filter(visibilidad__in=[1,2]) | Novedades.objects.filter(visibilidad__in=[3], categoria__in=alumno.obtener_deportes())
	ctx = {
		"posts": posts.order_by('-fecha_publicacion'),
	}
	return render_to_response(template, ctx , context_instance=RequestContext(request))

#Novedades de Profesores

#@login_required	
class ListarNovedades(ListView):
    model = Novedades
    context_object_name = 'novedades'

    def get_queryset(self):
        queryset = super(ListarNovedades, self).get_queryset()
        return queryset.filter(autor=self.request.user.id)

class DetallesNovedades(DetailView):
    model = Novedades
    
class CrearNovedades(CreateView):	 
	model = Novedades	
	context_object_name = 'novedades'  
	fields = ['titulo', 'contenido', 'imagen','visibilidad', 'categoria']

	def form_valid(self, form):
		a = form.save(commit = False)
		a.autor = Profesor.objects.get(id = self.request.user.id)
		return super(CrearNovedades, self).form_valid(form)

class ActualizarNovedades(UpdateView):
    model = Novedades
    
class EliminarNovedades(DeleteView):
    model = Novedades
    context_object_name = 'novedades'
    success_url = reverse_lazy('listar-novedades')

@login_required	
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
	if request.method == "POST":
		form = FormularioComentario(request.POST)
		if form.is_valid():
			texto = form.cleaned_data['texto']
			autor = Persona.objects.get(id=request.user.id)
			comentario = Comentario(texto=texto, autor=autor)
			comentario.save()
			novedad = Novedades.objects.get(id=pk)
			novedad.lista_comentarios.add(comentario)
			novedad.save()
			return HttpResponseRedirect('/novedades_alumnos') 

	 
	#url_fotoPerfil = (settings.BASE_DIR + settings.MEDIA_ROOT).replace('\\','/') + Alumno.objects.get(id=pk).foto_perfil.name
	ctx = {
		'novedad': Novedades.objects.get(id=pk),
		'formulario':form,
		'comentarios':Novedades.objects.get(id=pk).lista_comentarios.all(),
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))





