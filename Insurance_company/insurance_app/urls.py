from django.urls import path

from insurance_app.views import OfferListView, OfferDetailView

urlpatterns = [
    path('offer_list/', OfferListView.as_view(), name='offer_list'),
    path('offer_detail/', OfferDetailView.as_view(), name='offer_detail'),
]