from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class Place(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    address_city = models.CharField(max_length=100, blank=True, null=True)
    address_province = models.CharField(max_length=100, blank=True, null=True)
    address_country = models.CharField(max_length=100, default='Argentina')
    telephone_1 = models.CharField(max_length=100, blank=True, null=True)
    telephone_2 = models.CharField(max_length=100, blank=True, null=True)
    telephone_3 = models.CharField(max_length=100, blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

@python_2_unicode_compatible  # only if you need to support Python 2
class Evento(models.Model):
    EVENTOS_FOLDER_FORMAT = 'eventos/static/eventos/eventos_pics/%Y_%m/%d/%H_%M_%S/'
    name = models.CharField(max_length=200)
    pub_date = models.DateField(default=datetime.datetime.now)
    event_date = models.DateField()
    time_from = models.TimeField()
    duration = models.DurationField()
    recurrent_definition = models.CharField(max_length=20, blank=True)
    place = models.ForeignKey(Place, blank=True, null=True)
    approved = models.BooleanField(default=False)
    #the stupid strfmt is to prevent name clashes (just in case)
    image_1 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    image_2 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    image_3 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    image_4 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    image_5 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
