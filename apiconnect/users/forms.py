from django import forms
from .models import HospitalUser, DoctorUser, PatientUser, ResearchSiteUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# Start of Hospital Forms

class HospitalRegistrationForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = HospitalUser
        fields = ['username', 'email', 'password1', 'password2',  'hospital_name', 'phone_number', 'address']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")

        return cleaned_data

class HospitalProfileForm(forms.ModelForm):
    class Meta:
        model = HospitalUser
        fields = ['email', 'hospital_name', 'phone_number', 'address']

class HospitalLoginForm(AuthenticationForm):
    pass

# End of Hospital Forms


# Start of Doctor Forms

class DoctorRegistrationForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = DoctorUser
        fields = ['username', 'password1', 'password2', 'email', 'specialization', 'phone_number', 'address']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")

        return cleaned_data

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorUser
        fields = ['email', 'specialization', 'phone_number', 'address']

class DoctorLoginForm(AuthenticationForm):
    pass

# End of Doctor Forms

# Start of Patient Forms

class PatientRegistrationForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = PatientUser
        fields = ['username', 'password1', 'password2', 'email', 'age', 'gender', 'phone_number', 'address']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")

        return cleaned_data

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientUser
        fields = ['email', 'age', 'gender', 'phone_number', 'address']

class PatientLoginForm(AuthenticationForm):
    pass

# End of Patient Forms

# Start of Research Site Forms

class ResearchSiteRegistrationForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = ResearchSiteUser
        fields = ['username', 'password1', 'password2', 'email', 'site_location', 'site_manager', 'phone_number', 'address']
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")

        return cleaned_data

class ResearchSiteProfileForm(forms.ModelForm):
    class Meta:
        model = ResearchSiteUser
        fields = ['email', 'site_location', 'site_manager', 'phone_number', 'address']

class ResearchSiteLoginForm(AuthenticationForm):
    pass

# End of Research Site Forms