# Librerias
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from posts import views as posts_views
from users import views as users_views

# Rutas del programa
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', posts_views.listar_posts, name='post'),
    path('posts/new/', posts_views.create_post, name='create_post'),
    path('users/login/', users_views.login_view, name='login'),
    path('users/logout/', users_views.logout_view, name='logout'),
    path('users/signup/', users_views.signup, name='signup'),
    path('users/me/profile/', users_views.update_profile, name='update_profile'),
    path('users/me/detail/', users_views.show_profile, name='show_profile'),
    path('users/follow/', users_views.follow, name='follow'),
    path('posts/like/', posts_views.like, name='like'),
    path('posts/comment/', posts_views.hacer_comentario, name='hacer_comentario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
