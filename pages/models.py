from django.db import models

# Create your models here.

class UpcomingLaunch(models.Model):

    name = models.CharField(max_length=75)
    launch_provider = models.CharField(max_length=75)
    launch_provider_abbrev = models.CharField(max_length=75)
    launch_location = models.CharField(max_length=75)
    launch_date_time = models.CharField(max_length=75)
    launch_status = models.CharField(max_length=75)
    stream_url = models.URLField(blank=True, null=True, max_length=200)
    image = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        # shows an actual string representation of the rocket name.
        return self.name
    class Meta:
        verbose_name_plural = "Launches"

class Astronaut(models.Model):

    name = models.CharField(max_length=75)
    nationality = models.CharField(max_length=75)
    agency = models.CharField(blank=True, null=True, max_length=75)
    status = models.CharField(max_length=75)
    bio = models.TextField()
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        # shows an actual string representation of the astronauts name.
        return self.name

class Agency(models.Model):

    name = models.CharField(max_length=75)
    featured = models.BooleanField()
    administrator = models.CharField(max_length=75, null=True)
    type = models.CharField(max_length=75, null=True)
    country_code = models.CharField(max_length=25)
    abbreviation = models.CharField(max_length=25)
    description = models.TextField(null=True)
    founding_year = models.CharField(max_length=4, null=True)
    launchers = models.CharField(max_length=75, null=True)
    spacecrafts = models.CharField(max_length=75, null=True)
    total_launches = models.IntegerField()
    successful_launches = models.IntegerField()
    consecutive_successful_launches = models.IntegerField()
    failed_launches = models.IntegerField()
    pending_launches = models.IntegerField()
    home_webpage = models.URLField(null=True)
    wiki_page = models.URLField(null=True)
    nation_image = models.ImageField(null=True)
    logo = models.ImageField(null=True)

    def __str__(self):
        # shows an actual string representation of the astronauts name.
        return self.name
    class Meta:
        verbose_name_plural = "Agencies"