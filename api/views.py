from django.http import JsonResponse
import requests
from hng_stage1.settings import WEATHER_API_KEY
from ipware import get_client_ip


def index(request):
    # Get the visitor's IP address

    client_ip = request.META.get('HTTP_X_REAL_IP')
    if client_ip:
        client_ip = client_ip.split(',')[0]
    else:
        client_ip = request.META.get('REMOTE_ADDR')

    def get_location():
        ip_address = client_ip
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        location_data = {
            "ip": ip_address,
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country_name")
        }
        return location_data

    location = get_location()
    city = location['city']

    # Fetch temperature from a weather API (example)
    weather_api_key = WEATHER_API_KEY
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={weather_api_key}'
    weather_response = requests.get(weather_url)

    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        temperature = weather_data.get('main', {}).get('temp', 'Unknown')
    else:
        temperature = 'Unknown'

    # Construct JSON response
    response_data = {
        'client_ip': client_ip,
        'location': city,
        'greeting': f"Hello, {request.GET.get('visitor_name', 'Anonymous')}!, the temperature is {temperature} degrees Celsius in {city}"
    }
    print(response_data)
    return JsonResponse(response_data)

