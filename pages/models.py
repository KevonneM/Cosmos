from django.db import models

# Create your models here.

class UpcomingLaunch(models.Model):

    name = models.CharField(max_length=75)
    launch_provider = models.CharField(max_length=75)
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