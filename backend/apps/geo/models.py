import uuid
from django.db import models


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="India")
    country_code = models.CharField(max_length=3, default="IN")
    lat = models.FloatField()
    lng = models.FloatField()
    timezone = models.CharField(max_length=64, default="Asia/Kolkata")

    def __str__(self):
        return f"{self.name}, {self.state}"
