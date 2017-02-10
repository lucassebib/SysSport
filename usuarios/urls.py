from django.conf.urls import *
from django.contrib import admin
from usuarios.views import *
from django.contrib.auth.views import  password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth import views as auth_views



admin.autodiscover()

urlpatterns = patterns('',

	url(r'^registrarse$', vista_registrarse),
	url(r'^inicial-admin$', vista_inicial_admin, name= 'inicial_admin'),
	
	url(r'^cambiar-pass$', cambiar_contrasenia),
	url(r'^cambiar-telefono$', cambiar_telefono),
	url(r'^cambiar-direccion$', cambiar_direccion),
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

)

#URLs ALUMNOS
urlpatterns += patterns('',
	url(r'^modificar_perfil_alumno$', modificarPerfilAlumno, name='modificar_perfil_alumno'),
	url(r'^contacto_urgencia$', ver_contacto_urgencia, name='ver_contacto_urgencia'),
	url(r'^datos_medicos$', ver_datos_medicos, name='ver_datos_medicos'),
)