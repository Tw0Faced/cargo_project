from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from core.views import *

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'cargo', CargoViewSet, basename='Грузы')
router.register(r'clients', ClientViewSet, basename='Клиенты')
router.register(r'transports', TransportViewSet, basename='Транспорт')
router.register(r'routes', RouteViewSet, basename='Маршруты')
router.register(r'shipments', ShipmentViewSet, basename='Перевозки')

schema_view = get_schema_view(
    openapi.Info(
        title="Система управления грузоперевозками",
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
