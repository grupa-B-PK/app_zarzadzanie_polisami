from django.core.exceptions import ValidationError
from django.core.validators import validate_integer

from datetime import datetime

def validate_pesel(pesel):
    # validating length:
    if not pesel.isdigit() or len(pesel) != 11:
        raise ValidationError('PESEL must contain 11 digits.')
    validate_integer(pesel)

    # validating checksum:
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    checksum = sum(int(pesel[i]) * weights[i] for i in range(10))
    control_sum = checksum % 10
    if control_sum != 0:
        control_sum = 10 - control_sum
    if control_sum != int(pesel[10]):
        raise ValidationError('Invalid PESEL checksum.')

    # validating correct checksum but incorrect number
    if all(val == str(pesel)[0] for val in str(pesel)[1:]):
        raise ValidationError('This is not a correct PESEL number.')

def validate_pesel_unique(pesel):
    from accounts.models import Customer
    if Customer.objects.filter(pesel=pesel).exists():
        raise ValidationError('This PESEL is already registered.')

def validate_future_date(value):
    if value <= datetime.today().date():
        raise ValidationError('The date must be in the future.')

def validate_past_date(value):
    current_year = datetime.today().year
    if value >= current_year:
        raise ValidationError('The year must be in the past.')

def validate_uppercase(value):
    if not (value and value[0].isupper() and value[1:].islower()):
        raise ValidationError('The value must start with an uppercase letter and contain no other uppercase letters.')

def validate_first_name(value):
    validate_uppercase(value)

def validate_last_name(value):
    validate_uppercase(value)