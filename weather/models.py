from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Weather(models.Model):
    city = models.CharField(max_length=100)
    time = models.DateTimeField()
    title = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    wind_dir = models.CharField(max_length=50)
