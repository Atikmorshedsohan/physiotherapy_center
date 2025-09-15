from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main_app.forms import DoctorForm,DiseaseForm, DoctorDiseaseAssignmentForm
from main_app.models import *


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:   # ✅ only superusers
            login(request, user)
            return redirect('custom_admin:dashboard')  # redirect instead of render
        else:
            context = {'error': 'Invalid credentials or not an admin.'}
            return render(request, 'login.html', context)
    return render(request, 'login.html')


@login_required
def dashboard(request):
    context = {
        "doctor_count": Doctor.objects.count(),
        "patient_count": User.objects.filter(is_admin=False).count(),
        "appointment_count": Appointment.objects.count(),
        "message_count": ContactMessage.objects.count(),
        "recent_appointments": Appointment.objects.select_related("patient", "doctor").order_by("-created_at")[:5],
    }
    return render(request, "dashboard.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")



@login_required
def add_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            # show a success message and reset form
            form = DoctorForm()  
            return render(request, "add_doctor.html", {
                "form": form,
                "success": "Doctor added successfully!"
            })
    else:
        form = DoctorForm()
    return render(request, "add_doctor.html", {"form": form})




@login_required
def doctor_list(request):
    doctors = Doctor.objects.all().order_by("full_name")
    return render(request, "doctor_list.html", {"doctors": doctors})



@login_required
def patient_list(request):
    patients = User.objects.filter(is_admin=False, is_superuser=False, is_staff=False).order_by("full_name")
    return render(request, "patient_list.html", {"patients": patients})



@login_required
def appointment_list(request):
    appointments = Appointment.objects.select_related("patient", "doctor").order_by("-id", "-scheduled_date", "-scheduled_time")
    return render(request, "admin_appointment.html", {"appointments": appointments})



@login_required
def update_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ["Pending", "Confirmed", "Completed"]:
            appointment.status = new_status
            appointment.save()
    return redirect("custom_admin:appointment_list")



@login_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.delete()
    return redirect("custom_admin:appointment_list")



@login_required


def manage_diseases(request):
    disease_form = DiseaseForm()
    assignment_form = DoctorDiseaseAssignmentForm()
    latest_id = None

    if request.method == "POST":
        if "disease_submit" in request.POST:
            disease_form = DiseaseForm(request.POST)
            if disease_form.is_valid():
                disease = disease_form.save()
                latest_id = disease.id

        elif "assignment_submit" in request.POST:
            assignment_form = DoctorDiseaseAssignmentForm(request.POST)
            if assignment_form.is_valid():
                assignment = assignment_form.save()
                latest_id = assignment.id

        # If request is AJAX, return JSON
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"latest_id": latest_id})

    diseases = Disease.objects.all()
    assignments = DoctorDiseaseAssignment.objects.select_related("doctor", "disease")

    return render(request, "admin_diseases.html", {
        "disease_form": disease_form,
        "assignment_form": assignment_form,
        "diseases": diseases,
        "assignments": assignments,
        "latest_id": latest_id,
    })

