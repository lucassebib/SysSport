import datetime
from datetime import date

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
from usuarios.models import Alumno, Profesor, UsuarioInvitado, Persona
from usuarios.funciones import *

from forms import FormularioComentario, FormularioNovedades, FormularioNovedadesAdmin
from paginacion import Paginate

def vista_index_alumnos(request):

	template = "inicial_alumnos.html"
	#p = Peticionesservidor.objects.using('sysacad').all()[1]
	#n = Novedades.objects.using('default22').all()
	#print(p)
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


################################## NOVEDADES PARA ADMINISTRADOR ########################################
def ver_novedades_admin(request):
	template = "admin/ver_novedades_admin.html"
	consulta = Novedades.objects.all() 
	mensaje=''
	dia = ''
	mes = ''
	anio = ''
	

	# BUSCADOR
	if request.method == 'POST' and 'btn_buscar' in request.POST:
		if request.POST.get('q', '')=='':
			mensaje = 'No ha introducido ningun termino en la busqueda'
			consulta= ''
		else:
			if not request.POST.get('opcion'):
				mensaje = 'No ha introducido ningun parametro de busqueda'
				consulta=''
			else:
				#     BUSQUEDA POR TITULO
				if request.POST.get('opcion') == 'titulo':
					titulo = request.POST.get('q')
					consulta = Novedades.objects.filter(titulo__contains=titulo)
					if not consulta:
						mensaje = 'No se han encontrado coincidencias'

				else:
					#   BUSQUEDA POR FECHA
					if request.POST.get('opcion')=='fecha':
						fecha = request.POST.get('q')
						seleccionados = request.POST.getlist("fecha")						

						#VALIDAR ENTRADA DE FECHA
						valido = False
						if 'dia' in seleccionados and 'mes' in seleccionados and 'anio' in seleccionados:
							#DD/MM/YYYY
							dia = fecha[:2]
							separador1 = fecha[2]
							mes = fecha[3:5]
							separador2 = fecha[5]
							anio = fecha[6:]
							cadena = dia+mes+anio
							if cadena.isdigit() and separador1==separador2 and (separador1=='/' or separador1=='-') and len(fecha) == 10:
								valido = True								
						else:
							if 'dia' in seleccionados and 'mes' in seleccionados and not 'anio' in seleccionados:
								#DD/MM
								dia = fecha[:2]
								separador1 = fecha[2]
								mes = fecha[3:5]
								cadena = dia + mes 
								if cadena.isdigit() and (separador1=='/' or separador1=='-') and len(fecha) == 5:
									valido = True

							else:
								if 'dia' in seleccionados and 'anio' in seleccionados and not 'mes' in seleccionados:
									#DD/YYYY
									dia = fecha[:2]
									separador1 = fecha[2]
									anio = fecha[3:8]
									cadena = dia+anio
									if cadena.isdigit() and (separador1=='/' or separador1=='-') and len(fecha) == 7:
										valido = True
								else:
									if 'mes' in seleccionados and 'anio' in seleccionados and not 'dia' in seleccionados:
										#MM/YYYY
										mes = fecha[:2]
										separador1 = fecha[2]
										anio = fecha[3:8]
										cadena = mes+anio
										if cadena.isdigit() and (separador1=='/' or separador1=='-') and len(fecha) == 7:
											valido = True
									else:
										if 'anio' in seleccionados and not 'dia' in seleccionados and not 'mes' in seleccionados:
											#YYYY
											anio = fecha[:4]
											if anio.isdigit() and len(anio) == 4:
												valido = True	
										else:
											if 'dia' in seleccionados and not 'anio' in seleccionados and not 'mes' in seleccionados:
												#DD
												dia = fecha[:2]
												if dia.isdigit() and len(dia) == 2:
													valido = True
											else:
												if mes and not anio and not dia:
													#MM
													mes = fecha[:2]
													if mes.isdigit() and len(mes) == 2:
														valido = True
													
						if valido:
							#ENTRADA CORRECTA
							#SE REALIZA LA BUSQUEDA POR FECHA
							if 'dia' in seleccionados and 'mes' in seleccionados and 'anio' in seleccionados:
								#DD/MM/YYYY
								dia = fecha[:2]
								mes = fecha[3:5]
								anio = fecha[6:]
								fecha2 = datetime.date(int(anio), int(mes), int(dia))
								consulta = Novedades.objects.filter(fecha_publicacion__contains=fecha2)
							else:
								if 'dia' in seleccionados and 'mes' in seleccionados and not 'anio' in seleccionados:
									#DD/MM
									dia = fecha[:2]
									mes = fecha[3:5]
									fecha2 = datetime.date(1, int(mes), int(dia))
									consulta = Novedades.objects.filter(fecha_publicacion__day = fecha2.day, fecha_publicacion__month = fecha2.month)
								else:
									if 'dia' in seleccionados and 'anio' in seleccionados and not 'mes' in seleccionados:
										#DD/YYYY
										dia = fecha[:2]
										anio = fecha[3:8]
										fecha2 = datetime.date(int(anio), 1, int(dia))
										consulta = Novedades.objects.filter(fecha_publicacion__day = fecha2.day, fecha_publicacion__year = fecha2.year)
									else:
										if 'mes' in seleccionados and 'anio' in seleccionados and not 'dia' in seleccionados:
											#MM/YYYY
											mes = fecha[:2]
											anio = fecha[3:8]
											fecha2 = datetime.date(int(anio), int(mes), 1)
											consulta = Novedades.objects.filter(fecha_publicacion__month = fecha2.month, fecha_publicacion__year = fecha2.year)
										else:
											if 'anio' in seleccionados and not 'dia' in seleccionados and not 'mes' in seleccionados:
												#YYYY
												anio = fecha[:4]
												fecha2 = datetime.date(int(anio), 1, 1)
												consulta = Novedades.objects.filter(fecha_publicacion__year = fecha2.year)
											else:
												if 'dia' in seleccionados and not 'anio' in seleccionados and not 'mes' in seleccionados:
													#DD
													dia = fecha[:2]
													fecha2 = datetime.date(1, 1, int(dia))
													consulta = Novedades.objects.filter(fecha_publicacion__day = fecha2.day)
												else:
													if mes and not anio and not dia:
														#MM
														mes = fecha[:2]
														fecha2 = datetime.date(1, int(mes), 1)
														consulta = Novedades.objects.filter(fecha_publicacion__month = fecha2.month)

								if not consulta:
									mensaje = 'No se han encontrado coincidencias'
						else:
							consulta = ''
							mensaje = 'Por favor, introduzca una fecha con el formato DD/MM/YYYY o DD-MM-YYYY, de acuerdo a su opcion de busqueda'
					
					else:
						# BUSQUEDA POR AUTOR
						if request.POST.get('opcion')=='autor':
							nombre_apellido = request.POST.get('q')
							if 'opcion_autor' in request.POST:
								if request.POST.get('opcion_autor')=='nombre':
									usuarios = User.objects.filter(first_name__contains=nombre_apellido)
								else:
									usuarios = User.objects.filter(last_name__contains=nombre_apellido)
							else:
								consulta = ''
								mensaje = 'No ha ingresado ningun parametro de busqueda para Autor'
							
							consulta = Novedades.objects.filter(autor__in = usuarios)
							if not consulta:
								consulta = ''
								mensaje = 'No se han encontrado coincidencias para: ' +  request.POST.get('q')

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
	mensaje = 'ss'

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
		'mensaje': mensaje,
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
	 
	ctx = {
		'novedad': novedad,
		'formulario':form,
		'comentarios':novedad.lista_comentarios.all().order_by('-id'),
		'extiende': extiende,
		'puede_editar_comentarios': puede_editar_comentarios,
		'mensaje': mensaje
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))
########################################################################################################

###################################### NOVEDADES PARA TODOS ############################################	
	
def ver_novedades_visibilidadTodos(request):
	template = "novedades_visibilidad_todos.html"
	
	id_usuario = obtener_id(request)

	extiende = extiende_de(id_usuario, request)
	
	
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
			comentario = Comentario(texto=texto, autor=autor)
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
	 
	ctx = {
		'novedad': novedad,
		'formulario':form,
		'comentarios':novedad.lista_comentarios.all().order_by('-id'),
		'extiende': extiende,
		'puede_editar_comentarios': puede_editar_comentarios,
		'mensaje': mensaje,
		'usuario': g,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

################################## NOVEDADES DE PROFESORES #############################################
def novedades_profesores(request):
	template = "novedades_profesores.html"
	posts = Novedades.objects.filter(autor=request.user.id) | Novedades.objects.filter(visibilidad__in=[1,2])
	posts.order_by('fecha_publicacion')
	pag = Paginate(request, posts, 3)
	ctx = {
		'posts': pag['queryset'],
     	'paginator': pag,
	}
	return render_to_response(template, ctx , context_instance=RequestContext(request))

################################## NOVEDADES DE ALUMNOS #############################################

def novedades_alumnos(request):
	template = "novedades_alumnos.html"	
	
	try:
		alumno = Persona.objects.get(id=request.user.id)
	except Exception as e:
		alumno = Alumno.objects.get(legajo=int(request.session['user']))
	
	
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


def ver_novedad_filtrado(request, pk):
	template = "ver_novedad_filtrado.html"	
	
	try:
		alumno = Persona.objects.get(id=request.user.id)
	except Exception as e:
		alumno = Alumno.objects.get(legajo=int(request.session['user']))
		
	
	posts = Novedades.objects.filter(categoria__in=pk)
	deportes = alumno.obtener_deportes()	

	ctx = {
		"posts": posts.order_by('-fecha_publicacion'),
		"deportes": deportes,
	}

	return render_to_response(template, ctx , context_instance=RequestContext(request))










