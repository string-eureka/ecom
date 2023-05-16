from django import forms
from .models import BaseUser,CustomerUser,VendorUser
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    name = forms.CharField(label=' Name', max_length=100)
    phone_number = forms.CharField(label='Phone Number', max_length=12)
    address = forms.CharField(label='Address', max_length=255)
    email = forms.EmailField()
    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'name','phone_number','address','password1', 'password2']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        fields = ['name', 'phone_number', 'address']
