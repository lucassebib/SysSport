#-!-coding: utf-8 -!-
from usuarios.models import Alumno, Profesor, UsuarioInvitado, carreras_disponibles, lista_sexos

def buscador_alumnos(request, consulta, mensaje, pk):
	if request.method == 'GET' and 'btn_buscar' in request.GET:
		if request.GET.get('q', '')=='':
			mensaje = 'No ha introducido ningun término en la búsqueda'
			consulta=''
		else:
			if not request.GET.get('opcion'):
				mensaje = 'No ha introducido ningun parámetro de búsqueda'
				consulta=''
			else:
				if request.GET.get('opcion') == 'legajo':
					legajo = request.GET.get('q')
					if legajo.isdigit():
						consulta = Alumno.objects.filter(lista_deporte__in=pk, legajo=request.GET.get('q'))
						if not consulta:
							mensaje = 'No se han encontrado coincidencias'
					else:
						consulta=''
						mensaje='Ingrese un legajo numérico válido'
				else:
					#Inicio Busqueda por apellido
					if request.GET.get('opcion') == 'apellido' and 'btn_buscar' in request.GET:
						apellido = request.GET.get('q')
						if apellido.isalpha():
							consulta = Alumno.objects.filter(last_name__contains=apellido, lista_deporte__in=pk)
							if not consulta:
								mensaje = 'No se han encontrado coincidencias'
						else:
							consulta = ''
							mensaje = 'Usted ha ingresado un apellido invalido'
					#Fin busqueda por apellido
					else:
						#Inicio Busqueda por carrera
						if request.GET.get('opcion') == 'carrera' and 'btn_buscar' in request.GET:
							carrera = request.POST.get('q')
							carrera = carrera.upper()
							#((1,"ISI"),(2,"IQ"), (3, "IEM"), (4, "LAR"), (5, "TSP"), (6, "OTRO"))
							opcion_carrera = ''
							for c in carreras_disponibles:
								if carrera == c[1]:
									opcion_carrera = c[0]
							if opcion_carrera:
								consulta = Alumno.objects.filter(carrera=opcion_carrera, lista_deporte__in=pk)
							else:
								consulta = ''
								mensaje = 'No se han encontrado coincidencias. Recordar que las búsquedas por carrera se realizan mediante las iniciales. ISI para Ingeniería en Sistema de Información. IEM para Ingeniería Electromécanica. IQ para Ingeniería Química. TSP para Técnico Superior en Programación. LAR para Licenciatura en Administracion Rural'
	return consulta, mensaje						

def obtener_id(request):
	"""
		Recibe request como parametro y devuelve el id del usuario autenticado 
		segun sea o Alumno o (AlumnoInvitado|Profesor|Admin)
	"""
	
	if 'id_user' in request.session:
		id_usuario = int(request.session['id_user'])
	else:
		try:
			id_usuario = int(request.user.id)
		except Exception as e:
			id_usuario = 0
			print(e)
	
	return id_usuario

def extiende_de(id_usuario, request):
	"""
	"""
	extiende = ''
	try:
		if request.user.is_staff:
			extiende = 'baseAdmin.html'
		else: 
			g = Alumno.objects.get(id=id_usuario)
			extiende = 'baseAlumno.html'
	except Exception as e:
		try:
			g = Profesor.objects.get(id=id_usuario)
			extiende = 'baseProfesor.html'
		except Exception as e:
			try:
				g = UsuarioInvitado.objects.get(id=id_usuario)
				extiende = 'baseAlumno.html'
			except Exception as e:
				extiende = 'usuario_noLogueado.html'
	return extiende

def mostrar_carrera(cod_carrera):
	"""
	"""
	return dict(carreras_disponibles).get(cod_carrera)

def mostrar_sexo(cod_sexo):
	"""
	"""
	return dict(lista_sexos).get(cod_sexo)

def dar_formato(cadena):
	"""
		Recibe como parmetro un string y le aplica los siguientes cambios:
		- Lo deja en formato titulo
		- Eliminar caracteres en blanco a la izq y der
		- Eliminar excesos de blancos entre palabras
	"""
	c = cadena
	c = c.title()
	c = c.strip()
	corte = c.split()
	c = ''
	cont = 0
	for p in corte:
		cont = cont + 1
		if cont==len(corte):
			c = c + p
		else:
			c = c + p + ' ' 
	
	return c

def validar_nro_dpto(nro_dpto):
	"""
		Valida que un nro de dpto se encuetre en el rango 1..99 o A..Z
	"""
	alfabeto = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	flag = False
	if (nro_dpto.isalpha() and len(nro_dpto)==1 and (nro_dpto.lower() in alfabeto)):
		#nro_dpto en el rango A..Z o si es solo blanco
		flag = True
	else:
		#nro_dpto en el rango 1..99
		if nro_dpto.isdigit():
			flag = True
		else:
			if nro_dpto.isspace():
				return True

	return flag
