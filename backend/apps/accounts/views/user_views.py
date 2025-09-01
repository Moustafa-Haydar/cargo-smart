from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .utils import _user_payload
import json
from ..models import User
from django.apps import apps
from apps.rbac.models import Group, Permission, UserGroup, GroupPermission


def _user_payload(user):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
    }


def _parse_json(request):
    try:
        return json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON")


@login_required
@require_GET
def users(request):
    # TODO: check a specific permission, e.g., "accounts.view_user"
    qs = User.objects.all().order_by("username")
    data = [_user_payload(u) for u in qs]
    return JsonResponse({"users": data})


@login_required
@require_POST
@csrf_protect
@transaction.atomic
def create_user(request):
    """
    Body (JSON):
      {
        "username": str,
        "email": str,
        "password": str,
        "first_name": str?, 
        "last_name": str?,
        "group": str?   # e.g. "manager" or "admin" ...
      }
    """
    try:
        data = _parse_json(request)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    group_name = (data.get("group")      or "").strip()

    if not username or not password:
        return HttpResponseBadRequest("username and password are required")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"detail": "username already exists"}, status=409)
    if email and User.objects.filter(email=email).exists():
        return JsonResponse({"detail": "email already exists"}, status=409)

    group = None
    if group_name:
        Group = apps.get_model("rbac", "Group")
        try:
            group = Group.objects.get(name__iexact=group_name)
        except Group.DoesNotExist:
            return JsonResponse(
                {"detail": f"Group '{group_name}' does not exist"},
                status=400
            )

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
    except:
        return JsonResponse({"detail": "username or email already exists"}, status=409)

    if group:
        UserGroup = apps.get_model("rbac", "UserGroup")
        UserGroup.objects.get_or_create(user_id=user.id, group_id=group.id)

    return JsonResponse({"created": True, "user": _user_payload(user)}, status=201)


@login_required
@require_POST
@csrf_protect
@transaction.atomic
def update_user(request):
    """
    Body:
      {
        "id": uuid (required),
        "username": str?, "email": str?,
        "first_name": str?, "last_name": str?,
        "password": str?,                 # optional password reset
        "group_ids": [uuid, ...]?         # full replacement of memberships if provided
      }
    """
    try:
        data = _parse_json(request)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    user_id = data.get("id")
    if not user_id:
        return HttpResponseBadRequest("id is required")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"detail": "User not found"}, status=404)

    username = (data.get("username") or "").strip() or None
    email = (data.get("email") or "").strip() or None

    # Uniqueness checks only when provided
    if username and User.objects.filter(username=username).exclude(id=user_id).exists():
        return JsonResponse({"detail": "username already exists"}, status=409)
    if email and User.objects.filter(email=email).exclude(id=user_id).exists():
        return JsonResponse({"detail": "email already exists"}, status=409)

    # Apply updates
    for field in ("first_name", "last_name"):
        if field in data and data[field] is not None:
            setattr(user, field, (data[field] or "").strip())
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if data.get("password"):
        user.set_password(data["password"])

    user.save()

    # Replace group memberships if group_ids provided
    if "group_ids" in data and isinstance(data["group_ids"], list):
        new_ids = set(data["group_ids"])
        # delete old
        UserGroup.objects.filter(user=user).exclude(group_id__in=new_ids).delete()
        # add new
        existing = set(UserGroup.objects.filter(user=user).values_list("group_id", flat=True))
        to_add = [gid for gid in new_ids if gid not in existing]
        groups = Group.objects.filter(id__in=to_add)
        UserGroup.objects.bulk_create([UserGroup(user=user, group=g) for g in groups], ignore_conflicts=True)

    return JsonResponse({"updated": True, "user": _user_payload(user)})


@login_required
@require_POST
@csrf_protect
@transaction.atomic
def delete_user(request):
    """
    Body: { "id": uuid }
    """
    try:
        data = _parse_json(request)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    user_id = data.get("id")
    if not user_id:
        return HttpResponseBadRequest("id is required")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"detail": "User not found"}, status=404)

    user.delete()
    return JsonResponse({"deleted": True})