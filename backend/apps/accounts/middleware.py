from django.http import JsonResponse
from django.conf import settings
from apps.rbac.models import Group

class RequireAdminGroupMiddleware:
    """
    Blocks access to selected endpoints unless the logged-in user is in an ADMIN group.
    - Admin groups default to ["Admin"] and can be overridden via settings.RBAC_ADMIN_GROUPS = ["Admin", ...]
    - Superusers are always allowed.
    """

    PROTECTED_PATH_PREFIXES = (
        "/accounts/users/",
        "/accounts/users/create/",
        "/accounts/users/update/",
        "/accounts/users/delete/",
    )

    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_group_names = set(getattr(settings, "RBAC_ADMIN_GROUPS", ["Admin"]))

    def __call__(self, request):
        # Only guard selected endpoints
        if not any(request.path.startswith(p) for p in self.PROTECTED_PATH_PREFIXES):
            return self.get_response(request)

        # Must be authenticated
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return JsonResponse({"detail": "Authentication required"}, status=401)

        # Always allow Django superusers
        if getattr(user, "is_superuser", False):
            return self.get_response(request)

        # Check group membership (case-insensitive match)
        is_admin = Group.objects.filter(
            user_groups__user_id=user.id,
            name__in=self.admin_group_names
        ).exists()

        if not is_admin:
            return JsonResponse({"detail": "Admin access required"}, status=403)

        return self.get_response(request)
