from django.shortcuts import render
from django.views.generic import View, TemplateView

from .models import CarInsurance, HouseInsurance

class IndexView(TemplateView):
    template_name = 'index'

class PolicyListView(TemplateView):
    template_name = 'policy_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_insurances'] = CarInsurance.objects.all()
        context['house_insurances'] = HouseInsurance.objects.all()
        return context