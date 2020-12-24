from django.shortcuts import render

# Create your views here.
from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import include
# import urls

urlpatterns = [
	# path('', views.index, name = 'index'),
	# path('dashboard', views.dashboard, name = 'dashboard')
	path('dashboard/', views.dashboard, name = 'dashboard'),
	path('profile/', views.profile, name = 'profile')
]
