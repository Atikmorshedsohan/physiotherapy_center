import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from main_app.models import *
from .forms import *


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

            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                scheduled_date=data["scheduled_date"],
                scheduled_time=data["scheduled_time"],
                status=data.get("status", "Pending")
            )

            return JsonResponse({"success": True, "id": appointment.id})

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
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

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