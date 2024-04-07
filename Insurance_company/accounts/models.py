from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


User = settings.AUTH_USER_MODEL


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pesel = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True)
    privacy_policy_accepted = models.BooleanField(default=False)
    marketing_agreement = models.BooleanField(default=False)

def __str__(self):
    return f"Customer profile of {self.user.username}"


def clean(self):
    super().clean()
    # Checking the correctness of the PESEL checksum
    if self.pesel:
        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        checksum = sum(int(self.pesel[i]) * weights[i] for i in range(10))
        control_sum = checksum % 10
        if control_sum != 0:
            control_sum = 10 - control_sum
        if control_sum != int(self.pesel[10]):
            raise ValidationError('Invalid PESEL checksum')

