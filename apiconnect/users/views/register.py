from django.shortcuts import render, redirect
from ..forms import HospitalRegistrationForm, DoctorRegistrationForm, PatientRegistrationForm, ResearchSiteRegistrationForm


def register_hospital(request):
    if request.method == 'POST':
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the user with the hashed password
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = HospitalRegistrationForm()

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

