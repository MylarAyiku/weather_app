"""
Test News API
"""
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from dashboard.services import get_news_data

NEWS_URL = reverse('news')

def create_user(**params):
    """Helper function to create a user"""
    return get_user_model().objects.create_user(**params)

class NewsServiceTests(TestCase):
    """Test the news service function"""

    @patch('dashboard.services.requests.get')
    def test_get_news_data_success(self, mock_get):
        """Test retrieving news data successfully"""
        mock_response = {
            'articles': [
                {
                    'title': 'Test News',
                    'source': {'name': 'Test Source'},
                    'url': 'http://test.com'
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_news_data('technology')

        self.assertIsNotNone(result)
        self.assertEqual(len(result['news']), 1)
        self.assertEqual(result['news'][0]['title'], 'Test News')

    @patch('dashboard.services.requests.get')
    def test_get_news_data_failure(self, mock_get):
        """Test retrieving news data failure"""
        mock_get.return_value.status_code = 404

        result = get_news_data('technology')
        self.assertIsNone(result)


class NewsApiTests(TestCase):
    """Test the News API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='password123', name='Test User')

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(NEWS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('dashboard.views.get_news_data')
    def test_get_news_success(self, mock_get_news):
        """Test retrieving news for authenticated user"""
        self.client.force_authenticate(self.user)
        
        mock_get_news.return_value = {
            'news': [{'title': 'Test', 'source': 'Source', 'url': 'url'}],
            'cache_status': False
        }

        res = self.client.get(NEWS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['news']), 1)
        mock_get_news.assert_called_with('technology') # Default category

    @patch('dashboard.views.get_news_data')
    def test_get_news_category(self, mock_get_news):
        """Test retrieving news for specific category"""
        self.client.force_authenticate(self.user)
        
        mock_get_news.return_value = {
            'news': [],
            'cache_status': False
        }

        res = self.client.get(NEWS_URL, {'category': 'sports'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        mock_get_news.assert_called_with('sports')
