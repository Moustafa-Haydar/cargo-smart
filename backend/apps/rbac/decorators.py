from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .utils import has_perm


def require_perm(perm: str):
    def outer(view):
        @login_required
        @wraps(view)
        def inner(request, *args, **kwargs):
            if not has_perm(request.user, perm):
                return JsonResponse({"detail": "Forbidden", "required": perm}, status=403)
            return view(request, *args, **kwargs)
        return inner
    return outer
