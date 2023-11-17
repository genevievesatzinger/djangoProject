from django.shortcuts import render, redirect
from django.contrib.auth import login
from ..forms import HosptialRegisterForm
from ..models import HospitalProfile

def register_hospital(request):
    if request.method == 'POST':
        form = HosptialRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally, add first name and last name
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()

            # Create an HospitalProfile for this user
            HospitalProfile.objects.create(user=user)

            # Log the user in and redirect them to a different page
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired redirect URL
    else:
        form = HosptialRegisterForm()

    return render(request, 'register_hospital.html', {'form': form})