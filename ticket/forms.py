from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password  # Import for password hashing
from .models import UserRegistration

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
