from django.urls import path
from .views import (get_all_channels,
                    subscribe_to_channel,
                    unsubscribe_from_channel,
                    get_user_subscriptions,
                    toggle_subscription)

urlpatterns = [
    path("api/channels/", get_all_channels, name='get_all_channels'),
    path("api/subscribe/", subscribe_to_channel, name='subscribe_to_channel'),
    path("api/unsubscribe/", unsubscribe_from_channel, name='unsubscribe_from_channel'),
    path("api/subscriptions/<int:user_id>/", get_user_subscriptions, name='get_user_subscriptions'),
    path("api/toggle-subscription/", toggle_subscription, name='toggle_subscription'),
]
