from django import forms
from .models import *


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'


class DriverForm(forms.ModelForm):
    class Meta:
        model = Drivers
        fields = '__all__'


class TransportForm(forms.ModelForm):
    class Meta:
        model = Transports
        fields = '__all__'


class RouteForm(forms.ModelForm):
    class Meta:
        model = Routes
        fields = '__all__'


class DispatcherForm(forms.ModelForm):
    class Meta:
        model = Dispatchers
        fields = '__all__'


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipments
        fields = '__all__'


class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individuals
        fields = '__all__'


class LegalEntityForm(forms.ModelForm):
    class Meta:
        model = LegalEntities
        fields = '__all__'


class LicenseForm(forms.ModelForm):
    class Meta:
        model = Licenses
        fields = '__all__'