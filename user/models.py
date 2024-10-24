import uuid
from django.db import models


class User(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True, db_index=True)

    def __str__(self):
        return self.username
