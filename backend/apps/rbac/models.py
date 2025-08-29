import uuid
from django.db import models


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code


class Operation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ObjectModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)

    class Meta:
        db_table = "objects"

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey("rbac.Role", on_delete=models.CASCADE, related_name="role_permissions")
    permission = models.ForeignKey("rbac.Permission", on_delete=models.CASCADE, related_name="role_permissions")

    class Meta:
        unique_together = (("role", "permission"),)

    def __str__(self):
        return f"{self.role} → {self.permission}"


class PermissionOpObj(models.Model):
    """
    Matrix tying Permission -> Operation on ObjectModel.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission = models.ForeignKey("rbac.Permission", on_delete=models.CASCADE, related_name="op_objects")
    operation = models.ForeignKey("rbac.Operation", on_delete=models.CASCADE, related_name="permission_objects")
    objectmodel = models.ForeignKey("rbac.ObjectModel", on_delete=models.CASCADE, related_name="permission_operations")

    class Meta:
        db_table = "permission_ops_objs"
        unique_together = (("permission", "operation", "objectmodel"),)
        indexes = [
            models.Index(fields=["permission", "operation", "objectmodel"], name="perm_op_obj_idx"),
        ]

    def __str__(self):
        return f"{self.permission.code}: {self.operation.name} on {self.objectmodel.name}"


class Dashboard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    layout_config = models.JSONField(default=dict)
    role = models.ForeignKey("rbac.Role", on_delete=models.CASCADE, related_name="dashboards")

    def __str__(self):
        return f"{self.title} ({self.role.name})"
