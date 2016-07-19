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
    address_line_2 = models.CharField(max_length=100)
    address_city = models.CharField(max_length=100)
    address_province = models.CharField(max_length=100)
    address_country = models.CharField(max_length=100)
    telephone_1 = models.CharField(max_length=100)
    telephone_2 = models.CharField(max_length=100)
    telephone_3 = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    notes = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name

@python_2_unicode_compatible  # only if you need to support Python 2
class Evento(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateField(default=datetime.datetime.now)
    date = models.DateField()
    time_from = models.TimeField()
    duration = models.DurationField()
    recurrent_definition = models.CharField(max_length=20, blank=True)
    place = models.ForeignKey(Place, blank=True, null=True)
    
    def __str__(self):
        return self.name

