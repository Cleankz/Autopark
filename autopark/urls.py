from django.template.defaulttags import url
from django.urls import path

from django.urls import path
from . import views
from .views import LocationView

urlpatterns = [
    path('', views.index, name='home'),
    path('enterprise/', views.enterpriseview, name='enterprise'),
    path('enterprise/create', views.CreateEnterprise.as_view(), name='createenterprise'),
    path('vehicle/', views.vehicleview, name='vehicle'),
    path('vehicle/create', views.CreateVehicle.as_view(), name='createvehicle'),
    path('vehicle/update/<pk>', views.VehicleUpdateView.as_view(), name="updatevehicle"),
    path('vehicle/delete/<pk>', views.VehicleDeleteView.as_view(), name="deletevehicle"),
    path('enterprise/update/<pk>', views.EnterpriselUpdateView.as_view(), name="updateenterprise"),
    path('enterprise/delete/<pk>', views.EnterpriseDeleteView.as_view(), name="deleteenterprise"),
    path('path/', views.PathViewSet.as_view(), name="path"),
    path('locations/', LocationView.as_view(), name="location_list"),
]
