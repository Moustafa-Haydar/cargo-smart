import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.db import transaction

from ..models import Group, Permission, GroupPermission


# ---------- helpers ----------

def _split_code(code: str):
    """Split 'app.codename' -> (app, codename); default app 'core' if no dot."""
    return code.split(".", 1) if "." in code else ("core", code)

def _permission_payload(p: Permission):
    return {
        "id": str(p.id),
        "app_label": p.app_label,
        "codename": p.codename,
        "code": f"{p.app_label}.{p.codename}",   # convenience for frontend
        "name": p.name,
        "description": p.description,
    }


# ---------- GET all permissions ----------

@require_GET
def permissions(request):
    """
    Lists all permissions.
    """
    perms = Permission.objects.all().order_by("app_label", "codename")
    return JsonResponse({"permissions": [_permission_payload(p) for p in perms]})


# ---------- Create permission (supports 'code' or app/codename) ----------

@require_POST
@csrf_protect
def add_permission(request):
    """
    Body (either):
      { "code": "shipments.view", "description": "..." , "name": "View Shipments"? }
    or:
      { "app_label": "shipments", "codename": "view", "description": "...", "name": "View Shipments"? }
    Creates the permission if missing, updates description/name if it exists.
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    code = (data.get("code") or "").strip()
    app_label = (data.get("app_label") or "").strip()
    codename = (data.get("codename") or "").strip()
    description = (data.get("description") or "").strip()
    name = (data.get("name") or "").strip()

    if code and not (app_label and codename):
        app_label, codename = _split_code(code)

    if not app_label or not codename:
        return HttpResponseBadRequest("Provide either 'code' or both 'app_label' and 'codename'.")
    if not description:
        return HttpResponseBadRequest("Permission description is required")

    # default a reasonable display name if not given
    if not name:
        name = codename.replace("_", " ").title()

    perm, created = Permission.objects.get_or_create(
        app_label=app_label,
        codename=codename,
        defaults={"name": name, "description": description},
    )

    updates = {}
    if perm.description != description:
        updates["description"] = description
    # only update name if client provided it explicitly (keeps existing nice names)
    if data.get("name") and perm.name != name:
        updates["name"] = name
    if updates:
        for k, v in updates.items():
            setattr(perm, k, v)
        perm.save(update_fields=list(updates.keys()))

    return JsonResponse(
        {"created": created, "permission": _permission_payload(perm)},
        status=201 if created else 200,
    )


# ---------- Group permission management ----------

@require_http_methods(["GET", "POST"])
@csrf_protect
def group_permissions(request, group_id):
    """
    GET  /groups/<group_id>/permissions/     -> list permissions for the group
    POST /groups/<group_id>/permissions/     -> change permissions
      body:
        {
          "action": "grant" | "revoke" | "set",   # default: "set"
          "permission_ids": ["uuid1", "uuid2", ...]
        }
    """
    group = get_object_or_404(Group, pk=group_id)

    if request.method == "GET":
        perms = (
            Permission.objects
            .filter(group_permissions__group=group)
            .order_by("app_label", "codename")
        )
        out = [_permission_payload(p) for p in perms]
        return JsonResponse({"group_id": str(group.id), "permissions": out})

    # POST
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    action = (data.get("action") or "set").lower()
    if action not in {"grant", "revoke", "set"}:
        return JsonResponse({"detail": "action must be 'grant', 'revoke', or 'set'."}, status=400)

    ids = data.get("permission_ids") or []
    if not isinstance(ids, list):
        return JsonResponse({"detail": "permission_ids must be a list"}, status=400)

    # validate IDs exist
    found = set(Permission.objects.filter(id__in=ids).values_list("id", flat=True))
    missing = [pid for pid in ids if pid not in found]
    if missing:
        return JsonResponse({"detail": "Unknown permission ids", "missing": missing}, status=400)

    changed = {}
    with transaction.atomic():
        if action == "grant":
            GroupPermission.objects.bulk_create(
                [GroupPermission(group=group, permission_id=pid) for pid in ids],
                ignore_conflicts=True,
            )
            changed = {"granted": ids}

        elif action == "revoke":
            GroupPermission.objects.filter(group=group, permission_id__in=ids).delete()
            changed = {"revoked": ids}

        else:  # set (exact replace)
            current_ids = set(
                GroupPermission.objects.filter(group=group).values_list("permission_id", flat=True)
            )
            new_ids = set(ids)
            to_add = list(new_ids - current_ids)
            to_remove = list(current_ids - new_ids)

            if to_remove:
                GroupPermission.objects.filter(group=group, permission_id__in=to_remove).delete()
            if to_add:
                GroupPermission.objects.bulk_create(
                    [GroupPermission(group=group, permission_id=pid) for pid in to_add],
                    ignore_conflicts=True,
                )
            changed = {"added": to_add, "removed": to_remove}

    # return updated list
    perms = (
        Permission.objects
        .filter(group_permissions__group=group)
        .order_by("app_label", "codename")
    )
    out = [_permission_payload(p) for p in perms]
    return JsonResponse({"group_id": str(group.id), "permissions": out, **changed})
