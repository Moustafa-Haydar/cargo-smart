from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),
    path('accounts/', include("apps.accounts.urls")),
    path('rbac/', include("apps.rbac.urls")),
    
]

