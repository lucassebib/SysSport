from django import forms
from models import Novedades
from usuarios.models import Profesor 

class FormularioNovedades(forms.ModelForm):
	class Meta:
		model = Novedades
		fields = ['titulo','contenido', 'imagen','visibilidad']

	def form_valid(self, form):
		a = form.save(commit = False)
		a.autor = Profesor.objects.get(id = self.request.user.id)
		return super(FormularioNovedades, self).form_valid(form)

#	def __init__(self, *args, **kwargs): 
 #       user = kwargs.pop('user', None) # pop the 'user' from kwargs dictionary      
  #      super(FormularioNovedades, self).__init__(*args, **kwargs)
        #self.fields['categoria'] = forms.ModelChoiceField(queryset=Waypoint.objects.filter(user=user))


	