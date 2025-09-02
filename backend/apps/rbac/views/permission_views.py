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
def permissions(request, id=None):

    if id is not None:
        permission = Permission.objects.filter(pk=id).first()
        return JsonResponse({"permission":_permission_payload(permission)})

    perms = Permission.objects.all().order_by("app_label", "codename")
    return JsonResponse({"permissions": [_permission_payload(p) for p in perms]})


# ---------- Create permission (supports 'code' or app/codename) ----------

@require_POST
@csrf_protect
def create_permission(request):
    """
    Body:
      { "app_label": "shipments", "codename": "view", "name": "View Shipments", "description": "..." }
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


@require_POST
@csrf_protect
@transaction.atomic
def update_permission(request):
    """
    Body (PUT/PATCH):
      {
        "id": "uuid-or-int",
        "app_label": "app"?,
        "codename": "code"?,
        "name": "Nice Name"?,
        "description": "..."?
      }
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    perm_id = (data.get("id") or "").strip()
    if not perm_id:
        return HttpResponseBadRequest("'id' is required")

    try:
        perm = Permission.objects.select_for_update().get(id=perm_id)
    except Permission.DoesNotExist:
        return JsonResponse({"detail": "Permission not found"}, status=404)

    new_app_label = (data.get("app_label") or "").strip() if "app_label" in data else None
    new_codename  = (data.get("codename")  or "").strip() if "codename"  in data else None
    new_name      = (data.get("name")      or "").strip() if "name"      in data else None
    new_desc      = (data.get("description") or "").strip() if "description" in data else None

    if new_app_label == perm.app_label or new_codename == perm.codename:
        return JsonResponse({"detail": f"Permission '{new_app_label}.{new_codename}' already exists"}, status=409)

    updates = {}
    if new_app_label is not None:
        updates["app_label"] = new_app_label
    if new_codename is not None:
        updates["codename"] = new_codename
    if new_desc is not None and new_desc != perm.description:
        updates["description"] = new_desc
    if new_name is not None:
        updates["name"] = new_name

    if not updates:
        return JsonResponse({"updated": False, "permission": _permission_payload(perm)})

    # Apply & save
    for k, v in updates.items():
        setattr(perm, k, v)

    try:
        perm.save(update_fields=list(updates.keys()))
    except:
        return JsonResponse({"detail": "Conflict updating permission (race condition)."}, status=409)

    return JsonResponse({"updated": True, "permission": _permission_payload(perm)})


@require_POST
@csrf_protect
@transaction.atomic
def delete_permission(request):
    """
    Body (DELETE):
      { "id": "uuid" }   # required
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    perm_id = str(data.get("id") or "").strip()
    if not perm_id:
        return HttpResponseBadRequest("'id' is required")

    try:
        perm = Permission.objects.get(id=perm_id)
    except Permission.DoesNotExist:
        return JsonResponse({"detail": "Permission not found"}, status=404)

    try:
        perm.delete()
    except:
        return JsonResponse(
            {"detail": "Permission is in use and cannot be deleted"},
            status=409
        )

    return JsonResponse({"deleted": True, "id": perm_id})


# ---------- Group permission management ----------

@require_http_methods(["GET", "POST"])
@csrf_protect
def group_permissions(request, group_id):
    """
    GET  /groups/<group_id>/permissions/     -> list permissions for the group
    POST /groups/<group_id>/permissions/     -> change permissions
      body:
        {
          "permission_ids": ["uuid1", "uuid2", ...]
        }
    """
    group = get_object_or_404(Group, pk=group_id)

    # GET
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

    ids = data.get("permission_ids") or []
    if not ids:
        return JsonResponse({"detail": "permission_ids cannot be empty"}, status=400)

    # validate permissions exist
    found = set(
        str(pid) for pid in Permission.objects
                    .filter(id__in=ids)
                    .values_list("id", flat=True)
    )
    missing = [pid for pid in ids if pid not in found]
    if missing:
        return JsonResponse({"detail": "Unknown permission ids", "missing": missing}, status=400)

    # validate the group doesn't have the permissions
    existing = set(
        str(pid) for pid in GroupPermission.objects
                    .filter(group=group, permission_id__in=found)
                    .values_list("permission_id", flat=True)
    )
    to_add = [pid for pid in found if pid not in existing]
    if to_add:
        GroupPermission.objects.bulk_create(
            [GroupPermission(group=group, permission_id=pid) for pid in to_add],
        )

    # return updated list
    perms = (
        Permission.objects
        .filter(group_permissions__group=group)
        .order_by("app_label", "codename")
    )
    out = [_permission_payload(p) for p in perms]
    return JsonResponse({"group_id": str(group.id), "permissions": out})
