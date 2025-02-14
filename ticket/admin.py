from django.contrib import admin
from .models import UserRegistration, companyRegistration

admin.site.register(UserRegistration)
admin.site.register(companyRegistration)
