from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loguear, logout
from forms import FormularioAutenticacion
from novedades.models import Novedades, Alumno, Persona, Profesor, UsuarioInvitado
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect


def principal(request):
	form = FormularioAutenticacion()
	
	if request.method == "POST":
		form = FormularioAutenticacion(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=usuario, password=password)
 
			if user is not None:
				if user.is_active:
					loguear(request, user)
					id_usuario = request.user.id
					gente = Persona.objects.get(id=id_usuario)
					try:
						g = Alumno.objects.get(id=id_usuario)
					except Exception as e:
						try:
							g = Profesor.objects.get(id=id_usuario)
						except Exception as e:
							g = UsuarioInvitado.objects.get(id=id_usuario)
	
					if g.tipo_usuario(cadena='alumno'):
						return HttpResponseRedirect('/inicial_alumnos')
					else:
						if g.tipo_usuario(cadena="profesor"):
							return HttpResponseRedirect('/inicial_profesores')
						else: 
							if g.tipo_usuario(cadena= "invitado"):
								return HttpResponseRedirect('/inicial_invitados')

					#return HttpResponseRedirect('/hola')
				else:
					ctx = {"form":form, "mensaje": "Usuario Inactivo"}
					return render_to_response("index_prueba.html",ctx, context_instance=RequestContext(request))
			else:
				ctx = {"form":form, "mensaje": "Nombre de usuario o password incorrectos"}
				return render_to_response("index_prueba.html",ctx, context_instance=RequestContext(request))
				
	
	
	ctx = {"form":form, "mensaje":""}
	return render_to_response("inicio.html",ctx, context_instance=RequestContext(request))
	#return render_to_response('inicio.html')

def vista_index_alumnos(request):
	return render_to_response('inicial_alumnos.html')

def vista_index_profesores(request):
	return render_to_response('inicial_profesores.html')

def vista_index_invitados(request):
	return render_to_response('inicial_invitados.html')

	
def ingreso(request):
	return render_to_response('ingreso.html')
def base(request):
	return render_to_response('base.html')
def base2(request):
	return render_to_response('base2.html')

def login(request):
	return render_to_response('login.html')

def clave(request):
	return render_to_response('recup_clave.html')

def enviar(request):
	return render_to_response('gracias.html')

def formulario(request):
	return render_to_response('registro.html')

def inicial_alumnos(request):
	posts = Novedades.todos_novedades_objects.all()
	#diccionario de datos
	return render_to_response('inicial_alumnos.html',{'posts':posts})

def error(request):
	return render_to_response('error.html')


@login_required
def app_home(request):
	template = "error.html"
	return render_to_response(template, context_instance=RequestContext(request))

def app_login(request):
	form = FormularioAutenticacion()
	
	if request.method == "POST":
		form = FormularioAutenticacion(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=usuario, password=password)
 
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/hola')
				else:
					ctx = {"form":form, "mensaje": "Usuario Inactivo"}
					return render_to_response("index_prueba.html",ctx, context_instance=RequestContext(request))
			else:
				ctx = {"form":form, "mensaje": "Nombre de usuario o password incorrectos"}
				return render_to_response("index_prueba.html",ctx, context_instance=RequestContext(request))
				
	
	
	ctx = {"form":form, "mensaje":""}
	return render_to_response("index_prueba.html",ctx, context_instance=RequestContext(request))

def app_logout(request):
	logout(request)
	return HttpResponseRedirect('/inicio')

