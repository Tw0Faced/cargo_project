from rest_framework import serializers
from .models import *

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'

class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transports
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipments
        fields = '__all__'