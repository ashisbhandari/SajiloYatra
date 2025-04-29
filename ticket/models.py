from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import pytz
from django.utils import timezone

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
    nepal_tz = pytz.timezone('Asia/Kathmandu')
    nepal_time = timezone.now().astimezone(nepal_tz)
    vehicle_number = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    origin = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50)
    destination = models.CharField(max_length=100)
    passenger_capacity = models.IntegerField()
    comp_name = models.CharField(max_length=100)
    departure_time = models.DateTimeField(default=nepal_time)
    def __str__(self):
        return f"{self.vehicle_number} - {self.origin} to {self.destination}"
    def save(self, *args, **kwargs):
        # If comp_name is not set, assign the logged-in company's name
        if not self.comp_name and hasattr(self, 'request'):
            self.comp_name = self.request.user.username  # Assuming username stores the company name
        super().save(*args, **kwargs)
        
class Bus(models.Model):
    bus_id=5
    number = models.CharField(max_length=100, unique=True)
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='buses')
    total_seats = models.PositiveIntegerField(default=30)
    
    def __str__(self):
        return f"{self.number} ({self.route})"

class BookedTicket(models.Model):
    PAYMENT_TYPE = [
        ('Cash on counter', 'Cash on counter'),
        ('online payment', 'online payment'),
    ]

    payment = models.CharField(max_length=50, choices=PAYMENT_TYPE)
    name = models.CharField(max_length=100)
    email = models.EmailField()  # Removed unique=True to allow multiple bookings with same email
    phone = models.CharField(max_length=15)
    comments = models.CharField(max_length=500, blank=True, null=True)
    departure_time = models.DateField()
    vech_no = models.CharField(max_length=20)
    paymentproof = models.ImageField(
        upload_to='payment_proofs/',  # Optional: change folder name as needed
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'ticket_bookedticket'

    def __str__(self):
        return f"{self.name} - {self.departure_time}"