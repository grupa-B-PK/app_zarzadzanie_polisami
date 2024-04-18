from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Customer
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

class CustomerDetailView(View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)

        if not request.user.is_authenticated:
            return render(request, "404.html")
        elif request.user.customer != customer:
            return render(request, "404.html")

        context = {
            'customer': customer,
        }

        return render(request, 'accounts/customer_detail.html', context)


class CustomerUpdateView(View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)

        if not request.user.is_authenticated:
            return render(request, "404.html")
        elif request.user.customer != customer:
            return render(request, "404.html")

        form = CustomerForm(instance=customer)
        context = {'form': form, 'customer': customer}

        return render(request, 'accounts/customer_update.html', context)

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(request.POST, instance=customer)

        if not request.user.is_authenticated:
            return render(request, "404.html")
        elif request.user.customer != customer:
            return render(request, "404.html")

        if form.is_valid():
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')

            if new_password1 and new_password1 == new_password2:
                customer.user.set_password(new_password1)
                customer.user.save()

            form.save()
            messages.success(request, "Pomyślnie wprowadzono nowe dane.")
            return redirect('customer_detail', pk=customer.pk)

        context = {'form': form, 'customer': customer}
        return render(request, 'accounts/customer_update.html', context)