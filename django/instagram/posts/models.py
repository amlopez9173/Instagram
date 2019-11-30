# Librerias
from django.db import models
from django.contrib.auth.models import User

# Modelo para Publicaciones
class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
	titulo = models.CharField(max_length=255)
	foto = models.ImageField(upload_to='posts/fotos')
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{} by @{}'.format(self.titulo, self.user.username)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)