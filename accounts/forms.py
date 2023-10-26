from django import forms
from .models import Profile
class LoginForm(forms.Form):
    username= forms.CharField(max_length=250)
    password= forms.CharField(widget=forms.PasswordInput)
    
class CreateUserForm(forms.Form):
    class Meta:
        model=Profile
        fields='__all__'
