from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Ensures the password is hashed
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class UserRegistration(AbstractBaseUser, PermissionsMixin):
    PASSENGER_TYPE_CHOICES = [
        ('children', 'Children (0-10)'),
        ('adult', 'Adult'),
        ('old', 'Elder (50+)'),
        ('students', 'Students'),
    ]
    
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    passenger_type = models.CharField(max_length=10, choices=PASSENGER_TYPE_CHOICES)
    student_image = models.ImageField(upload_to='student_documents/', blank=True, null=True)
    password = models.CharField(max_length=255)  # Stored hashed, not plain text

    # Required fields for Django's default auth system
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # This can be set to True for admin users
    last_login = models.DateTimeField(auto_now=True)

    # Custom reverse relationships
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='user_registration_set', 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='user_registration_set', 
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username  # Return username instead of company_name
    
    class Meta:
        db_table = 'user_registration'
        

class companyRegistration(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('Long Route', 'Long Routes (Night Bus)'),
        ('Short Route', 'Short Route (Local Bus)'),
        ('Reservations', 'Small (Reservation) Vehicle'),
    ]
    DISTRICT_CHOICES = [
        ("acham", "Acham"), ("arghakhanchi", "Arghakhanchi"), ("baglung", "Baglung"), ("bajhang", "Bajhang"),
        # Add all your other district choices here...
    ]
    
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    origin = models.CharField(max_length=50, default='Unknown', choices=DISTRICT_CHOICES)
    destination = models.CharField(max_length=50, default='Unknown', choices=DISTRICT_CHOICES)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=15)
    passenger_capacity = models.IntegerField()
    password = models.CharField(max_length=255)  # Store hashed passwords in real scenarios
    # Required fields for Django's default auth system
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # This can be set to True for admin users
    last_login = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'company'


class BusRoute(models.Model):
    vehicle_number = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    origin = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50)
    destination = models.CharField(max_length=100)
    passenger_capacity = models.IntegerField()

    def __str__(self):
        return f"{self.vehicle_number} - {self.origin} to {self.destination}"
