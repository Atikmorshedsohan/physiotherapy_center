from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = "custom_admin"

urlpatterns = [
    path('', lambda request: redirect('custom_admin:login')),
    path('login/', views.admin_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path("doctors/", views.doctor_list, name="doctor_list"),
    path('patients/<int:pk>/update-opinion/', views.update_doctor_opinion, name='update_doctor_opinion'),
    path("patients/", views.patient_list, name="patient_list"),
    path('patients/<int:pk>/', views.patient_profile, name='patient_profile'),
    path("appointments/", views.appointment_list, name="appointment_list"),
    path("appointments/<int:pk>/update/", views.update_status, name="update_status"),
    path("appointments/<int:pk>/delete/", views.delete_appointment, name="delete_appointment"),
    path("diseases/", views.manage_diseases, name="diseases"),
    path("inbox/", views.inbox, name="inbox"),
]
