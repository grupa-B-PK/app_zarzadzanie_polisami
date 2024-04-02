from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import View


class LogoutConfirmView(View):
    def get(self, request):
        return render(request, "accounts/logout.html")


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/index/')
        form = UserCreationForm()
        ctx = {
            "form": form
        }

        return render(request, "accounts/register.html", ctx)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        ctx = {
            "form": form,
        }

        return render(request, "accounts/register.html", ctx)



