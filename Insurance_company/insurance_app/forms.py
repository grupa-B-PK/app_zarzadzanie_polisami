from django import forms
from django.forms import DateInput

from .models import CarInsurance, HouseInsurance
from utils.validators import validate_future_date, validate_past_date


class CarInsuranceModelForm(forms.ModelForm):
    class Meta:
        model = CarInsurance
        fields = ["policy_type", "valid_to", "car_model", "production_year", "fuel_type", "mileage",
                  "average_year_mileage", "is_rented",
                  "number_of_owners", "driver_under_26"]
        labels = {
            "policy_type": "Typ polisy",
            'valid_to': 'Termin ochrony',
            'car_model': 'Model samochodu',
            'production_year': 'Rok produkcji',
            'fuel_type': 'Typ paliwa',
            'mileage': 'Przebieg',
            'average_year_mileage': 'Średni roczny przebieg',
            'is_rented': 'Czy wynajmowane',
            'number_of_owners': 'Liczba współwłaścicieli',
            'driver_under_26': 'Kierowca poniżej 26 roku życia',
        }
        widgets = {
            'valid_to': DateInput(attrs={'type': 'date'})
        }

    def clean_valid_to(self):
        valid_to = self.cleaned_data.get('valid_to')
        validate_future_date(valid_to)
        return valid_to

    def clean_production_year(self):
        production_year = self.cleaned_data.get('production_year')
        validate_past_date(production_year)
        return production_year

class HouseInsuranceModelForm(forms.ModelForm):
    class Meta:
        model = HouseInsurance
        fields = ["policy_type", "valid_to", "house_type", "number_of_owners", "house_area", "house_city", "house_value"]
        labels = {
            "policy_type": "Typ polisy",
            'valid_to': 'Termin ochrony',
            'house_type': 'Typ domu',
            'number_of_owners': 'Liczba właścicieli',
            'house_area': 'Powierzchnia domu',
            'house_city': 'Miasto',
            'house_value': 'Wartość domu',
        }
        widgets = {
            'valid_to': DateInput(attrs={'type': 'date'})
        }
