from django.conf.urls import *
from novedades.views import *
from django.contrib.auth.views import login 
from django.contrib import admin
from views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^novedades/$', ListarNovedades.as_view(), name='listar-novedades'),
    url(r'^novedades/(?P<pk>[0-9]+)/$', DetallesNovedades.as_view(), name='detalle-novedad'),
    url(r'^novedades/crear/$', CrearNovedades.as_view(), name='crear-novedad'),
    url(r'^novedades/modificar/(?P<pk>[0-9]+)/$', ActualizarNovedades.as_view(), name='actualizar-novedad'),
    url(r'^novedades/eliminar/(?P<pk>[0-9]+)/$', EliminarNovedades.as_view(), name='eliminar-novedad'),
)

urlpatterns += patterns('',
    url(r'^inicial_alumnos$', vista_index_alumnos, name='inicial_alumnos'),
    url(r'^inicial_profesores$', vista_index_profesores, name='inicial_profesores'),
    url(r'^novedades_alumnos$', novedades_alumnos, name='novedades_alumnos'),
    url(r'^novedades/ver/(?P<pk>[0-9]+)/$', ver_novedades , name='ver_novedades'),
    url(r'^novedades_alumnos/filtrar/(?P<pk>[0-9]+)/$', ver_novedad_filtrado , name='ver_novedad_filtrado'),
    url(r'^novedades_todos$', ver_novedades_visibilidadTodos, name='ver_novedades_visibilidadTodos'),   
)

#Para ADMIN
urlpatterns += patterns('',
    url(r'^administrador/novedades/$', ver_novedades_admin, name='ver_novedades_admin'),
    url(r'^administrador/novedades/crear$', crear_novedad_admin, name='crear_novedad_admin'),
    url(r'^administrador/novedades/editar/(?P<pk>[0-9]+)/$', editar_novedades_admin, name='editar_novedad_admin'),
    url(r'^administrador/novedades/visualizar/(?P<pk>[0-9]+)/$', ver_novedad_admin, name='visualizar_novedad_admin'),


)


#Para profesores
urlpatterns += patterns('',
    url(r'^novedades_profesor$', novedades_profesores, name='novedades_profesores'),
)

    
