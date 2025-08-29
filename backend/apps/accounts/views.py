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

    login(request, user)              # <- creates session + sets session cookie
    return JsonResponse({"ok": True, "user": _user_payload(user)})

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
