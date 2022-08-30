import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

import requests
from decouple import config

from .forms import AgencyForm, AstronautForm

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

def agency_view(request):

    url = 'https://ll.thespacedevs.com/2.2.0/agencies/?search='

    LAUNCHLIBRARY2_KEY = config("LAUNCHLIBRARY2_KEY")

    headers = {
        "Accepts":"application/json",
        "Content-Type": "application/json",
        "Authorization": f"Token {LAUNCHLIBRARY2_KEY}"
        }

    request.META['HTTP_Authorization'] = "Token " + LAUNCHLIBRARY2_KEY

    if request.method == "POST":
        form = AgencyForm(request.POST)
        if form.is_valid():
            agency = form.cleaned_data['agency_name']

            url = 'https://ll.thespacedevs.com/2.2.0/agencies/?search='+agency

            r = requests.get(url, headers=headers)
            
            if r.status_code == 200:
                jsonResponse = r.json()

                for result in jsonResponse['results']:
                    print(r)
                    print(request.headers.get('Authorization'))
                    print("Response successfully returned for " + result['name'])

                context = {
                    "form": form,
                    'jsonResponse': jsonResponse
                }

                return render(request, 'agencies.html', context)
            elif r.status_code == 429:
                print(r)
                print(request.headers.get('Authorization'))
                return HttpResponse("Too many requests to LL2 Api.")
            else:
                print(r)
                return HttpResponse("No record of the requested Space Agency.")
        else:
            print(form)
            return HttpResponse("Form is invalid.")

    else:
        form = AgencyForm()

    return render(request, 'agencies.html', { 'form': form})

def iss_location_info_view(request):

    # API request for current astronauts in space count.
    # response variable == to jsonResponse2 in template.
    url2 = 'http://api.open-notify.org/astros.json'

    response = requests.get(url2).json()

    # API request for astronaut search.
    # response variable == to jsonResponse in template.
    url = 'https://ll.thespacedevs.com/2.2.0/astronaut/?search='

    LAUNCHLIBRARY2_KEY = config("LAUNCHLIBRARY2_KEY")

    headers = {
        "Accepts":"application/json",
        "Content-Type": "application/json",
        "Authorization": f"Token {LAUNCHLIBRARY2_KEY}"
        }

    request.META['HTTP_Authorization'] = "Token " + LAUNCHLIBRARY2_KEY

    if request.method == "POST":
        form = AstronautForm(request.POST)
        if form.is_valid():
            astronaut = form.cleaned_data['astronaut_name']

            url = 'https://ll.thespacedevs.com/2.2.0/astronaut/?search='+astronaut

            r = requests.get(url, headers=headers)
            
            if r.status_code == 200:
                jsonResponse = r.json()

                for result in jsonResponse['results']:
                    print(r)
                    print(request.headers.get('Authorization'))
                    print("Response successfully returned for " + result['name'])

                context = {
                    'form': form,
                    'jsonResponse': jsonResponse,
                    'jsonResponse2': response
                }

                return render(request, 'iss-location-astronauts.html', context)
            elif r.status_code == 429:
                print(r)
                print(request.headers.get('Authorization'))
                return HttpResponse("Too many requests to LL2 Api.")
            else:
                print(r)
                return HttpResponse("No record of the requested Astronaut.")
        else:
            print(form)
            return HttpResponse("Form is invalid.")

    else:
        form = AstronautForm()

    return render(request, 'iss-location-astronauts.html', {"form": form, "jsonResponse2": response})