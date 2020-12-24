from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
def index(request):
    return render(request, 'volt/index.html')


def logout(request):
    del request.session['sUserId']
    print("*******del session*******")
    return redirect('/')
