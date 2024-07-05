
from django.http import JsonResponse
import socket
import requests
import geocoder
from hng_stage1.settings import WEATHER_API_KEY

def index(request):
    # Get the visitor's hostname and IP address
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    # Request information about the IP address from ipinfo.io
    ip_ad = geocoder.ip(ip)

    client_ip = geocoder.ip("me")
    city = client_ip.city

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
        'client_ip': ip,
        'location': city,
        'greeting': f"Hello, {request.GET.get('visitor_name', 'Anonymous')}!, the temperature is {temperature} degrees Celsius in {city}"
    }
    print(response_data)
    return JsonResponse(response_data)

