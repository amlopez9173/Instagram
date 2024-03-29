# Librerias
from django import forms 
from django.contrib.auth.models import User
from users.models import Profile

# Formulario de registro
class SignupForm(forms.Form):
	username = forms.CharField(min_length=4, max_length=50)
	password = forms.CharField(max_length=70, widget=forms.PasswordInput())
	password_confirmation = forms.CharField(max_length=70, widget=forms.PasswordInput())
	first_name = forms.CharField(min_length=2, max_length=50)
	last_name = forms.CharField(min_length=2, max_length=50)
	email = forms.CharField(min_length=6, max_length=70, widget=forms.EmailInput())

	def clean_username(self):
		username = self.cleaned_data['username']
		username_taken = User.objects.filter(username=username).exists()
		if username_taken:
			raise forms.ValidationError('Usuario ya esta registrado')
		return username

	def clean(self):
		data = super().clean()
		password = data['password']
		password_confirmation = data['password_confirmation']
		if password != password_confirmation:
			raise forms.ValidationError('Password no son iguales')
		return data

	def save(self):
		data = self.cleaned_data
		data.pop('password_confirmation')
		user = User.objects.create_user(**data)
		profile = Profile(user=user)
		profile.save()

# Formulario de Perfil
class ProfileForm(forms.Form):
	biografia = forms.CharField(max_length=500, required=False)
	telefono = forms.CharField(max_length=20, required=False)
	foto = forms.ImageField()