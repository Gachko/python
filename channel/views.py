from django.http import JsonResponse, QueryDict
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RSSItem, RSSChannel, Subscription, ItemStatus
from django.views.decorators.csrf import csrf_exempt
from user.models import User
from .service import (
    get_channels,
    subscribe_to_channel,
    unsubscribe_from_channel,
    user_subscriptions
)

class ChannelListView(APIView):
    def get(self, request):
        channels = get_channels()
        return Response(channels)

class SubscribeToChannelView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        channel_id = request.data.get('channel_id')
        success, message, result = subscribe_to_channel(user_id, channel_id)

        if success:
            return Response({"message": message, "channel": result}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


class UnsubscribeFromChannelView(APIView):
    def delete(self, request):
        user_id = request.GET.get('user_id')
        channel_id = request.GET.get('channel_id')
        success, message = unsubscribe_from_channel(user_id, channel_id)

        if success:
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

class UserSubscriptionsView(APIView):
    def get(self, request, user_id):
        with_items = request.GET.get('items', 'false').lower() == 'true'
        try:
            result = user_subscriptions(user_id, with_items)
            return Response(result)

        except User.DoesNotExist:
            return Response({"error": "No such user exists."}, status=status.HTTP_404_NOT_FOUND)

# вопрос
class UpdateItemStatusView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        item_id = request.data.get('item_id')
        status_value = request.data.get('status')

        try:
            item = RSSItem.objects.get(id=item_id)
            user = User.objects.get(id=user_id)


            if not Subscription.objects.filter(user=user, channel=item.channel, active=True).exists():
                return Response({"error": "User is not subscribed to the channel of this item."}, status=status.HTTP_403_FORBIDDEN)


            item_status, created = ItemStatus.objects.update_or_create(
                user=user,
                item=item,
                defaults={'status': status_value}
            )

            return Response({"message": "Status updated successfully.", "item": item.title, "status": item_status.status}, status=status.HTTP_200_OK)

        except RSSItem.DoesNotExist:
            return Response({"error": "Item does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
