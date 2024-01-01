from django import forms
from .models import BaseUser, CustomerUser, VendorUser
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(label=" Name", max_length=100)
    phone_number = forms.IntegerField(label="Phone Number")
    address = forms.CharField(label="Address", max_length=255)

    class Meta:
        model = BaseUser
        fields = [
            "username",
            "email",
            "name",
            "phone_number",
            "address",
            "password1",
            "password2",
        ]


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        fields = ["name", "phone_number", "address"]


class UserProfileForm(forms.ModelForm):
    user_type = forms.ChoiceField(
        label="User Type",
        choices=BaseUser.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = BaseUser
        fields = ["name", "phone_number", "address", "user_type"]
