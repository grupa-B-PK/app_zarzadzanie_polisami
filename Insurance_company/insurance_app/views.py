from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

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

class PolicyDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        car_insurance = get_object_or_404(CarInsurance, id=id)
        house_insurance = get_object_or_404(HouseInsurance, id=id)
        ctx = {'car_insurance': car_insurance, 'house_insurance': house_insurance}
        return render(request, 'policy_detail.html', ctx)