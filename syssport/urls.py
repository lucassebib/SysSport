from django.conf.urls import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import *

admin.autodiscover()

urlpatterns = patterns('',
	
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('novedades.urls')),
    url(r'^', include('usuarios.urls')),
    url(r'^', include('deportes.urls')),
    url(r'^', include('canchas.urls')),

    url(r'^inicio$', vista_pagina_inicio, name='url_login'),
    url(r'^registrarse$', vista_registrarse, name='registrarse'),
    url(r'^logout/$', app_logout, name="url_logout"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT,}),
    
)

