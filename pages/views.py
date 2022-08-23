from django.shortcuts import render

# Create your views here.

def homepage_view(request):

    return render(request, 'home.html')

def launch_event_view(request):

    return render(request, 'launches-events.html')

def iss_location_info_view(request):

    return render(request, 'iss-location-astronauts.html')

def agency_view(request):

    return render(request, 'agencies.html')