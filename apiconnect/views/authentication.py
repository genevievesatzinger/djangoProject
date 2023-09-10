from django.shortcuts import render,redirect
import requests
from ..forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_page(request):

    if request.method == 'GET':
        form = LoginForm()
        return render(request,'apiconnect/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('home')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'apiconnect/login.html',{'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'apiconnect/register.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'apiconnect/register.html', {'form': form})
