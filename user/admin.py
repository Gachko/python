from .models import CustomUser, Role
from django.contrib import admin

class RSSChannelUser(admin.ModelAdmin):
    list_display = ('id', 'username')
# Register your models here.
admin.site.register(CustomUser, RSSChannelUser)
admin.site.register(Role)
