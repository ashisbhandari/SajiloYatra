from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('login',views.login,name='login'),
    path('register_user',views.register,name='register'),
]
