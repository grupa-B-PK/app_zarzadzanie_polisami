from insurance_app.models import current_year
from insurance_app.models import CarPolicyFactors

"""Scripts for calculatig price of insuraces for every each model
 To be merged after finishing CRUD forms
 """




class PolicyPriceCalculator:

    def __init__(self, production_year, fuel_factor, fuel_type, mileage, average_year_mileage, is_rented,
                 number_of_owners):
        try:
            self.car_policy_factors = CarPolicyFactors.objects.get(id=1)
        except CarPolicyFactors.DoesNotExist:
            print("Nie znaleziono obiektu CarPolicyFactors o podanym ID.")
        self.production_year = production_year
        self.fuel_type = fuel_type
        self.mileage = mileage
        self.average_year_mileage = average_year_mileage
        self.is_rented = is_rented
        self.number_of_owners = number_of_owners
        # self.age_factor = (current_year() - production_year) * CarPolicyFactors.age_factor
        self.fuel_factor = CarPolicyFactors.fuel_dict[fuel_type]

    def mileage_factor(self):
        if self.mileage < 100000:
            mileage_factor = (self.mileage // 1000) * self.car_policy_factors.mileage_factor_1
        elif self.mileage > 100000 and self.mileage < 250000:
            mileage_factor = (self.mileage // 1000) * self.car_policy_factors.mileage_factor_2
        else:
            mileage_factor = (self.mileage // 1000) * self.car_policy_factors.mileage_factor_3
        return mileage_factor

    def avg_mil_factor(self):
        if self.average_year_mileage == 1:
            return self.car_policy_factors.avg_year_mileage_1
        if self.average_year_mileage == 2:
            return self.car_policy_factors.avg_year_mileage_2
        if self.average_year_mileage == 3:
            return self.car_policy_factors.avg_year_mileage_3
        else:
            return self.car_policy_factors.avg_year_mileage_4

    def rented_factor(self):
        if self.is_rented:
            rented_factor = self.car_policy_factors.rented_factor_2
        else:
            rented_factor = self.car_policy_factors.rented_factor_1
        return rented_factor

    def owners_factor(self):
        if self.number_of_owners > 1:
            owners_factor = self.car_policy_factors.owners_factor_2
        elif self.number_of_owners > 1 and self.number_of_owners <= 3:
            owners_factor = self.car_policy_factors.owners_factor_3
        elif self.number_of_owners > 3:
            owners_factor = self.car_policy_factors.owners_factor_4
        else:
            owners_factor = self.car_policy_factors.owners_factor_1
        return owners_factor

    def calculate_price(self):
        return (self.car_policy_factors.base * self.fuel_factor * mileage_factor() * avg_mil_factor() *
                rented_factor() * owners_factor()) #+ self.age_factor