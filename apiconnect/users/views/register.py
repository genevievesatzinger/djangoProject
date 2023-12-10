from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..forms import HealthCenterRegistrationForm, DoctorRegistrationForm
from ..forms import AdminUserForm, PatientRegistrationForm, ResearchSiteRegistrationForm
from ..models import AdminUser, HealthCenterUser, DoctorUser
from django.contrib.auth.decorators import user_passes_test

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


def is_admin_user(user):
    return user.is_authenticated and isinstance(user, AdminUser)

@user_passes_test(is_admin_user)
def unapproved_health_center_users(request):
    unapproved_users = HealthCenterUser.objects.filter(is_approved=False)
    return render(request, 'unapproved_health_center_users.html', {'unapproved_users': unapproved_users})

@user_passes_test(is_admin_user)
def approve_health_center_user(request, user_id):
    user = get_object_or_404(HealthCenterUser, id=user_id)

    if request.method == 'POST':
        if 'approve' in request.POST:
            user.is_approved = True
            user.approved_by = request.user
            user.save()
            return redirect('unapproved_health_center_users')  # Redirect to the list

    return render(request, 'approve_health_center_user.html', {'user': user})