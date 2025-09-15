from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import User, Admin, Doctor, Disease, DoctorDiseaseAssignment, Appointment, Visit, ContactMessage


# ---------------- Custom User ----------------
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "username", "email", "full_name", "phone", "nid", "age", "gender", "is_admin", "is_staff"
    )
    search_fields = ("username", "email", "full_name", "phone", "nid")
    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("full_name", "phone", "nid", "age", "gender", "is_admin"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "fields": ("full_name", "phone", "nid", "age", "gender", "is_admin"),
        }),
    )

admin.site.register(User, CustomUserAdmin)


# ---------------- Admin Profile ----------------
@admin.register(Admin)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    search_fields = ("user__username", "role")


# ---------------- Doctor ----------------
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "specialization", "email", "phone")
    search_fields = ("full_name", "specialization", "email")


# ---------------- Disease ----------------
@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ---------------- Doctor-Disease Assignment ----------------
@admin.register(DoctorDiseaseAssignment)
class DoctorDiseaseAssignmentAdmin(admin.ModelAdmin):
    list_display = ("doctor", "disease")


# ---------------- Appointment ----------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient", "doctor", "scheduled_date", "scheduled_time",
        "status", "created_at", "approve_button", "cancel_button"
    )
    list_filter = ("status", "scheduled_date")
    search_fields = ("patient__username", "doctor__full_name")

    # --- Buttons ---
    def approve_button(self, obj):
        if obj.status == "Pending":
            url = reverse("admin:approve_appointment", args=[obj.id])
            return format_html('<a class="button" href="{}">Approve</a>', url)
        return "-"
    approve_button.short_description = "Approve"

    def cancel_button(self, obj):
        if obj.status in ["Pending", "Confirmed"]:
            url = reverse("admin:cancel_appointment", args=[obj.id])
            return format_html('<a class="button" href="{}">Cancel</a>', url)
        return "-"
    cancel_button.short_description = "Cancel"

    # --- Custom URLs ---
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "approve/<int:appointment_id>/",
                self.admin_site.admin_view(self.approve_view),
                name="approve_appointment",
            ),
            path(
                "cancel/<int:appointment_id>/",
                self.admin_site.admin_view(self.cancel_view),
                name="cancel_appointment",
            ),
        ]
        return custom_urls + urls

    # --- Views for Approve/Cancel ---
    def approve_view(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
            appointment.status = "Confirmed"
            appointment.save()
            self.message_user(request, f"Appointment {appointment.id} approved ✅", messages.SUCCESS)
        except Appointment.DoesNotExist:
            self.message_user(request, "Appointment not found ❌", messages.ERROR)
        return redirect("..")

    def cancel_view(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
            appointment.status = "Cancelled"
            appointment.save()
            self.message_user(request, f"Appointment {appointment.id} cancelled ❌", messages.WARNING)
        except Appointment.DoesNotExist:
            self.message_user(request, "Appointment not found ❌", messages.ERROR)
        return redirect("..")


# ---------------- Visit ----------------
@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("appointment", "disease", "visit_date")


# ---------------- Contact Message ----------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "submitted_at", "admin")
    search_fields = ("name", "email", "message")
