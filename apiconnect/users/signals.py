# users/signals.py or users/models.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, AdminProfile, HospitalProfile, PatientProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Logic to create user profiles
    # You might need some logic here to decide which profile to create
        AdminProfile.objects.create(user=instance)
        HospitalProfile.objects.create(user=instance)
        PatientProfile.objects.create(user=instance)
        # Create other profiles as needed