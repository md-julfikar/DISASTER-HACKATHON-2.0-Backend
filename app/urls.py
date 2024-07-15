from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Weather API",
        default_version='v1',
        description="Basic documentation for the Weather API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@weatherapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", views.home, name='home'),
    path("api/", views.WeatherView, name='api'),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
