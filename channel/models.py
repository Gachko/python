from django.db import models
import uuid
from user.models import User


class RSSChannel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, db_index=True)
    link = models.URLField(max_length=255)
    description = models.TextField()
    language = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subscribed_channels = models.ManyToManyField(
        User, through='Subscription', related_name='subscribed_channels', blank=True
    )

    def __str__(self):
        return self.title


class RSSItem(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, db_index=True)
    link = models.URLField(max_length=255)
    creator = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    channel = models.ForeignKey(
        RSSChannel, related_name='items', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    channel = models.ForeignKey(RSSChannel, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'channel')

    def __str__(self):
        return f"{self.user.username} -> {self.channel.title}"
