from usuarios.models import Alumno, Profesor, UsuarioInvitado

def obtener_id(request):
	"""
		Recibe request como parametro y devuelve el id del usuario autenticado 
		segun sea o Alumno o (AlumnoInvitado|Profesor|Admin)
	"""
	if 'id_user' in request.session:
		id_usuario = int(request.session['id'])
	else:
		id_usuario = int(request.user.id)
	
	return id_usuario

def extiende_de(id_usuario, request=None):
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
	return extiende