"""

    URLS MAIN

"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('livro1.urls',  namespace='livro1')),
]