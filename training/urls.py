from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('lesson1/', views.lesson1, name='lesson1'),
]