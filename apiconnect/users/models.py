from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.exceptions import ValidationError


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

class AdminUser(BaseUser):
    created_by = models.ForeignKey(
        'BaseUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_superuser': True},
        related_name='created_admin_users'
    )

class HealthCenterUser(BaseUser):
    organization_description = models.TextField(max_length=500)
    approved_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.phone_number:
            raise ValidationError("Phone number is required for Health Center User.")
        super().save(*args, **kwargs)

class DoctorUser(BaseUser):
    associated_organization = models.CharField(max_length=100)
    approved_by = models.ForeignKey(HealthCenterUser, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

class PatientUser(BaseUser):
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])


class ResearchSiteUser(BaseUser):
    site_location = models.CharField(max_length=100)
    site_manager = models.CharField(max_length=100)
    organization_description = models.TextField(max_length=500, default='')
    approved_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.phone_number:
            raise ValidationError("Phone number is required for Research Site User.")
        super().save(*args, **kwargs)
