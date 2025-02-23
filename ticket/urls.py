from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),  # Use trailing slash here
    path('register_user/', views.user_register, name='register'),
    path('register_company/', views.company_register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('comp_dash/', views.company_dashboard, name='dashboard'),
    path('test/', views.test, name='testpage'),
    path('Book_ticket/', views.book_ticket, name='bookticket'),
    path('Reserve_vehicle/', views.reservation, name='reserve_vech'),
    path('register/', views.register_bus, name='register_bus'),
    path('cancel_ticket/', views.cancel, name='cancel_ticket'),
    # path('vehicle-history/', views.vehicle_history, name='vehicle_history'),
    # path('con/',views.contctt, name="vech_contact"),,
    # path('bus-info/', views.bus_info_dashboard, name='bus_info_dashboard'),
]
