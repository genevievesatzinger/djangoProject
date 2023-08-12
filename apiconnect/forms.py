from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import NewUser

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=244)
    last_name = forms.CharField(max_length=250)
    password1 = forms.CharField(max_length=50, required=True)
    password2 = password1
    class Meta:
        model = NewUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

class LoginForm(forms.Forms):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)