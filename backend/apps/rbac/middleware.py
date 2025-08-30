# backend/apps/accounts/middleware.py
from django.http import JsonResponse
from django.urls import resolve

class RequireAdminRoleMiddleware:
    """
    Blocks access to selected endpoints unless the logged-in user's role_id == 1.
    Uses session first (set at login).
    """

    PROTECTED_PATH_PREFIXES = ("/rbac/addRole/",)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if request path starts with one of the protected prefixes
        if any(request.path.startswith(prefix) for prefix in self.PROTECTED_PATH_PREFIXES):
            if not request.user.is_authenticated:
                return JsonResponse({"detail": "Authentication required"}, status=401)

            # Prefer role_id from session
            role_id = request.session.get("role_id")

            if role_id is None:
                # Fallback: check attribute directly on user
                role_id = getattr(request.user, "role_id", None)
                if role_id is None and isinstance(getattr(request.user, "role", None), bool):
                    # If you store role as boolean (True = admin)
                    role_id = 1 if request.user.role else 0

            if role_id != 1:
                return JsonResponse({"detail": "Admin access required"}, status=403)

        return self.get_response(request)
