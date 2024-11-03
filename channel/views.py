from django.http import JsonResponse, QueryDict
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RSSItem, RSSChannel, Subscription, ItemStatus
from .serializers import RSSChannelSerializer, RSSItemSerializer
from django.views.decorators.csrf import csrf_exempt
from user.models import User
from .service import (
    get_channels,
    subscribe_to_channel,
    unsubscribe_from_channel,
    user_subscriptions,
    update_item_status
)

class GetAllChannelsView(APIView):
    def get(self, request):
        channels = get_channels()
        serializer = RSSChannelSerializer(channels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetChannelView(APIView):
    def get(self, request, channel_id):
        channel = get_object_or_404(RSSChannel, id=channel_id)
        serializer = RSSChannelSerializer(channel)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetItemsView(APIView):
    def get(self, request, channel_id):
        channel = get_object_or_404(RSSChannel, id=channel_id)
        items = channel.items.all()
        serializer = RSSItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetItemView(APIView):
    def get(self, request, channel_id, item_id):
        channel = get_object_or_404(RSSChannel, id=channel_id)
        item = get_object_or_404(RSSItem, id=item_id, channel=channel)
        serializer = RSSItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostSubscribeToChannelView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        channel_id = request.data.get('channel_id')

        user = get_object_or_404(User, id=user_id)
        channel = get_object_or_404(RSSChannel, id=channel_id)

        if Subscription.objects.filter(user=user, channel=channel).exists():
            return Response({"error": "The user is already subscribed to this channel."}, status=status.HTTP_400_BAD_REQUEST)

        subscribe_to_channel(user, channel)

        return Response({"message": "Successfully subscribed to the channel."}, status=status.HTTP_201_CREATED)


class DeleteSubscriptionToChannelView(APIView):
    def delete(self, request):
        user_id = request.GET.get('user_id')
        channel_id = request.GET.get('channel_id')

        user = get_object_or_404(User, id=user_id)
        channel = get_object_or_404(RSSChannel, id=channel_id)

        try:
            subscription = Subscription.objects.get(user=user, channel=channel)
        except Subscription.DoesNotExist:
            return Response({"error": "The user is not subscribed to this channel."}, status=status.HTTP_400_BAD_REQUEST)

        unsubscribe_from_channel(subscription)

        return  Response({"message": "Successfully unsubscribed from the channel."}, status=status.HTTP_200_OK)


class GetUserSubscriptionsView(APIView):
    def get(self, request, user_id):
        with_items = request.GET.get('items', 'false').lower() == 'true'

        user = get_object_or_404(User, id=user_id)

        channels = user_subscriptions(user)

        serialized_channels = RSSChannelSerializer(channels, many=True, context={'with_items': with_items})

        return Response(serialized_channels.data)


class PostItemStatusView(APIView):
    def post(self, request, channel_id, item_id):
        user_id = request.data.get('user_id')
        status_value = request.data.get('status')

        item = get_object_or_404(RSSItem, id=item_id, channel_id=channel_id)
        user = get_object_or_404(User, id=user_id)

        if not Subscription.objects.filter(user=user, channel=item.channel, active=True).exists():
            return Response({"error": "User is not subscribed to the channel of this item."}, status=status.HTTP_403_FORBIDDEN)

        item_status, created = update_item_status(user, item, status_value)

        return Response({"message": "Status updated successfully.", "item": item.title, "status": item_status.status}, status=status.HTTP_200_OK)