from django.contrib.auth.views import LoginView
from ..forms import AdminUserForm, HealthCenterLoginForm, DoctorLoginForm, PatientLoginForm, ResearchSiteLoginForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm

class login_admin(LoginView):   
    form_class = AuthenticationForm
    template_name = 'login_admin.html'

class login_health_center(LoginView):   
    form_class = HealthCenterLoginForm
    template_name = 'login_health_center.html'

class login_doctor(LoginView):
    form_class = DoctorLoginForm
    template_name = 'login_doctor.html'

class login_patient(LoginView):
    form_class = PatientLoginForm
    template_name = 'login_patient.html'

class login_research_site(LoginView):
    form_class = ResearchSiteLoginForm
    template_name = 'login_research_site.html'

def UserLogout(request):
    logout(request)
    return redirect('login')
