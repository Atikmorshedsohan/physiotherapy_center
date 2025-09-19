from django.db import transaction
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from main_app.models import *
from .forms import *
from django.db.models import F


# Home Page View
def home(request):
    return render(request, "index.html")


# Services Page View
def services(request):
    return render(request, "services.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

# Registration Page View
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # After successful registration
    else:
        form = UserRegisterForm()
    return render(request, "registration.html", {"form": form})


# Combined Login + Registration Handler
def auth_view(request):
    form = UserRegisterForm()

    # Login Attempt
    if request.method == "POST" and "username" in request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "authentication.html",
                {"form": form, "error": "Invalid credentials"},
            )

    # Registration Attempt
    elif request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    # GET Request or fallback
    return render(request, "authentication.html", {"form": form})


#  Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect("home")



def appointment_page(request):
    return render(request, "appointment.html") 


@csrf_protect
@login_required
def create_appointment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # ✅ always use logged-in user as patient
            patient = request.user
            doctor = Doctor.objects.get(id=data["doctor"])

            # 🔢 Calculate next serial number for this doctor & date
            existing_count = Appointment.objects.filter(
                doctor=doctor,
                scheduled_date=data["scheduled_date"]
            ).count()
            serial_number = existing_count + 1

            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                scheduled_date=data["scheduled_date"],
                scheduled_time=data["scheduled_time"],
                status=data.get("status", "Pending"),
                serial_number=serial_number  # 👈 new field
            )

            return JsonResponse({
                "success": True,
                "id": appointment.id,
                "serial_number": serial_number
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)




# API: return doctor list as JSON
def doctor_list(request):
    doctors = Doctor.objects.all().values(
        "id", "full_name", "specialization", "phone", "email", "availability"
    )
    return JsonResponse(list(doctors), safe=False)


@login_required
def profile(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    appointments = Appointment.objects.filter(patient_id=pk).order_by("scheduled_date", "scheduled_time")

    return render(request, "profile.html", {
        "profile": profile,
        "appointments": appointments
    })


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def cancel_appointment(request, appointment_id=None, pk=None):
    appt_id = appointment_id or pk
    if not appt_id:
        return redirect("patient_profile", pk=request.user.pk)

    try:
        with transaction.atomic():
            appointment = Appointment.objects.select_for_update().get(id=appt_id)

            doctor = appointment.doctor
            scheduled_date = appointment.scheduled_date
            cancelled_serial = appointment.serial_number

            appointment.delete()

            # shift later serials down by 1
            Appointment.objects.filter(
                doctor=doctor,
                scheduled_date=scheduled_date,
                serial_number__gt=cancelled_serial
            ).update(serial_number=F("serial_number") - 1)

        return redirect("patient_profile", pk=request.user.pk)

    except Appointment.DoesNotExist:
        return redirect("patient_profile", pk=request.user.pk)
    except Exception as e:
        return redirect("patient_profile", pk=request.user.pk)
    
    

def send_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            if request.user.is_authenticated:
                message.sender = request.user
            else:
                message.sender = None  # or handle guest sender

            admin_user = User.objects.filter(is_superuser=True).first()
            if admin_user:
                message.receiver = admin_user
                message.save()
                return redirect("about")
    else:
        form = MessageForm()

    return render(request, "send_message.html", {"form": form})


