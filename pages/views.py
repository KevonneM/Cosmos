from django.shortcuts import render
from django.http import HttpResponse

from django.core.paginator import Paginator

import requests
import schedule
import threading
import time
from decouple import config
from pages.models import UpcomingLaunch, Astronaut, Agency

from .forms import AgencyForm, AstronautForm, LaunchForm

def delete_update_create_upcoming_launches():
    # Info needed endpoint requests.
    LAUNCHLIBRARY2_KEY = config("LAUNCHLIBRARY2_KEY")

    headers = {
        "Authorization": f"Token {LAUNCHLIBRARY2_KEY}"
        }

    # API request for upcoming launches display.
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
                # Delete
                UpcomingLaunch.objects.get(name=existingLaunch).delete()
                print(f"Removed : {existingLaunch}")
                
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
                    launchObject = UpcomingLaunch.objects.filter(name=result['name'])

                    launchObject.update(launch_provider=result['launch_service_provider']['name'])
                    launchObject.update(launch_location=result['pad']['location']['name'])
                    launchObject.update(launch_date_time=result['window_start'])
                    launchObject.update(launch_status=result['status']['abbrev'])
                    launchObject.update(stream_url=stream_url)
                    launchObject.update(image=result['image'])

                    print(f"Updated : {result['name']}")
            
        # Create new objects from information we do not have.
        for newLaunch in results:
            if newLaunch['name'] not in existingNames:

                if newLaunch['vidURLs']:
                    stream_url = newLaunch['vidURLs'][0]['url']
                else:
                    stream_url = None

                UpcomingLaunch.objects.create(
                    name = newLaunch['name'],
                    launch_provider = newLaunch['launch_service_provider']['name'],
                    launch_location = newLaunch['pad']['location']['name'],
                    launch_date_time = newLaunch['window_start'],
                    launch_status = newLaunch['status']['abbrev'],
                    stream_url = stream_url,
                    image = newLaunch['image']
                )

                print(f"Added : {newLaunch['name']}")

    else:
        # Initially populate the database with first API call's information.
        for result in results:
            if result['vidURLs']:
                stream_url = result['vidURLs'][0]['url']
            else:
                stream_url = None

            UpcomingLaunch.objects.create(
                name = result['name'],
                launch_provider = result['launch_service_provider']['name'],
                launch_location = result['pad']['location']['name'],
                launch_date_time = result['window_start'],
                launch_status = result['status']['abbrev'],
                stream_url = stream_url,
                image = result['image']
            )

            print(f"Added : {result['name']}")

def delete_update_create_astronauts():
    # Info needed for endpoint requests.
    LAUNCHLIBRARY2_KEY = config("LAUNCHLIBRARY2_KEY")

    headers = {
        "Authorization": f"Token {LAUNCHLIBRARY2_KEY}"
        }

    # API request for astronauts display.
    # gather all results into a list to paginate from db.
    results = []
    limit = 100
    offset = 0

    while True:
        url = f'https://ll.thespacedevs.com/2.2.0/astronaut/?mode=detailed&limit={limit}&offset={offset}'
        print("requesting", url)
        astronautResponse = requests.get(url, headers=headers)
        astronautData = astronautResponse.json()

        results.extend(astronautData['results'])

        # Breaks out of loop if all results are aquired.
        if len(results) == astronautData['count']:
            break
        else:
            offset = offset + 100

    # Incoming data will be used to update the existing database.
    existingNames = []
    resultNames = []
    existingData = Astronaut.objects.all()

    for existingObject in existingData:
        existingNames.append(existingObject.name)

    for resultObject in results:
        resultNames.append(resultObject['name'])

    if existingData.exists():
        # A check to remove astronauts if they were removed from the api db.
        for existingAstronaut in existingNames:
            if existingAstronaut not in resultNames:
                # Delete
                Astronaut.objects.get(name=existingAstronaut).delete()
                print(f"Removed : {existingAstronaut}")

        # A check to update existing db if astronauts information has changed.
        # A check to populate existind db with new Astronauts.
        for existingAstronaut in existingNames:
            for result in results:

                if existingAstronaut == result['name']:

                    # Check for objects with null value for agency.
                    # Ex: Gregory Olsen
                    if result['agency'] == None:
                        agency = None
                    else:
                        agency = result['agency']['name']
                    # Check for objects with null value for DOB.
                    # Ex: Little Earth
                    if result['date_of_birth'] == None:
                        date_of_birth = None
                    else:
                        date_of_birth = result['date_of_birth']
                    # Check for objects with null value for DOD.
                    # Ex: Little Earth
                    if result['date_of_death'] == None:
                        date_of_death = None
                    else:
                        date_of_death = result['date_of_death']
                    # Check for objects with null value for Age.
                    # Ex: Little Earth
                    if result['age'] == None:
                        age = None
                    else:
                        age = result['age']

                    # Update if a match is found.
                    astronautObject = Astronaut.objects.filter(name=result['name'])

                    astronautObject.update(nationality=result['nationality'])
                    astronautObject.update(agency=agency)
                    astronautObject.update(status=result['status']['name'])
                    astronautObject.update(bio=result['bio'])
                    astronautObject.update(date_of_birth=date_of_birth)
                    astronautObject.update(date_of_death=date_of_death)
                    astronautObject.update(age=age)
                    astronautObject.update(image=result['profile_image'])

                    print(f"Updated : {result['name']}")

        # Create new objects from information we do not have.
        for newAstronaut in results:
            if newAstronaut['name'] not in existingNames:

                # Check for objects with null value for agency.
                # Ex: Gregory Olsen
                if result['agency'] == None:
                    agency = None
                else:
                    agency = result['agency']['name']
                # Check for objects with null value for DOB.
                # Ex: Little Earth
                if result['date_of_birth'] == None:
                    date_of_birth = None
                else:
                    date_of_birth = result['date_of_birth']
                # Check for objects with null value for DOD.
                # Ex: Little Earth
                if result['date_of_death'] == None:
                    date_of_death = None
                else:
                    date_of_death = result['date_of_death']
                # Check for objects with null value for Age.
                # Ex: Little Earth
                if result['age'] == None:
                    age = None
                else:
                    age = result['age']

                Astronaut.objects.create(
                    name=newAstronaut['name'],
                    nationality=newAstronaut['nationality'],
                    agency=agency,
                    status=newAstronaut['status']['name'],
                    bio=newAstronaut['bio'],
                    date_of_birth=date_of_birth,
                    date_of_death=date_of_death,
                    age=age,
                    image=newAstronaut['profile_image'],
                )

                print(f"Added : {newAstronaut['name']}")
    else:
        # Initially populate the database with the first API call's information.
        for result in results:

            # Check for objects with null value for agency.
            # Ex: Gregory Olsen
            if result['agency'] == None:
                agency = None
            else:
                agency = result['agency']['name']
            # Check for objects with null value for DOB.
            # Ex: Little Earth
            if result['date_of_birth'] == None:
                date_of_birth = None
            else:
                date_of_birth = result['date_of_birth']
            # Check for objects with null value for DOD.
            # Ex: Little Earth
            if result['date_of_death'] == None:
                date_of_death = None
            else:
                date_of_death = result['date_of_death']
            # Check for objects with null value for Age.
            # Ex: Little Earth
            if result['age'] == None:
                age = None
            else:
                age = result['age']

            Astronaut.objects.create(
                name=result['name'],
                nationality=result['nationality'],
                agency=agency,
                status=result['status']['name'],
                bio=result['bio'],
                date_of_birth=date_of_birth,
                date_of_death=date_of_death,
                age=age,
                image=result['profile_image'],
            )

            print(f"Added : {result['name']}")

def delete_update_create_agency():
    # Info needed endpoint requests.
    LAUNCHLIBRARY2_KEY = config("LAUNCHLIBRARY2_KEY")

    headers = {
        "Authorization": f"Token {LAUNCHLIBRARY2_KEY}"
        }

    # API request for upcoming launches display.
    # gather all results into a list to paginate.
    results = []
    limit = 100
    offset = 0

    while True:
        url = f'https://ll.thespacedevs.com/2.2.0/agencies/?mode=detailed&limit={limit}&offset={offset}'
        print("requesting ", url)
        launchResponse = requests.get(url, headers=headers)
        launchData = launchResponse.json()

        results.extend(launchData['results'])

        # Breaks out of loop if all results are acquired.
        if len(results) == launchData['count']:
            break
        else:
            offset = offset + 100

    # Incoming data will be used to update the existing database.
    existingNames = []
    resultNames = []
    existingData = Agency.objects.all()

    for existingObject in existingData:
        existingNames.append(existingObject.name)

    for resultObject in results:
        resultNames.append(resultObject['name'])

    if existingData.exists():
        # A check to delete launches that are no longer upcoming.
        for existingAgency in existingNames:
            if existingAgency not in resultNames:
                # Delete
                Agency.objects.get(name=existingAgency).delete()
                print(f"Removed : {existingAgency}")

        # A check to update existing db if Agency's information has changed.
        # A check to populate existing db with new Agencies.
        for existingAgency in existingNames:
            for result in results:

                if existingAgency == result['name']:

                    # Checkts to update objects with null values.
                    # Ex: CSIRO
                    if result['administrator'] == None:
                        administrator = None
                    else:
                        administrator = result['administrator']

                    if result['type'] == None:
                        agency_type = None
                    else:
                        agency_type = result['type']

                    if result['description'] == None:
                        description = None
                    else:
                        description = result['description']

                    if result['founding_year'] == None:
                        founding_year = None
                    else:
                        founding_year = result['founding_year']

                    if result['launchers'] == "":
                        launchers = None
                    else:
                        launchers = result['launchers']

                    if result['spacecraft'] == "":
                        spacecrafts = None
                    else:
                        spacecrafts = result['spacecraft']

                    if result['info_url'] == None:
                        home_webpage = None
                    else:
                        home_webpage = result['info_url']

                    if result['wiki_url'] == None:
                        wiki_page = None
                    else:
                        wiki_page = result['wiki_url']

                    if result['nation_url'] == None:
                        nation_image = None
                    else:
                        nation_image = result['nation_url']

                    if result['logo_url'] == None:
                        logo = None
                    else:
                        logo = result['logo_url']

                    #update if match is found.
                    agencyObject = Agency.objects.filter(name=result['name'])

                    agencyObject.update(administrator=administrator)
                    agencyObject.update(type=agency_type)
                    agencyObject.update(country_code=result['country_code'])
                    agencyObject.update(abbreviation=result['abbrev'])
                    agencyObject.update(description=description)
                    agencyObject.update(founding_year=founding_year)
                    agencyObject.update(launchers=launchers)
                    agencyObject.update(spacecrafts=spacecrafts)
                    agencyObject.update(total_launches=result['total_launch_count'])
                    agencyObject.update(successful_launches=result['successful_launches'])
                    agencyObject.update(consecutive_successful_launches=result['consecutive_successful_launches'])
                    agencyObject.update(failed_launches=result['failed_launches'])
                    agencyObject.update(pending_launches=result['pending_launches'])
                    agencyObject.update(home_webpage=home_webpage)
                    agencyObject.update(wiki_page=wiki_page)
                    agencyObject.update(nation_image=nation_image)
                    agencyObject.update(logo=logo)

                    print(f"Updated : {result['name']}")

        # Create new objects from information we do not have.
        for newAgency in results:
            if newAgency['name'] not in existingNames:

                # Checks to update objects with null values.
                # Ex: CSIRO
                if result['administrator'] == None:
                    administrator = None
                else:
                    administrator = result['administrator']

                if result['type'] == None:
                    agency_type = None
                else:
                    agency_type = result['type']

                if result['description'] == None:
                    description = None
                else:
                    description = result['description']

                if result['founding_year'] == None:
                    founding_year = None
                else:
                    founding_year = result['founding_year']

                if result['launchers'] == "":
                    launchers = None
                else:
                    launchers = result['launchers']

                if result['spacecraft'] == "":
                    spacecrafts = None
                else:
                    spacecrafts = result['spacecraft']

                if result['info_url'] == None:
                    home_webpage = None
                else:
                    home_webpage = result['info_url']

                if result['wiki_url'] == None:
                    wiki_page = None
                else:
                    wiki_page = result['wiki_url']

                if result['nation_url'] == None:
                    nation_image = None
                else:
                    nation_image = result['nation_url']

                if result['logo_url'] == None:
                    logo = None
                else:
                    logo = result['logo_url']

                Agency.objects.create(
                    name=newAgency['name'],
                    administrator=administrator,
                    type=agency_type,
                    country_code=newAgency['country_code'],
                    abbreviation=newAgency['abbrev'],
                    description=description,
                    founding_year=founding_year,
                    launchers=launchers,
                    spacecrafts=spacecrafts,
                    total_launches=newAgency['total_launch_count'],
                    successful_launches=newAgency['successful_launches'],
                    consecutive_successful_launches=newAgency['consecutive_successful_launches'],
                    failed_launches=newAgency['failed_launches'],
                    pending_launches=newAgency['pending_launches'],
                    home_webpage=home_webpage,
                    wiki_page=wiki_page,
                    nation_image=nation_image,
                    logo=logo
                )

                print(f"Added : {newAgency['name']}")

    else:
        # Initially populate the database with the first API call's information.
        for result in results:
            # Checks to update objects with null values.
            # Ex: CSIRO
            if result['administrator'] == None:
                administrator = None
            else:
                administrator = result['administrator']

            if result['type'] == None:
                agency_type = None
            else:
                agency_type = result['type']

            if result['description'] == None:
                description = None
            else:
                description = result['description']

            if result['founding_year'] == None:
                founding_year = None
            else:
                founding_year = result['founding_year']

            if result['launchers'] == "":
                launchers = None
            else:
                launchers = result['launchers']

            if result['spacecraft'] == "":
                spacecrafts = None
            else:
                spacecrafts = result['spacecraft']

            if result['info_url'] == None:
                home_webpage = None
            else:
                home_webpage = result['info_url']

            if result['wiki_url'] == None:
                wiki_page = None
            else:
                wiki_page = result['wiki_url']

            if result['nation_url'] == None:
                nation_image = None
            else:
                nation_image = result['nation_url']

            if result['logo_url'] == None:
                logo = None
            else:
                logo = result['logo_url']

            Agency.objects.create(
                name=result['name'],
                administrator=administrator,
                type=agency_type,
                country_code=result['country_code'],
                abbreviation=result['abbrev'],
                description=description,
                founding_year=founding_year,
                launchers=launchers,
                spacecrafts=spacecrafts,
                total_launches=result['total_launch_count'],
                successful_launches=result['successful_launches'],
                consecutive_successful_launches=result['consecutive_successful_launches'],
                failed_launches=result['failed_launches'],
                pending_launches=result['pending_launches'],
                home_webpage=home_webpage,
                wiki_page=wiki_page,
                nation_image=nation_image,
                logo=logo
            )

            print(f"Added: {result['name']}")

def home_get_APOD_view(request):

    NASA_KEY = config('NASA_KEY')

    url = 'https://api.nasa.gov/planetary/apod?api_key='+NASA_KEY

    response = requests.get(url).json()

    context = {
        "jsonResponse": response
    }

    return render(request, 'home.html', context)

def launch_event_view(request):
    # Info needed for endpoint requests.
    LAUNCHLIBRARY2_KEY = config("LAUNCHLIBRARY2_KEY")

    headers = {
        "Authorization": f"Token {LAUNCHLIBRARY2_KEY}"
        }

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
                print(r.request.headers)

                for result in jsonResponse['results']:

                    searchResults.append(result)

                context = {
                    'form': form,
                    'jsonResponse': searchResults,
                }

                return render(request, 'launches-events.html', context)
            elif r.status_code == 429:
                return HttpResponse("Too many requests to LL2 Api.")
            else:
                return HttpResponse("No record of the requested Astronaut.")
        else:
            return HttpResponse("Form is invalid.")

    else:
        form = LaunchForm()

    # Where you will be working with the data that is added and updated.
    results = UpcomingLaunch.objects.all().order_by('id')
    resultCount = results.count()

    paginator = Paginator(results, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Context for Default launch display.
    context = {
        'form': form,
        'resultCount': resultCount,
        'page_obj': page_obj
    }
    
    return render(request, 'launches-events.html', context)

def astronaut_view(request):
    # Info needed for endpoint requests.
    LAUNCHLIBRARY2_KEY = config("LAUNCHLIBRARY2_KEY")

    headers = {
        "Accepts":"application/json",
        "Content-Type": "application/json",
        "Authorization": f"Token {LAUNCHLIBRARY2_KEY}"
        }

    request.META['HTTP_Authorization'] = "Token " + LAUNCHLIBRARY2_KEY

    # API request for any astronaut search.
    # response variable == to jsonResponse in astronauts template.
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

    # Where you will be working with the data that is added and updated.
    results = Astronaut.objects.all().order_by('id')
    resultCount = results.count()

    paginator = Paginator(results, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Context for Default Astronaut display.
    context = {
        'form': form,
        'resultCount': resultCount,
        'page_obj': page_obj
    }

    return render(request, 'astronauts.html', context)

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

# A thread/(set of instructions) awaiting the completion of a few tasks.
schedule.every(5).minutes.at(":00").do(delete_update_create_upcoming_launches)
schedule.every(5).minutes.at(':00').do(delete_update_create_agency)
schedule.every(5).minutes.at(':00').do(delete_update_create_astronauts)

start_run_continuously = run_continuously()