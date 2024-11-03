from django.urls import path
from .views import (
    ChannelListView,
    SubscribeToChannelView,
    UnsubscribeFromChannelView,
    UserSubscriptionsView,
    UpdateItemStatusView
)

urlpatterns = [
    path('api/channels/', ChannelListView.as_view(), name='channel-list'),
    path('api/subscribe/', SubscribeToChannelView.as_view(), name='subscribe-to-channel'),
    path('api/unsubscribe/', UnsubscribeFromChannelView.as_view(), name='unsubscribe-from-channel'),
    path('api/subscriptions/<int:user_id>/', UserSubscriptionsView.as_view(), name='user-subscriptions'),
    path('api/channel/updateStatus/', UpdateItemStatusView.as_view(), name='update-item-status'),
]