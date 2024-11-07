from rest_framework import serializers
from .models import RSSChannel, RSSItem, Subscription

class RSSItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    link = serializers.URLField(max_length=255)
    creator = serializers.CharField(max_length=255, allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    publish_date = serializers.DateTimeField(allow_null=True)
    content = serializers.CharField(allow_blank=True)
    channel = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(source='created_at', read_only=True)
    updated = serializers.DateTimeField(source='updated_at', read_only=True)

class RSSChannelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    link = serializers.URLField(max_length=255)
    description = serializers.CharField(allow_blank=True)
    language = serializers.CharField(max_length=50)
    created = serializers.DateTimeField(source='created_at', read_only=True)
    updated = serializers.DateTimeField(source='updated_at', read_only=True)
    items = RSSItemSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return RSSChannel.objects.create(**validated_data)


class SubscriptionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    channel = serializers.PrimaryKeyRelatedField(read_only=True)