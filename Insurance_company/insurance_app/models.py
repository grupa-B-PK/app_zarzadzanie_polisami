from django.db import models
from _datetime import datetime
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator


# time functions

def current_year():
    return datetime.date.today().year


def generate_id():
    now = datetime.now()
    str_time = now.strftime('%Y%m%d%H%M%S')
    id_key = str(uuid.uuid4())[:5]+str_time
    return id_key


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
        (1, "Poniżej 5 tys. km"), # kategorie przebiegu do wykorzystania w kalkulatorze
        (2, "do 10 tys. km"),
        (3, "do 20 tys. km"),
        (4, "powyżej 20 tys. km")
    )

    # predefined fields
    policy_id = models.CharField(generate_id(), primary_key=True)
    policy_name = models.CharField(max_length=100)
    policy_description = models.TextField(max_length=2000)
    valid_to = models.DateField(auto_now=True)
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


class HouseInsurance(models.Model):

    HOUSE_TYPES = (
        (1, "Dom"),
        (2, "Szeregowiec"),
        (3, "Mieszkanie")
    )

    # predefined fields
    policy_id = models.CharField(generate_id(), primary_key=True)
    policy_name = models.CharField(max_length=100)
    policy_description = models.TextField(max_length=2000)
    valid_to = models.DateField(auto_now=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    # form fields
    house_type = models.CharField(max_length=100, choices=HOUSE_TYPES)
    number_of_owners = models.PositiveSmallIntegerField(default=1)
    house_area = models.PositiveIntegerField()
    house_city = models.CharField(max_length=50)

    def __str__(self):
        return f"Nazwa polisy: {self.policy_name}"






