from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loguear, logout
from forms import FormularioAutenticacion, FormularioDireccion
from usuarios.models import Alumno, Persona, Profesor, UsuarioInvitado 
from deportes.models import Deporte
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.conf import settings
from django.db.models import Q
from itertools import chain


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
						try:							
							g = Alumno.objects.get(id=id_usuario)
							return HttpResponseRedirect('/inicial_alumnos')
						except Exception as e:
							try:
								g = Profesor.objects.get(id=id_usuario)
								return HttpResponseRedirect('/inicial_profesores')
							except Exception as e:
								g = UsuarioInvitado.objects.get(id=id_usuario)
								return HttpResponseRedirect('/inicial_alumnos')									
					else:
						ctx = {"form":form, "mensaje": "Usuario Inactivo"}
						return render_to_response(template,ctx, context_instance=RequestContext(request))
				else:
					ctx = {"form":form, "mensaje": "Nombre de usuario o password incorrectos"}
					return render_to_response(template,ctx, context_instance=RequestContext(request))
			except Exception as e:
				if user.is_staff:
					return HttpResponseRedirect('/inicial-admin')

	ctx = {"form":form, "mensaje":""}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def app_logout(request):
	logout(request)
	return HttpResponseRedirect('/inicio')

def vista_recuperar_clave(request):
	return render_to_response('recup_clave.html')

def vista_registrarse(request):
	return render_to_response('registro.html')

@login_required
def vista_inicial_admin(request):	
	template = "admin/inicial_admin.html"
	return render_to_response(template, context_instance=RequestContext(request))

###########################PARA ALUMNOS###########################################


@login_required
def modificarPerfilAlumno(request):
	template = "alumno/modificar_perfil_alumno.html"
	try:
		alumno = Alumno.objects.get(id=request.user.id)
		tipo_usuario = "alumno"
		ctx1 = {
			'legajo': alumno.legajo,
			'carrera': alumno.ver_nombre_carrera,
		} 	 
	except Exception as e:
		alumno = UsuarioInvitado.objects.get(id=request.user.id)
		tipo_usuario = "invitado"
		ctx1 = {
			'institucion': alumno.institucion,
		} 		
	 

	#if request.method=='POST' and 'btn-cambiar-pass' in request.POST:
	#	return HttpResponseRedirect('/cambiar-pass')
	#
	#if request.method=='POST' and 'btn-cambiar-telefono' in request.POST:
	#	return HttpResponseRedirect('/cambiar-telefono')

	#if request.method=='POST' and 'btn-cambiar-direccion' in request.POST:
	#	return HttpResponseRedirect('/cambiar-direccion')

	ctx = {
			'usuario':request.user.username,
			'nombre': request.user.first_name,
			'apellido': request.user.last_name,
			'dni': alumno.dni,
			'sexo': alumno.ver_sexo,
			'fecha_nacimiento': alumno.fecha_nacimiento,
			'telefono': alumno.telefono,
			'direccion': alumno.direccion,
			'is_alumno': "alumno"==tipo_usuario,
			'is_invitado': "invitado"==tipo_usuario,		
			}

	ctx.update(ctx1)

	return render_to_response(template, ctx, context_instance=RequestContext(request))

@login_required
def cambiar_contrasenia(request):
	template = "confirm_cambiopass.html"
	return render_to_response(template, context_instance=RequestContext(request))

@login_required
def cambiar_telefono(request):
	template = "cambiar_telefono.html"
	return render_to_response(template, context_instance=RequestContext(request))

@login_required
def cambiar_direccion(request):
	template = "cambiar_direccion.html"
	ctx = {
		'form': FormularioDireccion
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def ver_contacto_urgencia(request):
	template = "alumno/ver_contacto_urgencia.html"
	contactos = ''

	try:
		contactos = Alumno.objects.get(id=request.user.id).contactos_de_urgencia.all()
	except Exception as e:
		contactos = UsuarioInvitado.objects.get(id=request.user.id).contactos_de_urgencia.all()


	ctx = {
		'contactos': contactos,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def ver_datos_medicos(request):
	template = "alumno/ver_datos_medicos.html"
	ctx = {}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

###########################PARA PROFESOR###########################################
@login_required
def ver_deportes_profesor(request):
	profesor = Profesor.objects.get(id=request.user.id)	 
	template = "profesor/ver_deportes.html"
	ctx = {
		'deportes': profesor.lista_deporte.all(),
		'otrosDeportes': Deporte.objects.filter(~Q(id__in=profesor.lista_deporte.all())) 
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

@login_required
def listar_alumnos_deporte(request, pk):
	template = "profesor/listar-alumno-deporte.html"
	alumnos = chain(Alumno.objects.filter(lista_deporte__in=pk ), UsuarioInvitado.objects.filter(lista_deporte__in=pk ))  
	ctx = {
		'alumnos': alumnos,
		'nombre': Deporte.objects.get(id=pk).nombre,
	}
	
	return render_to_response(template,ctx, context_instance=RequestContext(request))

def ver_usuarios(request):
	template='admin/ver_usuarios.html'
	ctx = {
		'usuarios': Persona.objects.all(),
	}
	return render_to_response(template,ctx, context_instance=RequestContext(request))

def ver_informacion_alumno(request, pk):
	template = "profesor/ver_informacion_alumno.html"
	try:
		alumno = Alumno.objects.get(id=pk)
		tipo_usuario = 'alumno'
	except Exception as e:
		alumno = UsuarioInvitado.objects.get(id=pk)
		tipo_usuario = 'invitado'

	ctx = {
		'alumno': alumno,
		'contactos': Alumno.objects.get(id=pk).contactos_de_urgencia.all(),
		'alumnoUTN': tipo_usuario=='alumno',
		'alumnoInvitado': tipo_usuario=='invitado',
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))
#############################################################################################################################

