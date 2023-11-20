from django.shortcuts import render, redirect
from ..forms import HospitalProfileForm, DoctorProfileForm, PatientProfileForm, ResearchSiteProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def edit_hospital_profile(request):
    if request.method == 'POST':
        form = HospitalProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to the profile view page
    else:
        form = HospitalProfileForm(instance=request.user)
    return render(request, 'profile/edit_hospital_profile.html', {'form': form})

@login_required
def edit_doctor_profile(request):
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to the profile view page
    else:
        form = DoctorProfileForm(instance=request.user)
    return render(request, 'profile/edit_doctor_profile.html', {'form': form})

@login_required
def edit_patient_profile(request):
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to the profile view page
    else:
        form = PatientProfileForm(instance=request.user)
    return render(request, 'profile/edit_patient_profile.html', {'form': form})

@login_required
def edit_research_site_profile(request):
    if request.method == 'POST':
        form = ResearchSiteProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to the profile view page
    else:
        form = ResearchSiteProfileForm(instance=request.user)
    return render(request, 'profile/edit_research_site_profile.html', {'form': form})