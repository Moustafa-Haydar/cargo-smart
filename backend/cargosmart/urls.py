from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include(("apps.accounts.urls", "accounts"), namespace="accounts")),
    path("rbac/",     include(("apps.rbac.urls", "rbac"), namespace="rbac")),
    path("shipments/",     include(("apps.shipments.urls", "shipments"), namespace="shipments")),
]

