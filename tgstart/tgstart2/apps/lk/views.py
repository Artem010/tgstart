from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

import os
import subprocess
import shutil
import datetime
import json
import signal
import requests

from django.db import models
from users.models import User

# *****custom Def******

def updStat(botID,userID, count):
    cUser = User.objects.get(id = userID)
    cBot = cUser.bot_set.get(id = botID)

    now = datetime.datetime.now()
    cDate = now.strftime("%d-%m-%Y")

    if ((cBot.messages_set.filter(date = cDate)).exists()):
        cBot.messages_set.filter(date =cDate).update(count = count)
        print('UPD')
    else:
        cBot.messages_set.create(date =cDate, count = count)
        print('create')

    return cBot.messages_set.filter(bot_name_id = botID)

def check_auth(request):
    sessionUserId=request.session.get('sUserId')
    if sessionUserId == None:
        return redirect('/')

    sUserId = sessionUserId
    uData = User.objects.filter(id = sUserId)
    return {'sUserId':request.session.get('sUserId'), 'uData':uData[0]}

# def getCurrentBotByGET():
#     cUser = User.objects.get(id = request.session.get('sUserId'))
#     cBotId =request.GET['id']
#     cBot = cUser.bot_set.get(id = cBotId)


# *****custom Def******


def removebot(request):
    deactivatebot(request)
    cUser = User.objects.get(id = request.session.get('sUserId'))
    cBotId =request.GET['id']
    cBot = cUser.bot_set.get(id = cBotId)

    cBot.delete();
    path = os.getcwd() + '/tgstart2/bots/' + str( request.session.get('sUserId')) + "/"+cBotId
    shutil.rmtree(path)
    print("*******del bot*******")
    return redirect('/mybots')

def activatebot(request):
    cUser = User.objects.get(id = request.session.get('sUserId'))
    cBotId =request.GET['id']
    cBot = cUser.bot_set.get(id = cBotId)

    cDir = os.getcwd() + '/tgstart2/bots/' + str( request.session.get('sUserId')) + "/"+str(cBotId)
    pr = subprocess.Popen(['python', cDir +'/main.py'])
    cUser.bot_set.filter(id=cBotId).update(pID = pr.pid, status = 1)
    print("*******Activated bot*******")
    return redirect('/mybots')

def deactivatebot(request):
    cUser = User.objects.get(id = request.session.get('sUserId'))
    cBotId =request.GET['id']
    cBot = cUser.bot_set.get(id = cBotId)
    print(cBot.pID)
    os.kill(cBot.pID, signal.SIGTERM)
    cUser.bot_set.filter(id = cBotId).update(pID = 0, status = 0)
    print("*******deactivated bot*******")
    return redirect('/mybots')

def dashboard(request):

    cUser = User.objects.get(id = request.session.get('sUserId'))
    print((cUser.bot_set.all()).count())
    if((cUser.bot_set.all()).count() > 0):
        cBotId =str((cUser.bot_set.all())[(cUser.bot_set.all()).count()-1].id)
        cDir = os.getcwd() + '/tgstart2/bots/' + str( request.session.get('sUserId')) + "/"+cBotId
        with open(cDir+"/stat.json", "r") as read_file:
            data = json.load(read_file)
        count = int(data['msgs'])
        dataChart = updStat(cBotId, request.session.get('sUserId'), count)
    else:
        dataChart = '0'

    return render(request, 'volt/dashboard.html', {'dataChart': dataChart, 'auth':check_auth(request)})

def mybots(request):


    if request.method == "POST":
#assigning a option(template) to a bot
        cUser = User.objects.get(id = request.session.get('sUserId'))
        if not (cUser.bot_set.filter(token=request.POST.get('tgToken')).exists()):

            requestAPI = requests.get('https://api.telegram.org/bot'+request.POST.get('tgToken')+'/getMe')
            parsed_string = json.loads(requestAPI.content)
            if (parsed_string['ok']):
                cBotFirstName = parsed_string['result']['first_name']
                cBotGlobalId = parsed_string['result']['id']
                cBotUsername = parsed_string['result']['username']
            else:
                cBotFirstName= 'none'
                cBotGlobalId= 'none'
                cBotUsername= 'none'
            print(cBotFirstName)

            cUser.bot_set.create(option = request.POST.get('exampleRadios'), token = request.POST.get('tgToken'), bot_name = cBotFirstName, global_id= cBotGlobalId, bot_username =cBotUsername )
            cBotId =str((cUser.bot_set.all())[(cUser.bot_set.all()).count()-1].id)
            cBot = cUser.bot_set.get(id = cBotId)
            now = datetime.datetime.now()
            startDate = now.strftime("%d-%m-%Y")


            cBot.messages_set.create(count = 0, date =startDate)



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
            text_config = open(cDir + sUserId + "/" + cBotId +"/stat.json", "w")
            text_config.write('{"msgs": 0,"users": []}')
            shutil.copyfile(cDir + "main.py", cDir + sUserId + "/" + cBotId +"/main.py")


            pr = subprocess.Popen(['python', cDir + sUserId + "/" + cBotId +'/main.py'])
            # pr = subprocess.Popen(['python3', cDir + sUserId + "/" + cBotId +'/main.py'])
            cUser.bot_set.filter(id=cBotId).update(pID = pr.pid)


    cUser = User.objects.get(id = request.session.get('sUserId'))


    return render(request, 'volt/mybots.html', {'bots':cUser.bot_set.all().order_by('-id'), 'auth': check_auth(request)})

def pay(request):
    return render(request, 'volt/pay.html', check_auth(request))

def senders(request):
    return render(request, 'volt/senders.html', check_auth(request))

def users(request):
    cUser = User.objects.get(id = request.session.get('sUserId'))
    print((cUser.bot_set.all()).count())
    if((cUser.bot_set.all()).count() > 0):
        cBotId =str((cUser.bot_set.all())[(cUser.bot_set.all()).count()-1].id)
        cBot = cUser.bot_set.get(id = cBotId)
        cBotToken = cBot.token
        cDir = os.getcwd() + '/tgstart2/bots/' + str( request.session.get('sUserId')) + "/"+cBotId
        with open(cDir+"/stat.json", "r") as read_file:
            data = json.load(read_file)

        data = data['users']
        for u in data:
            print(u)
            if (not cBot.botuser_set.filter(tg_id = u['tg_id']).exists()):
                cBot.botuser_set.create(username = u['username'], first_name =  u['first_name'],last_name =  u['last_name'],tg_id =  u['tg_id'], pathAvatar =u['pathAvatar'] )
        print(data)
        usersData = cBot.botuser_set.all()
    else:
        usersData = 0;
        cBotToken = 0;

    #     dataChart = updStat(cBotId, request.session.get('sUserId'), count)
    # else:
    #     dataChart = '0'

    return render(request, 'volt/users.html', {'usersData':usersData, 'tgToken':cBotToken, 'auth': check_auth(request)})
def profile(request):

    if request.method == "POST":
        cUser = User.objects.get(id=request.session.get('sUserId'))
        cUser.user_lastname = request.POST.get('last_name')
        cUser.user_email = request.POST.get('user_email')
        cUser.save()

    return render(request, 'volt/profile.html', check_auth(request))
