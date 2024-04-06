#from insurance_app.models import CarInsurance, HouseInsurance
from insurance_app.models import current_year
"""Scripts for calculatig price of insuraces for every each model
 To be merged after finishing CRUD forms
 """




#CarInsurance

base = 600
production_year = 2010
fuel_type = "LPG"
mileage = 350000
average_year_mileage = "do 10 tys. km"
is_rented = True
number_of_owners = 1




fuel_dict = {
    "Gasoline" : 1 ,
    "Diesel" : 1.2 ,
    "LPG": 1.4 ,
    "Electric": 1.7 ,
    "Hydrogen": 1.85 ,
    "Biodiesel": 1.5
}

age_factor = (current_year() - production_year) * 10


fuel_factor = fuel_dict[fuel_type]

def mileage_factor(mileage):
    if mileage < 100000:
        mileage_factor = (mileage // 1000) * 0.002
    elif mileage > 100000 and mileage < 250000:
        mileage_factor = (mileage // 1000) * 0.0033
    else: mileage_factor = (mileage // 1000) * 0.0044
    return mileage_factor

def avg_mil_factor(average_year_mileage):
    if average_year_mileage == 1:
        return 0.05
    if average_year_mileage == 2:
        return 0.07
    if average_year_mileage == 3:
        return 0.09
    else:
        return 0.1

def rented_factor(is_rented):
    if is_rented:
        rented_factor = 3
    else: rented_factor = 1
    return rented_factor

def owners_factor(number_of_owners):
    if number_of_owners > 1:
        owners_factor = 1.2
    elif number_of_owners > 1 and number_of_owners <= 3:
        owners_factor = 1.8
    elif number_of_owners > 3:
        owners_factor = 2
    else: owners_factor = 1
    return owners_factor

def calculate_price():
     return (base*fuel_factor*mileage_factor(mileage)*avg_mil_factor(average_year_mileage)*rented_factor(is_rented)*owners_factor(
         number_of_owners))+age_factor

print(calculate_price())