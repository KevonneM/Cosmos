# Create your form for users space queries here.
from django import forms

class AgencyForm(forms.Form):
    agency_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Agency Name', 'style': 'width: 300px;', 'class': 'form-control'}),label='', max_length=50)

class AstronautForm(forms.Form):
    astronaut_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name/Association/country', 'style': 'width: 300px;', 'class': 'form-control'}),label='', max_length=50)

class LaunchForm(forms.Form):
    launch_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Launch-Name or Association', 'style': 'width: 300px;', 'class': 'form-control'}),label='', max_length=50)