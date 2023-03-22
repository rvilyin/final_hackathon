from django.urls import path

from . import views

urlpatterns = [
    path('chat/', views.index, name='index'),
    path('<str:room_name>/create/', views.myroom, name='myroom'),
    path('<str:room_name>/', views.room, name='room'),
]