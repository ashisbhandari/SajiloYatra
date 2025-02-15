from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.db import connection

UserModel = get_user_model()

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        user_data = None
        
        with connection.cursor() as cursor:
            # Check in user_registration table
            cursor.execute("SELECT id, username, password FROM user_registration WHERE username = %s", [username])
            user_data = cursor.fetchone()

            # If not found, check in company table
            if not user_data:
                cursor.execute("SELECT id, username, password FROM company WHERE username = %s", [username])
                user_data = cursor.fetchone()
        if user_data:
            user_id, db_username, db_password = user_data
        if db_password == password:
            # Try to get or create a Django user object
            user, created = UserModel.objects.get_or_create(username=db_username, defaults={"id": user_id})
            return user
        
        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None