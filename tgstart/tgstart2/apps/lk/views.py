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
    uData = User.objects.filter(id = sUserId)
    return {'sUserId':request.session.get('sUserId'), 'uData':uData[0]}

def dashboard(request):
    return render(request, 'volt/dashboard.html', check_auth(request))

def mybots(request):


    if request.method == "POST":
#assigning a option(template) to a bot
        cUser = User.objects.get(id = request.session.get('sUserId'))
        cUser.bot_set.create(option = request.POST.get('exampleRadios'))
        cBotId =str((cUser.bot_set.all())[(cUser.bot_set.all()).count()-1].id)

#Creating a directory for a user's bot
        sUserId = str(request.session.get('sUserId'))
        cDir = os.getcwd() + '/tgstart2/bots/'
        if not os.path.isdir(cDir +sUserId):
            os.mkdir(cDir + sUserId)
        if not os.path.isdir(cDir +  sUserId + "/" + cBotId):
            os.mkdir(cDir + sUserId + "/" + cBotId)


        text_config = open(cDir + sUserId + "/" + cBotId +"/config.py", "w")
        text_config.write("token = '" + request.POST.get('tgToken')+ "'")
        shutil.copyfile(cDir + "main.py", cDir + sUserId + "/" + cBotId +"/main.py")

        print((cUser.bot_set.all())[0].id)


        subprocess.Popen(['python3', cDir + sUserId +'/main.py'])

    return render(request, 'volt/mybots.html', check_auth(request))

def pay(request):
    return render(request, 'volt/pay.html', check_auth(request))

def senders(request):
    return render(request, 'volt/senders.html', check_auth(request))

def users(request):
    return render(request, 'volt/users.html', check_auth(request))

def profile(request):

    if request.method == "POST":
        cUser = User.objects.get(tg_id=request.session.get('sUserId'))
        cUser.user_lastname = request.POST.get('last_name')
        cUser.user_email = request.POST.get('user_email')
        cUser.save()

    return render(request, 'volt/profile.html', check_auth(request))
