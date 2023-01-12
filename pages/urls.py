from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home_get_APOD_view, name='home'),
    path('launches-events/', views.launch_event_view, name='launches-events'),
    path('astronauts/', views.astronaut_view, name='astronauts'),
    path('agencies/', views.agency_view, name='agencies'),
    path('iss-location-info/', views.iss_location_info_view, name='iss-location-info'),
]