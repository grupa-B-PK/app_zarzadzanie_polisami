from django.contrib import admin
from insurance_app.models import CarInsurance, HouseInsurance, CarPolicyType, HousePolicyType

admin.site.register(CarInsurance)
admin.site.register(HouseInsurance)
admin.site.register(CarPolicyType)
admin.site.register(HousePolicyType)




