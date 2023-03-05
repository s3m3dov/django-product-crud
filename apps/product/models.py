import uuid as uuid_lib

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    uuid = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    logo = models.URLField(blank=True, null=True)
    rotate_duration = models.FloatField(null=True)
    modified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
