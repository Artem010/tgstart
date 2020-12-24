from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from django.db import models

from users.models import User


def check_auth(request):
    sessionUserId=request.session.get('sUserId')
    if sessionUserId == None:
        return redirect('/')

    sUserId = sessionUserId
    uData = User.objects.filter(id_user = sUserId)

    return {'sUserId':request.session.get('sUserId'), 'uData':uData[0]}

def dashboard(request):
    return render(request, 'volt/dashboard.html', check_auth(request))

def profile(request):

    print(request.POST.get('last_name'))
    print(request.POST.get('user_email'))

    

    return render(request, 'volt/profile.html', check_auth(request))
