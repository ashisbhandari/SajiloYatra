from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import SignupForm,companyEntry,BusRouteForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging,json
from django.http import JsonResponse

from django.db import connection
from django.contrib.auth.models import User
from .models import companyRegistration,BusRoute
from django.core.paginator import Paginator
from datetime import date,datetime
from ticket.models import UserRegistration, companyRegistration  # Import models

# Create your views here.

def home(request):
    return render(request, 'ticket/index.html')

def reservation(request):
    return render(request, 'ticket/reserve_vech.html')
def cancel(request):
    return render(request, 'ticket/cancel_ticket.html')
def seat(request):
    return render(request, 'ticket/seats.html')


logger = logging.getLogger(__name__)

# If you are returning a datetime in a response:
def custom_datetime_serialization(data):
    if isinstance(data, datetime):
        return data.isoformat()  # Convert datetime to a string
    raise TypeError("Type not serializable")


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            # Convert last_login to ISO format before storing it in session
            request.session['last_login'] = user.last_login.isoformat()  # Store as string
            request.session['username'] = user.username  #storing username in session
            if isinstance(user, UserRegistration):  # Correct the model name here
                return redirect('/dashboard')  # Redirect as a user
            # request.session['username'] = user.username  #storing username in session
            elif isinstance(user, companyRegistration):  # Correct the model name here
                return redirect('/comp_dash')  # Redirect as a company
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/login')
    return render(request, 'ticket/login.html')            
    #         # Print executed SQL queries to check the database
    #         for query in connection.queries:
    #             print(query)

    #         return redirect('dashboard')
    #     else:
    #         messages.error(request, "Invalid username or password.")
    #         return redirect('login')
    # else:
    #     return render(request, 'ticket/login.html')

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
@login_required
def dashboard(request):
    # Get all records from companyRegistration
    company_data = companyRegistration.objects.all()

    # Pagination: Show 10 records per page
    paginator = Paginator(company_data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the dashboard template and pass the paginated data
    return render(request, 'ticket/dashboard.html', {'page_obj': page_obj})
# @login_required
def company_dashboard(request):
    try:
        with connection.cursor() as curs:
            curs.execute("""SELECT vehicle_number,username,contact,origin,vehicle_type,destination,passenger_capacity,departure_date FROM ticket_busroute WHERE username = %s""",[request.user.username])
            route_data=curs.fetchall()
        paginator=Paginator(route_data,5)
        pageno=request.GET.get('page')
        pageobj=paginator.get_page(pageno)
    except Exception as ex:
        print("Error occur:",ex)
        pageobj=[]
    return render(request, 'ticket/company_dash.html',{'page_obj':pageobj})


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

def bus_route_info(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT vehicle_number, username, contact, vehicle_type, passenger_capacity, origin, destination FROM company""")
            data = cursor.fetchall()

        paginator = Paginator(data, 10)  # Show 10 results per page
        page_number = request.GET.get('page')
        page_obj1 = paginator.get_page(page_number)

    except Exception as e:
        print("Error executing query:", e)
        page_obj1 = []

    return render(request, 'ticket/company_dash.html', {'page_obj': page_obj1})

#sending seats value to another page
def book_ticket(request):
    selected_seats = request.GET.get('seats', '').split(',') if request.GET.get('seats') else []
    return render(request, 'ticket/booktkt.html', {'selected_seats': selected_seats})


def register_bus(request):
    today = date.today()  # Get today's date
    if request.method == 'POST':
        form = BusRouteForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('/comp_dash')  # Redirect to the vehicle travel history page
    else:
        form = BusRouteForm()

    return render(request, 'ticket/register_bus.html', {'form': form, 'today': today})


def test(request):
     # Get user input for 'from' and 'to' cities
    origin = request.GET.get('from', '')
    destination = request.GET.get('to', '')

    if not origin or not destination:  # If either from or to is empty, return empty results
        page_obj = []
    else:
        # Prepare SQL query to filter bus routes based on 'from' and 'to'
        qry = """SELECT username, vehicle_type, passenger_capacity, origin, destination 
                 FROM ticket_busroute 
                 WHERE origin LIKE %s AND destination LIKE %s"""
        
        # Parameters to prevent SQL injection
        params = [f"%{origin}%", f"%{destination}%"]

        try:
            with connection.cursor() as cur:
                cur.execute(qry, params)
                route_data = cur.fetchall()

                # Paginate the results
                paginator = Paginator(route_data, 5)
                page_no = request.GET.get('page')
                page_obj = paginator.get_page(page_no)

        except Exception as ex:
            print("Error occurred:", ex)
            page_obj = []

    return render(request, 'ticket/hi.html', {'page_obj': page_obj, 'origin': origin, 'destination': destination})