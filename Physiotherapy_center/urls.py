"""
URL configuration for Physiotherapy_center project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from main_app import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('register/', views.register_view, name='register'),
    path('login/', views.auth_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("appointment/", views.appointment_page, name="appointment_page"),
    path("api/doctors/", views.doctor_list, name="doctor_list"),
    path("api/appointments/", views.create_appointment, name="create_appointment"),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('custom_admin/', include('custom_admin.urls')),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
