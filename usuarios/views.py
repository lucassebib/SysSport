from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loguear, logout
from forms import *
from usuarios.models import Alumno, Persona, Profesor, UsuarioInvitado, Direccion, ContactoDeUrgencia 
from deportes.models import Deporte
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.conf import settings
from django.db.models import Q
from itertools import chain
from novedades.paginacion import Paginate


def vista_pagina_inicio(request):
	form1 = FormularioAutenticacion()
	template = "inicio.html"

	if request.method == "POST":
		form1 = FormularioAutenticacion(request.POST)
		if form1.is_valid():
			usuario = form1.cleaned_data['username']
			password = form1.cleaned_data['password']
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
						ctx = {"form1":form1, "mensaje": "Usuario Inactivo"}
						return render_to_response(template,ctx, context_instance=RequestContext(request))
				else:
					ctx = {"form1":form1, "mensaje": "Nombre de usuario o password incorrectos"}
					return render_to_response(template,ctx, context_instance=RequestContext(request))
			except Exception as e:
				if user.is_staff:
					return HttpResponseRedirect('/inicial-admin')

	ctx = {"form1":form1, "mensaje":""}
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

@login_required
def ver_informacion_perfil_persona(request, pk):
	template = "ver_informacion_perfil_persona.html"
	id_usuario = request.user.id
	tipo_usuario = "" 
	ctx1 = {}
	try:
		g = Alumno.objects.get(id=id_usuario)
		extiende = 'baseAlumno.html'
		tipo_usuario = 'alumno'
		ctx1 = {
			'carrera': g.ver_nombre_carrera,
		}
	except Exception as e:
		try:
			g = Profesor.objects.get(id=id_usuario)
			extiende = 'baseProfesor.html'
		except Exception as e:
			try:
				g = UsuarioInvitado.objects.get(id=id_usuario)
				extiende = 'baseAlumno.html'
				tipo_usuario = "invitado"
				
				ctx1 = {
					'institucion': g.institucion,
				} 	 

			except Exception as e:
				try:
					extiende = 'usuario_noLogueado.html'
				except Exception as e:
					if request.user.is_staff:
						extiende = 'baseAdmin.html'


	ctx = {
			'extiende': extiende,
			'persona': Persona.objects.get(id=pk),
			'is_invitado': "invitado"==tipo_usuario,
			'is_alumno': "alumno"==tipo_usuario,

			}
	ctx.update(ctx1)

	return render_to_response(template, ctx, context_instance=RequestContext(request))


###########################PARA ALUMNOS###########################################
#@login_required	
#def vista_index_noLogueado(request):
#	template = "usuario_noLogueado.html"	
#	return render_to_response(template, context_instance=RequestContext(request))

@login_required
def modificarPerfilAlumno(request):
	template = "alumno/modificar_perfil_alumno.html"
	form = FormularioCargarImagen()
	mensaje= ""

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

	try:
		alumno = Alumno.objects.get(id=request.user.id)
		tipo_usuario = "alumno"
		ctx1 = {
			'legajo': alumno.legajo,
			'alumno': alumno,
			'carrera': alumno.ver_nombre_carrera,
		} 	 
	except Exception as e:
		alumno = UsuarioInvitado.objects.get(id=request.user.id)
		tipo_usuario = "invitado"

		ctx1 = {
			'institucion': alumno.institucion,
			'alumno': alumno,
		} 

	ctx = {
			'form': form,
			'mensaje': mensaje,
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
def agregar_contactoUrgencia(request):
	template = "alumno/agregar_contacto_urgencia.html"
	form_principal = FormularioContactoDeUrgencia()
	form_direccion = FormularioDireccion()

	if request.method == "POST":
		form_principal = FormularioContactoDeUrgencia(request.POST)
		if form_principal.is_valid():
			

			nombre = form_principal.cleaned_data['nombre']
			apellido = form_principal.cleaned_data['apellido']
			parentezco = form_principal.cleaned_data['parentezco']
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

			direccion = Direccion(calle=calle, altura=altura, piso=piso, nro_departamento=nro_departamento, provincia=provincia, localidad=localidad)
			direccion.save()
			
			contacto = ContactoDeUrgencia(nombre=nombre, apellido=apellido, parentezco=parentezco, telefono=telefono, direccion=direccion)
			contacto.save()

			try:
				alumno = Alumno.objects.get(id=request.user.id)
			except Exception as e:
				alumno = UsuarioInvitado.objects.get(id=request.user.id)
			
			alumno.contactos_de_urgencia.add(contacto)
			alumno.save()
			
			return HttpResponseRedirect('/contacto_urgencia')

	ctx = {
		'form_principal': form_principal,
		'form_direccion': form_direccion,
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def ver_contacto_urgencia(request):
	template = "alumno/ver_contacto_urgencia.html"
	contactos = ''

	try:
		contactos = Alumno.objects.get(id=request.user.id).contactos_de_urgencia.all()
	except Exception as e:
		contactos = UsuarioInvitado.objects.get(id=request.user.id).contactos_de_urgencia.all()

	pag = Paginate(request, contactos, 1)

	ctx = {
		'contactos': pag['queryset'],
     	'paginator': pag,

	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

def ver_datos_medicos(request):
	template = "alumno/ver_datos_medicos.html"
	id_alumno = request.user.id
	form = FormularioCargarArchivo()
	mensaje=''

	try:
		alumno = Alumno.objects.get(id=id_alumno)
	except Exception as e:
		alumno = UsuarioInvitado.objects.get(id=id_alumno)

	if request.method == 'POST':
	        form = FormularioCargarArchivo(request.POST, request.FILES)
	        if form.is_valid():
	            if request.FILES:
	            	alumno.ficha_medica = form.cleaned_data['ficha_medica']
	            	alumno.save()
                    return HttpResponseRedirect('')
                else:
                	mensaje = 'no ha subido ningun archivo'


	ctx = {
		'deportes': alumno.lista_deporte.all(),
		'form': form,
		'mensaje': mensaje,
		'alumno': alumno,
	}
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
		'contactos': alumno.contactos_de_urgencia.all(),
		'alumnoUTN': tipo_usuario=='alumno',
		'alumnoInvitado': tipo_usuario=='invitado',
	}
	return render_to_response(template, ctx, context_instance=RequestContext(request))

@login_required
def modificarPerfilProfesor(request):
	template = "profesor/modificar_perfil_profesor.html"
	form = FormularioCargarImagen()
	mensaje=''
	profesor = Profesor.objects.get(id=request.user.id) 

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
			}

	return render_to_response(template, ctx, context_instance=RequestContext(request))
