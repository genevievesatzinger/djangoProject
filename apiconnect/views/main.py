from django.shortcuts import render,redirect
import requests
from django.http import HttpResponse

def home(request):
    return render(request, 'apiconnect/home.html')

def preloader(request):
    return render(request, 'apiconnect/preloader.html')

def clinical_trial_info(request):
    return render(request, 'apiconnect/clinical_trial_info.html')