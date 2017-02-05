from django.conf.urls import *
from novedades.views import *
from django.contrib.auth.views import login 
from django.contrib import admin
from views import *

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^inicial_alumnos$', vista_index_alumnos, name='inicial_alumnos'),
    url(r'^inicial_profesores$', vista_index_profesores, name='inicial_profesores'),
    url(r'^usuario_noLogueado$', vista_index_noLogueado, name= 'usuario_noLogueado'),

    url(r'^novedades_alumnos$', novedades_alumnos, name='novedades_alumnos'),
    
    
   
    url(r'^novedades_todos$', ver_novedades_visibilidadTodos, name='ver_novedades_visibilidadTodos'),	
)

#Para PROFESOR
urlpatterns += patterns('',
    url(r'^novedades/$', ListarNovedades.as_view(), name='listar-novedades'),
    url(r'^novedades/(?P<pk>[0-9]+)/$', DetallesNovedades.as_view(), name='detalle-novedad'),
    url(r'^novedades/crear/$', CrearNovedades.as_view(), name='crear-novedad'),
    url(r'^novedades/(?P<pk>[0-9]+)/modificar/$', ActualizarNovedades.as_view(), name='actualizar-novedad'),
    url(r'^novedades/(?P<pk>[0-9]+)/eliminar/$', EliminarNovedades.as_view(), name='eliminar-novedad'), 

)