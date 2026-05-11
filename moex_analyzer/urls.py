from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portfolio/', include(('portfolio.urls', 'portfolio'), namespace='portfolio')),
    path('training/', include('training.urls')),
]