from django.db import models
from django.contrib.auth.models import AbstractUser

# Extending Django User model (custom User model)
class User(AbstractUser):
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    nid = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, help_text='Admin Role, e.g., Superadmin, Receptionist')
    permissions = models.TextField(help_text='JSON or text for role-based access control')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Doctor(models.Model):
    full_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    availability = models.TextField(help_text='Availability schedule as JSON or text')

    def __str__(self):
        return self.full_name


class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class DoctorDiseaseAssignment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)


class Visit(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    visit_date = models.DateField()


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
