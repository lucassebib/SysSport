from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loguear, logout
from forms import FormularioAutenticacion
from usuarios.models import Alumno, Persona, Profesor, UsuarioInvitado 
from deportes.models import Deporte
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect

def vista_pagina_inicio(request):
	form = FormularioAutenticacion()
	template = "inicio.html"
	
	if request.method == "POST":
		form = FormularioAutenticacion(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			password = form.cleaned_data['password']
			
			user = authenticate(username=usuario, password=password)
 			try:
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
					else:
						ctx = {"form":form, "mensaje": "Usuario Inactivo"}
						return render_to_response("inicio.html",ctx, context_instance=RequestContext(request))
				else:
					ctx = {"form":form, "mensaje": "Nombre de usuario o password incorrectos"}
					return render_to_response("inicio.html",ctx, context_instance=RequestContext(request))
			except Exception as e:
				if user.is_staff:
					return HttpResponseRedirect('/admin')
					#ctx = {"form":form, "mensaje": "Nada que ver entres por aca wacho"}
					#return render_to_response("inicio.html",ctx, context_instance=RequestContext(request))

	ctx = {"form":form, "mensaje":""}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def app_logout(request):
	logout(request)
	return HttpResponseRedirect('/inicio')

def vista_recuperar_clave(request):
	return render_to_response('recup_clave.html')

def vista_registrarse(request):
	return render_to_response('registro.html')