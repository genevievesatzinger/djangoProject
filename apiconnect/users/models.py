from django.contrib.auth.models import AbstractUser
from django.db import models

class BaseUser(AbstractUser):
    # You can add any common fields here, if necessary
    pass

class HospitalUser(BaseUser):
    # Add additional fields specific to Hospital
    hospital_name = models.CharField(max_length=100)

class DoctorUser(BaseUser):
    # Additional fields for Doctor
    email = models.EmailField(unique=True)


class PatientUser(BaseUser):
    # Additional fields for Patient
    email = models.EmailField(unique=True)

class ResearchSiteUser(BaseUser):
    # Additional fields for ResearchSite
    site_location = models.CharField(max_length=100)
