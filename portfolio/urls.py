from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.find_ticker, name='find_ticker'),
    path('blue-chips/', views.blue_chips, name='blue_chips'),
    path('chart/<str:ticker>/', views.stock_chart, name='stock_chart'),
    path('info/<str:ticker>/', views.stock_info, name='stock_info'), 
    path('delete/<int:position_id>/', views.delete_position, name='delete_position'),
]