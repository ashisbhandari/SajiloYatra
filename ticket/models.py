from django.db import models

class UserRegistration(models.Model):
    PASSENGER_TYPE_CHOICES = [
        ('children', 'Children (0-10)'),
        ('adult', 'Adult'),
        ('old', 'Elder (50+)'),
        ('students', 'Students'),
    ]

    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    passenger_type = models.CharField(max_length=10, choices=PASSENGER_TYPE_CHOICES)
    student_image = models.ImageField(upload_to='student_documents/', blank=True, null=True)
    password = models.CharField(max_length=255)  # Store hashed passwords in real scenarios

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'user_registration'  