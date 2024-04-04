from django.urls import path

from insurance_app.views import OfferListView, OfferDetailView, policy_car_create, policy_car_detail

urlpatterns = [
    path('offer_list/', OfferListView.as_view(), name='offer_list'),
    path('offer_detail/', OfferDetailView.as_view(), name='offer_detail'),
    path('offer_detail/', OfferDetailView.as_view(), name='offer_detail'),
    path("policy_car_create/", policy_car_create),
    path("policy_car_detail/<uuid:policy_id>", policy_car_detail, name='policy_car_detail'),
]