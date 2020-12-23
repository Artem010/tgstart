from django.shortcuts import render

from django.http import HttpResponse

from django.db import models

from users.models import User

from django import forms

class UserForm(forms.Form):
    username= forms.CharField(max_length=100)
    first_name= forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    id_user = forms.CharField(max_length=100)


def index(request):
    submitbutton= request.POST.get("submit")

    username=''
    first_name=''
    last_name=''
    id_user=''

    form= UserForm(request.POST or None)
    if form.is_valid():
        username= form.cleaned_data.get("username")
        first_name= form.cleaned_data.get("first_name")
        last_name= form.cleaned_data.get("last_name")
        id_user= form.cleaned_data.get("id_user")
        a = User(user_name = username, user_firstname=first_name,user_lastname=last_name, id_user =id_user)
        a.save()
        print(username)
        print('done!!!!')

    context= {'form': form, 'username': username, 'first_name': first_name, 'last_name': last_name, 'submitbutton': submitbutton}

    return render(request, 'base.html', context)
