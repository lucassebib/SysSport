#-!-coding: utf-8 -!-
import hashlib, random
import time
from datetime import datetime, date, time, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loguear, logout

from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.template import Context
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from itertools import chain

from deportes.models import Deporte
from novedades.models import Notificacion
from peticiones.funciones import *
from usuarios.funciones import *
from usuarios.forms import *
from usuarios.models import Alumno, Persona, Profesor, UsuarioInvitado, Direccion, ContactoDeUrgencia, DatosMedicos, carreras_disponibles, MAX_CONTACTO_URGENCIA 


#################### AMB profeor Realizado Por el Admin ######################################
def alta_profesor(request):
	template = "admin/adminProfesores/alta_profe.html"
	form = FormularioAltaProfe()
	form_direccion = FormularioDireccion()
	mensaje = ''
	guardar = True
	mensaje_error = ''
	rechazo = False

	if request.method == "POST" and 'boton_alta' in request.POST:
		form = FormularioAltaProfe(request.POST, request.FILES)
		if form.is_valid():
			nombre = form.cleaned_data['first_name']
			apellido = form.cleaned_data['last_name']
			usuario = form.cleaned_data['username']
			contrasenia = form.cleaned_data['password']
			contrasenia2 = form.cleaned_data['password2']
			dni = form.cleaned_data['dni']
			fechaN = form.cleaned_data['fecha_nacimiento']
			sexo = form.cleaned_data['sexo']
			email = form.cleaned_data['email']
			telefono = form.cleaned_data['telefono']
			lista_deporte = form.cleaned_data['lista_deporte']
			
			p = Profesor()
			p.first_name = dar_formato(nombre)
			p.last_name = dar_formato(apellido)
			p.username = usuario
			p.dni = dni
			p.fecha_nacimiento = fechaN
			p.sexo = sexo
			p.email = email
			#p.password = contrasenia
			p.telefono = telefono
			#p.set_password(contrasenia)
			#p.save()
			
			form_direccion = FormularioDireccion(request.POST)

			calle = request.POST.get('calle')
			calle = dar_formato(calle)
			altura = request.POST.get('altura')
			if altura == '':
				altura = 0

			piso = request.POST.get('piso')
			if piso == '':
				piso = 0

			nro_departamento = request.POST.get('nro_departamento')
			if not nro_departamento:
				nro_departamento = ' '

			if not validar_nro_dpto(nro_departamento):
				guardar = False
				mensaje_error = 'Error: ingresar Nro de Departamento.'

			provincia = request.POST.get('provincia')
			provincia = dar_formato(provincia)
			
			localidad = request.POST.get('localidad')
			localidad = dar_formato(localidad)

			if guardar:
				direccion = Direccion(calle=calle, altura=altura, piso=piso, nro_departamento=nro_departamento, provincia=provincia, localidad=localidad)
				direccion.save()
				
			p.direccion = direccion

			## guarda profesor
			if contrasenia == contrasenia2:
				p.save()
				p.lista_deporte = lista_deporte
				p.set_password(contrasenia)
				rechazo = True
				p.save()
			else:
				messages.error(request, 'Passwords no coinciden.')

			
			if rechazo:
				return HttpResponseRedirect(reverse('listar_profes'))

	ctx = {
		'form': form,
		'form_direccion':form_direccion,
		'mensaje': mensaje,
		'rechazo': rechazo,
		'mensaje_error':mensaje_error,
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

def actualizar_profes(request, pk):
    template = "admin/adminProfesores/profes_modificar.html"
    p = Profesor.objects.get(id=pk)
    form = FormularioEditarProfesor()
    form_direccion = FormularioDireccion(request.POST or None, instance=direccion_instancia(p))
    mensaje =''
    direccion = Direccion()
    guardar = True
    rechazo = False


    form.initial = {
        'first_name': p.first_name,
        'last_name': p.last_name,
        'username': p.username,
        'dni':p.dni,
        'fecha_nacimiento':p.fecha_nacimiento,
        'sexo':p.sexo,
        'email':p.email,
        'telefono':p.telefono,
        'lista_deporte' : p.lista_deporte.all()    
    }
    
    if request.method == 'POST'and 'bModificar' in request.POST:
        form = FormularioEditarProfesor(request.POST, request.FILES)
        if form.is_valid():
            nuevo_nombre = form.cleaned_data['first_name']
            nuevo_apellido = form.cleaned_data['last_name']
            nueva_usuario = form.cleaned_data['username']
            nuevo_dni = form.cleaned_data['dni']
            nuevo_fechaN = form.cleaned_data['fecha_nacimiento']
            nuevo_sexo = form.cleaned_data['sexo']
            nuevo_email = form.cleaned_data['email']
            nuevo_telefono =form.cleaned_data['telefono']
            nuevo_deporte = form.cleaned_data['lista_deporte']

            nueva_contrasenia = form.cleaned_data['password']
            contrasenia2 = form.cleaned_data['password2']

            p.first_name = dar_formato(nuevo_nombre)
            p.last_name = dar_formato(nuevo_apellido)
            p.username = nueva_usuario
            p.dni = nuevo_dni
            p.fecha_nacimiento = nuevo_fechaN
            p.sexo = nuevo_sexo
            p.email = nuevo_email
            p.telefono = nuevo_telefono
            calle = request.POST.get('calle')
            calle = dar_formato(calle)
            altura = request.POST.get('altura')
            if altura == '':
            	altura = 0

            piso = request.POST.get('piso')
            if piso == '':
            	piso = 0
            nro_departamento = request.POST.get('nro_departamento')
            if not nro_departamento:
            	nro_departamento = ' '
            if not validar_nro_dpto(nro_departamento):
            	guardar = False
            	mensaje_error = 'Error: ingresar Nro de Departamento.'
            provincia = request.POST.get('provincia')
            provincia = dar_formato(provincia)
            localidad = request.POST.get('localidad')
            localidad = dar_formato(localidad)
            if guardar:
				direccion.calle =calle 
				direccion.altura=altura
				direccion.piso=piso
				direccion.nro_departamento=nro_departamento.upper()
				direccion.provincia=provincia
				direccion.localidad=localidad
				direccion.save()

				p.direccion = direccion

            if (nueva_contrasenia !='' or nueva_contrasenia is not None) and nueva_contrasenia ==contrasenia2:
            	p.save()
            	p.lista_deporte = nuevo_deporte
            	p.set_password(nueva_contrasenia)
            	rechazo = True
            	p.save()

            else:
            	messages.error(request, 'Passwords no coinciden.')

            if rechazo:
            	return HttpResponseRedirect(reverse('listar_profes'))
        else:
        	form = PostForm()

    ctx = {
        'form': form,
        'form_direccion':form_direccion,
        'mensaje':mensaje,
        'rechazo':rechazo,
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))

def direccion_instancia(persona_i):
	try:
		p = Direccion.objects.get(id=persona_i.direccion.id)
		
	except:
		d = Direccion()
		persona_i.direccion = d
		p = d

	return p
    
def listar_profes(request):
	template = "admin/adminProfesores/listar_profes.html"
	ctx = {
        'profes': Profesor.objects.all(),

    }
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def delete_profe(request, pk):
	template = "admin/adminProfesores/profe_confirm_delete.html"

	#string(pk)
	p = Profesor.objects.get(id= pk)

	
	if request.method == 'POST' and 'bEliminar' in request.POST:
		p.delete()
		url = 'listar_profes'
		return HttpResponseRedirect(reverse(url))

	ctx = {
		'profe': p,
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))


##################################  AMB ALUMNO Admin    #####################################################################
def alta_alumno(request):
	template = "admin/adminAlumnoInvitado/alta_alumno.html"
	form = FormularioAltaAlumnoInvitado()
	form_direccion = FormularioDireccion()
	guardar = True
	mensaje = ''
	mensaje_error = ''
	rechazo = False
	#u = User.objects.get()

	if request.method == "POST" and 'boton_alta' in request.POST:
		form = FormularioAltaAlumnoInvitado(request.POST , request.FILES)
		if form.is_valid():
			nombre = form.cleaned_data['first_name']
			apellido = form.cleaned_data['last_name']
			usuario = form.cleaned_data['username']
			contrasenia = form.cleaned_data['password']
			contrasenia2 = form.cleaned_data['password2']
			dni = form.cleaned_data['dni']
			fechaN = form.cleaned_data['fecha_nacimiento']
			sexo = form.cleaned_data['sexo']
			email = form.cleaned_data['email']
			telefono = form.cleaned_data['telefono']
			lista_deporte = form.cleaned_data['lista_deporte']

            
			a = UsuarioInvitado()

			a.first_name = nombre
			a.last_name = apellido
			a.username = usuario
			a.fecha_nacimiento =fechaN
			a.sexo = sexo
			a.email = email
			a.telefono = telefono

			form_direccion = FormularioDireccion(request.POST)

			calle = request.POST.get('calle')
			calle = dar_formato(calle)
			altura = request.POST.get('altura')
			if altura == '':
				altura = 0

			piso = request.POST.get('piso')
			if piso == '':
				piso = 0

			nro_departamento = request.POST.get('nro_departamento')
			if not nro_departamento:
				nro_departamento = ' '

			if not validar_nro_dpto(nro_departamento):
				guardar = False
				mensaje_error = 'Error: ingresar Nro de Departamento.'

			provincia = request.POST.get('provincia')
			provincia = dar_formato(provincia)
			
			localidad = request.POST.get('localidad')
			localidad = dar_formato(localidad)

			if guardar:
				direccion = Direccion(calle=calle, altura=altura, piso=piso, nro_departamento=nro_departamento, provincia=provincia, localidad=localidad)
				direccion.save()
			a.direccion = direccion				


			if contrasenia==contrasenia2:
				a.save()
				a.lista_deporte = lista_deporte
				a.set_password(contrasenia)
				rechazo = True
				a.save()
			else:
				messages.error(request, 'Passwords no coinciden.')

			if rechazo:
				return HttpResponseRedirect(reverse('listar_alumnos'))


	ctx = {
		'form': form,
		'from_direccion': form_direccion,
		'mensaje_error':mensaje_error,
		'mensaje': mensaje,
		'rechazo':rechazo,
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

def delete_alumno(request, pk):
	template = "admin/adminAlumnoInvitado/alumno_confirm_delete.html"

	#string(pk)
	a = UsuarioInvitado.objects.get(id= pk)

	
	if request.method == 'POST' and 'bEliminar' in request.POST:
		a.delete()
		url = 'listar_alumnos'
		return HttpResponseRedirect(reverse(url))

	ctx = {
		'alumno': a,

	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

def actualizar_alumnos(request, pk):
    template = "admin/adminAlumnoInvitado/alumno_modificar.html"
    a = UsuarioInvitado.objects.get(id=pk)
    form = FormularioEditarAlumnoInvitado()
    form_direccion = FormularioDireccion(request.POST or None, instance=direccion_instancia(a))
    mensaje = ''
    direccion = Direccion()
    rechazo = False
    guardar = True

    form.initial = {
        'first_name': a.first_name,
        'last_name': a.last_name,
        'username': a.username,
        'dni':a.dni,
        'fecha_nacimiento':a.fecha_nacimiento,
        'sexo':a.sexo,
        'email':a.email,
        'telefono':a.telefono,
        'lista_deporte' : a.lista_deporte.all()
        
    }
    
    if request.method == 'POST'and 'bModificar' in request.POST:
        form = FormularioEditarAlumnoInvitado(request.POST, request.FILES)
        if form.is_valid():
            nuevo_nombre = form.cleaned_data['first_name']
            nuevo_apellido = form.cleaned_data['last_name']
            nueva_usuario = form.cleaned_data['username']
            nueva_contrasenia = form.cleaned_data['password']
            contrasenia2 = form.cleaned_data['password2']
            nuevo_dni = form.cleaned_data['dni']
            nuevo_fechaN = form.cleaned_data['fecha_nacimiento']
            nuevo_sexo = form.cleaned_data['sexo']
            nuevo_email = form.cleaned_data['email']
            nuevo_telefono =form.cleaned_data['telefono']
            nuevo_deporte = form.cleaned_data['lista_deporte']
            
            a.first_name = nuevo_nombre
            a.last_name = nuevo_apellido
            a.username = nueva_usuario
            a.dni = nuevo_dni
            a.fecha_nacimiento = nuevo_fechaN
            a.sexo = nuevo_sexo
            a.foto = nuevo_foto
            a.email = nuevo_email
            a.telefono = nuevo_telefono
            calle = request.POST.get('calle')
            calle = dar_formato(calle)
            altura = request.POST.get('altura')
            if altura == '':
            	altura = 0

            piso = request.POST.get('piso')
            if piso == '':
            	piso = 0
            nro_departamento = request.POST.get('nro_departamento')
            if not nro_departamento:
            	nro_departamento = ' '
            if not validar_nro_dpto(nro_departamento):
            	guardar = False
            	mensaje_error = 'Error: ingresar Nro de Departamento.'
            provincia = request.POST.get('provincia')
            provincia = dar_formato(provincia)
            localidad = request.POST.get('localidad')
            localidad = dar_formato(localidad)
            if guardar:
				direccion.calle =calle 
				direccion.altura=altura
				direccion.piso=piso
				direccion.nro_departamento=nro_departamento.upper()
				direccion.provincia=provincia
				direccion.localidad=localidad
				direccion.save()

				a.direccion = direccion

    
            if (nueva_contrasenia !='' or nueva_contrasenia is not None) and nueva_contrasenia ==contrasenia2:
            	a.save()
            	a.lista_deporte = nuevo_deporte
            	a.set_password(nueva_contrasenia)
            	rechazo = True
            	a.save()

            else:
            	messages.error(request, 'Passwords no coinciden.')

            if rechazo:
            	return HttpResponseRedirect(reverse('listar_alumnos'))
        else:
        	form = PostForm()
           
    ctx = {
        'form': form,
        'form_direccion':form_direccion,
        'mensaje':mensaje,
        'rechazo': rechazo,

    }

    return render_to_response(template, ctx, context_instance=RequestContext(request))
    
def listar_alumnos(request):
	template = "admin/adminAlumnoInvitado/listar_alumno.html"
	ctx = {
        'alumnos': UsuarioInvitado.objects.all(),

    }
	return render_to_response(template, ctx, context_instance=RequestContext(request))
#######################################################################################################
def vista_pagina_inicio(request):
	form1 = FormularioAutenticacion()

#	if request.user.is_authenticated() or request.session:
#		id_usuario = request.user.id
#		try:
#			g = Alumno.objects.get(legajo=int(request.session['legajo']))
#			return HttpResponseRedirect('/inicial_alumnos')
#		except Exception as e:
#			try:
#				g = Profesor.objects.get(id=id_usuario)
#				return HttpResponseRedirect('/inicial_profesores')
#			except Exception as e:
#				g = UsuarioInvitado.objects.get(id=id_usuario)
#				return HttpResponseRedirect('/inicial_alumnos')	
#	else:
	template = "inicio.html"								
	if request.method == "POST":
		form1 = FormularioAutenticacion(request.POST)
		if form1.is_valid():
			usuario = form1.cleaned_data['username']
			password = form1.cleaned_data['password']	
			try:			
				#request.session.flush()
				#request.session.cycle_key()							
				
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
								return HttpResponseRedirect(reverse(url))
							except Exception as e:
								g = UsuarioInvitado.objects.get(id=id_usuario)
								url = 'inicial_alumnos'
								return HttpResponseRedirect(reverse(url))									
						else:
							ctx = {"form1":form1, "mensaje": "Usuario Inactivo"}
							return render_to_response(template,ctx, context_instance=RequestContext(request))
					else:
						ctx = {"form1":form1, "mensaje": "Nombre de usuario o password incorrectos"}
						return render_to_response(template,ctx, context_instance=RequestContext(request))
				except Exception as e:
					if user.is_staff:
						url = 'inicial_admin'
						return HttpResponseRedirect(reverse(url))

	ctx = {"form1":form1, "mensaje":""}
	return render_to_response(template, ctx, context_instance=RequestContext(request))


def app_logout(request):
	logout(request)
	return HttpResponseRedirect('/inicio')

def vista_recuperar_clave(request):
	return render_to_response('recup_clave.html')

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

			email = 'lorenarambados@gmail.com'
			dni = 366366636
			nombre = 'Lucas'

			#Creamos el alumno
			if validacion and datos_validos:
				#Enviar mail de confirmacion
				salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
				activation_key = hashlib.sha1(salt+email).hexdigest()
				key_expires = datetime.today() + timedelta(2)
				asunto = 'Confirmacion de cuenta en SysSport'
				direccion_servidor = 'http://127.0.0.1:8000/cuenta/confirmar'
				cuerpo = "Hola %s, Gracias por registrarte. Para activar tu cuenta da click en este link en menos de 48 horas: %s/%s" % (nombre, direccion_servidor, activation_key)
							
				print('esta por mandar')
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
		else:
				messages.error(request, 'Ya existe un usuario con el legajo ingresado.')
	
	ctx = {
		'form': form,
		'mensaje_error': mensaje_error,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def vista_confirmar_alta(request, activation_key):
	template = 'registracion/confirmar_alta.html'
	mensaje_error = ''
	direccion_servidor = ''

	# Verifica que el token de activacion sea valido
	a = Alumno.objects.get(activation_key=activation_key)
	
	if not a:
		mensaje_error = 'No ha sido posible activar la cuenta, intente nuevamente'
	else:
		# verifica si el token de activacion ha expirado y si es asi renderiza el html de registro expirado
		print(a.key_expires)
		print(timezone.now())
		if timezone.now() < a.key_expires:
			# Si el token no ha expirado, se activa el usuario y se muestra el html de confirmacion
			a.is_active = True
			a.save()
			mensaje_error = 'Cuentra creada con exito'
		else:
			mensaje_error = 'La autenticacion ha expirado'
			
	ctx = {
		'mensaje_error': mensaje_error,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def vista_registracion_exitosa(request):
	template = 'registracion/registracion_exitosa.html'
	ctx = {}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

@login_required
def vista_inicial_admin(request):	
	template = "admin/inicial_admin.html"
	return render_to_response(template, context_instance=RequestContext(request))


def ver_informacion_perfil_persona(request, pk):
	template = "ver_informacion_perfil_persona.html"
	
	id_usuario = obtener_id(request)
	
	tipo_usuario = "" 

	try:
		persona_visitada = Persona.objects.get(id=pk)
	except Exception as e:
		persona_visitada = Alumno.objects.get(id=pk)
		
	extiende = extiende_de(id_usuario, request)
	
	ctx1 = {}	
	try:
		g_visitado = Alumno.objects.get(id=pk)
		tipo_usuario_visitado = 'alumno'
		#OBTENER VALORES DEL SYSACAD
		carrera = 'obtener del sysacad'
		ctx1 = {
			'carrera': carrera,
		}
	except Exception as e:
		try:
			g_visitado = Profesor.objects.get(id=pk)
			tipo_usuario_visitado = 'profesor'
		except Exception as e:
			try:
				g_visitado = UsuarioInvitado.objects.get(id=pk)
				tipo_usuario_visitado = "invitado"				
				ctx1 = {
					'institucion': g_visitado.institucion,
				} 	
			except Exception as e:
				try:
					extiende = 'usuario_noLogueado.html'
				except Exception as e:
					if request.user.is_staff:
						extiende = 'baseAdmin.html'

	ctx = {
			'extiende': extiende,
			'persona': persona_visitada,
			'is_invitado': "invitado"==tipo_usuario_visitado,
			'is_alumno': "alumno"==tipo_usuario_visitado,
			'is_profesor': "profesor"==tipo_usuario_visitado,

			}
	ctx.update(ctx1)

	return render_to_response(template, ctx, context_instance=RequestContext(request))

def editar_error(request):
	template = "editar_error.html"
	extiende = ''
	id_usuario = request.user.id
	
	try:
		g = Alumno.objects.get(legajo=int(request.session['user']))
		extiende = 'baseAlumno.html'
	except Exception as e:
		try:
			g = Profesor.objects.get(id=id_usuario)
			extiende = 'baseProfesor.html'
		except Exception as e:
			g = UsuarioInvitado.objects.get(id=id_usuario)
			extiende = 'baseAlumno.html'

	ctx = {
		'extiende': extiende,
			}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

##########################################PARA ALUMNOS######################################################
def modificarPerfilAlumno(request):
	template = "alumno/modificar_perfil_alumno.html"
	form = FormularioCargarImagen()
	mensaje= ""
	extiende= "baseAlumno.html"

	if request.method == 'POST':
		form = FormularioCargarImagen(request.POST, request.FILES)
		if form.is_valid():
			if request.FILES:
				try:
					p = Persona.objects.get(id=request.user.id)
				except Exception as e:
					p = Alumno.objects.get(legajo=int(request.session['user']))
				

				if not p.foto_perfil == "usuarios/fotos_de_perfil/None/default_profile.jpg":
					p.foto_perfil.delete(False)
				
				p.foto_perfil = form.cleaned_data['foto_perfil']
				p.save()
				return HttpResponseRedirect('')
			else:
				mensaje='no ha seleccionado ninguna imagen'

	try:
		alumno = Alumno.objects.get(legajo=int(request.session['user']))
		tipo_usuario = "alumno"
		ctx1 = {
			'legajo': request.session['user'],
			'carrera': mostrar_carrera(request.session['carrera']),
			'email': request.session['correo'],
			'nombre': request.session['nombre'],
			'apellido': request.session['apellido'],
			'sexo': mostrar_sexo(request.session['sexo']),
			'fecha_nacimiento': request.session['fecha_nacimiento'],
			'telefono': request.session['telefono'],
			'direccion': request.session['direccion'],
		} 	 
	except Exception as e:
		alumno = UsuarioInvitado.objects.get(id=request.user.id)
		tipo_usuario = "invitado"

		ctx1 = {
			'institucion': alumno.institucion,
		
			'email': alumno.email,
			'nombre': request.user.first_name,
			'apellido': request.user.last_name,
			'sexo': alumno.ver_sexo,
			'fecha_nacimiento': alumno.fecha_nacimiento,
			'telefono': alumno.telefono,
			'direccion': alumno.direccion,
		} 

	ctx = {
			'form': form,
			'mensaje': mensaje,
			#'usuario':request.user.username,
			'alumno': alumno,
			'dni': alumno.dni,
			'is_alumno': "alumno"==tipo_usuario,
			'is_invitado': "invitado"==tipo_usuario,
			'extiende': extiende		
			}

	ctx.update(ctx1)

	return render_to_response(template, ctx, context_instance=RequestContext(request))

@login_required
def cambiar_contrasenia(request):
	template = "confirm_cambiopass.html"
	return render_to_response(template, context_instance=RequestContext(request))

def ver_tipo_usuario(request):
	template = "registracion/comprobar_usuario.html"
	
	if request.method=='POST':
		correo = request.POST.get('correo')
		dato = UsuarioInvitado.objects.filter(email= correo)
		if dato:
			url = reverse('password_reset')
			return HttpResponseRedirect(url)
		else:
			url = reverse('error_noInvitado')
			return HttpResponseRedirect(url)


	ctx = { 
		
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def error_noInvitado(request):
	template = "registracion/error_usuario_NoInvitado.html"
	return render_to_response(template, context_instance=RequestContext(request))

@login_required
def editar_perfil_alumno(request):
	#ESTA FUNCION ES SOLO PARA UN INVITADO, SOLAMENTE ESTE USUARIO PODRA CAMBIAR SU INFORMACION DE PERFIL
	template = "alumno/editar_perfil_alumno.html"
	invitado = UsuarioInvitado.objects.get(id=request.user.id)
	mensaje = 'inicio'
	id_usuario = obtener_id(request)
	extiende = extiende_de(id_usuario, request)

	form_principal = FormularioEdicionPerfilInvitado()
	form_principal.initial = {
		'first_name': invitado.first_name,
		'last_name': invitado.last_name,
		'email': invitado.email,
		'dni': invitado.dni,
		'fecha_nacimiento': invitado.fecha_nacimiento,
		'telefono': invitado.telefono,
	}

	form_direccion = FormularioDireccion()
	direccion = Direccion()
	tiene_direccion = False
	if invitado.direccion:
		tiene_direccion = True
		mensaje = 'tiene direccion'
		direccion = Direccion.objects.get(id=invitado.direccion.id)
		form_direccion.initial = {
			'calle': direccion.calle,
			'altura': direccion.altura,
			'piso': direccion.piso,
			'nro_departamento': direccion.nro_departamento,
			'provincia': direccion.provincia,
			'localidad': direccion.localidad,
		
		}
	else:
		mensaje = 'no tiene direccion'

	if request.method == "POST":
		mensaje = 'entro al if POST'
		form_principal = FormularioEdicionPerfilInvitado(request.POST)
		if form_principal.is_valid():
			mensaje = 'entro al POST ES VALIDO'
			nombre = form_principal.cleaned_data['first_name']
			apellido = form_principal.cleaned_data['last_name']
			email = form_principal.cleaned_data['email']
			dni = form_principal.cleaned_data['dni']
			fecha_nacimiento = form_principal.cleaned_data['fecha_nacimiento']
			telefono = form_principal.cleaned_data['telefono']

			form_direccion = FormularioDireccion(request.POST)
			calle = request.POST.get('calle')
			altura = request.POST.get('altura')
			if altura == '':
				altura = 0

			piso = request.POST.get('piso')
			if piso == '':
				piso = 0

			nro_departamento = request.POST.get('nro_departamento')
			if nro_departamento == '':
				nro_departamento = 0

			provincia = request.POST.get('provincia')
			localidad = request.POST.get('localidad')

			if not tiene_direccion:
				mensaje = 'aca tendria que crear una direccion'
				direccion = Direccion(calle=calle, altura=altura, piso=piso, nro_departamento=nro_departamento, provincia=provincia, localidad=localidad)
				direccion.save()
				invitado.direccion = direccion
			else:
				direccion.calle=calle 
				direccion.altura=altura
				direccion.piso=piso
				direccion.nro_departamento=nro_departamento
				direccion.provincia=provincia
				direccion.localidad=localidad
				direccion.save()
			
			invitado.first_name = nombre
			invitado.last_name = apellido
			invitado.email=email
			invitado.dni= dni
			invitado.fecha_nacimiento= fecha_nacimiento
			invitado.telefono = telefono
			
			invitado.save()	

			return HttpResponseRedirect('/alumno/modificar_perfil_alumno')

	ctx = {
		'mensaje': mensaje,
		'form_principal': form_principal,
		'form_direccion': form_direccion,
		'extiende': extiende,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

#-------#ABM CONTACTOS DE URGENCIA #---------#

def agregar_contactoUrgencia(request):
	template = "alumno/agregar_contacto_urgencia.html"
	form_principal = FormularioContactoDeUrgencia()
	form_direccion = FormularioDireccion()
	guardar = True
	mensaje_error = ''
	mostrar_mensaje = False

	if request.method == "POST":
		form_principal = FormularioContactoDeUrgencia(request.POST)
		if form_principal.is_valid():
			nombre = form_principal.cleaned_data['nombre']
			nombre = dar_formato(nombre)
			apellido = form_principal.cleaned_data['apellido']
			apellido = dar_formato(apellido)
			parentezco = form_principal.cleaned_data['parentezco']
			parentezco = dar_formato(parentezco)
			
			telefono = form_principal.cleaned_data['telefono']
			if not telefono.isdigit():
				guardar = False
				mensaje_error = 'Error: solo se permiten numeros en el Telefono'

			form_direccion = FormularioDireccion(request.POST)

			calle = request.POST.get('calle')
			calle = dar_formato(calle)
			altura = request.POST.get('altura')
			if altura == '':
				altura = 0

			piso = request.POST.get('piso')
			if piso == '':
				piso = 0

			nro_departamento = request.POST.get('nro_departamento')
			if not nro_departamento:
				nro_departamento = ' '

			if not validar_nro_dpto(nro_departamento):
				guardar = False
				mensaje_error = 'Error: ingresar Nro de Departamento.'

			provincia = request.POST.get('provincia')
			provincia = dar_formato(provincia)
			
			localidad = request.POST.get('localidad')
			localidad = dar_formato(localidad)

			#Se verifica que no se excedan la cantidad max de contactos
			try:
				alumno = Alumno.objects.get(legajo=int(request.session['user']))
			except Exception as e:
				alumno = UsuarioInvitado.objects.get(id=request.user.id)

			contactos = alumno.contactos_de_urgencia.all()
			contador = 0
			for c in contactos:
				contador = contador + 1

			if contador >=MAX_CONTACTO_URGENCIA:
				guardar = False

				mostrar_mensaje = True
				mensaje_error = 'Solo es posible agregar como maximo: ' + str(MAX_CONTACTO_URGENCIA) + ' contacto/s'

			if guardar:
				direccion = Direccion(calle=calle, altura=altura, piso=piso, nro_departamento=nro_departamento, provincia=provincia, localidad=localidad)
				direccion.save()
				
				contacto = ContactoDeUrgencia(nombre=nombre, apellido=apellido, parentezco=parentezco, telefono=telefono, direccion=direccion)
				contacto.save()

				
				
				alumno.contactos_de_urgencia.add(contacto)
				alumno.save()
				
				url = 'ver_contacto_urgencia'
				return HttpResponseRedirect(reverse(url))
		else:
			mensaje_error = 'Error: faltan datos obligatorios'
	ctx = {
		'form_principal': form_principal,
		'form_direccion': form_direccion,
		'mensaje_error': mensaje_error,
		'mostrar_mensaje': mostrar_mensaje,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def ver_contacto_urgencia(request):
	template = "alumno/ver_contacto_urgencia.html"
	contactos = ''

	try:
		contactos = Alumno.objects.get(legajo=request.session['user']).contactos_de_urgencia.all()
	except Exception as e:
		contactos = UsuarioInvitado.objects.get(id=request.user.id).contactos_de_urgencia.all()

	ctx = {
    	'contactos': contactos,

	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def eliminar_contactoUrgencia(request, pk):
	template = "alumno/eliminar_contactoUrgencia.html"
	alumno = ''
	contacto = ContactoDeUrgencia.objects.get(id=pk)

	try:
		alumno = Alumno.objects.get(legajo=request.session['user'])
	except Exception as e:
		alumno = UsuarioInvitado.objects.get(id=request.user.id)

	if request.method == "POST":
		alumno.contactos_de_urgencia.remove(pk)
		alumno.save()
		contacto.delete()
		return HttpResponseRedirect('/alumno/contacto_urgencia')

	ctx = {
		'nombre_contacto' : contacto.obtenerNombreCompleto,
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

def editar_contactoUrgencia(request, pk):
	template = "alumno/editar_contactoUrgencia.html"
	alumno = ''
	contacto = ContactoDeUrgencia.objects.get(id=pk)
	direccion = Direccion.objects.get(id=contacto.direccion.id)
	guardar = True
	mensaje_error = ''

	form_contacto = FormularioContactoDeUrgencia()
	form_contacto.initial = {
		'nombre': contacto.nombre,
		'apellido': contacto.apellido,
		'parentezco': contacto.parentezco,
		'telefono': contacto.telefono,
		}
	
	form_direccion = FormularioDireccion()
	form_direccion.initial = {
		'calle': direccion.calle,
		'altura': direccion.altura,
		'piso': direccion.piso,
		'nro_departamento': direccion.nro_departamento,
		'provincia': direccion.provincia,
		'localidad': direccion.localidad,
	}

	if request.method == "POST":
		form_contacto = FormularioContactoDeUrgencia(request.POST)
		if form_contacto.is_valid():
			nombre = form_contacto.cleaned_data['nombre']
			nombre = dar_formato(nombre)
			apellido = form_contacto.cleaned_data['apellido']
			apellido = dar_formato(apellido)
			parentezco = form_contacto.cleaned_data['parentezco']
			parentezco = dar_formato(parentezco)
			telefono = form_contacto.cleaned_data['telefono']
			if not telefono.isdigit():
				guardar = False
				mensaje_error = 'Error: solo se permiten numeros en el Telefono.'

			form_direccion = FormularioDireccion(request.POST)

			calle = request.POST.get('calle')
			calle = dar_formato(calle)
			
			altura = request.POST.get('altura')

			if altura == '':
				altura = 0

			piso = request.POST.get('piso')
			if piso == '':
				piso = 0

			nro_departamento = request.POST.get('nro_departamento')
			if not nro_departamento:
				nro_departamento = ' '
				
			if not validar_nro_dpto(nro_departamento):
				guardar = False
				mensaje_error = 'Error: ingresar Nro de Departamento.'

			provincia = request.POST.get('provincia')
			provincia = dar_formato(provincia)
			localidad = request.POST.get('localidad')
			localidad = dar_formato(localidad)

			if guardar:
				direccion.calle =calle 
				direccion.altura=altura
				direccion.piso=piso
				direccion.nro_departamento=nro_departamento.upper()
				direccion.provincia=provincia
				direccion.localidad=localidad
				direccion.save()
				
				contacto.nombre=nombre
				contacto.apellido=apellido
				contacto.parentezco=parentezco
				contacto.telefono=telefono
				contacto.direccion=direccion
				contacto.save()
				return HttpResponseRedirect('/alumno/contacto_urgencia')

	ctx = {
		'nombre_contacto' : contacto.obtenerNombreCompleto,
		'form_contacto': form_contacto,
		'form_direccion': form_direccion,
		'mensaje_error': mensaje_error,
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

#-----------------------------------------------#
def datos_medicos_instancia(alumno):

	a = alumno.datos_medicos
	if not a: 
		dm = DatosMedicos()
		dm.save()
		alumno.datos_medicos = dm
		alumno.save()
		a = alumno.datos_medicos

	return a 

def ver_datos_medicos(request):
	template = "alumno/ver_datos_medicos.html"
	id_alumno = request.user.id

	form = FormularioCargarArchivo()

	mensaje=''
	mensaje_error_dm = ''
	bandera = False

	try:
		alumno = Alumno.objects.get(legajo=request.session['user'])
	except Exception as e:
		alumno = UsuarioInvitado.objects.get(id=id_alumno)

	form_datosMedicos = FormularioDatosMedicos(request.POST or None, instance = datos_medicos_instancia(alumno))

	if request.method == 'POST' and 'boton_guardar_form' in request.POST:
		form = FormularioCargarArchivo(request.POST, request.FILES)
	        if form.is_valid():
	            if request.FILES:
	            	alumno.ficha_medica = form.cleaned_data['ficha_medica']
	            	alumno.save()
                    return HttpResponseRedirect('')
                else:
                	mensaje = 'No ha subido ningún archivo'
	
		
	if request.method == 'POST' and 'boton_guardar_form_dm' in request.POST:
		form_datosMedicos = FormularioDatosMedicos(request.POST)
		dm = DatosMedicos.objects.get(id=alumno.datos_medicos.id)
		if form_datosMedicos.is_valid():
			grupo_sanguineo = form_datosMedicos.cleaned_data['grupo_sanguineo'] 
			alergias = form_datosMedicos.cleaned_data['alergias']
			toma_medicamentos = form_datosMedicos.cleaned_data['toma_medicamentos']
			medicamentos_cuales = form_datosMedicos.cleaned_data['medicamentos_cuales']
			tuvo_operaciones = form_datosMedicos.cleaned_data['tuvo_operaciones']
			operaciones_cuales = form_datosMedicos.cleaned_data['operaciones_cuales']
			tiene_osocial = form_datosMedicos.cleaned_data['tiene_osocial']
			osocial_cual = form_datosMedicos.cleaned_data['osocial_cual']

			dm.grupo_sanguineo = grupo_sanguineo
			dm.alergias = alergias
			dm.toma_medicamentos = toma_medicamentos
			dm.medicamentos_cuales = medicamentos_cuales
			dm.tuvo_operaciones = tuvo_operaciones
			dm.operaciones_cuales = operaciones_cuales
			dm.tiene_osocial = tiene_osocial
			dm.osocial_cual = osocial_cual

			dm.save()

			alumno.datos_medicos = dm
			messages.success(request, 'Sus Datos Médicos han sido guardados correctamente.')
			alumno.save()
			#return HttpResponseRedirect('')
		else:
			messages.error(request, 'Hubo problemas al guardar sus Datos Médicos. Por favor, intente nuevamente.')

	ctx = {
		'deportes': alumno.lista_deporte.all(),
		'form': form,
		'mensaje_error_dm': mensaje_error_dm,
		'alumno': alumno,
		'form_dm': form_datosMedicos,
		'bandera': bandera,
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

###########################PARA PROFESOR###########################################
@login_required
def ver_notificaciones_profesor(request):
	template = "profesor/ver_notificaciones_profesor.html"
	id_profesor = request.user.id
	l_notificaciones = Notificacion.objects.filter(notificar_a = id_profesor)

	if request.method == "POST" and 'boton_eliminarNotificacion' in request.POST:
		id_notificacion = request.POST.get('boton_eliminarNotificacion')
		notificacion = Notificacion.objects.get(id=id_notificacion)
		notificacion.delete()

	ctx = {
		'lista_notificaciones': l_notificaciones, 
	}

	return render_to_response(template, ctx, context_instance=RequestContext(request))


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
	mensaje=''
	
	alumnos = chain(Alumno.objects.filter(lista_deporte__in=pk ), UsuarioInvitado.objects.filter(lista_deporte__in=pk ))  
	consulta = alumnos

	if request.method == 'POST' and 'btn_buscar' in request.POST:
		if request.POST.get('q', '')=='':
			mensaje = 'No ha introducido ningun término en la búsqueda'
			consulta=''
		else:
			if not request.POST.get('opcion'):
				mensaje = 'No ha introducido ningun parámetro de búsqueda'
				consulta=''
			else:
				if request.POST.get('opcion') == 'legajo':
					legajo = request.POST.get('q')
					if legajo.isdigit():
						consulta = Alumno.objects.filter(lista_deporte__in=pk, legajo=request.POST.get('q'))
						if not consulta:
							mensaje = 'No se han encontrado coincidencias'
					else:
						consulta=''
						mensaje='Ingrese un legajo numérico válido'
				else:
					#Inicio Busqueda por apellido
					if request.POST.get('opcion') == 'apellido' and 'btn_buscar' in request.POST:
						apellido = request.POST.get('q')
						if apellido.isalpha():
							consulta = Alumno.objects.filter(last_name__contains=apellido, lista_deporte__in=pk)
							if not consulta:
								mensaje = 'No se han encontrado coincidencias'
						else:
							consulta = ''
							mensaje = 'Usted ha ingresado un apellido invalido'
					#Fin busqueda por apellido
					else:
						#Inicio Busqueda por carrera
						if request.POST.get('opcion') == 'carrera' and 'btn_buscar' in request.POST:
							carrera = request.POST.get('q')
							carrera = carrera.upper()
							#((1,"ISI"),(2,"IQ"), (3, "IEM"), (4, "LAR"), (5, "TSP"), (6, "OTRO"))
							opcion_carrera = ''
							for c in carreras_disponibles:
								if carrera == c[1]:
									opcion_carrera = c[0]
							if opcion_carrera:
								consulta = Alumno.objects.filter(carrera=opcion_carrera, lista_deporte__in=pk)
							else:
								consulta = ''
								mensaje = 'No se han encontrado coincidencias.</br> Recordar que las búsquedas por carrera se realizan mediante las iniciales. </br>ISI para Ingeniería en Sistema de Información. </br>IEM para Ingeniería Electromécanica. </br>IQ para Ingeniería Química. </br>TSP para Técnico Superior en Programación. </br>LAR para Licenciatura en Administracion Rural'
						
	ctx = {
		'mensaje': mensaje,
		'alumnos': consulta,
		'nombre': Deporte.objects.get(id=pk).nombre,
	}
	
	return render_to_response(template,ctx, context_instance=RequestContext(request))

@login_required
def ver_usuarios(request):
	template='admin/ver_usuarios.html'
	ctx = {
		'usuarios': Persona.objects.all(),
	}
	return render_to_response(template,ctx, context_instance=RequestContext(request))

@login_required
def ver_informacion_alumno(request, pk):
	template = "profesor/ver_informacion_alumno.html"
	ctx = {}
	datos_medicos = ''
	cantidad =0
	
	try:
		alumno = Alumno.objects.get(id=pk)
		tipo_usuario = 'alumno'
		legajo = alumno.legajo
		
		if request.method == 'POST' and 'boton_calcular' in request.POST:
			f_desde = request.POST.get('fecha_desde')
			f_hasta = request.POST.get('fecha_hasta')
			cantidad = obtener_datos_academicos(username=str(legajo), f_desde=f_desde, f_hasta=f_hasta)

	except Exception as e:
		alumno = UsuarioInvitado.objects.get(id=pk)
		tipo_usuario = 'invitado'

	
	try:
		datos_medicos = DatosMedicos.objects.get(id=alumno.datos_medicos.id)
	except Exception as e:
		print(e)
	
	ctx = {
		'alumno': alumno,
		'contactos': alumno.contactos_de_urgencia.all(),
		'alumnoUTN': tipo_usuario=='alumno',
		'alumnoInvitado': tipo_usuario=='invitado',
		'cantidad': cantidad,
		#'dm': datos_medicos,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))
 

@login_required
def modificarPerfilProfesor(request):
	template = "profesor/modificar_perfil_profesor.html"
	form = FormularioCargarImagen()
	mensaje=''
	profesor = Profesor.objects.get(id=request.user.id) 
	extiende = 'baseProfesor.html'

	if request.method == 'POST':
		form = FormularioCargarImagen(request.POST, request.FILES)
		if form.is_valid():
			if request.FILES:
				p = Persona.objects.get(id=request.user.id)
				if not p.foto_perfil == "usuarios/fotos_de_perfil/None/default_profile.jpg":
					p.foto_perfil.delete(False)
	
				p.foto_perfil = form.cleaned_data['foto_perfil']
				p.save()
				return HttpResponseRedirect('')
			else:
				mensaje='no ha seleccionado ninguna imagen'

	ctx = {
			'form': form,
			'mensaje': mensaje,
			'legajo': profesor.legajo,
			'profesor': profesor,
			'usuario':request.user.username,
			'nombre': request.user.first_name,
			'apellido': request.user.last_name,
			'dni': profesor.dni,
			'sexo': profesor.ver_sexo,
			'fecha_nacimiento': profesor.fecha_nacimiento,
			'telefono': profesor.telefono,
			'direccion': profesor.direccion,
			'extiende': extiende,	
			}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

@login_required
def verPerfilProfesor(request, pk):
	template = "profesor/modificar_perfil_profesor.html"
	form = FormularioCargarImagen()
	mensaje=''
	profesor = Profesor.objects.get(id=pk)
	extiende = 'baseAdmin.html'
		
	if request.method == 'POST':
		form = FormularioCargarImagen(request.POST, request.FILES)
		if form.is_valid():
			if request.FILES:
				p = Persona.objects.get(id=request.user.id)
				if not p.foto_perfil == "usuarios/fotos_de_perfil/None/default_profile.jpg":
					p.foto_perfil.delete(False)
	
				p.foto_perfil = form.cleaned_data['foto_perfil']
				p.save()
				return HttpResponseRedirect('')
			else:
				mensaje='no ha seleccionado ninguna imagen'

	ctx = {
			'form': form,
			'mensaje': mensaje,
			'legajo': profesor.legajo,
			'profesor': profesor,
			'usuario':profesor.username,
			'nombre': profesor.first_name,
			'apellido': profesor.last_name,
			'dni': profesor.dni,
			'sexo': profesor.ver_sexo,
			'fecha_nacimiento': profesor.fecha_nacimiento,
			'telefono': profesor.telefono,
			'direccion': profesor.direccion,
			'email':profesor.email,	
			'extiende': extiende,
			}

	return render_to_response(template, ctx, context_instance=RequestContext(request))

@login_required
def verPerfilInvitado(request, pk):
	template = "alumno/modificar_perfil_alumno.html"
	form = FormularioCargarImagen()
	mensaje= ""
	extiende ="baseAdmin.html"

	if request.method == 'POST':
		form = FormularioCargarImagen(request.POST, request.FILES)
		if form.is_valid():
			if request.FILES:
				try:
					p = Persona.objects.get(id=request.user.id)
				except Exception as e:
					p = Alumno.objects.get(legajo=int(request.session['user']))
				

				if not p.foto_perfil == "usuarios/fotos_de_perfil/None/default_profile.jpg":
					p.foto_perfil.delete(False)
				
				p.foto_perfil = form.cleaned_data['foto_perfil']
				p.save()
				return HttpResponseRedirect('')
			else:
				mensaje='no ha seleccionado ninguna imagen'

	try:
		alumno = Alumno.objects.get(legajo=int(request.session['user']))
		tipo_usuario = "alumno"
		ctx1 = {
			'legajo': request.session['user'],
			'carrera': mostrar_carrera(request.session['carrera']),
			'email': request.session['correo'],
			'nombre': request.session['nombre'],
			'apellido': request.session['apellido'],
			'sexo': mostrar_sexo(request.session['sexo']),
			'fecha_nacimiento': request.session['fecha_nacimiento'],
			'telefono': request.session['telefono'],
			'email':alumno.email,
			'direccion': request.session['direccion'],
		} 	 
	except Exception as e:
		alumno = UsuarioInvitado.objects.get(id=pk)
		tipo_usuario = "invitado"

		ctx1 = {
			'institucion': alumno.institucion,
			'email': alumno.email,
			'nombre': alumno.first_name,
			'apellido': alumno.last_name,
			'sexo': alumno.ver_sexo,
			'fecha_nacimiento': alumno.fecha_nacimiento,
			'telefono': alumno.telefono,
			'email':alumno.email,
			'direccion': alumno.direccion,
		} 

	ctx = {
			'form': form,
			'mensaje': mensaje,
			#'usuario':request.user.username,
			'alumno': alumno,
			'dni': alumno.dni,
			'is_alumno': "alumno"==tipo_usuario,
			'is_invitado': "invitado"==tipo_usuario,		
			'extiende':extiende
			}

	ctx.update(ctx1)

	return render_to_response(template, ctx, context_instance=RequestContext(request))

