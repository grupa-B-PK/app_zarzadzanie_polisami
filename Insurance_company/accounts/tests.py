from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

from accounts.models import Customer
from accounts.forms import CustomUserForm, CustomerForm

User = get_user_model()

class CustomerPeselTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', first_name='John', last_name='Doe')

    # Ensure that valid PESEL passes validation
    def test_valid_pesel(self):
        valid_pesel = '44051401458'
        customer = Customer.objects.create(user=self.user, pesel=valid_pesel)
        self.assertIsNone(customer.clean())

    # Ensure that invalid PESEL with valid checksum raises ValidationError
    def test_invalid_pesel_with_valid_checksum(self):
        invalid_pesel_with_valid_checksum = '22222222222'
        customer = Customer(user=self.user, pesel=invalid_pesel_with_valid_checksum)
        with self.assertRaises(ValidationError):
            customer.full_clean()

    # Ensure that PESEL with invalid checksum raises ValidationError
    def test_invalid_pesel_with_invalid_checksum(self):
        invalid_pesel_with_invalid_checksum = '12345678900'
        customer = Customer(user=self.user, pesel=invalid_pesel_with_invalid_checksum)
        with self.assertRaises(ValidationError):
            customer.full_clean()

class UserDataTestCase(TestCase):
    def test_correct_user_data(self):

        valid_user_data = {
            'username': 'test_user',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        valid_customer_data = {
            'pesel': '44051401458',
            'address': '123 Test Street',
            'phone_number': '123456789',
            'privacy_policy_accepted': True,
            'marketing_agreement': False
        }

        user_form = CustomUserForm(data=valid_user_data)
        customer_form = CustomerForm(data=valid_customer_data)
        self.assertTrue(user_form.is_valid() and customer_form.is_valid())

    def test_invalid_user_data(self):

        invalid_user_data = {
            # Invalid because first_name is missing
            'username': 'test_user',
            'last_name': 'Doe',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        invalid_customer_data = {
            # Invalid because pesel is too short
            'pesel': '123',
            'address': '123 Test Street',
            'phone_number': '123456789',
            'privacy_policy_accepted': True,
            'marketing_agreement': False
        }

        # Test unsuccessful registration
        user_form = CustomUserForm(data=invalid_user_data)
        customer_form = CustomerForm(data=invalid_customer_data)
        self.assertFalse(user_form.is_valid() and customer_form.is_valid())