from django.shortcuts import render

from django.http import HttpResponse

from django.db import models
# from models import User


# 
# def score(request):
#    if request.is_ajax():
#      if request.method == 'GET':
#         user = UserProfile.objects.get(id=request.GET.get('userid'))
#         user.user_name = request.GET.get('total')
#         user.save()
#         return HttpResponse("%s" % user.score )

def index(requst):
	return render(requst, 'base.html')
