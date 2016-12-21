from django.conf.urls import patterns, include, url
from django.contrib import admin
from novedades.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'syssport.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^index$', pagina_principal),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^base/$', base),
    url(r'^login$', login)
)
