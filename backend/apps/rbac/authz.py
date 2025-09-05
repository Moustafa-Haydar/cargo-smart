from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

ACTION_TO_PERM = {
    "read" : "read",
    "create": "create",
    "update": "update",
    "delete": "delete",
}

def _load_perm_codes_for_user(user):
    """
    Build codes like 'vehicles.view', 'shipments.update' from your join tables:
    """
    from apps.rbac.models import Permission
    if not user.is_authenticated:
        return set()
    qs = Permission.objects.filter(
        group_permissions__group__user_groups__user=user
    ).values_list("app_label", "codename")
    return {f"{app}.{code}" for app, code in qs}

def user_has_perm_code(user, code: str) -> bool:
    if not user.is_authenticated:
        return False
    cache = getattr(user, "_perm_codes_cache", None)
    if cache is None:
        cache = _load_perm_codes_for_user(user)
        user._perm_codes_cache = cache
    return code in cache

def require_perm_code(code: str):
    """Decorator: require a specific permission code like 'shipments.view'."""
    def deco(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not user_has_perm_code(request.user, code):
                return JsonResponse({"detail": "Forbidden"}, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped
    return deco

def require_view(app_label: str):
    """For GET endpoints: require '<app>.view'."""
    return require_perm_code(f"{app_label}.view")

def require_set_for_action(app_label: str):
    """
    For SET endpoints: inspect body.action in {'create','update','delete'}
    and require '<app>.<mapped action>'.
    """
    def deco(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            import json
            try:
                payload = json.loads(request.body.decode() or "{}")
            except Exception:
                return JsonResponse({"detail": "Invalid JSON"}, status=400)

            action = (payload.get("action") or "").lower().strip()
            mapped = ACTION_TO_PERM.get(action)
            if not mapped:
                return JsonResponse({"detail": "Unknown action; use create/update/delete"}, status=400)

            code = f"{app_label}.{mapped}"
            if not user_has_perm_code(request.user, code):
                return JsonResponse({"detail": "Forbidden"}, status=403)

            # stash parsed payload so view doesn’t re-parse
            request._json = payload
            return view_func(request, *args, **kwargs)
        return _wrapped
    return deco
