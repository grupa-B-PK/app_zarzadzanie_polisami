from django.db import models

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

User = settings.AUTH_USER_MODEL


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pesel = models.CharField(max_length=11, unique=True, validators=[RegexValidator(regex='^\\d{11}$', message='PESEL must contain 11 digits')])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True)
    privacy_policy_accepted = models.BooleanField(default=False)


marketing_agreement = models.BooleanField(default=False)


def clean(self):
    super().clean()
    # Sprawdzenie poprawności sumy kontrolnej PESEL
    if self.pesel:
        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        checksum = sum(int(self.pesel[i]) * weights[i] for i in range(10))
        control_sum = checksum % 10
        if control_sum != 0:
            control_sum = 10 - control_sum
        if control_sum != int(self.pesel[10]):
            raise ValidationError('Invalid PESEL checksum')

