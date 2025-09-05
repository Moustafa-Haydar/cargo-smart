import uuid
from django.db import models

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3)
    locode = models.CharField(max_length=10, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    timezone = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name} ({self.country_code})"


class Facility(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=3)
    locode = models.CharField(max_length=10, blank=True)
    bic_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    smdg_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    location = models.ForeignKey("geo.Location", on_delete=models.PROTECT, related_name="facilities")

    def __str__(self):
        return self.name
