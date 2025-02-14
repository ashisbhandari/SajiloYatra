from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db import connection
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, username, password FROM user_registration WHERE username = %s", [username])
            user_data = cursor.fetchone()
        
        if user_data:
            user_id, db_username, db_password = user_data
            
            # If passwords match (You should hash passwords in the database)
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
