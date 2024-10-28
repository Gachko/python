from rest_framework import serializers
from .models import RSSChannel, RSSItem, Subscription

class RSSItemSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(source='created_at')
    updated = serializers.DateTimeField(source='updated_at')
    class Meta:
        model = RSSItem
        fields = ['id', 'title', 'link', 'creator', 'description', 'publish_date', 'content', 'channel', 'created', 'updated']

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
                representation.pop('items', None)
            return representation

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'channel']