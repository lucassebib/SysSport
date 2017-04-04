from usuarios.models import Alumno, Profesor, UsuarioInvitado, carreras_disponibles, lista_sexos


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

def extiende_de(id_usuario, request=None):
	"""
	"""
	extiende = ''
	try:
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
				if request.user.is_staff:
					extiende = 'baseAdmin.html'
				else:
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
	if (nro_dpto.isalpha() and len(nro_dpto)==1 and (nro_dpto.lower() in alfabeto)) or (nro_dpto.isspace()):
		#nro_dpto en el rango A..Z o si es solo blanco
		flag = True
	else:
		#nro_dpto en el rango 1..99
		if nro_dpto.isdigit():
			flag = True

	return flag
