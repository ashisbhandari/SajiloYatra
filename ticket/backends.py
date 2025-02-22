from django.contrib.auth.backends import BaseBackend
from ticket.models import UserRegistration, companyRegistration  # Make sure to use companyRegistration

class MultiUserAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check in UserRegistration table (Users)
        try:
            user = UserRegistration.objects.get(username=username, password=password)  # Plain text check
            return user  # Return the user object if found
        except UserRegistration.DoesNotExist:
            pass  # If not found, continue to check the company table

        # Check in companyRegistration table (Companies)
        try:
            company_user = companyRegistration.objects.get(username=username, password=password)  # Plain text check
            return company_user  # Return the company object if found
        except companyRegistration.DoesNotExist:
            return None  # If not found in both tables, return None

        return None  # If authentication fails

    def get_user(self, user_id):
        # Get user from either table
        try:
            return UserRegistration.objects.get(pk=user_id)
        except UserRegistration.DoesNotExist:
            try:
                return companyRegistration.objects.get(pk=user_id)
            except companyRegistration.DoesNotExist:
                return None
