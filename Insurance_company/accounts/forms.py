from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Customer
from utils.validators import validate_pesel, validate_pesel_unique, validate_first_name, validate_last_name


class CustomUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "password1", "password2")
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        validate_first_name(first_name)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        validate_last_name(last_name)
        return last_name


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['pesel', 'address', 'phone_number', 'privacy_policy_accepted', 'marketing_agreement']

    def clean_pesel(self):
        pesel = self.cleaned_data.get('pesel')
        instance = getattr(self, 'instance', None)

        queryset = Customer.objects.filter(pesel=pesel)

        if instance and instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

        if queryset.exists():
            validate_pesel_unique(pesel)

        validate_pesel(pesel)
        return pesel
