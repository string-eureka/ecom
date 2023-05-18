from django import forms
from Users.models import BaseUser

class AddMoneyForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        fields = ['balance']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['balance'].label = 'Amount to Add'