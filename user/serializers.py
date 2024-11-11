from .models import CustomUser, Role
from rest_framework import serializers

class RoleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(allow_blank=True)

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    roles = serializers.SerializerMethodField()
    def get_roles(self, obj):
        return [role.name for role in obj.roles.all()]