from django import forms
from .models import BaseUser,CustomerUser,VendorUser
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=12)
    address = forms.CharField(label='Address', max_length=255)
    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'first_name','last_name','phone_number','address','password1', 'password2',]