from deportes.models import *

# BUSCADOR
def buscador_deportes(request, consulta, mensaje):  
    if request.POST.get('q', '')=='':
        mensaje = ''
    else:
        if not request.POST.get('opcion'):
            mensaje = 'No ha introducido ningun parametro de busqueda'
            consulta=''
        else:
            #     BUSQUEDA POR TITULO
            if request.POST.get('opcion') == 'nombre':
                nombre = request.POST.get('q')
                consulta = consulta.filter(nombre__contains=nombre)
                if not consulta:
                    mensaje = 'No se han encontrado coincidencias'
    return consulta, mensaje
#finBUSCADOR
    