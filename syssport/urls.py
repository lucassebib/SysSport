from django.conf.urls import *
from django.contrib import admin
from novedades.views import *

admin.autodiscover()

urlpatterns = patterns('',
	
    url(r'^admin/', include(admin.site.urls)),
    url(r'^inicio$', principal),
    url(r'^ingreso$', ingreso),
    url(r'^base$', base),
    url(r'^base2$', base2),
    url(r'^login$', login),
    url(r'^enviar', enviar),
    url(r'^registro/$', formulario),
    url(r'^', include('novedades.urls')),
    url(r'^hola$', app_home, name="url_home"),
    url(r'^autenticar/$', app_login, name="url_login"),
    url(r'^logout/$', app_logout, name="url_logout"),

)