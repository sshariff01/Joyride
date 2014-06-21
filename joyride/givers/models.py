from django.db import models

# Create your models here.
class Giver(models.Model):
    fb_id = models.IntegerField(default=0)
    lng_start = models.IntegerField(default=0)
    lat_start = models.IntegerField(default=0)
    lng_end = models.IntegerField(default=0)
    lat_end = models.IntegerField(default=0)
    