from django.test import TestCase
from django.core.exceptions import ValidationError

from accounts.models import Customer

class CustomerPeselTestCase(TestCase):

    def test_pesel_validation(self):
        valid_pesel = '44051401458'
        invalid_pesel_with_valid_checksum = '22222222222'
        invalid_pesel_with_invalid_checksum = '12345678900'

        # Ensure that valid PESEL passes validation
        with self.subTest(pesel=valid_pesel):
            self.assertIsNone(Customer(pesel=valid_pesel).clean())

        # Ensure that invalid PESEL with valid checksum raises ValidationError
        with self.subTest(pesel=invalid_pesel_with_valid_checksum):
            with self.assertRaises(ValidationError):
                Customer(pesel=invalid_pesel_with_valid_checksum).clean()

        # Ensure that PESEL with invalid checksum raises ValidationError
        with self.subTest(pesel=invalid_pesel_with_invalid_checksum):
            with self.assertRaises(ValidationError):
                Customer(pesel=invalid_pesel_with_invalid_checksum).clean()
