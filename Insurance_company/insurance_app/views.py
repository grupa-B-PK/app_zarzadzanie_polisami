from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView

from .models import CarInsurance, HouseInsurance

class IndexView(TemplateView):
    template_name = 'index'

class PolicyListView(ListView):
    template_name = 'policy_list.html'
    context_object_name = 'policy_list'

    def get_queryset(self):
        car_insurances = CarInsurance.objects.all()
        house_insurances = HouseInsurance.objects.all()
        return list(car_insurances) + list(house_insurances)