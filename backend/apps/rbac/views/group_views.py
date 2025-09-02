# apps/rbac/views.py
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.db import transaction

from ..models import Group, Permission, GroupPermission


# ---------- helpers ----------

def _permission_payload(p: Permission):
    return {
        "id": str(p.id),
        "app_label": p.app_label,
        "codename": p.codename,
        "name": p.name,
        "description": p.description,
    }

def _group_payload(g: Group, include_permissions: bool = True):
    data = {
        "id": str(g.id),
        "name": g.name,
        "description": g.description,
    }
    if include_permissions:
        perms = (
            Permission.objects
            .filter(group_permissions__group=g)
            .distinct()
        )
        data["permissions"] = [_permission_payload(p) for p in perms]
        data["permission_ids"] = [str(p.id) for p in perms]
    return data


# ---------- get all groups ----------


@require_GET
@csrf_protect
def groups(request, id=None):
    
    if id is not None:
        group = Group.objects.filter(pk=id).first()
        return JsonResponse({"group" : _group_payload(group)})

    gs = Group.objects.all().order_by("name")
    return JsonResponse({"groups": [_group_payload(g) for g in gs]})


# ---------- create / update / delete group ----------

@require_POST
@csrf_protect
@transaction.atomic
def create_group(request):
    """
    Body:
      {
        "name": str,                       # required
        "description": str?,               # optional
        "permission_ids": [uuid, ...]?     # optional: assign on create
      }
    """   
    
    try:
        data = json.loads(request.body.decode() or "{}")
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    name = (data.get("name") or "").strip()
    description = (data.get("description") or "").strip()
    permission_ids = data.get("permission_ids") or []

    if not name:
        return HttpResponseBadRequest("Group name is required")

    if Group.objects.filter(name=name).exists():
        return JsonResponse({"detail": "Group with this name already exists"}, status=409)

    group = Group.objects.create(name=name, description=description)

    if permission_ids:
        perms = list(Permission.objects.filter(id__in=permission_ids))
        GroupPermission.objects.bulk_create(
            [GroupPermission(group=group, permission=p) for p in perms],
            ignore_conflicts=True,
        )

    return JsonResponse({"created": True, "group": _group_payload(group)}, status=201)


@require_POST
@csrf_protect
@transaction.atomic
def update_group(request):
    """
    Body:
      {
        "group_id": uuid,                  # required
        "name": str?, "description": str?,
        "permission_ids": [uuid, ...]?     # when present -> full replace
      }
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    group_id = data.get("group_id")
    if not group_id:
        return HttpResponseBadRequest("group_id is required")

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return JsonResponse({"detail": "Group not found"}, status=404)

    if "name" in data:
        name = (data.get("name") or "").strip()
        if not name:
            return HttpResponseBadRequest("name cannot be empty")
        if Group.objects.filter(name=name).exclude(id=group_id).exists():
            return JsonResponse({"detail": "Group with this name already exists"}, status=409)
        group.name = name

    if "description" in data:
        group.description = (data.get("description") or "").strip()

    group.save()

    if "permission_ids" in data:
        new_ids = set(data.get("permission_ids") or [])
        # delete removed
        GroupPermission.objects.filter(group=group).exclude(permission_id__in=new_ids).delete()
        # add new
        existing = set(GroupPermission.objects.filter(group=group).values_list("permission_id", flat=True))
        to_add = [pid for pid in new_ids if pid not in existing]
        if to_add:
            perms = Permission.objects.filter(id__in=to_add)
            GroupPermission.objects.bulk_create(
                [GroupPermission(group=group, permission=p) for p in perms],
                ignore_conflicts=True,
            )

    return JsonResponse({"updated": True, "group": _group_payload(group)})


@require_POST
@csrf_protect
@transaction.atomic
def delete_group(request):
    """
    Body: { "group_id": uuid }
    """
    try:
        data = json.loads(request.body.decode() or "{}")
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    group_id = data.get("group_id")
    if not group_id:
        return HttpResponseBadRequest("group_id is required")

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return JsonResponse({"detail": "Group not found"}, status=404)

    group.delete()
    return JsonResponse({"deleted": True})
