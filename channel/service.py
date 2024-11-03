from django.shortcuts import get_object_or_404
from .models import RSSChannel, Subscription, ItemStatus, RSSItem
from .serializers import RSSChannelSerializer, RSSItemSerializer
from user.models import User

def get_channels():
    channels = RSSChannel.objects.all()
    serializer = RSSChannelSerializer(channels, many=True)
    return serializer.data


def subscribe_to_channel(user_id, channel_id):
    user = get_object_or_404(User, id=user_id)
    channel = get_object_or_404(RSSChannel, id=channel_id)

    if Subscription.objects.filter(user=user, channel=channel).exists():
        return False, "The user is already subscribed to this channel.", {}

    Subscription.objects.create(user=user, channel=channel)

    return True, "Successfully subscribed to the channel.", channel.title


def unsubscribe_from_channel(user_id, channel_id):
    user = get_object_or_404(User, id=user_id)
    channel = get_object_or_404(RSSChannel, id=channel_id)
    try:
        subscription = Subscription.objects.get(user=user, channel=channel)
    except Subscription.DoesNotExist:
        return False, "The user is not subscribed to this channel."

    subscription.delete()
    return True, "Successfully unsubscribed from the channel."


def user_subscriptions(user_id, with_items):
    subscriptions = Subscription.objects.filter(user_id=user_id, active=True).select_related('channel')
    channels = [subscription.channel for subscription in subscriptions]

    serialized_data = RSSChannelSerializer(channels, many=True, context={'with_items': with_items}).data

    return serialized_data