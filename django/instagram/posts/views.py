# Librerias
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.forms import PostForm
from posts.models import Post, Like, Comment
from users.models import Follow

# Vista de listar publicaciones
@login_required
def listar_posts(request):
	id = request.user.id
	usuario = User.objects.get(pk=id)

	arreglo_followers = []
	arreglo_likes = []
	arreglo_comments = []

	followers = Follow.objects.all().filter(user=usuario)
	for follower in followers:
		arreglo_followers.append(follower.user_follow.id)

	arreglo_followers.append(usuario.id)
	posts = Post.objects.all().filter(user__in=arreglo_followers).order_by('-created')
	for post in posts:
		comments = Comment.objects.all().filter(post=post.id)
		for comment in comments:
			arreglo_comments.append([post.id, comment.user.username, comment.message])

		likes = Like.objects.filter(post=post.id).count()
		arreglo_likes.append([post.id, likes])

	return render(request, 'posts/posts.html', {'posts' : posts, 'likes' : arreglo_likes, 'comments' : arreglo_comments})

# Vista para crear una publicacion
@login_required
def create_post(request):
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('post')
	else:
		form = PostForm()

	return render(request=request, template_name = 'posts/new.html', context = {'form': form, 'user': request.user, 'profile': request.user.profile})

# Vista para dar like
@login_required
def like(request):
	if request.method == 'POST':
		post = Post.objects.get(pk = request.POST['id'])
		user = User.objects.get(pk = request.user.id)

		contador = Like.objects.filter(post=post, user=user).count()

		if contador > 0:
			eliminar = Like.objects.filter(post=post, user=user)
			eliminar.delete()
		else:
			Like.objects.create(post=post, user=user)

		return redirect('post')

	return render(request, 'posts/posts.html')

# Vista para crear comentarios
@login_required
def hacer_comentario(request):
	if request.method == 'POST':
		post = Post.objects.get(pk = request.POST['post'])
		user = User.objects.get(pk = request.user.id)

		Comment.objects.create(post=post, user=user, message=request.POST['message'])

		return redirect('post')

	return render(request, 'posts/posts.html')