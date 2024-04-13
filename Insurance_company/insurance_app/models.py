from django.db import models
from _datetime import datetime, date
import uuid

from accounts.models import Customer
from utils.validators import validate_future_date, validate_past_date


# time functions


def current_year():
    return datetime.today().year


def generate_id():
    now = datetime.now()
    str_time = now.strftime('%Y%m%d%H%M%S')
    id_key = (str_time + str(uuid.uuid4())[:5]).upper()
    return id_key


class CarPolicyFactors(models.Model):
    base = models.FloatField(default=600)
    age_factor = models.FloatField(default=1)
    mileage_factor_1 = models.FloatField(default=0.002)
    mileage_factor_2 = models.FloatField(default=0.0033)
    mileage_factor_3 = models.FloatField(default=0.0044)
    avg_year_mileage_1 = models.FloatField(default=0.05)
    avg_year_mileage_2 = models.FloatField(default=0.07)
    avg_year_mileage_3 = models.FloatField(default=0.09)
    avg_year_mileage_4 = models.FloatField(default=0.1)
    rented_factor_1 = models.FloatField(default=1)
    rented_factor_2 = models.FloatField(default=3)
    owners_factor_1 = models.FloatField(default=1)
    owners_factor_2 = models.FloatField(default=1.2)
    owners_factor_3 = models.FloatField(default=1.8)
    owners_factor_4 = models.FloatField(default=2)

    fuel_dict = {
        "Gasoline": 1,
        "Diesel": 1.2,
        "LPG": 1.4,
        "Electric": 1.7,
        "Hydrogen": 1.85,
        "Biodiesel": 1.5
    }

class HousePolicyFactors(models.Model):
    house_dict = {
        "Dom": 1,
        "Szeregowiec": 2,
        "Mieszkanie": 3
        }

class PolicyStatus(models.Model):
    STATUS_CHOICES = {
        "Active": "Your car is protected - policy is up to date.",
        "Expired": "Policy is expired"
    }


class CarPolicyType(models.Model):
    policy_type = models.CharField(primary_key=True, max_length=100)
    policy_description = models.TextField()
    type_factor = models.FloatField()

    def __str__(self):
        return self.policy_type

    def __repr__(self):
        return self.policy_type


class HousePolicyType(models.Model):
    policy_type = models.CharField(primary_key=True, max_length=100)
    policy_description = models.TextField()
    type_factor = models.FloatField()

    def __str__(self):
        return self.policy_type

    def __repr__(self):
        return self.policy_type


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

    MARK_AND_MODELS = (
        ("Toyota Corolla", "Toyota Corolla"),
        ("Skoda Octavia", "Skoda Octavia"),
        ("Toyota Yaris", "Toyota Yaris"),
        ("Toyota Yaris Cross:", "Toyota Yaris Cross"),
        ("Kia Sportage", "Kia Sportage"),
        ("Toyota C-HR", "Toyota C-HR"),
        ("Dacia Duster", "Dacia Duster"),
        ("Toyota RAV4", "Toyota RAV4"),
        ("Volkswagen T-Roc", "Volkswagen T-Roc"),
        ("Kia Ceed", "Kia Ceed"),
        ("BMW X3", "BMW X3"),
        ("Kia Stonic", "Kia Stonic"),
        ("Audi A4", "Audi A4"),
        ("BMW Serii 3", "BMW Serii 3"),
        ("Audi Q3", "Audi Q3"),
        ("Audi Q5", "Audi Q5"),
        ("Lexus NX", "Lexus NX"),
        ("Suzuki Vitara", "Suzuki Vitara"),
        ("Volkswagen Golf", "Volkswagen Golf"),
        ("Nissan Qashqai", "Nissan Qashqai"),
        ("Audi A3", "Audi A3"),
        ("Renault Clio", "Renault Clio"),
        ("Volkswagen Passat", "Volkswagen Passat"),
        ("Dacia Sandero", "Dacia Sandero"),
    )

    # predefined fields

    policy_id = models.CharField(primary_key=True, max_length=19, editable=False, unique=True,
                                 default=generate_id)
    policy_type = models.ForeignKey(CarPolicyType, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    valid_to = models.DateField(validators=[validate_future_date])
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    # form fields
    car_mark_model = models.CharField(max_length=100, choices=MARK_AND_MODELS)
    production_year = models.PositiveIntegerField(default=current_year(), validators=[validate_past_date])
    fuel_type = models.CharField(max_length=100, choices=FUEL_TYPES)
    mileage = models.PositiveIntegerField()
    average_year_mileage = models.PositiveIntegerField(choices=AVERAGE_YEAR_MILEAGE)
    is_rented = models.BooleanField(default=False)
    number_of_owners = models.PositiveSmallIntegerField()
    driver_under_26 = models.BooleanField(default=False)

    def __str__(self):
        return f"Nazwa polisy: {self.policy_type}"

    def __repr__(self):
        return f"Nazwa polisy: {self.policy_type}"

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

    # predefined fields

    policy_id = models.CharField(primary_key=True, max_length=19, editable=False, unique=True,
                                 default=generate_id)
    policy_type = models.ForeignKey(HousePolicyType, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    valid_to = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    # form fields
    house_type = models.CharField(max_length=100, choices=HOUSE_TYPES)
    number_of_owners = models.PositiveSmallIntegerField(default=1)
    house_area = models.PositiveIntegerField()
    house_city = models.CharField(max_length=50)
    house_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Nazwa polisy: {self.policy_type}"

    def __repr__(self):
        return f"Nazwa polisy: {self.policy_type}"
