from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

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
        }
    })

urlpatterns = [
    path("", root_view, name="root"),
    path("admin/", admin.site.urls),

    path("accounts/", include(("apps.accounts.urls", "accounts"), namespace="accounts")),
    path("rbac/", include(("apps.rbac.urls", "rbac"), namespace="rbac")),
    path("geo/", include(("apps.geo.urls", "geo"), namespace="geo")),
    path("shipments/", include(("apps.shipments.urls", "shipments"), namespace="shipments")),
    path("vehicles/", include(("apps.vehicles.urls", "vehicles"), namespace="vehicles")),
    path("routes/", include(("apps.routes.urls", "routes"), namespace="routes")),

    
]

