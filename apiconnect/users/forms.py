from django import forms
from .models import AdminUser, HealthCenterUser, DoctorUser, PatientUser, ResearchSiteUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# Start of Admin Forms

class AdminUserForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = AdminUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")

        return cleaned_data
    
# End of Admin Forms

# Start of Health Center Forms

class HealthCenterRegistrationForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = HealthCenterUser
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'address', 'organization_description']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")

        return cleaned_data

class HealthCenterProfileForm(forms.ModelForm):
    class Meta:
        model = HealthCenterUser
        fields = ['organization_description', 'approved_by', 'is_approved', 'phone_number']  # Add all the fields you need

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")

        if not phone_number:
            raise forms.ValidationError("Phone number is required.")
        
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")

        return cleaned_data

# End of Hospital Forms


# Start of Doctor Forms

class DoctorRegistrationForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = DoctorUser
        fields = ['username',  'email', 'phone_number', 'address', 'associated_organization', 'approved_by', 'is_approved']

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
        fields = ['email', 'phone_number', 'address']

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
        fields = ['username', 'password1', 'password2', 'email', 'site_location', 'site_manager', 'phone_number', 'address', 'organization_description']
    
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