from .models import CustomUser
from django.contrib import admin

class RSSChannelUser(admin.ModelAdmin):
    list_display = ('id', 'username')
# Register your models here.
admin.site.register(CustomUser, RSSChannelUser)
