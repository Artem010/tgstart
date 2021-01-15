from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

import os
import subprocess
import shutil
import datetime

from django.db import models
from users.models import User


def updStat(botID,userID, count):
    cUser = User.objects.get(id = userID)
    cBot = cUser.bot_set.get(id = botID)

    now = datetime.datetime.now()
    startDate = now.strftime("%d-%m-%Y")

    cBot.messages_set.filter(date =startDate).update(count = count)
    # cBot.messages_set.create(date ='10-01-2021', count = 11)


    return cBot.messages_set.filter(bot_name_id = botID)

def check_auth(request):
    sessionUserId=request.session.get('sUserId')
    if sessionUserId == None:
        return redirect('/')

    sUserId = sessionUserId
    uData = User.objects.filter(id = sUserId)
    return {'sUserId':request.session.get('sUserId'), 'uData':uData[0]}

def removebot(request):
    cUser = User.objects.get(id = request.session.get('sUserId'))
    cBotId =request.GET['id']
    cBot = cUser.bot_set.get(id = cBotId)
    cBot.delete();
    path = os.getcwd() + '/tgstart2/bots/' + str( request.session.get('sUserId')) + "/"+cBotId
    shutil.rmtree(path)
    print("*******del bot*******")
    return redirect('/mybots')

def dashboard(request):

    cUser = User.objects.get(id = request.session.get('sUserId'))
    print((cUser.bot_set.all()).count())
    if((cUser.bot_set.all()).count() > 0):
        cBotId =str((cUser.bot_set.all())[(cUser.bot_set.all()).count()-1].id)
        # updStat()
        cDir = os.getcwd() + '/tgstart2/bots/' + str( request.session.get('sUserId')) + "/"+cBotId+"/stat.py"
        f = open(cDir)
        count = f.read()
        dataChart = updStat(cBotId, request.session.get('sUserId'), count)
    else:
        dataChart = '0'

    return render(request, 'volt/dashboard.html', {'dataChart': dataChart, 'auth':check_auth(request)})

def mybots(request):


    if request.method == "POST":
#assigning a option(template) to a bot
        cUser = User.objects.get(id = request.session.get('sUserId'))
        cUser.bot_set.create(option = request.POST.get('exampleRadios'), token = request.POST.get('tgToken'))
        cBotId =str((cUser.bot_set.all())[(cUser.bot_set.all()).count()-1].id)

        cBot = cUser.bot_set.get(id = cBotId)

        now = datetime.datetime.now()
        startDate = now.strftime("%d-%m-%Y")

        cBot.messages_set.create(count = 0, date =startDate )


#Creating a directory for a user's bot
        sUserId = str(request.session.get('sUserId'))
        cDir = os.getcwd() + '/tgstart2/bots/'
        if not os.path.isdir(cDir +sUserId):
            os.mkdir(cDir + sUserId)
        if not os.path.isdir(cDir +  sUserId + "/" + cBotId):
            os.mkdir(cDir + sUserId + "/" + cBotId)


        text_config = open(cDir + sUserId + "/" + cBotId +"/config.py", "w")
        text_config.write("token = '" + request.POST.get('tgToken')+ "'\n")
        text_config.write("user_id = '" + sUserId+ "'\n")
        text_config.write("bot_id = '" + cBotId+ "'\n")
        text_config = open(cDir + sUserId + "/" + cBotId +"/stat.py", "w")
        text_config.write("0")
        shutil.copyfile(cDir + "main.py", cDir + sUserId + "/" + cBotId +"/main.py")

        # print((cUser.bot_set.all())[0].id)

        subprocess.Popen(['python', cDir + sUserId + "/" + cBotId +'/main.py'])
        # subprocess.Popen(['python3', cDir + sUserId + "/" + cBotId +'/main.py'])

    cUser = User.objects.get(id = request.session.get('sUserId'))
# Кол-во ботов юзера
    print(cUser.bot_set.all().count())

    now = datetime.datetime.now()
    startDate = now.strftime("%d-%m-%Y")
    print (startDate)


    return render(request, 'volt/mybots.html', {'bots':cUser.bot_set.all().order_by('-id'), 'auth': check_auth(request)})

def pay(request):
    return render(request, 'volt/pay.html', check_auth(request))

def senders(request):
    return render(request, 'volt/senders.html', check_auth(request))

def users(request):
    return render(request, 'volt/users.html', check_auth(request))

def profile(request):

    if request.method == "POST":
        cUser = User.objects.get(id=request.session.get('sUserId'))
        cUser.user_lastname = request.POST.get('last_name')
        cUser.user_email = request.POST.get('user_email')
        cUser.save()

    return render(request, 'volt/profile.html', check_auth(request))
