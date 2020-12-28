from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

import os
import  subprocess
import shutil


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

def mybots(request):

    if request.method == "POST":

        sUserId =  request.session.get('sUserId')
        cDir = os.getcwd()
        if not os.path.isdir(cDir + '/tgstart2/bots/' + sUserId):

            os.mkdir(cDir + '/tgstart2/bots/' + sUserId)

            text_config = open(cDir + "/tgstart2/bots/"+ sUserId +"/config.py", "w")
            text_config.write("token = '" + request.POST.get('tgToken')+ "'")

            shutil.copyfile(cDir + "/tgstart2/bots/main.py", cDir + "/tgstart2/bots/"+ sUserId +"/main.py")



        subprocess.Popen(['python3', cDir + '/tgstart2/bots/'+ sUserId +'/main.py'])

    return render(request, 'volt/mybots.html', check_auth(request))

def pay(request):
    return render(request, 'volt/pay.html', check_auth(request))

def senders(request):
    return render(request, 'volt/senders.html', check_auth(request))

def users(request):
    return render(request, 'volt/users.html', check_auth(request))

def profile(request):

    if request.method == "POST":
        # print(request.POST.get('last_name'))
        # print(request.POST.get('user_email'))

        cUser = User.objects.get(id_user=request.session.get('sUserId'))
        cUser.user_lastname = request.POST.get('last_name')
        cUser.user_email = request.POST.get('user_email')
        cUser.save()

    return render(request, 'volt/profile.html', check_auth(request))
