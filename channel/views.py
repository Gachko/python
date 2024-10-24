from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import RSSChannel, Subscription
from user.models import User

def get_all_channels(request):
    channels = RSSChannel.objects.all().values()
    return JsonResponse(list(channels), safe=False)

@csrf_exempt
def subscribe_to_channel(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        channel_id = request.POST.get('channel_id')
        print(user_id, channel_id, 'hereee')
        user = get_object_or_404(User, id=user_id)
        channel = get_object_or_404(RSSChannel, id=channel_id)


        if Subscription.objects.filter(user=user, channel=channel).exists():
            return JsonResponse({"error": "The user is already subscribed to this channel."}, status=400)


        Subscription.objects.create(user=user, channel=channel)
        return JsonResponse({"message": "Successfully subscribed to the channel."}, status=201)

    return JsonResponse({"error": "Method Not Allowed"}, status=405)

@csrf_exempt
def unsubscribe_from_channel(request):
    if request.method == 'DELETE':
        user_id = request.GET.get('user_id')
        channel_id = request.GET.get('channel_id')
        user = get_object_or_404(User, id=user_id)
        channel = get_object_or_404(RSSChannel, id=channel_id)

        try:
            subscription = Subscription.objects.get(user=user, channel=channel)
            subscription.delete()
            return JsonResponse({"message": "Successfully unsubscribed from the channel."}, status=200)
        except Subscription.DoesNotExist:
            return JsonResponse({"error": "The user is not subscribed to this channel."}, status=400)

    return JsonResponse({"error": "Method Not Allowed"}, status=405)

def get_user_subscriptions(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        subscriptions = Subscription.objects.filter(user=user, active=True).select_related('channel')
        subscription_data = [{"channel": subscription.channel.title, "channel_id": subscription.channel.id} for subscription in subscriptions]

        return JsonResponse(subscription_data, safe=False)
    except User.DoesNotExist:
        return JsonResponse({"error": "No such user exists."}, status=404)

# Page not found
@csrf_exempt
def toggle_subscription(request):
    if request.method == 'PATCH':
        body = request.body.decode('utf-8')
        patch_data = QueryDict(body)
        user_id = patch_data.get('user_id')
        channel_id = patch_data.get('channel_id')
        activate = patch_data.get('activate') == 'true'
        print(patch_data, 'patch_data')
        user = get_object_or_404(User, id=user_id)
        channel = get_object_or_404(RSSChannel, id=channel_id)

        try:
            subscription = Subscription.objects.get(user=user, channel=channel)
            subscription.active = activate
            subscription.save()
            status_message = "Activated" if activate else "Deactivated"
            return JsonResponse({"message": f"Subscription {status_message}."}, status=200)
        except Subscription.DoesNotExist:
            return JsonResponse({"error": "The user is not subscribed to this channel."}, status=400)

    return JsonResponse({"error": "Method Not Allowed."}, status=405)