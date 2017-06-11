from django.conf.urls import *
from django.contrib import admin
from views import *

admin.autodiscover()

urlpatterns = patterns('',
	#url(r'^deportes/$', lista_deportes, name='lista_deportes'),
    #url(r'^deportes/(?P<pk>[0-9]+)/$', DetallesDeportes.as_view(), name='deporte-detalles'),
    url(r'^deportes/crear/$', crear_deporte, name='crear_deporte'),
    #url(r'^deportes/(?P<pk>[0-9]+)/modificar/$', ActualizarDeportes.as_view(), name='deporte-actualizar'),
    #url(r'^deportes/(?P<pk>[0-9]+)/eliminar/$', EliminarDeportes.as_view(), name='eliminar-deportes'),

    url(r'^ver-lista-deportes$',ver_deportes_personas, name='ver_deportes_personas'),
    url(r'^listar_deportes$',listar_deportes, name='listar_deportes'),
    url(r'^inscripcion_deportes$',inscripcion_deportes, name='inscribir_deportes'),
    url(r'^baja_deporte/(?P<pk>[0-9]+)$',baja_deporte, name='desinscribir_deporte'),
    url(r'^inscribir_deporte/(?P<pk>[0-9]+)$',inscribir_deporte, name='inscripcion_deporte'),
    url(r'^deportes/detalle/(?P<pk>[0-9]+)$',deporte_detalle, name='deporte_detalle'),

)

#URLs PROFESOR
urlpatterns += patterns('',
    url(r'^ficha_medica/deportes$', listar_parafichaMedica, name='listar_parafichaMedica'),
    url(r'^ficha_medica/editar_ficha/(?P<pk>[0-9]+)$', subir_fichaMedicaStandar, name='subir_ficha'),
    url(r'^ficha_medica/eliminar/(?P<pk>[0-9]+)$', delete_fichamedica, name='delete_fichamedica'),
    url(r'^profesor/deporte/editar_informacion/(?P<pk>[0-9]+)$', editar_info_deporte, name='editar_info_deporte'),
    url(r'^profesor/deporte/editar_informacion/(?P<pk>[0-9]+)/agregar_entrenamiento/$', editar_entrenamiento_deporte, name='editar_entrenamiento_deporte'),
)

#URL ALUMNO
urlpatterns+= patterns('',

)

#URL ADMIN
urlpatterns+= patterns('',
    url(r'^administrador/nuevo_deporte$', crear_deporte, name='crear-deporte'),
    url(r'^administrador/deportes$', detalleDeporte, name = 'listar-deporte'),
    url(r'^administrador/eliminar_deporte/(?P<pk>[0-9]+)$', eliminar_deporte, name ='eliminar_deporte'),
    url(r'^administrador/modificar_deportes/(?P<pk>[0-9]+)$', modificar_deporte, name = 'modificar_deporte'),

)
