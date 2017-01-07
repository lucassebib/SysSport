from django.conf.urls import *
from django.contrib import admin
from novedades.views import *

admin.autodiscover()

urlpatterns = patterns('',
	
    url(r'^admin/', include(admin.site.urls)),
    url(r'^inicio$', principal, name="url_login"),

    url(r'^inicial_alumnos$', vista_index_alumnos),
    url(r'^inicial_profesores$', vista_index_profesores),
    url(r'^inicial_invitados$', vista_index_invitados),    

    url(r'^ingreso$', ingreso),
    url(r'^recup_clave$', clave),
    url(r'^login$', login),
    url(r'^enviar', enviar),
    url(r'^', include('novedades.urls')),
    url(r'^hola$', app_home, name="url_home"),
    url(r'^autenticar/$', app_login, name="url_login"),
    url(r'^logout/$', app_logout, name="url_logout"),

)