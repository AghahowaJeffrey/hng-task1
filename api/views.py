import socket
from django.http import JsonResponse
import requests
import geocoder
from hng_stage1.settings import WEATHER_API_KEY
from ipware import get_client_ip


def index(request):
    # Get the visitor's IP address
    client_ip = ''.join(socket.gethostbyname_ex(socket.gethostname())[2])
    # client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        client_ip = 'Unknown'

    print(f"IP Address: {client_ip}")

    geo = geocoder.ip('me')
    city = geo.city or 'Unknown'

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

