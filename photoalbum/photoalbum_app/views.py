from django.shortcuts import render
from .models import Category, Photo
from django.http import HttpResponse
# Create your views here.


def main(request):
    category = Category.objects.all()
    photos = Photo.objects.all()
    context = {'categories': category, 'photos': photos}
    return render(request, 'photoalbum_app/index.html', context)


def add_photo(request):
    return render(request, 'photoalbum_app/add.html')


def view_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photoalbum_app/photo.html', {'photo': photo})
