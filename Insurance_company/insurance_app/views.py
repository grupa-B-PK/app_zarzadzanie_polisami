from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound

from .forms import CarInsuranceModelForm
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


def policy_car_create(request):
    car_policy_form = CarInsuranceModelForm()
    if request.method == "GET":
        ctx = {
            "car_policy_form": car_policy_form,
        }
        return render(request, "policy_car_create.html", context=ctx)
    if request.method == "POST":
        car_policy_form = CarInsuranceModelForm(request.POST)
        if car_policy_form.is_valid():
            policy = car_policy_form.save()
            return redirect(f"/insurance_app/policy_car_detail/{policy.policy_id}")
        ctx = {"car_policy_form": car_policy_form,
               "error": "Wystąpił błąd w formularzu"}
        return render(request, "policy_car_create.html", context=ctx)


def policy_car_detail(request, policy_id):
    try:

        car_policy = CarInsurance.objects.get(policy_id=policy_id)
    except CarInsurance.DoesNotExist:
        return HttpResponseNotFound("Page Not Found")
    ctx = {
        "car_policy": car_policy,
    }

    return render(request, "policy_car_detail.html", context=ctx)

