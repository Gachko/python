from django.contrib import admin
from .models import RSSChannel, RSSItem
# Register your models here.

admin.site.register(RSSChannel)
admin.site.register(RSSItem)