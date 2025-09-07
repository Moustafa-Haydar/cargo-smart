from typing import Iterable, Dict, Any, Tuple
from django.db import transaction
from django.apps import apps

PERMISSIONS = [
    # Accounts / users (admin-only)
    ("accounts.read", "Read users"),
    ("accounts.create", "Create users"),
    ("accounts.update", "Update users"),
    ("accounts.delete", "Delete users"),

    # Groups (admin-only)
    ("groups.read", "Read groups"),
    ("groups.create", "Create groups"),
    ("groups.update", "Update groups"),
    ("groups.delete", "Delete groups"),
    ("groups.group_permissions", "Manage group permissions"),

    # Permissions (admin-only)
    ("permissions.read", "Read permissions"),
    ("permissions.create", "Create permissions"),
    ("permissions.update", "Update permissions"),
    ("permissions.delete", "Delete permissions"),

    # Shipments
    ("shipments.read", "Read shipments"),
    ("shipments.create", "Create shipments"),
    ("shipments.update", "Update shipments"),
    ("shipments.delete", "Delete shipments"),

    # Vehicles
    ("vehicles.read", "Read vehicles"),
    ("vehicles.create", "Create vehicles"),
    ("vehicles.update", "Update vehicles"),
    ("vehicles.delete", "Delete vehicles"),

    # Containers
    ("containers.read", "Read containers"),
    ("containers.create", "Create containers"),
    ("containers.update", "Update containers"),
    ("containers.delete", "Delete containers"),

    # Alerts
    ("alerts.read", "Read alerts"),
    ("alerts.resolve", "Resolve alerts"),

    # Notifications
    ("notifications.read", "Read notifications"),
    ("notifications.create", "Create notifications"),
]

GROUPS: Dict[str, Dict[str, Any]] = {
    "Admin": {
        "description": "Full access to all features.",
        "permission_codes": "__all__",   # special: give all permissions
    },
    "Ops Manager": {
        "description": "Operate shipments & vehicles; resolve alerts.",
        "permission_codes": [
            "core.read_dashboard",
            "shipments.read", "shipments.create", "shipments.update",
            "vehicles.read", "vehicles.update",
            "containers.read",
            "alerts.read", "alerts.resolve",
        ],
    },
    "Driver": {
        "description": "Track shipments & Get Notifications.",
        "permission_codes": [
            "shipments.read", "shipments.update",
            "notifications.read"
        ],
    },
    # add more groups later (reader, Analyst, ...)
}

def _split(code: str):
    return code.split(".", 1) if "." in code else ("core", code)

@transaction.atomic
def seed_rbac(stdout=None):
    Group = apps.get_model("rbac", "Group")
    Permission = apps.get_model("rbac", "Permission")
    Link = apps.get_model("rbac", "GroupPermission")

    # 1) ensure permissions
    code_to_id = {}
    for code, desc in PERMISSIONS:
        app, name = _split(code)
        perm, _ = Permission.objects.get_or_create(
            app_label=app,
            codename=name,
            defaults={"name": name.replace("_", " ").title(), "description": desc},
        )
        code_to_id[code] = perm.id

    all_codes = [c for c, _ in PERMISSIONS]  # preserve declared order

    # 2) ensure groups + links (append-only)
    for gname, spec in GROUPS.items():
        group, _ = Group.objects.get_or_create(
            name=gname, defaults={"description": spec.get("description", "")}
        )
        codes = all_codes if spec.get("permission_codes") == "__all__" else spec.get("permission_codes", [])
        want_ids = {code_to_id[c] for c in codes if c in code_to_id}
        existing = set(Link.objects.filter(group=group).values_list("permission_id", flat=True))
        to_add = want_ids - existing
        if to_add:
            Link.objects.bulk_create([Link(group=group, permission_id=pid) for pid in to_add], ignore_conflicts=True)
        if stdout:
            stdout.write(f"{gname}: +{len(to_add)}")

    if stdout:
        stdout.write("RBAC seed complete.")