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
from ticket.models import UserRegistration, companyRegistration,BookedTicket,Bus  # Import models

# Create your views here.

def home(request):
    origin = request.GET.get('from', '')
    destination = request.GET.get('to', '')

    if not origin or not destination:  # If either from or to is empty, return empty results
        page_obj = []
    else:
        # Prepare SQL query to filter bus routes based on 'from' and 'to'
        qry = """SELECT username, vehicle_number,vehicle_type, passenger_capacity, origin, destination,comp_name,contact 
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

    return render(request, 'ticket/index.html', {'page_obj': page_obj, 'origin': origin, 'destination': destination})
    # return render(request, 'ticket/index.html')

def reservation(request):
    return render(request, 'ticket/reserve_vech.html')
# url for payment
def payment(request):
    return render(request, 'ticket/payment.html')

def seat(request):
    return render(request, 'ticket/seats.html')
def seat(request, vehicle_no):
    # You can use vehicle_no to query bus/seat details from DB
    return render(request, 'ticket/seats.html', {'vehicle_no': vehicle_no})
from django.shortcuts import get_object_or_404

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
# @login_required
# def dashboard(request):
#     # Get all records from companyRegistration
#     company_data = companyRegistration.objects.all()

#     # Pagination: Show 10 records per page
#     paginator = Paginator(company_data, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Render the dashboard template and pass the paginated data
#     return render(request, 'ticket/dashboard.html', {'page_obj': page_obj})
# # @login_required


from django.db import connection
from django.core.paginator import Paginator
from django.shortcuts import render

def company_dashboard(request):
    vehicle_number = request.GET.get('vehicle_number')
    try:
        # Route data for the logged-in company
        with connection.cursor() as curs:
            curs.execute("""
                SELECT vehicle_number, username, contact, origin, vehicle_type, destination, passenger_capacity
                FROM ticket_busroute
                WHERE comp_name = %s
            """, [request.user.username])
            route_data = curs.fetchall()

        # Ticket data for the searched vehicle number
        data = []
        total_tickets = 0
        if vehicle_number:
            with connection.cursor() as c:
                c.execute("""
                    SELECT vech_no, name, phone, email, seat_no, payment, ticket_no, departure_time, paymentproof
                    FROM ticket_bookedticket
                    WHERE vech_no = %s
                """, [vehicle_number])
                data = c.fetchall()

                # Total ticket count for that vehicle
                c.execute("SELECT COUNT(ticket_no) FROM ticket_bookedticket WHERE vech_no = %s", [vehicle_number])
                total_tickets = c.fetchone()[0]

        # Pagination setup
        pageno = request.GET.get('page')
        route_paginator = Paginator(route_data, 5)
        ticket_paginator = Paginator(data, 5)
        pageobj = route_paginator.get_page(pageno)
        pageobjs = ticket_paginator.get_page(pageno)

    except Exception as ex:
        print("Error occurred:", ex)
        pageobj = []
        pageobjs = []
        total_tickets = 0

    return render(request, 'ticket/company_dash.html', {
        'page_obj': pageobj,
        'page_obj1': pageobjs,
        'total_tickets': total_tickets,
        'vehicle_number': vehicle_number
    })

def dashboard(request):
    try:
        with connection.cursor() as curs:
            curs.execute("""SELECT vehicle_number,username,contact,origin,vehicle_type,destination,passenger_capacity,departure_time FROM ticket_busroute """)
            route_data=curs.fetchall()
        paginator=Paginator(route_data,10)
        pageno=request.GET.get('page')
        pageobj=paginator.get_page(pageno)
    except Exception as ex:
        print("Error occur:",ex)
        pageobj=[]
    return render(request, 'ticket/dashboard.html',{'page_obj':pageobj})

def bus_route_info(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT vehicle_number, username, contact, vehicle_type, passenger_capacity, origin, destination,departure_time FROM company""")
            data = cursor.fetchall()

        paginator = Paginator(data, 10)  # Show 10 results per page
        page_number = request.GET.get('page')
        page_obj1 = paginator.get_page(page_number)

    except Exception as e:
        print("Error executing query:", e)
        page_obj1 = []

    return render(request, 'ticket/company_dash.html', {'page_obj': page_obj1})

#sending seats value to another page
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

def book_ticket(request):
    selected_seats = request.GET.get('seats', '').split(',') if request.GET.get('seats') else []
    year = datetime.now().year
    return render(request, 'ticket/booktkt.html', {'selected_seats': selected_seats,'year': year,})


from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .forms import BookedTicketForm
from .models import BookedTicket
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from datetime import datetime
from .forms import BookedTicketForm

def book_ticket(request):
    year = datetime.now().year
    selected_seats = request.GET.get('seats', '').split(',')
    vech_no = request.GET.get('vech_no', '')
    seat_str = request.GET.get('seats', '')  # For filling Seat_no field

    if request.method == 'POST':
        post_data = request.POST.copy()

        post_data.setdefault('vech_no', vech_no)
        post_data.setdefault('Seat_no', seat_str)

        form = BookedTicketForm(post_data, request.FILES)
        if form.is_valid():
            ticket = form.save()

            # Send email after booking
            subject = "Your Ticket Booking Confirmation - SajiloYatra"
            message = f"""
Dear {ticket.name},

Thank you for booking your ticket with SajiloYatra.

🔖 Ticket Details:
- Ticket No: {ticket.Ticket_no}
- Seat(s): {ticket.Seat_no}
- Departure Date: {ticket.departure_time}
- Vehicle No: {ticket.vech_no}
- Payment Type: {ticket.payment}

If you chose online payment, please ensure you have uploaded the payment proof.

Safe travels!
SajiloYatra Team
"""
            send_mail(
                subject,
                message,
                'photolaija@gmail.com',  # Sender 
                [ticket.email],               # Recipient
                fail_silently=False,
            )

            return redirect('/')  # Redirect after successful booking

    else:
        form = BookedTicketForm(initial={
            'vech_no': vech_no,
            'Seat_no': seat_str,
        })

    return render(request, 'ticket/booktkt.html', {
        'form': form,
        'selected_seats': selected_seats,
        'year': year,
        'vech_no': vech_no,
        'Seat_no': seat_str,
    })


def map(request):
    return render(request, 'ticket/check.html')


def register_bus(request):
    today = date.today()  # Get today's date
    if request.method == 'POST':
        form = BusRouteForm(request.POST)
        if form.is_valid():
            bus_route = form.save(commit=False)  # Don't save to DB yet
            bus_route.comp_name = request.user.username  # Assign company name
            bus_route.save()  # Now save to DB
            return redirect('/comp_dash')  # Redirect to dashboard
    else:
        form = BusRouteForm()

    return render(request, 'ticket/register_bus.html', {'form': form, 'today': today})
def search_vech(request):
     # Get user input for 'from' and 'to' cities
    origin = request.GET.get('from', '')
    destination = request.GET.get('to', '')

    if not origin or not destination:  # If either from or to is empty, return empty results
        page_obj = []
    else:
        # Prepare SQL query to filter bus routes based on 'from' and 'to'
        qry = """SELECT username, vehicle_type, passenger_capacity, origin, destination,comp_name 
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

    return render(request, 'ticket/search_vech.html', {'page_obj': page_obj, 'origin': origin, 'destination': destination})

# for sending email from fillup form of index page

from django.core.mail import send_mail
def contact(request):
    return render(request, 'ticket/main.html')
def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        comments = request.POST.get('comments')  
        subject = f'Feedback to SajiloYatra by {name }'
        message = f'''
        Name: {name}
        Contact: {contact}
        Email: {email}
        Comments: {comments}
        '''

        recipient = 'photolaija@gmail.com'  # Your admin/support email
        sender = email  # Fixed sender value

        try:
            send_mail(subject, message, sender, [recipient])
        except Exception as e:
            print(f"Error sending email: {e}")
            messages.error(request, "There was an error sending your message. Please try again later.")
            return redirect('/')

        messages.success(request, "Your message has been sent successfully!")
        return redirect('/')

    return render(request, 'ticket/main.html')


def cancel(request):
    try:
        with connection.cursor() as curs:
            curs.execute("""SELECT vech_no,name,phone,email,seat_no,payment,ticket_no, departure_time,paymentproof FROM ticket_bookedticket """)
            route_data=curs.fetchall()
        paginator=Paginator(route_data,10)
        pageno=request.GET.get('page')
        pageobj=paginator.get_page(pageno)
    except Exception as ex:
        print("Error occur:",ex)
        pageobj=[]
    return render(request,'ticket/cancel_ticket.html',{'page_obj':pageobj})