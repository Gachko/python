from django.urls import path
from .views import (
    GetAllChannelsView,
    PostSubscribeToChannelView,
    DeleteSubscriptionToChannelView,
    GetUserSubscriptionsView,
    PostItemStatusView,
    GetChannelView,
    GetItemsView,
    GetItemView
)

urlpatterns = [
    path('channels/', GetAllChannelsView.as_view(), name='get-all-channels'),
    path('channels/<int:channel_id>/', GetChannelView.as_view(), name='get-channel'),
    path('channels/<int:channel_id>/items/', GetItemsView.as_view(), name='get-items'),
    path('channels/<int:channel_id>/items/<int:item_id>/', GetItemView.as_view(), name='get-item'),
    path('channels/subscribe/', PostSubscribeToChannelView.as_view(), name='post-subscribe-to-channel'),
    path('channels/subscribe/', DeleteSubscriptionToChannelView.as_view(), name='delete-subscription-to-channel'),
    path('channels/subscriptions/', GetUserSubscriptionsView.as_view(), name='get-user-subscriptions'),
    path('channel/<int:channel_id>/item/<int:item_id>/', PostItemStatusView.as_view(), name='post-item-status'),
]