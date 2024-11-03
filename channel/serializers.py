from rest_framework import serializers
from .models import RSSChannel, RSSItem, Subscription

class RSSItemSerializer(serializers.ModelSerializer):
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


class RSSChannelSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(source='created_at')
    updated = serializers.DateTimeField(source='updated_at')
    items = RSSItemSerializer(many=True, read_only=True)
    class Meta:
        model = RSSChannel
        fields = ['id', 'title', 'link', 'description', 'language', 'created', 'updated', 'items']
    def to_representation(self, instance):
            representation = super().to_representation(instance)
            if not self.context.get('with_items', False):
                representation['items'] = []
            return representation


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'channel']