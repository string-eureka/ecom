from django import forms
from Users.models import BaseUser
from .models import Review
class AddMoneyForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        fields = ['balance']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['balance'].label = 'Amount to Add'


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,  
        label='Quantity',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'audit']
