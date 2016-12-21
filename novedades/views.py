from django.shortcuts import render_to_response

# Create your views here.

def pagina_principal(request):
	return render_to_response('index.html')

def  base(request):
	return render_to_response('base.html')

def login(request):
	return render_to_response('login.html')

def formulario(request):
	return render_to_response('formularioRegistro.html')
