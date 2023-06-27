from django.core.serializers import serialize
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import StaffAuthForm
from .models import Vehicle, Enterprise, Routes
from .serializers import VehicleSerializer, PathSerializer, LocationSerializer
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required



class VehicleAPIView(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAdminUser,)

class VehicleAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleAPIList(generics. ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


def index(request):
    vehicles = Vehicle.objects.all().order_by('brand')[:8]
    enterprises = Enterprise.objects.all().order_by('name')
    context = {'vehicles': vehicles, 'enterprises':enterprises}
    return render(request, 'index.html', context=context)

def vehicleview(request):
    vehicles = Vehicle.objects.all().order_by('brand')[:8]
    context = {'vehicles': vehicles}
    return render(request, 'vehicle.html', context=context)

def enterpriseview(request):
    enterprises = Enterprise.objects.all().order_by('name')
    context = {'enterprises':enterprises}
    return render(request, 'enterprise.html', context=context)

class CreateEnterprise(CreateView):
    model = Enterprise
    template_name = 'create_enterprise_form.html'
    fields = ['name','address','num_of_employee']
    success_url = reverse_lazy('enterprise')

class CreateVehicle(CreateView):
    model = Vehicle
    template_name = 'create_vehicle_form.html'
    fields = ['year_manufacture','mileage','price','brand','owner']
    success_url = reverse_lazy('vehicle')


class VehicleUpdateView(UpdateView):
    model = Vehicle
    template_name = 'vehicle_update_form.html'
    fields = ['year_manufacture','mileage','price','brand','owner']

class EnterpriselUpdateView(UpdateView):
    model = Enterprise
    template_name = 'enterprise_update_form.html'
    fields = ['name','address','num_of_employee']

class VehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = 'vehicle_delete_form.html'
    success_url = reverse_lazy('vehicle')

class EnterpriseDeleteView(DeleteView):
    model = Enterprise
    template_name = 'enterprise_delete_form.html'
    fields = ['name','address','num_of_employee']

class PathViewSet(generics.ListAPIView):
    queryset = Routes.objects.all()
    serializer_class = PathSerializer
    fields = ['id', 'car', 'route','timestamp']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['car','timestamp']
    serialize('geojson', Routes.objects.all(),
              geometry_field='route',
              fields=('id', 'car', 'route','timestamp'))

class LocationView(APIView):
    def get(self, request):
        locations = Routes.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)