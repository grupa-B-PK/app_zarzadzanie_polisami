from django.test import TestCase
from django.core.exceptions import ValidationError

from accounts.models import Customer

class CustomerPeselTestCase(TestCase):
    # Ensure that valid PESEL passes validation
    def test_valid_pesel(self):
        valid_pesel = '44051401458'
        self.assertIsNone(Customer(pesel=valid_pesel).clean())

    # Ensure that invalid PESEL with valid checksum raises ValidationError
    def test_invalid_pesel_with_valid_checksum(self):
        invalid_pesel_with_valid_checksum = '22222222222'
        with self.assertRaises(ValidationError):
            Customer(pesel=invalid_pesel_with_valid_checksum).clean()

    # Ensure that PESEL with invalid checksum raises ValidationError
    def test_invalid_pesel_with_invalid_checksum(self):
        invalid_pesel_with_invalid_checksum = '12345678900'
        with self.assertRaises(ValidationError):
            Customer(pesel=invalid_pesel_with_invalid_checksum).clean()
