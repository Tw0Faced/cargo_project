from rest_framework import serializers
from .models import *

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ['c_id', 'c_type', 'c_name']
        extra_kwargs = {
            'c_id': {'read_only': True}
        }

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['g_id', 'g_name', 'g_weight', 'g_volume', 'g_type', 'c']
        extra_kwargs = {
            'g_id': {'read_only': True}
        }

class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transports
        fields = ['t_id', 't_mark', 't_model', 't_number', 't_cap', 'dr']
        extra_kwargs = {
            't_id': {'read_only': True}
        }

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = ['r_id', 'r_from', 'r_to', 'r_dist', 'r_time']
        extra_kwargs = {
            'r_id': {'read_only': True}
        }

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipments
        fields = ['tr_id', 'cargo', 'transport', 'route', 'client', 'tr_date_start', 'tr_date_end', 'tr_status']
        extra_kwargs = {
            'tr_id': {'read_only': True}
        }