from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound

from .forms import CarInsuranceModelForm
from .models import CarInsurance, HouseInsurance


class IndexView(TemplateView):
    template_name = 'index'

class MainPageView(TemplateView):
    template_name = 'main_page'

class OfferCarView(View):
    def get(self, request, *args, **kwargs):
        policy_types = CarInsurance.POLICY_TYPES
        ctx = {'policy_types': policy_types}
        return render(request, 'offer_car.html', ctx)

class OfferHouseView(View):
    pass

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

