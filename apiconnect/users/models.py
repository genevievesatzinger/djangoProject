from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models

class BaseUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="baseuser_set",  # Unique related_name
        related_query_name="baseuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="baseuser_set",  # Unique related_name
        related_query_name="baseuser",
    )

class HospitalUser(BaseUser):
    hospital_name = models.CharField(max_length=100)

class DoctorUser(BaseUser):
    specialization = models.CharField(max_length=100)

class PatientUser(BaseUser):
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

class ResearchSiteUser(BaseUser):
    site_location = models.CharField(max_length=100)
    site_manager = models.CharField(max_length=100)