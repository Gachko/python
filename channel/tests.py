import pytest
from rest_framework import status
from rest_framework.test import APIClient
from .models import RSSChannel


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