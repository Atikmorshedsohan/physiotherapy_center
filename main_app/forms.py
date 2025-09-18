from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

# User Registration Form


GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
]


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Full Name"}),
    )
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"placeholder": "Email"})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Phone Number"}),
    )
    nid = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "NID"}),
    )
    age = forms.IntegerField(
        required=True, widget=forms.NumberInput(attrs={"placeholder": "Age"})
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select())
    username = forms.CharField(
        help_text="",  # Removes default help text
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        help_text="",  # Removes default help text
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(),
        help_text="",  # Removes default help text
    )

    class Meta:
        model = User
        fields = [
            "username",
            "full_name",
            "email",
            "phone",
            "nid",
            "age",
            "gender",
            "password1",
            "password2",
        ]


# Admin Form
class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ["user", "role", "permissions"]


# Doctor Form
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["full_name", "specialization", "phone", "email", "availability"]
        widgets = {
            "availability": forms.Textarea(attrs={"rows": 3}),
        }


# Disease Form
class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ["name", "description"]


# Doctor-Disease Assignment Form
class DoctorDiseaseAssignmentForm(forms.ModelForm):
    class Meta:
        model = DoctorDiseaseAssignment
        fields = ["doctor", "disease"]


# Appointment Form
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "scheduled_date", "scheduled_time", "status"]


# Visit Form
class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = [
            "appointment",
            "disease",
            "symptoms",
            "diagnosis",
            "treatment_plan",
            "visit_date",
        ]


# Contact Message Form
class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message", "admin"]
        
         
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'age', 'medical_history']


class DoctorOpinionForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['doctor_opinion']  # only allow updating this field