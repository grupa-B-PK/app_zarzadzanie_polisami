from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound

from .forms import CarInsuranceModelForm, HouseInsuranceModelForm
from .models import CarPolicyType, CarInsurance, HousePolicyType, HouseInsurance


class IndexView(TemplateView):
    template_name = 'index'


class MainPageView(TemplateView):
    template_name = 'main_page'


class OfferCarView(View):
    def get(self, request, *args, **kwargs):
        car_policies = CarPolicyType.objects.all()
        context = {'car_policies': car_policies}
        return render(request, 'offer_car.html', context)


class OfferHouseView(View):
    def get(self, request, *args, **kwargs):
        policy_types = HouseInsurance.POLICY_TYPES
        policy_descriptions = HouseInsurance.POLICY_DESC
        ctx = {'policy_types': policy_types, 'policy_descriptions': policy_descriptions}
        return render(request, 'offer_house.html', ctx)


@login_required
def policy_list(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        car_insurances = CarInsurance.objects.filter(customer=customer)
        house_insurances = HouseInsurance.objects.filter(customer=customer)
        return render(request, 'policy_list.html',
                      {'car_insurances': car_insurances, 'house_insurances': house_insurances})
    else:
        return redirect('login')


@login_required
def policy_car_create(request):
    if request.method == "POST":
        car_policy_form = CarInsuranceModelForm(request.POST)
        if car_policy_form.is_valid():
            request.session['car_policy_data'] = request.POST.dict()  # Zapisanie danych formularza w sesji
            return redirect("policy_car_confirm")
    else:
        car_policy_form = CarInsuranceModelForm()
    return render(request, "policy_car_create.html", {"car_policy_form": car_policy_form})


@login_required
def policy_car_confirm(request):
    if 'car_policy_data' in request.session:
        car_policy_data = request.session['car_policy_data']
        car_policy_form = CarInsuranceModelForm(car_policy_data)
        if request.method == "POST":
            if car_policy_form.is_valid():
                car_policy = car_policy_form.save(commit=False)
                car_policy.customer = request.user.customer
                car_policy.save()
                del request.session['car_policy_data']  # Usunięcie danych formularza z sesji po zapisie
                return redirect("policy_car_detail", policy_id=car_policy.policy_id)
        return render(request, "policy_car_confirm.html", {"car_policy_form": car_policy_form})
    else:
        return redirect("policy_car_create")


@login_required
def policy_car_detail(request, policy_id):
    try:

        car_policy = CarInsurance.objects.get(policy_id=policy_id)
    except CarInsurance.DoesNotExist:
        return HttpResponseNotFound("Page Not Found")
    ctx = {
        "car_policy": car_policy,
    }

    return render(request, "policy_car_detail.html", context=ctx)


@login_required
def policy_house_create(request):
    if request.method == "POST":
        house_policy_form = HouseInsuranceModelForm(request.POST)
        if house_policy_form.is_valid():
            request.session['house_policy_data'] = request.POST.dict()  # Zapisanie danych formularza w sesji
            return redirect("policy_house_confirm")
    else:
        house_policy_form = HouseInsuranceModelForm()
    return render(request, "policy_house_create.html", {"house_policy_form": house_policy_form})


def policy_house_confirm(request):
    if 'house_policy_data' in request.session:
        house_policy_data = request.session['house_policy_data']
        house_policy_form = HouseInsuranceModelForm(house_policy_data)
        if request.method == "POST":
            if house_policy_form.is_valid():
                house_policy = house_policy_form.save(commit=False)
                house_policy.customer = request.user.customer
                house_policy.save()
                del request.session['house_policy_data']  # Usunięcie danych formularza z sesji po zapisie
                return redirect("policy_house_detail", policy_id=house_policy.policy_id)
        return render(request, "policy_house_confirm.html", {"house_policy_form": house_policy_form})
    else:
        return redirect("policy_house_create")


@login_required
def policy_house_detail(request, policy_id):
    try:
        house_policy = HouseInsurance.objects.get(policy_id=policy_id)
    except CarInsurance.DoesNotExist:
        return HttpResponseNotFound("Page Not Found")
    ctx = {
        "house_policy": house_policy,
    }

    return render(request, "policy_house_detail.html", context=ctx)
