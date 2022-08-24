from django.shortcuts import render

import requests
from decouple import config

# Create your views here.

def home_get_APOD_view(request):

    NASA_KEY = config('NASA_KEY')

    url = 'https://api.nasa.gov/planetary/apod?api_key='+NASA_KEY

    response = requests.get(url).json()

    context = {
        "jsonResponse": response
    }

    return render(request, 'home.html', context)

def launch_event_view(request):

    return render(request, 'launches-events.html')

def iss_location_info_view(request):

    return render(request, 'iss-location-astronauts.html')

def agency_view(request):

    return render(request, 'agencies.html')