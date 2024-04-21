from django.db import models
from django.conf import settings

from utils.validators import validate_pesel, validate_pesel_unique

User = settings.AUTH_USER_MODEL


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pesel = models.CharField(max_length=11, validators=[validate_pesel, validate_pesel_unique])
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True)
    privacy_policy_accepted = models.BooleanField(default=False)
    marketing_agreement = models.BooleanField(default=False)

    def __str__(self):
        return f"Customer profile of {self.user.username}"