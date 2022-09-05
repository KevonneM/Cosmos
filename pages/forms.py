# Create your form for users space queries here.
from django import forms

class AgencyForm(forms.Form):
    agency_name = forms.CharField(label='agency_name', max_length=50)

class AstronautForm(forms.Form):
    astronaut_name = forms.CharField(label='astronaut_name', max_length=50)

class LaunchForm(forms.Form):
    launch_name = forms.CharField(label='launch_name', max_length=50)