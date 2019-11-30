# Librerias
from django.contrib import admin
from posts.models import Post

# Modelos agregados al panel administrativo
admin.site.register(Post)