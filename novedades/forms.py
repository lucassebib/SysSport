from django import forms
from models import Comentario, Novedades
from usuarios.models import Persona, Profesor
from deportes.models import Deporte
#from tinymce import models as tinymce_models

class FormularioComentario(forms.ModelForm):
	def form_valid(self, form):
		a = form.save(commit = False)
		a.autor = Persona.objects.get(id = self.request.user.id)
		return super(FormularioComentario, self).form_valid(form)

	class Meta:
		model = Comentario
		fields = ['texto']

class FormularioNovedades(forms.ModelForm):
	#contenido = tinymce_models.HTMLField()

	class Meta:
		model = Novedades
		fields = ['titulo', 'contenido', 'imagen','visibilidad', 'categoria']
		widgets = {
           'categoria': forms.CheckboxSelectMultiple,
        }

	def __init__(self, user, *args, **kwargs):
		super(FormularioNovedades, self).__init__(*args, **kwargs)
		deportes = Profesor.objects.get(id = user.id).lista_deporte.all()
		#self.fields["categoria"].widget = forms.CheckboxSelectMultiple()
        	self.fields["categoria"].queryset = Deporte.objects.filter(id__in=deportes)



 

    

	