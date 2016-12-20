from django.shortcuts import render_to_response

# Create your views here.

def pagina_principal(request):
	return render_to_response('index.html')
