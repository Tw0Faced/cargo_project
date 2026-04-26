from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from core.views import *

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'cargo', CargoViewSet)
router.register(r'transports', TransportViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'shipments', ShipmentViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Cargo API",
        default_version='v1',
        description="API для грузоперевозок",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),

    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0)),
]
