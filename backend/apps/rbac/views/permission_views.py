import json
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.decorators.http import require_http_methods
from ..models import Role, Permission, RolePermission


@require_http_methods(["GET", "POST"])
@csrf_protect
def role_permissions(request, role_id):
    """
    GET  /roles/<role_id>/permissions/         -> list permissions for the role
    POST /roles/<role_id>/permissions/         -> change permissions
      body:
        {
          "action": "grant" | "revoke" | "set",   # default: "set"
          "permission_ids": ["uuid1", "uuid2", ...]
        }
    """
    role = get_object_or_404(Role, pk=role_id)

    if request.method == "GET":
        perms = (
            Permission.objects
            .filter(role_permissions__role=role)
            .values("id", "code", "description")
            .order_by("code")
        )
        return JsonResponse({"role_id": role.id, "permissions": list(perms)})

    # POST
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    action = (data.get("action") or "set").lower()
    ids = data.get("permission_ids", [])
    if not isinstance(ids, list):
        return JsonResponse({"detail": "permission_ids must be a list"}, status=400)

    # Validate all IDs exist — uncomment if you want strict checking
    found = set(Permission.objects.filter(id__in=ids).values_list("id", flat=True))
    missing = [pid for pid in ids if pid not in found]
    if missing:
        return JsonResponse({"detail": "Unknown permission ids", "missing": missing}, status=400)

    changed = {}
    with transaction.atomic():
        if action == "grant":
            for pid in ids:
                RolePermission.objects.get_or_create(role=role, permission_id=pid)
            changed = {"granted": ids}

        elif action == "revoke":
            RolePermission.objects.filter(role=role, permission_id__in=ids).delete()
            changed = {"revoked": ids}

        elif action == "set":
            current_ids = set(
                RolePermission.objects.filter(role=role).values_list("permission_id", flat=True)
            )
            new_ids = set(ids)
            to_add = list(new_ids - current_ids)
            to_remove = list(current_ids - new_ids)

            if to_remove:
                RolePermission.objects.filter(role=role, permission_id__in=to_remove).delete()
            if to_add:
                RolePermission.objects.bulk_create(
                    [RolePermission(role=role, permission_id=pid) for pid in to_add],
                    ignore_conflicts=True,
                )
            changed = {"added": to_add, "removed": to_remove}

        else:
            return JsonResponse({"detail": "action must be 'grant', 'revoke', or 'set'."}, status=400)

    # Return the updated list
    perms = (
        Permission.objects
        .filter(role_permissions__role=role)
        .values("id", "code", "description")
        .order_by("code")
    )
    return JsonResponse({"role_id": role.id, "permissions": list(perms), **changed})
