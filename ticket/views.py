from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'ticket/home.html')


def login(request):
    return render(request, 'ticket/login.html')

def user_register(request):
    return render(request, 'ticket/user_signup.html')

def company_register(request):
    return render(request, 'ticket/company_signup.html')


def dashboard(request):
    return render(request, 'ticket/dashboard.html')

def book_ticket(request):
    return render(request,'ticket/booktkt.html')
