from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),  # Use trailing slash here
    path('register_user/', views.user_register, name='register'),
    path('register_company/', views.company_register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('test/', views.test, name='testpage'),
    path('Book_ticket/', views.book_ticket, name='bookticket'),
    # path('con/',views.contctt, name="vech_contact"),
    # path('bus-info/', views.bus_info_dashboard, name='bus_info_dashboard'),
]
