from django.db import models

# Create your models here.
import uuid
from django.db import models


class RSSChannel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, db_index=True)
    link = models.URLField(max_length=255)
    description = models.TextField()
    language = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title


class RSSItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, db_index=True)
    link = models.URLField(max_length=255)
    creator = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    channel = models.ForeignKey(RSSChannel, related_name='items', on_delete=models.CASCADE)
