from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from ..forms import UserUpdateForm
from django.contrib import messages


@login_required
def update_profile(request):

    if request.method == 'GET':
        form = UserUpdateForm(instance=request.user)
        return render(request, 'apiconnect/update_profile.html', {'form': form})    
   
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('my_profile')
    
    return render(request, 'apiconnect/update_profile.html', {'form': form})

@login_required
def my_profile(request):
    user_form = UserUpdateForm(instance=request.user)
        
    context = {
        'user_form': user_form
    }
        
    return render(request, 'apiconnect/profile.html', context)