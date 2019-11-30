# Librerias
from django import forms
from posts.models import Post

# Formularios creados en el HTML
class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('user', 'profile', 'titulo', 'foto')