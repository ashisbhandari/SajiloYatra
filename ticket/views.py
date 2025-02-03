from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'ticket/home.html')


def login(request):
    return render(request, 'ticket/login.html')

def register(request):
    return render(request, 'ticket/signup.html')

