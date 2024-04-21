from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import LogoutConfirmView, RegisterView, CustomerDetailView, CustomerUpdateView, CustomerPasswordChangeView

urlpatterns = [
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="accounts/logged_out.html"), name="logout"),
    path("logout_confirm/", LogoutConfirmView.as_view(), name="logout_confirm"),
    path("register/", RegisterView.as_view(), name="register"),
    path("customer_detail/<int:pk>", CustomerDetailView.as_view(), name="customer_detail"),
    path("customer_detail/<int:pk>/update/", CustomerUpdateView.as_view(), name="customer_update"),
    path("customer_detail/<int:pk>/password_change", CustomerPasswordChangeView.as_view(), name="password_change"),
]