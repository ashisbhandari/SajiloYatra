from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password  # Import for password hashing
from .models import UserRegistration,companyRegistration,BusRoute,BookedTicket

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, label="Your Name", widget=forms.TextInput(attrs={'placeholder': 'Enter your company name'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    contact = forms.CharField(max_length=15, label="Contact Number", widget=forms.NumberInput(attrs={'placeholder': 'Enter Contact number'}))
    
    # Passengers Type field
    passenger_type = forms.ChoiceField(
        choices=[('children', 'Children (0-10)'), ('adult', 'Adult'), ('old', 'Elder (50+)'), ('students', 'Students')],
        label="Passenger Type",
        widget=forms.Select(attrs={'onchange': 'showImageUpload()'})
    )
    
    # Student Image field, only required if 'students' is selected
    student_image = forms.ImageField(label="Upload valid documents", required=False)
    
    # Password field
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'}), label="Password")
    
    # Confirm Password field
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your password'}), label="Confirm Password")

    # Custom validation for password match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError("Passwords do not match!")

        return cleaned_data

    # Custom validation for student image, required if 'students' is selected in passengers_type
    # def clean_student_image(self):
    #     passenger_type = self.cleaned_data.get("passengers_type")
    #     student_image = self.cleaned_data.get("student_image")

    #     if passenger_type == "students" and not student_image:
    #         raise ValidationError("Uploading a valid document is required for students.")
        
    #     return student_image
    
    def save(self):
        # Hashing the password before saving
        
        # Save the user data to the UserRegistration model
        user = UserRegistration(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            contact=self.cleaned_data["contact"],
            passenger_type=self.cleaned_data["passenger_type"],
            # student_image=self.cleaned_data.get("student_image"),  # student_image is optional
            password = self.cleaned_data["password"],  # Store the hashed password
        )
        user.save()
        return user
    
    
class companyEntry(forms.Form):
    username = forms.CharField(max_length=100, label="Your Name", widget=forms.TextInput(attrs={'placeholder': 'Enter your company name'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    contact = forms.CharField(max_length=15, label="Contact Number", widget=forms.NumberInput(attrs={'placeholder': 'Enter Contact number'}))
    vehicle_number = forms.CharField(max_length=15, label="Vehicle Number", widget=forms.TextInput(attrs={'placeholder': 'Enter your vehicle number'}))

    # vehicle Type field
    vehicle_type = forms.ChoiceField(
        choices=[('Long Route', 'Long Routes (Night Bus)'), 
                 ('Short Route', 'Short Route (Local Bus)'), 
                 ('Reservations', 'Small (Reservation) Vehicle')],
        label="Vehicle Type"
    )
    #destination / origin type
    destination=forms.ChoiceField(
        choices= [
        ('Kathmandu', 'Kathmandu'),
        ('Pokhara', 'Pokhara'),
        ('Chitwan', 'Chitwan'),
        ('Biratnagar', 'Biratnagar'),
        ('Butwal', 'Butwal'),
        ('Jhapa', 'Jhapa'),
    ],
        label="destination"
    )
    #destination / origin type
    origin=forms.ChoiceField(
        choices=[
        ('Kathmandu', 'Kathmandu'),
        ('Pokhara', 'Pokhara'),
        ('Chitwan', 'Chitwan'),
        ('Biratnagar', 'Biratnagar'),
        ('Butwal', 'Butwal'),
        ('Jhapa', 'Jhapa'),
    ],
        label="origin"
    )
        
    

    passenger_capacity = forms.IntegerField(label="Passenger Capacity", widget=forms.NumberInput(attrs={'placeholder': 'Enter passenger capacity number'}))

    # Password field
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'}), label="Password")

    # Confirm Password field
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your password'}), label="Confirm Password")

    # Custom validation for password match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self):
        # Save the user data to the companyRegistration model
        user = companyRegistration(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            contact=self.cleaned_data["contact"],
            vehicle_number=self.cleaned_data["vehicle_number"],
            vehicle_type=self.cleaned_data["vehicle_type"],
            origin=self.cleaned_data["origin"],
            destination=self.cleaned_data["destination"],
            passenger_capacity=self.cleaned_data["passenger_capacity"],
            password=self.cleaned_data["password"],  # Store the hashed password
        )
        user.save()
        return user
    
    

class BusRouteForm(forms.ModelForm):
    # Define the choices for origin, destination, and vehicle types
    ORIGIN_CHOICES = [
        ('Kathmandu', 'Kathmandu'),
        ('Pokhara', 'Pokhara'),
        ('Chitwan', 'Chitwan'),
        ('Biratnagar', 'Biratnagar'),
        ('Butwal', 'Butwal'),
    ]

    DESTINATION_CHOICES = [
        ('Kathmandu', 'Kathmandu'),
        ('Pokhara', 'Pokhara'),
        ('Chitwan', 'Chitwan'),
        ('Biratnagar', 'Biratnagar'),
        ('Butwal', 'Butwal'),
    ]
    
    VEHICLE_TYPE_CHOICES = [
        ('Long Route', 'Long Routes (Night Bus)'),
        ('Short Route', 'Short Route (Local Bus)'),
        ('Reservations', 'Small (Reservation) Vehicle'),
    ]

    origin = forms.ChoiceField(choices=ORIGIN_CHOICES, required=True)
    destination = forms.ChoiceField(choices=DESTINATION_CHOICES, required=True)
    vehicle_number = forms.CharField(max_length=10, required=True)
    vehicle_type = forms.ChoiceField(choices=VEHICLE_TYPE_CHOICES, required=True)
    username = forms.CharField(max_length=100, required=True)
    contact = forms.CharField(max_length=15, required=True)
    passenger_capacity = forms.IntegerField(min_value=1, required=True)
    departure_date = forms.DateField(required=True)

    class Meta:
        model = BusRoute
        fields = ['origin', 'destination', 'vehicle_number', 'vehicle_type', 'username', 'contact', 'passenger_capacity', 'departure_date']

    def clean(self):
        cleaned_data = super().clean()
        origin = cleaned_data.get('origin')
        destination = cleaned_data.get('destination')

        # Add custom validation: origin and destination must not be the same
        if origin == destination:
            raise forms.ValidationError("Origin and destination cannot be the same.")

        # Return the cleaned data
        return cleaned_data
    
from django import forms
from .models import BookedTicket  # Make sure this model is imported

# class BookedTicketForm(forms.ModelForm):
#     PAYMENT_TYPE = [
#         ('Cash on counter', 'Cash on counter'),
#         ('online payment', 'online payment'),
#     ]
    
#     payment = forms.ChoiceField(choices=PAYMENT_TYPE, required=True)
#     name = forms.CharField(max_length=100, label="Passenger Name", widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
#     email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
#     phone = forms.CharField(max_length=15, label="Contact Number", widget=forms.NumberInput(attrs={'placeholder': 'Enter contact number'}))
#     comments = forms.CharField(max_length=500, required=False, label="Special Instructions", widget=forms.Textarea(attrs={'placeholder': 'Optional'}))
#     departure_time = forms.DateField(required=True)
#     paymentproof = forms.ImageField(label="Upload Payment Screenshot (if applicable)", required=False)
#     vech_no = forms.CharField(max_length=20, label="Vehicle Number", widget=forms.TextInput(attrs={'placeholder': 'E.g. BA 2 KHA 1234'}))  # ✅ new field

#     class Meta:
#         model = BookedTicket  # Link the form to the BookedTicket model
#         fields = ['name', 'email', 'phone', 'comments', 'payment', 'departure_time', 'paymentproof', 'vech_no']  # Include all the fields for the model

#     def clean(self):
#         cleaned_data = super().clean()
#         return cleaned_data
#     def __init__(self, *args, **kwargs):
#         vech_no = kwargs.pop('vech_no', None)
#         super().__init__(*args, **kwargs)
#         if vech_no:
#             self.fields['vech_no'].initial = vech_no
            
#     def save(self):
#         user = BookedTicket(
#             name=self.cleaned_data["name"],
#             phone=self.cleaned_data["phone"],
#             email=self.cleaned_data["email"],
#             comments=self.cleaned_data["comments"],
#             departure_time=self.cleaned_data["departure_time"],
#             paymentproof=self.cleaned_data.get("paymentproof"),
#             payment=self.cleaned_data["payment"],
#             vech_no=self.cleaned_data["vech_no"],  # ✅ new field
#         )
#         user.save()
#         return user
import uuid

class BookedTicketForm(forms.ModelForm):
    PAYMENT_TYPE = [
        ('Cash on counter', 'Cash on counter'),
        ('online payment', 'online payment'),
    ]

    payment = forms.ChoiceField(choices=PAYMENT_TYPE, required=True)
    name = forms.CharField(max_length=100, label="Passenger Name", widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    phone = forms.CharField(max_length=15, label="Contact Number", widget=forms.NumberInput(attrs={'placeholder': 'Enter contact number'}))
    comments = forms.CharField(max_length=500, required=False, label="Special Instructions", widget=forms.Textarea(attrs={'placeholder': 'Optional'}))
    departure_time = forms.DateField(required=True)
    paymentproof = forms.ImageField(label="Upload Payment Screenshot (if applicable)", required=False)
    vech_no = forms.CharField(max_length=20, label="Vehicle Number", widget=forms.TextInput(attrs={'placeholder': 'E.g. BA 2 KHA 1234'}))
    Seat_no = forms.CharField(max_length=20, label="Your Selected Seats:")
    class Meta:
        model = BookedTicket
        fields = ['name', 'email', 'phone', 'comments', 'payment', 'departure_time', 'paymentproof', 'vech_no', 'Seat_no']
    
    def __init__(self, *args, **kwargs):
        vech_no = kwargs.pop('vech_no', None)
        super().__init__(*args, **kwargs)
        if vech_no:
            self.fields['vech_no'].initial = vech_no

    def clean(self):
        cleaned_data = super().clean()
        payment = cleaned_data.get('payment')
        paymentproof = cleaned_data.get('paymentproof')

        if payment == 'online payment' and not paymentproof:
            self.add_error('paymentproof', 'Payment screenshot is required for online payments.')

        return cleaned_data

    def save(self):
        vech_no = self.cleaned_data["vech_no"]
        seat_no = self.cleaned_data["Seat_no"]
        ticket_no = f"{vech_no}-{seat_no}".replace(" ", "")  # remove spaces to keep it clean

        # Ensure the Ticket_no is unique
        if BookedTicket.objects.filter(Ticket_no=ticket_no).exists():
            raise forms.ValidationError("This ticket number already exists. Please change seat or vehicle.")

        user = BookedTicket(
            name=self.cleaned_data["name"],
            phone=self.cleaned_data["phone"],
            email=self.cleaned_data["email"],
            comments=self.cleaned_data["comments"],
            departure_time=self.cleaned_data["departure_time"],
            paymentproof=self.cleaned_data.get("paymentproof"),
            payment=self.cleaned_data["payment"],
            vech_no=vech_no,
            Seat_no=seat_no,
            Ticket_no=ticket_no,
        )
        user.save()
        return user
