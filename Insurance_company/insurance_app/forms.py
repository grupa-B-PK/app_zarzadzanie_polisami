from django import forms
from django.forms import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from .models import CarInsurance, HouseInsurance


class CarInsuranceModelForm(forms.ModelForm):
    # helper = FormHelper()
    # helper.layout = Layout(
    #     Div(
    #         Field('policy_type', 'valid_to', 'car_model', 'production_year', 'fuel_type', css_class='col-md-6'),
    #         Field('mileage', 'average_year_mileage', 'is_rented', 'number_of_owners', 'driver_under_26',
    #           css_class='col-md-6'),
    #         css_class = 'row-fluid'
    #     )
    # )
    # def __init__(self, *args, **kwargs):
    #     super(CarInsuranceModelForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Div(
    #             Div('policy_type', 'valid_to', 'car_model', 'production_year', 'fuel_type', css_class='col-md-3'),
    #             Div('mileage', 'average_year_mileage', 'is_rented', 'number_of_owners', 'driver_under_26',css_class='col-md-3'),
    #             css_class='row-fluid'
    #         )
    #     )
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



class HouseInsuranceModelForm(forms.ModelForm):
    class Meta:
        model = HouseInsurance
        fields = ["policy_type", "valid_to", "house_type", "number_of_owners", "house_area", "house_city",
                  "house_value"]
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
