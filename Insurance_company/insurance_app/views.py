from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .models import CarInsurance, HouseInsurance

class IndexView(TemplateView):
    template_name = 'index'

class OfferListView(ListView):
    template_name = 'offer_list.html'
    context_object_name = 'offer_list'

    def get_queryset(self):
        car_insurances = CarInsurance.objects.all()
        house_insurances = HouseInsurance.objects.all()
        return list(car_insurances) + list(house_insurances)

class OfferDetailView(View):
    def get(self, request, *args, **kwargs):
        car_insurance = CarInsurance.objects.all()
        house_insurance = HouseInsurance.objects.all()
        ctx = {'car_insurance': car_insurance, 'house_insurance': house_insurance}
        return render(request, 'offer_detail.html', ctx)