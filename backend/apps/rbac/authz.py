from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

CRUD = {"read", "create", "update", "delete"}

def _perm_codes(user):
    """Return a cached set like {'shipments.read', 'vehicles.update'}."""
    if not user.is_authenticated:
        return set()
    cache = getattr(user, "_perm_codes_cache", None)
    if cache is None:
        from apps.rbac.models import Permission
        qs = Permission.objects.filter(
            group_permissions__group__user_groups__user=user
        ).values_list("app_label", "codename")
        cache = {f"{a}.{c}" for a, c in qs}
        user._perm_codes_cache = cache
    return cache

def require_code(code: str):
    """Require an exact permission code (e.g., 'alerts.resolve')."""
    def deco(view):
        @login_required
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if code not in _perm_codes(request.user):
                return JsonResponse({"detail": "Forbidden"}, status=403)
            return view(request, *args, **kwargs)
        return wrapped
    return deco

def require_read(app_label: str):
    """For GET endpoints."""
    return require_code(f"{app_label}.read")

def require_set(app_label: str):
    """
    For POST “SET” endpoints.
    Expects body.action in {'create','update','delete'} and checks '<app>.<action>'.
    """
    def deco(view):
        @login_required
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            try:
                payload = json.loads(request.body or "{}")
            except Exception:
                return JsonResponse({"detail": "Invalid JSON"}, status=400)

            action = (payload.get("action") or "").lower()
            if action not in {"create", "update", "delete"}:
                return JsonResponse({"detail": "Unknown action"}, status=400)

            request._json = payload  # let the view reuse the parsed body
            if f"{app_label}.{action}" not in _perm_codes(request.user):
                return JsonResponse({"detail": "Forbidden"}, status=403)
            return view(request, *args, **kwargs)
        return wrapped
    return deco
