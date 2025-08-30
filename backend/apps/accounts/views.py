import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.middleware.csrf import get_token


def _user_payload(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }


@require_GET
@ensure_csrf_cookie
def csrf(request):
    """Return a CSRF token (also sets csrftoken cookie)."""
    token = get_token(request)        # same token as the cookie
    return JsonResponse({"csrfToken": token})


@require_POST
@csrf_protect
def login(request):
    """
    Accepts JSON {username, password}.
    On success: creates a Django session and sets the session cookie.
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return HttpResponseBadRequest("username and password are required")

    user = authenticate(request, username=username, password=password)
    if not user:
        return JsonResponse({"ok": False, "error": "Invalid credentials"}, status=401)

    auth_login(request, user)  # sets sessionid cookie
    return JsonResponse({"ok": True, "user": {"id": user.id, "username": user.username}})


@require_POST
@csrf_protect
def logout(request):
    """Logs out by clearing the server-side session and expiring the cookie."""
    logout(request)
    return JsonResponse({"ok": True})


@require_GET
def me(request):
    """Returns who you are based on the session cookie."""
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True, "user": _user_payload(request.user)})
    return JsonResponse({"authenticated": False}, status=401)


@require_POST
# @csrf_protect
# @staff_or_super_required
def create_user(request):
    """
    Body: { "username": str, "email": str, "password": str, "role": pk? }
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password")
    role = bool(data.get("role", False))

    if not username or not password:
        return HttpResponseBadRequest("username and password are required")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"detail": "username already exists"}, status=409)

    user = User.objects.create_user(username=username, email=email, password=password)
    if role:
        user.role = True
        user.save(update_fields=["role"])

    return JsonResponse({"created": True, "user": _user_payload(user)}, status=201)