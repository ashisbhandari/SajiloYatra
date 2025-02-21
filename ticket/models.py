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
        
         
class companyRegistration(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('Long Route', 'Long Routes (Night Bus)'),
        ('Short Route', 'Short Route (Local Bus)'),
        ('Reservations', 'Small (Reservation) Vehicle'),
    ]
    DISTRICT_CHOICES = [
    ("acham", "Acham"), ("arghakhanchi", "Arghakhanchi"), ("baglung", "Baglung"), ("bajhang", "Bajhang"), 
    ("bajura", "Bajura"), ("baitadi", "Baitadi"), ("banke", "Banke"), ("bardiya", "Bardiya"), ("bara", "Bara"), 
    ("bhaktapur", "Bhaktapur"), ("bhojpur", "Bhojpur"), ("chitwan", "Chitwan"), ("dadeldhura", "Dadeldhura"), 
    ("dang", "Dang"), ("dailekh", "Dailekh"), ("darchula", "Darchula"), ("dhading", "Dhading"), ("dhankuta", "Dhankuta"), 
    ("dhanusha", "Dhanusha"), ("dolakha", "Dolakha"), ("dolpa", "Dolpa"), ("doti", "Doti"), ("eastern_rukum", "Eastern Rukum"), 
    ("gulmi", "Gulmi"), ("gorkha", "Gorkha"), ("humla", "Humla"), ("ilam", "Ilam"), ("jhapa", "Jhapa"), ("jajarkot", "Jajarkot"), 
    ("jumla", "Jumla"), ("kathmandu", "Kathmandu"), ("kanchanpur", "Kanchanpur"), ("kailali", "Kailali"), ("kalikot", "Kalikot"), 
    ("kapilvastu", "Kapilvastu"), ("kaski", "Kaski"), ("khotang", "Khotang"), ("kavrepalanchok", "Kavrepalanchok"), 
    ("lalitpur", "Lalitpur"), ("lamjung", "Lamjung"), ("mahendranagar", "Mahendranagar"), ("mahottari", "Mahottari"), 
    ("makwanpur", "Makwanpur"), ("manang", "Manang"), ("morang", "Morang"), ("mugu", "Mugu"), ("myagdi", "Myagdi"), 
    ("mustang", "Mustang"), ("nawalpur", "Nawalpur"), ("east-nawalparasi", "East-Nawalparasi"), ("west-nawalparasi", "West-Nawalparasi"), 
    ("nuwakot", "Nuwakot"), ("okhaldhunga", "Okhaldhunga"), ("parbat", "Parbat"), ("parsa", "Parsa"), ("pachthar", "Pachthar"), 
    ("palpa", "Palpa"), ("pyuthan", "Pyuthan"), ("rajbiraj", "Rajbiraj"), ("rautahat", "Rautahat"), ("ramechap", "Ramechap"), 
    ("rasuwa", "Rasuwa"), ("rupandehi", "Rupandehi"), ("rolpa", "Rolpa"), ("salyan", "Salyan"), ("sankhuwasabha", "Sankhuwasabha"), 
    ("saptari", "Saptari"), ("sarlahi", "Sarlahi"), ("sindhuli", "Sindhuli"), ("sindhupalchok", "Sindhupalchok"), 
    ("siraha", "Siraha"), ("solukhumbu", "Solukhumbu"), ("sunsari", "Sunsari"), ("surkhet", "Surkhet"), ("syangja", "Syangja"), 
    ("tanahun", "Tanahun"), ("taplejung", "Taplejung"), ("terhathum", "Terhathum"), ("udayapur", "Udayapur"), ("western_rukum", "Western Rukum")
]

    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    origin = models.CharField(max_length=50,default='Unknown', choices=DISTRICT_CHOICES)
    destination = models.CharField(max_length=50,default='Unknown', choices=DISTRICT_CHOICES)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    # contact = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=15)
    passenger_capacity = models.IntegerField()
    # vehicle_type = models.CharField(max_length=30, choices=VEHICLE_TYPE_CHOICES)
    # student_image = models.ImageField(upload_to='student_documents/', blank=True, null=True)
    password = models.CharField(max_length=255)  # Store hashed passwords in real scenarios

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