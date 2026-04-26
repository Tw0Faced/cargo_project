from django.contrib import admin
from .models import *

admin.site.register(Clients)
admin.site.register(Cargo)
admin.site.register(Transports)
admin.site.register(Routes)
admin.site.register(Shipments)
admin.site.register(Drivers)
admin.site.register(Dispatchers)