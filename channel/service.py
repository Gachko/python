from django.shortcuts import get_object_or_404
from .models import RSSChannel, Subscription, ItemStatus, RSSItem

def get_channels():
    return RSSChannel.objects.all()

def create_rss_channel(data):
    return RSSChannel.objects.create(**data)

def subscribe_to_channel(user, channel):
    Subscription.objects.create(user=user, channel=channel)


def unsubscribe_from_channel(subscription):
    subscription.delete()


def user_subscriptions(user_id):
    subscriptions = Subscription.objects.filter(user_id=user_id).select_related('channel')
    channels = [subscription.channel for subscription in subscriptions]

    return channels

def update_item_status(user, item, status_value):
    item_status, created = ItemStatus.objects.update_or_create(
            user=user,
            item=item,
            defaults={'status': status_value}
    )

    return item_status, created