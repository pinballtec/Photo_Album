from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main_page'),
    path('add/', views.add_photo, name='add_photo'),
    path('view/<int:pk>', views.view_photo, name='view_photo'),
]