from .models import RSSChannel, RSSItem, Subscription, ItemStatus
from django.contrib import admin

# Register your models here.
class RSSItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

class RSSChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

admin.site.register(RSSChannel, RSSChannelAdmin)
admin.site.register(RSSItem, RSSItemAdmin)
admin.site.register(Subscription)
admin.site.register(ItemStatus)
