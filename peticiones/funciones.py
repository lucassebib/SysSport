import xml.etree.ElementTree as ET
import time

from datetime import datetime

from peticiones.models import Peticionesservidor

def autenticacion(username, password):
	permitecursado = ''
	fecha = datetime.now().strftime('%Y%m%d%H%M%S')
	IDEXTERNA = str(fecha) + str(username) + 'D'
	peticion = Peticionesservidor()
	peticion.peticion = 300
	peticion.idexterna = IDEXTERNA
	peticion.estado = 0
	peticion.parametro1 = '<?xml version = "1.0" encoding="Windows-1252" standalone="yes"?> <VFPData> <_parametro1> <legajo>'+str(username)+'</legajo> <dni>00</dni> <password>"'+password+'"</password> <tipologueo>3</tipologueo> </_parametro1> </VFPData>'
	try:
		peticion.save(force_insert = True, using='sysacad')
		for x in range(20):
			time.sleep(0.5)
			newPeticion = Peticionesservidor.objects.using('sysacad').get(idexterna = IDEXTERNA)
			if newPeticion.estado > 1:
				break
		estado = newPeticion.estado
		paramXML = ET.fromstring(newPeticion.parametro2.encode('ISO-8859-1'))
		print(newPeticion.parametro2)
		for x in paramXML:
			for z in x:
				if z.tag == 'dni':
					dni = z.text
				elif z.tag == 'permiteinscripcioncursado':
					permitecursado = z.text
				elif z.tag == 'nuevo':
					cambio = z.text

		if estado == 3:
			#todo mal
			return False
		else:
			if estado == 2:
				return True
	except Exception as a:
		return a