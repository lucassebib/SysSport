from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^', include('novedades.urls')),
    url(r'^', include('usuarios.urls')),

    url(r'^inicio$', 'usuarios.views.vista_pagina_inicio', name="url_login"),

    #url(r'^ingreso$', ingreso),
    
    #url(r'^login$', login),
    #url(r'^enviar', enviar),
   
    url(r'^logout/$', 'usuarios.views.app_logout', name="url_logout"),
)