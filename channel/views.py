from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import RSSItem, RSSChannel, Subscription, ItemStatus
from .serializers import RSSChannelSerializer, RSSItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from user.models import CustomUser
from rest_framework.permissions import AllowAny
from .service import (
    get_channels,
    subscribe_to_channel,
    unsubscribe_from_channel,
    user_subscriptions,
    update_item_status
)

class ChannelViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return RSSChannel.objects.all()

    def list(self, request):
        channels = self.get_queryset()
        serializer = RSSChannelSerializer(channels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, channel_id=None, pk=None):
        channel = get_object_or_404(self.get_queryset(), id=pk)
        serializer = RSSChannelSerializer(channel)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ItemViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request, channel_id=None):
        channel = get_object_or_404(RSSChannel, id=channel_id)
        items = channel.items.all()
        serializer = RSSItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, channel_id=None, item_id=None, pk=None):
        channel = get_object_or_404(RSSChannel, id=channel_id)
        item = get_object_or_404(RSSItem, id=pk, channel=channel)
        serializer = RSSItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubscriptionViewSet(viewsets.ViewSet):
    @csrf_exempt
    def create(self, request):
        channel_id = request.data.get('channel_id')
        user = request.user
        channel = get_object_or_404(RSSChannel, id=channel_id)

        if Subscription.objects.filter(user=user, channel=channel).exists():
            return Response({"error": "The user is already subscribed to this channel."}, status=status.HTTP_400_BAD_REQUEST)

        subscribe_to_channel(user, channel)
        return Response({"message": "Successfully subscribed to the channel."}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    def destroy(self, request, channel_id=None, pk=None):
        print('channel_id', channel_id)
        user = request.user
        channel = get_object_or_404(RSSChannel, id=pk)

        try:
            subscription = Subscription.objects.get(user=user, channel=channel)
        except Subscription.DoesNotExist:
            return Response({"error": "The user is not subscribed to this channel."}, status=status.HTTP_400_BAD_REQUEST)

        unsubscribe_from_channel(subscription)
        return Response({"message": "Successfully unsubscribed from the channel."}, status=status.HTTP_200_OK)

    def list(self, request):
        user = request.user
        with_items = request.GET.get('items', 'false').lower() == 'true'
        channels = user_subscriptions(user)
        serialized_channels = RSSChannelSerializer(channels, many=True, context={'with_items': with_items})
        return Response(serialized_channels.data)

class ItemStatusViewSet(viewsets.ViewSet):
    def create(self, request, channel_id=None, item_id=None):
        user = request.user
        status_value = request.data.get('status')
        item = get_object_or_404(RSSItem, id=item_id, channel_id=channel_id)

        if not Subscription.objects.filter(user=user, channel=item.channel).exists():
            return Response({"error": "User is not subscribed to the channel of this item."}, status=status.HTTP_403_FORBIDDEN)

        item_status, created = update_item_status(user, item, status_value)
        return Response({"message": "Status updated successfully.", "item": item.title, "status": item_status.status}, status=status.HTTP_200_OK)