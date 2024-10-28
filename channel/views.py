from django.http import JsonResponse, QueryDict
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RSSChannelSerializer, RSSItemSerializer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import RSSChannel, Subscription
from user.models import User

class ChannelListView(APIView):
    def get(self, request):
        channels = RSSChannel.objects.all()
        serializer = RSSChannelSerializer(channels, many=True)
        return Response(serializer.data)

class SubscribeToChannelView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        channel_id = request.data.get('channel_id')

        user = get_object_or_404(User, id=user_id)
        channel = get_object_or_404(RSSChannel, id=channel_id)

        if Subscription.objects.filter(user=user, channel=channel).exists():
            return Response({"error": "The user is already subscribed to this channel."}, status=status.HTTP_400_BAD_REQUEST)

        Subscription.objects.create(user=user, channel=channel)
        return Response({"message": "Successfully subscribed to the channel.", "channel": channel.title}, status=status.HTTP_201_CREATED)

class UnsubscribeFromChannelView(APIView):
    def delete(self, request):
        user_id = request.GET.get('user_id')
        channel_id = request.GET.get('channel_id')

        user = get_object_or_404(User, id=user_id)
        channel = get_object_or_404(RSSChannel, id=channel_id)

        try:
            subscription = Subscription.objects.get(user=user, channel=channel)
        except Subscription.DoesNotExist:
            return Response({"error": "The user is not subscribed to this channel."}, status=status.HTTP_400_BAD_REQUEST)

        subscription.delete()
        return Response({"message": "Successfully unsubscribed from the channel."}, status=status.HTTP_200_OK)

class UserSubscriptionsView(APIView):
    def get(self, request, user_id):
        with_items = request.GET.get('items', 'false').lower() == 'true'
        try:
            subscriptions = Subscription.objects.filter(user_id=user_id, active=True).select_related('channel')
            channels = [subscription.channel for subscription in subscriptions]

            serialized_data = RSSChannelSerializer(channels, many=True, context={'with_items': with_items}).data
            return Response(serialized_data)

        except User.DoesNotExist:
            return Response({"error": "No such user exists."}, status=status.HTTP_404_NOT_FOUND)