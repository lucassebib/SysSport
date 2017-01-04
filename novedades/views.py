from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from forms import FormularioAutenticacion
from novedades.models import Novedades, Alumno
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect

def pagina_principal(request):
	return render_to_response('index.html')

def base(request):
	return render_to_response('base.html')

def login2(request):
	return render_to_response('login.html')

def enviar(request):
	return render_to_response('gracias.html')

def formulario2(request):
	return render_to_response('formulario2.html')

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
	return HttpResponseRedirect('/autenticar')

