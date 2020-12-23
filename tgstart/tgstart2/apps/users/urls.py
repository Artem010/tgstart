from django.shortcuts import render

# Create your views here.
from django.urls import path

from . import views


from django.urls import include
# import urls

urlpatterns = [
	path('', views.index, name = 'index')
]
