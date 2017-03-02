from django.conf.urls import *
from django.contrib import admin
from usuarios.views import *
from django.contrib.auth.views import  password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = patterns('',

	url(r'^registrarse$', vista_registrarse),
	url(r'^inicial-admin$', vista_inicial_admin, name= 'inicial_admin'),
	url(r'^perfil/user/(?P<pk>[0-9]+)$',ver_informacion_perfil_persona, name='ver_informacion_perfil_persona'),

#	url(r'^cambiar-telefono$', cambiar_telefono),
#	url(r'^cambiar-direccion$', cambiar_direccion),
)

#URLs RESET PASSWORD
urlpatterns += patterns('',
	url(r'^cambiar-pass$', cambiar_contrasenia),
	url(r'^password_reset$', password_reset, 
		{ 'template_name' : 'registracion/password_reset_form.html' , 
		'email_template_name' : 'registracion/password_reset_email.html'},
			 name='password_reset'),
    url(r'^reset(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$' ,password_reset_confirm,  
    	{ 'template_name' : 'registracion/password_reset_confirm.html'}, 
    	 name='password_reset_confirm'),
    url(r'^done$' , password_reset_complete, 
    	{ 'template_name' : 'registracion/password_reset_complete.html'}, 
    		name='password_reset_complete'),
    url(r'^password_reset_done$' , password_reset_done, 
    		{ 'template_name' : 'registracion/password_reset_done.html'}, 
    		name='password_reset_done'),
	
)

#URLs ADMIN
urlpatterns += patterns('',
	url(r'^ver-usuarios$', ver_usuarios, name='ver_usuarios'),  
)

#URLs PROFESOR
urlpatterns += patterns('',
	url(r'^ver-deportes$', ver_deportes_profesor, name='ver-deportes'),
	url(r'^ver-alumnos/deporte/(?P<pk>[0-9]+)$', listar_alumnos_deporte, name='ver-alumnos'),
	url(r'^ver-alumnos/deporte/alumno/(?P<pk>[0-9]+)$', ver_informacion_alumno, name='info-alumno'),
	url(r'^modificar_perfil_profesor$', modificarPerfilProfesor, name='modificar_perfil_profesor'),
	url(r'^modificar_perfil_profesor$', modificarPerfilProfesor, name='modificar_perfil_profesor'),
)

#URLs ALUMNOS
urlpatterns += patterns('',
	url(r'^alumno/modificar_perfil_alumno$', modificarPerfilAlumno, name='modificar_perfil_alumno'),
	url(r'^alumno/contacto_urgencia$', ver_contacto_urgencia, name='ver_contacto_urgencia'),
	url(r'^alumno/datos_medicos$', ver_datos_medicos, name='ver_datos_medicos'),
	url(r'^alumno/nuevo_contacto$', agregar_contactoUrgencia, name='agregar_contactoUrgencia'),
	url(r'^alumno/eliminar_contacto/(?P<pk>[0-9]+)$', eliminar_contactoUrgencia, name='eliminar_contactoUrgencia'),

)