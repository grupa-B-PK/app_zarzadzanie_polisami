from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Customer


class CustomUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "password1", "password2")


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['pesel', 'address', 'phone_number', 'privacy_policy_accepted', 'marketing_agreement']

    def clean_pesel(self):
        pesel = self.cleaned_data.get('pesel')
        if Customer.objects.filter(pesel=pesel).exists():
            raise forms.ValidationError('This PESEL is already registered.')
        return pesel
