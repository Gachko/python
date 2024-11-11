import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import RSSChannel, Subscription, CustomUser


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def valid_channel_data():
    return {
        'title': 'Test Channel',
        'link': 'https://example.com',
        'description': 'This is a test channel.',
        'language': 'en',
    }

@pytest.fixture
def create_rss_channel(valid_channel_data):
    return RSSChannel.objects.create(**valid_channel_data)

@pytest.mark.django_db
def test_create_rss_channel(api_client, valid_channel_data):
    url = '/api/channels/'
    response = api_client.post(url, valid_channel_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data
    assert response.data['title'] == valid_channel_data['title']
    assert response.data['link'] == valid_channel_data['link']
    assert response.data['description'] == valid_channel_data['description']
    assert response.data['language'] == valid_channel_data['language']


@pytest.mark.django_db
def test_create_rss_channel_invalid_data(api_client):
    url = '/api/channels/'
    invalid_data = {
        'title': '',
        'link': 'invalid-url',
        'language': 'en',
    }

    response = api_client.post(url, invalid_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'title' in response.data
    assert 'link' in response.data


# -------------------------------TESTS FOR SubscriptionViewSet--------------------------------------------

@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(username='testuser', password='password')

@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def rss_channel():
    return RSSChannel.objects.create(
        title='Sample Channel',
        link='https://sample.com',
        description='A sample RSS channel',
        language='en',
    )

@pytest.mark.django_db
def test_create_subscription(api_client, user, rss_channel):
    url = reverse('subscriptions-list')
    data = {'channel_id': rss_channel.id}
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'Successfully subscribed to the channel.'

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'The user is already subscribed to this channel.'

@pytest.mark.django_db
def test_unsubscribe_from_channel(api_client, user, rss_channel):
    Subscription.objects.create(user=user, channel=rss_channel)

    url = reverse('subscriptions-detail', args=[rss_channel.id])
    response = api_client.delete(url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Successfully unsubscribed from the channel.'

    response = api_client.delete(url, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'The user is not subscribed to this channel.'

@pytest.mark.django_db
def test_list_subscriptions(api_client, user, rss_channel):
    Subscription.objects.create(user=user, channel=rss_channel)

    url = reverse('subscriptions-list')
    response = api_client.get(url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['title'] == rss_channel.title
    assert response.data[0]['link'] == rss_channel.link