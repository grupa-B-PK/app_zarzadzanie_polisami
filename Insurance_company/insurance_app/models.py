from django.db import models
from _datetime import datetime, date
import uuid

# time functions


def current_year():
    return datetime.today().year


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
        ("Poniżej 5 tys. km", "Poniżej 5 tys. km"), # kategorie przebiegu do wykorzystania w kalkulatorze
        ("do 10 tys. km", "do 10 tys. km"),
        ("do 20 tys. km", "do 20 tys. km"),
        ("powyżej 20 tys. km", "powyżej 20 tys. km")
    )

    POLICY_TYPES = (
        ("Standard OC", "Standard OC"),
        ("OC + AC", "OC + AC"),
        ("PREMIUM", "PREMIUM"),
    )

    POLICY_DESC = {
        "Standard OC" : "Ubezpieczenie odpowiedzialności cywilnej (OC) samochodu obejmuje przede wszystkim rekompensatę szkód, powstałych w wyniku spowodowania kolizji lub wypadku drogowego. Dotyczy to zarówno szkód osobowych, jak i materialnych. Co istotne, polisa OC przypisana jest do konkretnego samochodu, a nie do jego właściciela.",
        "OC + AC" : "Ubezpieczenie OC pokrywa szkody osoby przez nas poszkodowanej, z kolei odszkodowanie z tytułu AC likwiduje szkody własne. Zakres ubezpieczenia OC jest identyczny bez względu na zakład ubezpieczeń, zaś w przypadku polisy AC panuje pełna dowolność, dlatego oferta każdej firmy może być zupełnie inna.",
        "PREMIUM" : "Ubezpieczenie w Wariancie PREMIUM obejmuje utratę, zniszczenie lub uszkodzenie pojazdu wraz z wyposażeniem podstawowym, w zakresie szkody częściowej i całkowitej powstałej w wyniku zdarzeń nie wyłączonych z zakresu odpowiedzialności. Ubezpieczenie obejmuje parkowanie pojazdu po szkodzie w każdym wariancie."
    }


    # predefined fields
    policy_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    policy_name = models.CharField(max_length=100, unique=True)
    policy_type = models.CharField(max_length=100, choices=POLICY_TYPES, default="Standard OC")
    policy_description = models.TextField()
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
    def valid_to_status(self):
        if self.valid_to < date.today():
            return "Your car is protected - policy is up to date."
        else:
            return "Policy is expired"

    @property
    def get_desc(self):
        description = CarInsurance.POLICY_DESC[CarInsurance.policy_type]
        return description






class HouseInsurance(models.Model):

    HOUSE_TYPES = (
        ("Dom", "Dom"),
        ("Szeregowiec", "Szeregowiec"),
        ("Mieszkanie", "Mieszkanie")
    )

    # predefined fields
    policy_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    policy_name = models.CharField(max_length=100, unique=True)
    policy_description = models.TextField(max_length=2000)
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






