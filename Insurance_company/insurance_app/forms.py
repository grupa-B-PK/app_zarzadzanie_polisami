from django import forms
from .models import CarInsurance, HouseInsurance


class CarInsuranceModelForm(forms.ModelForm):
    class Meta:
        model = CarInsurance
        fields = ["policy_name", "policy_type", "valid_to", "car_model", "production_year", "fuel_type", "mileage",
                  "average_year_mileage", "is_rented",
                  "number_of_owners", "driver_under_26"]
        labels = {
            'policy_name': "Nazwa polisy",
            'policy_type': 'Typ polisy',
            'valid_to': 'Termin ochorny',
            'car_model': 'Model samochodu',
            'production_year': 'Rok produkcji',
            'fuel_type': 'Typ paliwa',
            'mileage': 'Przebieg',
            'average_year_mileage': 'Średni roczny przebieg',
            'is_rented': 'Czy wynajmowane',
            'number_of_owners': 'Liczba współwłaścicieli',
            'driver_under_26': 'Kierowca poniżej 26 roku życia',
        }


class HouseInsuranceModelForm(forms.ModelForm):
    class Meta:
        model = HouseInsurance
        fields = ["policy_name", "valid_to", "house_type", "number_of_owners", "house_area", "house_city",
                  "house_value"]
        labels = {
            'policy_name': "Nazwa polisy",
            'valid_to': 'Termin ochorny',
            'house_type': 'Typ domu',
            'number_of_owners': 'Liczba właścicieli',
            'house_area': 'Powierzchnia domu',
            'house_city': 'Miasto',
            'house_value': 'Wartość domu',
        }
