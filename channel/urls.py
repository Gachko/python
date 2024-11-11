from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChannelViewSet, ItemViewSet, SubscriptionViewSet, ItemStatusViewSet

router = DefaultRouter()
router.register(r'channels', ChannelViewSet, basename='channels')
router.register(r'channels/(?P<channel_id>\d+)/items', ItemViewSet, basename='channel-items')
router.register(r'subscribe', SubscriptionViewSet, basename='subscriptions')
router.register(r'channel/(?P<channel_id>\d+)/item/(?P<item_id>\d+)/status', ItemStatusViewSet, basename='item-status')

urlpatterns = [
    path('', include(router.urls)),
]