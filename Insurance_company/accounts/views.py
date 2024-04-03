from django.shortcuts import render, redirect
from django.views.generic import View

from accounts.forms import CustomerForm, CustomUserForm


class LogoutConfirmView(View):
    def get(self, request):
        return render(request, "accounts/logout.html")


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('login')
        user_form = CustomUserForm()
        customer_form = CustomerForm()
        ctx = {
            "user_form": user_form,
            "customer_form": customer_form,
        }

        return render(request, "accounts/register.html", ctx)

    def post(self, request):
        data = request.POST
        user_form = CustomUserForm(data)
        customer_form = CustomerForm(data)

        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            if self.create_customer_profile(user, customer_form):
                return redirect("login")
        ctx = {
            "user_form": user_form,
            "customer_form": customer_form,

        }

        return render(request, "accounts/register.html", ctx)

    def create_customer_profile(self, customer, form):
        customer_profile = form.save(commit=False)
        customer_profile.user = customer
        customer_profile.save()

        return customer_profile
