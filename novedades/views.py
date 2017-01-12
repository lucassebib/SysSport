from django.shortcuts import render, render_to_response, RequestContext, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loguear, logout
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from novedades.models import Novedades
from usuarios.models import Alumno
from deportes.models import Deporte

@login_required	
def vista_index_alumnos(request):

	template = "inicial_alumnos.html"
	
	id_usuario = request.user.id
	alumno = Alumno.objects.get(id=id_usuario)
	
	deportes_alumno = alumno.obtener_deportes()
	
	posts = Novedades.objects.filter(visibilidad__in=[1,2])
	post_exclusivos = Novedades.objects.filter(visibilidad__in=[3], categoria__in=deportes_alumno)

	posts_visibles = posts | post_exclusivos

	#posts_visibles = []

	deportes_existentes = Deporte.objects.all()

	ctx = {
		"deportes": deportes_alumno,
		"sport": deportes_existentes,
		#"posts": posts_visibles,
		"posts": posts_visibles.order_by('-fecha_publicacion'),
	}
	return render_to_response(template,ctx , context_instance=RequestContext(request))

def vista_index_profesores(request):
	return render_to_response('inicial_profesores.html')

def vista_index_invitados(request):
	return render_to_response('inicial_invitados.html')
	
#def ingreso(request):
	#return render_to_response('ingreso.html')

#def base(request):
	#return render_to_response('base.html')
	
#def base2(request):
	#return render_to_response('base2.html')

#def login(request):
	#return render_to_response('login.html')



#def enviar(request):
	#return render_to_response('gracias.html')

#def formulario(request):
	#return render_to_response('registro.html')





