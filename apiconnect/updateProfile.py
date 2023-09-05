from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm
from django.contrib.auth.decorators import login_required


class UpdateProfile(LoginRequiredMixin, View):
    @login_required
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        
        context = {
            'user_form': user_form
        }
        
        return render(request, 'apiconnect/update_profile.html', context)
    
    @login_required
    def post(self,request):
        user_form = UserUpdateForm(
            request.POST, 
            instance=request.user
        )        

        if user_form.is_valid():
            user_form.save()
            
            messages.success(request,'Your profile has been updated successfully!')
            
            return redirect('profile')
        else:
            context = {
                'user_form': user_form,
            }
            messages.error(request,'An error occurred while updating you profile')
            
            return render(request, 'apiconnect/profile.html', context)