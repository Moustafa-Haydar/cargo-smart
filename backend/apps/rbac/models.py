import uuid
from django.conf import settings
from django.db import models

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app_label = models.CharField(max_length=100)
    codename = models.CharField(max_length=150)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["app_label", "codename"],
                name="uniq_permission_app_label_codename",
            )
        ]

    def __str__(self):
        return f"{self.app_label}.{self.codename}"


class UserGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_groups")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="user_groups")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "group"], name="uniq_user_group")
        ]


class GroupPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_permissions")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="group_permissions")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["group", "permission"], name="uniq_group_permission")
        ]


class Operation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Object(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class PermissionOperationObject(models.Model):
    """
    Bridges permissions to (operation, object).
    Think: permission 'shipments.view' == (READ, Shipment).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="op_objs")
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name="op_permissions")
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="obj_permissions")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["permission", "operation", "object"],
                name="uniq_permission_operation_object",
            )
        ]
