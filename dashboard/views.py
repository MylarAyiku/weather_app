from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .services import get_weather_data, get_news_data
from rest_framework.response import Response





class WeatherView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1. Check if user sent a specific city in the URL (e.g., ?city=London)
        city = request.query_params.get('city')

        # 2. If not, use the user's default city from the database
        if not city:
            city = user.city

        # 3. If we still don't have a city, complain.
        if not city:
            return Response({'error': 'No city provided. Please set a profile city or pass ?city=Name parameter.'},
                            status=400)

        # 4. Call our Service Layer
        weather_data = get_weather_data(city)

        if weather_data :
            print(weather_data)
            return Response(weather_data)
        else:
            return Response({'error':'Could not fetch weather for that city'},status=404)


class NewsView(APIView):
    """handle News request """
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Allow user to pick a category (e.g., ?category=sports)
        # Default to 'technology' if they don't choose.
        category = request.query_params.get('category', 'technology')

        news_data = get_news_data(category)

        if news_data:
            return Response(news_data)

        else:
            return Response({'error': 'Could not fetch news'}, status=503)










