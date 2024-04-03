from django.urls import path

from insurance_app.views import PolicyListView, PolicyDetailView

urlpatterns = [
    path('policy_list/', PolicyListView.as_view(), name='policy_list'),
    path('policy_detail/<int:id>/', PolicyDetailView.as_view(), name="policy_detail"),

]
