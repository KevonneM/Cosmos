from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from django.core.paginator import Paginator

import requests
import schedule
import threading
import time
from pprint import pprint
from decouple import config
from pages.models import UpcomingLaunch

from .forms import AgencyForm, AstronautForm, LaunchForm

def delete_update_create_upcoming_launches():
    # Info needed for both endpoint requests.
    LAUNCHLIBRARY2_KEY = config("LAUNCHLIBRARY2_KEY")

    headers = {
        "Authorization": f"Token {LAUNCHLIBRARY2_KEY}"
        }

    # API request for simple upcoming launches display.
    # gather all results into a list to paginate.
    results = []
    limit = 100
    offset = 0
    
    while True:
        url = f'https://ll.thespacedevs.com/2.2.0/launch/upcoming/?mode=detailed&limit={limit}&offset={offset}'
        print("requesting ", url)
        launchResponse = requests.get(url, headers=headers)
        launchData = launchResponse.json()

        results.extend(launchData['results'])

        # Breaks out of loop if all results are acquired.
        if len(results) == launchData['count']:
            break
        else:
            offset = offset + 100

        resultCount = launchData['count']

    # Incoming data will be used to update the existing database.
    existingNames = []
    resultNames = []
    existingData = UpcomingLaunch.objects.all()

    for existingObject in existingData:
        existingNames.append(existingObject.name)

    for resultObject in results:
        resultNames.append(resultObject['name'])

    if existingData.exists():
        # A check to delete launches that are no longer upcoming.
        for existingLaunch in existingNames:
            if existingLaunch not in resultNames:
                #Delete
                print("Removing : " + existingLaunch)
                UpcomingLaunch.objects.get(name=existingLaunch).delete()
                
        # A check to update existing db if launch is still upcoming.
        # A check to populate existing db with new upcoming launches
        for existingLaunch in existingNames:
            for result in results:

                if existingLaunch == result['name']:

                    if result['vidURLs']:
                        stream_url = result['vidURLs'][0]['url']
                    else:
                        stream_url = None

                    #update if match is found.
                    print("Updating : " + result['name'])
                    launchObject = UpcomingLaunch.objects.filter(name=result['name'])

                    launchObject.update(launch_provider=result['launch_service_provider']['name'])
                    launchObject.update(launch_location=result['pad']['location']['name'])
                    launchObject.update(launch_date_time=result['window_start'])
                    launchObject.update(launch_status=result['status']['abbrev'])
                    launchObject.update(stream_url=stream_url)
                    launchObject.update(image=result['image'])
            
            # Create new objects from information we do not have.
            for newLaunch in results:
                if newLaunch['name'] not in existingNames:

                    if newLaunch['vidURLs']:
                        stream_url = newLaunch['vidURLs'][0]['url']
                    else:
                        stream_url = None

                    print("Adding : " + newLaunch['name'])

                    UpcomingLaunch.objects.create(
                        name = newLaunch['name'],
                        launch_provider = newLaunch['launch_service_provider']['name'],
                        launch_location = newLaunch['pad']['location']['name'],
                        launch_date_time = newLaunch['window_start'],
                        launch_status = newLaunch['status']['abbrev'],
                        stream_url = stream_url,
                        image = newLaunch['image']
                    )

    else:
        # Initially populate the database with first api call information.
        for result in results:
            if result['vidURLs']:
                stream_url = result['vidURLs'][0]['url']
            else:
                stream_url = None

            print("Adding : " + result['name'])

            UpcomingLaunch.objects.create(
                name = result['name'],
                launch_provider = result['launch_service_provider']['name'],
                launch_location = result['pad']['location']['name'],
                launch_date_time = result['window_start'],
                launch_status = result['status']['abbrev'],
                stream_url = stream_url,
                image = result['image']
            )

    return resultCount

def home_get_APOD_view(request):

    NASA_KEY = config('NASA_KEY')

    url = 'https://api.nasa.gov/planetary/apod?api_key='+NASA_KEY

    response = requests.get(url).json()

    context = {
        "jsonResponse": response
    }

    return render(request, 'home.html', context)

def launch_event_view(request):
    # Info needed for both endpoint requests.
    LAUNCHLIBRARY2_KEY = config("LAUNCHLIBRARY2_KEY")

    headers = {
        "Authorization": f"Token {LAUNCHLIBRARY2_KEY}"
        }

    # Where you will be working with the data that is added and updated.

    results = UpcomingLaunch.objects.all().order_by('id')
    resultCount = results.count()

    # API request for any launch search.
    # response variable == to jsonResponse in launch/events template.
    if request.method == "POST":

        searchResults = []

        form = LaunchForm(request.POST)
        if form.is_valid():
            launch = form.cleaned_data['launch_name']

            url = 'https://ll.thespacedevs.com/2.2.0/launch/?mode=detailed&search=' + launch

            r = requests.get(url, headers=headers)
            
            if r.status_code == 200:
                jsonResponse = r.json()

                for result in jsonResponse['results']:

                    searchResults.append(result)
                    
                    pprint(jsonResponse)
                    print(r.request.headers)
                    print(r)

                    if result['vidURLs']:

                        if 'url' in result['vidURLs'][0]:
                            streamURL = result['vidURLs'][0].get('url')
                            pprint(streamURL)

                            context = {
                                'form': form,
                                'jsonResponse': searchResults,
                                'streamURL': streamURL
                            }
                    else:

                        context = {
                            'form': form,
                            'jsonResponse': searchResults,
                        }

                return render(request, 'launches-events.html', context)
            elif r.status_code == 429:
                print(r.request.headers)
                print(r)
                return HttpResponse("Too many requests to LL2 Api.")
            else:
                print(r)
                return HttpResponse("No record of the requested Astronaut.")
        else:
            print(form)
            return HttpResponse("Form is invalid.")

    else:
        form = LaunchForm()

    paginator = Paginator(results, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Context for Default launch display.
    context = {
        'form': form,
        'resultCount': resultCount,
        'page_obj': page_obj,
    }
    
    return render(request, 'launches-events.html', context)

def astronaut_view(request):

    # API request for astronaut search.
    # response variable == to jsonResponse in astronauts template.
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
                }

                return render(request, 'astronauts.html', context)
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

    return render(request, 'astronauts.html', {'form': form})

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
    # response variable == to jsonResponse2 in ISS template.
    url = 'http://api.open-notify.org/astros.json'

    jsonResponse = requests.get(url).json()

    return render(request, 'iss-location-astronauts.html', {"jsonResponse": jsonResponse})


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

schedule.every(15).minutes.at(":00").do(delete_update_create_upcoming_launches)

start_run_continuously = run_continuously()