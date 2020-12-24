from django.shortcuts import render

from django.http import HttpResponse

from django.db import models

from users.models import User



def dashboard(request):
    cUser = {'first_name': 'ARTEM', 'last_name':'IPATOV'}


    if request.session.get('sUserId') != None:
        context = {'sUserId': request.session.get('sUserId')}

    sUserId = context['sUserId']
    uData = User.objects.filter(id_user = sUserId)

    for a in uData:
        print(a.user_firstname)

    # context.add(uData)


    print(context)

    # print (allUsers[0])
    # print (cUser)
    return render(request, 'volt/dashboard.html', {'sUserId':request.session.get('sUserId'), 'uData':uData})
