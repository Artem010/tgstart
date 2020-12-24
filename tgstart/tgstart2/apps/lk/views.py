from django.shortcuts import render

from django.http import HttpResponse

from django.db import models

from users.models import User



def dashboard(request):
    allUsers = list(User.objects.all())
    cUser = {'first_name': 'ARTEM', 'last_name':'IPATOV'}
    # print (allUsers[0])
    print (cUser)
    return render(request, 'volt/dashboard.html', cUser)
