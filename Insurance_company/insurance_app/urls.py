from django.urls import path

from insurance_app.views import OfferListView, OfferDetailView,IndexView

urlpatterns = [
    path('index/', IndexView.as_view(template_name='index.html')),
    path('offer_list/', OfferListView.as_view(), name='offer_list'),
    path('offer_detail/', OfferDetailView.as_view(), name='offer_detail'),
]