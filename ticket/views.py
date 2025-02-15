from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import SignupForm,companyEntry
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging
from django.db import connection
from django.contrib.auth.models import User
from .models import companyRegistration
from django.core.paginator import Paginator


# Create your views here.

def home(request):
    return render(request, 'ticket/index.html')
def test(request):
    return render(request, 'ticket/hi.html')


logger = logging.getLogger(__name__)

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            # Print executed SQL queries to check the database
            for query in connection.queries:
                print(query)

            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    else:
        return render(request, 'ticket/login.html')

def user_register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')  # Redirect after successful form submission
        else:
            # Print form errors for debugging
            print(form.errors)
            messages.error(request, "There was an error with your form submission. Please try again.")
    else:
        form = SignupForm()
    return render(request, 'ticket/user_signup.html', {'form': form})

def company_register(request):
    if request.method == 'POST':
        form = companyEntry(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')  # Redirect after successful form submission
        else:
            # Print form errors for debugging
            print(form.errors)
            messages.error(request, "There was an error with your form submission. Please try again.")
    else:
        form = companyEntry()
    return render(request, 'ticket/company_signup.html', {'form': form})
def dashboard(request):
    # Get all records from companyRegistration
    company_data = companyRegistration.objects.all()

    # Pagination: Show 10 records per page
    paginator = Paginator(company_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the dashboard template and pass the paginated data
    return render(request, 'ticket/dashboard.html', {'page_obj': page_obj})
def book_ticket(request):
    return render(request,'ticket/booktkt.html')

def bus_info_dashboard(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT vehicle_number, username, contact, vehicle_type, passenger_capacity, origin, destination FROM company""")
            data = cursor.fetchall()

        paginator = Paginator(data, 10)  # Show 10 results per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except Exception as e:
        print("Error executing query:", e)
        page_obj = []

    return render(request, 'ticket/dashboard.html', {'page_obj': page_obj})