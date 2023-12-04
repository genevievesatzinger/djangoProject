from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import HealthCenterRegistrationForm, DoctorRegistrationForm
from ..forms import AdminUserForm, PatientRegistrationForm, ResearchSiteRegistrationForm

@login_required
def register_admin_user(request):
    if not request.user.is_superuser:
        return redirect('some_error_view')
    
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            admin_user = form.save(commit=False)
            admin_user.created_by = request.user
            admin_user.save()
            return redirect('login')
    else:
        form = AdminUserForm()
    return render(request, 'register_admin_user.html', {'form': form})

def register_health_center(request):
    if request.method == 'POST':
        form = HealthCenterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the user with the hashed password
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = HealthCenterRegistrationForm()

    return render(request, 'register_hospital.html', {'form': form})


def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the user with the hashed password
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = DoctorRegistrationForm()
    return render(request, 'register_doctor.html', {'form': form})

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the user with the hashed password
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = PatientRegistrationForm()
    return render(request, 'register_patient.html', {'form': form})

def register_research_site(request):
    if request.method == 'POST':
        form = ResearchSiteRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the user with the hashed password
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = ResearchSiteRegistrationForm()
    return render(request, 'register_research_site.html', {'form': form})

