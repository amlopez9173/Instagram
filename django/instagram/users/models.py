# Librerias
from django.db import models
from django.contrib.auth.models import User 

# Modelo para Perfil
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	biografia = models.TextField(blank=True)
	telefono = models.CharField(max_length=20, blank=True)

	foto = models.ImageField(upload_to='users/pictures', blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username

# Modelo para Seguidores
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_one')
    user_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_two')