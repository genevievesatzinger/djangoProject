from django.shortcuts import render,redirect
import requests
from django.http import HttpResponse

def home(request):
    return render(request, 'apiconnect/home.html')