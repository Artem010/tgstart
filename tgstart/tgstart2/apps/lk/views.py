from django.shortcuts import render

from django.http import HttpResponse

from django.db import models



def index(request):
    return render(request, 'volt/index.html')
