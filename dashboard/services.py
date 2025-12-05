from decouple import config
from django.core.cache import cache
import requests


def get_weather_data(city):

    # 1. Create a unique key for the cache (e.g., "weather_London")
    # We clean the string so 'London' and 'london' are treated the same.
    cache_key = f"weather_{city.lower()}"
    cache_status =False

    # 2. Check if data exists in cache
    cached_data = cache.get(cache_key)


    if cached_data:
        cache_status= True
        cached_data['cache_status']=cache_status
        # OPTIONAL: Print to console to prove it worked
        print(f"------------ HIT CACHE FOR {city} ------------")
        return cached_data

    # 3. If NOT in cache, do the API calls (The existing code you wrote)
    print(f"------------ CALLING API FOR {city} ------------")

    """
    Fetches weather data using Open-Meteo (No API Key required).
    1. Converts City Name -> Coordinates
    2. Fetches Weather -> Returns JSON
    """
    # Step 1: Get Coordinates for the city
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {'name': city, 'count': 1, 'language': 'en', 'format': 'json'}

    geo_response = requests.get(geo_url, params=geo_params)

    # If we can't find the city, return None
    if geo_response.status_code != 200 or not geo_response.json().get('results'):
        return None

    # Extract Lat/Lon from the first result
    location = geo_response.json()['results'][0]
    lat = location['latitude']
    lon = location['longitude']


    # Step 2: Get Weather for those coordinates
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': 'true'
    }

    weather_response = requests.get(weather_url, params=weather_params)


    if weather_response.status_code == 200:
        data = weather_response.json()
        # We clean up the data to make it easier for our Frontend
        final_data = {
            'city': location['name'],
            'temperature': data['current_weather']['temperature'],
            'windspeed': data['current_weather']['windspeed'],
            'description': 'Clear sky',
           'cache_status':cache_status

        }
        # 4. Before returning, SAVE it to cache
        # 60 * 15 means 900 seconds (15 minutes)
        cache.set(cache_key, final_data, timeout=60 * 15)


        return final_data
    else:
        return None


def get_news_data(category='technology'):

    print(category)
    ### create a unique key for the news categories
    cache_key = f'news_{category.lower()}'

    cache_status = False

    #### check if the data exist in the cache
    cache_data = cache.get(cache_key)


    #### when there is a hit
    if cache_data:
        cache_status =True
        cache_data['cache_status'] = cache_status

        ####  print hit to console
        print(f'----- HIT ON CATEGORY {category} ------- ')

        return cache_data

    print(f'----- No HIT FOR CATEGORY {category} -------')


    """
    Fetches top headlines from NewsAPI.
    """
    api_key = config('NEWS_API_KEY')
    url = "https://newsapi.org/v2/top-headlines"
    header ={'X-Api-Key':api_key}

    params = {
        'category': category,
        'language': 'en',
    }

    response = requests.get(url, params=params,headers=header)

    if response.status_code == 200:
        data = response.json()
        # Let's return a simplified list of articles
        articles = data.get('articles', [])[:5]  # Just top 5

        cleaned_data = []
        for article in articles:
            cleaned_data.append({
                'title': article['title'],
                'source': article['source']['name'],
                'url': article['url'],

            })
        final_result = {
            'news': cleaned_data,
            'cache_status': False
        }

        # 4. Save to Cache
        cache.set(cache_key, final_result, timeout=60 * 60)

        return final_result
    else:
        return None