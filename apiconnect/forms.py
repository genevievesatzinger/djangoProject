from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    
# Create register forms for each user profile type
# First one is general, can delete later
class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=65, required=True)
    email = forms.CharField(max_length=65, required=True)
    first_name = forms.CharField(max_length=65, required=False)
    last_name = forms.CharField(max_length=65, required=False)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    class Meta:
        model=User
        fields = ['username','email', 'first_name', 'last_name', 'password1','password2']

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']