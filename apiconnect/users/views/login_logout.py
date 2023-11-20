from django.contrib.auth.views import LoginView
from ..forms import HospitalLoginForm, DoctorLoginForm, PatientLoginForm, ResearchSiteLoginForm
from django.contrib.auth import logout
from django.shortcuts import redirect

class login_hospital(LoginView):
    form_class = HospitalLoginForm
    template_name = 'login_hospital.html'

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