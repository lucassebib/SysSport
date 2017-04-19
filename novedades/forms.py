
from django import forms
from models import Comentario, Novedades
from usuarios.models import Persona, Profesor
from deportes.models import Deporte

class FormularioComentario(forms.ModelForm):
	def form_valid(self, form):
		a = form.save(commit = False)
		a.autor = Persona.objects.get(id = self.request.user.id)
		return super(FormularioComentario, self).form_valid(form)

	class Meta:
		model = Comentario
		fields = ['texto']
		widgets={
			'texto': forms.Textarea(attrs={'cols':'60', 'rows':'20', 'onKeyDown':"contador(this.form.texto,this.form.remLen,125);", 'onKeyUp':"contador(this.form.mensaje,this.form.remLen,125);"})
		}

class FormularioNovedades(forms.ModelForm):
	class Meta:
		model = Novedades
		fields = ['titulo', 'contenido', 'imagen','visibilidad', 'categoria']
		contenido =forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows':'20'}))
		#categoria= forms.MultipleChoiceField( widget=forms.CheckboxSelectMultiple())
		

	def __init__(self, user, *args, **kwargs):
		super(FormularioNovedades, self).__init__(*args, **kwargs)
		deportes = Profesor.objects.get(id = user.id).lista_deporte.all()
		self.fields["categoria"].widget = forms.CheckboxSelectMultiple()
		self.fields["categoria"].queryset = Deporte.objects.filter(id__in=deportes)


class FormularioNovedadesAdmin(forms.ModelForm):
	class Meta:
		model = Novedades
		exclude = ['lista_comentarios', 'autor']
		widgets = {
           'categoria': forms.CheckboxSelectMultiple,
        }

	#def form_valid(self, form):
	#	a = form.save(commit = False)
	#	a.autor = self.request.user
	#	return super(FormularioNovedadesAdmin, self).form_valid(form)



 

    

	