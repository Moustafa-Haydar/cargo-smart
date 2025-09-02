from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.http import JsonResponse, HttpResponseBadRequest
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
import json
from .utils import _user_payload, _user_permissions
from apps.accounts.models import User
from apps.rbac.models import Group, Permission, UserGroup, GroupPermission


@require_GET
@ensure_csrf_cookie
def csrf(request):
    """
    Returns a CSRF token and sets the csrftoken cookie.
    """
    token = get_token(request)
    return JsonResponse({"csrfToken": token})


@require_POST
@csrf_protect
def login(request):
    """
    Body: { "username": str, "password": str }
    Creates a Django session on success.
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    if not username or not password:
        return HttpResponseBadRequest("username and password are required")

    user = authenticate(request, username=username, password=password)
    if not user:
        return JsonResponse({"ok": False, "error": "Invalid credentials"}, status=401)

    auth_login(request, user)

    # Optional: cache permission ids in session for quick checks (invalidate on group updates)
    perm_ids, _ = _user_permissions(user)
    request.session["permission_ids"] = perm_ids

    return JsonResponse({"ok": True, "user": _user_payload(user)})


@require_POST
@csrf_protect
def logout(request):
    auth_logout(request)
    return JsonResponse({"ok": True})


@require_GET
def me(request):
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True, "user": _user_payload(request.user)})
    return JsonResponse({"authenticated": False}, status=401)