from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpResponseBadRequest
from .utils import _user_payload
from apps.rbac.models import Role
from ..models import User
import json

def _user_payload(user):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
        "role": user.role_id
    }


@require_GET
@csrf_protect
def users(request):
    """
    List all users
    """
    users = User.objects.all()

    users_data = [_user_payload(user) for user in users]
    print(users_data)
    return JsonResponse({"users": users_data})


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


@require_POST
@csrf_protect
def update_user(request):
    """
    Update the user info
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    
    user_id = data.get("id")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    username = data.get("username")
    email = data.get("email")
    role = data.get("role")
    
    if not user_id:
        return HttpResponseBadRequest("user_id is required")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"detail": "User not found"}, status=404)
    
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if username:
        user.username = username
    if email:
        user.email = email
    if role:
        user.role = role

    if User.objects.filter(username=username).exclude(id=user_id).exists():
        return JsonResponse({"detail": "User with this username already exists"}, status=409)
    if User.objects.filter(email=email).exclude(id=user_id).exists():
        return JsonResponse({"detail": "User with this email already exists"}, status=409)
    
    user.save()
    return JsonResponse({"updated": True, "user": _user_payload(user)})