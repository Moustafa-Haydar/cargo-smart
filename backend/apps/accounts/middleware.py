from django.http import JsonResponse
from django.conf import settings
from apps.rbac.models import Group
from fnmatch import fnmatch
from django.urls import resolve
from django.db.models.functions import Lower


class RequireAdminGroupMiddleware:
    """
    Allow only users in RBAC_ADMIN_GROUPS (or superusers) to access URLs
    whose qualified name matches any pattern in RBAC_ADMIN_PROTECTED.
    Example patterns: "accounts:*", "rbac:permissions-*"
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # case-insensitive set of allowed admin group names
        self.admin_group_names = {n.casefold() for n in getattr(settings, "RBAC_ADMIN_GROUPS", ["Admin"])}
        self.protected_patterns = list(getattr(settings, "RBAC_ADMIN_PROTECTED", []))

    def __call__(self, request):
        # Resolve to namespaced URL name like "accounts:users" or "rbac:permission-delete"
        try:
            match = resolve(request.path_info)
            parts = list(match.namespaces)
            if match.url_name:
                parts.append(match.url_name)
            qualified = ":".join(parts) if parts else ""
        except Exception:
            # If resolution fails (404 later), don't block here
            return self.get_response(request)

        # Not a protected endpoint? let it through
        if not any(fnmatch(qualified, pat) for pat in self.protected_patterns):
            return self.get_response(request)

        # Must be authenticated
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return JsonResponse({"detail": "Authentication required"}, status=401)

        # Superusers always allowed
        if getattr(user, "is_superuser", False):
            return self.get_response(request)

        # Case-insensitive membership in one of the admin groups
        is_admin = Group.objects.filter(
            user_groups__user_id=user.id
        ).annotate(name_l=Lower("name")).filter(
            name_l__in=self.admin_group_names
        ).exists()

        if not is_admin:
            return JsonResponse({"detail": "Admin access required"}, status=403)

        return self.get_response(request)
