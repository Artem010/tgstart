from django.shortcuts import render
from django.shortcuts import redirect
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

        # currentUser =

        currentUser = User.objects.filter(id_user=form.cleaned_data.get("id_user")).exists()
        if not currentUser:
            username= form.cleaned_data.get("username")
            first_name= form.cleaned_data.get("first_name")
            last_name= form.cleaned_data.get("last_name")
            id_user= form.cleaned_data.get("id_user")
            a = User(user_name = username, user_firstname=first_name, user_lastname=last_name, id_user =id_user)
            a.save()
        request.session['sUserId'] = form.cleaned_data.get("id_user")
        return redirect('/dashboard')



        print("REDIRECT")
        # if(currentUser):
        #     username= form.cleaned_data.get("username")
        #     first_name= form.cleaned_data.get("first_name")
        #     last_name= form.cleaned_data.get("last_name")
        #     id_user= form.cleaned_data.get("id_user")
        #     a = User(user_name = username, user_firstname=first_name,user_lastname=last_name, id_user =id_user)
        #     a.save()
        # else:
        #     username = "Такой пользователь уже существует!"
    # allUsers = User.objects.values_list('user_name')
    allUsers = list(User.objects.all())


    context= {'allUsers': allUsers, 'form': form, 'username': username, 'first_name': first_name, 'last_name': last_name, 'submitbutton': submitbutton}

    return render(request, 'users/auth.html', context)
