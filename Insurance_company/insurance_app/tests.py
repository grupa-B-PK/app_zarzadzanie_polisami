from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import date, timedelta

from insurance_app.models import CarInsurance, CarPolicyType
from insurance_app.forms import CarInsuranceModelForm
from accounts.models import Customer

User = get_user_model()

class CarDataTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user', first_name='John', last_name='Doe')
        self.customer = Customer.objects.create(user=self.user)
        self.policy_type = CarPolicyType.objects.create(
            policy_type='Test Policy',
            policy_description='Test Policy Description',
            type_factor=1.0
        )

    def test_correct_car_data(self):
        form_data = {
            'policy_type': self.policy_type,
            'valid_to': date.today() + timedelta(days=7),
            'car_mark_model': 'Toyota Corolla',
            'production_year': 2022,
            'fuel_type': 'Gasoline',
            'mileage': 50000,
            'average_year_mileage': 3,
            'is_rented': False,
            'number_of_owners': 1,
            'driver_under_26': False
        }

        form = CarInsuranceModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_car_data(self):
        form_data = {
            'policy_type': self.policy_type,
            'valid_to': date.today() - timedelta(days=7),  # valid_to must be set in the future
            'car_mark_model': 'Toyota Corolla',
            'production_year': 2099,  # production year should be a past or present year
            'fuel_type': 'Gasoline',
            'mileage': 50000,
            'average_year_mileage': 3,
            'is_rented': False,
            'number_of_owners': 1,
            'driver_under_26': False
        }

        form = CarInsuranceModelForm(data=form_data)
        self.assertFalse(form.is_valid())