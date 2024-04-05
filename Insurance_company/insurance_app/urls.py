from django.urls import path

from insurance_app.views import IndexView, MainPageView, OfferCarView, OfferHouseView, policy_car_create, \
    policy_car_detail, policy_house_detail, policy_house_create

urlpatterns = [
    path('index/', IndexView.as_view(template_name='index.html'), name='index'),
    path('main_page/', MainPageView.as_view(template_name='main_page.html'), name='main_page'),
    path('offer_car/', OfferCarView.as_view(), name='offer_car'),
    path('offer_house/', OfferHouseView.as_view(), name='offer_house'),
    path("policy_car_create/", policy_car_create, name='policy_car_create'),
    path("policy_car_detail/<uuid:policy_id>", policy_car_detail, name='policy_car_detail'),
    path("policy_house_create/", policy_house_create, name='policy_house_create'),
    path("policy_house_detail/<uuid:policy_id>", policy_house_detail, name='policy_house_detail'),
]