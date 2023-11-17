# users/admin.py
from django.contrib import admin
from .models import AdminProfile, HospitalProfile, PatientProfile

admin.site.register(AdminProfile)
admin.site.register(HospitalProfile)
admin.site.register(PatientProfile)
