from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def main(request):
    return render(request, 'photoalbum_app/index.html')


def add_photo(request):
    return render(request, 'photoalbum_app/add.html')


def view_photo(request, pk):
    return render(request, 'photoalbum_app/photo.html')
