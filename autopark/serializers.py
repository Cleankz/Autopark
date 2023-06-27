from rest_framework import serializers
from .models import Vehicle, Routes



class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('year_manufacture','mileage','price','brand','owner')


class PathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = ('id', 'car', 'route','timestamp')

class LocationSerializer(serializers.Serializer):
    class Meta:
        model = Routes
        geo_field = "route"
        fields = ('id', 'car', 'route','timestamp')