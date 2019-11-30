# Librerias
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.models import Profile, Follow
from posts.models import Post
from users.forms import ProfileForm, SignupForm
from django.db.utils import IntegrityError

# Vista de iniciar sesión
def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			return redirect('post')
		else:
			return render(request, 'users/login.html', {'error': 'Inválido usuario o contraseña'})
	return render(request, 'users/login.html')

# Vista de cerrar sesión
@login_required
def logout_view(request):
	logout(request)
	return redirect('login')

# Vista de registrarse
def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = SignupForm()

	return render(request=request, template_name = 'users/signup.html', context = {'form' : form})

# Vista de actualizar perfil
@login_required
def update_profile(request):
	profile = request.user.profile

	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES)
		if form.is_valid():
			data = form.cleaned_data
			profile.telefono = data['telefono']
			profile.biografia = data['biografia']
			profile.foto = data['foto']
			profile.save()

			return redirect('update_profile')

	else:
		form = ProfileForm()
	
	return render(request=request, template_name = 'users/update_profile.html', context = {'profile': profile, 'user':	request.user, 'form' : form})

# Vista de mostrar perfil
@login_required
def show_profile(request):
	if request.method == 'POST':
		buscador = request.POST['buscador']
		usuario = User.objects.get(username=request.POST['buscador'])

		posts = Post.objects.filter(user=usuario).count()
		profile = Post.objects.all().filter(user=usuario.id)
		followers = Follow.objects.filter(user_follow=usuario).count()
		following = Follow.objects.filter(user=usuario).count()

		return render(request, 'users/profile.html', {'user':usuario, 'profile':profile, 'posts':posts, 'followers':followers, 'following':following})
	else:
		usuario = User.objects.get(id=request.user.id)

		posts = Post.objects.filter(user=request.user).count()
		profile = Post.objects.all().filter(user=usuario)

		followers = Follow.objects.filter(user_follow=request.user).count()
		following = Follow.objects.filter(user=request.user).count()

		return render(request, 'users/profile.html', {'user':request.user, 'profile':profile, 'posts':posts, 'followers':followers, 'following':following})
		
	return render(request, 'users/profile.html')

# Vista de seguir usuario
@login_required
def follow(request):
	if request.method == 'POST':
		user = User.objects.get(pk=request.POST['id'])
		user_follow = User.objects.get(pk=request.user.id)

		contador = Follow.objects.filter(user=user_follow, user_follow=user).count()

		if contador > 0:
			eliminar = Follow.objects.get(user=user_follow, user_follow=user)
			eliminar.delete()
		else:
			Follow.objects.create(user=user_follow, user_follow=user)

		posts = Post.objects.filter(user=user).count()
		followers = Follow.objects.filter(user_follow=user).count()
		following = Follow.objects.filter(user=user).count()

		return render(request, 'users/profile.html', {'user':user, 'posts':posts, 'followers':followers, 'following':following})
		
	return render(request, 'users/profile.html')