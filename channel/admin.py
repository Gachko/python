from .models import RSSChannel, RSSItem, Subscription
from django.contrib import admin

# Register your models here.

admin.site.register(RSSChannel)
admin.site.register(RSSItem)
admin.site.register(Subscription)
