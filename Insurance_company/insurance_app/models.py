from django.db import models
from _datetime import datetime, date
import uuid


# time functions


def current_year():
    return datetime.today().year


class PolicyStatus(models.Model):
    STATUS_CHOICES = {
        "Active": "Your car is protected - policy is up to date.",
        "Expired": "Policy is expired"
    }


class CarPolicyType(models.Model):
    policy_type = models.CharField(primary_key=True, max_length=100)
    policy_description = models.TextField()
    type_factor = models.FloatField()


class HousePolicyType(models.Model):
    policy_type = models.CharField(primary_key=True, max_length=100)
    policy_description = models.TextField()
    type_factor = models.FloatField()


class CarInsurance(models.Model):
    FUEL_TYPES = (
        ("Gasoline", "Gasoline"),
        ("Diesel", "Diesel"),
        ("LPG", "LPG"),
        ("Electric", "Electric"),
        ("Hydrogen", "Hydrogen"),
        ("Biodiesel", "Biodiesel")
    )

    AVERAGE_YEAR_MILEAGE = (
        (1, "Poniżej 5 tys. km"),  # kategorie przebiegu do wykorzystania w kalkulatorze
        (2, "do 10 tys. km"),
        (3, "do 20 tys. km"),
        (4, "powyżej 20 tys. km")
    )

    # predefined fields
    policy_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    policy_type = models.ForeignKey(CarPolicyType, on_delete=models.CASCADE, blank=False,
                                    null=False)
    valid_to = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    # form fields
    car_model = models.CharField(max_length=100)
    production_year = models.PositiveIntegerField(default=current_year())
    fuel_type = models.CharField(max_length=100, choices=FUEL_TYPES)
    mileage = models.PositiveIntegerField()
    average_year_mileage = models.PositiveSmallIntegerField(choices=AVERAGE_YEAR_MILEAGE)
    is_rented = models.BooleanField(default=False)
    number_of_owners = models.PositiveSmallIntegerField()
    driver_under_26 = models.BooleanField(default=False)

    def __str__(self):
        return f"Nazwa polisy: {self.policy_name}"

    @property
    def status_validation(self):
        if self.valid_to < date.today():
            return PolicyStatus.STATUS_CHOICES["Active"]
        else:
            return PolicyStatus.STATUS_CHOICES["Expired"]


class HouseInsurance(models.Model):
    HOUSE_TYPES = (
        ("Dom", "Dom"),
        ("Szeregowiec", "Szeregowiec"),
        ("Mieszkanie", "Mieszkanie")
    )

    POLICY_DESC = {
        "Standard": "Standardowe ubezpieczenie domu zapewnia ochronę na wypadek szkód spowodowanych pożarem, zalaniem, kradzieżą i innymi zdarzeniami określonymi w polisie. Obejmuje ono także koszty naprawy lub odbudowy uszkodzonego budynku oraz jego wyposażenia.",
        "Premium": "Ubezpieczenie wariantu Premium oferuje rozszerzony zakres ochrony w porównaniu do standardowej polisy. Dodatkowo może obejmować np. zabezpieczenie przed ryzykiem zalania z powodzi, kradzieżą z włamaniem, czy uszkodzeniem wyposażenia ogrodu.",
        "Super Premium": "Najwyższy wariant ubezpieczenia domu, znany również jako Super Premium, to gwarancja najszerszego zakresu ochrony. Zapewnia on kompleksowe zabezpieczenie na wypadek praktycznie wszystkich ryzyk, włączając w to nawet najbardziej nietypowe sytuacje."
    }

    # predefined fields
    policy_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    policy_type = models.ForeignKey(HousePolicyType, on_delete=models.CASCADE, blank=False,
                                    null=False)
    valid_to = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    # form fields
    house_type = models.CharField(max_length=100, choices=HOUSE_TYPES)
    number_of_owners = models.PositiveSmallIntegerField(default=1)
    house_area = models.PositiveIntegerField()
    house_city = models.CharField(max_length=50)
    house_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Nazwa polisy: {self.policy_name}"
