from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('register_user',views.user_register,name='register'),
    path('register_company',views.company_register,name='register'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('Book_ticket',views.book_ticket,name='bookticket'),
]
