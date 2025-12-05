"""
Test Weather API
"""
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from dashboard.services import get_weather_data

WEATHER_URL = reverse('weather')

def create_user(**params):
    """Helper function to create a user"""
    return get_user_model().objects.create_user(**params)

class WeatherServiceTests(TestCase):
    """Test the weather service function"""

    @patch('dashboard.services.requests.get')
    def test_get_weather_data_success(self, mock_get):
        """Test retrieving weather data successfully"""
        # Mock Geocoding API response
        mock_geo_response = {
            'results': [{'latitude': 51.5074, 'longitude': -0.1278, 'name': 'London'}]
        }
        # Mock Weather API response
        mock_weather_response = {
            'current_weather': {
                'temperature': 15.0,
                'windspeed': 10.0
            }
        }

        # Configure side_effect for multiple calls
        mock_get.side_effect = [
            type('Response', (object,), {'status_code': 200, 'json': lambda: mock_geo_response}),
            type('Response', (object,), {'status_code': 200, 'json': lambda: mock_weather_response})
        ]

        result = get_weather_data('London')

        self.assertIsNotNone(result)
        self.assertEqual(result['city'], 'London')
        self.assertEqual(result['temperature'], 15.0)
        self.assertEqual(result['windspeed'], 10.0)

    @patch('dashboard.services.requests.get')
    def test_get_weather_data_city_not_found(self, mock_get):
        """Test retrieving weather data for non-existent city"""
        # Mock Geocoding API response (empty results)
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'results': []}

        result = get_weather_data('UnknownCity')
        self.assertIsNone(result)


class WeatherApiTests(TestCase):
    """Test the Weather API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='password123', name='Test User', city='London')

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(WEATHER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('dashboard.views.get_weather_data')
    def test_get_weather_success(self, mock_get_weather):
        """Test retrieving weather for authenticated user"""
        self.client.force_authenticate(self.user)
        
        mock_get_weather.return_value = {
            'city': 'London',
            'temperature': 20,
            'windspeed': 5,
            'description': 'Clear sky',
            'cache_status': False
        }

        res = self.client.get(WEATHER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['city'], 'London')
        mock_get_weather.assert_called_with('London')

    @patch('dashboard.views.get_weather_data')
    def test_get_weather_custom_city(self, mock_get_weather):
        """Test retrieving weather for a specific city param"""
        self.client.force_authenticate(self.user)
        
        mock_get_weather.return_value = {
            'city': 'Paris',
            'temperature': 22,
            'windspeed': 8,
            'description': 'Clear sky',
            'cache_status': False
        }

        res = self.client.get(WEATHER_URL, {'city': 'Paris'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['city'], 'Paris')
        mock_get_weather.assert_called_with('Paris')

