#-!-coding: utf-8 -!-
import hashlib, random
import time
from django.contrib import messages
from django.contrib.auth import authenticate, login as loguear, logout
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from datetime import datetime, date, time, timedelta
from django.shortcuts import render
from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context
from django.utils import timezone

from .forms import FormularioAutenticacion, FormularioRegistracion

from peticiones.funciones import *
from usuarios.models import Alumno, UsuarioInvitado, Profesor

def vista_pagina_inicio(request):
	form1 = FormularioAutenticacion()
	template = "inicio.html"
	url = ''

	if request.user.is_authenticated() or 'id_user' in request.session:
		try:
			g = Alumno.objects.get(legajo=int(request.session['user']))
			url = 'inicial_alumnos'
		except Exception as e:
			try:
				g = Profesor.objects.get(id=request.user.id)
				url = 'inicial_profesores'
			except Exception as e:
				try:
					g = UsuarioInvitado.objects.get(id=request.user.id)
					url = 'inicial_alumnos'
				except Exception as e:
					if request.user.is_superuser:
						url= 'inicial_admin'

		return HttpResponseRedirect(reverse(url))
									
	if request.method == "POST" and 'btn_ingresar' in request.POST:
		form1 = FormularioAutenticacion(request.POST)
		if form1.is_valid():
			usuario = form1.cleaned_data['username']
			password = form1.cleaned_data['password']	
			try:					
				#--Intento iniciar sesion de Alumno UTN
				alumno_utn_bd = Alumno.objects.get(legajo=int(usuario))	

				#--Resultado de la autenticacion del Sysacad	
				#alumno_utn = autenticacion(usuario, password)
				alumno_utn = True

				if alumno_utn_bd and alumno_utn and alumno_utn_bd.is_active:
					#--Se inicia sesion de un alumno UTN
					#datos = obtener_datos_iniciales(usuario, password)	
					datos = {'nombre': 'Tahiel', 'apellido': 'Bastiani', 'carrera': 5}				
					request.session["user"] = usuario
					request.session['id_user']= alumno_utn_bd.id
					request.session["nombre"] = datos['nombre']
					request.session["apellido"] = datos['apellido']
					request.session["carrera"] = int(datos['carrera'])
					request.session["correo"] = 'elduendeloco@hotmail.com'

					# Tener en cuenta que: (1,"Masculino"),(2,"Femenino")
					request.session["sexo"] = 1
					
					request.session["fecha_nacimiento"] = 'DD/MM/AAAA'
					request.session["telefono"] = '37042171212'
					request.session["direccion"] = 'Lestani 123'
					url = 'inicial_alumnos'
					return HttpResponseRedirect(reverse(url))
	
			except Exception as e:
				#Inicia Sesion Alumno invitado, profesor o administrador
				user = authenticate(username=usuario, password=password)
	 			try:
					if user is not None:
						if user.is_active:
							loguear(request, user)
							id_usuario = request.user.id

							try:
								g = Profesor.objects.get(id=id_usuario)
								url = 'inicial_profesores'							
							except Exception as e:
								g = UsuarioInvitado.objects.get(id=id_usuario)
								url = 'inicial_alumnos'
							return HttpResponseRedirect(reverse(url))									
						else:
							ctx = {"form1":form1, "mensaje": "Usuario Inactivo"}
							return render_to_response(template,ctx, context_instance=RequestContext(request))
					else:
						ctx = {"form1":form1, "mensaje": "Usuario o contraseña incorrectos"}
						return render_to_response(template,ctx, context_instance=RequestContext(request))
						#mensaje = "Usuario o contraseña incorrectos"
				except Exception as e:
					if user.is_staff:
						url = 'inicial_admin'
						return HttpResponseRedirect(reverse(url))
		
	ctx = {"form1":form1, "mensaje":""}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def app_logout(request):
	logout(request)
	return HttpResponseRedirect('/inicio')

def vista_registrarse(request):
	template = 'registro.html'
	form = FormularioRegistracion(request.POST or None)
	mensaje_error = ''
	error_mail = False

	if request.method == 'POST' and 'boton_enviar' in request.POST:
		#form = FormularioRegistracion(request.POST)		
		legajo = request.POST.get('legajo')
		password = request.POST.get('password')
		lista_deporte = request.POST.get('lista_deporte')

		#Verifico si no existe registrados alumnos con el legajo ingresado
		alumnos_registrados = Alumno.objects.filter(legajo=int(legajo))

		if not alumnos_registrados:
			#validar datos
			datos_validos = True

			#validacion con el sysacad
			validacion = True
			#validacion = establecer_conexion(int(legajo), password)

			#datos sysacad
			email = 'el_lucas992@hotmail.com'
			dni = 366366636
			nombre = 'Lucas'

			if validacion and datos_validos:
				#Enviar mail de confirmacion
				salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
				activation_key = hashlib.sha1(salt+email).hexdigest()
				key_expires = datetime.today() + timedelta(2)
				asunto = 'Confirmacion de cuenta en SysSport'
				direccion_servidor = 'http://127.0.0.1:8000/cuenta/confirmar'
				cuerpo = "Hola %s, Gracias por registrarte. Para activar tu cuenta da click en este link en menos de 48 horas: %s/%s" % (nombre, direccion_servidor, activation_key)
				
				try:
					send_mail(
						asunto, 
						cuerpo, 
						'ver_cuenta@example.com', 
						[email], 
						fail_silently=False
					)
					a = Alumno(legajo=legajo, dni=dni)
					a.save()
					a.lista_deporte.add(lista_deporte)
					a.save()
					a.activation_key = activation_key
					a.key_expires = key_expires
					a.save()
					url = 'vista_registracion_exitosa'
					return HttpResponseRedirect(reverse(url))
				except Exception as e:
					messages.error(request, 'Ha ocurrido un Problema, intente nuevamente...')							
		else:
				messages.error(request, 'Ya existe un usuario con el legajo ingresado.')
	
	ctx = {
		'form': form,
		'mensaje_error': mensaje_error,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

