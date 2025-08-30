from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpResponseBadRequest
from .utils import _user_payload
from apps.rbac.models import Role
from ..models import User
import json


@require_POST
@csrf_protect
def create_user(request):
    """
    Body: { "username": str, "email": str, "password": str, "role_id": pk? }
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    username = (data.get("username") or "").strip()
    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password")
    role_id = data.get("role_id")

    if not username or not password:
        return HttpResponseBadRequest("username and password are required")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"detail": "username already exists"}, status=409)

    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)

    if role_id:
        # Validate FK exists before assigning
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            return JsonResponse({"detail": "invalid role_id"}, status=400)
        user.role = role
        user.save(update_fields=["role"])

    return JsonResponse({"created": True, "user": _user_payload(user)}, status=201)