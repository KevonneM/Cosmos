# Create your form for users space queries here.
from django import forms
from django.forms import fields

class AgencyForm(forms.Form):
    agency_name = forms.CharField(label='agency_name', max_length=50)