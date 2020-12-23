from django.urls import path

from . import views


# from django.conf.urls import include, url
# from django.contrib import admin

from django.urls import include
# import urls

urlpatterns = [
	# url(r'/poll/score/$', 'user_name', name='user_name'),
	path('', views.index, name = 'index')
]
