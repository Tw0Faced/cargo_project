from rest_framework import viewsets
from django.shortcuts import render, redirect

from .models import *
from .serializers import *
from .forms import *


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = ClientSerializer


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class TransportViewSet(viewsets.ModelViewSet):
    queryset = Transports.objects.all()
    serializer_class = TransportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Routes.objects.all()
    serializer_class = RouteSerializer


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipments.objects.all()
    serializer_class = ShipmentSerializer


def index(request):

    form_classes = {
        'client': ClientForm,
        'cargo': CargoForm,
        'driver': DriverForm,
        'transport': TransportForm,
        'route': RouteForm,
        'dispatcher': DispatcherForm,
        'shipment': ShipmentForm,
    }

    forms = {
        'client_form': ClientForm(),
        'cargo_form': CargoForm(),
        'driver_form': DriverForm(),
        'transport_form': TransportForm(),
        'route_form': RouteForm(),
        'dispatcher_form': DispatcherForm(),
        'shipment_form': ShipmentForm(),
    }

    if request.method == 'POST':

        form_type = request.POST.get('form_type')
        form_class = form_classes.get(form_type)

        if form_class:

            form = form_class(request.POST)

            if form.is_valid():
                form.save()
                return redirect('index')

            else:
                forms[f'{form_type}_form'] = form

    context = {
        **forms,

        'clients': Clients.objects.all(),
        'cargo_list': Cargo.objects.all(),
        'drivers': Drivers.objects.all(),
        'transports': Transports.objects.all(),
        'routes': Routes.objects.all(),
        'dispatchers': Dispatchers.objects.all(),
        'shipments': Shipments.objects.all(),
    }

    return render(request, 'index.html', context)