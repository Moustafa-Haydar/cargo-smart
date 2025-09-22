from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

def root_view(request):
    """Simple root endpoint for testing connectivity"""
    return JsonResponse({
        'message': 'CargoSmart Backend is running!',
        'status': 'success',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'accounts': '/accounts/',
            'shipments': '/shipments/',
            'vehicles': '/vehicles/',
            'routes': '/routes/',
            'rbac': '/rbac/',
            'geo': '/geo/',
            'agent_reroute': '/api/agentic/',
            'swagger': '/swagger/',
            'redoc': '/redoc/',
        }
    })

# Swagger/OpenAPI Schema Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="CargoSmart API",
        default_version='v1',
        description="""
        CargoSmart is an AI-powered intelligent logistics platform that leverages machine learning 
        and agentic AI to autonomously optimize delivery routes, predict delays, and automate 
        shipment management decisions in real-time.
        
        ## Features
        - Machine Learning Model for delay prediction with 86%+ accuracy
        - AI Agent for optimal route generation using Dijkstra's algorithm
        - N8N automation engine for real-time monitoring
        - Interactive Google Maps-powered operations center
        - Real-time vehicle tracking and shipment management
        
        ## Authentication
        This API supports both session-based and token-based authentication:
        - **Session Auth**: Use CSRF tokens for web applications
        - **Bearer Token**: Use JWT tokens for mobile applications
        """,
        terms_of_service="https://www.cargosmart.com/terms/",
        contact=openapi.Contact(email="contact@cargosmart.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", root_view, name="root"),
    path("admin/", admin.site.urls),

    # API endpoints
    path("accounts/", include(("apps.accounts.urls", "accounts"), namespace="accounts")),
    path("rbac/", include(("apps.rbac.urls", "rbac"), namespace="rbac")),
    path("geo/", include(("apps.geo.urls", "geo"), namespace="geo")),
    path("shipments/", include(("apps.shipments.urls", "shipments"), namespace="shipments")),
    path("vehicles/", include(("apps.vehicles.urls", "vehicles"), namespace="vehicles")),
    path("routes/", include(("apps.routes.urls", "routes"), namespace="routes")),
    path("api/agentic/", include(("apps.agent_reroute.urls", "agent_reroute"), namespace="agent_reroute")),

    # Swagger/OpenAPI Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

