from django import forms
from .models import HospitalUser, DoctorUser, PatientUser, ResearchSiteUser
from django.contrib.auth.forms import UserCreationForm

# Create register forms specific to each user model
# First one is general, can delete later
class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=65, required=True)
    email = forms.CharField(max_length=65, required=True)
    first_name = forms.CharField(max_length=65, required=False)
    last_name = forms.CharField(max_length=65, required=False)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    class Meta:
        model=User
        fields = ['username','email', 'first_name', 'last_name', 'password1','password2']

class HosptialRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=65, required=True)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    class Meta:
        model=HospitalUser
        fields = ['username','email', 'password1','password2']

class DoctorRegisterForm(UserCreationForm):
    email = forms.CharField(max_length=65, required=True)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    class Meta:
        model=DoctorUser
        fields = ['username','email', 'first_name', 'last_name', 'password1','password2']

class PatientRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=65, required=True)
    email = forms.CharField(max_length=65, required=True)
    first_name = forms.CharField(max_length=65, required=False)
    last_name = forms.CharField(max_length=65, required=False)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    class Meta:
        model=PatientUser
        fields = ['username','email', 'first_name', 'last_name', 'password1','password2']

class ResearchSiteRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=65, required=True)
    email = forms.CharField(max_length=65, required=True)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    class Meta:
        model=ResearchSiteUser
        fields = ['username','email', 'password1','password2']