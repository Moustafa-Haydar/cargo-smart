import uuid
from django.db import models
from apps.rbac.models import Permission

class Dashboard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    # JSON/YAML string; keep TextField so you can drop whatever you like
    layout_config = models.TextField()
    required_permission = models.ForeignKey(
        Permission,
        on_delete=models.PROTECT,
        related_name="dashboards",
    )

    def __str__(self):
        return self.title
