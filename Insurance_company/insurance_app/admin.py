from django.contrib import admin
from insurance_app.models import CarInsurance, HouseInsurance, CarPolicyType, HousePolicyType, CarPolicyFactors, HousePolicyFactors

admin.site.register(CarInsurance)
admin.site.register(HouseInsurance)
admin.site.register(CarPolicyType)
admin.site.register(HousePolicyType)
admin.site.register(CarPolicyFactors)
admin.site.register(HousePolicyFactors)







