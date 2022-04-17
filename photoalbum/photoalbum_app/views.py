from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
# Create your views here.


def main(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)

    categories = Category.objects.all()
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photoalbum_app/index.html', context)


def add_photo(request):
    category = Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                name=data['category_new'])
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


def view_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photoalbum_app/photo.html', {'photo': photo})


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main_page')
    return render(request, 'photoalbum_app/login.html')


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'photoalbum_app/register.html', context)