from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
# Create your views here.
from django.contrib.auth.decorators import login_required


@login_required(login_url=login)
def main(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photoalbum_app/index.html', context)


@login_required(login_url=login)
def add_photo(request):
    user = request.user
    category = Category.objects.filter(user=user)
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(user=user, name=data['category_new'])
        else:
            category = None
        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image,
        )
        return redirect('main_page')

    context = {'categories': category}
    return render(request, 'photoalbum_app/add.html', context)


@login_required(login_url=login)
def view_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photoalbum_app/photo.html', {'photo': photo})


def login_page(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
    return render(request, 'photoalbum_app/login.html', {'page': page})


def logout_page(request):
    logout(request)
    return redirect('login')


def register(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            if user is not None:
                login(request, user)
                return redirect('main_page')
    context = {'form': form}
    return render(request, 'photoalbum_app/login.html', context)