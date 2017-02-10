from django import forms
from models import Comentario
from usuarios.models import Persona



class FormularioComentario(forms.ModelForm):
	def form_valid(self, form):
		a = form.save(commit = False)
		a.autor = Persona.objects.get(id = self.request.user.id)
		return super(FormularioComentario, self).form_valid(form)

	class Meta:
		model = Comentario
		fields = ['texto']

 

    

	