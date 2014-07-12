from django.db import models

# Create your models here.
class Giver(models.Model):
    fb_id = models.TextField(default=0)
    lng_start = models.TextField(default=0)
    lat_start = models.TextField(default=0)
    lng_end = models.TextField(default=0)
    lat_end = models.TextField(default=0)
    