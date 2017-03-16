from django.conf.urls import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
	
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('novedades.urls')),
    url(r'^', include('usuarios.urls')),
    url(r'^', include('deportes.urls')),
    url(r'^', include('canchas.urls')),

    url(r'^inicio$', 'usuarios.views.vista_pagina_inicio', name='url_login'),
    url(r'^logout/$', 'usuarios.views.app_logout', name="url_logout"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT,}),
    #url(r'^usuario_noLogueado$', 'usuarios.views.vista_index_noLogueado', name= 'usuario_noLogueado'),
    #url(r'^ingreso$', ingreso),
    #url(r'^login$', login),
    #url(r'^enviar', enviar),
   
    
)

